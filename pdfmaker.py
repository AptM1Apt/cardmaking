from PIL import Image
import os

OUTPUT_FOLDER = "output_sheets"  # Папка с листами
PDF_FILE = "final_cards.pdf"  # Итоговый PDF

def images_to_pdf():
    images = [os.path.join(OUTPUT_FOLDER, f) for f in sorted(os.listdir(OUTPUT_FOLDER)) if f.endswith(".png")]

    if not images:
        print("Нет изображений для объединения в PDF.")
        return

    # Открываем первое изображение и преобразуем в RGB (чтобы избежать проблем с PNG)
    first_image = Image.open(images[0]).convert("RGB")
    
    # Открываем остальные и конвертируем в RGB
    image_list = [Image.open(img).convert("RGB") for img in images[1:]]

    # Сохраняем в PDF
    first_image.save(PDF_FILE, save_all=True, append_images=image_list)
    
    print(f"PDF создан: {PDF_FILE}")

# Запускаем
images_to_pdf()
