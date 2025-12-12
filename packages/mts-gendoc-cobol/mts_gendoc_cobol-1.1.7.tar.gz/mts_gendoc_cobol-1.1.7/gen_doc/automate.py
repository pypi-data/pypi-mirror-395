import os 
import argparse


def automate():
    args = argparse.ArgumentParser(description="Automate folder generation based on unique filenames.")
    args.add_argument("-i" , "--input", required=True, help="Path to input folder")
    parsed_args = args.parse_args()

    input_folder = parsed_args.input
    for root,dirs,files in os.walk(input_folder):
        for file in files:
            # grab all of the file name before the word 'prompt'
            unique_name = file.split("prompt")[0].strip()
            unique_folder_path = os.path.join(input_folder, unique_name)
            if not os.path.exists(unique_folder_path):
                os.makedirs(unique_folder_path)
            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(unique_folder_path, file)
            os.rename(old_file_path, new_file_path)
            if os.path.exists(old_file_path):
                # move the file to the existing folder with the same name
                os.rename(old_file_path, new_file_path)
            

if __name__ == "__main__":
    automate()