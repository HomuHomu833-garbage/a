import os
import subprocess
import argparse

astcenc_tool = r"./astcenc"

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description="Process images in a folder and its subfolders.")
    parser.add_argument('folder', help="The path to the folder containing images")
    return parser.parse_args()

def main():
    args = parse_args()
    folder_path = args.folder

    if not os.path.isdir(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".png"):
                image_path = os.path.join(root, file)

                try:
                    astc_file = image_path.replace(".png", ".astc")
                    astcenc_command = [astcenc_tool, "-cl", image_path, astc_file, "8x8", "-thorough", "-perceptual"]
                    run_command(astcenc_command)

                    os.remove(image_path)

                except Exception as e:
                    print(f"Error processing image {image_path}: {e}")

    print("Processing complete.")

if __name__ == "__main__":
    main()
