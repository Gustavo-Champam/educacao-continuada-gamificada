package br.com.educacao.gamificada.af;
import org.junit.jupiter.api.*;
import org.springframework.mock.web.*;
import java.util.Base64;
import java.util.concurrent.atomic.AtomicBoolean;
import static org.junit.jupiter.api.Assertions.*;
class AcessoAfTest {
 private final AcessoAf filter=new AcessoAf("admin-seguro-123","aluno1-seguro-123","aluno2-seguro-123");
 private int request(String method,String path,String user,String password,boolean header)throws Exception{
  var req=new MockHttpServletRequest(method,path);var res=new MockHttpServletResponse();
  if(user!=null)req.addHeader("Authorization","Basic "+Base64.getEncoder().encodeToString((user+":"+password).getBytes()));
  if(header)req.addHeader("X-AF-Request","1");
  var passed=new AtomicBoolean(false);filter.doFilter(req,res,(a,b)->passed.set(true));return passed.get()?200:res.getStatus();
 }
 @Test void credenciaisEConsentimentoDeRequisicao()throws Exception{
  assertEquals(401,request("GET","/api/alunos",null,null,false));
  assertEquals(401,request("GET","/api/alunos","champam","errada",false));
  assertEquals(401,request("GET","/api/alunos","desconhecido","admin-seguro-123",false));
  assertEquals(200,request("GET","/api/alunos","champam","admin-seguro-123",false));
  assertEquals(200,request("POST","/api/af/treinamentos","camargo","admin-seguro-123",true));
  assertEquals(403,request("POST","/api/af/treinamentos","camargo","admin-seguro-123",false));
 }
 @Test void alunosNaoAcessamOutrosNemTreinamento()throws Exception{
  assertEquals(200,request("GET","/api/alunos/1","aluno1","aluno1-seguro-123",false));
  assertEquals(200,request("GET","/api/alunos/2/recompensas","aluno2","aluno2-seguro-123",false));
  assertEquals(403,request("GET","/api/alunos/2","aluno1","aluno1-seguro-123",false));
  assertEquals(403,request("GET","/api/alunos","aluno1","aluno1-seguro-123",false));
  assertEquals(403,request("POST","/api/af/treinamentos","aluno1","aluno1-seguro-123",true));
  assertEquals(200,request("POST","/api/af/alunos/1/agente","aluno1","aluno1-seguro-123",true));
 }
 @Test void saudePublicaESenhasFracas()throws Exception{
  assertEquals(200,request("GET","/actuator/health",null,null,false));assertEquals(200,request("GET","/af.html",null,null,false));
  assertThrows(IllegalArgumentException.class,()->new AcessoAf("curta","aluno1-seguro-123","aluno2-seguro-123"));
 }
 @Test void rejeitaCabecalhosMalformadosESenhasFracasRestantes()throws Exception{
  for(String auth:new String[]{"Bearer token","Basic !!!","Basic "+Base64.getEncoder().encodeToString("sem-separador".getBytes())}){
   var req=new MockHttpServletRequest("GET","/api/alunos");req.addHeader("Authorization",auth);var res=new MockHttpServletResponse();filter.doFilter(req,res,(a,b)->fail());assertEquals(401,res.getStatus());
  }
  assertThrows(IllegalArgumentException.class,()->new AcessoAf("admin-seguro-123","curta","aluno2-seguro-123"));
  assertThrows(IllegalArgumentException.class,()->new AcessoAf("admin-seguro-123","aluno1-seguro-123","curta"));
 }
}
