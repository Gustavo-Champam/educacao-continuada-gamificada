package br.com.educacao.gamificada.af;

import br.com.educacao.gamificada.af.application.ClassificarCompetencias;
import org.junit.jupiter.api.Test;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;

class ClassificarCompetenciasTest {
 @Test void combinaAvaliacaoComHistoricoConfiavelSemDependerDeHttp() {
  var caso = new ClassificarCompetencias<Map<String,Object>>(id->{assertEquals(7L,id);return 12;}, atributos->atributos);
  assertEquals(Map.of("programming_experience_months",6.0,"completed_courses",12,
   "average_assessment_score",80.0,"weekly_study_hours",4.0,"rest_knowledge_score",50.0,
   "database_knowledge_score",60.0),caso.executar(7L,6,80,4,50,60));
 }
 @Test void alunoInexistenteNaoDisparaInferencia() {
  var caso=new ClassificarCompetencias<String>(id->{throw new IllegalArgumentException("aluno ausente");},
   atributos->{fail("Não deve enviar dados sem aluno válido");return "";});
  assertThrows(IllegalArgumentException.class,()->caso.executar(9L,0,0,0,0,0));
 }
}
