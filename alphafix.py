import os
from PIL import Image
from concurrent.futures import ProcessPoolExecutor

Image.MAX_IMAGE_PIXELS = None

def premultiply_alpha(image_path):
    try:
        image = Image.open(image_path).convert("RGBA")
        pixels = image.load()
        width, height = image.size

        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                r = (r * a) // 255
                g = (g * a) // 255
                b = (b * a) // 255
                pixels[x, y] = (r, g, b, a)

        image.save(image_path, "PNG")
        print(f"Fixed: {image_path}")
    except Exception as e:
        print(f"Error fixing {image_path}: {e}")

def collect_pngs(root_folder):
    png_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(".png"):
                png_files.append(os.path.join(root, file))
    return png_files

def process_folder_multithread(root_folder):
    png_files = collect_pngs(root_folder)
    with ProcessPoolExecutor() as executor:
        executor.map(premultiply_alpha, png_files)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python batch_premultiply_fast.py path/to/folder")
    else:
        folder = sys.argv[1]
        process_folder_multithread(folder)
        print("All PNGs processed with multithreading!")
