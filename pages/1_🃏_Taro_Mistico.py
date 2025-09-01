# pages/1_🃏_Taro_Mistico.py

# ------------------------------------------------------------------------------
# 1. IMPORTS E CONFIGURAÇÃO INICIAL
# ------------------------------------------------------------------------------
import streamlit as st
import random
import openai
import os
from datetime import datetime
import unicodedata
from uuid import uuid4
import re

try:
    import stripe
except ImportError:
    stripe = None # Se a importação falhar, a variável 'stripe' existirá como None

# NOVOS IMPORTS DOS MÓDulos CENTRALIZADOS
from utils.theme import apply_mystical_theme
from utils.helpers import get_img_as_base64, strip_emojis, mystical_divider, reset_app_state
from utils.pdf_templates import MysticalPDF, create_reading_pdf

try:
    # <<< CORREÇÃO AQUI: Usando os.environ.get para ler as variáveis de ambiente >>>
    openai_api_key = os.environ.get("TAROT_OPENAI_API_KEY")
    stripe_price_id = os.environ.get("TAROT_STRIPE_PRICE_ID")

    # Chaves comuns
    stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY")
    app_base_url = os.environ.get("APP_BASE_URL")

    # Verificação para garantir que todas as chaves foram encontradas
    if not all([openai_api_key, stripe_price_id, stripe_secret_key, app_base_url]):
        raise KeyError("Uma ou mais variáveis de ambiente não foram encontradas.")

    if stripe:
        stripe.api_key = stripe_secret_key
    openai.api_key = openai_api_key

except KeyError as e:
    st.error(f"ERRO CRÍTICO: Verifique se as variáveis de ambiente (ex: TAROT_OPENAI_API_KEY) estão configuradas no Render. Detalhe: {e}")
    st.stop()


# ==============================================================================
# 2. CONFIGURAÇÃO INICIAL E LÓGICA DE PASSOS
# ==============================================================================

st.set_page_config(
    page_title="🔮 Tarô Místico - Sua Revelação Sagrada",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="auto"
)

apply_mystical_theme()

# --- NOVA LINHA ---
# Inicializa a chave do snapshot para garantir que ela sempre exista.
if "selected" not in st.session_state:
    st.session_state.selected = {}

if 'tarot_step' not in st.session_state:
    st.session_state.tarot_step = 'welcome'

query_params = st.query_params
stripe_session_id = query_params.get("session_id")

# Se um session_id está na URL, o usuário está voltando do pagamento.
if stripe_session_id and 'payment_verified' not in st.session_state:
    # Verificação defensiva
    if stripe is None:
        st.error("ERRO CRÍTICO: A biblioteca de pagamento (Stripe) não está disponível. Verifique o arquivo requirements.txt.")
        st.stop()

    try:

        session = stripe.checkout.Session.retrieve(stripe_session_id)

        if session.payment_status == "paid":
            meta = session.metadata or {}

            # Reconstrói o snapshot a partir do Stripe
            st.session_state.selected = {
                "spread_choice": meta.get("spread_choice"),
                "reading_style": meta.get("reading_style"),
                "question": meta.get("question", ""),
                "user_name": meta.get("user_name"),
            }

            # Atualiza o estado principal
            st.session_state.user_name = meta.get("user_name")

            st.session_state.payment_verified = True
            st.session_state.tarot_step = 'result'
            st.query_params.clear()
            st.rerun()
        else:
            st.warning("O pagamento não foi concluído. Por favor, tente novamente.")
            st.session_state.tarot_step = 'payment'
            st.query_params.clear()
            st.rerun()

    except Exception as e:
        st.error(f"Ocorreu um erro ao verificar seu pagamento: {e}")
        st.session_state.tarot_step = 'welcome'

# ==============================================================================
# 3. DADOS E FUNÇÕES PRINCIPAIS
# ==============================================================================

# --- DADOS (DECK, SPREAD_EXPLANATIONS, STYLE_EXPLANATIONS) ---

# --- DADOS (DECK, SPREAD_EXPLANATIONS, STYLE_EXPLANATIONS) ---

# --- DADOS DO BARALHO DE TARÔ ---
# Dicionário Completo e Aprimorado das 78 Cartas do Tarô
# Projetado para uma experiência transformadora e profundamente interpretativa

DECK = [
    # ═══════════════════════════════════════════════════════════════════
    #                           ARCANOS MAIORES
    # A Jornada da Alma - Os 22 Arquétipos Universais da Experiência Humana
    # ═══════════════════════════════════════════════════════════════════

    {
        "name": "O Louco",
        "number": 0,
        "type": "Arcano Maior",
        "element": "Ar",
        "astrology": "Urano",
        "keywords": ["inocência", "novo começo", "espontaneidade", "potencial infinito", "fé", "aventura"],
        "upright": "Inocência pura, novos começos cheios de potencial, espontaneidade divina, espírito livre e corajoso, fé no desconhecido, aventura da alma em sua jornada. Representa o primeiro passo em direção ao crescimento espiritual.",
        "reversed": "Inconsequência perigosa, negligência com as oportunidades, riscos desnecessários, estupidez que bloqueia o crescimento, medo de mudanças, resistência ao chamado da alma.",
        "archetype": "O Viajante Eterno",
        "life_lesson": "Confiar no processo da vida e abraçar o desconhecido com coragem.",
        "shadow": "Irresponsabilidade que sabota o próprio crescimento.",
        "themes": ["amor", "carreira", "espiritualidade", "autoconhecimento"]
    },

    {
        "name": "O Mago",
        "number": 1,
        "type": "Arcano Maior",
        "element": "Mercúrio",
        "astrology": "Mercúrio",
        "keywords": ["manifestação", "poder pessoal", "habilidade", "foco", "recursos", "alquimia"],
        "upright": "Poder de manifestação através da vontade focada, habilidade de unir céu e terra, concentração que transforma sonhos em realidade, ação consciente e direcionada, domínio sobre os elementos da criação.",
        "reversed": "Manipulação das energias para fins egoístas, má utilização do poder pessoal, truques que enganam a si mesmo, ilusões que afastam da verdade, potencial desperdiçado por falta de foco.",
        "archetype": "O Alquimista",
        "life_lesson": "Usar o poder pessoal com sabedoria e responsabilidade.",
        "shadow": "Manipulação e uso do poder para controlar outros.",
        "themes": ["carreira", "manifestação", "liderança", "criatividade"]
    },

    {
        "name": "A Sacerdotisa",
        "number": 2,
        "type": "Arcano Maior",
        "element": "Água",
        "astrology": "Lua",
        "keywords": ["intuição", "mistério", "sabedoria interior", "subconsciente", "receptividade", "conhecimento oculto"],
        "upright": "Intuição profunda que revela verdades ocultas, conexão com a sabedoria feminina ancestral, mistérios do subconsciente revelados, receptividade aos sinais do universo, conhecimento que vem do silêncio interior.",
        "reversed": "Desconexão com a intuição natural, segredos que causam confusão, falta de receptividade aos sinais, bloqueio do conhecimento interior, racionalização excessiva que afasta da sabedoria.",
        "archetype": "A Guardiã dos Mistérios",
        "life_lesson": "Confiar na sabedoria interior e na voz da intuição.",
        "shadow": "Segredos que isolam e confusão mental.",
        "themes": ["espiritualidade", "amor", "autoconhecimento", "intuição"]
    },

    {
        "name": "A Imperatriz",
        "number": 3,
        "type": "Arcano Maior",
        "element": "Terra",
        "astrology": "Vênus",
        "keywords": ["criatividade", "abundância", "maternidade", "natureza", "beleza", "fertilidade"],
        "upright": "Criatividade que floresce em abundância, energia maternal que nutre o crescimento, conexão profunda com a natureza e seus ciclos, beleza que inspira e cura, fertilidade em todos os aspectos da vida.",
        "reversed": "Bloqueio da energia criativa, dependência emocional que limita, estagnação dos projetos criativos, desconexão com a natureza e intuição feminina, escassez onde deveria haver abundância.",
        "archetype": "A Grande Mãe",
        "life_lesson": "Nutrir a criatividade e permitir que a abundância flua naturalmente.",
        "shadow": "Dependência e bloqueio criativo por medo.",
        "themes": ["criatividade", "abundância", "amor", "família"]
    },

    {
        "name": "O Imperador",
        "number": 4,
        "type": "Arcano Maior",
        "element": "Fogo",
        "astrology": "Áries",
        "keywords": ["autoridade", "estrutura", "liderança", "disciplina", "proteção", "ordem"],
        "upright": "Autoridade natural baseada na sabedoria, estrutura que oferece segurança e crescimento, liderança responsável e protetiva, disciplina que constrói o futuro, ordem que permite a manifestação dos sonhos.",
        "reversed": "Dominação tirânica que sufoca o crescimento, controle excessivo nascido do medo, rigidez que impede a adaptação, inflexibilidade que quebra relacionamentos, autoritarismo que aliena.",
        "archetype": "O Pai Arquetípico",
        "life_lesson": "Liderar com sabedoria, protegendo sem controlar.",
        "shadow": "Tirania e controle baseados no medo de perder poder.",
        "themes": ["liderança", "carreira", "autoridade", "estrutura"]
    },

    {
        "name": "O Hierofante",
        "number": 5,
        "type": "Arcano Maior",
        "element": "Terra",
        "astrology": "Touro",
        "keywords": ["tradição", "ensino", "sabedoria", "conformidade", "orientação espiritual", "instituições"],
        "upright": "Sabedoria tradicional que orienta o crescimento, ensino que preserva conhecimentos ancestrais, conformidade consciente com princípios elevados, orientação espiritual através de mentores, educação que liberta.",
        "reversed": "Rebelião necessária contra dogmas limitantes, questionamento de autoridades desatualizadas, busca por caminhos espirituais alternativos, liberdade das convenções sociais restritivas.",
        "archetype": "O Mestre Espiritual",
        "life_lesson": "Equilibrar tradição com crescimento pessoal.",
        "shadow": "Dogmatismo que impede o crescimento espiritual.",
        "themes": ["espiritualidade", "educação", "tradição", "orientação"]
    },

    {
        "name": "Os Amantes",
        "number": 6,
        "type": "Arcano Maior",
        "element": "Ar",
        "astrology": "Gêmeos",
        "keywords": ["amor", "escolhas", "união", "harmonia", "dualidade", "relacionamentos"],
        "upright": "Amor que une almas em harmonia perfeita, escolhas conscientes baseadas no coração, relacionamentos que elevam e transformam, harmonia entre opostos complementares, união sagrada de energias.",
        "reversed": "Desarmonia nos relacionamentos, escolhas baseadas no medo ou conveniência, conflitos entre coração e mente, desalinhamento de valores fundamentais, relacionamentos que drenam energia.",
        "archetype": "A União Sagrada",
        "life_lesson": "Fazer escolhas alinhadas com o coração e valores profundos.",
        "shadow": "Escolhas que traem a própria essência.",
        "themes": ["amor", "relacionamentos", "escolhas", "harmonia"]
    },

    {
        "name": "A Carruagem",
        "number": 7,
        "type": "Arcano Maior",
        "element": "Água",
        "astrology": "Câncer",
        "keywords": ["determinação", "controle", "vitória", "direção", "vontade", "progresso"],
        "upright": "Determinação inabalável que supera obstáculos, controle consciente sobre as forças opostas da vida, vitória conquistada através da persistência, direção clara rumo aos objetivos, vontade triunfante.",
        "reversed": "Perda de controle sobre as circunstâncias, falta de direção clara, agressividade que afasta oportunidades, obstáculos que parecem intransponíveis, dispersão de energia em múltiplas direções.",
        "archetype": "O Guerreiro Vitorioso",
        "life_lesson": "Manter o foco e a determinação mesmo diante dos desafios.",
        "shadow": "Perda de controle e direção por falta de foco.",
        "themes": ["carreira", "objetivos", "determinação", "sucesso"]
    },

    {
        "name": "A Força",
        "number": 8,
        "type": "Arcano Maior",
        "element": "Fogo",
        "astrology": "Leão",
        "keywords": ["coragem interior", "compaixão", "gentileza", "autocontrole", "paciência", "domínio"],
        "upright": "Força interior que vence através da gentileza, coragem que nasce da compaixão, autocontrole que domina os instintos primitivos, paciência que transforma situações difíceis, poder suave mas inabalável.",
        "reversed": "Fraqueza interior mascarada por agressividade, insegurança que gera comportamentos destrutivos, falta de autocontrole emocional, dúvidas que paralisam a ação, medo de mostrar vulnerabilidade.",
        "archetype": "A Força Gentil",
        "life_lesson": "Verdadeira força vem da compaixão e autocontrole.",
        "shadow": "Fraqueza e falta de autocontrole emocional.",
        "themes": ["autoconhecimento", "coragem", "compaixão", "autocontrole"]
    },

    {
        "name": "O Eremita",
        "number": 9,
        "type": "Arcano Maior",
        "element": "Terra",
        "astrology": "Virgem",
        "keywords": ["introspecção", "sabedoria interior", "orientação", "solidão", "busca", "iluminação"],
        "upright": "Introspecção profunda que revela verdades essenciais, busca solitária pela sabedoria interior, orientação que vem do silêncio e reflexão, iluminação gradual através da experiência, maturidade espiritual.",
        "reversed": "Isolamento que se torna fuga da realidade, solidão que gera amargura, reclusão excessiva que impede o crescimento, resistência à orientação externa, orgulho espiritual que isola.",
        "archetype": "O Sábio Solitário",
        "life_lesson": "Encontrar respostas através da reflexão interior.",
        "shadow": "Isolamento que se torna fuga da vida.",
        "themes": ["espiritualidade", "autoconhecimento", "sabedoria", "introspecção"]
    },

    {
        "name": "A Roda da Fortuna",
        "number": 10,
        "type": "Arcano Maior",
        "element": "Fogo",
        "astrology": "Júpiter",
        "keywords": ["destino", "ciclos", "mudança", "sorte", "karma", "oportunidade"],
        "upright": "Ciclos naturais da vida trazendo novas oportunidades, destino que se desdobra de forma positiva, mudanças que elevam a consciência, sorte que recompensa ações passadas, karma positivo em manifestação.",
        "reversed": "Resistência às mudanças necessárias, má sorte resultante de escolhas passadas, ciclos negativos que precisam ser quebrados, oportunidades perdidas por falta de percepção, karma desafiador.",
        "archetype": "O Tecelão do Destino",
        "life_lesson": "Aceitar os ciclos da vida e fluir com as mudanças.",
        "shadow": "Resistência às mudanças e vitimização.",
        "themes": ["destino", "mudanças", "oportunidades", "ciclos"]
    },

    {
        "name": "A Justiça",
        "number": 11,
        "type": "Arcano Maior",
        "element": "Ar",
        "astrology": "Libra",
        "keywords": ["equilíbrio", "verdade", "justiça", "causa e efeito", "decisões", "integridade"],
        "upright": "Equilíbrio perfeito entre dar e receber, verdade que liberta e cura, justiça que restaura a harmonia, decisões baseadas na integridade, causa e efeito operando de forma justa, responsabilidade consciente.",
        "reversed": "Injustiça que gera desequilíbrio, decisões baseadas em preconceitos, desonestidade que corrompe relacionamentos, falta de responsabilidade pelas próprias ações, parcialidade que distorce a verdade.",
        "archetype": "A Balança Cósmica",
        "life_lesson": "Viver com integridade e aceitar as consequências das ações.",
        "shadow": "Injustiça e desequilíbrio causados por desonestidade.",
        "themes": ["justiça", "equilíbrio", "decisões", "responsabilidade"]
    },

    {
        "name": "O Enforcado",
        "number": 12,
        "type": "Arcano Maior",
        "element": "Água",
        "astrology": "Netuno",
        "keywords": ["sacrifício", "rendição", "perspectiva", "pausa", "entrega", "transformação"],
        "upright": "Sacrifício consciente que traz crescimento espiritual, rendição que abre novas perspectivas, pausa necessária para reflexão profunda, entrega confiante ao processo da vida, transformação através da aceitação.",
        "reversed": "Resistência teimosa às mudanças necessárias, atrasos causados pela recusa em se adaptar, indecisão que paralisa o progresso, martírio desnecessário, sacrifícios que não trazem crescimento.",
        "archetype": "O Sacrifício Sagrado",
        "life_lesson": "Às vezes é preciso soltar para receber algo maior.",
        "shadow": "Teimosia e resistência às mudanças necessárias.",
        "themes": ["transformação", "sacrifício", "aceitação", "perspectiva"]
    },

    {
        "name": "A Morte",
        "number": 13,
        "type": "Arcano Maior",
        "element": "Água",
        "astrology": "Escorpião",
        "keywords": ["transformação", "fim", "renascimento", "mudança", "renovação", "ciclo"],
        "upright": "Transformação profunda que renova completamente a vida, fim necessário que permite novos começos, morte simbólica de padrões limitantes, mudança inevitável mas libertadora, renascimento em um nível superior.",
        "reversed": "Resistência às transformações necessárias, medo da mudança que causa estagnação, fim adiado que prolonga o sofrimento, apego a situações que já não servem, transformação bloqueada por medo.",
        "archetype": "O Transformador",
        "life_lesson": "Abraçar as transformações como parte natural da evolução.",
        "shadow": "Medo da mudança que causa estagnação.",
        "themes": ["transformação", "mudança", "renascimento", "libertação"]
    },

    {
        "name": "A Temperança",
        "number": 14,
        "type": "Arcano Maior",
        "element": "Fogo",
        "astrology": "Sagitário",
        "keywords": ["equilíbrio", "moderação", "alquimia", "cura", "paciência", "harmonia"],
        "upright": "Equilíbrio perfeito entre opostos complementares, moderação que traz paz interior, alquimia espiritual que transforma energias, cura através da harmonização, paciência que permite a manifestação divina.",
        "reversed": "Desequilíbrio que causa turbulência interior, excesso em todas as áreas da vida, impaciência que sabota o processo, desalinhamento com o propósito superior, falta de moderação que leva ao caos.",
        "archetype": "O Alquimista Divino",
        "life_lesson": "Encontrar equilíbrio e moderação em todas as coisas.",
        "shadow": "Excesso e desequilíbrio que causam caos interior.",
        "themes": ["equilíbrio", "cura", "harmonia", "moderação"]
    },

    {
        "name": "O Diabo",
        "number": 15,
        "type": "Arcano Maior",
        "element": "Terra",
        "astrology": "Capricórnio",
        "keywords": ["sombra", "tentação", "materialismo", "vício", "ilusão", "aprisionamento"],
        "upright": "Confronto necessário com a sombra pessoal, tentações que revelam desejos ocultos, materialismo que ensina sobre valores verdadeiros, vícios que mostram áreas de cura, ilusões que precisam ser dissolvidas.",
        "reversed": "Libertação das correntes autoimpostas, desapego de vícios e compulsões, quebra de padrões destrutivos, autoconhecimento que dissolve ilusões, liberdade conquistada através da consciência.",
        "archetype": "O Espelho da Sombra",
        "life_lesson": "Reconhecer e integrar aspectos sombrios para encontrar liberdade.",
        "shadow": "Negação da sombra que perpetua padrões destrutivos.",
        "themes": ["autoconhecimento", "libertação", "sombra", "vícios"]
    },

    {
        "name": "A Torre",
        "number": 16,
        "type": "Arcano Maior",
        "element": "Fogo",
        "astrology": "Marte",
        "keywords": ["despertar", "revelação", "mudança súbita", "destruição", "liberdade", "iluminação"],
        "upright": "Despertar súbito que destrói ilusões, revelação que liberta de falsas crenças, mudança dramática mas necessária, destruição de estruturas limitantes, iluminação através da crise, liberdade conquistada.",
        "reversed": "Medo das mudanças necessárias, resistência ao despertar, evitação de crises que trariam crescimento, apego a estruturas que já não servem, adiamento de transformações inevitáveis.",
        "archetype": "O Destruidor Sagrado",
        "life_lesson": "Aceitar que às vezes é preciso destruir para reconstruir melhor.",
        "shadow": "Medo da mudança que evita crescimento necessário.",
        "themes": ["despertar", "mudança súbita", "libertação", "revelação"]
    },

    {
        "name": "A Estrela",
        "number": 17,
        "type": "Arcano Maior",
        "element": "Ar",
        "astrology": "Aquário",
        "keywords": ["esperança", "inspiração", "cura", "fé", "orientação", "renovação"],
        "upright": "Esperança que renasce após períodos difíceis, inspiração divina que orienta o caminho, cura profunda em todos os níveis, fé renovada no futuro, orientação através da intuição superior, renovação espiritual.",
        "reversed": "Desespero que obscurece a visão do futuro, falta de fé nas próprias capacidades, desânimo que impede o progresso, desconexão com a orientação superior, perda de esperança e inspiração.",
        "archetype": "A Portadora da Luz",
        "life_lesson": "Manter a fé e esperança mesmo nos momentos mais escuros.",
        "shadow": "Desespero e perda de fé que paralisa.",
        "themes": ["esperança", "cura", "fé", "inspiração"]
    },

    {
        "name": "A Lua",
        "number": 18,
        "type": "Arcano Maior",
        "element": "Água",
        "astrology": "Peixes",
        "keywords": ["intuição", "ilusão", "subconsciente", "medo", "mistério", "imaginação"],
        "upright": "Intuição profunda que navega através das ilusões, subconsciente revelando verdades ocultas, medos que precisam ser enfrentados para crescer, mistérios que se desvendam gradualmente, imaginação que cria realidades.",
        "reversed": "Medos irreais que paralisam a ação, confusão mental que distorce a percepção, ilusões dissolvidas pela luz da consciência, verdades ocultas finalmente reveladas, clareza mental após período de confusão.",
        "archetype": "A Guardiã dos Sonhos",
        "life_lesson": "Navegar através das ilusões com a luz da intuição.",
        "shadow": "Medos irracionais e ilusões que distorcem a realidade.",
        "themes": ["intuição", "subconsciente", "medos", "ilusões"]
    },

    {
        "name": "O Sol",
        "number": 19,
        "type": "Arcano Maior",
        "element": "Fogo",
        "astrology": "Sol",
        "keywords": ["sucesso", "alegria", "vitalidade", "clareza", "positividade", "realização"],
        "upright": "Sucesso radiante em todos os empreendimentos, alegria pura que ilumina o caminho, vitalidade renovada que energiza todos os aspectos da vida, clareza mental que dissolve confusões, positividade contagiante.",
        "reversed": "Falta de sucesso devido a pessimismo, tristeza que obscurece as oportunidades, baixa vitalidade que impede o progresso, falta de clareza sobre os objetivos, negatividade que afasta bênçãos.",
        "archetype": "A Luz Divina",
        "life_lesson": "Irradiar luz e positividade para iluminar o mundo.",
        "shadow": "Pessimismo e negatividade que obscurecem a luz interior.",
        "themes": ["sucesso", "alegria", "vitalidade", "clareza"]
    },

    {
        "name": "O Julgamento",
        "number": 20,
        "type": "Arcano Maior",
        "element": "Fogo",
        "astrology": "Plutão",
        "keywords": ["renascimento", "chamado", "julgamento", "absolvição", "despertar", "propósito"],
        "upright": "Renascimento espiritual para uma nova fase da vida, chamado superior que desperta o propósito, julgamento sábio baseado na experiência, absolvição que liberta do passado, despertar para a verdadeira missão.",
        "reversed": "Autocrítica destrutiva que impede o crescimento, ignorar o chamado superior, dúvidas que paralizam a evolução, culpa que mantém preso ao passado, resistência ao renascimento espiritual.",
        "archetype": "O Despertador",
        "life_lesson": "Responder ao chamado superior e renascer para um propósito maior.",
        "shadow": "Autocrítica e culpa que impedem a evolução.",
        "themes": ["renascimento", "propósito", "chamado", "despertar"]
    },

    {
        "name": "O Mundo",
        "number": 21,
        "type": "Arcano Maior",
        "element": "Terra",
        "astrology": "Saturno",
        "keywords": ["realização", "completude", "integração", "sucesso", "harmonia", "plenitude"],
        "upright": "Realização completa de um ciclo importante, integração harmoniosa de todas as experiências, sucesso que coroa uma longa jornada, plenitude que traz paz profunda, harmonia perfeita entre todos os aspectos da vida.",
        "reversed": "Falta de conclusão em projetos importantes, sensação de incompletude, busca por atalhos que não levam à realização verdadeira, atrasos na conclusão de ciclos, falta de integração das experiências.",
        "archetype": "A Realização Cósmica",
        "life_lesson": "Integrar todas as experiências para alcançar a plenitude.",
        "shadow": "Incompletude e falta de integração das experiências.",
        "themes": ["realização", "completude", "sucesso", "integração"]
    },

    #  ARCANOS_MENORES

    # ═══════════════════════════════════════════════════════════════════
    #                           NAIPE DE PAUS
    #                     (Elemento Fogo - Energia, Paixão, Criatividade)
    # ═══════════════════════════════════════════════════════════════════

    {
        "name": "Ás de Paus",
        "number": 1,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["inspiração divina", "potencial criativo", "nova energia", "paixão ardente", "iniciativa", "centelha sagrada"],
        "upright": "A centelha divina da inspiração que inflama novos projetos e possibilidades infinitas. Representa o potencial criativo em seu estado mais puro, a energia vital renovada que impulsiona grandes realizações, e a paixão que pode transformar sonhos em realidade. É o chamado para a ação corajosa e a iniciativa que abre caminhos inéditos na vida.",
        "reversed": "Inspiração bloqueada por medos profundos ou autocrítica destrutiva, falta de motivação para abraçar novos começos, oportunidades criativas desperdiçadas por procrastinação ou autoboicote, energia vital baixa devido a burnout emocional, iniciativas fracas por falta de confiança interior.",
        "themes": ["criatividade", "carreira", "inspiração", "energia vital", "novos começos"],
        "affirmation": "Eu abraço a centelha divina da inspiração e permito que ela guie meus novos projetos com paixão e coragem.",
        "shadow_work": "Que medos ou crenças limitantes estão bloqueando minha energia criativa natural?",
        "spiritual_message": "O universo está oferecendo uma nova oportunidade de expressão criativa. Confie na sua intuição e dê o primeiro passo."
    },

    {
        "name": "Dois de Paus",
        "number": 2,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["planejamento estratégico", "visão futura", "poder pessoal", "domínio", "escolhas conscientes", "liderança"],
        "upright": "O planejamento estratégico que constrói o futuro desejado através de decisões conscientes e bem fundamentadas. Representa a visão clara dos objetivos de longo prazo, o poder pessoal sendo exercido com sabedoria e responsabilidade, e o domínio sobre as circunstâncias da vida através de escolhas alinhadas com o propósito maior.",
        "reversed": "Falta de planejamento adequado que leva ao caos, medo paralisante do desconhecido, indecisão crônica que desperdiça oportunidades preciosas, falta de visão clara sobre o futuro desejado, poder pessoal mal utilizado ou negligenciado por insegurança.",
        "themes": ["planejamento", "decisões", "futuro", "poder pessoal", "liderança"],
        "affirmation": "Eu tenho o poder de moldar meu futuro através de decisões conscientes e planejamento sábio.",
        "shadow_work": "Onde estou evitando tomar decisões importantes por medo do desconhecido?",
        "spiritual_message": "Você possui mais poder sobre sua vida do que imagina. É hora de assumir o controle consciente do seu destino."
    },

    {
        "name": "Três de Paus",
        "number": 3,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["expansão", "visão de futuro", "exploração", "progresso", "oportunidades distantes", "crescimento"],
        "upright": "A expansão natural que surge quando plantamos sementes com intenção clara e nutrimos com dedicação. Representa a visão que se estende além do horizonte conhecido, o progresso constante em direção aos objetivos, e a capacidade de reconhecer oportunidades em territórios inexplorados da vida.",
        "reversed": "Obstáculos que impedem o progresso natural, atrasos frustrantes em planos importantes, falta de visão ampla que limita as possibilidades, resistência inconsciente à expansão por medo do sucesso ou mudança.",
        "themes": ["expansão", "progresso", "oportunidades", "visão", "crescimento"],
        "affirmation": "Eu expando minha visão além do conhecido e abraço as oportunidades de crescimento que se apresentam.",
        "shadow_work": "Que limitações autoim postas estão impedindo minha expansão natural?",
        "spiritual_message": "Seus esforços estão florescendo. Mantenha a fé e continue expandindo sua visão do possível."
    },

    {
        "name": "Quatro de Paus",
        "number": 4,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["celebração", "harmonia", "realização", "comunidade", "estabilidade alegre", "marcos alcançados"],
        "upright": "A celebração merecida dos marcos alcançados e das realizações conquistadas através do esforço dedicado. Representa a harmonia encontrada entre ambição pessoal e conexões significativas, a estabilidade que permite relaxar e desfrutar dos frutos do trabalho, e a importância da comunidade em nossa jornada de crescimento.",
        "reversed": "Conflitos domésticos que perturbam a paz interior, falta de harmonia entre vida pessoal e profissional, instabilidade emocional que impede a verdadeira celebração, isolamento que priva da alegria compartilhada.",
        "themes": ["celebração", "harmonia", "comunidade", "estabilidade", "realização"],
        "affirmation": "Eu celebro minhas conquistas e cultivo a harmonia em todos os aspectos da minha vida.",
        "shadow_work": "Estou permitindo que conflitos externos perturbem minha paz interior?",
        "spiritual_message": "É momento de celebrar suas conquistas e reconhecer o quanto já cresceu em sua jornada."
    },

    {
        "name": "Cinco de Paus",
        "number": 5,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["conflito criativo", "competição saudável", "tensão transformadora", "crescimento através do desafio", "diversidade", "debate"],
        "upright": "O conflito criativo que surge quando diferentes perspectivas se encontram, gerando crescimento e inovação. Representa a competição saudável que nos desafia a dar o melhor de nós, a tensão necessária que impulsiona a transformação pessoal, e a importância de defender nossas convicções com integridade.",
        "reversed": "Resolução harmoniosa de conflitos antigos, fim de lutas desnecessárias, acordo pacífico entre partes divergentes, superação de tensões que não serviam ao crescimento, união após períodos de divisão.",
        "themes": ["conflito", "crescimento", "competição", "transformação", "diversidade"],
        "affirmation": "Eu transformo conflitos em oportunidades de crescimento e defendo minhas convicções com respeito.",
        "shadow_work": "Como posso usar os conflitos em minha vida como catalisadores para o crescimento?",
        "spiritual_message": "Os desafios atuais estão fortalecendo sua determinação e clarificando seus valores essenciais."
    },

    {
        "name": "Seis de Paus",
        "number": 6,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["vitória merecida", "reconhecimento público", "sucesso", "liderança inspiradora", "progresso visível", "triunfo"],
        "upright": "A vitória merecida que surge após períodos de esforço consistente e dedicação autêntica. Representa o reconhecimento público das nossas capacidades e conquistas, o sucesso que inspira outros a buscar sua própria excelência, e o momento de colher os frutos de uma jornada percorrida com integridade.",
        "reversed": "Queda da posição conquistada por negligência ou arrogância, falta de reconhecimento por esforços genuínos, fracasso que ensina humildade e redireciona o caminho, sucesso superficial que não traz satisfação real.",
        "themes": ["vitória", "reconhecimento", "sucesso", "liderança", "progresso"],
        "affirmation": "Eu celebro minhas vitórias com humildade e uso meu sucesso para inspirar outros.",
        "shadow_work": "Estou buscando reconhecimento externo em detrimento da minha satisfação interior?",
        "spiritual_message": "Sua dedicação está sendo reconhecida. Continue liderando com o exemplo e inspirando outros."
    },

    {
        "name": "Sete de Paus",
        "number": 7,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["defesa de princípios", "perseverança", "coragem diante da adversidade", "proteção", "resistência", "determinação"],
        "upright": "A defesa corajosa dos princípios e valores que definem nossa essência, mesmo quando confrontados por oposição ou adversidade. Representa a perseverança que nos mantém firmes em nossos objetivos, a coragem de proteger o que é sagrado para nós, e a determinação que supera obstáculos aparentemente intransponíveis.",
        "reversed": "Desistência prematura por exaustão emocional, sentimento de estar sobrecarregado pelos desafios, falta de energia para continuar a luta, esgotamento que compromete a capacidade de defesa dos próprios valores.",
        "themes": ["defesa", "perseverança", "coragem", "proteção", "resistência"],
        "affirmation": "Eu defendo meus valores com coragem e persevero mesmo diante das maiores adversidades.",
        "shadow_work": "Estou lutando pelas coisas certas ou desperdiçando energia em batalhas desnecessárias?",
        "spiritual_message": "Sua perseverança está sendo testada, mas você tem a força interior necessária para prevalecer."
    },

    {
        "name": "Oito de Paus",
        "number": 8,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["movimento acelerado", "progresso rápido", "comunicação eficaz", "energia em movimento", "velocidade", "dinamismo"],
        "upright": "O movimento acelerado que surge quando todas as forças se alinham em direção ao objetivo desejado. Representa o progresso rápido e eficiente, a comunicação clara que remove obstáculos, a energia em movimento constante que gera resultados visíveis, e o dinamismo que transforma intenções em realidade.",
        "reversed": "Atrasos frustrantes que testam a paciência, estagnação que gera ansiedade e impaciência, desaceleração forçada que exige reajuste de expectativas, energia bloqueada que precisa encontrar novos canais de expressão.",
        "themes": ["movimento", "progresso", "comunicação", "velocidade", "dinamismo"],
        "affirmation": "Eu fluo com a energia do progresso e permito que o movimento natural da vida me leve adiante.",
        "shadow_work": "Estou resistindo ao fluxo natural da vida ou forçando resultados prematuramente?",
        "spiritual_message": "As coisas estão se movendo rapidamente a seu favor. Mantenha-se flexível e receptivo às mudanças."
    },

    {
        "name": "Nove de Paus",
        "number": 9,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["resiliência testada", "força interior", "persistência heroica", "último esforço", "coragem final", "determinação inabalável"],
        "upright": "A resiliência profunda que emerge nos momentos de maior desafio, quando parece que chegamos ao nosso limite. Representa a força interior que se revela apenas nas situações mais difíceis, a persistência heroica que recusa a desistência, e a coragem final que nos leva à vitória mesmo quando as odds estão contra nós.",
        "reversed": "Exaustão profunda que compromete a capacidade de continuar, cansaço emocional que leva à desistência prematura, paranoia que distorce a percepção da realidade, esgotamento que exige descanso e recuperação.",
        "themes": ["resiliência", "força interior", "persistência", "coragem", "superação"],
        "affirmation": "Eu possuo uma força interior inesgotável que me sustenta nos momentos mais desafiadores.",
        "shadow_work": "Estou verdadeiramente esgotado ou apenas com medo de dar o último passo?",
        "spiritual_message": "Você está mais próximo da vitória do que imagina. Sua força interior é maior do que qualquer obstáculo."
    },

    {
        "name": "Dez de Paus",
        "number": 10,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["fardo pesado", "responsabilidade excessiva", "conclusão próxima", "último esforço", "peso da liderança", "sacrifício necessário"],
        "upright": "O fardo pesado das responsabilidades que assumimos em nossa jornada de crescimento e liderança. Representa o peso que carregamos quando nos comprometemos verdadeiramente com nossos objetivos, o sacrifício necessário antes da recompensa, e a compreensão de que grandes realizações exigem grandes esforços.",
        "reversed": "Liberação de fardos desnecessários através de delegação inteligente, alívio que surge quando aprendemos a compartilhar responsabilidades, recuperação de energia após períodos de sobrecarga, renovação que vem com o término de ciclos pesados.",
        "themes": ["responsabilidade", "fardo", "esforço", "conclusão", "sacrifício"],
        "affirmation": "Eu carrego minhas responsabilidades com propósito e sei quando é hora de compartilhar o fardo.",
        "shadow_work": "Estou assumindo responsabilidades excessivas por medo de perder controle ou por necessidade de aprovação?",
        "spiritual_message": "O peso que você carrega é temporário. Sua dedicação será recompensada em breve."
    },

    {
        "name": "Pajem de Paus",
        "number": 11,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["entusiasmo jovem", "exploração criativa", "liberdade de expressão", "curiosidade ardente", "aventura", "potencial emergente"],
        "upright": "O entusiasmo contagiante da juventude que vê possibilidades infinitas em cada oportunidade. Representa a exploração criativa sem limites ou preconceitos, a liberdade de expressão autêntica, a curiosidade ardente que nos leva a descobrir novos talentos, e o potencial emergente que anseia por manifestação.",
        "reversed": "Inquietação que não encontra direção construtiva, falta de foco que dispersa a energia criativa, procrastinação que adia a materialização dos talentos, impaciência que compromete o desenvolvimento natural das habilidades.",
        "themes": ["entusiasmo", "exploração", "criatividade", "liberdade", "potencial"],
        "affirmation": "Eu abraço meu entusiasmo natural e permito que minha curiosidade me guie a novas descobertas.",
        "shadow_work": "Minha inquietação é um sinal de crescimento ou uma fuga da responsabilidade?",
        "spiritual_message": "Sua curiosidade e entusiasmo são dons preciosos. Use-os para explorar seu potencial criativo."
    },

    {
        "name": "Cavaleiro de Paus",
        "number": 12,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["ação impulsiva", "paixão ardente", "aventura corajosa", "energia em movimento", "liderança natural", "coragem pioneira"],
        "upright": "A ação impulsiva guiada pela paixão autêntica e o desejo genuíno de progresso. Representa a aventura corajosa que nos leva a territórios inexplorados, a energia em movimento constante que não aceita estagnação, e a liderança natural que inspira outros através do exemplo dinâmico.",
        "reversed": "Impulsividade destrutiva que ignora as consequências, pressa excessiva que compromete a qualidade dos resultados, falta de direção clara que desperdiça energia preciosa, frustração que surge quando a ação não é seguida de planejamento.",
        "themes": ["ação", "paixão", "aventura", "liderança", "movimento"],
        "affirmation": "Eu canalizo minha paixão em ações construtivas e lidero através do exemplo inspirador.",
        "shadow_work": "Minhas ações impulsivas estão me aproximando ou me afastando dos meus objetivos verdadeiros?",
        "spiritual_message": "Sua paixão é uma força poderosa. Channel-a com sabedoria para alcançar grandes realizações."
    },

    {
        "name": "Rainha de Paus",
        "number": 13,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["confiança magnética", "liderança calorosa", "independência sábia", "determinação gentil", "carisma natural", "força feminina"],
        "upright": "A confiança magnética que atrai oportunidades e pessoas alinhadas com nossa visão. Representa a liderança calorosa que inspira através do exemplo e da compaixão, a independência sábia que não teme a solidão mas valoriza as conexões autênticas, e a determinação gentil que alcança objetivos sem perder a humanidade.",
        "reversed": "Insegurança mascarada por atitudes defensivas, ciúme que revela feridas não curadas, agressividade que afasta as pessoas que mais amamos, dominância que confunde força com controle.",
        "themes": ["confiança", "liderança", "independência", "determinação", "carisma"],
        "affirmation": "Eu lidero com confiança e compaixão, mantendo minha independência sem perder minha conexão humana.",
        "shadow_work": "Onde minha confiança se torna arrogância ou minha independência se torna isolamento?",
        "spiritual_message": "Sua força interior é um farol para outros. Use-a para elevar e inspirar aqueles ao seu redor."
    },

    {
        "name": "Rei de Paus",
        "number": 14,
        "type": "Arcano Menor",
        "suit": "Paus",
        "element": "Fogo",
        "keywords": ["liderança visionária", "empreendedorismo sábio", "autoridade natural", "visão de longo prazo", "integridade", "poder responsável"],
        "upright": "A liderança visionária que constrói legados duradouros através de decisões éticas e estratégicas. Representa o empreendedorismo sábio que cria valor para todos os envolvidos, a autoridade natural que se manifesta através da competência e integridade, e o poder responsável que serve ao bem maior.",
        "reversed": "Impulsividade que compromete a liderança responsável, pressa que atropela processos importantes, crueldade que surge da frustração com limitações, expectativas irreais que geram decepção e conflito.",
        "themes": ["liderança", "visão", "autoridade", "integridade", "responsabilidade"],
        "affirmation": "Eu lidero com visão, integridade e responsabilidade, criando valor duradouro para todos.",
        "shadow_work": "Estou usando meu poder para servir ou para controlar? Minha liderança eleva ou diminui os outros?",
        "spiritual_message": "Você possui a sabedoria e a força necessárias para liderar com integridade. Use seu poder para o bem comum."
    },

    # ═══════════════════════════════════════════════════════════════════
    #                           NAIPE DE COPAS
    #                      (Elemento Água - Emoções, Intuição, Amor)
    # ═══════════════════════════════════════════════════════════════════

    {
        "name": "Ás de Copas",
        "number": 1,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["amor divino", "compaixão universal", "criatividade emocional", "conexão espiritual", "intuição pura", "coração aberto"],
        "upright": "O amor divino que flui livremente quando abrimos nosso coração para receber e compartilhar sem condições. Representa a compaixão universal que nos conecta a todos os seres, a criatividade emocional que nasce da autenticidade, e a intuição pura que nos guia através da sabedoria do coração.",
        "reversed": "Amor reprimido por medos de vulnerabilidade, bloqueio emocional que impede conexões profundas, tristeza que nubla a capacidade de dar e receber afeto, desconexão espiritual que gera vazio interior.",
        "themes": ["amor", "compaixão", "criatividade", "espiritualidade", "intuição"],
        "affirmation": "Eu abro meu coração para receber e compartilhar amor incondicional com o mundo.",
        "shadow_work": "Que medos estão impedindo meu coração de se abrir completamente para o amor?",
        "spiritual_message": "O amor universal está fluindo através de você. Permita-se ser um canal de compaixão no mundo."
    },

    {
        "name": "Dois de Copas",
        "number": 2,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["parceria sagrada", "amor equilibrado", "união de almas", "harmonia emocional", "reciprocidade", "conexão profunda"],
        "upright": "A parceria sagrada que surge quando duas almas se reconhecem e escolhem caminhar juntas em harmonia. Representa o amor equilibrado baseado em respeito mútuo e crescimento compartilhado, a união que fortalece ambas as partes, e a conexão profunda que transcende o físico e toca o espiritual.",
        "reversed": "Rompimento doloroso que ensina sobre nossos padrões relacionais, desarmonia que revela incompatibilidades fundamentais, desequilíbrio que surge quando uma parte dá mais do que recebe, conflitos que testam a autenticidade da conexão.",
        "themes": ["parceria", "amor", "união", "harmonia", "reciprocidade"],
        "affirmation": "Eu atraio e cultivo relacionamentos baseados em amor equilibrado e crescimento mútuo.",
        "shadow_work": "Estou buscando completude no outro ou já me sinto completo em mim mesmo?",
        "spiritual_message": "O amor verdadeiro está se manifestando em sua vida. Abra-se para conexões autênticas e nutritivas."
    },

    {
        "name": "Três de Copas",
        "number": 3,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["celebração comunitária", "amizade genuína", "criatividade coletiva", "alegria compartilhada", "sororidade", "abundância emocional"],
        "upright": "A alegria que nasce do compartilhamento autêntico com aqueles que verdadeiramente nos compreendem e apoiam. Representa a força da comunidade emocional, a criatividade que floresce na colaboração, e a celebração das vitórias que se tornam mais significativas quando divididas com amor.",
        "reversed": "Isolamento autoimposto por medo de julgamento, superficialidade nas conexões sociais, fofoca que destrói laços genuínos, excesso que mascara vazios emocionais e busca por validação externa.",
        "themes": ["amizade", "comunidade", "celebração", "criatividade", "alegria"],
        "affirmation": "Eu celebro a vida em comunhão com aqueles que nutrem minha alma.",
        "shadow_work": "Estou me conectando autenticamente ou apenas buscando aprovação social?",
        "spiritual_message": "A alegria é multiplicada quando compartilhada. Permita-se celebrar suas vitórias com quem realmente importa."
    },

    {
        "name": "Quatro de Copas",
        "number": 4,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["contemplação profunda", "reavaliação emocional", "descontentamento sagrado", "busca interior", "pausa reflexiva", "despertar espiritual"],
        "upright": "O momento sagrado de pausa e contemplação que precede grandes transformações interiores. Representa o descontentamento saudável que nos leva a questionar nossas escolhas, a necessidade de olhar para dentro antes de seguir adiante, e a sabedoria de não aceitar menos do que merecemos emocionalmente.",
        "reversed": "Apatia que nos desconecta da vida, perda de oportunidades por excesso de passividade, estagnação que nasce do medo de mudança, recusa em ver as bênçãos presentes em nossa jornada.",
        "themes": ["contemplação", "reavaliação", "busca interior", "transformação", "discernimento"],
        "affirmation": "Eu honro minha necessidade de contemplação e busco clareza antes de tomar decisões importantes.",
        "shadow_work": "Estou em contemplação produtiva ou fugindo das responsabilidades da vida?",
        "spiritual_message": "Às vezes precisamos parar para olhar dentro de nós. Esta pausa trará clareza sobre seu próximo passo."
    },

    {
        "name": "Cinco de Copas",
        "number": 5,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["luto sagrado", "transformação através da perda", "aceitação da dor", "renascimento emocional", "sabedoria do sofrimento", "cura profunda"],
        "upright": "O processo sagrado de luto que nos ensina sobre a impermanência e nos conecta com nossa humanidade mais profunda. Representa a transformação que nasce da perda, a sabedoria que emerge do sofrimento conscientemente vivido, e a força que descobrimos quando atravessamos nossos momentos mais escuros.",
        "reversed": "Aceitação gradual que permite o movimento adiante, perdão que liberta o coração do ressentimento, capacidade de encontrar esperança mesmo nas situações mais desafiadoras, cura que nasce da integração da experiência dolorosa.",
        "themes": ["luto", "perda", "transformação", "aceitação", "cura"],
        "affirmation": "Eu permito que minha dor me ensine e me transforme, sabendo que ela é parte de meu crescimento.",
        "shadow_work": "Como posso honrar minha dor sem me identificar completamente com ela?",
        "spiritual_message": "Suas lágrimas são sagradas. Elas estão lavando sua alma para um novo renascimento."
    },

    {
        "name": "Seis de Copas",
        "number": 6,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["inocência recuperada", "cura da criança interior", "nostalgia sagrada", "reconexão com a essência", "simplicidade", "amor puro"],
        "upright": "O retorno à inocência e pureza que residem eternamente em nosso coração, independente das experiências vividas. Representa a cura da criança interior, a capacidade de ver o mundo com olhos de admiração novamente, e a reconexão com a simplicidade e espontaneidade que nutrem nossa alma.",
        "reversed": "Fixação no passado que impede crescimento presente, idealização que distorce a realidade atual, ingenuidade que nos torna vulneráveis a manipulações, recusa em amadurecer e assumir responsabilidades adultas.",
        "themes": ["infância", "inocência", "simplicidade", "nostalgia", "cura interior"],
        "affirmation": "Eu abraço minha criança interior com amor e permito que sua sabedoria inocente guie meu coração.",
        "shadow_work": "Estou honrando meu passado ou sendo prisioneiro dele?",
        "spiritual_message": "Sua pureza interior permanece intacta. Reconecte-se com a criança sábia que vive em seu coração."
    },

    {
        "name": "Sete de Copas",
        "number": 7,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["visões espirituais", "discernimento intuitivo", "múltiplas possibilidades", "imaginação criativa", "sonhos proféticos", "escolhas do coração"],
        "upright": "A riqueza de possibilidades que se abre quando sintonizamos nossa intuição e imaginação criativa. Representa a capacidade de sonhar além das limitações aparentes, a visão espiritual que enxerga potenciais ocultos, e o dom de escolher com o coração aquilo que verdadeiramente ressoa com nossa alma.",
        "reversed": "Ilusões que nos afastam da realidade prática, fantasia excessiva que impede ação concreta, confusão entre desejos ego e chamados da alma, dispersão que nos impede de focar no essencial.",
        "themes": ["visões", "imaginação", "possibilidades", "escolhas", "intuição"],
        "affirmation": "Eu uso minha imaginação para criar realidades alinhadas com meu propósito mais elevado.",
        "shadow_work": "Minhas visões me inspiram à ação ou me mantêm em fantasia improdutiva?",
        "spiritual_message": "Suas visões são sementes de realidades futuras. Escolha com sabedoria e aja com determinação."
    },

    {
        "name": "Oito de Copas",
        "number": 8,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["busca espiritual", "desapego sagrado", "jornada interior", "coragem de partir", "busca por significado", "transformação profunda"],
        "upright": "A coragem sagrada de deixar para trás aquilo que não nos serve mais, mesmo quando é familiar e confortável. Representa a jornada espiritual em busca de significado mais profundo, o desapego que nos liberta para crescer, e a sabedoria de reconhecer quando é tempo de seguir um novo caminho.",
        "reversed": "Medo de mudança que nos mantém em situações estagnadas, apego excessivo ao conhecido mesmo quando é limitante, fuga de responsabilidades ao invés de transformação consciente, estagnação emocional e espiritual.",
        "themes": ["desapego", "jornada", "busca", "transformação", "coragem"],
        "affirmation": "Eu tenho coragem de deixar ir aquilo que não me serve mais para abraçar meu crescimento.",
        "shadow_work": "Estou partindo por crescimento ou fugindo por medo?",
        "spiritual_message": "Sua alma está chamando você para uma jornada mais profunda. Confie na sabedoria de seu coração."
    },

    {
        "name": "Nove de Copas",
        "number": 9,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["satisfação emocional", "abundância do coração", "gratidão profunda", "realização pessoal", "alegria genuína", "plenitude interior"],
        "upright": "A satisfação profunda que nasce quando alinhamos nossa vida exterior com nossos valores mais autênticos. Representa a abundância emocional que vem da gratidão, a alegria genuína que brota de conquistas significativas, e a sensação de plenitude que surge quando honramos nossos verdadeiros desejos.",
        "reversed": "Busca de satisfação em fontes externas que não preenchem verdadeiramente, materialismo que mascara vazio emocional, desejos nunca saciados por não nascerem da alma, superficialidade que impede conexão com a verdadeira alegria.",
        "themes": ["satisfação", "abundância", "gratidão", "realização", "alegria"],
        "affirmation": "Eu celebro minhas conquistas e cultivo gratidão pela abundância que já existe em minha vida.",
        "shadow_work": "Minha satisfação vem de fontes autênticas ou de validação externa?",
        "spiritual_message": "Você merece celebrar suas vitórias. Permita-se sentir a plenitude que conquistou."
    },

    {
        "name": "Dez de Copas",
        "number": 10,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["harmonia familiar", "legado emocional", "amor incondicional", "ciclo completo", "felicidade duradoura", "conexão geracional"],
        "upright": "A realização máxima no plano emocional através da construção de laços familiares e comunitários baseados em amor incondicional. Representa a harmonia que surge quando cada membro se sente valorizado, o legado emocional positivo que transmitimos, e a felicidade duradoura que nasce de relacionamentos autênticos.",
        "reversed": "Conflitos familiares que revelam valores desalinhados, laços quebrados por expectativas não atendidas, superficialidade nas conexões que parecem perfeitas por fora, disfunção mascarada por aparências sociais.",
        "themes": ["família", "harmonia", "legado", "amor", "plenitude"],
        "affirmation": "Eu cultivo relacionamentos familiares baseados em amor incondicional e aceitação mútua.",
        "shadow_work": "Estou construindo harmonia verdadeira ou mantendo aparências?",
        "spiritual_message": "O amor que você semeia em sua família e comunidade é seu maior legado. Continue nutrindo esses laços sagrados."
    },

    {
        "name": "Pajem de Copas",
        "number": 11,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["mensageiro do coração", "intuição emergente", "criatividade nascente", "sensibilidade artística", "pureza emocional", "abertura espiritual"],
        "upright": "A chegada de mensagens importantes através da intuição e sensibilidade emocional. Representa o despertar da criatividade artística, a pureza de sentimentos que ainda não foram contaminados por cinismo, e a abertura espiritual que nos conecta com dimensões sutis da existência.",
        "reversed": "Imaturidade emocional que gera decisões impulsivas, bloqueio criativo por medo de vulnerabilidade, hipersensibilidade que dificulta relacionamentos, insegurança que impede expressão autêntica dos sentimentos.",
        "themes": ["intuição", "criatividade", "sensibilidade", "mensagens", "pureza"],
        "affirmation": "Eu confio nas mensagens que meu coração e intuição me enviam.",
        "shadow_work": "Como posso honrar minha sensibilidade sem me tornar refém dela?",
        "spiritual_message": "Sua sensibilidade é um dom. Use-a para criar beleza e conexão no mundo."
    },

    {
        "name": "Cavaleiro de Copas",
        "number": 12,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["romântico espiritual", "busca do amor ideal", "charme autêntico", "imaginação elevada", "idealismo transformador", "beleza interior"],
        "upright": "A busca apaixonada pela expressão mais elevada do amor e da beleza em todas as áreas da vida. Representa o charme que nasce da autenticidade, a imaginação que cria realidades mais belas, e o idealismo que nos inspira a elevar nossos padrões emocionais e espirituais.",
        "reversed": "Idealismo excessivo que gera desilusão constante, charme superficial usado para manipulação, ciúme que nasce de insegurança profunda, instabilidade emocional que prejudica relacionamentos duradouros.",
        "themes": ["romance", "idealismo", "charme", "beleza", "busca"],
        "affirmation": "Eu busco e expresso a beleza mais elevada em todos os meus relacionamentos.",
        "shadow_work": "Meu idealismo me inspira ou me impede de aceitar a realidade?",
        "spiritual_message": "Seu coração romântico é uma força transformadora. Use-o para elevar a qualidade do amor ao seu redor."
    },

    {
        "name": "Rainha de Copas",
        "number": 13,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["mãe divina", "compaixão incondicional", "intuição madura", "cuidado nutritivo", "sabedoria emocional", "fluidez adaptativa"],
        "upright": "A personificação da mãe divina que nutre e protege com amor incondicional. Representa a compaixão madura que compreende sem julgar, a intuição refinada que percebe necessidades não expressas, e a sabedoria emocional que oferece cura e conforto a todos que se aproximam.",
        "reversed": "Codependência que prejudica ao invés de ajudar, manipulação emocional disfarçada de cuidado, hipersensibilidade que gera instabilidade nos relacionamentos, tendência a absorver emoções alheias perdendo os próprios limites.",
        "themes": ["compaixão", "intuição", "cuidado", "sabedoria", "nutrição"],
        "affirmation": "Eu ofereço amor incondicional mantendo limites saudáveis e respeitosos.",
        "shadow_work": "Estou cuidando com amor ou tentando controlar através do cuidado?",
        "spiritual_message": "Sua compaixão é uma força de cura no mundo. Use-a com sabedoria e discernimento."
    },

    {
        "name": "Rei de Copas",
        "number": 14,
        "type": "Arcano Menor",
        "suit": "Copas",
        "element": "Água",
        "keywords": ["mestre emocional", "liderança compassiva", "sabedoria do coração", "diplomacia amorosa", "equilíbrio emocional", "autoridade espiritual"],
        "upright": "O domínio maduro sobre o mundo emocional, combinando sensibilidade com estabilidade e sabedoria. Representa a liderança que inspira através do exemplo amoroso, a diplomacia que resolve conflitos com compaixão, e a autoridade espiritual que guia outros no caminho do coração.",
        "reversed": "Manipulação emocional para obter vantagens pessoais, instabilidade de humor que afeta negativamente outros, autoritarismo disfarçado de cuidado paternal, volatilidade que contradiz a sabedoria aparente.",
        "themes": ["liderança", "sabedoria", "equilíbrio", "compaixão", "maturidade"],
        "affirmation": "Eu lidero com sabedoria emocional e tomo decisões alinhadas com o amor e a compaixão.",
        "shadow_work": "Estou usando minha maturidade emocional para servir ou para controlar?",
        "spiritual_message": "Sua sabedoria emocional pode ser uma luz para outros. Lidere com o coração aberto e a mente clara."
    },

    # ═══════════════════════════════════════════════════════════════════
    #                           NAIPE DE ESPADAS
    #                    (Elemento Ar - Mente, Comunicação, Verdade)
    # ═══════════════════════════════════════════════════════════════════

    {
        "name": "Ás de Espadas",
        "number": 1,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["clareza mental", "verdade revelada", "força intelectual", "justiça divina", "comunicação poderosa", "discernimento puro"],
        "upright": "A força cortante da verdade que elimina ilusões e traz clareza absoluta sobre situações complexas. Representa o poder mental focado que pode transformar realidades, a comunicação autêntica que inspira mudanças, e o discernimento que separa o essencial do supérfluo com precisão cirúrgica.",
        "reversed": "Confusão mental que nubla julgamentos importantes, desinformação que distorce percepções da realidade, falta de clareza que gera decisões precipitadas, caos mental que impede progresso e crescimento.",
        "themes": ["clareza", "verdade", "comunicação", "discernimento", "justiça"],
        "affirmation": "Eu busco e expresso a verdade com clareza, coragem e compaixão.",
        "shadow_work": "Estou usando minha clareza mental para construir ou para destruir?",
        "spiritual_message": "A verdade está se revelando. Use sua clareza mental para tomar decisões sábias e justas."
    },

    {
        "name": "Dois de Espadas",
        "number": 2,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["decisão consciente", "equilíbrio mental", "pausa reflexiva", "integração de opostos", "mediação interna", "sabedoria da espera"],
        "upright": "O momento sagrado de pausa antes de decisões importantes, quando equilibramos cuidadosamente todas as informações disponíveis. Representa a capacidade de manter equilíbrio mental mesmo diante de pressões, a sabedoria de não agir precipitadamente, e a integração consciente de perspectivas opostas.",
        "reversed": "Indecisão paralisante que impede progresso necessário, sobrecarga de informações que confunde ao invés de esclarecer, evitação de decisões que precisam ser tomadas, análise excessiva que substitui a ação necessária.",
        "themes": ["decisão", "equilíbrio", "reflexão", "integração", "paciência"],
        "affirmation": "Eu tomo decisões equilibradas, integrando razão e intuição com sabedoria.",
        "shadow_work": "Estou sendo prudente ou evitando responsabilidades?",
        "spiritual_message": "Nem todas as decisões precisam ser tomadas imediatamente. Confie no timing divino."
    },

    {
        "name": "Três de Espadas",
        "number": 3,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["transformação através da dor", "cura emocional", "libertação de ilusões", "crescimento pela adversidade", "compaixão profunda", "sabedoria do sofrimento"],
        "upright": "A dor necessária que quebra ilusões e abre espaço para crescimento autêntico. Representa o processo sagrado de luto que honra perdas importantes, a coragem de sentir emoções difíceis completamente, e a transformação que emerge quando atravessamos nossos desafios emocionais com presença e aceitação.",
        "reversed": "Cura gradual que traz renovada esperança, perdão que liberta o coração de ressentimentos antigos, superação consciente de traumas passados, integração saudável de experiências dolorosas que geram sabedoria.",
        "themes": ["transformação", "cura", "aceitação", "crescimento", "compaixão"],
        "affirmation": "Eu honro minha dor como professora e permito que ela me transforme em alguém mais sábio e compassivo.",
        "shadow_work": "Estou permitindo que minha dor me ensine ou estou me identificando com ela?",
        "spiritual_message": "Toda dor carrega uma semente de transformação. Permita que seu coração seja curado pelo amor."
    },

    {
        "name": "Quatro de Espadas",
        "number": 4,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["renovação interior", "meditação profunda", "pausa sagrada", "recalibramento mental", "silêncio restaurador", "preparação consciente"],
        "upright": "O retiro consciente da mente que busca paz e clareza através do silêncio interior. Representa a necessidade sagrada de pausar para integrar experiências, a prática de meditação que restaura equilíbrio mental, e a sabedoria de criar espaços de quietude para receber insights divinos.",
        "reversed": "Exaustão mental que sinaliza necessidade urgente de descanso, esgotamento que resulta de resistir ao que a vida apresenta, estagnação que surge da evitação de responsabilidades, estresse acumulado que obscurece clareza natural.",
        "themes": ["renovação", "meditação", "descanso", "integração", "preparação"],
        "affirmation": "Eu honro minha necessidade de silêncio e descanso como atos sagrados de autocuidado.",
        "shadow_work": "Estou descansando conscientemente ou fugindo de responsabilidades?",
        "spiritual_message": "O silêncio é onde a sabedoria nasce. Permita-se momentos de quietude restauradora."
    },

    {
        "name": "Cinco de Espadas",
        "number": 5,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["conflito transformador", "lições de humildade", "reavaliação de valores", "crescimento através de desafios", "sabedoria das perdas", "renovação de estratégias"],
        "upright": "O conflito que revela padrões tóxicos e força crescimento através de confrontos necessários. Representa lições difíceis sobre ego e cooperação, a descoberta de que nem toda vitória vale o preço pago, e a sabedoria que emerge quando questionamos nossos métodos e motivações.",
        "reversed": "Reconciliação genuína que cura feridas antigas, crescimento em humildade que permite relacionamentos mais autênticos, consciência renovada sobre impactos de nossas ações, perdão mútuo que restaura harmonia e confiança.",
        "themes": ["conflito", "crescimento", "humildade", "reconciliação", "sabedoria"],
        "affirmation": "Eu transformo conflitos em oportunidades de crescimento e compreensão mútua.",
        "shadow_work": "Estou lutando por princípios ou alimentando meu ego?",
        "spiritual_message": "Nem toda batalha precisa ser vencida. Às vezes, a maior vitória está em escolher a paz."
    },

    {
        "name": "Seis de Espadas",
        "number": 6,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["transição consciente", "jornada de cura", "movimento para águas calmas", "guia interior", "carregando sabedoria", "travessia transformadora"],
        "upright": "A jornada corajosa que nos leva de águas turbulentas para territórios de maior paz e clareza. Representa a transição consciente entre fases da vida, levando apenas o essencial da experiência passada, e a confiança de que existe orientação disponível durante mudanças importantes.",
        "reversed": "Resistência a mudanças necessárias que prolonga sofrimento desnecessário, bagagem emocional que impede progresso saudável, medo de deixar o familiar mesmo quando não serve mais, apego a situações que limitam crescimento.",
        "themes": ["transição", "cura", "orientação", "libertação", "progresso"],
        "affirmation": "Eu navego mudanças com confiança, carregando apenas a sabedoria que me serve.",
        "shadow_work": "O que estou me recusando a deixar para trás?",
        "spiritual_message": "Confie na jornada. Você está sendo guiado para águas mais calmas e consciência mais ampla."
    },

    {
        "name": "Sete de Espadas",
        "number": 7,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["estratégia inteligente", "diplomacia sutil", "navegação cuidadosa", "adaptabilidade criativa", "discernimento social", "movimento calculado"],
        "upright": "A arte de navegar situações complexas com inteligência estratégica e adaptabilidade criativa. Representa a capacidade de encontrar soluções não convencionais para problemas desafiadores, a diplomacia que evita confrontos desnecessários, e o discernimento sobre quando ser direto ou sutil.",
        "reversed": "Desonestidade que corrói confiança e integridade pessoal, manipulação que prejudica relacionamentos autênticos, estratégias baseadas em medo ao invés de sabedoria, peso da consciência quando ações não alinham com valores.",
        "themes": ["estratégia", "adaptabilidade", "discernimento", "inteligência", "navegação"],
        "affirmation": "Eu navego desafios com inteligência, integridade e criatividade adaptativa.",
        "shadow_work": "Minhas estratégias servem o bem maior ou apenas interesses pessoais?",
        "spiritual_message": "A sabedoria às vezes requer movimentos sutis. Confie em sua inteligência intuitiva."
    },

    {
        "name": "Oito de Espadas",
        "number": 8,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["libertação de limitações", "quebra de padrões mentais", "reconhecimento do próprio poder", "superação de crenças limitantes", "clareza que liberta", "despertar da consciência"],
        "upright": "O reconhecimento poderoso de que muitas limitações são construções mentais que podem ser transcendidas através de nova perspectiva. Representa o momento de despertar quando percebemos nosso poder de escolha, a coragem de questionar crenças limitantes, e a liberdade que vem com responsabilidade pessoal.",
        "reversed": "Libertação gradual de padrões que não servem mais, desenvolvimento de novas perspectivas que expandem possibilidades, aceitação crescente de responsabilidade pessoal, movimento consciente em direção à autenticidade e autocompaixão.",
        "themes": ["libertação", "perspectiva", "poder pessoal", "consciência", "escolha"],
        "affirmation": "Eu reconheço meu poder de escolher novos pensamentos e criar nova realidade.",
        "shadow_work": "Quais crenças sobre mim mesmo estou pronto para questionar?",
        "spiritual_message": "A liberdade sempre foi sua. É tempo de reconhecer e usar seu poder de escolha."
    },

    {
        "name": "Nove de Espadas",
        "number": 9,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["confronto com medos", "noite escura da alma", "purificação através da adversidade", "coragem diante do desconhecido", "transformação profunda", "renascimento interior"],
        "upright": "A experiência intensa de confrontar nossos medos mais profundos e descobrir que podemos sobreviver e crescer através deles. Representa a jornada corajosa através da 'noite escura da alma', onde encontramos recursos internos que desconhecíamos possuir, e a transformação que emerge da travessia consciente de territórios sombrios.",
        "reversed": "Libertação gradual de padrões ansiosos que consomem energia vital, descoberta de recursos de apoio que oferecem esperança renovada, emergência de perspectivas otimistas após períodos difíceis, cura que traz paz interior e confiança renovada.",
        "themes": ["coragem", "transformação", "confronto", "crescimento", "renascimento"],
        "affirmation": "Eu tenho coragem para enfrentar meus medos e descobrir minha força interior.",
        "shadow_work": "Que medos estão me impedindo de viver plenamente?",
        "spiritual_message": "Seus medos são professores disfarçados. Atravesse-os com coragem e descubra sua luz interior."
    },

    {
        "name": "Dez de Espadas",
        "number": 10,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["fim transformador", "liberação total", "renascimento através da crise", "sabedoria das perdas", "phoenix interior", "novo começo radical"],
        "upright": "O final doloroso mas necessário que limpa completamente padrões antigos e abre espaço para renascimento autêntico. Representa o momento quando sistemas que não servem mais colapsam completamente, criando terreno fértil para crescimento genuíno, e a sabedoria que emerge quando atravessamos completamente processos de transformação.",
        "reversed": "Recuperação gradual que honra lições aprendidas através de experiências difíceis, regeneração consciente que integra sabedoria adquirida, resistência interior que evita repetição de padrões destrutivos, renascimento que emerge da travessia completa de desafios.",
        "themes": ["transformação", "renascimento", "liberação", "sabedoria", "novo começo"],
        "affirmation": "Eu confio que finais dolorosos abrem espaço para começos mais autênticos e alinhados.",
        "shadow_work": "O que em minha vida precisa morrer para que eu possa renascer?",
        "spiritual_message": "Todo fim é um começo disfarçado. Confie no processo de renovação que está ocorrendo."
    },

    {
        "name": "Pajem de Espadas",
        "number": 11,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["curiosidade intelectual", "mente aberta", "comunicação fresca", "aprendizado ávido", "perspectivas novas", "energia mental jovem"],
        "upright": "A energia jovem e curiosa da mente que se aproxima do conhecimento com entusiasmo genuíno e abertura para novas perspectivas. Representa a sede natural de aprender e compreender, a comunicação espontânea que inspira outros, e a coragem intelectual de questionar assumções e explorar territórios mentais desconhecidos.",
        "reversed": "Impulsividade mental que gera mal-entendidos desnecessários, comunicação precipitada que fere sem intenção, curiosidade que se transforma em fofoca destrutiva, energia intelectual dispersa que não gera resultados construtivos.",
        "themes": ["curiosidade", "aprendizado", "comunicação", "frescor", "exploração"],
        "affirmation": "Eu cultivo curiosidade saudável e comunico minhas descobertas com entusiasmo e responsabilidade.",
        "shadow_work": "Minha curiosidade está servindo meu crescimento ou satisfazendo ego?",
        "spiritual_message": "Mantenha sua mente jovem e curiosa. O aprendizado é uma jornada eterna de descoberta."
    },

    {
        "name": "Cavaleiro de Espadas",
        "number": 12,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["ação decidida", "coragem intelectual", "movimento direcionado", "liderança mental", "determinação focada", "pioneirismo corajoso"],
        "upright": "A energia dinâmica de ação mental focada que corta através de obstáculos com determinação e clareza de propósito. Representa a coragem de defender verdades importantes mesmo diante de resistência, o movimento rápido quando a situação demanda decisão, e a liderança intelectual que inspira outros através do exemplo.",
        "reversed": "Impulsividade que cria mais problemas do que soluções, agressividade mental que aliena ao invés de inspirar, ação precipitada sem consideração de consequências, opinião forçada que não respeita perspectivas alheias.",
        "themes": ["ação", "coragem", "liderança", "determinação", "foco"],
        "affirmation": "Eu ajo com coragem e determinação, equilibrando rapidez com sabedoria.",
        "shadow_work": "Minha ação está servindo um propósito maior ou apenas minha necessidade de controle?",
        "spiritual_message": "Coragem e sabedoria caminham juntas. Aja com determinação, mas permaneça aberto ao aprendizado."
    },

    {
        "name": "Rainha de Espadas",
        "number": 13,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["sabedoria madura", "clareza compassiva", "independência sábia", "comunicação precisa", "discernimento refinado", "liderança através da verdade"],
        "upright": "A expressão madura da clareza mental equilibrada com compaixão profunda e sabedoria experiencial. Representa a capacidade de ver através de ilusões com gentileza, a comunicação que é ao mesmo tempo honesta e bondosa, e a liderança que guia através do exemplo de integridade e discernimento refinado.",
        "reversed": "Frieza emocional que distancia de conexões autênticas, julgamento severo que pune ao invés de educar, isolamento que resulta de padrões perfeccionistas, comunicação cortante que fere sem necessidade.",
        "themes": ["sabedoria", "clareza", "compaixão", "integridade", "discernimento"],
        "affirmation": "Eu expresso minha sabedoria com clareza compassiva e discernimento amoroso.",
        "shadow_work": "Minha clareza está servindo o amor ou alimentando superioridade?",
        "spiritual_message": "Verdadeira sabedoria sempre vem acompanhada de compaixão. Seja clara, mas seja gentil."
    },

    {
        "name": "Rei de Espadas",
        "number": 14,
        "type": "Arcano Menor",
        "suit": "Espadas",
        "element": "Ar",
        "keywords": ["autoridade sábia", "justiça equilibrada", "liderança ética", "visão clara", "responsabilidade madura", "poder através da verdade"],
        "upright": "A expressão máxima da autoridade intelectual exercida através de princípios éticos elevados e compromisso inabalável com a justiça. Representa a liderança que inspira através da integridade, a capacidade de tomar decisões difíceis mas necessárias, e o poder que vem de alinhar ações com verdades universais.",
        "reversed": "Autoritarismo que impõe vontade através de medo ao invés de respeito, manipulação intelectual que distorce verdades para benefício pessoal, crueldade disfarçada de justiça, desonestidade que corrói confiança e autoridade moral.",
        "themes": ["autoridade", "justiça", "ética", "liderança", "integridade"],
        "affirmation": "Eu exerço minha autoridade com sabedoria, justiça e profunda responsabilidade pelo bem comum.",
        "shadow_work": "Estou usando meu poder para servir ou para dominar?",
        "spiritual_message": "Verdadeiro poder vem da dedicação à verdade e ao serviço. Lidere com integridade e compaixão."
    },

    # ═══════════════════════════════════════════════════════════════════
    #                           NAIPE DE OUROS
    #                  (Elemento Terra - Manifestação, Abundância, Materialidade)
    # ═══════════════════════════════════════════════════════════════════

    {
        "name": "Ás de Ouros",
        "number": 1,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["manifestação divina", "abundância nascente", "oportunidade dourada", "fundação sólida", "prosperidade alinhada", "materialização de sonhos"],
        "upright": "A energia pura de manifestação que transforma visões em realidade tangível através de ação consciente e alinhamento com propósito maior. Representa oportunidades douradas que surgem quando estamos prontos para recebê-las, o início de ciclos de abundância genuína, e a capacidade de materializar sonhos através de trabalho dedicado e visão clara. É o momento de plantar sementes em solo fértil, confiando no processo natural de crescimento e colheita.",
        "reversed": "Oportunidades perdidas por falta de preparação ou reconhecimento, planejamento deficiente que sabota potencial de sucesso, ganância que corrompe propósitos nobres, materialismo que desconecta de valores espirituais essenciais. Pode indicar recursos desperdiçados ou investimentos mal direcionados que impedem o verdadeiro crescimento.",
        "themes": ["manifestação", "oportunidade", "abundância", "propósito", "materialização"],
        "affirmation": "Eu reconheço e abraço oportunidades alinhadas com meu propósito maior.",
        "shadow_work": "Estou manifestando a partir do amor ou do medo de escassez?",
        "spiritual_message": "O universo está oferecendo uma nova oportunidade de crescimento material. Receba com gratidão."
    },

    {
        "name": "Dois de Ouros",
        "number": 2,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["equilíbrio dinâmico", "adaptabilidade consciente", "priorização sábia", "gestão harmoniosa", "flexibilidade responsável", "dança da vida"],
        "upright": "A arte graceful de equilibrar múltiplas responsabilidades e prioridades com flexibilidade consciente e sabedoria adaptativa. Representa a capacidade de navegar mudanças mantendo estabilidade essencial, a habilidade de priorizar com clareza em meio à complexidade, e a dança harmoniosa entre diferentes aspectos da vida. É sobre encontrar fluidez na estrutura e estabilidade no movimento.",
        "reversed": "Desequilíbrio que resulta em sobrecarga e esgotamento desnecessário, desorganização que cria caos ao invés de produtividade, dificuldade em estabelecer prioridades que gera dispersão de energia, rigidez que impede adaptação a mudanças necessárias. Pode sinalizar tentativas de controlar demais situações que requerem flexibilidade.",
        "themes": ["equilíbrio", "adaptabilidade", "priorização", "flexibilidade", "harmonia"],
        "affirmation": "Eu navego a complexidade da vida com equilíbrio, flexibilidade e sabedoria.",
        "shadow_work": "Onde estou perdendo equilíbrio por tentar controlar demais?",
        "spiritual_message": "A vida é uma dança dinâmica. Mantenha-se flexível e confiante no fluxo."
    },

    {
        "name": "Três de Ouros",
        "number": 3,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["colaboração sagrada", "maestria compartilhada", "construção coletiva", "aprendizado mútuo", "excelência técnica", "sinergia criativa"],
        "upright": "A força transformadora da colaboração genuína onde habilidades individuais se unem para criar algo maior que a soma das partes. Representa o desenvolvimento de maestria através de troca de conhecimentos, a construção de projetos duradouros baseados em expertise compartilhada, e o reconhecimento de que a verdadeira excelência surge da união de talentos diversos. É sobre criar legados através do trabalho conjunto e dedicado.",
        "reversed": "Trabalho desalinhado onde egos individuais sabotam objetivos coletivos, falta de colaboração que resulta em projetos inacabados ou de qualidade inferior, competição destrutiva que impede crescimento mútuo, má qualidade resultado da pressa ou falta de dedicação artesanal.",
        "themes": ["colaboração", "maestria", "construção", "aprendizado", "excelência"],
        "affirmation": "Eu contribuo com meus talentos únicos para criar algo maior e mais belo.",
        "shadow_work": "Estou competindo quando deveria estar colaborando?",
        "spiritual_message": "A maestria verdadeira floresce quando compartilhamos conhecimento com generosidade."
    },

    {
        "name": "Quatro de Ouros",
        "number": 4,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["segurança consciente", "conservação sábia", "estabilidade duradoura", "proteção necessária", "base sólida", "guardiania responsável"],
        "upright": "A necessidade sábia de estabelecer segurança e estabilidade como fundação para crescimento futuro. Representa a capacidade de conservar recursos de forma consciente, criar estruturas duradouras que protegem o que foi conquistado, e exercer controle responsável sobre recursos materiais. É sobre construir bases sólidas que permitam expansão segura e sustentável.",
        "reversed": "Ganância que corrompe a busca natural por segurança, materialismo excessivo que aprisiona o espírito em preocupações mundanas, avareza que impede fluxo natural de abundância, medo de perda que paralisa crescimento e impede generosidade necessária para verdadeira prosperidade.",
        "themes": ["segurança", "estabilidade", "conservação", "proteção", "controle"],
        "affirmation": "Eu cultivo segurança sem me apegar, protejo sem me isolar.",
        "shadow_work": "Onde o medo de perda está limitando meu crescimento e generosidade?",
        "spiritual_message": "Verdadeira segurança vem de confiar no fluxo natural da abundância."
    },

    {
        "name": "Cinco de Ouros",
        "number": 5,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["adversidade transformadora", "humildade necessária", "lição de escassez", "força interior", "renovação através da perda", "purificação material"],
        "upright": "O período desafiador de escassez que, embora doloroso, oferece oportunidades profundas de crescimento espiritual e redefinição de valores. Representa a capacidade de encontrar força interior quando recursos externos se esgotam, a descoberta de que verdadeira riqueza transcende bens materiais, e a oportunidade de reconstruir sobre fundações mais autênticas. É sobre transformar adversidade em sabedoria.",
        "reversed": "Recuperação gradual após período de dificuldade através de ajuda recebida ou esforço próprio, assistência chegando no momento certo, caridade que restaura dignidade, perdão que liberta de ciclos de escassez, superação de isolamento através de conexões humanas autênticas.",
        "themes": ["adversidade", "humildade", "renovação", "força interior", "transformação"],
        "affirmation": "Eu encontro força e sabedoria mesmo nos momentos de maior desafio.",
        "shadow_work": "Como a escassez está me ensinando sobre verdadeira abundância?",
        "spiritual_message": "Nas maiores dificuldades, descobrimos nossa riqueza interior mais profunda."
    },

    {
        "name": "Seis de Ouros",
        "number": 6,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["generosidade equilibrada", "reciprocidade sagrada", "justiça compassiva", "fluxo harmonioso", "abundância compartilhada", "caridade consciente"],
        "upright": "O fluxo harmonioso de dar e receber que mantém a abundância circulando de forma equilibrada e justa. Representa a capacidade de ser generoso sem se esgotar, receber ajuda sem perder dignidade, e participar conscientemente dos ciclos naturais de abundância. É sobre compreender que verdadeira riqueza se multiplica quando compartilhada com sabedoria e compaixão.",
        "reversed": "Desequilíbrio no dar e receber que cria dependência ou esgotamento, egoísmo que bloqueia fluxo natural de abundância, dívidas (materiais ou emocionais) que criam ciclos de escassez, mesquinhez que impede participação nos ciclos de prosperidade coletiva.",
        "themes": ["generosidade", "reciprocidade", "justiça", "fluxo", "compartilhamento"],
        "affirmation": "Eu participo conscientemente dos ciclos de abundância, dando e recebendo com equilíbrio.",
        "shadow_work": "Onde estou desequilibrando o fluxo natural do dar e receber?",
        "spiritual_message": "A abundância verdadeira flui quando compartilhamos com coração aberto e mãos generosas."
    },

    {
        "name": "Sete de Ouros",
        "number": 7,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["paciência frutífera", "investimento sábio", "colheita merecida", "perseverança recompensada", "visão de longo prazo", "crescimento sustentável"],
        "upright": "A sabedoria de investir tempo e energia com paciência, confiando no processo natural de crescimento e maturação. Representa a capacidade de perseverar mesmo quando resultados não são imediatamente visíveis, a compreensão de que verdadeiras conquistas requerem tempo e dedicação consistente, e a alegria de colher frutos de esforços sustentados. É sobre confiar no timing divino e na recompensa do trabalho consciente.",
        "reversed": "Impaciência que sabota processos naturais de crescimento, falta de visão de longo prazo que resulta em decisões precipitadas, recompensas limitadas devido à inconsistência ou falta de perseverança, frustração com timing que não corresponde às expectativas pessoais.",
        "themes": ["paciência", "investimento", "perseverança", "crescimento", "recompensa"],
        "affirmation": "Eu confio no processo natural de crescimento e colho no tempo certo.",
        "shadow_work": "Onde minha impaciência está sabotando meu crescimento natural?",
        "spiritual_message": "As sementes plantadas com amor e paciência sempre produzem frutos abundantes."
    },

    {
        "name": "Oito de Ouros",
        "number": 8,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["dedicação artesanal", "maestria em desenvolvimento", "aperfeiçoamento constante", "trabalho sagrado", "habilidade refinada", "excelência através da prática"],
        "upright": "O caminho nobre da maestria através de dedicação constante, aperfeiçoamento contínuo e amor pelo ofício. Representa a transformação do trabalho em arte através de atenção aos detalhes, a satisfação profunda que vem do desenvolvimento de habilidades autênticas, e a compreensão de que verdadeira excelência é fruto de prática consciente e dedicada. É sobre honrar o processo de aprendizado como sagrado.",
        "reversed": "Perfeccionismo que paralisa ao invés de aperfeiçoar, falta de ambição que resulta em estagnação de talentos, trabalho repetitivo sem crescimento ou propósito, pressa que compromete qualidade e satisfação pessoal com o processo criativo.",
        "themes": ["dedicação", "maestria", "aperfeiçoamento", "habilidade", "excelência"],
        "affirmation": "Eu honro meu trabalho como expressão sagrada de meus talentos únicos.",
        "shadow_work": "Estou buscando perfeição ou excelência? Qual é a diferença?",
        "spiritual_message": "Cada momento de prática consciente é um passo sagrado no caminho da maestria."
    },

    {
        "name": "Nove de Ouros",
        "number": 9,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["abundância merecida", "independência conquistada", "autossuficiência sábia", "luxo consciente", "conquista pessoal", "liberdade através da disciplina"],
        "upright": "A realização satisfatória de independência e abundância conquistadas através de esforço próprio, disciplina e sabedoria. Representa a capacidade de desfrutar dos frutos do trabalho sem culpa, a liberdade que vem da autossuficiência responsável, e o prazer refinado de apreciar beleza e qualidade na vida. É sobre celebrar conquistas pessoais mantendo gratidão e perspectiva.",
        "reversed": "Excesso que corrompe apreciação genuína por conquistas, dependência disfarçada que compromete verdadeira liberdade, superficialidade que substitui satisfação profunda por ostentação vazia, isolamento que resulta de privilegiar bens materiais sobre conexões humanas.",
        "themes": ["abundância", "independência", "autossuficiência", "conquista", "liberdade"],
        "affirmation": "Eu celebro minhas conquistas com gratidão e as compartilho com generosidade.",
        "shadow_work": "Minha abundância está me conectando ou isolando dos outros?",
        "spiritual_message": "Verdadeira riqueza é poder escolher como usar seus recursos para o bem maior."
    },

    {
        "name": "Dez de Ouros",
        "number": 10,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["legado duradouro", "riqueza transgeracional", "estabilidade familiar", "herança consciente", "prosperidade coletiva", "abundância compartilhada"],
        "upright": "A culminação de esforços em riqueza e estabilidade que beneficia não apenas o indivíduo, mas gerações futuras. Representa a capacidade de criar legados duradouros baseados em valores sólidos, a satisfação de contribuir para prosperidade coletiva, e a responsabilidade sábia de administrar recursos que transcendem necessidades pessoais. É sobre construir abundância que honra o passado e nutre o futuro.",
        "reversed": "Perda financeira que abala estruturas familiares, instabilidade que compromete segurança coletiva, conflitos familiares relacionados a questões materiais, herança mal administrada que se torna fonte de discórdia ao invés de bênção.",
        "themes": ["legado", "família", "estabilidade", "herança", "prosperidade coletiva"],
        "affirmation": "Eu construo abundância que honra meus ancestrais e abençoa as futuras gerações.",
        "shadow_work": "Que tipo de legado material e espiritual estou criando?",
        "spiritual_message": "Verdadeira riqueza se mede pela capacidade de nutrir e sustentar aqueles que amamos."
    },

    {
        "name": "Pajem de Ouros",
        "number": 11,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["curiosidade prática", "aprendizado terreno", "potencial em germinação", "estudioso dedicado", "ambição saudável", "oportunidade de crescimento"],
        "upright": "A energia jovem e entusiástica de quem está começando a explorar o mundo material com curiosidade genuína e desejo de aprender. Representa oportunidades de crescimento através de educação prática, a disposição de começar do básico para construir fundamentos sólidos, e o potencial ainda não totalmente desenvolvido que busca manifestação consciente. É sobre abraçar o papel de eterno estudante da vida.",
        "reversed": "Procrastinação que impede aproveitamento de oportunidades de aprendizado, falta de compromisso com processo de crescimento necessário, sonhos irrealistas que não se conectam com ação prática, impaciência com etapas necessárias de desenvolvimento.",
        "themes": ["aprendizado", "potencial", "curiosidade", "crescimento", "oportunidade"],
        "affirmation": "Eu abraço cada oportunidade de aprender como um presente precioso.",
        "shadow_work": "Onde minha pressa está impedindo meu aprendizado genuíno?",
        "spiritual_message": "Cada momento de aprendizado consciente planta sementes para abundância futura."
    },

    {
        "name": "Cavaleiro de Ouros",
        "number": 12,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["determinação constante", "produtividade consciente", "responsabilidade assumida", "trabalho sagrado", "progresso sustentável", "dedicação exemplar"],
        "upright": "A energia confiável e determinada de quem compreende que verdadeiras conquistas são resultado de esforço consistente e responsabilidade assumida. Representa a capacidade de manter produtividade sem perder qualidade, a sabedoria de criar rotinas que sustentam crescimento, e a compreensão de que pequenos passos consistentes levam a grandes realizações. É sobre honrar o trabalho como expressão de propósito.",
        "reversed": "Tédio resultado de falta de propósito mais profundo no trabalho, estagnação que surge de resistência a mudanças necessárias, perfeccionismo que paralisa ao invés de aperfeiçoar, preguiça que sabota potencial de crescimento e realização.",
        "themes": ["determinação", "produtividade", "responsabilidade", "consistência", "progresso"],
        "affirmation": "Eu encontro propósito e satisfação em cada tarefa que abraço conscientemente.",
        "shadow_work": "Onde estou trabalhando por hábito ao invés de propósito?",
        "spiritual_message": "O trabalho consciente e dedicado é uma forma de oração em ação."
    },

    {
        "name": "Rainha de Ouros",
        "number": 13,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["abundância nutritiva", "praticidade amorosa", "cuidado maternal", "segurança criada", "generosidade sábia", "lar como santuário"],
        "upright": "A energia maternal e nutritiva que cria abundância através de cuidado consciente, praticidade amorosa e generosidade sábia. Representa a capacidade de transformar espaços em santuários de amor e segurança, nutrir crescimento através de apoio prático e emocional, e criar prosperidade que beneficia toda a comunidade. É sobre ser fonte de estabilidade e abundância para si mesma e outros.",
        "reversed": "Insegurança financeira que gera ansiedade e controle excessivo, desordem que reflete desequilíbrio interior, negligência com responsabilidades práticas que afeta bem-estar próprio e de outros, ciúme que surge de sentimentos de inadequação material.",
        "themes": ["abundância", "cuidado", "praticidade", "generosidade", "segurança"],
        "affirmation": "Eu crio abundância através do amor, cuidado e sabedoria prática.",
        "shadow_work": "Como posso nutrir outros sem me esgotar ou criar dependência?",
        "spiritual_message": "Verdadeira riqueza flui através de corações que cuidam com amor incondicional."
    },

    {
        "name": "Rei de Ouros",
        "number": 14,
        "type": "Arcano Menor",
        "suit": "Ouros",
        "element": "Terra",
        "keywords": ["liderança abundante", "sucesso consciente", "riqueza responsável", "autoridade sábia", "prosperidade compartilhada", "poder através do serviço"],
        "upright": "A culminação da maestria material expressa através de liderança sábia, abundância responsável e capacidade de criar prosperidade que beneficia todos. Representa o poder de transformar recursos em oportunidades para crescimento coletivo, a autoridade que vem de competência genuína e integridade, e a compreensão de que verdadeiro sucesso inclui responsabilidade social. É sobre usar abundância para servir propósito maior.",
        "reversed": "Ganância que corrompe propósito nobre de liderança, materialismo que desconecta de valores humanos essenciais, teimosia que impede adaptação necessária, corrupção que usa poder para benefício próprio ao invés de bem coletivo.",
        "themes": ["liderança", "sucesso", "responsabilidade", "abundância", "serviço"],
        "affirmation": "Eu uso minha autoridade e recursos para criar prosperidade que beneficia todos.",
        "shadow_work": "Como posso usar meu poder e recursos para servir algo maior que meu ego?",
        "spiritual_message": "Verdadeira realeza se mede pela capacidade de elevar e prosperar toda a comunidade."
    }
]

for card in DECK:
    card['image_file'] = card['name'].lower().replace(' ', '_').replace('á', 'a').replace('ã', 'a').replace('ç', 'c') + ".png"

# <<< DICIONÁRIO ATUALIZADO COM TODAS AS EXPLICAÇÕES >>>
SPREAD_EXPLANATIONS = {
    "Conselho do Dia (1 carta)": {
        "title": "🃏 Tiragem de Uma Carta", "image": "images/spread_1_card.png",
        "purpose": "Obter uma resposta direta, um conselho rápido ou uma visão geral do momento presente.",
        "how_it_works": "Sorteia-se apenas uma carta, que é interpretada sozinha para fornecer uma mensagem clara e focada.",
        "ideal_for": ["Reflexão diária.", "Respostas para perguntas simples.", "Uma dose rápida de intuição ou inspiração."]
    },
    "Passado, Presente e Futuro (3 cartas)": {
        "title": "🕰️ Tiragem de Três Cartas", "image": "images/spread_3_cards.png",
        "purpose": "Analisar a evolução de uma situação através de uma linha do tempo clara.",
        "how_it_works": "As três cartas representam o Passado (as bases da situação), o Presente (o desafio ou estado atual) e o Futuro (o resultado provável).",
        "ideal_for": ["Analisar o progresso de relacionamentos ou projetos.", "Obter um panorama com começo, meio e fim.", "Entender como eventos passados influenciam o agora."]
    },
    "Tiragem Temática (3 cartas)": {
        "title": "✨ Tiragem Temática", "image": "images/spread_theme.png",
        "purpose": "Explorar uma área específica da vida (como amor ou carreira) com mais profundidade.",
        "how_it_works": "As três cartas têm significados contextuais: Contexto Atual (onde você está), O Desafio (o que superar) e O Conselho (a ação recomendada).",
        "ideal_for": ["Leituras direcionadas e focadas.", "Quando você tem uma área da vida que precisa de clareza.", "Receber orientação prática sobre um problema."]
    },
    "Cruz Celta (10 cartas)": {
        "title": "🧭 Cruz Celta", "image": "images/spread_celtic_cross.png",
        "purpose": "Fazer uma análise profunda, estruturada e estratégica de uma questão.",
        "how_it_works": "Uma tiragem completa usando 10 cartas com significados interconectados, cobrindo a situação, desafios, passado, futuro, influências e o resultado provável.",
        "ideal_for": ["Questões complexas ou decisões difíceis.", "Leituras profundas com contexto e nuances.", "Sessões de tarô detalhadas."]
    },
    "Caminhos da Decisão (4 cartas)": {
        "title": "🔄 Tiragem de Caminhos", "image": "images/spread_choices.png",
        "purpose": "Avaliar os resultados prováveis de duas escolhas diferentes.",
        "how_it_works": "Duas cartas são sorteadas para cada caminho. O 'Caminho A' mostra a situação e resultado de uma escolha, e o 'Caminho B' faz o mesmo para a outra opção.",
        "ideal_for": ["Escolher entre dois empregos, relacionamentos ou decisões de vida.", "Avaliar consequências prováveis antes de agir.", "Quando se sentir em uma encruzilhada."]
    },
    "Conselho Espiritual (3 cartas)": {
        "title": "💡 Tiragem de Conselho Espiritual", "image": "images/spread_spiritual.png",
        "purpose": "Conectar-se com orientações mais profundas, intuitivas e espirituais.",
        "how_it_works": "Três cartas com foco em: 1. Qual lição aprender, 2. Qual energia integrar, 3. Qual bloqueio liberar.",
        "ideal_for": ["Meditação e reflexão interna.", "Desenvolvimento pessoal e espiritual.", "Quando a pergunta não é sobre 'o que fazer', mas 'como ser'."]
    },
    "Jornada do Autoconhecimento (5 cartas)": {
        "title": "🧘‍♂️ Tiragem de Autoconhecimento", "image": "images/spread_self_knowledge.png",
        "purpose": "Entender aspectos internos da própria personalidade, padrões emocionais ou conflitos internos.",
        "how_it_works": "Cinco cartas representando arquétipos e forças internas: 1. Eu exterior, 2. Eu interior, 3. Meu desafio, 4. Meu potencial, 5. Meu equilíbrio.",
        "ideal_for": ["Exploração psicológica.", "Entender padrões de comportamento.", "Trabalho com a sombra e integração pessoal."]
    }
}


# <<< NOVO DICIONÁRIO COM AS EXPLICAÇÕES DOS ESTILOS >>>
STYLE_EXPLANATIONS = {
    "Mística e Inspiradora": "Conecta-se ao simbolismo profundo do tarô, trazendo interpretações envolventes e carregadas de energia espiritual. Enfatiza o mistério, a magia e a conexão com o invisível. Ideal para quem busca uma experiência rica em atmosfera esotérica e deseja sentir a leitura como um ritual sagrado.",
    "Prática e Direta": "Foca em mensagens objetivas, claras e aplicáveis ao dia a dia. A interpretação é uma ferramenta de orientação pragmática, priorizando conselhos concretos e ações imediatas. Indicado para quem quer clareza rápida e direcionamento prático para resolver questões ou tomar decisões.",
    "Terapêutica e Reflexiva": "Explora as cartas como espelhos da mente e das emoções, incentivando a introspecção e a compreensão dos padrões de comportamento. Atua como uma conversa de aconselhamento, promovendo autoconhecimento e acolhimento. Perfeito para quem busca compreender sentimentos e identificar bloqueios.",
    "Poética e Introspectiva": "Transforma a leitura em uma narrativa sensível e literária, com ricas metáforas e imagens. Convida à contemplação e à conexão com a beleza das palavras, abrindo espaço para um significado subjetivo e artístico. A melhor escolha para quem aprecia leituras que tocam o coração e despertam a imaginação."
}


# --- FUNÇÕES DA APLICAÇÃO ---

def get_image_filename(card_name):
    return card_name.lower().replace(' ', '_').replace('á', 'a').replace('ã', 'a').replace('ç', 'c') + ".png"

def normalize_text(text):
    return unicodedata.normalize('NFKD', str(text)).encode('latin-1', 'ignore').decode('latin-1')


def draw_cards(num_cards):
    drawn_cards_info = []
    if num_cards > len(DECK):
        st.error("Erro: tentando sortear mais cartas do que existem no baralho.")
        return []
    deck_copy = DECK[:]
    drawn_cards_sample = random.sample(deck_copy, num_cards)
    for card in drawn_cards_sample:
        is_reversed = random.choice([True, False])
        drawn_cards_info.append({"card": card, "is_reversed": is_reversed})
    return drawn_cards_info

def get_interpretation(cards_drawn, spread_positions, question, style, api_key):
    openai.api_key = api_key

    # 1. LÓGICA DE TAMANHO: INSTRUÇÃO vs. REDE DE SEGURANÇA
    num_cards = len(cards_drawn)
    word_count_guideline = ""   # A instrução para a IA
    max_response_tokens = 2000  # Uma rede de segurança generosa por padrão

    # Define a INSTRUÇÃO de tamanho para o prompt
    if num_cards == 1:
        word_count_guideline = "entre 150 e 250 palavras."
        max_response_tokens = 500  # Rede de segurança para até ~375 palavras
    elif num_cards <= 3:
        word_count_guideline = "entre 400 e 600 palavras."
        max_response_tokens = 1000 # Rede de segurança para até ~750 palavras
    elif num_cards <= 5:
        word_count_guideline = "entre 700 e 800 palavras."
        max_response_tokens = 1300 # Rede de segurança para até ~975 palavras
    else:  # Para Cruz Celta (10 cartas)
        word_count_guideline = "entre 900 e 1.200 palavras."
        max_response_tokens = 2000 # Rede de segurança para até ~1500 palavras

    # 2. PREPARAÇÃO DOS DETALHES DAS CARTAS
    card_details = ""
    for i, item in enumerate(cards_drawn):
        card = item["card"]
        orientation = "Invertida" if item["is_reversed"] else "Reta"
        meaning = card["reversed"] if item["is_reversed"] else card["upright"]
        card_details += f"### Carta {i+1}: {spread_positions[i]} - {card['name']} ({orientation})\n- Significado Base: {meaning}\n\n"

    effective_question = question if question else 'Uma orientação geral para o meu momento presente.'

    # 3. PROMPT APRIMORADO COM INSTRUÇÃO DE CONCLUSÃO
    prompt = f"""
    ### PERSONA
    Você é o 'Oráculo do Tarô Místico', um guardião ancestral dos segredos cósmicos. Sua essência transcende o tempo. Você não apenas lê cartas - você desvenda os fios do destino, traduz sussurros do universo e ilumina caminhos ocultos.

    ### MISSÃO SAGRADA (INSTRUÇÕES)
    Como ponte entre os mundos, você deve tecer uma revelação que toque a mente e a alma do consulente. Siga estes passos sagrados:

    1.  **TAMANHO E CONCLUSÃO:** Sua revelação deve ter **{word_count_guideline}** É **essencial** que você conclua sua resposta de forma natural e completa dentro deste limite de palavras, sem cortes abruptos.
    2.  **ESTILO:** Aderindo estritamente ao estilo de revelação **'{style}'**.
    3.  **FORMATAÇÃO:** Use Markdown. Destaque conceitos chave com **negrito** e crie seções claras com títulos, como `### A Tapeçaria Cósmica` ou `### Conselho do Oráculo`.
    4.  **ACOLHIMENTO:** Comece com palavras de acolhimento, reconhecendo a coragem do consulente.
    5.  **NARRATIVA CENTRAL:** Desvende a tapeçaria cósmica que as cartas revelam. Conecte cada símbolo em uma narrativa fluida. Não descreva as cartas individualmente; REVELE os padrões e as mensagens que dançam entre elas.
    6.  **SABEDORIA PRÁTICA:** Traduza os arquétipos em conselhos práticos e específicos.
    7.  **SÍNTESE E BÊNÇÃO:** Encerre com uma síntese poderosa e uma bênção transformadora que sirva como um catalisador para crescimento.

    ### DADOS DA CONSULTA
    - **A Alma Busca Orientação Sobre:** "{effective_question}"
    - **As Cartas do Destino se Manifestaram Assim:**
    {card_details}
    ---
    Agora, em Português do Brasil, com a eloquência de um poeta místico e a precisão de um sábio ancestral, revele a sabedoria das cartas.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Você é uma IA especializada em interpretações de Tarô, assumindo a persona de um oráculo místico que sempre conclui suas respostas de forma coesa e completa."},
                      {"role": "user", "content": prompt}],
            temperature=0.75,
            max_tokens=max_response_tokens # Usando a REDE DE SEGURANÇA generosa
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ocorreu um erro ao contatar o oráculo digital: {e}"

def display_card(card_item, position_text, container):
    """Exibe uma única carta usando HTML puro, incluindo as palavras-chave."""
    with container:
        card = card_item["card"]
        caption = f"{card['name']}{' (Invertida)' if card_item['is_reversed'] else ''}"
        image_local_path = os.path.join("images", card["image_file"])

        base64_img = get_img_as_base64(image_local_path)

        if base64_img:
            img_src = f"data:image/png;base64,{base64_img}"

            # --- CORREÇÃO: ADICIONA AS PALAVRAS-CHAVE ---
            keywords_str = ", ".join(card.get("keywords", []))

            st.html(f"""
                <div class="card-reveal">
                    <figure style="margin:0; text-align:center;">
                        <img src="{img_src}" alt="{caption}"
                             style="width:100%; height:auto; border-radius:15px;
                                    border:3px solid var(--primary-gold);
                                    box-shadow:0 10px 30px rgba(0,0,0,.5);" />
                        <figcaption style="margin-top:.5rem; color:var(--secondary-gold); font-family:'Cinzel',serif; font-weight:600; font-size:1.1rem; text-shadow: 1px 1px 3px #000;">
                            {caption}
                        </figcaption>
                    </figure>
                    <!-- Adiciona o parágrafo com as palavras-chave -->
                    <p style="text-align:center; font-style:italic; font-size:0.9rem; color:var(--text-muted); margin-top:0.5rem; text-shadow:none;">
                        {keywords_str}
                    </p>
                </div>
            """)
        else:
            st.warning(f"Imagem {card['image_file']} não encontrada.")
            st.markdown(f"**{caption}**")

for card in DECK:
    card['image_file'] = get_image_filename(card['name'])


# ==============================================================================
# 4. ÁREA PRINCIPAL COM FLUXO GUIADO (ESTRUTURA CORRIGIDA)
# ==============================================================================

def page_welcome():
    # --- Seção Principal ---
    with st.container(border=True):
        st.header("✨ Adentre o Santuário")
        st.markdown(
            """
            *Respire fundo, viajante. Você chegou a um lugar onde os véus entre os mundos são tênues.*
            *Aqui, os arquétipos do Tarô não preveem um futuro fixo, mas sussurram os segredos da sua alma, revelando os caminhos que se abrem à sua frente.*
            """
        )
        st.text_input(
            "Para começar, diga ao Oráculo o nome pelo qual ele deve se dirigir a você:",
            key="user_name",
            placeholder="Digite seu nome ou apelido..."
        )

    if st.button("🌟 Iniciar Jornada Mística", use_container_width=True):
        user_name_input = st.session_state.get("user_name", "").strip()
        if user_name_input:
            st.session_state.selected = {
                "user_name": user_name_input,
                **st.session_state.get("selected", {})
            }
            st.session_state.tarot_step = 'configure'
            st.rerun()
        else:
            st.warning("O Oráculo aguarda seu nome para criar a conexão.")

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # --- link para Voltar ao Santuário Principal ---
    st.page_link("🔮_Santuario_Principal.py", label="⬅ Voltar ao Santuário Principal", icon="↩️")

    # --- link para a página de políticas ---
    st.markdown("<p style='text-align: center; margin-top: 2rem;'>Ao prosseguir, você concorda com nossos <a href='/Politicas' target='_self'>Termos e Políticas</a>.</p>", unsafe_allow_html=True)


def page_configure():
    # Lê o nome do snapshot, que é a fonte confiável
    user_name = st.session_state.selected.get("user_name", "Viajante")

    with st.container(border=True):
        st.header(f"Passo 1: A Intenção, {user_name}")
        st.markdown("Escolha as ferramentas que guiarão sua consulta. Cada escolha molda a energia da sua leitura.")
        mystical_divider(margin="1rem 0")

        spread_options = {
            "Conselho do Dia (1 carta)": 1, "Passado, Presente e Futuro (3 cartas)": 3, "Tiragem Temática (3 cartas)": 3,
            "Cruz Celta (10 cartas)": 10, "Caminhos da Decisão (4 cartas)": 4, "Conselho Espiritual (3 cartas)": 3,
            "Jornada do Autoconhecimento (5 cartas)": 5
        }
        st.selectbox("🔮 Primeiro, escolha o tipo de tiragem:", list(spread_options.keys()), key="spread_choice")

        # --- CÓDIGO RESTAURADO: EXPLICAÇÃO DA TIRAGEM COM st.expander ---
        # Pega a escolha atual para exibir a explicação correspondente.
        spread_choice = st.session_state.get("spread_choice")
        explanation = SPREAD_EXPLANATIONS.get(spread_choice)
        if explanation:
            with st.expander("Saiba mais sobre esta tiragem"):
                st.subheader(explanation['title'])
                st.markdown(f"**Propósito:** {explanation['purpose']}")
                st.markdown(f"**Como Funciona:** {explanation['how_it_works']}")
        # -----------------------------------------------------------------

        mystical_divider(margin="1rem 0")
        st.text_area("❓ Em seguida, concentre-se em seu foco. Faça uma pergunta (opcional):", placeholder="Ex: 'Qual caminho profissional devo seguir?'", key="question")
        mystical_divider(margin="1rem 0")
        st.selectbox("✨ Por fim, escolha o tom da voz do Oráculo:", list(STYLE_EXPLANATIONS.keys()), key="reading_style")

        # --- CÓDIGO RESTAURADO: EXPLICAÇÃO DO ESTILO COM st.expander ---
        reading_style = st.session_state.get("reading_style")
        if reading_style in STYLE_EXPLANATIONS:
            with st.expander("Clique para entender os diferentes tons do Oráculo"):
                st.markdown(f"#### {reading_style}")
                st.write(STYLE_EXPLANATIONS[reading_style])
            # --------------------------------------------------------------

    if st.button("Confirmar Intenção e Preparar o Oráculo ➡", use_container_width=True, key="to_payment_button"):
        # A lógica de snapshot robusta que já funciona
        current_snapshot = st.session_state.get("selected", {})
        st.session_state.selected = {
            **current_snapshot,
            "spread_choice": st.session_state.get("spread_choice"),
            "reading_style": st.session_state.get("reading_style"),
            "question": (st.session_state.get("question") or "").strip(),
        }
        st.session_state.tarot_step = 'payment'
        st.rerun()

    if st.button("⬅️ Voltar e Corrigir Nome", use_container_width=True, key="back_to_welcome_button"):
        st.session_state.tarot_step = 'welcome'
        st.rerun()


def page_payment():
    # Verificação defensiva no início da função
    if stripe is None:
        st.error("ERRO CRÍTICO: A biblioteca de pagamento (Stripe) não está disponível. Verifique o arquivo requirements.txt.")
        st.stop()

    sel = st.session_state.get("selected", {})
    user_name = sel.get("user_name", "Viajante")

    with st.container(border=True):
        st.header(f"Passo 2: O Portal de Pagamento")
        st.markdown(f"Sua intenção foi recebida, **{user_name}**. As cartas foram consagradas à sua energia. A revelação aguarda do outro lado do portal.")
        mystical_divider()

        st.subheader("Resumo da sua Consulta:")
        st.markdown(f'**- Tipo de Tiragem:** `{sel.get("spread_choice", "—")}`')
        st.markdown(f'**- Estilo de Leitura:** `{sel.get("reading_style", "—")}`')
        if sel.get("question"):
            st.markdown(f'**- Foco:** `{sel["question"]}`')

        st.markdown(f'**- Valor da Consulta:** R$ 5,90')

        mystical_divider()

    try:
        host_url = app_base_url
        spread_choice = sel.get("spread_choice", "Consulta Padrão")
        user_name_for_stripe = sel.get("user_name", "Viajante")

        metadata = {
            "spread_choice": spread_choice,
            "reading_style": sel.get("reading_style", ""),
            "question": sel.get("question", ""),
            "user_name": user_name_for_stripe,
        }

        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price': stripe_price_id, # Usa a variável de ambiente
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{host_url}/Taro_Mistico?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{host_url}/Taro_Mistico",
            client_reference_id=str(uuid4()),
            metadata=metadata,
        )

        # --- A CORREÇÃO FINAL FINALÍSSIMA ---
        # Trocamos para target="_blank" para forçar a abertura em uma nova guia,
        # contornando a interceptação de eventos do Streamlit.
        payment_link_html = f"""
            <a href="{checkout_session.url}" target="_blank" class="payment-button-container" style="text-decoration: none;">
                Pagar e Cruzar o Portal para a Revelação
            </a>
        """
        st.markdown(payment_link_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Ocorreu um erro ao preparar o portal de pagamento: {e}")
        st.warning("Por favor, tente voltar e refazer sua configuração.")

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("⬅ Voltar e Alterar Intenção", use_container_width=True, key="back_to_configure_button"):
        st.session_state.tarot_step = 'configure'
        st.rerun()


def page_result():

    # <<< VERIFICAÇÃO DE SEGURANÇA >>>
    if not st.session_state.get('payment_verified'):
        st.error("Acesso não autorizado.")
        st.warning("Por favor, inicie uma nova consulta e complete o pagamento para ver sua revelação.")
        if st.button("Voltar ao Início"):
            reset_app_state('tarot')
        st.stop() # Interrompe a execução da página
    # <<< FIM DA VERIFICAÇÃO >>>

    # A lógica de verificação do Stripe já restaurou o estado.
    # Apenas lemos o estado confiável para exibir a página.
    user_name = st.session_state.get("user_name", "Viajante")

    if 'final_interpretation' not in st.session_state:
        sel = st.session_state.get("selected", {})
        spread_choice = sel.get("spread_choice", "Conselho do Dia (1 carta)")
        reading_style = sel.get("reading_style", "Mística e Inspiradora")
        question = sel.get("question", "")

        # Sincroniza o resto do estado da sessão para a primeira execução
        st.session_state.spread_choice = spread_choice
        st.session_state.reading_style = reading_style
        st.session_state.question = question

        with st.spinner("O oráculo está consultando as estrelas e tecendo sua resposta... ✨"):
            api_key_secreta = openai_api_key

            spread_options = {"Conselho do Dia (1 carta)": 1, "Passado, Presente e Futuro (3 cartas)": 3, "Tiragem Temática (3 cartas)": 3, "Cruz Celta (10 cartas)": 10, "Caminhos da Decisão (4 cartas)": 4, "Conselho Espiritual (3 cartas)": 3, "Jornada do Autoconhecimento (5 cartas)": 5}
            num_cards = spread_options[spread_choice]
            spread_positions = []
            if spread_choice == "Conselho do Dia (1 carta)": spread_positions = ["Seu Conselho"]
            elif spread_choice == "Passado, Presente e Futuro (3 cartas)": spread_positions = ["O Passado", "O Presente", "O Futuro"]
            elif spread_choice == "Tiragem Temática (3 cartas)": spread_positions = ["Contexto Atual", "O Desafio", "O Conselho"]
            elif spread_choice == "Cruz Celta (10 cartas)": spread_positions = ["1. Situação Atual", "2. Obstáculo", "3. Base", "4. Passado", "5. Objetivo", "6. Futuro", "7. Atitude", "8. Ambiente", "9. Esperanças/Medos", "10. Resultado"]
            elif spread_choice == "Caminhos da Decisão (4 cartas)": spread_positions = ["Caminho A: Situação", "Caminho A: Resultado", "Caminho B: Situação", "Caminho B: Resultado"]
            elif spread_choice == "Conselho Espiritual (3 cartas)": spread_positions = ["Lição a Aprender", "Energia a Integrar", "Bloqueio a Liberar"]
            elif spread_choice == "Jornada do Autoconhecimento (5 cartas)": spread_positions = ["Eu Exterior", "Eu Interior", "Meu Desafio", "Meu Potencial", "Equilíbrio"]
            st.session_state.spread_positions = spread_positions
            drawn_cards = draw_cards(num_cards)
            st.session_state.drawn_cards = drawn_cards
            st.session_state.final_interpretation = get_interpretation(drawn_cards, spread_positions, question, reading_style, api_key=api_key_secreta)

    with st.container(border=True):
        st.header(f"Sua Revelação Sagrada, {user_name}")
        st.subheader(f"Leitura: {st.session_state.spread_choice}")
        drawn_cards = st.session_state.drawn_cards
        spread_positions = st.session_state.spread_positions
        num_cards = len(drawn_cards)
        mystical_divider()
        if st.session_state.spread_choice == "Cruz Celta (10 cartas)":
            st.markdown("##### O Coração da Questão"); cols_1_2 = st.columns(2); display_card(drawn_cards[0], spread_positions[0], cols_1_2[0]); display_card(drawn_cards[1], spread_positions[1], cols_1_2[1])
            mystical_divider()
            st.markdown("##### As Fundações"); cols_3_4 = st.columns(2); display_card(drawn_cards[2], spread_positions[2], cols_3_4[0]); display_card(drawn_cards[3], spread_positions[3], cols_3_4[1])
            mystical_divider()
            st.markdown("##### O Potencial e o Futuro"); cols_5_6 = st.columns(2); display_card(drawn_cards[4], spread_positions[4], cols_5_6[0]); display_card(drawn_cards[5], spread_positions[5], cols_5_6[1])
            mystical_divider()
            st.markdown("##### Influências e Resultado Final"); cols_7_8 = st.columns(2); display_card(drawn_cards[6], spread_positions[6], cols_7_8[0]); display_card(drawn_cards[7], spread_positions[7], cols_7_8[1])
            cols_9_10 = st.columns(2); display_card(drawn_cards[8], spread_positions[8], cols_9_10[0]); display_card(drawn_cards[9], spread_positions[9], cols_9_10[1])
        elif st.session_state.spread_choice == "Caminhos da Decisão (4 cartas)":
            col_a, col_b = st.columns(2, gap="large")
            with col_a: st.markdown("<p class='path-title'>Caminho A</p>", unsafe_allow_html=True); display_card(drawn_cards[0], spread_positions[0], col_a); display_card(drawn_cards[1], spread_positions[1], col_a)
            with col_b: st.markdown("<p class='path-title'>Caminho B</p>", unsafe_allow_html=True); display_card(drawn_cards[2], spread_positions[2], col_b); display_card(drawn_cards[3], spread_positions[3], col_b)
        else:
            for i in range(0, num_cards, 2):
                row_cards = drawn_cards[i:i + 2]; row_positions = spread_positions[i:i + 2]; num_cards_in_row = len(row_cards)
                if num_cards_in_row == 1:
                    _, card_col, _ = st.columns([1, 2, 1]); display_card(row_cards[0], row_positions[0], card_col)
                else:
                    cols = st.columns(num_cards_in_row)
                    for j, item in enumerate(row_cards):
                        display_card(item, row_positions[j], cols[j])


    with st.container(border=True):
        mystical_divider()
        st.subheader("A Interpretação do Oráculo:")
        st.markdown(st.session_state.final_interpretation)

    with st.container(border=True):
        mystical_divider()

        # Pega o snapshot, que é a fonte de verdade
        sel = st.session_state.get("selected", {})
        user_name = sel.get("user_name", "Viajante")

        # Passa o snapshot 'sel' para a função do PDF
        pdf_byte_array = create_reading_pdf(
            sel,
            st.session_state.final_interpretation,
            st.session_state.drawn_cards,
            st.session_state.spread_positions
        )
        pdf_data_as_bytes = bytes(pdf_byte_array)

        st.download_button(
            label="📥 Baixar seu Pergaminho em PDF",
            data=pdf_data_as_bytes,
            file_name=f"leitura_taro_mistico_{normalize_text(user_name)}.pdf",
            mime="application/pdf",
            width='stretch'
        )

        st.button(
            "Iniciar uma Nova Jornada",
            on_click=reset_app_state,
            args=('tarot',),
            use_container_width=True
        )

# --- ROTEADOR PRINCIPAL ---
st.html("""
<div class="header-container">
    <h1 class="main-title">Tarô Místico</h1>
    <!-- A tag <p> agora não tem mais estilo inline, ele será aplicado pelo CSS global -->
    <p>Um portal para o autoconhecimento através dos arquétipos universais</p>
    <div style="text-align: center; margin: 1rem 0;">
        <div style="font-size: 1.5rem; color: #d4af37; opacity: 0.8; animation: pulse 2s ease-in-out infinite alternate;">
            ⟡ ◦ ❋ ◦ ⟡
        </div>
    </div>
</div>
""")


if "tarot_step" not in st.session_state:
    st.session_state.tarot_step = "welcome"

step = st.session_state.get('tarot_step', 'welcome')

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
