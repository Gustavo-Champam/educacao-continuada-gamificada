package br.com.educacao.gamificada.af;
import br.com.educacao.gamificada.service.AlunoService;
import br.com.educacao.gamificada.dto.AlunoResponse;
import br.com.educacao.gamificada.domain.Plano;
import org.junit.jupiter.api.*;
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
class OrientacaoControllerTest {
 HttpServer server;OrientacaoController controller;AlunoService alunos;int status=200;String requestBody;
 @BeforeEach void setup()throws Exception{
  alunos=mock(AlunoService.class);when(alunos.buscar(1L)).thenReturn(new AlunoResponse(1L,"Teste",Plano.BASICO,3,0,0));
  server=HttpServer.create(new InetSocketAddress("127.0.0.1",0),0);
  server.createContext("/",e->{requestBody=new String(e.getRequestBody().readAllBytes());byte[] b="{\"profile\":\"INICIANTE\",\"resposta\":\"DOC-01\"}".getBytes();e.getResponseHeaders().add("Content-Type","application/json");e.sendResponseHeaders(status,b.length);e.getResponseBody().write(b);e.close();});server.start();
  String url="http://127.0.0.1:"+server.getAddress().getPort();controller=new OrientacaoController(alunos,url,url);
 }
 @AfterEach void stop(){server.stop(0);}
 @Test void usaCursosReaisDaAc1(){
  var result=controller.classificar(1L,new OrientacaoController.Avaliacao(12,80,6,75,75));assertEquals("INICIANTE",result.get("profile").asText());assertTrue(requestBody.contains("\"completed_courses\":3"));
 }
 @Test void recomendacaoEAgenteExigemAlunoEConsentimento()throws Exception{
  var p=new OrientacaoController.Pergunta("Java REST","iniciante",true);assertEquals("DOC-01",controller.recomendar(1L,p).get("resposta").asText());assertNotNull(controller.agente(1L,p));
  var enviado=new com.fasterxml.jackson.databind.ObjectMapper().readTree(requestBody);
  assertEquals("BASICO",enviado.path("progresso").path("plano").asText());
  assertEquals(3,enviado.path("progresso").path("cursosConcluidos").asInt());
  assertFalse(requestBody.contains("Teste"));assertFalse(enviado.path("progresso").has("id"));
  clearInvocations(alunos);
  var e=assertThrows(org.springframework.web.server.ResponseStatusException.class,()->controller.agente(1L,new OrientacaoController.Pergunta("Java","iniciante",false)));assertEquals(403,e.getStatusCode().value());
  verifyNoInteractions(alunos);
 }
 @Test void entradaInvalidaRetorna400SemConsultarAlunoOuIa()throws Exception{
  var http=org.springframework.test.web.servlet.setup.MockMvcBuilders.standaloneSetup(controller).build();
  for(String corpo:java.util.List.of(
   "{\"pergunta\":\"Oi\",\"perfil\":\"iniciante\"}",
   "{\"pergunta\":\"Java REST\",\"perfil\":\"administrador\"}")){
   http.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post("/api/af/alunos/1/recomendacao")
    .contentType("application/json").content(corpo))
    .andExpect(org.springframework.test.web.servlet.result.MockMvcResultMatchers.status().isBadRequest());
  }
  verifyNoInteractions(alunos);assertNull(requestBody);
 }
 @Test void falhaDeIaNaoInventaResultado(){status=503;var e=assertThrows(org.springframework.web.server.ResponseStatusException.class,()->controller.recomendar(1L,new OrientacaoController.Pergunta("Java","iniciante",false)));assertEquals(503,e.getStatusCode().value());}
}
