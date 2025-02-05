from PIL import Image, ImageDraw, ImageFont
import os

# Константы
CARD_WIDTH = 1000  # Увеличенная ширина карточки
CARD_HEIGHT = 600  # Увеличенная высота карточки
PADDING = 40  # Отступы между карточками
HEADER_HEIGHT = 150  # Высота заголовка (0 = без заголовка)

A4_WIDTH = 2480  # Ширина A4 в пикселях (при 300 DPI)
A4_HEIGHT = 3508  # Высота A4 в пикселях (при 300 DPI)
OUTPUT_FOLDER = "output_sheets"  # Папка для листов

HEADER_TEXT = "Карточки для игры"  # Заголовок (можно изменить или убрать)
FONT_PATH = "claccon.ttf"  # Путь к шрифту
FONT_SIZE = 80  # Размер шрифта заголовка

def create_a4_sheets(input_folder):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Получаем все изображения карточек
    images = [os.path.join(input_folder, f) for f in os.listdir(input_folder)
              if f.endswith((".png", ".jpg", ".jpeg"))]

    # Количество карточек по горизонтали (центрируем их)
    cols = A4_WIDTH // (CARD_WIDTH + PADDING)  # Сколько карточек по ширине
    total_card_width = cols * CARD_WIDTH + (cols - 1) * PADDING  # Общая ширина блока карточек
    x_offset = (A4_WIDTH - total_card_width) // 2  # Смещение для центрирования

    # Количество карточек по вертикали
    rows = (A4_HEIGHT - HEADER_HEIGHT) // (CARD_HEIGHT + PADDING)  
    cards_per_sheet = cols * rows  # Сколько карточек влезет на один лист

    sheet_index = 1
    for i in range(0, len(images), cards_per_sheet):
        # Создаём лист A4
        sheet = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
        draw = ImageDraw.Draw(sheet)

        # Добавляем заголовок, если нужно
        if HEADER_HEIGHT > 0 and HEADER_TEXT:
            try:
                font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
            except IOError:
                font = ImageFont.load_default()  # Если шрифт не найден
            text_bbox = font.getbbox(HEADER_TEXT)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            draw.text(((A4_WIDTH - text_width) // 2, 20), HEADER_TEXT, fill="black", font=font)

        # Размещаем карточки
        chunk = images[i:i + cards_per_sheet]
        for j, img_path in enumerate(chunk):
            img = Image.open(img_path).resize((CARD_WIDTH, CARD_HEIGHT))
            x = x_offset + (j % cols) * (CARD_WIDTH + PADDING)
            y = HEADER_HEIGHT + (j // cols) * (CARD_HEIGHT + PADDING)
            sheet.paste(img, (x, y))

        # Сохраняем лист
        sheet.save(os.path.join(OUTPUT_FOLDER, f"sheet_{sheet_index}.png"))
        sheet_index += 1

    print(f"Создано {sheet_index - 1} листов.")

# Использование
input_folder = "cards"  # Папка с карточками
create_a4_sheets(input_folder)
