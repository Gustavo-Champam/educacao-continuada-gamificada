package br.com.educacao.gamificada.af;
import org.junit.jupiter.api.*;
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
class AvaliacaoControllerTest {
 HttpServer server;AvaliacaoController c;int status=200;
 @BeforeEach void setup()throws Exception{server=HttpServer.create(new InetSocketAddress("127.0.0.1",0),0);server.createContext("/",e->{assertEquals("token-teste",e.getRequestHeaders().getFirst("X-AF-Service"));e.getRequestBody().readAllBytes();byte[] b="{\"status\":\"running\"}".getBytes();e.getResponseHeaders().add("Content-Type","application/json");e.sendResponseHeaders(status,b.length);e.getResponseBody().write(b);e.close();});server.start();c=new AvaliacaoController("http://127.0.0.1:"+server.getAddress().getPort(),"token-teste");}
 @AfterEach void stop(){server.stop(0);}
 @Test void encaminhaEConsulta(){for(String ref:new String[]{null,"Java REST"})assertEquals("running",c.iniciar(new AvaliacaoController.Pedido("Java?","DOC-01",List.of("Java REST"),ref)).get("status").asText());assertEquals("running",c.consultar(UUID.randomUUID().toString()).get("status").asText());assertThrows(IllegalArgumentException.class,()->c.consultar("../segredo"));}
 @Test void indisponibilidadeExplicita(){status=503;assertThrows(org.springframework.web.server.ResponseStatusException.class,()->c.iniciar(new AvaliacaoController.Pedido("Java?","DOC-01",List.of("Java REST"),"")));assertThrows(org.springframework.web.server.ResponseStatusException.class,()->c.consultar(UUID.randomUUID().toString()));}
}
