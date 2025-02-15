from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import pyphen
from pydantic import BaseModel, PositiveInt 
from pydantic_extra_types.color import ColorTuple
import logging


class Item(BaseModel):
    name: str
    condition: int # from 1 to 12 TODO: Добавить ограничение.
    price: PositiveInt
    description: str
    type_of_item: str = "Предмет"
    type_of_damage: str | None
    damage_dice: str | None # Куб урона. TODO: Подумать над преобразованием в класс.
    usage: int # Заряд оружия

class ItemCardGenerator(BaseModel):
    _width: PositiveInt = 500
    _height: PositiveInt = 300  
    _margin = 5 # Типа Padding, но не падингтон
    _padding = 20
    _bg_primary_color: ColorTuple = (255, 255, 255)
    _bg_secondary_color: ColorTuple = (200, 200, 200)
    _text_color: ColorTuple = (0,0,0)
    _font_path: str = Path("/") / "assets" / "claccon.ttf"
    _header_max_length: int = 21
    _overlay_color: ColorTuple = (80, 80, 80, 120)
    output: Path = Path("/") / "output" / "cards"      

    def _wrap_text(text: str, max_length: int, is_header: bool = 0) -> str:
        length_coef = 2.4
        dic = pyphen.Pyphen(lang='ru')
        words = text.split()
        result = [] # каждый элемент - отдельная строка
        line = "" 

        # Почему нам нужно выходить за максимальную длину, а не укладываться в неё?
        if is_header and len(words) <= 2 and len(text) > max_length: # Загловок влезает в ограничения
            return "\n".join(words)  
        
        for word in words:
            if len(line) + len(word) + 1 < max_length: # Хватает места для слова
                line += word + " "
                continue

            if len(result) == 1 and is_header:  # Уже есть одна строка заголовка
                break

            if len(word) < max_length / length_coef:  # Считаем, что слово не переносится?
                result.append(line) # r.strip()
                line = word + " "
                continue

            avaiable_length = max_length - len(line)

            parts = dic.wrap(word, avaiable_length)
            if parts: # Слово переносится
                line += parts[0]
                result.append(line) # r.strip()
                line = parts[1] + " "
            else: # Слово НЕ переносится
                result.append(line) # r.strip()
                line = word + " "
            
        result.append(line.rstrip())  
        return "\n".join(result)
    
    def _add_comment_prefix(text, prefix="# "):
        return "\n".join(f"{prefix}{line}" for line in text.splitlines())

    def create_image(self, item: Item) -> Image:    
        img = Image.new("RGB", (self._width, self._height), self._bg_primary_color)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype(self._font_path, 24)  # Обычный шрифт
        except IOError:
            logging.WARNING("не получилось загрузить шрифт по пути", self._font_path)
            font = ImageFont.load_default()  # Запасной вариант

        draw.rectangle(xy=(0, 0, self._width, self._padding * 3),
                        fill=self._bg_secondary_color) # Фон заголовка    
        draw.line(xy=(0,self._padding * 3, self._width, self._padding * 3),
                   fill=self._text_color, width=5) # Разделительная линия

        #BORDER
        draw.rectangle(xy=(0,0,self._margin,self._height), fill=self._text_color)
        draw.rectangle(xy=(0,0,self._text_color,self._margin), fill=self._text_color)
        draw.rectangle(xy=(self._width-self._margin,0,self._width,self._height),
                        fill=self._text_color)
        draw.rectangle(xy=(0,self._height-self._margin,self._width,self._height),
                        fill=self._text_color)

        #NAME
        fortext = r"{}".format(
            self._add_comment_prefix(
            self._wrap_text(self.name, self._header_max_length, True)))
        if fortext.count('\n') > 0: 
            draw.text((self._padding + self._margin, self._padding * 0.75), f"{fortext}",
                       font=font, fill=self._text_color)
        else:
            draw.text((self._padding + self._margin, self._padding + self._margin), f"{fortext}",
                       font=font, fill=self._text_color)

        #PRICE
        draw.text((self._width - self._padding * 8, self._padding + self._margin),
                   f"G0: {self.price}", font=font, fill=self._text_color)
        #DESCRIPTION
        draw.multiline_text((self._padding + self._margin, 3.5 * self._padding),
                             f"ТИП: {self.typeofitem}\nОПИСАНИЕ = \'\'\'\n{self._wrap_text(item.description,36)}\n \
                                \'\'\'\n# Макс. Состояние: {item.condition}\n# Тек. Состояние: ___",
                                  font=font, fill=self._text_color, spacing=9)
        
        #INNER BORDER 
        # Если карточка оружия 
        if (item.damage_dice != None):
            draw.rectangle(xy=(0, self._height - self._padding * 2, self._width, self._height), fill=self._bg_secondary_color)
            draw.line(xy=(0,self._height - self._padding * 2, self._width, self._height - self._padding * 2), fill=self._text_color, width=5)
            draw.text((self._padding+self._margin, self._height - self._padding - 1.5 * self._margin), f"# {item.type_of_damage}:{item.damage_dice}", font=font, fill=self._text_color)
            if (item.usage!=None):
                draw.text((self._width - self._padding * 8, self._height - self._padding - 1.5 * self._margin), f"Исп:{item.usage}", font=font, fill=self._text_color)
        

        pixels = img.load() # TODO: Нужна ли это строка?

        # Добавляем линии на каждую вторую строку # TODO: Реализовать наложением фильтра
        for y in range(0, self._height, 2):
            for x in range(self._width):
                pixels[x, y] = tuple(
                    (p + c) // 2 for p, c in zip(pixels[x, y], self._overlay_color)
                )

        return img

