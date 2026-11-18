package br.com.educacao.gamificada.af;
import org.junit.jupiter.api.Test;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import java.util.UUID;

class CursosAfTest {
 @Test void catalogoPersisteValidaEntradaERejeitaDuplicata() throws Exception {
  var db=new JdbcTemplate(new DriverManagerDataSource("jdbc:h2:mem:"+UUID.randomUUID()+";DB_CLOSE_DELAY=-1","sa",""));
  var mvc=MockMvcBuilders.standaloneSetup(new CursosAf(db)).build();
  String curso="{\"codigo\":\"JAVA-01\",\"nome\":\"Java REST\",\"descricao\":\"APIs REST com Java\"}";
  mvc.perform(post("/api/af/cursos").contentType("application/json").content(curso)).andExpect(status().isCreated()).andExpect(jsonPath("$.nome").value("Java REST"));
  mvc.perform(post("/api/af/cursos").contentType("application/json").content(curso)).andExpect(status().isConflict());
  mvc.perform(post("/api/af/cursos").contentType("application/json").content("{\"codigo\":\"\",\"nome\":\"\",\"descricao\":\"\"}")).andExpect(status().isBadRequest());
  var outraInstancia=MockMvcBuilders.standaloneSetup(new CursosAf(db)).build();
  outraInstancia.perform(get("/api/af/cursos")).andExpect(status().isOk()).andExpect(jsonPath("$[0].codigo").value("JAVA-01")).andExpect(jsonPath("$[0].descricao").value("APIs REST com Java"));
 }
}
