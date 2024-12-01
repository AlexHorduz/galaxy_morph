import os

import pandas as pd
from PIL import Image

input_folder = 'D:/GalaxyMorphology/gz_decals_dr5_png_part1'
output_folder = 'D:/GalaxyMorphology/gz_decals_dr5_png_part1_cropped'
csv_file = 'D:/GalaxyMorphology/gz_decals_auto_posteriors.csv'

df = pd.read_csv(csv_file)

filtered_df = df[df['iauname'].str.startswith(
    tuple(f"J{str(i).zfill(3)}" for i in range(101)))]

if filtered_df.empty:
    print("Порожній .csv")
    exit()

os.makedirs(output_folder, exist_ok=True)


def process_image(image_path, output_path):
    if os.path.isfile(os.path.join(output_path, os.path.basename(image_path))):
        return

    image = Image.open(image_path)

    gray_image = image.convert('L')

    width, height = gray_image.size

    left = width // 5
    top = height // 5
    right = width - (width // 5)
    bottom = height - (height // 5)

    cropped_image = gray_image.crop((left, top, right, bottom))

    try:
        cropped_image.save(
            os.path.join(
                output_path,
                os.path.basename(image_path)),
            format='png')
    except Exception as e:
        print(e)


for _, row in filtered_df.iterrows():
    iauname = row['iauname']
    subfolder = iauname[:4]
    image_name = iauname + ".png"

    image_path = os.path.join(input_folder, subfolder, image_name)

    if os.path.exists(image_path):
        print(f"Обробка зображення: {image_path}")
        process_image(image_path, output_folder)
    else:
        print(f"Зображення не знайдено: {image_path}")
