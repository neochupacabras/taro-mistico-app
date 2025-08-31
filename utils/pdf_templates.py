# utils/pdf_templates.py

import os
import re
import unicodedata
from fpdf import FPDF, XPos, YPos
# O import do strip_emojis vem de helpers.py
from .helpers import strip_emojis, get_img_as_base64 # Adicionado para corrigir dependência implícita

class MysticalPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.GOLD_COLOR = (212, 175, 55)
        self.PURPLE_COLOR = (46, 26, 71)
        self.TEXT_COLOR = (50, 50, 50)
        self.PARCHMENT_COLOR = (244, 228, 166)

    def header(self):
        self.set_fill_color(*self.PARCHMENT_COLOR)
        self.rect(0, 0, self.w, self.h, 'F')

    def footer(self):
        self.set_y(-15)
        self.set_font('CormorantGaramond', 'I', 8)
        self.set_text_color(*self.TEXT_COLOR)
        self.cell(0, 10, f'Página {self.page_no()}', new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
        self.cell(0, 10, 'Gerado pelo Oráculo do Tarô Místico', new_x=XPos.RIGHT, new_y=YPos.TOP, align='R')

    def mystical_title(self, text):
        if self.page_no() == 0:
            self.add_page()
        self.set_font('Cinzel', 'B', 24)
        self.set_text_color(*self.GOLD_COLOR)
        self.set_fill_color(*self.PURPLE_COLOR)
        self.cell(0, 15, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C', fill=True)
        self.ln(10)

    def chapter_title(self, text):
        self.set_font('Cinzel', 'B', 16)
        self.set_text_color(*self.PURPLE_COLOR)
        self.cell(0, 10, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(2)

    def chapter_body(self, text):
        self.set_font('CormorantGaramond', '', 12)
        self.set_text_color(*self.TEXT_COLOR)
        self.multi_cell(0, 7, text)
        self.ln(5)

    def sub_heading(self, text):
        self.set_font('Cinzel', 'B', 14)
        self.set_text_color(*self.PURPLE_COLOR)
        self.cell(0, 8, text.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(2)

    def write_markdown_body(self, text):
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('### '):
                self.sub_heading(line.replace('### ', ''))
            elif not line:
                self.ln(4)
            else:
                parts = line.split('**')
                self.set_font('CormorantGaramond', '', 12)
                self.set_text_color(*self.TEXT_COLOR)
                for i, part in enumerate(parts):
                    if i % 2 == 1:
                        self.set_font('', 'B')
                    else:
                        self.set_font('', '')
                    self.write(7, part)
                self.ln()
        self.ln(5)

    def mystical_divider(self):
        self.set_draw_color(*self.GOLD_COLOR)
        self.set_line_width(0.5)
        x = self.get_x()
        w = self.w - self.l_margin - self.r_margin
        self.line(x, self.get_y(), x + w, self.get_y())
        self.ln(8)

    def draw_card_details(self, card_item, position):
        card = card_item['card']
        card_name = card['name']
        orientation = "(Invertida)" if card_item['is_reversed'] else ""
        image_path = os.path.join("images", get_image_filename(card['name']))
        y_start = self.get_y()
        if os.path.exists(image_path):
            self.image(image_path, x=self.l_margin, y=y_start, w=40)
        text_x_pos = self.l_margin + 45
        self.set_xy(text_x_pos, y_start)
        self.set_font('CormorantGaramond', 'B', 14)
        self.set_text_color(*self.PURPLE_COLOR)
        self.cell(0, 7, position, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(text_x_pos)
        self.set_font('Cinzel', 'B', 12)
        self.set_text_color(*self.TEXT_COLOR)
        self.cell(0, 7, f"{card_name} {orientation}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(text_x_pos)
        self.set_font('CormorantGaramond', 'I', 10)
        keywords_str = ", ".join(card.get("keywords", []))
        self.multi_cell(self.w - self.l_margin - self.r_margin - 45, 5, keywords_str)
        y_after_image = y_start + 60
        y_after_text = self.get_y()
        self.set_y(max(y_after_image, y_after_text) + 5)
        self.ln(5)

def get_image_filename(card_name):
    # Função auxiliar movida para cá para que create_reading_pdf funcione
    # Idealmente, esta função também estaria em helpers.py
    return card_name.lower().replace(' ', '_').replace('á', 'a').replace('ã', 'a').replace('ç', 'c') + ".png"

def create_reading_pdf(sel, interpretation, drawn_cards, spread_positions):
    import streamlit as st # Import local para evitar dependência circular
    user_name = sel.get("user_name", "Viajante")
    question = sel.get("question", "")
    spread_choice = sel.get("spread_choice", "")

    pdf = MysticalPDF('P', 'mm', 'A4')
    try:
        pdf.add_font('Cinzel', 'B', 'fonts/Cinzel-Bold.ttf')
        pdf.add_font('CormorantGaramond', '', 'fonts/CormorantGaramond-Regular.ttf')
        pdf.add_font('CormorantGaramond', 'I', 'fonts/CormorantGaramond-Italic.ttf')
        pdf.add_font('CormorantGaramond', 'B', 'fonts/CormorantGaramond-Bold.ttf')
    except RuntimeError:
        # st.error não funciona fora de um script Streamlit, então apenas usamos Helvetica
        pdf.add_page()
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, "Erro: Fontes personalizadas nao encontradas.")
        return pdf.output()

    clean_user_name = strip_emojis(user_name)
    clean_question = strip_emojis(question)
    clean_spread_choice = strip_emojis(spread_choice)
    clean_interpretation = strip_emojis(interpretation)

    pdf.mystical_title(f"Sua Revelação, {clean_user_name}")
    pdf.chapter_title("Foco da Consulta")
    pdf.chapter_body(clean_question if clean_question else "Uma orientação geral para o momento presente.")
    pdf.chapter_title("Tipo de Tiragem")
    pdf.chapter_body(clean_spread_choice)
    pdf.mystical_divider()
    pdf.chapter_title("As Cartas Reveladas")
    for i, item in enumerate(drawn_cards):
        if pdf.get_y() > pdf.h - 70:
            pdf.add_page()
            pdf.chapter_title("As Cartas Reveladas (continuação)")
        clean_position = strip_emojis(spread_positions[i])
        pdf.draw_card_details(item, clean_position)
    pdf.mystical_divider()
    pdf.chapter_title("A Interpretação do Oráculo")
    pdf.write_markdown_body(clean_interpretation)

    return pdf.output()


class CosmicPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.GOLD_COLOR = (212, 175, 55)
        self.DEEP_BLUE_COLOR = (15, 15, 35)
        self.TEXT_COLOR = (50, 50, 50)
        self.BG_COLOR = (245, 240, 225)

    def header(self):
        self.set_fill_color(*self.BG_COLOR)
        self.rect(0, 0, self.w, self.h, 'F')

    def footer(self):
        self.set_y(-15)
        self.set_font('CormorantGaramond', 'I', 8)
        self.set_text_color(*self.TEXT_COLOR)
        self.cell(0, 10, f'Página {self.page_no()}', new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
        self.cell(0, 10, 'Gerado pelos Ecos Estelares', new_x=XPos.RIGHT, new_y=YPos.TOP, align='R')

    def cosmic_title(self, text):
        if self.page_no() == 0:
            self.add_page()
        self.set_font('Cinzel', 'B', 24)
        self.set_text_color(*self.GOLD_COLOR)
        self.set_fill_color(*self.DEEP_BLUE_COLOR)
        self.cell(0, 15, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C', fill=True)
        self.ln(10)

    def chapter_title(self, text):
        self.set_font('Cinzel', 'B', 16)
        self.set_text_color(*self.DEEP_BLUE_COLOR)
        self.cell(0, 10, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(2)

    def chapter_body(self, text):
        self.set_font('CormorantGaramond', '', 12)
        self.set_text_color(*self.TEXT_COLOR)
        self.multi_cell(0, 7, text)
        self.ln(5)

    def sub_heading(self, text):
        self.set_font('Cinzel', 'B', 14)
        self.set_text_color(*self.DEEP_BLUE_COLOR)
        self.cell(0, 8, text.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(2)

    def write_markdown_body(self, text):
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('### '):
                self.sub_heading(line.replace('### ', ''))
            elif not line:
                self.ln(4)
            else:
                parts = re.split(r'(\*\*.*?\*\*)', line)
                self.set_font('CormorantGaramond', '', 12)
                self.set_text_color(*self.TEXT_COLOR)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        self.set_font('', 'B')
                        self.write(7, part[2:-2])
                    else:
                        self.set_font('', '')
                        self.write(7, part)
                self.ln()
        self.ln(5)

    def cosmic_divider(self):
        self.set_draw_color(*self.GOLD_COLOR)
        self.set_line_width(0.5)
        x = self.get_x()
        w = self.w - self.l_margin - self.r_margin
        self.line(x, self.get_y(), x + w, self.get_y())
        self.ln(8)

    def draw_astro_details(self, planet_name, planet_data, keywords):
        icon_map = {
            "Sol": "sun.png", "Lua": "moon.png", "Ascendente": "ascendant.png",
            "Mercúrio": "mercury.png", "Vênus": "venus.png", "Marte": "mars.png"
        }
        icon_filename = icon_map.get(planet_name, "default.png")
        image_path = os.path.join("images", "icons", icon_filename)

        y_start = self.get_y()

        if os.path.exists(image_path):
            self.image(image_path, x=self.l_margin, y=y_start, h=20)

        text_x_pos = self.l_margin + 25
        self.set_xy(text_x_pos, y_start)

        self.set_font('Cinzel', 'B', 16)
        self.set_text_color(*self.DEEP_BLUE_COLOR)
        self.cell(0, 8, planet_name, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_x(text_x_pos)

        self.set_font('CormorantGaramond', 'B', 14)
        self.set_text_color(*self.TEXT_COLOR)
        position_text = f"em {planet_data['sign']} na Casa {planet_data['house']}"
        self.cell(0, 8, position_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_x(text_x_pos)

        self.set_font('CormorantGaramond', 'I', 10)
        keywords_str = ", ".join(keywords)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 25, 5, keywords_str)

        y_after_icon = y_start + 22
        y_after_text = self.get_y()
        self.set_y(max(y_after_icon, y_after_text) + 5)
        self.ln(5)

# <<< CORREÇÃO AQUI: Adicionado o parâmetro PLANETARY_DATA >>>
def create_astro_pdf(session_data, interpretation, PLANETARY_DATA):
    user_name = session_data.get("user_name", "Viajante das Estelas")
    analysis_choice = session_data.get("analysis_choice", "Análise Padrão")
    chart_data = session_data.get("chart_data", {})

    pdf = CosmicPDF('P', 'mm', 'A4')
    try:
        pdf.add_font('Cinzel', 'B', 'fonts/Cinzel-Bold.ttf')
        pdf.add_font('CormorantGaramond', '', 'fonts/CormorantGaramond-Regular.ttf')
        pdf.add_font('CormorantGaramond', 'I', 'fonts/CormorantGaramond-Italic.ttf')
        pdf.add_font('CormorantGaramond', 'B', 'fonts/CormorantGaramond-Bold.ttf')
    except RuntimeError as e:
        print(f"Erro ao carregar fontes para o PDF: {e}")
        pdf.set_font("Helvetica", '', 12)
        pdf.add_page()
        pdf.cell(0, 10, "Erro: Fontes personalizadas nao encontradas.")
        return pdf.output()

    clean_user_name = strip_emojis(user_name)
    clean_analysis_choice = strip_emojis(analysis_choice)
    clean_interpretation = strip_emojis(interpretation)

    pdf.cosmic_title(f"Sua Revelação, {clean_user_name}")
    pdf.chapter_title("Foco da Sua Consulta")
    pdf.chapter_body(clean_analysis_choice)
    pdf.cosmic_divider()

    pdf.chapter_title("Sua Configuração Estelar")

    # <<< CORREÇÃO AQUI: Usa o PLANETARY_DATA passado como argumento >>>
    planet_key = PLANETARY_DATA[analysis_choice]['key']
    planet_data = chart_data.get(planet_key)

    if planet_data:
        keywords = PLANETARY_DATA[analysis_choice].get("keywords", [])
        pdf.draw_astro_details(planet_key, planet_data, keywords)
    else:
        pdf.chapter_body("Não foi possível carregar os detalhes da sua configuração estelar.")

    pdf.cosmic_divider()

    pdf.chapter_title("A Interpretação do Oráculo")
    pdf.write_markdown_body(clean_interpretation)

    return pdf.output()



class DreamOraclePDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.EARTH_COLOR = (85, 107, 47)
        self.GOLD_COLOR = (212, 175, 55)
        self.TEXT_COLOR = (40, 40, 40)
        self.PARCHMENT_COLOR = (245, 235, 215)
        self.TITLE_BG_COLOR = (45, 24, 16)

    def header(self):
        self.set_fill_color(*self.PARCHMENT_COLOR)
        self.rect(0, 0, self.w, self.h, 'F')

    def footer(self):
        self.set_y(-15)
        self.set_font('CrimsonText', 'I', 8)
        self.set_text_color(*self.TEXT_COLOR)
        self.cell(0, 10, f'Página {self.page_no()}', new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
        self.cell(0, 10, 'Gerado pelo Portal dos Sonhos Ancestrais', new_x=XPos.RIGHT, new_y=YPos.TOP, align='R')

    def main_document_title(self, text):
        if self.page_no() == 0:
            self.add_page()
        self.set_font('UncialAntiqua', 'B', 24)
        self.set_text_color(*self.GOLD_COLOR)
        self.set_fill_color(*self.TITLE_BG_COLOR)
        self.cell(0, 15, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C', fill=True)
        self.ln(10)

    def chapter_title(self, text):
        self.set_font('UncialAntiqua', 'B', 18)
        self.set_text_color(*self.EARTH_COLOR)
        self.cell(0, 10, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(5)

    def write_markdown_body(self, text):
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('### '):
                self.set_font('UncialAntiqua', 'B', 14)
                self.set_text_color(*self.EARTH_COLOR)
                self.cell(0, 8, line.replace('### ', '').upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.ln(2)
            elif not line:
                self.ln(4)
            else:
                parts = re.split(r'(\*\*.*?\*\*)', line)
                self.set_font('CrimsonText', '', 12)
                self.set_text_color(*self.TEXT_COLOR)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        self.set_font('', 'B')
                        self.write(7, part[2:-2])
                    else:
                        self.set_font('', '')
                        self.write(7, part)
                self.ln()
        self.ln(5)

    def shamanic_divider(self):
        self.set_draw_color(*self.GOLD_COLOR)
        self.set_line_width(0.8)
        x = self.get_x()
        w = self.w - self.l_margin - self.r_margin
        self.line(x, self.get_y(), x + w, self.get_y())
        self.ln(8)

def create_dream_pdf(session_data, interpretation):
    user_name = session_data.get("user_name", "Viajante dos Sonhos")
    dream_title = session_data.get("dream_title", "Sonho Sem Título")
    dream_description = session_data.get("dream_description", "Nenhuma descrição fornecida.")

    pdf = DreamOraclePDF('P', 'mm', 'A4')
    try:
        pdf.add_font('UncialAntiqua', 'B', 'fonts/UncialAntiqua-Regular.ttf')
        pdf.add_font('CrimsonText', '', 'fonts/CrimsonText-Regular.ttf')
        pdf.add_font('CrimsonText', 'I', 'fonts/CrimsonText-Italic.ttf')
        pdf.add_font('CrimsonText', 'B', 'fonts/CrimsonText-Bold.ttf')
    except RuntimeError as e:
        print(f"ERRO DE FONTE: {e}. Verifique se os arquivos .ttf estão na pasta 'fonts'.")
        pdf.set_font("Helvetica", '', 12)
        pdf.add_page()
        pdf.cell(0, 10, "Erro: Fontes personalizadas nao encontradas.")
        return pdf.output()

    clean_user_name = strip_emojis(user_name)
    clean_dream_title = strip_emojis(dream_title)
    clean_dream_description = strip_emojis(dream_description)
    clean_interpretation = strip_emojis(interpretation)

    pdf.main_document_title(f"Revelação de: {clean_dream_title}")

    pdf.chapter_title(f"O Sonho de {clean_user_name}")
    pdf.set_font('CrimsonText', 'I', 12)
    pdf.multi_cell(0, 7, f'"{clean_dream_description}"')

    pdf.shamanic_divider()

    pdf.chapter_title("A Interpretação do Oráculo")
    pdf.write_markdown_body(clean_interpretation)

    return pdf.output()
