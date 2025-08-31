# pages/Politicas.py

import streamlit as st
import base64
import os
# <<< CORREÇÃO: Importando a função de tema do local correto >>>
from utils.theme import apply_cosmic_theme

# ==============================================================================
# Configuração da Página e Aplicação do Tema
# ==============================================================================
st.set_page_config(
    page_title="📜 Políticas - Santuário das Revelações",
    page_icon="📜",
    layout="centered"
)
apply_cosmic_theme()

# ==============================================================================
# Conteúdo da Página
# ==============================================================================

def display_policies():
    """Exibe as informações e políticas."""
    with st.container(border=True):
        st.header("Informações e Políticas")

        with st.expander("Contato e Suporte ao Cliente"):
            st.markdown("""
            Para dúvidas, suporte ou questões sobre sua consulta, por favor, entre em contato pelo e-mail:
            **taromisticoapp@gmail.com**

            Nosso tempo de resposta é de até 72 horas.
            """)

        with st.expander("Política de Reembolso e Disputas"):
            st.markdown("""
            **Natureza dos Serviços Digitais:** Nossas interpretações são produtos digitais gerados por IA e entregues instantaneamente após o pagamento. Devido a essa natureza e aos custos computacionais incorridos para gerar cada revelação única, **não oferecemos reembolsos** após a entrega do resultado.

            **Disputas:** Caso ocorra um problema técnico e você não receba sua interpretação após um pagamento bem-sucedido, por favor, entre em contato com nosso suporte. Faremos o possível para investigar e garantir que você receba o serviço pelo qual pagou.
            """)

        with st.expander("Termos e Condições do Serviço"):
            st.markdown("""
            1.  **Natureza do Serviço:** As ferramentas do "Santuário das Revelações" são para fins de entretenimento e autoconhecimento. As interpretações são geradas por um modelo de inteligência artificial e devem ser vistas como uma fonte de inspiração e reflexão, não como aconselhamento profissional (financeiro, legal, médico, psicológico) ou previsões factuais do futuro.
            2.  **Idade Mínima:** Você deve ter 18 anos ou mais para utilizar este serviço.
            3.  **Pagamento:** Todos os pagamentos são processados de forma segura através do Stripe. Ao efetuar o pagamento, você concorda com nossa política de não reembolso.
            4.  **Uso dos Dados:** Seus dados (nome, perguntas, dados de nascimento, descrição de sonhos) são usados exclusivamente para gerar sua interpretação e não são armazenados ou utilizados para qualquer outro fim após a conclusão da sua sessão.
            """)

# --- Renderiza a página ---
st.html("""
<div class="header-container">
    <h1 class="main-title">Políticas do Oráculo</h1>
</div>
""")

display_policies()

# <<< CORREÇÃO PRINCIPAL AQUI >>>
# O link agora aponta para o arquivo correto e tem estilo consistente.
st.page_link("🔮_Santuario_Principal.py", label="⬅ Voltar ao Santuário Principal", icon="↩️")
