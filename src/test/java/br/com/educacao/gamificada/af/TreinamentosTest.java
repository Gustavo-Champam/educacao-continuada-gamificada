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
 @Test void declaraFilasDuraveisEIgnoraStatusInvalido()throws Exception{
  assertEquals(2,new FilasAf().filas().getDeclarables().size());
  String id=(String)service.criar().get("job_id");service.resultado(new Message(("{\"job_id\":\""+id+"\",\"status\":\"invalido\"}").getBytes()));assertEquals("received",service.consultar(id).get("STATUS"));
 }
 @Test void naoMarcaPublicadoSeBrokerNegaOuDevolve(){
  String id=(String)service.criar().get("job_id");
  doAnswer(inv->{CorrelationData c=inv.getArgument(3);c.getFuture().complete(new CorrelationData.Confirm(false,"nack"));return null;})
   .when(rabbit).send(eq(""),eq("ml.training.requests"),any(Message.class),any(CorrelationData.class));
  service.publicar();assertEquals(false,service.consultar(id).get("PUBLISHED"));
  doAnswer(inv->{CorrelationData c=inv.getArgument(3);c.setReturned(new org.springframework.amqp.core.ReturnedMessage(inv.getArgument(2),312,"sem rota","","ml.training.requests"));c.getFuture().complete(new CorrelationData.Confirm(true,null));return null;})
   .when(rabbit).send(eq(""),eq("ml.training.requests"),any(Message.class),any(CorrelationData.class));
  service.publicar();assertEquals(false,service.consultar(id).get("PUBLISHED"));
 }
}
