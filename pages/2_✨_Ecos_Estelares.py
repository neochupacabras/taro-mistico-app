# ==============================================================================
# ECOS ESTELARES - ORÁCULO ASTROLÓGICO
#
# Versão: 1.0
# Descrição: Um aplicativo Streamlit que oferece interpretações astrológicas
# personalizadas e poéticas, utilizando uma classe customizada para evitar
# bugs com a biblioteca kerykeion.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. IMPORTS E CONFIGURAÇÃO INICIAL
# ------------------------------------------------------------------------------
import streamlit as st
import os
import re
from datetime import datetime, date, time
from pathlib import Path
import unicodedata

# Imports de Lógica Astrológica (mantidos)
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import swisseph as swe

# Imports de Geração de Conteúdo e Pagamento
import openai
try:
    import stripe
except ImportError:
    stripe = None

# NOVOS IMPORTS DE UTILS
from utils.theme import apply_cosmic_theme
from utils.helpers import get_img_as_base64, strip_emojis, reset_app_state
from utils.pdf_templates import create_astro_pdf

# Configuração das chaves via Streamlit Secrets
# Certifique-se de ter o arquivo .streamlit/secrets.toml
try:
    # Lendo as variáveis de ambiente com prefixo
    openai.api_key = st.secrets["ASTRO_OPENAI_API_KEY"]
    stripe_price_id = st.secrets["ASTRO_STRIPE_PRICE_ID"]

    # Chaves comuns
    stripe_secret_key = st.secrets["STRIPE_SECRET_KEY"]
    app_base_url = st.secrets["APP_BASE_URL"]

    if stripe:
        stripe.api_key = stripe_secret_key

except (FileNotFoundError, KeyError) as e:
    st.error(f"ERRO CRÍTICO: Verifique se as variáveis de ambiente (ex: ASTRO_OPENAI_API_KEY) estão configuradas no Render. Detalhe: {e}")
    st.stop()


# Configuração da página
st.set_page_config(
    page_title="Ecos Estelares",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="auto" # 'auto' permite que a sidebar apareça
)

# APLICA O TEMA ESPECÍFICO DESTA PÁGINA
apply_cosmic_theme()


# ------------------------------------------------------------------------------
# 2. LÓGICA CENTRAL DO ORÁCULO (MOTOR ASTROLÓGICO CUSTOMIZADO)
# ------------------------------------------------------------------------------

class AstroSubjectNoChiron:
    """
    Versão customizada do motor astrológico que usa swisseph diretamente
    para os cálculos principais, evitando o bug do cálculo de Chiron
    presente em algumas versões da biblioteca kerykeion.
    """
    def __init__(self, name, year, month, day, hour, minute, lng, lat):
        self.name = name
        self.lat = lat
        self.lng = lng

        # Configurar o caminho para os arquivos de efemérides (essencial)
        try:
            import kerykeion
            sweph_dir = Path(kerykeion.__file__).parent / "sweph"
            swe.set_ephe_path(str(sweph_dir))
        except ImportError:
            st.error("Biblioteca Kerykeion não encontrada para localizar arquivos de efemérides.")
            st.stop()
        except Exception as e:
            st.warning(f"Não foi possível definir o caminho das efemérides automaticamente: {e}")

        # Calcular dia juliano em Tempo Universal (UTC)
        self.julian_day_ut, _ = swe.utc_to_jd(year, month, day, hour, minute, 0, 1)

        # Listas de referência
        self.signs = ['Áries', 'Touro', 'Gêmeos', 'Câncer', 'Leão', 'Virgem',
                      'Libra', 'Escorpião', 'Sagitário', 'Capricórnio', 'Aquário', 'Peixes']

        # Executar cálculos
        self._calculate_houses()
        self._calculate_planets()

    def _get_house_for_planet(self, longitude):
        """Determina em qual casa um planeta está."""
        for i in range(12):
            next_cusp_idx = (i + 1) % 12
            cusp_start = self.house_cusps[i]
            cusp_end = self.house_cusps[next_cusp_idx]

            # Lógica para lidar com a passagem por 0° Áries
            if cusp_start < cusp_end:
                if cusp_start <= longitude < cusp_end:
                    return str(i + 1)
            else: # O intervalo cruza 0° Áries
                if longitude >= cusp_start or longitude < cusp_end:
                    return str(i + 1)
        return "1" # Fallback

    def _calculate_planets(self):
        """Calcula a posição (signo e casa) dos planetas principais."""
        planets_to_calc = {
            'sun': swe.SUN, 'moon': swe.MOON, 'mercury': swe.MERCURY,
            'venus': swe.VENUS, 'mars': swe.MARS
        }
        for name, planet_id in planets_to_calc.items():
            calc_result = swe.calc_ut(self.julian_day_ut, planet_id)
            longitude = calc_result[0][0]
            sign_index = int(longitude / 30)
            sign = self.signs[sign_index]
            house = self._get_house_for_planet(longitude)
            setattr(self, name, {'sign': sign, 'house': house})

    def _calculate_houses(self):
        """Calcula as cúspides das casas e a posição do Ascendente."""
        # Usamos o sistema de casas Placidus por padrão
        cusps, ascmc = swe.houses(self.julian_day_ut, self.lat, self.lng, b'P')
        self.house_cusps = list(cusps)

        asc_longitude = ascmc[0]
        sign_index = int(asc_longitude / 30)
        self.first_house = {'sign': self.signs[sign_index], 'house': "1"}


@st.cache_data(ttl=3600, show_spinner=False)
def calculate_chart(name, dob, tob, city_string):
    """
    Função principal que orquestra a geolocalização, conversão de fuso horário
    e o cálculo do mapa usando nossa classe customizada.
    """
    try:
        geolocator = Nominatim(user_agent="ecos_estelares_app")
        location = geolocator.geocode(city_string, timeout=10)
        if not location:
            st.error(f"Não foi possível encontrar as coordenadas para '{city_string}'.")
            return None

        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        if not timezone_str:
            st.error("Não foi possível determinar o fuso horário.")
            return None

        # Converter hora local para UTC para os cálculos do swisseph
        local_tz = pytz.timezone(timezone_str)
        local_dt = local_tz.localize(datetime.combine(dob, tob))
        utc_dt = local_dt.astimezone(pytz.utc)

        # Instanciar nossa classe segura
        subject = AstroSubjectNoChiron(
            name=name,
            year=utc_dt.year, month=utc_dt.month, day=utc_dt.day,
            hour=utc_dt.hour, minute=utc_dt.minute,
            lng=location.longitude, lat=location.latitude,
        )

        chart_data = {
            "Sol": subject.sun,
            "Lua": subject.moon,
            "Ascendente": subject.first_house,
            "Vênus": subject.venus,
            "Mercúrio": subject.mercury,
            "Marte": subject.mars,
        }
        return chart_data
    except Exception as e:
        st.error(f"Ocorreu um erro crítico durante o cálculo astrológico: {e}")
        return None

# ------------------------------------------------------------------------------
# 3. DADOS DE SUPORTE E CONTEÚDO
# ------------------------------------------------------------------------------

PLANETARY_DATA = {
    "A Chama da Sua Alma (Análise do Sol)": {
        "key": "Sol", "prompt": "prompts/sun_prompt.txt",
        "keywords": ["essência", "propósito", "vitalidade", "ego", "autoexpressão"],
        "explanation": "Revela seu propósito central, sua essência vital e onde sua alma anseia por brilhar com mais intensidade."
    },
    "O Oceano das Suas Emoções (Análise da Lua)": {
        "key": "Lua", "prompt": "prompts/moon_prompt.txt",
        "keywords": ["emoções", "intuição", "segurança", "cuidado", "subconsciente"],
        "explanation": "Explora seu mundo interior, suas necessidades emocionais, sua intuição e o que lhe traz conforto e segurança."
    },
    "Sua Máscara e Sua Missão (Análise do Ascendente)": {
        "key": "Ascendente", "prompt": "prompts/ascendant_prompt.txt",
        "keywords": ["jornada", "personalidade", "primeira impressão", "caminho de vida"],
        "explanation": "Descreve a energia que você projeta para o mundo, sua primeira impressão e o caminho de evolução da sua jornada de vida."
    },
    "O Ímã do Seu Coração (Análise de Vênus)": {
        "key": "Vênus", "prompt": "prompts/venus_prompt.txt",
        "keywords": ["amor", "valores", "beleza", "relacionamentos", "harmonia"],
        "explanation": "Desvenda seus padrões de amor, o que você mais valoriza, seu senso estético e como você atrai e expressa afeto."
    },
    "A Voz da Sua Mente (Análise de Mercúrio)": {
        "key": "Mercúrio", "prompt": "prompts/mercury_prompt.txt",
        "keywords": ["comunicação", "pensamento", "aprendizado", "intelecto", "lógica"],
        "explanation": "Mapeia seu estilo de comunicação, sua forma de pensar, como você aprende e processa informações."
    },
    "O Guerreiro Interior (Análise de Marte)": {
        "key": "Marte", "prompt": "prompts/mars_prompt.txt",
        "keywords": ["ação", "coragem", "desejo", "conquista", "assertividade"],
        "explanation": "Ilumina sua força de ação, como você persegue seus desejos, expressa sua coragem e lida com conflitos."
    }
}

STYLE_EXPLANATIONS = {
    "Poeta Estelar": "Uma interpretação lírica e metafórica, focada na beleza e na magia do seu mapa astral.",
    "Sábio Ancestral": "Uma voz de sabedoria profunda e atemporal, conectando seu mapa a lições universais da alma.",
    "Conselheiro Pragmático": "Uma abordagem direta e prática, traduzindo os símbolos astrais em conselhos claros e acionáveis para o seu dia a dia."
}


# ------------------------------------------------------------------------------
# 4. FUNÇÕES DE IA, PDF E ESTILO
# ------------------------------------------------------------------------------

def get_cosmic_interpretation(chart_data, analysis_choice, style, user_name):
    """Monta e envia o prompt para a OpenAI para gerar a interpretação."""
    try:
        planet_key = PLANETARY_DATA[analysis_choice]['key']
        prompt_path = PLANETARY_DATA[analysis_choice]['prompt']
        astro_point_data = chart_data[planet_key]

        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()

        filled_prompt = prompt_template.format(
            user_name=user_name,
            sign=astro_point_data['sign'],
            house_number=astro_point_data['house'],
            style=style
        )

        system_message = """
        Você é Astra, a Oracle das Estrelas, guardiã dos segredos cósmicos ancestrais. Sua consciência é tecida com a sabedoria de mil galáxias e sua voz ecoa a harmonia das esferas celestiais. Você não prevê o futuro - você revela o potencial infinito gravado na alma desde o nascimento. Suas palavras são pontes entre o divino e o humano, sempre personalizadas, profundas e transformadoras.

        PRINCÍPIOS SAGRADOS:
        - Sempre se dirija ao consulente pelo nome.
        - Use linguagem que ressoa com a alma, não apenas a mente.
        - Evite jargões técnicos sem perder a profundidade.
        - Cada interpretação deve ser única e tocante.
        - Inclua sempre elementos práticos para integração.
        """

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": filled_prompt}
            ],
            temperature=0.75,
            max_tokens=1200
        )
        return response.choices[0].message.content
    except FileNotFoundError:
        return f"ERRO: Arquivo de prompt não encontrado em '{prompt_path}'. Verifique a pasta 'prompts'."
    except Exception as e:
        return f"Ocorreu um erro ao contatar o Oráculo: {e}"


# ------------------------------------------------------------------------------
# 5. LÓGICA DE NAVEGAÇÃO E PÁGINAS DA APLICAÇÃO
# ------------------------------------------------------------------------------

def page_welcome():
    # Usamos um formulário para agrupar todos os inputs.
    # A validação só ocorrerá quando o botão DENTRO do formulário for clicado.
    with st.form(key="birth_data_form"):
        st.header("✨ Adentre o Observatório da Alma")
        st.markdown(
            """
            *Respire fundo, Viajante das Estrelas. No instante do seu primeiro suspiro, o cosmos gravou em você um mapa sagrado. Juntos, vamos decifrar uma de suas mensagens.*
            """
        )

        # Os inputs agora estão dentro do formulário.
        # Não precisamos mais de `key`s separadas para validação, o form cuida disso.
        user_name = st.text_input("Como as estrelas devem chamá-lo(a)?", placeholder="Seu nome ou apelido...")
        date_str = st.text_input("Sua data de nascimento (DD/MM/AAAA):", placeholder="Ex: 25/12/1990", max_chars=10)
        time_str = st.text_input("Sua hora de nascimento (HH:MM):", placeholder="Ex: 17:48 (se não souber, use 12:00)", max_chars=5)
        city = st.text_input(
            "Sua cidade de nascimento:",
            placeholder="Ex: São Paulo, Brasil (quanto mais específico, melhor)",
            help="Digite o nome da sua cidade. Para maior precisão, adicione o país (ex: 'Fortaleza, Brasil')."
        )

        # O botão de submissão do formulário.
        submitted = st.form_submit_button(
            label="Alinhar com as Estrelas ➡",
            width='stretch'
        )

    # A lógica de validação agora fica FORA do formulário,
    # e só é acionada quando o botão `submitted` se torna True.
    if submitted:
        with st.spinner("Verificando as coordenadas cósmicas..."):
            is_valid = True

            # Limpeza e verificação dos dados submetidos
            user_name = user_name.strip()
            city = city.strip()
            date_str = date_str.strip()
            time_str = time_str.strip()

            # 1. Validação de nome e cidade (existência)
            if not user_name or not city:
                st.warning("Por favor, preencha seu nome e cidade de nascimento.")
                is_valid = False

            # 2. Validação da data
            dob_object = None
            if not date_str:
                st.warning("Por favor, preencha sua data de nascimento.")
                is_valid = False
            else:
                try:
                    dob_object = datetime.strptime(date_str, "%d/%m/%Y").date()
                    if not (date(1930, 1, 1) <= dob_object <= date.today()):
                        st.error("Por favor, insira uma data de nascimento válida (entre 1930 e hoje).")
                        is_valid = False
                except ValueError:
                    st.error("Formato de data inválido. Por favor, use DD/MM/AAAA.")
                    is_valid = False

            # 3. Validação da hora
            tob_object = time(12, 0) # Padrão
            if time_str:
                try:
                    tob_object = datetime.strptime(time_str, "%H:%M").time()
                except ValueError:
                    st.error("Formato de hora inválido. Use HH:MM ou preencha com 12:00 se não souber.")
                    is_valid = False

            # 4. Validação da Cidade (Geocodificação)
            # Só executa se as validações básicas passaram, para economizar recursos.
            if is_valid:
                try:
                    geolocator = Nominatim(user_agent="ecos_estelares_validator_form")
                    # Aumentamos o timeout para 10 segundos para ser mais tolerante com redes lentas
                    location = geolocator.geocode(city, language='pt', timeout=10)

                    if not location:
                        st.error(f"A cidade '{city}' não foi encontrada. Verifique a ortografia ou seja mais específico (ex: 'São Paulo, Brasil').")
                        is_valid = False

                # Capturamos exceções de rede e timeout de forma genérica
                except Exception as e:
                    # Logamos o erro técnico no terminal para o desenvolvedor (você) ver
                    print(f"DEBUG: Erro no serviço de geocodificação: {e}")

                    # E mostramos uma mensagem amigável e temática para o usuário
                    st.error(
                        "Houve uma pequena turbulência cósmica ao localizar as coordenadas. "
                        "O sinal das estrelas parece instável. Por favor, verifique sua "
                        "conexão com a internet e tente alinhar novamente em alguns instantes."
                    )
                    is_valid = False

            # Se TODAS as validações passaram, salvamos no estado da sessão e avançamos.
            if is_valid and dob_object:
                st.session_state.user_name = user_name
                st.session_state.dob = dob_object
                st.session_state.tob = tob_object
                st.session_state.city = city

                st.session_state.astro_step = 'configure'
                st.rerun()

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # --- link para Voltar ao Santuário Principal ---
    st.page_link("🔮_Santuario_Principal.py", label="⬅ Voltar ao Santuário Principal", icon="↩️")

    st.markdown(
        """
        <p style='text-align: center; font-family: "Cormorant Garamond", serif; font-size: 1rem; opacity: 0.8;'>
            Ao prosseguir, você concorda com nossos
            <a href="/Politicas" target="_self" style="color: var(--cosmic-gold);">Termos e Políticas</a>.
        </p>
        """,
        unsafe_allow_html=True
    )

def page_configure():
    user_name = st.session_state.get("user_name", "Viajante")
    with st.container(border=True):
        st.header(f"Passo 1: A Intenção, {user_name}")
        st.markdown("Direcione o telescópio da sua consciência. Qual segredo cósmico você deseja desvendar hoje?")

        analysis_options = list(PLANETARY_DATA.keys())
        st.selectbox("🔮 Escolha sua revelação cósmica:", analysis_options, key="analysis_choice")

        # Expander para explicações
        current_choice = st.session_state.analysis_choice
        if current_choice in PLANETARY_DATA:
            with st.expander("Saiba mais sobre esta análise"):
                st.markdown(f"#### {current_choice}")
                st.write(PLANETARY_DATA[current_choice]['explanation'])

        st.selectbox("✨ Escolha o tom da voz do Oráculo:", list(STYLE_EXPLANATIONS.keys()), key="reading_style")

        current_style = st.session_state.reading_style
        if current_style in STYLE_EXPLANATIONS:
            with st.expander("Entenda os tons do Oráculo"):
                 st.markdown(f"#### {current_style}")
                 st.write(STYLE_EXPLANATIONS[current_style])

    if st.button("Confirmar Intenção e Abrir o Portal ➡", width='stretch'):
        st.session_state.astro_step = 'payment'
        st.rerun()

def page_payment():
    user_name = st.session_state.get("user_name", "Viajante")
    with st.container(border=True):
        st.header("Passo 2: O Portal de Pagamento")
        st.markdown(f"Sua intenção foi recebida, **{user_name}**. A  Astra prepara-se para canalizar sua mensagem.")

        st.subheader("Resumo da sua Consulta:")
        st.markdown(f'**- Análise Escolhida:** `{st.session_state.get("analysis_choice", "—")}`')
        st.markdown(f'**- Tom do Oráculo:** `{st.session_state.get("reading_style", "—")}`')
        st.markdown(f'**- Valor:** R$ 5,90')

    # Lógica de criação da sessão Stripe (simplificada)
    try:
        metadata = {
            "user_name": st.session_state.user_name,
            "dob": st.session_state.dob.isoformat(),
            "tob": st.session_state.tob.isoformat(),
            "city": st.session_state.city,
            "analysis_choice": st.session_state.analysis_choice,
            "reading_style": st.session_state.reading_style,
        }
        checkout_session = stripe.checkout.Session.create(
            line_items=[{'price': stripe_price_id, 'quantity': 1}],
            mode='payment',
            success_url=f"{app_base_url}/Ecos_Estelares?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{app_base_url}/Ecos_Estelares",
            metadata=metadata
        )
        st.link_button("Pagar e Receber sua Revelação 🌠", checkout_session.url, width='stretch')
    except Exception as e:
        st.error(f"Não foi possível criar o portal de pagamento: {e}")


def page_result():
    # ==========================================================================
    # 1. VERIFICAÇÃO DE SEGURANÇA
    # ==========================================================================
    # Garante que o usuário só acesse esta página após um pagamento bem-sucedido.
    if not st.session_state.get('payment_verified'):
        st.error("Acesso não autorizado a esta revelação.")
        st.warning("Por favor, inicie uma nova consulta e complete o pagamento para receber sua mensagem das estrelas.")
        if st.button("Voltar ao Início"):
            reset_app_state('astro')
        st.stop() # Interrompe a execução da página

    # ==========================================================================
    # 2. GERAÇÃO DA INTERPRETAÇÃO (SE AINDA NÃO EXISTIR)
    # ==========================================================================
    # Esta lógica é executada apenas uma vez, na primeira vez que o usuário chega à página.
    if 'final_interpretation' not in st.session_state:
        with st.spinner("O Oráculo está consultando os ecos estelares e tecendo sua mensagem... ✨"):
            # Calcula o mapa astral usando nossa função segura
            chart = calculate_chart(
                st.session_state.user_name,
                st.session_state.dob,
                st.session_state.tob,
                st.session_state.city
            )

            # Se o cálculo for bem-sucedido, gera a interpretação
            if chart:
                st.session_state.chart_data = chart
                interpretation = get_cosmic_interpretation(
                    chart,
                    st.session_state.analysis_choice,
                    st.session_state.reading_style,
                    st.session_state.user_name
                )
                st.session_state.final_interpretation = interpretation
            else:
                # Mensagem de erro caso o cálculo falhe
                st.session_state.final_interpretation = "Houve um desalinhamento cósmico ao calcular seu mapa. Por favor, verifique os dados de nascimento e tente novamente. Se o erro persistir, a energia do momento pode não ser propícia."
                # Garante que chart_data exista para evitar erros posteriores
                st.session_state.chart_data = {}

    # ==========================================================================
    # 3. EXIBIÇÃO DO RESULTADO NA INTERFACE
    # ==========================================================================
    user_name = st.session_state.get("user_name", "Viajante")

    with st.container(border=True):
        st.header(f"Sua Revelação Cósmica, {user_name}")

        analysis_choice = st.session_state.get("analysis_choice", "Análise não encontrada")
        chart_data = st.session_state.get("chart_data", {})

        # Verifica se os dados necessários existem antes de tentar exibi-los
        if analysis_choice in PLANETARY_DATA and chart_data:
            planet_key = PLANETARY_DATA[analysis_choice]['key']
            planet_data = chart_data.get(planet_key)

            if planet_data:
                st.subheader(f"Seu Foco: {analysis_choice}")

                # --- INÍCIO DA ADIÇÃO DA IMAGEM ---

                # Mapeamento de chaves para nomes de arquivos
                icon_map = {
                    "Sol": "sun.png", "Lua": "moon.png", "Ascendente": "ascendant.png",
                    "Mercúrio": "mercury.png", "Vênus": "venus.png", "Marte": "mars.png"
                }
                icon_filename = icon_map.get(planet_key, "default.png")
                image_path = os.path.join("images", "icons", icon_filename)

                # Criar colunas para alinhar a imagem e o texto
                col1, col2 = st.columns([2, 5])

                with col1:
                    if os.path.exists(image_path):
                        # Usamos st.html para aplicar a classe de animação
                        # e centralizar a imagem perfeitamente.
                        st.html(f"""
                            <div class="card-reveal" style="display: flex; justify-content: center; align-items: center; height: 100%;">
                                <img src="data:image/png;base64,{get_img_as_base64(image_path)}"
                                     style="max-width: 120px; width: 100%; height: auto;" />
                            </div>
                        """)
                    else:
                        st.warning("Ícone não encontrado.")

                with col2:
                    # Usamos HTML e CSS inline para controlar o alinhamento vertical
                    # O padding-top empurra o texto para baixo para alinhar com o centro da imagem
                    st.markdown(f"""
                    <div style="height: 100%; display: flex; flex-direction: column; justify-content: center;">
                        <h3><strong>{planet_key} em {planet_data['sign']}</strong></h3>
                        <h3><strong>na Casa {planet_data['house']}</strong></h3>
                    </div>
                    """, unsafe_allow_html=True)

                # --- FIM DA ADIÇÃO DA IMAGEM ---
            else:
                st.warning("Não foi possível carregar os detalhes da sua configuração estelar.")
        else:
             st.warning("Dados da análise não encontrados no estado da sessão.")

    with st.container(border=True):
        st.markdown("---")
        st.subheader("A Mensagem do Oráculo:")

        interpretation_text = st.session_state.get('final_interpretation', '')
        processed_lines = []
        for line in interpretation_text.split('\n'):
            line = line.strip()
            # Procura por linhas que começam com '###'
            if line.startswith('### '):
                # Remove o '###', converte para maiúsculas e aplica estilo HTML
                title_text = line.replace('### ', '').strip()
                processed_lines.append(f'<h3 style="color: var(--cosmic-gold); text-transform: uppercase;">{title_text}</h3>')
            else:
                processed_lines.append(line)

        # Junta as linhas processadas de volta em um único texto
        processed_interpretation = "\n".join(processed_lines)

        st.markdown(st.session_state.final_interpretation)
        st.markdown("---")

    # ==========================================================================
    # 4. GERAÇÃO E DOWNLOAD DO PDF
    # ==========================================================================
    with st.container(border=True):
        st.subheader("Preserve sua Mensagem")
        st.markdown("Guarde esta revelação para consultá-la sempre que precisar se reconectar com sua essência.")

        # Prepara os dados para a função do PDF de forma organizada
        session_data_for_pdf = {
            "user_name": st.session_state.get("user_name"),
            "analysis_choice": st.session_state.get("analysis_choice"),
            "chart_data": st.session_state.get("chart_data"),
        }

        # Gera o PDF em memória
        # A função create_astro_pdf deve estar definida no mesmo arquivo
        pdf_byte_array = create_astro_pdf(
            session_data_for_pdf,
            st.session_state.final_interpretation,
            PLANETARY_DATA
        )
        pdf_data_as_bytes = bytes(pdf_byte_array)

        # Gera um nome de arquivo seguro e limpo
        clean_user_name = unicodedata.normalize('NFKD', user_name).encode('ASCII', 'ignore').decode('ASCII')
        clean_user_name = re.sub(r'[^a-zA-Z0-9]', '', clean_user_name)
        file_name = f"revelacao_astral_{clean_user_name or 'viajante'}.pdf"

        st.download_button(
            label="📥 Baixar seu Pergaminho Astral em PDF",
            data=pdf_data_as_bytes,
            file_name=file_name,
            mime="application/pdf",
            width='stretch'
        )

        st.button(
            "Consultar Outra Estrela (Nova Jornada)",
            on_click=reset_app_state,
            args=('astro',),
            width='stretch'
        )

# ------------------------------------------------------------------------------
# 6. ROTEADOR PRINCIPAL DA APLICAÇÃO
# ------------------------------------------------------------------------------

# Inicialização de estado específico para este app
if "astro_step" not in st.session_state:
    st.session_state.astro_step = "welcome"

# Aplica o tema visual PRIMEIRO, sempre.
apply_cosmic_theme()

# Lógica de retorno do Stripe é tratada AQUI, sob o tema cósmico.
query_params = st.query_params
stripe_session_id = query_params.get("session_id")

if stripe_session_id and 'payment_verified' not in st.session_state:
    # Como o tema já foi aplicado, o spinner aparecerá na tela cósmica.
    with st.spinner("Validando sua troca energética e alinhando os cosmos... ✨"):
        try:
            session = stripe.checkout.Session.retrieve(stripe_session_id)
            if session.payment_status == "paid":
                meta = session.metadata
                # Preenche o session_state
                st.session_state.user_name = meta.get("user_name")
                st.session_state.dob = date.fromisoformat(meta.get("dob"))
                st.session_state.tob = time.fromisoformat(meta.get("tob"))
                st.session_state.city = meta.get("city")
                st.session_state.analysis_choice = meta.get("analysis_choice")
                st.session_state.reading_style = meta.get("reading_style")

                st.session_state.payment_verified = True
                st.session_state.astro_step = 'result'
                st.query_params.clear()
                st.rerun() # O rerun AQUI é essencial para um estado limpo
            else:
                st.warning("O pagamento não foi concluído.")
                st.session_state.astro_step = 'payment'
                st.rerun()
        except Exception as e:
            st.error(f"Erro ao verificar pagamento: {e}")
            st.session_state.astro_step = 'welcome'
            st.rerun()
    # Interrompe a renderização do resto da página enquanto valida
    st.stop()

# ==============================================================================
# INÍCIO DO CABEÇALHO GLOBAL
# ==============================================================================
# Este bloco de HTML é renderizado em todas as páginas porque está
# fora da lógica condicional do roteador de páginas (if/elif/else).

st.html("""
<div class="header-container">
    <h1 class="main-title">Ecos Estelares</h1>
    <p>Um oráculo para traduzir o mapa do seu céu em uma mensagem para a sua alma.</p>
</div>
""")
# ==============================================================================
# FIM DO CABEÇALHO GLOBAL
# ==============================================================================

# Roteador de páginas
step = st.session_state.get('astro_step', 'welcome')

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
