import os
import zlib
import hashlib
import csv
import PySimpleGUI as sg

def calculate_hashes(file_path):
    hashes = {
        "CRC32": 0,
        "MD5": hashlib.md5(),
        "SHA256": hashlib.sha256()
    }

    with open(file_path, "rb") as file:
        while True:
            data = file.read(65536)  # 64 KB chunks
            if not data:
                break

            hashes["CRC32"] = zlib.crc32(data, hashes["CRC32"])
            hashes["MD5"].update(data)
            hashes["SHA256"].update(data)

    # Convert the MD5 and SHA-256 hexdigests to uppercase strings
    hashes["MD5"] = hashes["MD5"].hexdigest().upper() 
    hashes["SHA256"] = hashes["SHA256"].hexdigest().upper() 

    return hashes

def calculate_hashes_for_folder(folder_path, file_extension):
    hash_table = {}  # Dictionary to store file names and hashes

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith(file_extension.lower()):
                file_path = os.path.join(root, file_name)
                file_hashes = calculate_hashes(file_path)
                hash_table[file_name] = file_hashes

    return hash_table

def save_hash_table_to_csv(table, csv_folder, csv_filename):
    csv_file_path = os.path.join(csv_folder, csv_filename)
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Define the CSV header with hash types
        header = ["File Name", "CRC32", "MD5", "SHA256"]
        csv_writer.writerow(header)
        for file_name, hashes in table.items():
            row = [file_name, hashes["CRC32"], hashes["MD5"], hashes["SHA256"]]
            csv_writer.writerow(row)

def main():
    sg.theme('DarkGrey5')  # Change the theme if desired

    layout = [
        [sg.Text('Dossier Emplacement:'), sg.InputText(key='folder_path'), sg.FolderBrowse()],
        [sg.Text('Extension Fichier (ex: .h,.ass,.c,..):'), sg.InputText(key='file_extension')],
        [sg.Button('Calculer Empreintes'), sg.Button('Exit')]
    ]

    window = sg.Window('Hash Calculator', layout)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Calculate Hashes':
            folder_path = values['folder_path']
            file_extension = values['file_extension']
            output_folder = folder_path

            hash_table = calculate_hashes_for_folder(folder_path, file_extension)
            save_hash_table_to_csv(hash_table, output_folder, "Empreintes.csv")

    window.close()

if __name__ == "__main__":
    main()
