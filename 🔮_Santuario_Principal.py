# 🔮_Santuario_Principal.py

import streamlit as st
from utils.theme import apply_mystical_theme
from utils.helpers import mystical_divider, get_img_as_base64

# Configuração da página e aplicação do tema
st.set_page_config(
    page_title="Santuário das Revelações",
    page_icon="🔮",
    layout="wide"  # Layout amplo para desktop
)
apply_mystical_theme()

# --- Pré-carregamento das imagens em Base64 para uso no HTML ---
try:
    icon_tarot_b64 = get_img_as_base64("images/icon_tarot.png")
    icon_stars_b64 = get_img_as_base64("images/icon_stars.png")
    icon_dream_b64 = get_img_as_base64("images/icon_dream.png")
except Exception as e:
    st.error(f"Erro ao carregar imagens dos ícones: {e}")
    icon_tarot_b64 = icon_stars_b64 = icon_dream_b64 = None

# CSS personalizado para o portal (SEU CÓDIGO ORIGINAL - SEM ALTERAÇÕES)
st.html("""
<style>
.portal-card {
    background: linear-gradient(135deg, rgba(74, 20, 140, 0.15), rgba(147, 51, 234, 0.1));
    border: 2px solid rgba(139, 92, 246, 0.3);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    transition: all 0.4s ease;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
    min-height: 300px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    cursor: pointer;
    text-decoration: none;
    color: inherit;
}

.portal-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.1) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.4s ease;
}

.portal-card:hover::before {
    opacity: 1;
}

.portal-card:hover {
    transform: translateY(-8px);
    border-color: rgba(139, 92, 246, 0.8);
    box-shadow: 0 20px 40px rgba(139, 92, 246, 0.3);
    background: linear-gradient(135deg, rgba(74, 20, 140, 0.25), rgba(147, 51, 234, 0.2));
}

.portal-card:active {
    transform: translateY(-4px);
}

.portal-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 1.5rem;
    padding: 1rem;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(168, 85, 247, 0.15));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.3s ease;
}

.portal-card:hover .portal-icon {
    transform: scale(1.1) rotate(5deg);
}

.portal-title {
    color: #A78BFA;
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
    text-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);
    transition: color 0.3s ease;
}

.portal-card:hover .portal-title {
    color: #C4B5FD;
}

.portal-description {
    color: #E5E7EB;
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    opacity: 0.9;
    transition: opacity 0.3s ease;
}

.portal-card:hover .portal-description {
    opacity: 1;
}

.click-hint {
    color: #8B5CF6;
    font-size: 0.85rem;
    font-weight: 500;
    opacity: 0.7;
    margin-top: 1rem;
    transition: all 0.3s ease;
}

.portal-card:hover .click-hint {
    opacity: 1;
    color: #A78BFA;
    transform: translateY(-2px);
}

.intro-section {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(168, 85, 247, 0.05));
    border-radius: 20px;
    margin-bottom: 3rem;
    border: 1px solid rgba(139, 92, 246, 0.2);
}

.intro-text {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #D1D5DB;
    font-style: italic;
    max-width: 800px;
    margin: 0 auto;
}

.footer-note {
    text-align: center;
    margin-top: 4rem;
    padding: 1.5rem;
    background: rgba(139, 92, 246, 0.08);
    border-radius: 10px;
    border: 1px solid rgba(139, 92, 246, 0.2);
    color: #F3F4F6;
}

.footer-note p {
    color: #E5E7EB;
    margin-bottom: 0.5rem;
}

.footer-note a {
    color: #C4B5FD !important;
    text-decoration: none;
    font-weight: bold;
    transition: color 0.3s ease;
}

.footer-note a:hover {
    color: #DDD6FE !important;
    text-decoration: underline;
}

.footer-blessing {
    color: #D1D5DB !important;
    font-size: 0.9rem;
    opacity: 0.9;
    margin-top: 1rem;
}

/* Oculta botões padrão para não interferir com os cards */
.stButton {
    display: none !important;
}
</style>
""")

# Conteúdo da Página Principal
st.html("""
<div class="header-container">
    <h1 class="main-title">Santuário das Revelações</h1>
</div>

<div class="intro-section">
    <div class="intro-text">
        Respire fundo, viajante. Você adentrou um espaço sagrado onde os véus entre os mundos são tênues.
        Três câmaras de sabedoria ancestral aguardam para iluminar sua jornada.
        Cada uma oferece uma chave única para os mistérios da sua alma.
        <br><br>
        <strong>Qual portal você escolherá cruzar primeiro?</strong>
    </div>
</div>
""")

# --- CORREÇÃO E SIMPLIFICAÇÃO DO LAYOUT ---
# Usamos st.columns que já é responsivo. O CSS fará o resto.
col1, col2, col3 = st.columns(3, gap="large")

# Tarô Místico
with col1:
    icon_html = f'<img src="data:image/png;base64,{icon_tarot_b64}" style="width: 60px; height: 60px; object-fit: contain;" />' if icon_tarot_b64 else "🔮"

    st.html(f"""
    <a href="Taro_Mistico" target="_self" style="text-decoration: none;">
        <div class="portal-card">
            <div class="portal-icon">
                {icon_html}
            </div>
            <h3 class="portal-title">Tarô Místico</h3>
            <p class="portal-description">
                Desvende os padrões do destino através da sabedoria atemporal das cartas.
                Permita que os arcanos revelem os caminhos ocultos de sua jornada.
            </p>
            <div class="click-hint">✨ Clique para entrar ✨</div>
        </div>
    </a>
    """)

# Ecos Estelares
with col2:
    icon_html = f'<img src="data:image/png;base64,{icon_stars_b64}" style="width: 60px; height: 60px; object-fit: contain;" />' if icon_stars_b64 else "⭐"

    st.html(f"""
    <a href="Ecos_Estelares" target="_self" style="text-decoration: none;">
        <div class="portal-card">
            <div class="portal-icon">
                {icon_html}
            </div>
            <h3 class="portal-title">Ecos Estelares</h3>
            <p class="portal-description">
                Ouça a canção que as estrelas cantaram no momento do seu nascimento.
                Descubra como os astros influenciam sua essência e propósito.
            </p>
            <div class="click-hint">✨ Clique para consultar ✨</div>
        </div>
    </a>
    """)

# Intérprete Xamânico
with col3:
    icon_html = f'<img src="data:image/png;base64,{icon_dream_b64}" style="width: 60px; height: 60px; object-fit: contain;" />' if icon_dream_b64 else "🌙"

    st.html(f"""
    <a href="Interprete_Xamanico" target="_self" style="text-decoration: none;">
        <div class="portal-card">
            <div class="portal-icon">
                {icon_html}
            </div>
            <h3 class="portal-title">Intérprete Xamânico</h3>
            <p class="portal-description">
                Navegue pelas paisagens simbólicas de seus sonhos e decodifique
                as mensagens que sua alma sussurra durante o sono.
            </p>
            <div class="click-hint">✨ Clique para explorar ✨</div>
        </div>
    </a>
    """)


# Seção final com link para políticas
st.html("""
<div class="footer-note">
    <p>
        Ao prosseguir, você concorda com nossos
        <a href="Politicas" target="_self">Termos e Políticas</a>.
    </p>
    <p class="footer-blessing">
        ✨ Que a sabedoria dos cosmos ilumine seu caminho ✨
    </p>
</div>
""")
