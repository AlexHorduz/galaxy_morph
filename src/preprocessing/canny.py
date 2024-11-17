import os
import cv2

input_folder = 'C:/galaxy_images'
output_folder_denoised = './denoised_images'
output_folder_canny = './processed_images'

os.makedirs(output_folder_denoised, exist_ok=True)
os.makedirs(output_folder_canny, exist_ok=True)

def canny_edges_image(in_path, out_path_denoised, out_path_canny, use_denoiser=True):
    image = cv2.imread(in_path, cv2.IMREAD_GRAYSCALE)
    if use_denoiser:
        image = cv2.bilateralFilter(image, d=9, sigmaColor=100, sigmaSpace=75)
        image = cv2.fastNlMeansDenoising(image, h=15, templateWindowSize=7, searchWindowSize=21)
        cv2.imwrite(out_path_denoised, image)
    maxVal = 150
    minVal = int(0.4*maxVal)
    canny = cv2.Canny(image, minVal, maxVal, apertureSize=5)
    cv2.imwrite(out_path_canny, canny)


for filename in os.listdir(input_folder):
    image_path = os.path.join(input_folder, filename)
    if os.path.isfile(image_path) and filename.lower().endswith(('jpg', 'jpeg', 'png')):
        output_path_denoised = os.path.join(output_folder_denoised, filename)
        output_path_canny = os.path.join(output_folder_canny, filename)
        try:
            canny_edges_image(image_path, output_path_denoised, output_path_canny)
            #print(f'Оброблено: {filename}')
        except Exception as e:
            print(f'Помилка при обробці {filename}: {e}')