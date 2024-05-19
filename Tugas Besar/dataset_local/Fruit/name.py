import os

def change_name_file_in_folder(folder_path):
    count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            count += 1
            new_filename = str(count) + ".jpg"
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))

change_name_file_in_folder("savefoto")

