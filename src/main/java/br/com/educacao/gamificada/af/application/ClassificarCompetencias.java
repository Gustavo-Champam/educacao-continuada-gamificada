package br.com.educacao.gamificada.af.application;

import java.util.Map;

/** Caso de uso independente de Spring, HTTP e persistência. */
public final class ClassificarCompetencias<R> {
    public interface HistoricoAluno { int cursosConcluidos(Long alunoId); }
    public interface Classificador<R> { R prever(Map<String, Object> atributos); }

    private final HistoricoAluno historico;
    private final Classificador<R> classificador;

    public ClassificarCompetencias(HistoricoAluno historico, Classificador<R> classificador) {
        this.historico = historico;
        this.classificador = classificador;
    }

    public R executar(Long alunoId, double experiencia, double nota, double horas,
                      double rest, double banco) {
        int cursos = historico.cursosConcluidos(alunoId);
        return classificador.prever(Map.of(
            "programming_experience_months", experiencia, "completed_courses", cursos,
            "average_assessment_score", nota, "weekly_study_hours", horas,
            "rest_knowledge_score", rest, "database_knowledge_score", banco));
    }
}
