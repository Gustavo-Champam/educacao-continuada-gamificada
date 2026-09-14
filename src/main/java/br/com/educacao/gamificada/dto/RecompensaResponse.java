package br.com.educacao.gamificada.dto;
import br.com.educacao.gamificada.entity.RecompensaEntity;
import java.time.Instant;
public record RecompensaResponse(Long alunoId, int vouchers, int moedas, String origem, Instant registradoEm) {
    public static RecompensaResponse from(RecompensaEntity registro) {
        return new RecompensaResponse(registro.getAlunoId(), registro.getVouchers(), registro.getMoedas(), registro.getOrigem(), registro.getRegistradoEm());
    }
}
