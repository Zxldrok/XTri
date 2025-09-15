#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organisateur de Fichiers avec Interface Graphique Complète
Auteur: Zx
Description: Interface graphique moderne pour ranger automatiquement les fichiers par type
"""

import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import threading
from datetime import datetime

class FileOrganizerGUI:
    def __init__(self):
        # Définition des catégories et extensions
        self.categories = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            'Vidéos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv'],
            'Documents': ['.pdf', '.docx', '.doc', '.txt', '.pptx', '.xlsx', '.csv'],
            'Musique': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz']
        }
        
        # Variables
        self.current_folder = str(Path.home() / "Downloads")
        self.files_data = []
        self.selected_files = set()
        
        # Interface principale
        self.root = tk.Tk()
        self.root.title("Organisateur de Fichiers - Interface Graphique")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Titre
        title_label = ttk.Label(main_frame, text="🗂️ Organisateur de Fichiers", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Section sélection de dossier
        folder_frame = ttk.LabelFrame(main_frame, text="Dossier à organiser", padding="10")
        folder_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        folder_frame.columnconfigure(1, weight=1)
        
        ttk.Label(folder_frame, text="Dossier:").grid(row=0, column=0, sticky=tk.W)
        
        self.folder_var = tk.StringVar(value=self.current_folder)
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, state="readonly")
        self.folder_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        
        ttk.Button(folder_frame, text="Parcourir", 
                  command=self.select_folder).grid(row=0, column=2)
        
        ttk.Button(folder_frame, text="Scanner", 
                  command=self.scan_folder).grid(row=0, column=3, padx=(5, 0))
        
        # Section liste des fichiers
        files_frame = ttk.LabelFrame(main_frame, text="Fichiers trouvés", padding="10")
        files_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        files_frame.columnconfigure(0, weight=1)
        files_frame.rowconfigure(1, weight=1)
        
        # Boutons de sélection
        selection_frame = ttk.Frame(files_frame)
        selection_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(selection_frame, text="Tout sélectionner", 
                  command=self.select_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(selection_frame, text="Tout désélectionner", 
                  command=self.deselect_all).pack(side=tk.LEFT, padx=(0, 5))
        
        self.count_label = ttk.Label(selection_frame, text="Aucun fichier")
        self.count_label.pack(side=tk.RIGHT)
        
        # Treeview pour les fichiers
        tree_frame = ttk.Frame(files_frame)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Colonnes du treeview
        columns = ('selected', 'filename', 'size', 'category', 'destination')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configuration des colonnes
        self.tree.heading('selected', text='✓')
        self.tree.heading('filename', text='Nom du fichier')
        self.tree.heading('size', text='Taille')
        self.tree.heading('category', text='Catégorie')
        self.tree.heading('destination', text='Destination')
        
        self.tree.column('selected', width=30, minwidth=30)
        self.tree.column('filename', width=250, minwidth=200)
        self.tree.column('size', width=80, minwidth=80)
        self.tree.column('category', width=100, minwidth=100)
        self.tree.column('destination', width=150, minwidth=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Placement du treeview et scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Bind pour la sélection
        self.tree.bind('<Button-1>', self.on_tree_click)
        
        # Section contrôles
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Barre de progression
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(control_frame, variable=self.progress_var, 
                                       maximum=100, length=300)
        self.progress.pack(side=tk.LEFT, padx=(0, 10))
        
        self.progress_label = ttk.Label(control_frame, text="Prêt")
        self.progress_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Boutons d'action
        ttk.Button(control_frame, text="Organiser les fichiers sélectionnés", 
                  command=self.organize_files).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Section résultats
        self.results_frame = ttk.LabelFrame(main_frame, text="Résultats", padding="10")
        self.results_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.results_text = tk.Text(self.results_frame, height=6, wrap=tk.WORD)
        results_scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, 
                                         command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Scanner le dossier par défaut
        self.scan_folder()
        
    def get_file_category(self, file_path):
        """Détermine la catégorie d'un fichier"""
        extension = Path(file_path).suffix.lower()
        for category, extensions in self.categories.items():
            if extension in extensions:
                return category
        return 'Autres'
    
    def format_file_size(self, size_bytes):
        """Formate la taille du fichier"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
    
    def select_folder(self):
        """Sélectionne un dossier"""
        folder = filedialog.askdirectory(
            title="Sélectionnez le dossier à organiser",
            initialdir=self.current_folder
        )
        if folder:
            self.current_folder = folder
            self.folder_var.set(folder)
            self.scan_folder()
    
    def scan_folder(self):
        """Scanne le dossier sélectionné"""
        if not os.path.exists(self.current_folder):
            messagebox.showerror("Erreur", f"Le dossier {self.current_folder} n'existe pas.")
            return
        
        # Vider la liste précédente
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.files_data = []
        self.selected_files = set()
        
        try:
            files = [f for f in os.listdir(self.current_folder) 
                    if os.path.isfile(os.path.join(self.current_folder, f))]
            
            for filename in files:
                file_path = os.path.join(self.current_folder, filename)
                file_size = os.path.getsize(file_path)
                category = self.get_file_category(file_path)
                destination = os.path.join(self.current_folder, category)
                
                file_data = {
                    'filename': filename,
                    'path': file_path,
                    'size': file_size,
                    'category': category,
                    'destination': destination
                }
                
                self.files_data.append(file_data)
                
                # Ajouter à la treeview
                item_id = self.tree.insert('', 'end', values=(
                    '☐',  # Non sélectionné par défaut
                    filename,
                    self.format_file_size(file_size),
                    category,
                    category
                ))
                
            self.update_count_label()
            self.log_message(f"Scan terminé: {len(files)} fichiers trouvés dans {self.current_folder}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du scan: {str(e)}")
    
    def on_tree_click(self, event):
        """Gère les clics sur la treeview"""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == '#1':  # Colonne de sélection
                item = self.tree.identify_row(event.y)
                if item:
                    self.toggle_selection(item)
    
    def toggle_selection(self, item):
        """Bascule la sélection d'un élément"""
        if item in self.selected_files:
            self.selected_files.remove(item)
            self.tree.set(item, 'selected', '☐')
        else:
            self.selected_files.add(item)
            self.tree.set(item, 'selected', '☑')
        
        self.update_count_label()
    
    def select_all(self):
        """Sélectionne tous les fichiers"""
        for item in self.tree.get_children():
            if item not in self.selected_files:
                self.selected_files.add(item)
                self.tree.set(item, 'selected', '☑')
        self.update_count_label()
    
    def deselect_all(self):
        """Désélectionne tous les fichiers"""
        for item in self.tree.get_children():
            if item in self.selected_files:
                self.selected_files.remove(item)
                self.tree.set(item, 'selected', '☐')
        self.update_count_label()
    
    def update_count_label(self):
        """Met à jour le label de comptage"""
        total = len(self.files_data)
        selected = len(self.selected_files)
        self.count_label.config(text=f"{selected}/{total} fichiers sélectionnés")
    
    def log_message(self, message):
        """Ajoute un message au log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()
    
    def create_folder_if_not_exists(self, folder_path):
        """Crée un dossier s'il n'existe pas"""
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            self.log_message(f"Dossier créé: {os.path.basename(folder_path)}")
    
    def organize_files(self):
        """Organise les fichiers sélectionnés"""
        if not self.selected_files:
            messagebox.showwarning("Attention", "Aucun fichier sélectionné.")
            return
        
        # Confirmation
        result = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous organiser {len(self.selected_files)} fichiers sélectionnés?"
        )
        
        if not result:
            return
        
        # Lancer l'organisation dans un thread séparé
        thread = threading.Thread(target=self._organize_files_thread)
        thread.daemon = True
        thread.start()
    
    def _organize_files_thread(self):
        """Thread pour organiser les fichiers"""
        try:
            selected_items = list(self.selected_files)
            total_files = len(selected_items)
            moved_count = 0
            error_count = 0
            
            self.progress_var.set(0)
            self.progress_label.config(text="Organisation en cours...")
            
            for i, item in enumerate(selected_items):
                # Trouver les données du fichier
                filename = self.tree.set(item, 'filename')
                file_data = next((f for f in self.files_data if f['filename'] == filename), None)
                
                if file_data:
                    try:
                        # Créer le dossier de destination
                        self.create_folder_if_not_exists(file_data['destination'])
                        
                        # Déplacer le fichier
                        destination_path = os.path.join(file_data['destination'], filename)
                        
                        # Gérer les conflits de noms
                        counter = 1
                        original_destination = destination_path
                        while os.path.exists(destination_path):
                            name, ext = os.path.splitext(original_destination)
                            destination_path = f"{name}_{counter}{ext}"
                            counter += 1
                        
                        shutil.move(file_data['path'], destination_path)
                        moved_count += 1
                        
                        self.log_message(f"✓ {filename} → {file_data['category']}")
                        
                        # Supprimer de la liste
                        self.tree.delete(item)
                        self.selected_files.remove(item)
                        
                    except Exception as e:
                        error_count += 1
                        self.log_message(f"✗ Erreur avec {filename}: {str(e)}")
                
                # Mettre à jour la progression
                progress = ((i + 1) / total_files) * 100
                self.progress_var.set(progress)
                self.progress_label.config(text=f"Traitement: {i + 1}/{total_files}")
            
            # Résumé final
            self.progress_var.set(100)
            self.progress_label.config(text="Terminé")
            self.log_message(f"\n=== RÉSUMÉ ===")
            self.log_message(f"Fichiers déplacés: {moved_count}")
            self.log_message(f"Erreurs: {error_count}")
            
            # Mettre à jour le compteur
            self.root.after(0, self.update_count_label)
            
            # Réinitialiser la progression après 3 secondes
            self.root.after(3000, lambda: [
                self.progress_var.set(0),
                self.progress_label.config(text="Prêt")
            ])
            
        except Exception as e:
            self.log_message(f"Erreur générale: {str(e)}")
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

def main():
    """Fonction principale"""
    app = FileOrganizerGUI()
    app.run()

if __name__ == "__main__":
    main()