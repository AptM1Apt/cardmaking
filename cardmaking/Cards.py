from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
import pandas as pd 
import pyphen

class card:
    CARD_WIDTH, CARD_HEIGHT = 500, 300  
    W = 5
    OUT = 20

    def __init__(self, 
                 name, 
                 condition, 
                 price, 
                 description, 
                 typeofitem="Предмет", 
                 typeofdamage=None, 
                 damage=None, 
                 usage=None, 
                 BG_COLOR=(255,255,255), 
                 BG_COLOR2=(200,200,200), 
                 TEXT_COLOR=(0,0,0)):
        
        if not os.path.exists("output\\cards"):
            os.makedirs("output\\cards")
        
        self.name = name
        self.condition = condition
        self.price = price
        self.description = description
        self.output = "output\\cards\\" + name + ".png"
        self.typeofitem = typeofitem
        self.typeofdamage = typeofdamage
        self.damage = damage
        self.usage = usage 
        self.BG_COLOR = BG_COLOR
        self.BG_COLOR2 = BG_COLOR2
        self.TEXT_COLOR = TEXT_COLOR
        self.cardimage = self.create_card()

    def create_card(self):    
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

        def add_comment_prefix(text, prefix="# "):
            return "\n".join(f"{prefix}{line}" for line in text.splitlines())

        img = Image.new("RGB", (self.CARD_WIDTH, self.CARD_HEIGHT), self.BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("assets\\claccon.ttf", 24)  # Обычный шрифт
        except IOError:
            font = ImageFont.load_default()  # Запасной вариант
        draw.rectangle(xy=(0, 0, self.CARD_WIDTH, self.OUT * 3), fill=self.BG_COLOR2)    
        draw.line(xy=(0,self.OUT * 3, self.CARD_WIDTH, self.OUT * 3), fill=self.TEXT_COLOR, width=5)

        #INNER BORDER
        if (self.damage != None and type != None):
            draw.rectangle(xy=(0, self.CARD_HEIGHT - self.OUT * 2, self.CARD_WIDTH, self.CARD_HEIGHT), fill=self.BG_COLOR2)
            draw.line(xy=(0,self.CARD_HEIGHT - self.OUT * 2, self.CARD_WIDTH, self.CARD_HEIGHT - self.OUT * 2), fill=self.TEXT_COLOR, width=5)
        
        #BORDER
        draw.rectangle(xy=(0,0,self.W,self.CARD_HEIGHT), fill=self.TEXT_COLOR)
        draw.rectangle(xy=(0,0,self.CARD_WIDTH,self.W), fill=self.TEXT_COLOR)
        draw.rectangle(xy=(self.CARD_WIDTH-self.W,0,self.CARD_WIDTH,self.CARD_HEIGHT), fill=self.TEXT_COLOR)
        draw.rectangle(xy=(0,self.CARD_HEIGHT-self.W,self.CARD_WIDTH,self.CARD_HEIGHT), fill=self.TEXT_COLOR)

        #NAME
        fortext = r"{}".format(add_comment_prefix(wrap_text(self.name, 21, 1)))
        if fortext.count(chr(10)) > 0: 
            draw.text((self.OUT + self.W, self.OUT * 0.75), f"{fortext}" , font=font, fill=self.TEXT_COLOR)
        else:
            draw.text((self.OUT + self.W, self.OUT + self.W), f"{fortext}" , font=font, fill=self.TEXT_COLOR)
        #PRICE
        draw.text((self.CARD_WIDTH - self.OUT * 8, self.OUT + self.W), f"G0: {self.price}", font=font, fill=self.TEXT_COLOR)
        #DESCRIPTION
        draw.multiline_text((self.OUT + self.W, 3.5 * self.OUT), f"ТИП: {self.typeofitem}\nОПИСАНИЕ = \'\'\'\n{wrap_text(self.description,36)}\n\'\'\'\n# Макс. Состояние: {self.condition}\n# Тек. Состояние: ___", font=font, fill=self.TEXT_COLOR, spacing=9)
        
        #DAMAGE AND ALL STUFF
        if (self.damage!=None and type!=None):
            draw.text((self.OUT+self.W, self.CARD_HEIGHT - self.OUT - 1.5 * self.W), f"# {self.typeofdamage}:{self.damage}", font=font, fill=self.TEXT_COLOR)
        if (self.usage!=None):
            draw.text((self.CARD_WIDTH - self.OUT * 8, self.CARD_HEIGHT - self.OUT - 1.5 * self.W), f"Исп:{self.usage}", font=font, fill=self.TEXT_COLOR)
        
        pixels = img.load()

        overlay_color = (80, 80, 80, 120)

        # Добавляем линии на каждую вторую строку
        for y in range(0, self.CARD_HEIGHT, 2):
            for x in range(self.CARD_WIDTH):
                pixels[x, y] = tuple(
                    (p + c) // 2 for p, c in zip(pixels[x, y], overlay_color)
                )

        return img

    def save_card(self):
        (self.cardimage).save(self.output)


def create_cards_CSV(df: pd.DataFrame):
    cards = []
    for i in range(len(df)):
        name, condition, price, description, typeofitem, typeofdamage, damage, usage = df.iloc[i]
        item = card(name, condition, price, description, typeofitem, typeofdamage, damage, usage)
        cards.append(item)
    
    cards.sort(key=lambda card: card.typeofitem)
    return cards
