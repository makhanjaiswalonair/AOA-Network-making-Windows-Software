import os
import subprocess

def gather_data_files():
    data_files = []
    directories = ["Spreadsheet_images", "dashboard_images"]

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                data_files.append((file_path, root))
    
    return data_files

def build_executable(script_name):
    data_files = gather_data_files()
    add_data_options = []

    for src, dest in data_files:
        if os.name == 'nt':  # Windows
            add_data_options.append(f"--add-data \"{src};{dest}\"")
    
    add_data_str = ' '.join(add_data_options)
    command = f"pyinstaller --onefile --windowed {add_data_str} {script_name}"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    build_executable("dash.py")
