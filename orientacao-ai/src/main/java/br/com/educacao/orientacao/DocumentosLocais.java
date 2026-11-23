package br.com.educacao.orientacao;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.text.Normalizer;
import java.util.*;
import java.util.stream.Collectors;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;
@Component
public class DocumentosLocais implements OrientarAluno.Documentos {
 private final List<OrientarAluno.Fonte> documentos;
 private static final Set<String> IGNORAR=Set.of("de","da","do","das","dos","em","com","para","por","um","uma","os","as","no","na","que","quero","qual","como","me","meu","minha","aprender","curso","cursos","trilha","trilhas","seguir","preciso","sobre","iniciante","intermediario","avancado");
 public DocumentosLocais(ObjectMapper json)throws IOException{try(var entrada=new ClassPathResource("documentos.json").getInputStream()){documentos=List.of(json.readValue(entrada,OrientarAluno.Fonte[].class));}}
 private Set<String> termos(String texto){return Arrays.stream(Normalizer.normalize(texto.toLowerCase(Locale.ROOT),Normalizer.Form.NFD).replaceAll("\\p{M}","").split("[^a-z0-9]+")) .filter(t->t.length()>1).filter(t->!IGNORAR.contains(t)).collect(Collectors.toSet());}
 private double pontuar(Set<String> consulta,OrientarAluno.Fonte fonte){var palavras=termos(fonte.title()+" "+fonte.text());long comuns=consulta.stream().filter(palavras::contains).count();long titulo=consulta.stream().filter(termos(fonte.title())::contains).count();return comuns/Math.sqrt(Math.max(1,consulta.size())*palavras.size())+titulo/(double)Math.max(1,consulta.size());}
 public List<OrientarAluno.Fonte> buscar(String pergunta){var consulta=termos(pergunta);double melhor=documentos.stream().mapToDouble(d->pontuar(consulta,d)).max().orElse(0);return documentos.stream().filter(d->pontuar(consulta,d)>Math.max(.10,melhor*.5)).sorted(Comparator.<OrientarAluno.Fonte>comparingDouble(d->pontuar(consulta,d)).reversed().thenComparing(OrientarAluno.Fonte::id)).limit(3).toList();}
}
