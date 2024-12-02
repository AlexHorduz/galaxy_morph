import os
import argparse
from PIL import Image
import cv2


def crop_image(image_path: str, output_path: str,
               crop_factor: float = 0.2) -> None:
    """
    Opens an image, converts it to grayscale, crops it based on the crop factor, and saves the result.

    :param image_path: Path to the original image.
    :param output_path: Path to save the cropped image.
    :param crop_factor: Proportion of the image to crop from each side (default: 0.2).
                        Must be between 0 and 0.5.
    """
    if not (0 <= crop_factor <= 0.5):
        raise ValueError("crop_factor must be between 0 and 0.5")

    image = Image.open(image_path)

    gray_image = image.convert('L')

    width, height = gray_image.size

    left = int(width * crop_factor)
    top = int(height * crop_factor)
    right = int(width * (1 - crop_factor))
    bottom = int(height * (1 - crop_factor))

    cropped_image = gray_image.crop((left, top, right, bottom))

    cropped_image.save(output_path)


def canny_edges_image(
    in_path: str,
    out_path_denoised: str,
    out_path_canny: str,
    use_denoiser: bool = True
) -> None:
    """
    Processes an image to detect edges using the Canny algorithm.
    Optionally applies denoising filters before edge detection.

    :param in_path: Path to the input image.
    :param out_path_denoised: Path to save the denoised image.
    :param out_path_canny: Path to save the image with edges detected.
    :param use_denoiser: Flag to apply denoising filters before edge detection (default: True).
    """
    image = cv2.imread(in_path, cv2.IMREAD_GRAYSCALE)

    if use_denoiser:
        image = cv2.bilateralFilter(image, d=9, sigmaColor=100, sigmaSpace=75)
        image = cv2.fastNlMeansDenoising(
            image, h=12, templateWindowSize=7, searchWindowSize=21)
        cv2.imwrite(out_path_denoised, image)

    max_val = 150
    min_val = int(0.4 * max_val)

    canny = cv2.Canny(image, min_val, max_val, apertureSize=5)

    cv2.imwrite(out_path_canny, canny)


def process_images(
    input_folder: str,
    output_folder: str,
    mode: str,
    crop_factor: float = 0.2
) -> None:
    """
    Processes all images in the input folder and saves results to the output folder.

    :param input_folder: Folder containing input images.
    :param output_folder: Folder to save processed images.
    :param mode: Processing mode ('canny' or 'crop').
    :param crop_factor: Crop factor for cropping mode (default: 0.2).
    """
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, filename)

        if os.path.isfile(image_path) and filename.lower().endswith(
                ('jpg', 'jpeg', 'png')):
            output_path = os.path.join(output_folder, filename)

            try:
                if mode == 'canny':
                    output_denoised = os.path.join(
                        output_folder, f"denoised_{filename}")
                    output_canny = os.path.join(
                        output_folder, f"canny_{filename}")
                    canny_edges_image(
                        image_path, output_denoised, output_canny)
                elif mode == 'crop':
                    crop_image(
                        image_path,
                        output_path,
                        crop_factor=crop_factor)
                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process images using Canny edge detection or cropping.")
    parser.add_argument(
        "input_folder",
        type=str,
        help="Path to the input folder containing images.")
    parser.add_argument(
        "output_folder",
        type=str,
        help="Path to the output folder to save processed images.")
    parser.add_argument(
        "mode",
        type=str,
        choices=[
            "canny",
            "crop"],
        help="Processing mode: 'canny' or 'crop'.")
    parser.add_argument(
        "--crop_factor",
        type=float,
        default=0.2,
        help="Crop factor for cropping mode (default: 0.2).")

    args = parser.parse_args()

    process_images(
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        mode=args.mode,
        crop_factor=args.crop_factor
    )
