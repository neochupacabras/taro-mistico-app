# utils/theme.py
import streamlit as st

# <<< ADICIONE ESTA LINHA
from .helpers import get_img_as_base64

def apply_mystical_theme():
    """Aplica o tema visual místico avançado e imersivo à aplicação."""
    # img = get_img_as_base64("images/pergaminho.png")
    fallback_gradient = "linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 75%, #000000 100%)"

    st.html(f"""
    <style>
        /* ==================== IMPORTAÇÃO DE FONTES ==================== */
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Cormorant+Garamond:ital,wght@0,400;1,400&display=swap');

        /* ==================== VARIÁVEIS CSS CUSTOMIZADAS ==================== */
        :root {{
            --primary-gold: #d4af37;
            --secondary-gold: #f4e4a6;
            --deep-purple: #2e1a47;
            --mystic-blue: #1e3a5f;
            --dark-bg: #0f0f23;
            --card-shadow: 0 15px 40px rgba(212, 175, 55, 0.15);
            --text-light: #f5f5dc; /* Cor bege/branca para textos claros */
            --text-muted: #b8860b;
            --border-mystical: 2px solid rgba(212, 175, 55, 0.3);
        }}

        /* ==================== BACKGROUND E ESTRUTURA PRINCIPAL ==================== */
        .stApp {{
            /* <<< CORREÇÃO 2: Aplica o gradiente diretamente, sem a imagem >>> */
            background: {fallback_gradient};
            background-attachment: fixed; /* Mantém o gradiente fixo ao rolar */
        }}

        .stApp::before {{
            content: '';
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: linear-gradient(45deg, rgba(15, 15, 35, 0.85) 0%, rgba(46, 26, 71, 0.75) 50%, rgba(0, 0, 0, 0.9) 100%);
            pointer-events: none;
            z-index: -1;
        }}

        /* ==================== TIPOGRAFIA MÍSTICA ==================== */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Cinzel', serif !important;
            color: var(--primary-gold) !important;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.5), 0 0 10px rgba(212, 175, 55, 0.5), 0 0 20px rgba(212, 175, 55, 0.3);
            letter-spacing: 1px;
        }}

        h1 {{ font-size: 3.5rem !important; font-weight: 700 !important; text-align: center; margin-bottom: 0.5rem !important; padding-bottom: 0 !important; border-bottom: none !important; }}
        h2 {{ font-size: 2.2rem !important; font-weight: 600 !important; border-bottom: 2px solid rgba(212, 175, 55, 0.3); padding-bottom: 0.5rem; }}
        h3 {{ font-size: 1.8rem !important; font-weight: 500 !important; color: var(--secondary-gold) !important; }}

        /* Regra de fonte segura que já corrigiu o ícone do expander */
        .st-emotion-cache-1629p8f p, .stMarkdown p, .stMarkdown li, .sttextinput_label, .sttextarea_label, .stselectbox_label, div[data-baseweb="select"] > div, [data-testid="stExpander"] summary, .stButton > button, [data-testid="stDownloadButton"] button div, [data-testid="stAlert"] div[role="alert"] {{
            font-family: 'Cormorant Garamond', serif !important;
            color: var(--text-light) !important;
            font-size: 1.2rem !important;
            line-height: 1.7 !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
        }}
        .stButton > button, [data-testid="stDownloadButton"] button {{ font-family: 'Cinzel', serif !important; }}

        /* CORREÇÃO PARA O SUBTÍTULO DO CABEÇALHO */
        .header-container p {{
            color: var(--text-light) !important;
            font-family: 'Cormorant Garamond', serif !important;
            font-size: 1.1rem !important;
            font-style: italic !important;
            text-align: center;
            margin-top: -1rem;
            margin-bottom: 0;
        }}

        /* <<< CORREÇÃO FINAL: Cor dos rótulos dos widgets >>> */
        /* Esta regra força os labels dos widgets a usarem a nossa cor de texto clara. */
        [data-testid="stWidgetLabel"] p {{
            color: var(--text-light) !important;
            font-size: 1.2rem !important; /* Mantém o tamanho consistente */
        }}

        /* <<< NOVA REGRA: Cor do texto do Spinner >>> */
        [data-testid="stSpinner"] > div {{
            color: var(--text-light) !important;
            font-family: 'Cormorant Garamond', serif !important;
            font-size: 1.2rem !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7) !important;
        }}

        /* ==================== CONTAINERS E CARDS MÍSTICOS (SOLUÇÃO CORRIGIDA) ==================== */

        /* Regra para o cabeçalho, que já funciona bem */
        .header-container {{
            background: linear-gradient(160deg, rgba(46, 26, 71, 0.95) 0%, rgba(26, 26, 46, 0.9) 70%, rgba(15, 15, 35, 0.95) 100%) !important;
            border: var(--border-mystical) !important;
            border-radius: 15px !important;
            box-shadow: var(--card-shadow) !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
        }}

        /* SOLUÇÃO CORRIGIDA: Usando o seletor correto para containers com bordas arredondadas */
        .stVerticalBlock[style*="border-radius"] {{
            background: linear-gradient(160deg, rgba(46, 26, 71, 0.95) 0%, rgba(26, 26, 46, 0.9) 70%, rgba(15, 15, 35, 0.95) 100%) !important;
            border: var(--border-mystical) !important;
            border-radius: 15px !important;
            box-shadow: var(--card-shadow) !important;
            backdrop-filter: blur(5px) !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            position: relative !important;
        }}

        /* Alternativa: Todos os .stVerticalBlock (caso o filtro acima não funcione) */
        .stVerticalBlock {{
            background: linear-gradient(160deg, rgba(46, 26, 71, 0.95) 0%, rgba(26, 26, 46, 0.9) 70%, rgba(15, 15, 35, 0.95) 100%) !important;
            border: var(--border-mystical) !important;
            border-radius: 15px !important;
            box-shadow: var(--card-shadow) !important;
            backdrop-filter: blur(5px) !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            position: relative !important;
        }}

        /* Garantir que o conteúdo dos containers fique visível */
        .stVerticalBlock > div {{
            position: relative !important;
            z-index: 1 !important;
        }}

        /* ==================== BOTÕES MÍSTICOS AVANÇADOS ==================== */
        .stButton > button, [data-testid="stDownloadButton"] button {{
            background: linear-gradient(145deg, var(--deep-purple) 0%, var(--mystic-blue) 50%, var(--deep-purple) 100%) !important;
            color: var(--primary-gold) !important; border: 2px solid var(--primary-gold) !important; border-radius: 25px !important;
            font-family: 'Cinzel', serif !important; font-size: 1.1rem !important; font-weight: 500 !important;
            padding: 0.8rem 2rem !important; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100%; position: relative;
        }}
        .stButton > button:hover, [data-testid="stDownloadButton"] button:hover {{
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 15px 35px rgba(212, 175, 55, 0.3) !important;
            border-color: var(--secondary-gold) !important;
        }}
        [data-testid="stDownloadButton"] button a {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; text-indent: -9999px; z-index: 1; }}
        [data-testid="stDownloadButton"] button div {{ color: var(--primary-gold) !important; z-index: 2; position: relative; }}
        [data-testid="stDownloadButton"] button:hover div {{ color: var(--secondary-gold) !important; }}

        /* <<< Estilo do st.page_link >>> */
        [data-testid="stPageLink"] a p {{
            color: var(--text-light) !important; /* Cor branca para a label */
            font-weight: 700 !important; /* Opcional: dá mais destaque */
            text-decoration: underline; /* Opcional: deixa claro que é um link */
        }}
        [data-testid="stPageLink"] a:hover p {{
            color: var(--primary-gold) !important; /* Opcional: muda de cor no hover */
        }}

        /* ==================== EXPANDER MÍSTICO (ACORDEÃO) - VERSÃO LIMPA ==================== */
        [data-testid="stExpander"] {{
            border-color: rgba(212, 175, 55, 0.4) !important;
            transition: all 0.3s ease-in-out !important;
            background: transparent !important;
        }}

        [data-testid="stExpander"]:hover {{
            border-color: var(--primary-gold) !important;
            box-shadow: 0 0 10px rgba(212, 175, 55, 0.2) !important;
        }}

        /* Cabeçalho do expander - estilo limpo */
        [data-testid="stExpander"] summary {{
            color: var(--secondary-gold) !important;
            font-style: italic !important;
            background: transparent !important;
            padding: 0.75rem !important;
        }}

        /* Ícone do expander */
        [data-testid="stExpander"] summary svg {{
            fill: var(--primary-gold) !important;
        }}

        /* CORREÇÃO: Remove qualquer fundo branco/sobreposição */
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"][open] > summary,
        [data-testid="stExpander"][open] > summary:hover,
        [data-testid="stExpander"][open] > summary:focus,
        [data-testid="stExpander"][open] > summary:active {{
            background-color: transparent !important;
            background-image: none !important;
            box-shadow: none !important;
            border: none !important;
        }}

        /* Remove qualquer pseudo-elemento que possa estar causando duplicação */
        [data-testid="stExpander"] summary::before,
        [data-testid="stExpander"] summary::after {{
            display: none !important;
        }}

        /* Garante que o conteúdo interno tenha fundo sutil */
        [data-testid="stExpander"] > div:last-child {{
            background: rgba(15, 15, 35, 0.2) !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            margin-top: 0.5rem !important;
        }}

        /* ==================== CAMPOS DE ENTRADA MÍSTICOS ==================== */
        .stTextInput input, .stTextArea textarea {{
            background: linear-gradient(145deg, rgba(15, 15, 35, 0.8) 0%, rgba(46, 26, 71, 0.6) 100%) !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important; border-radius: 10px !important;
            color: var(--text-light) !important; caret-color: var(--primary-gold) !important;
        }}
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {{ color: var(--text-muted) !important; font-style: italic; }}
        .stSelectbox > div > div {{
            background: linear-gradient(145deg, rgba(15, 15, 35, 0.9) 0%, rgba(46, 26, 71, 0.7) 100%) !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important; border-radius: 10px !important;
        }}

        /* ==================== SELECTBOX DROPDOWN (OPÇÕES) ==================== */
        div[data-baseweb="popover"] {{
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}

        div[data-baseweb="popover"] ul {{
            background: linear-gradient(160deg, var(--deep-purple) 0%, #1a1a2e 70%, #0f0f23 100%) !important;
            border: 2px solid var(--primary-gold) !important;
            border-radius: 10px !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5) !important;
            padding: 0.5rem 0 !important;
        }}

        div[data-baseweb="popover"] li {{
            font-family: 'Cormorant Garamond', serif !important;
            color: var(--text-light) !important;
            transition: background-color 0.2s ease-in-out !important;
            padding: 0.75rem 1.5rem !important;
        }}

        div[data-baseweb="popover"] li:hover,
        div[data-baseweb="popover"] li[aria-selected="true"] {{
            background-color: rgba(212, 175, 55, 0.25) !important;
            color: var(--secondary-gold) !important;
        }}

        /* ==================== ALERTAS E NOTIFICAÇÕES MÍSTICAS ==================== */
        [data-testid="stAlert"] {{
            background: linear-gradient(145deg, rgba(46, 26, 71, 0.85) 0%, rgba(15, 15, 35, 0.95) 100%) !important;
            border: 2px solid var(--primary-gold) !important;
            border-radius: 10px !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5) !important;
            padding: 1rem 1.5rem !important;
        }}

        [data-testid="stAlert"] div[role="alert"] {{
            color: var(--text-light) !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
            font-family: 'Cormorant Garamond', serif !important;
            font-size: 1.1rem !important;
        }}

        /* ==================== CARDS DE TARÔ MÁGICOS ==================== */
        .stImage > img {{
            border-radius: 15px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(212, 175, 55, 0.2) !important;
            border: 3px solid var(--primary-gold) !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        .stImage:hover > img {{ transform: translateY(-5px) scale(1.03) !important; }}
        button[aria-label="View fullscreen"] {{ display: none !important; }}

        /* ==================== EFEITOS ESPECIAIS ==================== */
        .main-title {{
            background: linear-gradient(45deg, var(--primary-gold), var(--secondary-gold), var(--primary-gold));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; background-size: 200% 200%;
            animation: gradientShift 3s ease infinite;
        }}
        @keyframes gradientShift {{ 0%, 100% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} }}

        .payment-button-container {{
            background: linear-gradient(145deg, var(--secondary-gold) 0%, var(--primary-gold) 50%, var(--secondary-gold) 100%) !important;
            background-size: 200% auto !important;
            color: var(--deep-purple) !important;
            font-family: 'Cinzel', serif !important;
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            border: 2px solid var(--primary-gold) !important;
            border-radius: 50px !important;
            padding: 1rem 2.5rem !important;
            text-align: center !important;
            text-shadow: none !important;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), 0 0 15px rgba(244, 228, 166, 0.4) !important;
            transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
            display: block !important;
        }}

        .payment-button-container:hover {{
            transform: translateY(-4px) scale(1.03) !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4), 0 0 25px rgba(244, 228, 166, 0.7), 0 0 40px rgba(212, 175, 55, 0.5) !important;
            background-position: right center !important;
        }}

        .card-reveal {{ animation: cardReveal 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards; opacity: 0; }}
        @keyframes cardReveal {{ from {{ transform: rotateY(90deg) scale(0.8); opacity: 0; }} to {{ transform: rotateY(0deg) scale(1); opacity: 1; }} }}

        [data-testid="column"]:nth-child(1) .card-reveal {{ animation-delay: 0.1s; }}
        [data-testid="column"]:nth-child(2) .card-reveal {{ animation-delay: 0.3s; }}
        [data-testid="column"]:nth-child(3) .card-reveal {{ animation-delay: 0.5s; }}

        /* ==================== FORÇAR VISIBILIDADE DOS CONTAINERS (ÚLTIMA LINHA DE DEFESA) ==================== */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            opacity: 1 !important;
            visibility: visible !important;
        }}

        /* ==================== OCULTAR ELEMENTOS PADRÃO DO STREAMLIT ==================== */
        /* Oculta o cabeçalho que contém o menu hambúrguer e a faixa branca */
        header {{
            display: none !important;
        }}

        /* Oculta o rodapé "Made with Streamlit" */
        footer {{
            display: none !important;
        }}

        /* ==================== OCULTAR BARRA LATERAL ==================== */
        /* Esconde a barra lateral de navegação para uma experiência imersiva */
        [data-testid="stSidebar"] {{
            display: none;
        }}
    </style>
    """)



def apply_cosmic_theme():
    """Aplica o tema visual dos Ecos Estelares - Portal Cósmico com tons de azul galáctico."""
    # img = get_img_as_base64("images/pergaminho.png")
    # Gradiente cósmico profundo inspirado no universo noturno, agora com base azul
    fallback_gradient = "radial-gradient(ellipse at center top, #001f5c 0%, #16213e 30%, #0d1421 60%, #000511 100%)"

    st.html(f"""
    <style>
        /* ==================== IMPORTAÇÃO DE FONTES ESTELARES ==================== */
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,400&family=EB+Garamond:ital,wght@0,400;1,400&display=swap');

        /* ==================== VARIÁVEIS CÓSMICAS DOS ECOS ESTELARES (TEMA AZUL) ==================== */
        :root {{
            /* Paleta Estelar Principal */
            --cosmic-gold: #ffd700;
            --stardust-silver: #e6e6fa;
            --galaxy-blue-deep: #001f5c;   /* Substitui o roxo profundo */
            --galaxy-blue-medium: #1e5288; /* Um azul médio para gradientes */
            --starlight-cyan: #00bfff;     /* Ciano para brilhos, substitui o rosa */
            --deep-void: #020412;         /* Um preto ainda mais profundo e azulado */
            --celestial-white: #f8f8ff;

            /* Cores dos Planetas (mantidas) */
            --sun-gold: #ffb347;
            --moon-silver: #c0c0c0;
            --mercury-copper: #cd7f32;
            --venus-rose: #ffc0cb;
            --mars-red: #cd5c5c;

            /* Sombras e Efeitos com base azul */
            --stellar-shadow: 0 8px 32px rgba(255, 215, 0, 0.2), 0 0 40px rgba(0, 31, 92, 0.4);
            --portal-glow: 0 0 30px rgba(255, 215, 0, 0.5), 0 0 60px rgba(255, 215, 0, 0.3), 0 0 90px rgba(0, 191, 255, 0.2);
            --cosmic-border: 2px solid rgba(255, 215, 0, 0.6);
            --ethereal-backdrop: backdrop-filter: blur(10px) saturate(150%);
        }}

        /* ==================== PORTAL CÓSMICO - FUNDO UNIVERSAL ==================== */
        .stApp {{
            background:
                       radial-gradient(ellipse at 20% 80%, rgba(0, 191, 255, 0.1) 0%, transparent 50%),
                       radial-gradient(ellipse at 80% 20%, rgba(30, 82, 136, 0.15) 0%, transparent 50%),
                       radial-gradient(ellipse at 40% 40%, rgba(0, 31, 92, 0.25) 0%, transparent 70%),
                       linear-gradient(135deg, var(--deep-void) 0%, #0d1421 25%, #16213e 50%, var(--galaxy-blue-deep) 75%, var(--deep-void) 100%);
            min-height: 100vh;
            position: relative;
        }}

        /* Véu Etéreo sobre o Cosmos */
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background:
                radial-gradient(circle at 10% 10%, rgba(255, 215, 0, 0.05) 0%, transparent 25%),
                radial-gradient(circle at 90% 90%, rgba(0, 191, 255, 0.08) 0%, transparent 30%),
                radial-gradient(circle at 50% 50%, rgba(0, 31, 92, 0.1) 0%, transparent 40%);
            pointer-events: none;
            z-index: -1;
            animation: cosmicPulse 8s ease-in-out infinite alternate;
        }}

        @keyframes cosmicPulse {{
            0% {{ opacity: 0.3; }}
            100% {{ opacity: 0.7; }}
        }}

        /* ==================== TIPOGRAFIA CELESTIAL ==================== */
        /* A tipografia com dourado e prata permanece, pois combina perfeitamente com o azul */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Cinzel', serif !important;
            background: linear-gradient(45deg, var(--cosmic-gold), var(--stardust-silver), var(--cosmic-gold));
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
            letter-spacing: 2px;
            animation: stellarShimmer 6s ease-in-out infinite;
        }}

        @keyframes stellarShimmer {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}

        h1 {{
            font-size: 3.8rem !important;
            font-weight: 700 !important;
            text-align: center;
            margin: 2rem 0 !important;
            filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.5));
        }}

        h2 {{
            font-size: 2.4rem !important;
            font-weight: 500 !important;
            border-bottom: 2px solid rgba(255, 215, 0, 0.4);
            padding-bottom: 0.8rem;
            margin-bottom: 1.5rem;
        }}

        h3 {{
            font-size: 1.9rem !important;
            font-weight: 400 !important;
            color: var(--stardust-silver) !important;
        }}

        /* Texto Contemplativo */
        .st-emotion-cache-1629p8f p, .stMarkdown p, .stMarkdown li,
        .sttextinput_label, .sttextarea_label, .stselectbox_label,
        div[data-baseweb="select"] > div, [data-testid="stExpander"] summary,
        .stButton > button, [data-testid="stDownloadButton"] button div,
        [data-testid="stAlert"] div[role="alert"] {{
            font-family: 'Cormorant Garamond', serif !important;
            color: var(--celestial-white) !important;
            font-size: 1.25rem !important;
            line-height: 1.8 !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8), 0 0 10px rgba(248, 248, 255, 0.1);
            font-weight: 400;
        }}

        /* Subtítulo Poético */
        .header-container p {{
            color: var(--stardust-silver) !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.2rem !important;
            font-style: italic !important;
            text-align: center;
            margin-top: -1rem;
            opacity: 0.9;
        }}

        /* Rótulos dos Oráculos */
        [data-testid="stWidgetLabel"] p {{
            color: var(--stardust-silver) !important;
            font-size: 1.3rem !important;
            font-weight: 500 !important;
            text-shadow: 0 0 8px rgba(230, 230, 250, 0.3);
        }}

        /* Mensagem do Portal */
        [data-testid="stSpinner"] > div {{
            color: var(--cosmic-gold) !important;
            font-family: 'Cormorant Garamond', serif !important;
            font-size: 1.3rem !important;
            font-style: italic !important;
            text-shadow: 0 0 15px rgba(255, 215, 0, 0.6) !important;
        }}

        /* ==================== CARTÕES CELESTIAIS (CONTAINERS) ==================== */
        .header-container {{
            background: linear-gradient(160deg,
                rgba(0, 31, 92, 0.35) 0%,      /* Roxo substituído por azul */
                rgba(30, 82, 136, 0.25) 40%,    /* Azul médio */
                rgba(2, 4, 18, 0.3) 100%) !important; /* Fundo mais azulado */
            border: var(--cosmic-border) !important;
            border-radius: 20px !important;
            box-shadow: var(--stellar-shadow) !important;
            backdrop-filter: blur(15px) saturate(120%) !important;
            padding: 2rem !important;
            margin: 1.5rem 0 !important;
            position: relative !important;
        }}

        .header-container::before {{
            content: '';
            position: absolute;
            top: -1px; left: -1px; right: -1px; bottom: -1px;
            background: linear-gradient(45deg,
                transparent,
                rgba(255, 215, 0, 0.3),
                transparent,
                rgba(0, 191, 255, 0.25),      /* Rosa substituído por ciano */
                transparent);
            border-radius: 20px;
            z-index: -1;
            animation: borderGlow 4s linear infinite;
        }}

        @keyframes borderGlow {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        /* Containers dos Oráculos */
        .stVerticalBlock[style*="border-radius"], .stVerticalBlock {{
            background: linear-gradient(160deg,
                rgba(0, 31, 92, 0.2) 0%,      /* Roxo substituído por azul */
                rgba(30, 82, 136, 0.15) 40%,
                rgba(2, 4, 18, 0.25) 100%) !important;
            border: 1px solid rgba(255, 215, 0, 0.3) !important;
            border-radius: 18px !important;
            box-shadow:
                0 8px 32px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(12px) saturate(110%) !important;
            padding: 2rem !important;
            margin: 1.2rem 0 !important;
            position: relative !important;
            transition: all 0.3s ease-in-out !important;
        }}

        .stVerticalBlock:hover {{
            border-color: rgba(255, 215, 0, 0.6) !important;
            box-shadow:
                0 12px 40px rgba(0, 0, 0, 0.5),
                0 0 20px rgba(255, 215, 0, 0.2) !important;
            transform: translateY(-2px) !important;
        }}

        /* ==================== BOTÕES DO PORTAL CÓSMICO ==================== */
        [data-testid="stFormSubmitButton"] button,
        .stButton > button, [data-testid="stDownloadButton"] button {{
            background: linear-gradient(135deg,
                var(--galaxy-blue-deep) 0%,
                var(--galaxy-blue-medium) 50%,
                var(--galaxy-blue-deep) 100%) !important;
            color: var(--cosmic-gold) !important;
            border: 2px solid rgba(255, 215, 0, 0.6) !important;
            border-radius: 30px !important;
            font-family: 'Cinzel', serif !important;
            font-size: 1.15rem !important;
            font-weight: 500 !important;
            padding: 1rem 2.5rem !important;
            width: 100% !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow:
                0 4px 15px rgba(0, 31, 92, 0.5), /* Sombra azulada */
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        }}

        [data-testid="stLinkButton"] a {{
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            text-decoration: none !important;
            width: 100%;
        }}

        .stButton > button::before {{
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg,
                transparent,
                rgba(255, 215, 0, 0.2),
                transparent);
            transition: left 0.6s ease;
        }}

        .stButton > button:hover::before {{
            left: 100%;
        }}

        .stButton > button:hover, [data-testid="stDownloadButton"] button:hover {{
            transform: translateY(-3px) scale(1.02) !important;
            border-color: var(--cosmic-gold) !important;
            box-shadow:
                0 8px 25px rgba(0, 31, 92, 0.7), /* Sombra azulada mais forte */
                0 0 30px rgba(255, 215, 0, 0.3) !important;
            color: var(--stardust-silver) !important;
        }}

        /* Link Cósmico (st.page_link) */
        [data-testid="stPageLink"] a p {{
            color: var(--cosmic-gold) !important;
            font-weight: 500 !important;
            text-decoration: none !important;
            border-bottom: 1px dotted rgba(255, 215, 0, 0.5) !important;
            transition: all 0.3s ease !important;
        }}

        [data-testid="stPageLink"] a:hover p {{
            color: var(--stardust-silver) !important;
            border-bottom-color: var(--stardust-silver) !important;
            text-shadow: 0 0 8px rgba(230, 230, 250, 0.5) !important;
        }}

        /* ==================== REVELAÇÂO MÍSTICA (EXPANDER) ==================== */
        [data-testid="stExpander"] {{
            border: 1px solid rgba(255, 215, 0, 0.4) !important;
            border-radius: 15px !important;
            background: linear-gradient(145deg,
                rgba(0, 31, 92, 0.15) 0%,   /* Roxo substituído por azul */
                rgba(2, 4, 18, 0.2) 100%) !important;
            transition: all 0.4s ease-in-out !important;
            overflow: hidden !important;
        }}

        [data-testid="stExpander"]:hover {{
            border-color: var(--cosmic-gold) !important;
            box-shadow: var(--portal-glow) !important;
        }}

        [data-testid="stExpander"] summary {{
            color: var(--stardust-silver) !important;
            font-style: italic !important;
            font-weight: 500 !important;
            background: transparent !important;
            padding: 1rem !important;
            transition: color 0.3s ease !important;
        }}

        [data-testid="stExpander"] summary:hover {{
            color: var(--cosmic-gold) !important;
        }}

        [data-testid="stExpander"] summary svg {{
            fill: var(--cosmic-gold) !important;
            filter: drop-shadow(0 0 3px rgba(255, 215, 0, 0.5)) !important;
        }}

        [data-testid="stExpander"] > div:last-child {{
            background: linear-gradient(135deg,
                rgba(2, 4, 18, 0.4) 0%,
                rgba(0, 31, 92, 0.2) 100%) !important; /* Roxo substituído por azul */
            border-radius: 12px !important;
            padding: 1.5rem !important;
            margin: 0.5rem !important;
            border-top: 1px solid rgba(255, 215, 0, 0.2) !important;
        }}

        /* ==================== CAMPOS DE ENERGIA (INPUTS) ==================== */
        .stTextInput input, .stTextArea textarea {{
            background: linear-gradient(135deg,
                rgba(2, 4, 18, 0.8) 0%,
                rgba(0, 31, 92, 0.4) 100%) !important; /* Roxo substituído por azul */
            border: 1px solid rgba(255, 215, 0, 0.4) !important;
            border-radius: 12px !important;
            color: var(--celestial-white) !important;
            caret-color: var(--cosmic-gold) !important;
            padding: 0.8rem !important;
            font-family: 'Cormorant Garamond', serif !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
        }}

        .stTextInput input:focus, .stTextArea textarea:focus {{
            border-color: var(--cosmic-gold) !important;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.3) !important;
            outline: none !important;
        }}

        .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
            color: rgba(230, 230, 250, 0.6) !important;
            font-style: italic !important;
        }}

        .stSelectbox > div > div {{
            background: linear-gradient(135deg,
                rgba(2, 4, 18, 0.9) 0%,
                rgba(0, 31, 92, 0.5) 100%) !important; /* Roxo substituído por azul */
            border: 1px solid rgba(255, 215, 0, 0.4) !important;
            border-radius: 12px !important;
            color: var(--celestial-white) !important;
        }}

        .stSelectbox div[data-baseweb="select"] > div {{
            min-height: 50px !important;
            display: flex !important;
            align-items: center !important;
            padding-top: 0.2rem !important;
            padding-bottom: 0.2rem !important;
        }}

        .stSelectbox svg {{
             filter: drop-shadow(0 0 3px rgba(255, 215, 0, 0.5)) !important;
        }}

        /* Dropdown Celestial */
        div[data-baseweb="popover"] ul {{
            background: linear-gradient(160deg,
                var(--galaxy-blue-deep) 0%,
                var(--deep-void) 100%) !important;
            border: 2px solid var(--cosmic-gold) !important;
            border-radius: 15px !important;
            box-shadow:
                0 10px 40px rgba(0, 0, 0, 0.7),
                0 0 20px rgba(255, 215, 0, 0.3) !important;
            padding: 0.5rem 0 !important;
        }}

        div[data-baseweb="popover"] li {{
            color: var(--celestial-white) !important;
            padding: 0.8rem 1.5rem !important;
            font-family: 'Cormorant Garamond', serif !important;
            font-size: 1.1rem !important;
            transition: all 0.2s ease !important;
        }}

        div[data-baseweb="popover"] li:hover,
        div[data-baseweb="popover"] li[aria-selected="true"] {{
            background: linear-gradient(90deg,
                rgba(255, 215, 0, 0.2),
                rgba(255, 215, 0, 0.1)) !important;
            color: var(--cosmic-gold) !important;
            text-shadow: 0 0 8px rgba(255, 215, 0, 0.5) !important;
        }}

        /* ==================== MENSAGENS CELESTIAIS (ALERTAS) ==================== */
        [data-testid="stAlert"] {{
            background: linear-gradient(135deg,
                rgba(0, 31, 92, 0.4) 0%,
                rgba(30, 82, 136, 0.25) 50%,
                rgba(2, 4, 18, 0.4) 100%) !important; /* Gradiente azulado */
            border: 2px solid var(--cosmic-gold) !important;
            border-radius: 15px !important;
            box-shadow:
                0 8px 30px rgba(0, 0, 0, 0.5),
                0 0 20px rgba(255, 215, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
            padding: 1.5rem 2rem !important;
        }}

        [data-testid="stAlert"] div[role="alert"] {{
            color: var(--celestial-white) !important;
            text-shadow: 0 0 10px rgba(248, 248, 255, 0.3) !important;
            font-size: 1.2rem !important;
        }}

        /* ==================== CARTÕES CELESTIAIS (IMAGENS) ==================== */
        .stImage > img {{
            border-radius: 20px !important;
            border: 3px solid var(--cosmic-gold) !important;
            box-shadow:
                0 15px 40px rgba(0, 0, 0, 0.6),
                0 0 30px rgba(255, 215, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
            filter: brightness(1.05) contrast(1.1) !important;
        }}

        .stImage:hover > img {{
            transform: translateY(-8px) scale(1.05) rotateY(5deg) !important;
            box-shadow:
                0 25px 60px rgba(0, 0, 0, 0.8),
                0 0 50px rgba(255, 215, 0, 0.5) !important;
            border-color: var(--stardust-silver) !important;
        }}

        button[aria-label="View fullscreen"] {{ display: none !important; }}

        /* ==================== EFEITOS ESPECIAIS DOS ECOS ESTELARES ==================== */

        /* Título Principal - Ecos Estelares */
        .main-title {{
            background: linear-gradient(45deg,
                var(--cosmic-gold),
                var(--stardust-silver),
                var(--starlight-cyan),      /* Rosa substituído por ciano */
                var(--cosmic-gold));
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: echoShimmer 8s ease-in-out infinite;
            filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.4));
        }}

        @keyframes echoShimmer {{
            0%, 100% {{ background-position: 0% 50%; }}
            25% {{ background-position: 100% 0%; }}
            75% {{ background-position: 0% 100%; }}
        }}

        /* Botão de Troca Energética */
        [data-testid="stLinkButton"] a {{
            background: linear-gradient(135deg,
                var(--sun-gold) 0%,
                var(--cosmic-gold) 30%,
                var(--starlight-cyan) 70%,   /* Rosa substituído por ciano */
                #00aaff 100%) !important;
            background-size: 300% auto !important;
            color: var(--deep-void) !important;
            font-family: 'Cinzel', serif !important;
            font-size: 1.4rem !important;
            font-weight: 700 !important;
            border: 3px solid var(--cosmic-gold) !important;
            border-radius: 50px !important;
            padding: 1.2rem 3rem !important;
            text-align: center !important;
            text-shadow: none !important;
            box-shadow:
                0 8px 25px rgba(0, 0, 0, 0.4),
                0 0 30px rgba(255, 215, 0, 0.5),
                inset 0 2px 0 rgba(255, 255, 255, 0.3) !important;
            transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
            position: relative !important;
            overflow: hidden !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            text-decoration: none !important;
            width: 100%;
        }}

        [data-testid="stLinkButton"] a::before {{
            content: '✨';
            position: absolute;
            top: 50%; left: -30px;
            transform: translateY(-50%);
            font-size: 1.5rem;
            animation: sparkleTravel 3s linear infinite;
        }}

        [data-testid="stLinkButton"] a:hover {{
            transform: translateY(-6px) scale(1.05) !important;
            background-position: right center !important;
            box-shadow:
                0 15px 40px rgba(0, 0, 0, 0.6),
                0 0 50px rgba(255, 215, 0, 0.8),
                0 0 80px rgba(0, 191, 255, 0.5) !important; /* Brilho ciano */
            border-color: var(--stardust-silver) !important;
            color: var(--deep-void) !important;
        }}

        /* Animação de Revelação dos Cartões */
        .card-reveal {{
            animation: stellarReveal 1.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            opacity: 0;
        }}

        @keyframes stellarReveal {{
            0% {{
                transform: translateY(50px) rotateX(90deg) scale(0.8);
                opacity: 0;
                filter: blur(10px);
            }}
            60% {{
                transform: translateY(-10px) rotateX(-5deg) scale(1.05);
                opacity: 0.8;
                filter: blur(2px);
            }}
            100% {{
                transform: translateY(0) rotateX(0deg) scale(1);
                opacity: 1;
                filter: blur(0px);
            }}
        }}

        [data-testid="column"]:nth-child(1) .card-reveal {{ animation-delay: 0.2s; }}
        [data-testid="column"]:nth-child(2) .card-reveal {{ animation-delay: 0.5s; }}
        [data-testid="column"]:nth-child(3) .card-reveal {{ animation-delay: 0.8s; }}

        /* ==================== OCULTAÇÃO DE ELEMENTOS STREAMLIT ==================== */

        /* Esconde a barra lateral de navegação para uma experiência imersiva */
        [data-testid="stSidebar"] {{
            display: none;
        }}

        header {{ display: none !important; }}
        footer {{ display: none !important; }}

        /* Forçar visibilidade dos containers */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            opacity: 1 !important;
            visibility: visible !important;
        }}

        /* ==================== TOQUE FINAL - PARTÍCULAS ESTELARES ==================== */
        .stApp::after {{
            content: '';
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background-image:
                radial-gradient(1px 1px at 20% 30%, rgba(255, 215, 0, 0.3), transparent),
                radial-gradient(1px 1px at 40% 70%, rgba(230, 230, 250, 0.4), transparent),
                radial-gradient(1px 1px at 80% 10%, rgba(0, 191, 255, 0.35), transparent), /* Partículas ciano */
                radial-gradient(1px 1px at 10% 80%, rgba(30, 82, 136, 0.4), transparent),  /* Partículas azuis */
                radial-gradient(1px 1px at 90% 40%, rgba(255, 215, 0, 0.3), transparent);
            background-size: 550px 550px;
            animation: starField 120s linear infinite;
            pointer-events: none;
            z-index: -2;
        }}

        @keyframes starField {{
            0% {{ background-position: 0 0, 0 0, 0 0, 0 0, 0 0; }}
            100% {{ background-position: 550px 550px, -550px 550px, 550px -550px, -550px -550px, 550px 550px; }}
        }}
    </style>
    """)




def apply_shamanic_theme():
    """Aplica o tema visual do Portal dos Sonhos Ancestrais, com containers mais opacos para melhor legibilidade."""
    # Use a imagem de fundo que você criou, ex: 'dreamcatcher_forest.png'
    img = get_img_as_base64("images/dreamcatcher_forest.png")

    st.html(f"""
    <style>
        /* ==================== IMPORTAÇÃO DE FONTES ANCESTRAIS ==================== */
        @import url('https://fonts.googleapis.com/css2?family=Uncial+Antiqua&family=Philosopher:ital,wght@0,400;0,700;1,400&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

        /* ==================== VARIÁVEIS XAMÂNICAS ==================== */
        :root {{
            /* Paleta Principal */
            --sacred-amber: #ff8c00;
            --moon-silver: #c0c0c0;
            --earth-brown: #8b4513;
            --forest-green: #228b22;
            --spirit-white: #f5f5dc;
            --shadow-black: #1c1c1c;

            /* Sombras e Efeitos */
            --sacred-shadow: 0 8px 32px rgba(139, 69, 19, 0.3), 0 0 40px rgba(34, 139, 34, 0.2);
            --fire-glow: 0 0 30px rgba(255, 140, 0, 0.5), 0 0 60px rgba(255, 140, 0, 0.3);
            --sacred-border: 2px solid rgba(255, 140, 0, 0.6);
            --forest-backdrop: backdrop-filter: blur(10px) sepia(10%);
        }}

        /* ==================== PORTAL ANCESTRAL - FUNDO ==================== */
        .stApp {{
            background: {'url(data:image/png;base64,' + img + ') center/cover fixed,' if img else ''}
                       radial-gradient(ellipse at 80% 20%, rgba(34, 139, 34, 0.15) 0%, transparent 50%),
                       radial-gradient(ellipse at 20% 80%, rgba(255, 140, 0, 0.1) 0%, transparent 50%),
                       linear-gradient(135deg, #1c1c1c 0%, #0a1a0a 25%, #2d1810 75%, #1c1c1c 100%);
            min-height: 100vh;
            position: relative;
        }}

        /* (O resto do CSS até os containers permanece o mesmo...) */

        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Uncial Antiqua', serif !important;
            background: linear-gradient(45deg, var(--sacred-amber), var(--spirit-white), var(--sacred-amber));
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 20px rgba(255, 140, 0, 0.4);
            letter-spacing: 2px;
            animation: fireShimmer 8s ease-in-out infinite;
        }}

        @keyframes fireShimmer {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}

        h1 {{
            font-size: 3.8rem !important;
            text-align: center;
            margin: 2rem 0 !important;
            filter: drop-shadow(0 0 15px rgba(255, 140, 0, 0.5));
        }}

        h2 {{
            font-size: 2.4rem !important;
            border-bottom: 2px solid rgba(255, 140, 0, 0.4);
            padding-bottom: 0.8rem;
            margin-bottom: 1.5rem;
        }}

        .st-emotion-cache-1629p8f p, .stMarkdown p, .stMarkdown li,
        .sttextinput_label, .sttextarea_label, .stselectbox_label,
        div[data-baseweb="select"] > div, [data-testid="stExpander"] summary,
        .stButton > button, [data-testid="stDownloadButton"] button div,
        [data-testid="stAlert"] div[role="alert"] {{
            font-family: 'Philosopher', sans-serif !important;
            color: var(--spirit-white) !important;
            font-size: 1.25rem !important;
            line-height: 1.8 !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.9);
        }}

        .header-container p {{
            font-family: 'Crimson Text', serif !important;
            color: var(--moon-silver) !important;
            font-size: 1.3rem !important;
            font-style: italic !important;
            margin-top: -1rem;
        }}

        [data-testid="stWidgetLabel"] p {{
            color: var(--moon-silver) !important;
            font-family: 'Philosopher', sans-serif !important;
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            text-shadow: 0 0 8px rgba(192, 192, 192, 0.3);
        }}

        [data-testid="stSpinner"] > div {{
            color: var(--sacred-amber) !important;
            font-family: 'Crimson Text', serif !important;
            font-size: 1.3rem !important;
            font-style: italic !important;
            text-shadow: 0 0 15px rgba(255, 140, 0, 0.6) !important;
        }}

        /* ====================================================================== */
        /* ==================== CONTAINERS COM MAIOR OPACIDADE ==================== */
        /* ====================================================================== */

        .header-container, .stVerticalBlock[style*="border-radius"], .stVerticalBlock {{
            /* A MUDANÇA ESTÁ AQUI: Adicionamos uma camada de fundo escura e semi-sólida */
            background:
                /* Camada de cor (por cima) */
                linear-gradient(160deg,
                    rgba(139, 69, 19, 0.35) 0%,   /* Earth Brown um pouco mais forte */
                    rgba(34, 139, 34, 0.25) 50%, /* Forest Green um pouco mais forte */
                    rgba(28, 28, 28, 0.45) 100%), /* Sombra mais forte */

                /* Camada de base sólida (por baixo) para bloquear a imagem de fundo */
                linear-gradient(rgba(28, 28, 28, 0.85), rgba(28, 28, 28, 0.85))
                !important;

            border: 1px solid rgba(255, 140, 0, 0.4) !important;
            border-radius: 18px !important;
            box-shadow:
                0 8px 32px rgba(0, 0, 0, 0.6), /* Sombra mais forte */
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(12px) sepia(8%) !important;
            padding: 2rem !important;
            margin: 1.2rem 0 !important;
            transition: all 0.3s ease-in-out !important;
        }}

        .header-container {{
            padding: 2.5rem !important;
            margin-top: 2rem !important;
        }}

        .stVerticalBlock:hover {{
            border-color: rgba(255, 140, 0, 0.7) !important;
            box-shadow: var(--sacred-shadow) !important;
            transform: translateY(-2px) !important;
        }}

        /* (O restante do CSS continua o mesmo a partir daqui...) */

        [data-testid="stFormSubmitButton"] button,
        .stButton > button, [data-testid="stDownloadButton"] button, [data-testid="stLinkButton"] a {{
            background: linear-gradient(135deg,
                var(--earth-brown) 0%,
                var(--forest-green) 50%,
                var(--earth-brown) 100%) !important;
            color: var(--spirit-white) !important;
            border: 2px solid rgba(255, 140, 0, 0.6) !important;
            border-radius: 30px !important;
            font-family: 'Philosopher', sans-serif !important;
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            padding: 1rem 2.5rem !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
        }}

        [data-testid="stLinkButton"] a {{
            display: flex !important; justify-content: center !important;
            align-items: center !important; text-decoration: none !important; width: 100%;
        }}

        .stButton > button:hover, [data-testid="stDownloadButton"] button:hover, [data-testid="stLinkButton"] a:hover {{
            transform: translateY(-3px) scale(1.02) !important;
            border-color: var(--sacred-amber) !important;
            box-shadow: var(--fire-glow) !important;
            color: var(--sacred-amber) !important;
            background-position: right center !important;
        }}

        .stTextInput input, .stTextArea textarea {{
            background: linear-gradient(135deg, rgba(28, 28, 28, 0.8) 0%, rgba(139, 69, 19, 0.3) 100%) !important;
            border: 1px solid rgba(255, 140, 0, 0.4) !important;
            border-radius: 12px !important;
            color: var(--spirit-white) !important;
            caret-color: var(--sacred-amber) !important;
        }}

        .stTextInput input:focus, .stTextArea textarea:focus {{
            border-color: var(--sacred-amber) !important;
            box-shadow: 0 0 15px rgba(255, 140, 0, 0.3) !important;
        }}

        .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
            color: var(--moon-silver) !important; /* Cor alterada para prata/claro */
            opacity: 0.8; /* Opacidade ajustada para um bom contraste */
            font-style: italic !important;
        }}

        /* ============================================================== */
        /* ==================== SELECTBOX CORRIGIDO ===================== */
        /* ============================================================== */

        /* Caixa principal do Selectbox */
        .stSelectbox > div > div {{
            background: linear-gradient(135deg, rgba(28, 28, 28, 0.9) 0%, rgba(139, 69, 19, 0.4) 100%) !important;
            border: 1px solid rgba(255, 140, 0, 0.4) !important;
            border-radius: 12px !important;
        }}

        /* Aumenta a altura da caixa para acomodar a fonte e centraliza o texto */
        .stSelectbox div[data-baseweb="select"] > div {{
            min-height: 55px !important; /* Aumenta a altura */
            display: flex !important;
            align-items: center !important; /* Centraliza verticalmente */
        }}

        /* Dropdown (a lista de opções que abre) */
        div[data-baseweb="popover"] ul {{
            background: linear-gradient(160deg, var(--earth-brown) 0%, var(--shadow-black) 100%) !important;
            border: 2px solid var(--sacred-amber) !important;
            border-radius: 15px !important;
            box-shadow: var(--sacred-shadow) !important;
            padding: 0.5rem 0 !important;
        }}

        /* Itens individuais na lista dropdown */
        div[data-baseweb="popover"] li {{
            font-family: 'Philosopher', sans-serif !important;
            color: var(--spirit-white) !important;
            font-size: 1.2rem !important;
            padding: 0.8rem 1.5rem !important;
            transition: all 0.2s ease !important;
        }}

        /* Efeito de hover e item selecionado no dropdown */
        div[data-baseweb="popover"] li:hover,
        div[data-baseweb="popover"] li[aria-selected="true"] {{
            background: linear-gradient(90deg, rgba(255, 140, 0, 0.2), rgba(255, 140, 0, 0.1)) !important;
            color: var(--sacred-amber) !important;
            text-shadow: 0 0 8px rgba(255, 140, 0, 0.5) !important;
        }}

        /* ============================================================== */
        /* ============================================================== */

        /* ============================================================== */
        /* ==================== EXPANDER CORRIGIDO ====================== */
        /* ============================================================== */

        /* Container geral do Expander */
        [data-testid="stExpander"] {{
            border: 1px solid rgba(255, 140, 0, 0.4) !important;
            border-radius: 15px !important;
            background: linear-gradient(145deg, rgba(139, 69, 19, 0.15) 0%, rgba(28, 28, 28, 0.3) 100%) !important;
            transition: all 0.4s ease-in-out !important;
            overflow: hidden !important;
        }}

        [data-testid="stExpander"]:hover {{
            border-color: var(--sacred-amber) !important;
            box-shadow: var(--fire-glow) !important;
        }}

        /* Cabeçalho clicável do Expander */
        [data-testid="stExpander"] summary {{
            background: transparent !important;
            padding: 1rem !important;
            transition: color 0.3s ease !important;
        }}

        [data-testid="stExpander"] summary:hover {{
            color: var(--sacred-amber) !important;
        }}

        /* Área de conteúdo do Expander (quando aberto) */
        [data-testid="stExpander"] > div:last-child {{
            background: linear-gradient(135deg, rgba(28, 28, 28, 0.5) 0%, rgba(139, 69, 19, 0.2) 100%) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            margin: 0.5rem !important;
            border-top: 1px solid rgba(255, 140, 0, 0.2) !important;
        }}

        /* ============================================================== */
        /* ============================================================== */

        [data-testid="stAlert"] {{
            background: linear-gradient(135deg, rgba(139, 69, 19, 0.3) 0%, rgba(34, 139, 34, 0.2) 100%) !important;
            border: 2px solid var(--sacred-amber) !important;
            border-radius: 15px !important;
        }}

        .stImage > img {{
            border-radius: 20px !important;
            border: 3px solid var(--sacred-amber) !important;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6), 0 0 30px rgba(255, 140, 0, 0.3);
            filter: brightness(1.1) contrast(1.1) sepia(10%);
        }}

        /* ==================== OCULTAR BARRA LATERAL ==================== */
        /* Esconde a barra lateral de navegação para uma experiência imersiva */
        [data-testid="stSidebar"] {{
            display: none;
        }}

        header {{ display: none !important; }}
        footer {{ display: none !important; }}

        .stApp::after {{
            content: '';
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background-image:
                radial-gradient(2px 2px at 20% 30%, rgba(255, 140, 0, 0.3), transparent),
                radial-gradient(1px 1px at 40% 70%, rgba(192, 192, 192, 0.4), transparent),
                radial-gradient(1px 1px at 80% 10%, rgba(34, 139, 34, 0.3), transparent);
            background-size: 550px 550px;
            animation: spiritDance 120s linear infinite;
            pointer-events: none;
            z-index: -2;
        }}

        @keyframes spiritDance {{
            0% {{ background-position: 0 0; }}
            100% {{ background-position: 550px 550px; }}
        }}
    </style>
    """)
