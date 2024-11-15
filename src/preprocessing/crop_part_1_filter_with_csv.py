import os

import pandas as pd
from PIL import Image

# Визначаємо шляхи до папок
input_folder = 'D:/GalaxyMorphology/gz_decals_dr5_png_part1'
output_folder = 'D:/GalaxyMorphology/gz_decals_dr5_png_part1_cropped'
csv_file = 'D:/GalaxyMorphology/gz_decals_auto_posteriors.csv'

# Вантажимо CSV
df = pd.read_csv(csv_file)

# Фільтруємо записи, у яких 'iauname' починається на J000-J100 (перша тека)
filtered_df = df[df['iauname'].str.startswith(tuple(f"J{str(i).zfill(3)}" for i in range(101)))]

# Перевірка на дурника
if filtered_df.empty:
    print("Порожній .csv")
    exit()

# Створюємо теку для збереження оброблених зображень, якщо її ще немає
os.makedirs(output_folder, exist_ok=True)


# Функція для обробки зображень
def process_image(image_path, output_path):
    if os.path.isfile(os.path.join(output_path, os.path.basename(image_path))):
        return

    # Відкриваємо зображення
    image = Image.open(image_path)

    # Перетворюємо зображення у відтінки сірого
    gray_image = image.convert('L')

    # Отримуємо розміри зображення
    width, height = gray_image.size

    # Обрізаємо зображення: 1/5 з кожної сторони
    left = width // 5
    top = height // 5
    right = width - (width // 5)
    bottom = height - (height // 5)

    cropped_image = gray_image.crop((left, top, right, bottom))

    # Зберігаємо оброблене зображення
    try:
        cropped_image.save(os.path.join(output_path, os.path.basename(image_path)), format='png')
    except Exception as e:
        print(e)


# Проходження по відфільтрованому .csv
for _, row in filtered_df.iterrows():
    iauname = row['iauname']
    subfolder = iauname[:4]  # Наприклад, J000, J001, ..., J100
    image_name = iauname + ".png"

    # Формуємо шлях до файлу
    image_path = os.path.join(input_folder, subfolder, image_name)

    if os.path.exists(image_path):
        print(f"Обробка зображення: {image_path}")
        process_image(image_path, output_folder)
    else:
        print(f"Зображення не знайдено: {image_path}")
