# pages/2_Politicas.py

import streamlit as st
# Importa a função de estilo do seu aplicativo principal
from app_11 import apply_mystical_theme

# Configura a página e aplica o tema místico
st.set_page_config(page_title="📜 Políticas - Tarô Místico", page_icon="📜", layout="centered")
apply_mystical_theme()

def display_business_info():
    """Exibe as informações comerciais e políticas em um container."""
    with st.container(border=True):
        st.header("Informações e Políticas")

        with st.expander("Contato e Suporte ao Cliente"):
            st.markdown("""
            Para dúvidas, suporte ou questões sobre sua leitura, por favor, entre em contato pelo e-mail:
            **taromisticoapp@gmail.com**

            Nosso tempo de resposta é de até 72 horas.
            """)

        with st.expander("Política de Reembolso e Disputas"):
            st.markdown("""
            **Natureza dos Serviços Digitais:** Nossas leituras de tarô são produtos digitais gerados por IA e entregues instantaneamente após o pagamento. Devido a essa natureza e aos custos computacionais incorridos (uso da API da OpenAI) para gerar cada interpretação única, **não oferecemos reembolsos** após a entrega da leitura.

            **Disputas:** Caso ocorra um problema técnico e você não receba sua leitura após um pagamento bem-sucedido, por favor, entre em contato com nosso suporte. Faremos o possível para investigar e garantir que você receba o serviço pelo qual pagou.
            """)

        with st.expander("Termos e Condições do Serviço"):
            st.markdown("""
            1.  **Natureza do Serviço:** O "Tarô Místico" é uma ferramenta de entretenimento e autoconhecimento. As leituras são geradas por um modelo de inteligência artificial e devem ser vistas como uma fonte de inspiração e reflexão, não como aconselhamento profissional (financeiro, legal, médico, etc.) ou previsões factuais do futuro.
            2.  **Idade Mínima:** Você deve ter 18 anos ou mais para utilizar este serviço.
            3.  **Pagamento:** Todos os pagamentos são processados de forma segura através do Stripe. Ao efetuar o pagamento, você concorda com nossa política de não reembolso.
            4.  **Uso dos Dados:** A pergunta que você faz e o seu nome são usados exclusivamente para gerar sua leitura e não são armazenados ou utilizados para qualquer outro fim após a conclusão da sua sessão.
            """)

# --- Renderiza a página ---
st.html("""
<div class="header-container">
    <h1 class="main-title">Políticas do Oráculo</h1>
</div>
""")

display_business_info()

# Adiciona um botão para voltar facilmente à página principal
st.page_link("app_11.py", label="⬅️ Voltar ao Oráculo", use_container_width=True)
