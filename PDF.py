from PIL import Image
import os

def images_to_pdf(INPUT_FOLDER: str, PDF_FILE:str):
    images = [os.path.join(INPUT_FOLDER, f) for f in sorted(os.listdir(INPUT_FOLDER)) if f.endswith(".png")]

    if not images:
        print("Нет изображений для объединения в PDF.")
        return

    # Открываем первое изображение и преобразуем в RGB (чтобы избежать проблем с PNG)
    first_image = Image.open(images[0]).convert("RGB")
    
    # Открываем остальные и конвертируем в RGB
    image_list = [Image.open(img).convert("RGB") for img in images[1:]]
    PDF_FILE += ".pdf"
    # Сохраняем в PDF
    first_image.save(PDF_FILE, save_all=True, append_images=image_list)

