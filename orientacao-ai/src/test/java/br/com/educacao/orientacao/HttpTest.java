package br.com.educacao.orientacao;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.ai.chat.model.ChatModel;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
@SpringBootTest(properties="af.service-token=teste-interno-123456") @AutoConfigureMockMvc
class HttpTest {
 @Autowired MockMvc http;@MockitoBean ChatModel modelo;
 @Test void tokenObrigatorio()throws Exception{http.perform(post("/recomendar")).andExpect(status().isUnauthorized());http.perform(post("/recomendar").header("X-AF-Service","errado")).andExpect(status().isUnauthorized());verifyNoInteractions(modelo);}
 @Test void consentimentoObrigatorio()throws Exception{http.perform(post("/agente").header("X-AF-Service","teste-interno-123456").contentType("application/json").content("{\"pergunta\":\"Java REST\",\"perfil\":\"iniciante\"}")).andExpect(status().isForbidden());verifyNoInteractions(modelo);}
 @Test void entradaInvalidaESemFonte()throws Exception{http.perform(post("/recomendar").header("X-AF-Service","teste-interno-123456").contentType("application/json").content("{\"pergunta\":\"\",\"perfil\":\"admin\"}")).andExpect(status().isBadRequest());http.perform(post("/recomendar").header("X-AF-Service","teste-interno-123456").contentType("application/json").content("{\"pergunta\":\"astronomia telescopios\",\"perfil\":\"iniciante\"}")).andExpect(status().isOk()).andExpect(jsonPath("$.geracao").value(false));verifyNoInteractions(modelo);}
}
