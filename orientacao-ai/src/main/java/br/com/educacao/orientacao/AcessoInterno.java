package br.com.educacao.orientacao;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
@Component
public class AcessoInterno extends OncePerRequestFilter {
 private final byte[] segredo;
 public AcessoInterno(@Value("${af.service-token}")String segredo){if(segredo.length()<16)throw new IllegalArgumentException("Token interno mínimo de 16 caracteres.");this.segredo=segredo.getBytes(StandardCharsets.UTF_8);}
 protected void doFilterInternal(HttpServletRequest p,HttpServletResponse r,FilterChain c)throws ServletException,IOException{if(p.getRequestURI().equals("/actuator/health")){c.doFilter(p,r);return;}String token=p.getHeader("X-AF-Service");if(token==null||!MessageDigest.isEqual(segredo,token.getBytes(StandardCharsets.UTF_8))){r.sendError(401);return;}c.doFilter(p,r);}
}
