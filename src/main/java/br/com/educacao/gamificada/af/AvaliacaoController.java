package br.com.educacao.gamificada.af;
import com.fasterxml.jackson.databind.JsonNode;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import java.util.*;
import java.time.Duration;
import java.net.http.HttpClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Profile;
import org.springframework.http.HttpStatus;
import org.springframework.http.client.JdkClientHttpRequestFactory;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.*;
import org.springframework.web.server.ResponseStatusException;
@RestController @Profile("af") @RequestMapping("/api/af/avaliacoes")
public class AvaliacaoController {
 private final RestClient client;
 public AvaliacaoController(@Value("${af.evaluation.url:http://127.0.0.1:8013}") String url,@Value("${af.service-token:}") String token){
  var factory=new JdkClientHttpRequestFactory(HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(1)).build());factory.setReadTimeout(Duration.ofSeconds(10));
  client=RestClient.builder().baseUrl(url).requestFactory(factory).defaultHeader("X-AF-Service",token).build();
 }
 public record Pedido(@NotBlank @Size(max=1000) String question,@NotBlank @Size(max=12000) String answer,@NotEmpty @Size(max=5) List<@NotBlank @Size(max=5000) String> contexts,@Size(max=5000) String reference){}
 @PostMapping @ResponseStatus(HttpStatus.ACCEPTED) public JsonNode iniciar(@Valid @RequestBody Pedido p){
  try{return client.post().uri("/experiments/run").body(Map.of("trace_id",1,"question",p.question(),"answer",p.answer(),"contexts",p.contexts(),"reference",p.reference()==null?"":p.reference())).retrieve().body(JsonNode.class);}
  catch(RestClientException e){throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,"Avaliador local indisponivel");}
 }
 @GetMapping("/{id}") public JsonNode consultar(@PathVariable String id){
  UUID.fromString(id);
  try{return client.get().uri("/experiments/"+id).retrieve().body(JsonNode.class);}
  catch(RestClientException e){throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,"Nao foi possivel consultar a avaliacao");}
 }
}
