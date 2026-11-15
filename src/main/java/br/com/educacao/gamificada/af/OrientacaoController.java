package br.com.educacao.gamificada.af;

import br.com.educacao.gamificada.service.AlunoService;
import com.fasterxml.jackson.databind.JsonNode;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import java.time.Duration;
import java.net.http.HttpClient;
import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Profile;
import org.springframework.http.HttpStatus;
import org.springframework.http.client.JdkClientHttpRequestFactory;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;
import org.springframework.web.server.ResponseStatusException;

@RestController
@Profile("af")
@RequestMapping("/api/af")
public class OrientacaoController {
 @Value("${af.service-token:}") private String serviceToken="";
 private final AlunoService alunos;
 private final RestClient orientacao;
 private final RestClient ml;
 public OrientacaoController(AlunoService alunos, @Value("${af.orientacao.url:http://127.0.0.1:8012}") String orientacaoUrl,
   @Value("${af.ml.url:http://127.0.0.1:8011}") String mlUrl) {
  this.alunos=alunos; this.orientacao=client(orientacaoUrl,120); this.ml=client(mlUrl,2);
 }
 private RestClient client(String url,int seconds){
  var factory=new JdkClientHttpRequestFactory(HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(1)).build());
  factory.setReadTimeout(Duration.ofSeconds(seconds));return RestClient.builder().baseUrl(url).requestFactory(factory).build();
 }
 public record Avaliacao(@Min(0) @Max(120) double experienciaMeses,
  @Min(0) @Max(100) double nota, @Min(0) @Max(30) double horasSemanais,
  @Min(0) @Max(100) double conhecimentoRest, @Min(0) @Max(100) double conhecimentoBanco) {}
 public record Pergunta(@NotBlank @Size(max=1000) String pergunta, @NotBlank @Size(max=40) String perfil, boolean autorizaConsulta) {}
 @PostMapping("/alunos/{id}/classificacao")
 public JsonNode classificar(@PathVariable Long id,@Valid @RequestBody Avaliacao a){
  var aluno=alunos.buscar(id);
  return post(ml,"/predict",Map.of("programming_experience_months",a.experienciaMeses(),"completed_courses",aluno.cursosConcluidos(),
   "average_assessment_score",a.nota(),"weekly_study_hours",a.horasSemanais(),"rest_knowledge_score",a.conhecimentoRest(),"database_knowledge_score",a.conhecimentoBanco()));
 }
 @PostMapping("/alunos/{id}/recomendacao")
 public JsonNode recomendar(@PathVariable Long id,@Valid @RequestBody Pergunta p){
  alunos.buscar(id);return post(orientacao,"/recomendar",Map.of("pergunta",p.pergunta(),"perfil",p.perfil()));
 }
 @PostMapping("/alunos/{id}/agente")
 public JsonNode agente(@PathVariable Long id,@Valid @RequestBody Pergunta p){
  alunos.buscar(id);
  if(!p.autorizaConsulta())throw new ResponseStatusException(HttpStatus.FORBIDDEN,"Autorize a consulta antes de executar o agente.");
  return post(orientacao,"/agente",Map.of("pergunta",p.pergunta(),"perfil",p.perfil(),"autoriza_consulta",true));
 }
 private JsonNode post(RestClient client,String path,Object body){
  try{return client.post().uri(path).header("X-AF-Service",serviceToken).body(body).retrieve().body(JsonNode.class);}
  catch(RestClientException e){throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,"Servico de IA indisponivel; os cadastros continuam funcionando.");}
 }
}
