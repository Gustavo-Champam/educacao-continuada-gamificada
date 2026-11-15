package br.com.educacao.gamificada.af;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.rabbit.connection.CorrelationData;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import java.util.UUID;

class TreinamentosTest {
 JdbcTemplate db;RabbitTemplate rabbit;Treinamentos service;
 @BeforeEach void setup(){
  db=new JdbcTemplate(new DriverManagerDataSource("jdbc:h2:mem:"+UUID.randomUUID()+";DB_CLOSE_DELAY=-1","sa",""));
  rabbit=mock(RabbitTemplate.class);service=new Treinamentos(db,rabbit,new ObjectMapper());
 }
 @Test void aceitaComBrokerIndisponivelEReenviaDepois(){
  var result=service.criar();String id=(String)result.get("job_id");verifyNoInteractions(rabbit);
  doThrow(new RuntimeException("broker offline")).when(rabbit).send(eq(""),eq("ml.training.requests"),any(Message.class),any(CorrelationData.class));
  service.publicar();assertEquals(false,service.consultar(id).get("PUBLISHED"));
  doAnswer(inv->{CorrelationData c=inv.getArgument(3);c.getFuture().complete(new CorrelationData.Confirm(true,null));return null;})
   .when(rabbit).send(eq(""),eq("ml.training.requests"),any(Message.class),any(CorrelationData.class));
  service.publicar();assertEquals(true,service.consultar(id).get("PUBLISHED"));assertEquals("queued",service.consultar(id).get("STATUS"));
 }
 @Test void resultadoTerminalNaoRegrideComEventoAtrasado()throws Exception{
  String id=(String)service.criar().get("job_id");
  for(String status:new String[]{"completed","running","failed"})service.resultado(new Message(("{\"job_id\":\""+id+"\",\"status\":\""+status+"\"}").getBytes()));
  assertEquals("completed",service.consultar(id).get("STATUS"));
 }
 @Test void consultaInexistenteRetorna404(){
  var e=assertThrows(org.springframework.web.server.ResponseStatusException.class,()->service.consultar("ausente"));assertEquals(404,e.getStatusCode().value());
 }
}
