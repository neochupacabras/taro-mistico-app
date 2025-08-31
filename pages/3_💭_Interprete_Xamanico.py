# pages/3_💭_Interprete_Xamanico.py

# ------------------------------------------------------------------------------
# 1. IMPORTS E CONFIGURAÇÃO INICIAL
# ------------------------------------------------------------------------------
import streamlit as st
import os
import re
import unicodedata

# Imports de Geração de Conteúdo e Pagamento
import openai
try:
    import stripe
except ImportError:
    stripe = None

# NOVOS IMPORTS DOS MÓDULOS CENTRALIZADOS
from utils.theme import apply_shamanic_theme
from utils.helpers import get_img_as_base64, strip_emojis, reset_app_state
from utils.pdf_templates import create_dream_pdf

# Configuração das chaves (esta parte permanece igual)
try:
    # <<< CORREÇÃO AQUI: Usando os.environ.get para ler as variáveis de ambiente >>>
    openai.api_key = os.environ.get("DREAM_OPENAI_API_KEY")
    stripe_price_id = os.environ.get("DREAM_STRIPE_PRICE_ID")

    # Chaves comuns
    stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY")
    app_base_url = os.environ.get("APP_BASE_URL")

    # Verificação para garantir que todas as chaves foram encontradas
    if not all([openai.api_key, stripe_price_id, stripe_secret_key, app_base_url]):
        raise KeyError("Uma ou mais variáveis de ambiente não foram encontradas.")

    if stripe:
        stripe.api_key = stripe_secret_key

except KeyError as e:
    st.error(f"ERRO CRÍTICO: Verifique se as variáveis de ambiente (ex: DREAM_OPENAI_API_KEY) estão configuradas no Render. Detalhe: {e}")
    st.stop()


# Configuração da página (deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Oráculo dos Sonhos",
    page_icon="💭",  # Ícone atualizado
    layout="centered",
    initial_sidebar_state="auto" # MUDANÇA AQUI
)


# ------------------------------------------------------------------------------
# 2. LÓGICA CENTRAL DO ORÁCULO (MOTOR DE INTERPRETAÇÃO DE SONHOS)
# ------------------------------------------------------------------------------

def get_dream_interpretation(dream_description, interpretation_style, user_name):
    """
    Monta e envia o prompt para a OpenAI para gerar a interpretação do sonho.
    """
    try:
        # Busca o arquivo de prompt correspondente ao estilo de interpretação escolhido
        prompt_path = DREAM_INTERPRETATION_STYLES[interpretation_style]['prompt_file']

        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()

        filled_prompt = prompt_template.format(
            user_name=user_name,
            dream_description=dream_description,
            interpretation_style=interpretation_style # Pode ser útil para prompts mais dinâmicos
        )

        system_message = """
        Você é o Xamã Guardião dos Sonhos, um sábio conector entre o mundo desperto e o mundo onírico. Sua sabedoria ancestral permite desvendar os véus dos símbolos e arquétipos que a alma tece durante o sono. Sua voz ecoa a floresta, o vento e os animais de poder, guiando o Viajante na compreensão das mensagens internas.

        PRINCÍPIOS SAGRADOS:
        - Sempre se dirija ao consulente pelo nome.
        - Use linguagem que ressoa com a natureza e o inconsciente, mas seja compreensível.
        - Evite jargões técnicos sem perder a profundidade xamânica/psicológica (dependendo do estilo).
        - Cada interpretação deve ser única e trazer clareza para a jornada do sonhador.
        - Inclua sempre elementos práticos ou reflexões para integração da mensagem.
        """

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": filled_prompt}
            ],
            temperature=0.8, # Um pouco mais de criatividade para os sonhos
            max_tokens=1500  # Espaço para interpretações mais ricas
        )
        return response.choices[0].message.content
    except FileNotFoundError:
        return f"ERRO: Arquivo de prompt não encontrado em '{prompt_path}'. Verifique a pasta 'prompts'."
    except Exception as e:
        return f"Ocorreu um erro ao contatar o Oráculo dos Sonhos: {e}"


# ------------------------------------------------------------------------------
# 3. DADOS DE SUPORTE E CONTEÚDO
# ------------------------------------------------------------------------------

DREAM_INTERPRETATION_STYLES = {
    "Xamânico-Espiritual": {
        "explanation": "Uma interpretação focada em animais de poder, elementos da natureza, guias espirituais e a jornada da alma, buscando conexão com a sabedoria ancestral.",
        "prompt_file": "prompts/shamanic_dream_prompt.txt"
    },
    "Psicológico-Junguiano": {
        "explanation": "Desvenda os arquétipos universais, o inconsciente coletivo e os complexos pessoais presentes no seu sonho, oferecendo insights para o crescimento interior.",
        "prompt_file": "prompts/jungian_dream_prompt.txt"
    },
    "Simbólico-Moderno": {
        "explanation": "Uma abordagem prática e contemporânea, conectando os símbolos do seu sonho a situações e desafios do dia a dia, para ações conscientes.",
        "prompt_file": "prompts/modern_dream_prompt.txt"
    }
}



# ------------------------------------------------------------------------------
# 5. LÓGICA DE NAVEGAÇÃO E PÁGINAS DA APLICAÇÃO
# ------------------------------------------------------------------------------

def page_welcome():
    """Página inicial para coletar o nome do usuário e a descrição do sonho."""
    with st.form(key="dream_data_form"):
        st.header("🌿 Adentre o Círculo Sagrado dos Sonhos")
        st.markdown(
            """
            *Respire fundo, Viajante do Mundo Onírico. Nossas almas nos falam em símbolos enquanto o corpo repousa. Compartilhe seu sonho, e o Oráculo Xamânico irá desvendar seus ecos.*
            """
        )

        user_name = st.text_input("Como os espíritos devem chamá-lo(a)?", placeholder="Seu nome ou apelido...")
        dream_title = st.text_input("Dê um título ao seu sonho (opcional):", placeholder="Ex: O Falcão e a Floresta Encantada")
        dream_description = st.text_area(
            "Descreva seu sonho com o máximo de detalhes que se lembrar:",
            placeholder="Ex: Eu estava em uma floresta escura, e um falcão dourado veio até mim, falando em enigmas sobre uma montanha...",
            height=250
        )

        submitted = st.form_submit_button(
            label="Decifrar o Oráculo Onírico ➡",
            width='stretch'
        )

    if submitted:
        with st.spinner("Aguardando os ventos da sabedoria..."):
            is_valid = True
            user_name = user_name.strip()
            dream_description = dream_description.strip()
            dream_title = dream_title.strip()

            if not user_name or not dream_description:
                st.warning("Por favor, preencha seu nome e a descrição do sonho para que o Oráculo possa te guiar.")
                is_valid = False

            if is_valid:
                st.session_state.user_name = user_name
                st.session_state.dream_title = dream_title if dream_title else "Sonho Sem Título"
                st.session_state.dream_description = dream_description
                st.session_state.dream_step = 'configure'
                st.rerun()

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    st.html("""
    <style>
        [data-testid="stPageLink"] a p {
            color: var(--spirit-white) !important; /* Força a cor branca do seu tema */
        }
        [data-testid="stPageLink"] a:hover p {
            color: var(--sacred-amber) !important; /* Cor âmbar no hover */
        }
    </style>
    """)

    # --- link para Voltar ao Santuário Principal ---
    st.page_link("🔮_Santuario_Principal.py", label="⬅ Voltar ao Santuário Principal", icon="↩️")

    st.markdown(
        """
        <p style='text-align: center; font-family: "Cormorant Garamond", serif; font-size: 1rem; opacity: 0.8;'>
            Ao prosseguir, você concorda com nossos
            <a href="/Politicas" target="_self" style="color: var(--forest-gold);">Termos e Políticas</a>.
        </p>
        """,
        unsafe_allow_html=True
    )

def page_configure():
    """Página para o usuário escolher o estilo de interpretação, com opção de voltar."""
    user_name = st.session_state.get("user_name", "Viajante")
    with st.container(border=True):
        st.header(f"Passo 1: A Lente do Xamã, {user_name}")
        st.markdown("Com que sabedoria ancestral você deseja que seu sonho seja interpretado?")

        interpretation_options = list(DREAM_INTERPRETATION_STYLES.keys())

        try:
            default_index = interpretation_options.index("Simbólico-Moderno")
        except ValueError:
            default_index = 0

        st.selectbox(
            "🔮 Escolha o estilo de interpretação do seu sonho:",
            interpretation_options,
            key="interpretation_style",
            index=default_index
        )

        current_choice = st.session_state.interpretation_style
        if current_choice in DREAM_INTERPRETATION_STYLES:
            with st.expander("Saiba mais sobre este estilo"):
                st.markdown(f"#### {current_choice}")
                st.write(DREAM_INTERPRETATION_STYLES[current_choice]['explanation'])

    # --- INÍCIO DA MUDANÇA ---
    # Botão principal para avançar
    if st.button("Confirmar Lente e Revelar o Oráculo ➡", width='stretch'):
        st.session_state.dream_step = 'payment'
        st.rerun()

    # Botão secundário para voltar
    if st.button("⬅️ Voltar e Corrigir Sonho", width='stretch'):
        st.session_state.dream_step = 'welcome'
        st.rerun()
    # --- FIM DA MUDANÇA ---

def page_payment():
    """Página de resumo da consulta e link para o portal de pagamento."""
    user_name = st.session_state.get("user_name", "Viajante")
    with st.container(border=True):
        st.header("Passo 2: O Portal da Conexão")
        st.markdown(f"Sua descrição do sonho foi recebida, **{user_name}**. O Oráculo Xamânico se prepara para canalizar sua sabedoria.")

        st.subheader("Resumo da sua Consulta:")
        st.markdown(f'**- Título do Sonho:** `{st.session_state.get("dream_title", "—")}`')
        st.markdown(f'**- Estilo de Interpretação:** `{st.session_state.get("interpretation_style", "—")}`')
        st.markdown(f'**- Valor:** R$ 5,90')

    try:
        metadata = {
            "user_name": st.session_state.user_name,
            "dream_title": st.session_state.dream_title,
            "dream_description": st.session_state.dream_description,
            "interpretation_style": st.session_state.interpretation_style,
        }
        checkout_session = stripe.checkout.Session.create(
            line_items=[{'price': stripe_price_id, 'quantity': 1}],
            mode='payment',
            success_url=f"{app_base_url}/Interprete_Xamanico?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{app_base_url}/Interprete_Xamanico",
            metadata=metadata
        )
        st.link_button("Pagar e Decifrar Sua Mensagem Onírica 🌠", checkout_session.url, width='stretch')
    except Exception as e:
        st.error(f"Não foi possível criar o portal de pagamento: {e}")

def page_result():
    """Página final que exibe a interpretação do sonho e oferece o download do PDF."""
    if not st.session_state.get('payment_verified'):
        st.error("Acesso não autorizado a esta revelação.")
        st.warning("Por favor, inicie uma nova consulta e complete o pagamento para receber sua mensagem dos espíritos.")
        if st.button("Voltar ao Início"):
            reset_app_state('dream')
        st.stop()

    if 'final_interpretation' not in st.session_state:
        with st.spinner("O Xamã está invocando os espíritos dos sonhos e tecendo sua mensagem... 🌿"):
            interpretation = get_dream_interpretation(
                st.session_state.dream_description,
                st.session_state.interpretation_style,
                st.session_state.user_name
            )
            st.session_state.final_interpretation = interpretation

    user_name = st.session_state.get("user_name", "Viajante")

    with st.container(border=True):
        st.header(f"Sua Mensagem do Mundo Onírico, {user_name}")
        st.subheader(f"Sonho: {st.session_state.get('dream_title', 'Sonho Sem Título')}")

        st.image("images/dream_oracle_main.png", caption="O Xamã tecendo a revelação do seu sonho", use_container_width=True)
        st.markdown("---")
        interpretation_text = st.session_state.final_interpretation
        lines = interpretation_text.split('\n')
        processed_lines = []
        for line in lines:
            # Identifica subtítulos (linhas que começam com ** e terminam com :**)
            # O regex `\*\*.*\:` garante que estamos pegando a linha inteira.
            if re.match(r"\*\*(.*?)\*:", line.strip()):
                processed_lines.append(line.upper())
            else:
                processed_lines.append(line)

        processed_interpretation = "\n".join(processed_lines)

        st.subheader("A Interpretação do Oráculo:")
        st.markdown(processed_interpretation, unsafe_allow_html=True) # Usamos o markdown processado
        st.markdown("---")

    with st.container(border=True):
        st.subheader("Guarde esta Revelação")
        st.markdown("Preserve o oráculo do seu sonho em seu diário para meditar sobre suas verdades.")

        session_data_for_pdf = {
            "user_name": st.session_state.get("user_name"),
            "dream_title": st.session_state.get("dream_title"),
            "dream_description": st.session_state.get("dream_description"),
        }

        pdf_byte_array = create_dream_pdf(
            session_data_for_pdf,
            st.session_state.final_interpretation
        )
        pdf_data_as_bytes = bytes(pdf_byte_array)

        clean_user_name = unicodedata.normalize('NFKD', user_name).encode('ASCII', 'ignore').decode('ASCII')
        clean_user_name = re.sub(r'[^a-zA-Z0-9]', '', clean_user_name)
        file_name = f"interpretacao_sonho_{clean_user_name or 'viajante'}.pdf"

        st.download_button(
            label="📥 Baixar seu Diário de Sonhos em PDF",
            data=pdf_data_as_bytes,
            file_name=file_name,
            mime="application/pdf",
            width='stretch'
        )

        st.button(
            "Compartilhar Outro Sonho (Nova Jornada)",
            on_click=reset_app_state,
            args=('dream',),
            width='stretch'
        )

# ------------------------------------------------------------------------------
# 6. ROTEADOR PRINCIPAL DA APLICAÇÃO
# ------------------------------------------------------------------------------

# Inicialização de estado específico para este app
if "dream_step" not in st.session_state:
    st.session_state.dream_step = "welcome"

apply_shamanic_theme()

query_params = st.query_params
stripe_session_id = query_params.get("session_id")

if stripe_session_id and 'payment_verified' not in st.session_state:
    with st.spinner("Validando sua troca energética e alinhando os mundos... ✨"):
        try:
            session = stripe.checkout.Session.retrieve(stripe_session_id)
            if session.payment_status == "paid":
                meta = session.metadata
                # Preenche o session_state com os dados do sonho
                st.session_state.user_name = meta.get("user_name")
                st.session_state.dream_title = meta.get("dream_title")
                st.session_state.dream_description = meta.get("dream_description")
                st.session_state.interpretation_style = meta.get("interpretation_style")

                st.session_state.payment_verified = True
                st.session_state.dream_step = 'result'
                st.query_params.clear()
                st.rerun()
            else:
                st.warning("O pagamento não foi concluído.")
                st.session_state.dream_step = 'payment'
                st.rerun()
        except Exception as e:
            st.error(f"Erro ao verificar pagamento: {e}")
            st.session_state.dream_step = 'welcome'
            st.rerun()
    st.stop()

# ==================== CABEÇALHO GLOBAL ====================
st.html("""
<div class="header-container">
    <h1 class="main-title">Portal dos Sonhos Ancestrais</h1>
    <p>Um oráculo para traduzir as mensagens da sua alma em sabedoria para sua jornada.</p>
</div>
""")
# ==========================================================


# Roteador de páginas
step = st.session_state.get('dream_step', 'welcome')

if step == 'welcome':
    page_welcome()
elif step == 'configure':
    page_configure()
elif step == 'payment':
    page_payment()
elif step == 'result':
    page_result()
else:
    page_welcome()
