package br.com.educacao.gamificada.af;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.util.List;
import java.util.Map;
import org.springframework.context.annotation.Profile;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

/** Catálogo persistente; não altera os critérios de conclusão da AC1. */
@RestController @Profile("af") @RequestMapping("/api/af/cursos")
public class CursosAf {
 private final JdbcTemplate db;
 public CursosAf(JdbcTemplate db){
  this.db=db;
  db.execute("create table if not exists af_curso (codigo varchar(60) primary key, nome varchar(150) not null, descricao varchar(1000) not null)");
 }
 public record Curso(@NotBlank @Size(max=60) String codigo, @NotBlank @Size(max=150) String nome, @NotBlank @Size(max=1000) String descricao){}
 @PostMapping @ResponseStatus(HttpStatus.CREATED)
 public Curso criar(@Valid @RequestBody Curso curso){
  try{db.update("insert into af_curso(codigo,nome,descricao) values (?,?,?)",curso.codigo(),curso.nome(),curso.descricao());}
  catch(DuplicateKeyException e){throw new ResponseStatusException(HttpStatus.CONFLICT,"Codigo de curso ja cadastrado");}
  return curso;
 }
 @GetMapping public List<Map<String,Object>> listar(){
  return db.query("select codigo,nome,descricao from af_curso order by codigo",(rs,n)->Map.of("codigo",rs.getString(1),"nome",rs.getString(2),"descricao",rs.getString(3)));
 }
}
