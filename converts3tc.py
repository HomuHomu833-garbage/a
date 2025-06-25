import os
import subprocess
import argparse
import shutil

texconv_tool = r".\texconv.exe"  # <-- Replace with actual path to texconv.exe
temp_output = "temp_dds"

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description="Convert PNG images in a folder to DXT5 DDS using texconv.")
    parser.add_argument('folder', help="The path to the folder containing images")
    return parser.parse_args()

def main():
    args = parse_args()
    folder_path = args.folder

    if not os.path.isdir(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    os.makedirs(temp_output, exist_ok=True)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".png"):
                image_path = os.path.join(root, file)
                filename_wo_ext = os.path.splitext(file)[0]
                dds_filename = filename_wo_ext + ".dds"
                temp_dds_path = os.path.join(temp_output, dds_filename)
                final_dds_path = os.path.join(root, dds_filename)

                try:
                    texconv_command = [
                        texconv_tool,
                        "-f", "DXT5",
                        "-m", "1",
                        "-y",
                        "-o", temp_output,
                        image_path
                    ]

                    run_command(texconv_command)

                    if os.path.exists(temp_dds_path):
                        shutil.move(temp_dds_path, final_dds_path)
                        os.remove(image_path)
                    else:
                        print(f"Failed to find output DDS for {file}")

                except Exception as e:
                    print(f"Error processing image {image_path}: {e}")

    # Clean up temp folder if empty
    try:
        shutil.rmtree(temp_output)
    except Exception as e:
        print(f"Could not remove temp folder: {e}")

    print("Conversion to DXT5 complete.")

if __name__ == "__main__":
    main()
