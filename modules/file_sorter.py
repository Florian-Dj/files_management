# -*- coding: utf-8 -*-

import os
import re
import shutil
from datetime import datetime
import time
import modules

path_folder = os.getcwd()  # Chemin à changer dans le fichier de config
list_folder = []  # Liste des dossiers
list_file = []  # Liste des fichiers sans dossiers
logs_list = []  # Liste des logs
check_folder = ["Vrac", "Films", "Doublon"]  # Liste des dossiers obligatoire


def folders_list():  # Liste des dossiers
    for folder in next(os.walk(path_folder))[1]:  # Check tous les dossiers
        if folder not in check_folder:  # Si le dossier check n'est pas dans la liste check_folder
            list_folder.append(folder)  # Ajout du dossier dans la liste list_folder
        else:
            check_folder.remove(folder)  # Supprime le dossier si existant de la liste check_folder
    for folders in check_folder:
        os.mkdir("{p}\\{f}".format(p=path_folder, f=folders))  # Création dossiers qui reste dans la liste check_folder
        logs_add(folders, folders, folders, "NEWS")
    return list_folder


def files_list():  # Liste des fichiers en .mp4 et .mkv
    for files in os.listdir(path_folder):
        _, ext = os.path.splitext(files)
        if ext == ".mp4" or ext == ".mkv" or ext == ".MP4" or ext == ".avi":
            list_file.append(files)
    return list_file


def compare(folder_list, file_list):  # Comparaison des dossiers et des fichiers
    for file in file_list:  # Boucle des fichiers
        mirror_folder = []
        for folder in folder_list:  # Boucle des dossiers
            if file.split('.')[0] == folder.split(" ")[0] or \
                file.split("_")[0] == folder.split(" ")[0] or \
                file.split(" ")[0] == folder.split(" ")[0] or \
                    file.split("-")[0] == folder.split(" ")[0]:  # Premier mot file == premier mot folder
                mirror_folder.append(folder)
        if len(mirror_folder) == 1:
            move_rename(file, mirror_folder[0])
        elif len(mirror_folder) > 1:
            mirror_folders(file, mirror_folder)
        else:
            text_warning(file)

    logs_write(logs_list)


# Gestion du fichier si aucun dossier est en commain


def text_warning(file):
    print("""====== Fichier sans dossier ======
    {f}
    1 - Voir les dossiers existant
    2 - Déplacer dans le dossier Vrac
    3 - Déplacer dans le dossier Films
    4 - Créer un dossier
    0 - Pas actions
    """.format(f=file))
    warning(file)


def warning(file):
    choose = input("Merci de faire votre choix :")  # Input pour faire son choix d'action
    choose_list = ["1", "2", "3", "4", "0"]  # Liste des choix possible
    if choose in choose_list:
        if choose == "1":
            text_choose_folder(file)
        elif choose == "2":  # On Déplace le fichier dans le dossier Vrac
            move(file, "Vrac")
        elif choose == "3":  # On déplace le fichier dans le dossier Films
            move(file, "Films")
        elif choose == "4":
            create_folder(file)
        elif choose == "0":
            pass
    else:
        print("Faire une bonne saisie!")
        warning(file)


# Gestion du fichier si choix 1 est choisi


def text_choose_folder(file):
    # Print pour voir tous les dossiers existant
    print("""====== Fichier sans dossier ======
    {}""".format(file))
    n = 1
    for folder in list_folder:
        print("    {n} - {f}".format(n=n, f=folder))
        n += 1
    print("    0 - Retour")
    choose_folder(file)


def choose_folder(file):
    choose = int(input("Dans quel dossier voulez-vous transférer le fichier ?"))
    if choose == 0:
        text_warning(file)
    elif 1 <= choose <= len(list_folder):
        move_rename(file, list_folder[choose - 1])
    else:
        print("Mauvaise saisie !")
        choose_folder(file)


# Gestion du rename et/ou du fichier selectionner


def move(file, folder):
    if folder == "Vrac":
        logs_add(folder, file, file, "WARNING")  # Lance la function pour les logs
    else:
        logs_add(folder, file, file, "INFO")  # Lance la function pour les logs
    old_file = "{p}\\{a}".format(p=path_folder, a=file)  # Chemin de l'ancien fichier
    if duplicate(file, folder, old_file):
        new_file = "{p}\\{f}\\{a}.mp4".format(p=path_folder, f=folder, a=file)  # Chemin du nouveau fichier
        shutil.move(old_file, new_file)  # Déplace le fichier dans le dossier


def move_rename(file, folder):  # Déplacer et Renommer un fichier
    try:  # Si le fichier a un numéro
        # Trouve le numéro dans le nom du fichier
        if re.findall(r"Épisode \d+", file):
            number = re.findall(r"Épisode \d+", file)[0][8:]
        elif re.findall(r"S\d+\.\d+", file):
            number = re.findall(r"S\d+\.\d+", file)[0].split('.')[1]
        elif re.findall(r"E\d+", file):
            number = re.findall(r"E\d+", file)[0].split('E')[1]
        elif re.findall(r"EP\d+", file):
            number = re.findall(r"EP\d+", file)[0].split('EP')[1]
        else:
            number = re.findall(r'\d+', file)[0]
        number_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        if number in number_list:
            number = "0" + number
        new_name = "{f} {n}.mp4".format(f=folder, n=number)  # Nom du nouveau fichier
    except IndexError:  # Si fichier non numéro
        new_name = "{f}.mp4".format(f=folder)  # Nom du nouveau fichier
    old_file = "{p}\\{a}".format(p=path_folder, a=file)  # Chemin de l'ancien fichier
    if duplicate(new_name, folder, old_file):
        new_file = "{p}\\{f}\\{n}".format(p=path_folder, f=folder, n=new_name)  # Chemin du nouveau fichier
        shutil.move(old_file, new_file)  # Déplace le fichier dans le dossier
        logs_add(folder, file, new_name, "INFO")  # Lance la function pour les logs


# Gestion du fichier si plusieurs dossier en commain


def mirror_folders(file, list_folders):
    # Print pour voir tous les dossiers en commun
    print("""====== Fichier avec plusieurs dossiers ======
    {}""".format(file))
    n = 1
    for folder in list_folders:
        print("    {n} - {f}".format(n=n, f=folder))
        n += 1
    choose_mirror_folder(file, list_folders)


def choose_mirror_folder(file, list_folders):
    choose = int(input("Dans quel dossier voulez-vous transférer le fichier ?"))
    if 1 <= choose <= len(list_folders):
        move_rename(file, list_folders[choose - 1])
    else:
        print("Mauvaise saisie !")
        choose_mirror_folder(file, list_folders)


def create_folder(file):  # Création de dossier
    new_folder = input("Nom du nouveau dossier :")
    if new_folder in list_folder:
        print("Un dossier du même nom existe déjà")
        create_folder(file)
    else:
        os.mkdir("{p}\\{n}".format(p=path_folder, n=new_folder))
        logs_add(new_folder, file, file, "NEWS")
        move_rename(file, new_folder)


def duplicate(file, folder, old_file):  # Verifie si le fichier n'existe pas déjà dans le dossier
    name = old_file.split("\\")[3]
    list_files = "{p}\\{f}".format(p=path_folder, f=folder)
    check = True
    for files in os.listdir(list_files):
        if file == files:
            logs_add("Doublon", name, name, "DUPLICATE")  # Lance la function pour les logs
            new_file = "{p}\\{f}".format(p=path_folder, f="Doublon")  # Chemin du nouveau fichier
            shutil.move(old_file, new_file)  # Déplace le fichier dans le dossier
            check = False
    if check:
        return check


# Functions pour les Logs


def logs_read():  # Lire le fichier des logs
    if "logs.txt" in os.listdir(path_folder):
        with open("{p}\\logs.txt".format(p=path_folder), mode="r", encoding='utf-8') as text:
            logs_list.append(text.read())
    else:
        with open("{p}\\logs.txt".format(p=path_folder), mode="w", encoding='utf-8') as text:
            text.write("{d}[NEWS]: Création de logs.txt".format(d=datetime.now().strftime("[%d-%m-%Y - %H:%M:%S]")))
    return logs_list


def logs_add(folder, old_file, new_file, info):  # Ajouter les logs dans la liste log
    time_info = datetime.now().strftime("[%d-%m-%Y - %H:%M:%S]")
    if info == "NEWS":  # Ecriture dans le fichier logs
        logs_list.insert(0, "{d}[{i}]: Création du dossier {f}\n".format(d=time_info, i=info, f=folder))
    else:  # Ecriture dans le fichier logs
        logs_list.insert(0, "{d}[{i}]: {o} ==> {f}\\{n}\n"
                         .format(d=time_info, i=info, o=old_file, f=folder, n=new_file))
    return logs_list


def logs_write(logs):  # Ecriture les logs dans le fichier
    with open("{p}\\logs.txt".format(p=path_folder), mode="w", encoding='utf-8') as text:
        for logs_list_write in logs:  # Boucle pour lire toute la liste logs
            text.write(logs_list_write)  # Ecriture dans le fichier logs


if __name__ == "__main__":
    logs_read()
    compare(folders_list(), files_list())
    time.sleep(0.2)
    modules.missing_files.compares(list_folder, path_folder, logs_list)
