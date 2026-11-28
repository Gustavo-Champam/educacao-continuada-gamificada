package br.com.educacao.gamificada.af;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Base64;
import java.util.regex.Pattern;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

/** Contas didáticas por papel. Produção requer provedor de identidade e TLS. */
@Component @Profile("af")
public class AcessoAf extends OncePerRequestFilter {
 private final String admin,aluno1,aluno2;
 public AcessoAf(@Value("${af.admin-password}") String admin,@Value("${af.aluno1-password}") String aluno1,@Value("${af.aluno2-password}") String aluno2){
  if(admin.length()<12 || aluno1.length()<12 || aluno2.length()<12)throw new IllegalArgumentException("Defina senhas locais com ao menos 12 caracteres");
  this.admin=admin;this.aluno1=aluno1;this.aluno2=aluno2;
 }
 @Override protected void doFilterInternal(HttpServletRequest request,HttpServletResponse response,FilterChain chain)throws ServletException,IOException{
  String path=request.getRequestURI();
  if(!path.startsWith("/api/") && !path.startsWith("/actuator/")){chain.doFilter(request,response);return;}
  if(path.equals("/actuator/health")){chain.doFilter(request,response);return;}
  String[] login=credentials(request.getHeader("Authorization"));
  String expected=switch(login[0]){case "champam","camargo"->admin;case "aluno1"->aluno1;case "aluno2"->aluno2;default->null;};
  if(expected==null || !MessageDigest.isEqual(expected.getBytes(StandardCharsets.UTF_8),login[1].getBytes(StandardCharsets.UTF_8))){response.sendError(401,"Autenticacao necessaria");return;}
  if(!request.getMethod().equals("GET") && !"1".equals(request.getHeader("X-AF-Request"))){response.sendError(403,"Cabecalho de confirmacao ausente");return;}
  boolean staff=login[0].equals("champam")||login[0].equals("camargo");
  if(!staff){
   String id=login[0].equals("aluno1")?"1":"2";
   boolean ownGet=request.getMethod().equals("GET") && path.matches("/api/alunos/"+id+"(/recompensas)?");
   boolean ownAi=request.getMethod().equals("POST") && path.matches("/api/af/alunos/"+id+"/(classificacao|recomendacao|agente)");
   if(!ownGet && !ownAi){response.sendError(403,"Acesso fora do escopo da conta");return;}
  }
  chain.doFilter(new HttpServletRequestWrapper(request){@Override public String getRemoteUser(){return login[0];}},response);
 }
 private String[] credentials(String header){
  if(header==null||!header.startsWith("Basic "))return new String[]{"",""};
  try{String[] values=new String(Base64.getDecoder().decode(header.substring(6)),StandardCharsets.UTF_8).split(":",2);return values.length==2?values:new String[]{"",""};}
  catch(IllegalArgumentException e){return new String[]{"",""};}
 }
}
