# -*- coding: utf-8 -*-

import re
import os
from datetime import datetime

list_files = []  # Liste des fichiers sans dossiers
missing_files = []  # Liste des fichiers manquant


def compare(list_folder, path_folder, logs_list):
    for folders in list_folder:
        # Liste avec nom dossier + nom fichiers eux même dans une liste
        list_files.append([folders] + [os.listdir("{p}\\{f}".format(p=path_folder, f=folders))])
    i = 0  # Variable i pour incrémenter dossiers
    while i < len(list_files):
        o = 0  # Variable o pour incrémenter fichiers
        while o < len(list_files[i][1]):
            _, ext = os.path.splitext(list_files[i][1][o])  # Inspecte l'extension du fichier
            if not ext == ".mp4" or ext == ".mkv" or ext == ".MP4":
                list_files[i][1].remove(list_files[i][1][o])  # Sup les fichiers sans la bonne extension de la liste
            else:
                o += 1
        maximum = int(re.findall(r" \d+", list_files[i][1][-1])[0])  # Look le numero max des fichiers dans le dossier
        minimum = int(re.findall(r" \d+", list_files[i][1][0])[0])  # Look le numero min des fichiers dans le dossier
        if len(list_files[i][1]) < maximum - minimum + 1:  # Si moins de fichier que le calcul max - min + 1
            x = minimum  # Incémente le numéro du fichier par le nom
            y = 0  # Incémente le numéro du fichier dans la liste
            missing_number = []  # Reset de la liste des numéros manquant
            while y < len(list_files[i][1]):
                # Si numéro du fichier dans la liste == numéro du fichier par la nom
                if int(re.findall(r" \d+", list_files[i][1][y])[0].split(" ")[1]) == x:
                    x += 1
                    y += 1
                else:
                    missing_number.append(x)  # Ajout du numéro du fichier manquant dans la liste missing_list
                    x += 1
            # Ajout du nom du dossier et de la missing_list dans une liste
            missing_files.append([list_files[i][0], missing_number])
        i += 1
    for logs in missing_files:
        log(logs, path_folder, logs_list)  # Lancement de la function logs


def log(logs, path_folder, logs_list):
    logs_list.insert(0, "{d}[{i}]: {f} il manque les fichiers {n}\n".format(d=datetime.now().strftime("\
[%d-%m-%Y - %H:%M:%S]"), i="MISSING", f=logs[0], n=logs[1]))  # Insertion du texte logs dans la liste logs
    with open("{p}\\logs.txt".format(p=path_folder), mode="w", encoding='utf-8') as text:
        for logs_list_write in logs_list:  # Boucle pour lire toute la liste logs
            text.write(logs_list_write)  # Ecriture dans le fichier logs
