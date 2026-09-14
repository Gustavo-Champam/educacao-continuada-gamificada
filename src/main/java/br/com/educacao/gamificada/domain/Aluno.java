package br.com.educacao.gamificada.domain;

public class Aluno {

    private String nome;
    private Plano plano;
    private int cursosConcluidos;

    public Aluno(String nome, Plano plano, int cursosConcluidos) {
        if (nome == null || nome.isBlank()) {
            throw new IllegalArgumentException("O nome é obrigatório.");
        }
        if (plano == null) {
            throw new IllegalArgumentException("O plano é obrigatório.");
        }
        if (cursosConcluidos < 0) {
            throw new IllegalArgumentException("A quantidade de cursos não pode ser negativa.");
        }
        this.nome = nome;
        this.plano = plano;
        this.cursosConcluidos = cursosConcluidos;
    }

    public boolean concluirCurso(double media) {
        if (!Double.isFinite(media) || media < 0 || media > 10) {
            throw new IllegalArgumentException("A média deve estar entre 0 e 10.");
        }
        if (media < 7.0) return false;
        cursosConcluidos++;
        if (plano == Plano.BASICO && cursosConcluidos >= 12) {
            plano = Plano.PREMIUM;
            return true;
        }
        return false;
    }

    public String getNome() { return nome; }
    public Plano getPlano() { return plano; }
    public int getCursosConcluidos() { return cursosConcluidos; }
}
