import os
import pandas as pd

original_csv = 'D:/GalaxyMorphology/gz_decals_auto_posteriors.csv'
processed_images_dir = 'D:/GalaxyMorphology/gz_decals_dr5_png_part1_cropped'
output_csv = 'D:/GalaxyMorphology/gz_decals_auto_posteriors_cropped.csv'

df = pd.read_csv(original_csv)

processed_images = {os.path.splitext(f)[0] for f in os.listdir(processed_images_dir) if f.endswith('.png')}

filtered_df = df[df['iauname'].isin(processed_images)]

if filtered_df.empty:
    print("Немає відповідних записів для збереження.")
else:
    filtered_df.to_csv(output_csv, index=False)
    print(f"Новий файл збережено як {output_csv}")
