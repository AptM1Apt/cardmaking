from PIL import Image, ImageDraw, ImageFont
import os
import numpy as nm 
import pandas as pd 
import pyphen

# Настройки карточки
CARD_WIDTH, CARD_HEIGHT = 500, 300  # Горизонтальная ориентация
BG_COLOR = (255, 255, 255)  # Белый фон\
BG_COLOR2 = (200,200,200) 
TEXT_COLOR = (0, 0, 0)  # Черный текст
W = 5
OUT = 20
# Функция для создания карточки
def create_card(name, condition, price, description, OUTPUT, typeofitem="Предмет", typeofdamage=None, damage=None, usage=None):    
#================ВСТРОЕННАЯ ФУНКЦИЯ ДЛЯ ПЕРЕНОСА СТРОК==================================
    def wrap_text(text: str, max_length: int, q=0) -> str:
        dic = pyphen.Pyphen(lang='ru')
        words = text.split()
        result = []
        line = ""
        
        if q == 1 and len(words) == 2 and len(text) > max_length:
            return "\n".join(words)  # Просто переносим слова без обработки
        
        for word in words:
            if len(line) + len(word) + 1 > max_length:
                if len(result) == 1 and q == 1:  # Если уже есть одна строка, переносим остаток во вторую и выходим
                    break
                if len(word) > max_length / 2.4:  # Разбиваем длинное слово
                    parts = dic.wrap(word, max_length - len(line))
                    if parts:
                        line += parts[0]
                        result.append(line.rstrip())
                        line = parts[1] + " "
                    else:
                        result.append(line.rstrip())
                        line = word + " "
                else:
                    result.append(line.rstrip())
                    line = word + " "
            else:
                line += word + " "
        
        result.append(line.rstrip())  # Добавляем последнюю строку
        
        return "\n".join(result)
#================ВСТРОЕННАЯ ФУНКЦИЯ ДЛЯ ПЕРЕНОСА СТРОК==================================
#================ВСТРОЕННАЯ ФУНКЦИЯ ДЛЯ ДОБАВЛЕНИЯ СИМВОЛОВ=============================
    def add_comment_prefix(text, prefix="# "):
        return "\n".join(f"{prefix}{line}" for line in text.splitlines())
#================ВСТРОЕННАЯ ФУНКЦИЯ ДЛЯ ДОБАВЛЕНИЯ СИМВОЛОВ=============================
    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    
    output_path = OUTPUT + name + ".png"

    img = Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("claccon.ttf", 24)  # Обычный шрифт
    except IOError:
        font = ImageFont.load_default()  # Запасной вариант
    draw.rectangle(xy=(0, 0, CARD_WIDTH, OUT * 3), fill=BG_COLOR2)    
    draw.line(xy=(0,OUT * 3, CARD_WIDTH, OUT * 3), fill=TEXT_COLOR, width=5)

    #INNER BORDER
    if (damage != None and type != None):
        draw.rectangle(xy=(0, CARD_HEIGHT - OUT * 2, CARD_WIDTH, CARD_HEIGHT), fill=BG_COLOR2)
        draw.line(xy=(0,CARD_HEIGHT - OUT * 2, CARD_WIDTH, CARD_HEIGHT - OUT * 2), fill=TEXT_COLOR, width=5)
    
    #BORDER
    draw.rectangle(xy=(0,0,W,CARD_HEIGHT), fill=TEXT_COLOR)
    draw.rectangle(xy=(0,0,CARD_WIDTH,W), fill=TEXT_COLOR)
    draw.rectangle(xy=(CARD_WIDTH-W,0,CARD_WIDTH,CARD_HEIGHT), fill=TEXT_COLOR)
    draw.rectangle(xy=(0,CARD_HEIGHT-W,CARD_WIDTH,CARD_HEIGHT), fill=TEXT_COLOR)

    #NAME
    fortext = r"{}".format(add_comment_prefix(wrap_text(name, 21, 1)))
    if fortext.count(chr(10)) > 0: 
        draw.text((OUT + W, OUT * 0.75), f"{fortext}" , font=font, fill=TEXT_COLOR)
    else:
        draw.text((OUT + W, OUT + W), f"{fortext}" , font=font, fill=TEXT_COLOR)
    #PRICE
    draw.text((CARD_WIDTH - OUT * 8, OUT + W), f"G0: {price}", font=font, fill=TEXT_COLOR)
    #DESCRIPTION
    draw.multiline_text((OUT + W, 3.5 * OUT), f"ТИП: {typeofitem}\nОПИСАНИЕ = \'\'\'\n{wrap_text(description,36)}\n\'\'\'\n# Макс. Состояние: {condition}\n# Тек. Состояние: ___", font=font, fill=TEXT_COLOR, spacing=9)
    
    #DAMAGE AND ALL STUFF
    if (damage!=None and type!=None):
        draw.text((OUT+W, CARD_HEIGHT - OUT - 1.5 * W), f"# {typeofdamage}:{damage}", font=font, fill=TEXT_COLOR)
    if (usage!=None):
        draw.text((CARD_WIDTH - OUT * 8, CARD_HEIGHT - OUT - 1.5 * W), f"Исп:{usage}", font=font, fill=TEXT_COLOR)
    
    pixels = img.load()

    overlay_color = (80, 80, 80, 120)

    # Добавляем линии на каждую вторую строку
    for y in range(0, CARD_HEIGHT, 2):
        for x in range(CARD_WIDTH):
            pixels[x, y] = tuple(
                (p + c) // 2 for p, c in zip(pixels[x, y], overlay_color)
            )

    img.save(output_path)

def create_cards_CSV(df: pd.DataFrame, OUTPUT: str):
    for i in range(len(df)):
        name, condition, price, description, typeofitem, typeofdamage, damage, usage = df.iloc[i]
        create_card(name, condition, price, description, OUTPUT, typeofitem, typeofdamage, damage, usage)
