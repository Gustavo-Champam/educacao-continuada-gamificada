package br.com.educacao.orientacao;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.*;
import org.junit.jupiter.api.Test;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.model.*;
import org.springframework.ai.chat.prompt.Prompt;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
class OrientacaoTest {
 @Test void recuperaSemInventarRelevancia()throws Exception{var d=new DocumentosLocais(new ObjectMapper());assertEquals("DOC-01",d.buscar("Java REST").get(0).id());assertEquals("DOC-02",d.buscar("C4 arquitetura").get(0).id());assertEquals("DOC-03",d.buscar("Machine Learning").get(0).id());assertTrue(d.buscar("astronomia telescopios").isEmpty());assertTrue(d.buscar("iniciante curso").isEmpty());}
 @Test void consentimentoAntesDasFerramentas(){var d=mock(OrientarAluno.Documentos.class);var g=mock(OrientarAluno.Gerador.class);var a=new OrientarAluno(d,g);assertThrows(SecurityException.class,()->a.acompanhar("Java","iniciante",false,null));assertThrows(IllegalArgumentException.class,()->a.acompanhar("Java","iniciante",true,null));verifyNoInteractions(d,g);}
 @Test void ausenciaDeFontesNaoChamaModelo(){var g=mock(OrientarAluno.Gerador.class);var r=new OrientarAluno(p->List.of(),g).recomendar("astronomia","iniciante");assertFalse(r.geracao());assertFalse(r.efeitosExternos());verifyNoInteractions(g);}
 @Test void agenteUsaProgressoSemEscrita(){var f=new OrientarAluno.Fonte("DOC-01","Java","Aprenda Java");var p=new OrientarAluno.Progresso("BASICO",11);var a=new OrientarAluno(q->List.of(f),(q,n,fs,pr)->{assertEquals(p,pr);return "Java";});var r=a.acompanhar("Java","iniciante",true,p);assertEquals(1,r.progresso().cursosRestantes());assertFalse(r.efeitosExternos());assertEquals(List.of("consultar_progresso","buscar_documentos","gerar_orientacao"),r.ferramentas());assertEquals(0,new OrientarAluno.Progresso("PREMIUM",13).cursosRestantes());}
 @Test void springAiValidaFontesESaida(){var m=mock(ChatModel.class);var g=new GeradorSpringAi(m,new ObjectMapper());var fontes=List.of(new OrientarAluno.Fonte("DOC-01","Java","Aprenda Java"));when(m.call(any(Prompt.class))).thenReturn(new ChatResponse(List.of(new Generation(new AssistantMessage("{\"orientacao\":\"Estude Java\",\"fontes\":[\"DOC-01\"]}")))));assertTrue(g.gerar("Java","iniciante",fontes,new OrientarAluno.Progresso("BASICO",3)).contains("DOC-01"));for(String invalido:List.of("invalido","{}","{\"orientacao\":\"Java\",\"fontes\":[\"DOC-999\"]}")){when(m.call(any(Prompt.class))).thenReturn(new ChatResponse(List.of(new Generation(new AssistantMessage(invalido)))));assertThrows(IllegalStateException.class,()->g.gerar("Java","iniciante",fontes,null));}when(m.call(any(Prompt.class))).thenThrow(new RuntimeException("offline"));assertThrows(IllegalStateException.class,()->g.gerar("Java","iniciante",fontes,null));}
 @Test void recusaAtribuicaoInstitucionalMesmoComFonteValida(){
  var modelo=mock(ChatModel.class);
  var gerador=new GeradorSpringAi(modelo,new ObjectMapper());
  var fontes=List.of(new OrientarAluno.Fonte("DOC-01","Java","Trilha didática Java"));
  when(modelo.call(any(Prompt.class))).thenReturn(new ChatResponse(List.of(new Generation(new AssistantMessage("{\"orientacao\":\"Trilha disponível na FACENS\",\"fontes\":[\"DOC-01\"]}")))));
  assertThrows(IllegalStateException.class,()->gerador.gerar("Java","iniciante",fontes,null));
 }
}
