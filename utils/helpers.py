# utils/helpers.py
import streamlit as st
import base64
import re

@st.cache_data
def get_img_as_base64(file):
    """Lê um arquivo de imagem e o converte para uma string Base64."""
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

def strip_emojis(text):
    """Remove caracteres emoji de uma string."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", text) if text else ""

def mystical_divider(margin="2rem 0"):
    """Cria um divisor místico animado com margem customizável."""
    st.html(f"""
    <div style="text-align: center; margin: {margin};">
        <div style="font-size: 1.5rem; color: #d4af37; opacity: 0.8; animation: pulse 2s ease-in-out infinite alternate;">
            ⟡ ◦ ❋ ◦ ⟡
        </div>
    </div>
    <style> @keyframes pulse {{ from {{ opacity: 0.6; transform: scale(1); }} to {{ opacity: 1; transform: scale(1.05); }} }} </style>
    """)

def reset_app_state(app_key_prefix):
    """Limpa o estado da sessão para um app específico para recomeçar."""
    # Limpa chaves específicas do app (ex: 'tarot_', 'astro_')
    keys_to_clear = [k for k in st.session_state.keys() if k.startswith(app_key_prefix)]

    # Limpa chaves genéricas que podem ser compartilhadas ou que precisam ser limpas
    generic_keys = [
        'payment_verified', 'stripe_session_id', 'final_interpretation',
        'drawn_cards', 'chart_data', 'dream_description', 'user_name', 'city',
        'dob', 'tob'
    ]
    # Adiciona as chaves genéricas à lista, evitando duplicatas
    for key in generic_keys:
        if key not in keys_to_clear:
            keys_to_clear.append(key)

    # Deleta as chaves do estado da sessão
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    # Define a etapa inicial para o app específico e força a atualização da página
    st.session_state[f'{app_key_prefix}_step'] = 'welcome'
    st.rerun()
