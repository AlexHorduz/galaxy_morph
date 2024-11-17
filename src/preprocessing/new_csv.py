import os
import pandas as pd

# Шляхи до файлів і папок
original_csv = 'D:/GalaxyMorphology/gz_decals_auto_posteriors.csv'
processed_images_dir = 'D:/GalaxyMorphology/gz_decals_dr5_png_part1_cropped'
output_csv = 'D:/GalaxyMorphology/gz_decals_auto_posteriors_cropped.csv'

# Завантаження оригінального .csv
df = pd.read_csv(original_csv)

# Отримання списку оброблених файлів (з іменами без розширення)
processed_images = {os.path.splitext(f)[0] for f in os.listdir(processed_images_dir) if f.endswith('.png')}

# Фільтрація записів, де `iauname` відповідає обробленим зображенням
filtered_df = df[df['iauname'].isin(processed_images)]

# Перевірка, чи є дані для збереження
if filtered_df.empty:
    print("Немає відповідних записів для збереження.")
else:
    # Збереження у новий .csv
    filtered_df.to_csv(output_csv, index=False)
    print(f"Новий файл збережено як {output_csv}")
