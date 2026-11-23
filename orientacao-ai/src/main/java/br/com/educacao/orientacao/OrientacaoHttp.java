package br.com.educacao.orientacao;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
@RestController
public class OrientacaoHttp {
 private final OrientarAluno orientacao;
 public OrientacaoHttp(OrientarAluno.Documentos documentos,OrientarAluno.Gerador gerador){orientacao=new OrientarAluno(documentos,gerador);}
 public record Progresso(@NotNull @Pattern(regexp="BASICO|PREMIUM")String plano,@Min(0)int cursosConcluidos){}
 public record Pedido(@NotBlank @Size(min=3,max=1000)String pergunta,@NotNull @Pattern(regexp="iniciante|intermediario|avancado")String perfil,boolean autoriza_consulta,@Valid Progresso progresso){}
 @PostMapping("/recomendar")public OrientarAluno.Resposta recomendar(@Valid @RequestBody Pedido p){return orientacao.recomendar(p.pergunta(),p.perfil());}
 @PostMapping("/agente")public OrientarAluno.Resposta agente(@Valid @RequestBody Pedido p){if(!p.autoriza_consulta())throw new SecurityException("Consulta não autorizada.");return orientacao.acompanhar(p.pergunta(),p.perfil(),true,p.progresso()==null?null:new OrientarAluno.Progresso(p.progresso().plano(),p.progresso().cursosConcluidos()));}
 @ExceptionHandler(SecurityException.class)public ProblemDetail proibido(SecurityException e){return ProblemDetail.forStatusAndDetail(HttpStatus.FORBIDDEN,e.getMessage());}
 @ExceptionHandler(IllegalArgumentException.class)public ProblemDetail invalido(IllegalArgumentException e){return ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST,e.getMessage());}
 @ExceptionHandler(IllegalStateException.class)public ProblemDetail indisponivel(IllegalStateException e){return ProblemDetail.forStatusAndDetail(HttpStatus.SERVICE_UNAVAILABLE,e.getMessage());}
}
