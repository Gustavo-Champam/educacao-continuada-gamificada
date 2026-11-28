package br.com.educacao.orientacao;
import java.util.*;
/** Caso de uso independente de Spring. Fluxo controlado, somente leitura. */
public class OrientarAluno {
 public record Fonte(String id,String title,String text){}
 public record Progresso(String plano,int cursosConcluidos){public int cursosRestantes(){return Math.max(0,12-cursosConcluidos);}}
 public record Resposta(String resposta,List<Fonte> fontes,boolean geracao,List<String> ferramentas,Progresso progresso,boolean efeitosExternos){}
 public interface Documentos{List<Fonte> buscar(String pergunta);}
 public interface Gerador{String gerar(String pergunta,String perfil,List<Fonte> fontes,Progresso progresso);}
 private final Documentos documentos;private final Gerador gerador;
 public OrientarAluno(Documentos documentos,Gerador gerador){this.documentos=documentos;this.gerador=gerador;}
 public Resposta recomendar(String pergunta,String perfil){return executar(pergunta,perfil,null);}
 public Resposta acompanhar(String pergunta,String perfil,boolean autorizado,Progresso progresso){
  if(!autorizado)throw new SecurityException("Autorize a consulta documental e do progresso nesta solicitação.");
  if(progresso==null)throw new IllegalArgumentException("Progresso do Core obrigatório.");
  return executar(pergunta,perfil,progresso);
 }
 private Resposta executar(String pergunta,String perfil,Progresso progresso){
  var fontes=documentos.buscar(pergunta);var ferramentas=new ArrayList<String>();
  if(progresso!=null)ferramentas.add("consultar_progresso");
  ferramentas.add("buscar_documentos");
  if(fontes.isEmpty())return new Resposta("Não encontrei documentos relevantes para esse objetivo.",List.of(),false,List.copyOf(ferramentas),progresso,false);
  String resposta=gerador.gerar(pergunta,perfil,fontes,progresso);ferramentas.add("gerar_orientacao");
  return new Resposta(resposta,fontes,true,List.copyOf(ferramentas),progresso,false);
 }
}
