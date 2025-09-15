#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de rangement automatique des fichiers par type
Auteur: Assistant IA
Description: Range automatiquement les fichiers d'un dossier dans des sous-dossiers selon leur type
             avec confirmation utilisateur via Tkinter
"""

import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path

class FileOrganizer:
    def __init__(self):
        # Définition des catégories et extensions
        self.categories = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            'Vidéos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv'],
            'Documents': ['.pdf', '.docx', '.doc', '.txt', '.pptx', '.xlsx', '.csv'],
            'Musique': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz']
        }
        
        # Dossier par défaut (Téléchargements)
        self.default_folder = str(Path.home() / "Downloads")
        
        # Interface Tkinter
        self.root = tk.Tk()
        self.root.withdraw()  # Cacher la fenêtre principale
        
    def get_file_category(self, file_path):
        """Détermine la catégorie d'un fichier selon son extension"""
        extension = Path(file_path).suffix.lower()
        
        for category, extensions in self.categories.items():
            if extension in extensions:
                return category
        
        return 'Autres'  # Catégorie par défaut
    
    def create_folder_if_not_exists(self, folder_path):
        """Crée un dossier s'il n'existe pas"""
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Dossier créé: {folder_path}")
    
    def ask_confirmation(self, file_name, source_path, destination_path):
        """Affiche une fenêtre de confirmation pour le déplacement d'un fichier"""
        message = f"Voulez-vous déplacer le fichier:\n\n{file_name}\n\nVers le dossier:\n{destination_path}?"
        
        result = messagebox.askyesno(
            "Confirmation de déplacement", 
            message,
            icon='question'
        )
        
        return result
    
    def move_file(self, source_path, destination_folder):
        """Déplace un fichier vers le dossier de destination"""
        try:
            file_name = os.path.basename(source_path)
            destination_path = os.path.join(destination_folder, file_name)
            
            # Gérer les conflits de noms
            counter = 1
            original_destination = destination_path
            while os.path.exists(destination_path):
                name, ext = os.path.splitext(original_destination)
                destination_path = f"{name}_{counter}{ext}"
                counter += 1
            
            shutil.move(source_path, destination_path)
            print(f"Fichier déplacé: {file_name} -> {destination_folder}")
            return True
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du déplacement du fichier {file_name}:\n{str(e)}")
            return False
    
    def select_folder(self):
        """Permet à l'utilisateur de sélectionner le dossier à ranger"""
        # Demander si l'utilisateur veut utiliser le dossier par défaut
        use_default = messagebox.askyesno(
            "Sélection du dossier",
            f"Voulez-vous ranger le dossier Téléchargements par défaut?\n\n{self.default_folder}",
            icon='question'
        )
        
        if use_default and os.path.exists(self.default_folder):
            return self.default_folder
        else:
            # Ouvrir le sélecteur de dossier
            folder = filedialog.askdirectory(
                title="Sélectionnez le dossier à ranger",
                initialdir=self.default_folder if os.path.exists(self.default_folder) else os.path.expanduser("~")
            )
            return folder
    
    def organize_files(self, folder_path):
        """Organise tous les fichiers du dossier sélectionné"""
        if not os.path.exists(folder_path):
            messagebox.showerror("Erreur", f"Le dossier {folder_path} n'existe pas.")
            return
        
        # Obtenir la liste des fichiers (pas les dossiers)
        files = [f for f in os.listdir(folder_path) 
                if os.path.isfile(os.path.join(folder_path, f))]
        
        if not files:
            messagebox.showinfo("Information", "Aucun fichier à ranger dans ce dossier.")
            return
        
        # Statistiques
        moved_count = 0
        skipped_count = 0
        
        # Traiter chaque fichier
        for file_name in files:
            source_path = os.path.join(folder_path, file_name)
            category = self.get_file_category(source_path)
            
            # Créer le dossier de destination
            destination_folder = os.path.join(folder_path, category)
            self.create_folder_if_not_exists(destination_folder)
            
            # Demander confirmation
            if self.ask_confirmation(file_name, source_path, destination_folder):
                if self.move_file(source_path, destination_folder):
                    moved_count += 1
                else:
                    skipped_count += 1
            else:
                skipped_count += 1
                print(f"Fichier ignoré: {file_name}")
        
        # Afficher le résumé
        summary_message = f"Rangement terminé!\n\nFichiers déplacés: {moved_count}\nFichiers ignorés: {skipped_count}"
        messagebox.showinfo("Résumé", summary_message)
    
    def run(self):
        """Lance l'application"""
        try:
            # Message de bienvenue
            messagebox.showinfo(
                "Organisateur de fichiers",
                "Bienvenue dans l'organisateur de fichiers!\n\nCe programme va ranger vos fichiers dans des dossiers selon leur type.\n\nCliquez sur OK pour commencer."
            )
            
            # Sélectionner le dossier
            folder_path = self.select_folder()
            
            if folder_path:
                # Organiser les fichiers
                self.organize_files(folder_path)
            else:
                messagebox.showinfo("Annulé", "Opération annulée par l'utilisateur.")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur inattendue s'est produite:\n{str(e)}")
        
        finally:
            self.root.destroy()

def main():
    """Fonction principale"""
    organizer = FileOrganizer()
    organizer.run()

if __name__ == "__main__":
    main()