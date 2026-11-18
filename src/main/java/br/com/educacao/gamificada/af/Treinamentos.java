package br.com.educacao.gamificada.af;
import java.util.*;
import org.springframework.context.annotation.*;
import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.rabbit.connection.CorrelationData;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.scheduling.annotation.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.*;
import org.springframework.web.server.ResponseStatusException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.concurrent.TimeUnit;

@Configuration @Profile("af") @EnableScheduling
class FilasAf {
 @Bean Declarables filas(){return new Declarables(new org.springframework.amqp.core.Queue("ml.training.requests",true),new org.springframework.amqp.core.Queue("ml.training.results",true));}
}
@RestController @Profile("af") @RequestMapping("/api/af/treinamentos")
public class Treinamentos {
 private final JdbcTemplate db;private final RabbitTemplate rabbit;private final ObjectMapper json;
 public Treinamentos(JdbcTemplate db,RabbitTemplate rabbit,ObjectMapper json){
  this.db=db;this.rabbit=rabbit;this.json=json;
  db.execute("create table if not exists af_training_job (id varchar(36) primary key, status varchar(20) not null, published boolean not null, result_text text)");
 }
 @PostMapping @ResponseStatus(HttpStatus.ACCEPTED)
 public Map<String,Object> criar(){
  String id=UUID.randomUUID().toString();
  // A própria linha do job é a outbox: uma única inserção durável, sem depender de ML ou broker.
  db.update("insert into af_training_job (id,status,published) values (?,?,false)",id,"received");
  return Map.of("job_id",id,"status","received","consulta","/api/af/treinamentos/"+id);
 }
 @GetMapping("/{id}") public Map<String,Object> consultar(@PathVariable String id){
  var rows=db.queryForList("select id,status,published,result_text from af_training_job where id=?",id);
  if(rows.isEmpty())throw new ResponseStatusException(HttpStatus.NOT_FOUND,"Treinamento nao encontrado");return rows.get(0);
 }
 @Scheduled(fixedDelayString="${af.outbox.delay:5000}")
 public void publicar(){
  for(String id:db.queryForList("select id from af_training_job where published=false",String.class)){
   try{
    var correlation=new CorrelationData(UUID.randomUUID().toString());
    byte[] body=json.writeValueAsBytes(Map.of("job_id",id,"seed",42));
    var msg=MessageBuilder.withBody(body).setContentType("application/json").setDeliveryMode(MessageDeliveryMode.PERSISTENT).build();
    rabbit.setMandatory(true);rabbit.send("","ml.training.requests",msg,correlation);
    var confirm=correlation.getFuture().get(3,TimeUnit.SECONDS);
    if(confirm.isAck() && correlation.getReturned()==null)
      db.update("update af_training_job set published=true,status=case when status='received' then 'queued' else status end where id=?",id);
   }catch(Exception ex){break;} // Registro permanece pendente para a próxima tentativa.
  }
 }
 @RabbitListener(queues="ml.training.results")
 public void resultado(Message message)throws Exception{
  var event=json.readTree(message.getBody());String id=event.path("job_id").asText(),status=event.path("status").asText();
  if(!Set.of("running","completed","failed").contains(status))return;
  // Reentregas e mensagens running atrasadas não substituem um estado terminal.
  db.update("update af_training_job set status=?,result_text=? where id=? and status not in ('completed','failed')",status,json.writeValueAsString(event),id);
 }
}
