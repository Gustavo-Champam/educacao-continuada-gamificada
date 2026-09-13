package br.com.educacao.gamificada.domain;

public class Aluno {

    private String nome;
    private Plano plano;
    private int cursosConcluidos;

    public Aluno(String nome, Plano plano, int cursosConcluidos) {
        this.nome = nome;
        this.plano = plano;
        this.cursosConcluidos = cursosConcluidos;
    }
}
