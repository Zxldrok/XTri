#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite d'Optimisation PC - Organisateur de Fichiers et Outils d'Optimisation
Auteur: Assistant IA
Description: Interface complète avec organisation de fichiers et optimisation PC
"""

import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import threading
from datetime import datetime
import tempfile
import psutil
import hashlib
from collections import defaultdict
import subprocess
import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from collections import deque
import time

class PCOptimizerSuite:
    def __init__(self):
        # Définition des catégories et extensions pour l'organisation
        self.categories = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff'],
            'Vidéos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'Documents': ['.pdf', '.docx', '.doc', '.txt', '.pptx', '.xlsx', '.csv', '.rtf', '.odt'],
            'Musique': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz']
        }
        
        # Variables
        self.current_folder = str(Path.home() / "Downloads")
        self.files_data = []
        self.selected_files = set()
        
        # Variables pour le gestionnaire de services
        self.services_list = []
        self.filtered_services = []
        
        # Interface principale
        self.root = tk.Tk()
        self.root.title("🚀 Suite d'Optimisation PC - XTri")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface utilisateur avec onglets"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Titre principal
        title_label = ttk.Label(main_frame, text="🚀 Suite d'Optimisation PC - XTri", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Notebook pour les onglets
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Créer les onglets
        self.create_file_organizer_tab()
        self.create_temp_cleaner_tab()
        self.create_recycle_bin_tab()
        self.create_disk_analyzer_tab()
        self.create_duplicate_finder_tab()
        self.create_browser_cleaner_tab()
        self.create_system_info_tab()
        self.create_performance_monitor_tab()
        self.create_startup_manager_tab()
        self.create_registry_cleaner_tab()
        self.create_service_manager_tab()
        
    def create_file_organizer_tab(self):
        """Onglet d'organisation des fichiers"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="📁 Organisation Fichiers")
        
        tab_frame.columnconfigure(1, weight=1)
        tab_frame.rowconfigure(2, weight=1)
        
        # Section sélection de dossier
        folder_frame = ttk.LabelFrame(tab_frame, text="Dossier à organiser", padding="10")
        folder_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
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
        files_frame = ttk.LabelFrame(tab_frame, text="Fichiers trouvés", padding="10")
        files_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
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
        
        columns = ('selected', 'filename', 'size', 'category', 'destination')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
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
        
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.tree.bind('<Button-1>', self.on_tree_click)
        
        # Contrôles
        control_frame = ttk.Frame(tab_frame)
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(control_frame, text="Organiser les fichiers sélectionnés", 
                  command=self.organize_files).pack(side=tk.RIGHT)
        
    def create_temp_cleaner_tab(self):
        """Onglet de nettoyage des fichiers temporaires"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="🧹 Nettoyage Temp")
        
        # Titre
        ttk.Label(tab_frame, text="Nettoyage des Fichiers Temporaires", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Options de nettoyage
        options_frame = ttk.LabelFrame(tab_frame, text="Options de nettoyage", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.clean_temp_var = tk.BooleanVar(value=True)
        self.clean_cache_var = tk.BooleanVar(value=True)
        self.clean_logs_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="Fichiers temporaires Windows", 
                       variable=self.clean_temp_var).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Cache utilisateur", 
                       variable=self.clean_cache_var).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Fichiers de logs (attention !)", 
                       variable=self.clean_logs_var).pack(anchor=tk.W)
        
        # Boutons d'action
        action_frame = ttk.Frame(tab_frame)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(action_frame, text="Analyser", 
                  command=self.analyze_temp_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="Nettoyer", 
                  command=self.clean_temp_files).pack(side=tk.LEFT)
        
        # Résultats
        self.temp_results = tk.Text(tab_frame, height=15, wrap=tk.WORD)
        temp_scrollbar = ttk.Scrollbar(tab_frame, orient=tk.VERTICAL, command=self.temp_results.yview)
        self.temp_results.configure(yscrollcommand=temp_scrollbar.set)
        
        self.temp_results.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        temp_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_recycle_bin_tab(self):
        """Onglet de gestion de la corbeille"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="🗑️ Corbeille")
        
        ttk.Label(tab_frame, text="Gestion de la Corbeille", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Informations sur la corbeille
        info_frame = ttk.LabelFrame(tab_frame, text="Informations", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.recycle_info_label = ttk.Label(info_frame, text="Cliquez sur 'Analyser' pour voir les informations")
        self.recycle_info_label.pack()
        
        # Boutons d'action
        action_frame = ttk.Frame(tab_frame)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(action_frame, text="Analyser la corbeille", 
                  command=self.analyze_recycle_bin).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="Vider la corbeille", 
                  command=self.empty_recycle_bin).pack(side=tk.LEFT)
        
        # Liste des fichiers dans la corbeille
        self.recycle_tree = ttk.Treeview(tab_frame, columns=('name', 'size', 'date'), show='headings', height=12)
        self.recycle_tree.heading('name', text='Nom du fichier')
        self.recycle_tree.heading('size', text='Taille')
        self.recycle_tree.heading('date', text='Date de suppression')
        
        recycle_scrollbar = ttk.Scrollbar(tab_frame, orient=tk.VERTICAL, command=self.recycle_tree.yview)
        self.recycle_tree.configure(yscrollcommand=recycle_scrollbar.set)
        
        self.recycle_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        recycle_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_disk_analyzer_tab(self):
        """Onglet d'analyse de l'espace disque"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="💾 Analyse Disque")
        
        ttk.Label(tab_frame, text="Analyse de l'Espace Disque", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Sélection du disque
        disk_frame = ttk.LabelFrame(tab_frame, text="Sélection du disque", padding="10")
        disk_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.disk_var = tk.StringVar()
        self.disk_combo = ttk.Combobox(disk_frame, textvariable=self.disk_var, state="readonly")
        self.disk_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(disk_frame, text="Analyser", 
                  command=self.analyze_disk_space).pack(side=tk.LEFT)
        
        # Résultats de l'analyse
        self.disk_results = tk.Text(tab_frame, height=15, wrap=tk.WORD)
        disk_scrollbar = ttk.Scrollbar(tab_frame, orient=tk.VERTICAL, command=self.disk_results.yview)
        self.disk_results.configure(yscrollcommand=disk_scrollbar.set)
        
        self.disk_results.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        disk_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Charger les disques disponibles
        self.load_available_disks()
        
    def create_browser_cleaner_tab(self):
        """Onglet de nettoyage du cache navigateur"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="🌐 Cache Navigateur")
        
        ttk.Label(tab_frame, text="Nettoyage du Cache Navigateur", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Options de navigateurs
        browsers_frame = ttk.LabelFrame(tab_frame, text="Navigateurs à nettoyer", padding="10")
        browsers_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.chrome_var = tk.BooleanVar(value=True)
        self.firefox_var = tk.BooleanVar(value=True)
        self.edge_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(browsers_frame, text="Google Chrome", 
                       variable=self.chrome_var).pack(anchor=tk.W)
        ttk.Checkbutton(browsers_frame, text="Mozilla Firefox", 
                       variable=self.firefox_var).pack(anchor=tk.W)
        ttk.Checkbutton(browsers_frame, text="Microsoft Edge", 
                       variable=self.edge_var).pack(anchor=tk.W)
        
        # Options de nettoyage
        options_frame = ttk.LabelFrame(tab_frame, text="Options de nettoyage", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.cache_var = tk.BooleanVar(value=True)
        self.cookies_var = tk.BooleanVar(value=False)
        self.history_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="Cache et fichiers temporaires", 
                       variable=self.cache_var).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Cookies (attention !)", 
                       variable=self.cookies_var).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Historique de navigation (attention !)", 
                       variable=self.history_var).pack(anchor=tk.W)
        
        # Boutons d'action
        action_frame = ttk.Frame(tab_frame)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(action_frame, text="Analyser", 
                  command=self.analyze_browser_cache).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="Nettoyer", 
                  command=self.clean_browser_cache).pack(side=tk.LEFT)
        
        # Résultats
        self.browser_results = tk.Text(tab_frame, height=12, wrap=tk.WORD)
        browser_scrollbar = ttk.Scrollbar(tab_frame, orient=tk.VERTICAL, command=self.browser_results.yview)
        self.browser_results.configure(yscrollcommand=browser_scrollbar.set)
        
        self.browser_results.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        browser_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_duplicate_finder_tab(self):
        """Onglet de recherche de doublons"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="🔍 Doublons")
        
        ttk.Label(tab_frame, text="Recherche de Fichiers Doublons", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Sélection du dossier à analyser
        folder_frame = ttk.LabelFrame(tab_frame, text="Dossier à analyser", padding="10")
        folder_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.duplicate_folder_var = tk.StringVar(value=str(Path.home()))
        ttk.Entry(folder_frame, textvariable=self.duplicate_folder_var, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(folder_frame, text="Parcourir", command=self.select_duplicate_folder).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(folder_frame, text="Rechercher", command=self.find_duplicates).pack(side=tk.LEFT)
        
        # Résultats
        self.duplicate_results = tk.Text(tab_frame, height=15, wrap=tk.WORD)
        duplicate_scrollbar = ttk.Scrollbar(tab_frame, orient=tk.VERTICAL, command=self.duplicate_results.yview)
        self.duplicate_results.configure(yscrollcommand=duplicate_scrollbar.set)
        
        self.duplicate_results.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        duplicate_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_system_info_tab(self):
        """Onglet d'informations système"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="ℹ️ Système")
        
        ttk.Label(tab_frame, text="Informations Système", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Bouton de rafraîchissement
        ttk.Button(tab_frame, text="Actualiser les informations", 
                  command=self.refresh_system_info).pack(pady=(0, 10))
        
        # Informations système
        self.system_info = tk.Text(tab_frame, height=20, wrap=tk.WORD)
        system_scrollbar = ttk.Scrollbar(tab_frame, orient=tk.VERTICAL, command=self.system_info.yview)
        self.system_info.configure(yscrollcommand=system_scrollbar.set)
        
        self.system_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        system_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Charger les informations au démarrage
        self.refresh_system_info()
    
    def create_performance_monitor_tab(self):
        """Crée l'onglet de monitoring des performances"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="📊 Performances")
        
        # Titre
        ttk.Label(tab_frame, text="Moniteur de Performances Temps Réel", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Frame pour les contrôles
        controls_frame = ttk.Frame(tab_frame)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        # Boutons de contrôle
        self.start_monitoring_btn = ttk.Button(controls_frame, text="▶️ Démarrer", 
                                              command=self.start_performance_monitoring)
        self.start_monitoring_btn.pack(side='left', padx=5)
        
        self.stop_monitoring_btn = ttk.Button(controls_frame, text="⏹️ Arrêter", 
                                             command=self.stop_performance_monitoring, state='disabled')
        self.stop_monitoring_btn.pack(side='left', padx=5)
        
        # Label d'intervalle
        ttk.Label(controls_frame, text="Intervalle (s):").pack(side='left', padx=(20, 5))
        self.interval_var = tk.StringVar(value="1")
        interval_spin = ttk.Spinbox(controls_frame, from_=0.5, to=10, increment=0.5, 
                                   width=5, textvariable=self.interval_var)
        interval_spin.pack(side='left', padx=5)
        
        # Frame pour les graphiques
        graphs_frame = ttk.Frame(tab_frame)
        graphs_frame.pack(fill='both', expand=True)
        
        # Créer la figure matplotlib
        self.perf_fig = Figure(figsize=(12, 8), dpi=100)
        self.perf_fig.patch.set_facecolor('#f0f0f0')
        
        # Sous-graphiques
        self.cpu_ax = self.perf_fig.add_subplot(3, 1, 1)
        self.memory_ax = self.perf_fig.add_subplot(3, 1, 2)
        self.network_ax = self.perf_fig.add_subplot(3, 1, 3)
        
        # Configuration des graphiques
        self.cpu_ax.set_title('Utilisation CPU (%)', fontweight='bold')
        self.cpu_ax.set_ylim(0, 100)
        self.cpu_ax.grid(True, alpha=0.3)
        
        self.memory_ax.set_title('Utilisation Mémoire (%)', fontweight='bold')
        self.memory_ax.set_ylim(0, 100)
        self.memory_ax.grid(True, alpha=0.3)
        
        self.network_ax.set_title('Trafic Réseau (MB/s)', fontweight='bold')
        self.network_ax.grid(True, alpha=0.3)
        
        # Ajuster l'espacement
        self.perf_fig.tight_layout()
        
        # Canvas pour afficher les graphiques
        self.perf_canvas = FigureCanvasTkAgg(self.perf_fig, graphs_frame)
        self.perf_canvas.draw()
        self.perf_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Initialiser les données
        self.max_data_points = 60  # 60 points pour 1 minute à 1s d'intervalle
        self.cpu_data = deque(maxlen=self.max_data_points)
        self.memory_data = deque(maxlen=self.max_data_points)
        self.network_sent_data = deque(maxlen=self.max_data_points)
        self.network_recv_data = deque(maxlen=self.max_data_points)
        self.time_data = deque(maxlen=self.max_data_points)
        
        # Variables de monitoring
        self.monitoring_active = False
        self.monitoring_thread = None
        self.last_network_stats = None
        
        # Variables pour le gestionnaire de démarrage
        self.startup_programs = []
        
        # Variables pour le nettoyeur de registre
        self.registry_issues = []
        self.backup_folder = str(Path.home() / "Documents" / "XTri_Registry_Backups")
        
    # Méthodes pour l'organisation des fichiers (reprises de la version précédente)
    def get_file_category(self, file_path):
        extension = Path(file_path).suffix.lower()
        for category, extensions in self.categories.items():
            if extension in extensions:
                return category
        return 'Autres'
    
    def format_file_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
    
    def select_folder(self):
        folder = filedialog.askdirectory(
            title="Sélectionnez le dossier à organiser",
            initialdir=self.current_folder
        )
        if folder:
            self.current_folder = folder
            self.folder_var.set(folder)
            self.scan_folder()
    
    def scan_folder(self):
        if not os.path.exists(self.current_folder):
            messagebox.showerror("Erreur", f"Le dossier {self.current_folder} n'existe pas.")
            return
        
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
                
                item_id = self.tree.insert('', 'end', values=(
                    '☐',
                    filename,
                    self.format_file_size(file_size),
                    category,
                    category
                ))
                
            self.update_count_label()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du scan: {str(e)}")
    
    def on_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == '#1':
                item = self.tree.identify_row(event.y)
                if item:
                    self.toggle_selection(item)
    
    def toggle_selection(self, item):
        if item in self.selected_files:
            self.selected_files.remove(item)
            self.tree.set(item, 'selected', '☐')
        else:
            self.selected_files.add(item)
            self.tree.set(item, 'selected', '☑')
        self.update_count_label()
    
    def select_all(self):
        for item in self.tree.get_children():
            if item not in self.selected_files:
                self.selected_files.add(item)
                self.tree.set(item, 'selected', '☑')
        self.update_count_label()
    
    def deselect_all(self):
        for item in self.tree.get_children():
            if item in self.selected_files:
                self.selected_files.remove(item)
                self.tree.set(item, 'selected', '☐')
        self.update_count_label()
    
    def update_count_label(self):
        total = len(self.files_data)
        selected = len(self.selected_files)
        self.count_label.config(text=f"{selected}/{total} fichiers sélectionnés")
    
    def organize_files(self):
        if not self.selected_files:
            messagebox.showwarning("Attention", "Aucun fichier sélectionné.")
            return
        
        result = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous organiser {len(self.selected_files)} fichiers sélectionnés?"
        )
        
        if result:
            thread = threading.Thread(target=self._organize_files_thread)
            thread.daemon = True
            thread.start()
    
    def _organize_files_thread(self):
        try:
            selected_items = list(self.selected_files)
            moved_count = 0
            
            for item in selected_items:
                filename = self.tree.set(item, 'filename')
                file_data = next((f for f in self.files_data if f['filename'] == filename), None)
                
                if file_data:
                    try:
                        if not os.path.exists(file_data['destination']):
                            os.makedirs(file_data['destination'])
                        
                        destination_path = os.path.join(file_data['destination'], filename)
                        counter = 1
                        original_destination = destination_path
                        while os.path.exists(destination_path):
                            name, ext = os.path.splitext(original_destination)
                            destination_path = f"{name}_{counter}{ext}"
                            counter += 1
                        
                        shutil.move(file_data['path'], destination_path)
                        moved_count += 1
                        
                        self.tree.delete(item)
                        self.selected_files.remove(item)
                        
                    except Exception as e:
                        print(f"Erreur avec {filename}: {str(e)}")
            
            self.root.after(0, self.update_count_label)
            messagebox.showinfo("Terminé", f"{moved_count} fichiers ont été organisés avec succès !")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur générale: {str(e)}")
    
    # Nouvelles méthodes pour l'optimisation PC
    def analyze_temp_files(self):
        """Analyse les fichiers temporaires"""
        self.temp_results.delete(1.0, tk.END)
        self.temp_results.insert(tk.END, "Analyse des fichiers temporaires...\n\n")
        
        thread = threading.Thread(target=self._analyze_temp_files_thread)
        thread.daemon = True
        thread.start()
    
    def _analyze_temp_files_thread(self):
        total_size = 0
        file_count = 0
        
        temp_dirs = [
            tempfile.gettempdir(),
            os.path.expandvars(r'%LOCALAPPDATA%\Temp'),
            os.path.expandvars(r'%TEMP%')
        ]
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                size = os.path.getsize(file_path)
                                total_size += size
                                file_count += 1
                            except:
                                continue
                except:
                    continue
        
        result = f"Analyse terminée:\n"
        result += f"Fichiers temporaires trouvés: {file_count}\n"
        result += f"Espace total utilisé: {self.format_file_size(total_size)}\n\n"
        
        self.root.after(0, lambda: self.temp_results.insert(tk.END, result))
    
    def clean_temp_files(self):
        """Nettoie les fichiers temporaires"""
        result = messagebox.askyesno(
            "Confirmation",
            "Êtes-vous sûr de vouloir nettoyer les fichiers temporaires ?\n\nCette action est irréversible."
        )
        
        if result:
            thread = threading.Thread(target=self._clean_temp_files_thread)
            thread.daemon = True
            thread.start()
    
    def _clean_temp_files_thread(self):
        deleted_count = 0
        freed_space = 0
        
        temp_dirs = [tempfile.gettempdir()]
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                size = os.path.getsize(file_path)
                                os.remove(file_path)
                                deleted_count += 1
                                freed_space += size
                            except:
                                continue
                except:
                    continue
        
        result = f"Nettoyage terminé:\n"
        result += f"Fichiers supprimés: {deleted_count}\n"
        result += f"Espace libéré: {self.format_file_size(freed_space)}\n\n"
        
        self.root.after(0, lambda: [
            self.temp_results.insert(tk.END, result),
            messagebox.showinfo("Terminé", f"Nettoyage terminé !\n{deleted_count} fichiers supprimés\nEspace libéré: {self.format_file_size(freed_space)}")
        ])
    
    def analyze_recycle_bin(self):
        """Analyse le contenu de la corbeille"""
        try:
            # Vider la liste précédente
            for item in self.recycle_tree.get_children():
                self.recycle_tree.delete(item)
            
            # Sur Windows, la corbeille est dans $Recycle.Bin
            recycle_paths = []
            for drive in ['C:', 'D:', 'E:', 'F:']:
                recycle_path = f"{drive}\\$Recycle.Bin"
                if os.path.exists(recycle_path):
                    recycle_paths.append(recycle_path)
            
            total_size = 0
            file_count = 0
            
            for recycle_path in recycle_paths:
                try:
                    for root, dirs, files in os.walk(recycle_path):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                size = os.path.getsize(file_path)
                                mtime = os.path.getmtime(file_path)
                                date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                                
                                self.recycle_tree.insert('', 'end', values=(
                                    file,
                                    self.format_file_size(size),
                                    date_str
                                ))
                                
                                total_size += size
                                file_count += 1
                            except:
                                continue
                except:
                    continue
            
            info_text = f"Fichiers dans la corbeille: {file_count} | Espace utilisé: {self.format_file_size(total_size)}"
            self.recycle_info_label.config(text=info_text)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'analyse de la corbeille: {str(e)}")
    
    def empty_recycle_bin(self):
        """Vide la corbeille"""
        result = messagebox.askyesno(
            "Confirmation",
            "Êtes-vous sûr de vouloir vider la corbeille ?\n\nCette action est irréversible."
        )
        
        if result:
            try:
                # Méthode alternative plus compatible
                if platform.system() == "Windows":
                    # Utiliser la commande rd pour vider la corbeille
                    recycle_paths = [
                        os.path.expandvars(r'%SystemDrive%\$Recycle.Bin'),
                        os.path.expandvars(r'%SystemDrive%\RECYCLER')
                    ]
                    
                    success = False
                    for recycle_path in recycle_paths:
                        if os.path.exists(recycle_path):
                            try:
                                # Essayer avec PowerShell d'abord
                                subprocess.run([
                                    'powershell', '-Command', 
                                    'Clear-RecycleBin -DriveLetter C -Force -Confirm:$false'
                                ], check=True, capture_output=True, text=True)
                                success = True
                                break
                            except:
                                # Si PowerShell échoue, essayer avec cmd
                                try:
                                    subprocess.run([
                                        'cmd', '/c', 'echo', 'Y', '|', 'del', '/s', '/q', 
                                        f'{recycle_path}\\*.*'
                                    ], check=True, capture_output=True)
                                    success = True
                                    break
                                except:
                                    continue
                    
                    if success:
                        messagebox.showinfo("Terminé", "La corbeille a été vidée avec succès !")
                    else:
                        messagebox.showwarning(
                            "Avertissement", 
                            "Impossible de vider la corbeille automatiquement.\n"
                            "Veuillez la vider manuellement ou exécuter en tant qu'administrateur."
                        )
                else:
                    messagebox.showerror("Erreur", "Cette fonctionnalité n'est disponible que sur Windows.")
                    
                self.analyze_recycle_bin()  # Actualiser l'affichage
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du vidage de la corbeille: {str(e)}")
    
    def load_available_disks(self):
        """Charge la liste des disques disponibles"""
        try:
            disks = []
            for partition in psutil.disk_partitions():
                disks.append(partition.device)
            
            self.disk_combo['values'] = disks
            if disks:
                self.disk_combo.current(0)
        except Exception as e:
            print(f"Erreur lors du chargement des disques: {e}")
    
    def analyze_disk_space(self):
        """Analyse l'espace disque"""
        selected_disk = self.disk_var.get()
        if not selected_disk:
            messagebox.showwarning("Attention", "Veuillez sélectionner un disque.")
            return
        
        self.disk_results.delete(1.0, tk.END)
        self.disk_results.insert(tk.END, f"Analyse de l'espace disque {selected_disk}...\n\n")
        
        thread = threading.Thread(target=self._analyze_disk_space_thread, args=(selected_disk,))
        thread.daemon = True
        thread.start()
    
    def _analyze_disk_space_thread(self, disk):
        try:
            usage = psutil.disk_usage(disk)
            
            result = f"=== ANALYSE DU DISQUE {disk} ===\n\n"
            result += f"Espace total: {self.format_file_size(usage.total)}\n"
            result += f"Espace utilisé: {self.format_file_size(usage.used)}\n"
            result += f"Espace libre: {self.format_file_size(usage.free)}\n"
            result += f"Pourcentage utilisé: {(usage.used / usage.total * 100):.1f}%\n\n"
            
            # Analyser les dossiers les plus volumineux
            result += "=== DOSSIERS LES PLUS VOLUMINEUX ===\n\n"
            
            folder_sizes = []
            try:
                for item in os.listdir(disk):
                    item_path = os.path.join(disk, item)
                    if os.path.isdir(item_path):
                        try:
                            size = sum(os.path.getsize(os.path.join(dirpath, filename))
                                     for dirpath, dirnames, filenames in os.walk(item_path)
                                     for filename in filenames)
                            folder_sizes.append((item, size))
                        except:
                            continue
                
                folder_sizes.sort(key=lambda x: x[1], reverse=True)
                
                for folder, size in folder_sizes[:10]:
                    result += f"{folder}: {self.format_file_size(size)}\n"
                    
            except Exception as e:
                result += f"Erreur lors de l'analyse des dossiers: {str(e)}\n"
            
            self.root.after(0, lambda: self.disk_results.insert(tk.END, result))
            
        except Exception as e:
            error_msg = f"Erreur lors de l'analyse: {str(e)}\n"
            self.root.after(0, lambda: self.disk_results.insert(tk.END, error_msg))
    
    def select_duplicate_folder(self):
        """Sélectionne le dossier pour la recherche de doublons"""
        folder = filedialog.askdirectory(
            title="Sélectionnez le dossier à analyser pour les doublons",
            initialdir=self.duplicate_folder_var.get()
        )
        if folder:
            self.duplicate_folder_var.set(folder)
    
    def find_duplicates(self):
        """Recherche les fichiers doublons"""
        folder = self.duplicate_folder_var.get()
        if not os.path.exists(folder):
            messagebox.showerror("Erreur", "Le dossier sélectionné n'existe pas.")
            return
        
        self.duplicate_results.delete(1.0, tk.END)
        self.duplicate_results.insert(tk.END, f"Recherche de doublons dans {folder}...\n\n")
        
        thread = threading.Thread(target=self._find_duplicates_thread, args=(folder,))
        thread.daemon = True
        thread.start()
    
    def _find_duplicates_thread(self, folder):
        try:
            file_hashes = defaultdict(list)
            
            # Calculer les hash des fichiers
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                            file_hashes[file_hash].append(file_path)
                    except:
                        continue
            
            # Trouver les doublons
            duplicates = {hash_val: paths for hash_val, paths in file_hashes.items() if len(paths) > 1}
            
            result = f"=== RÉSULTATS DE LA RECHERCHE ===\n\n"
            
            if duplicates:
                total_duplicates = sum(len(paths) - 1 for paths in duplicates.values())
                result += f"Groupes de doublons trouvés: {len(duplicates)}\n"
                result += f"Fichiers doublons: {total_duplicates}\n\n"
                
                for i, (hash_val, paths) in enumerate(duplicates.items(), 1):
                    result += f"--- Groupe {i} ---\n"
                    for path in paths:
                        try:
                            size = os.path.getsize(path)
                            result += f"  {path} ({self.format_file_size(size)})\n"
                        except:
                            result += f"  {path} (taille inconnue)\n"
                    result += "\n"
            else:
                result += "Aucun doublon trouvé !\n"
            
            self.root.after(0, lambda: self.duplicate_results.insert(tk.END, result))
            
        except Exception as e:
            error_msg = f"Erreur lors de la recherche: {str(e)}\n"
            self.root.after(0, lambda: self.duplicate_results.insert(tk.END, error_msg))
    
    def analyze_browser_cache(self):
        """Analyse le cache des navigateurs"""
        self.browser_results.delete(1.0, tk.END)
        self.browser_results.insert(tk.END, "Analyse du cache des navigateurs...\n\n")
        
        thread = threading.Thread(target=self._analyze_browser_cache_thread)
        thread.daemon = True
        thread.start()
    
    def _analyze_browser_cache_thread(self):
        try:
            total_size = 0
            total_files = 0
            
            browser_paths = self._get_browser_cache_paths()
            
            result = "=== ANALYSE DU CACHE NAVIGATEUR ===\n\n"
            
            for browser_name, paths in browser_paths.items():
                browser_size = 0
                browser_files = 0
                
                result += f"--- {browser_name} ---\n"
                
                for path_info in paths:
                    path = path_info['path']
                    name = path_info['name']
                    
                    if os.path.exists(path):
                        try:
                            for root, dirs, files in os.walk(path):
                                for file in files:
                                    try:
                                        file_path = os.path.join(root, file)
                                        size = os.path.getsize(file_path)
                                        browser_size += size
                                        browser_files += 1
                                    except:
                                        continue
                            
                            result += f"  {name}: {self.format_file_size(browser_size)} ({browser_files} fichiers)\n"
                        except Exception as e:
                            result += f"  {name}: Erreur d'accès\n"
                    else:
                        result += f"  {name}: Non trouvé\n"
                
                total_size += browser_size
                total_files += browser_files
                result += f"  Total {browser_name}: {self.format_file_size(browser_size)}\n\n"
            
            result += f"=== RÉSUMÉ GLOBAL ===\n"
            result += f"Taille totale du cache: {self.format_file_size(total_size)}\n"
            result += f"Nombre total de fichiers: {total_files}\n"
            
            self.root.after(0, lambda: self.browser_results.insert(tk.END, result))
            
        except Exception as e:
            error_msg = f"Erreur lors de l'analyse: {str(e)}\n"
            self.root.after(0, lambda: self.browser_results.insert(tk.END, error_msg))
    
    def clean_browser_cache(self):
        """Nettoie le cache des navigateurs"""
        result = messagebox.askyesno(
            "Confirmation",
            "Êtes-vous sûr de vouloir nettoyer le cache des navigateurs ?\n\n" +
            "ATTENTION: Fermez tous les navigateurs avant de continuer.\n" +
            "Cette action est irréversible."
        )
        
        if result:
            thread = threading.Thread(target=self._clean_browser_cache_thread)
            thread.daemon = True
            thread.start()
    
    def _clean_browser_cache_thread(self):
        try:
            deleted_files = 0
            freed_space = 0
            
            browser_paths = self._get_browser_cache_paths()
            
            result = "=== NETTOYAGE DU CACHE NAVIGATEUR ===\n\n"
            
            for browser_name, paths in browser_paths.items():
                if not self._should_clean_browser(browser_name):
                    continue
                
                browser_deleted = 0
                browser_freed = 0
                
                result += f"--- Nettoyage {browser_name} ---\n"
                
                for path_info in paths:
                    path = path_info['path']
                    name = path_info['name']
                    
                    if os.path.exists(path):
                        try:
                            for root, dirs, files in os.walk(path, topdown=False):
                                for file in files:
                                    try:
                                        file_path = os.path.join(root, file)
                                        size = os.path.getsize(file_path)
                                        os.remove(file_path)
                                        browser_deleted += 1
                                        browser_freed += size
                                    except:
                                        continue
                                
                                # Supprimer les dossiers vides
                                for dir in dirs:
                                    try:
                                        dir_path = os.path.join(root, dir)
                                        if not os.listdir(dir_path):
                                            os.rmdir(dir_path)
                                    except:
                                        continue
                            
                            result += f"  {name}: {browser_deleted} fichiers supprimés, {self.format_file_size(browser_freed)} libérés\n"
                        except Exception as e:
                            result += f"  {name}: Erreur lors du nettoyage\n"
                
                deleted_files += browser_deleted
                freed_space += browser_freed
                result += f"  Total {browser_name}: {self.format_file_size(browser_freed)}\n\n"
            
            result += f"=== RÉSUMÉ GLOBAL ===\n"
            result += f"Fichiers supprimés: {deleted_files}\n"
            result += f"Espace libéré: {self.format_file_size(freed_space)}\n"
            
            self.root.after(0, lambda: [
                self.browser_results.insert(tk.END, result),
                messagebox.showinfo("Terminé", f"Nettoyage terminé !\n{deleted_files} fichiers supprimés\nEspace libéré: {self.format_file_size(freed_space)}")
            ])
            
        except Exception as e:
            error_msg = f"Erreur lors du nettoyage: {str(e)}\n"
            self.root.after(0, lambda: self.browser_results.insert(tk.END, error_msg))
    
    def _get_browser_cache_paths(self):
        """Retourne les chemins de cache pour chaque navigateur"""
        user_profile = os.path.expanduser("~")
        
        paths = {
            'Chrome': [
                {
                    'name': 'Cache',
                    'path': os.path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cache')
                },
                {
                    'name': 'Code Cache',
                    'path': os.path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Code Cache')
                }
            ],
            'Firefox': [
                {
                    'name': 'Cache2',
                    'path': os.path.join(user_profile, 'AppData', 'Local', 'Mozilla', 'Firefox', 'Profiles')
                }
            ],
            'Edge': [
                {
                    'name': 'Cache',
                    'path': os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache')
                },
                {
                    'name': 'Code Cache',
                    'path': os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Code Cache')
                }
            ]
        }
        
        return paths
    
    def _should_clean_browser(self, browser_name):
        """Vérifie si le navigateur doit être nettoyé selon les options sélectionnées"""
        if browser_name == 'Chrome':
            return self.chrome_var.get()
        elif browser_name == 'Firefox':
            return self.firefox_var.get()
        elif browser_name == 'Edge':
            return self.edge_var.get()
        return False
    
    def refresh_system_info(self):
        """Actualise les informations système"""
        self.system_info.delete(1.0, tk.END)
        
        try:
            # Informations générales
            info = f"=== INFORMATIONS SYSTÈME ===\n\n"
            info += f"Système d'exploitation: {platform.system()} {platform.release()}\n"
            info += f"Architecture: {platform.architecture()[0]}\n"
            info += f"Processeur: {platform.processor()}\n\n"
            
            # Informations CPU
            info += f"=== PROCESSEUR ===\n"
            info += f"Cœurs physiques: {psutil.cpu_count(logical=False)}\n"
            info += f"Cœurs logiques: {psutil.cpu_count(logical=True)}\n"
            info += f"Utilisation CPU: {psutil.cpu_percent(interval=1)}%\n\n"
            
            # Informations mémoire
            memory = psutil.virtual_memory()
            info += f"=== MÉMOIRE ===\n"
            info += f"Mémoire totale: {self.format_file_size(memory.total)}\n"
            info += f"Mémoire utilisée: {self.format_file_size(memory.used)} ({memory.percent}%)\n"
            info += f"Mémoire disponible: {self.format_file_size(memory.available)}\n\n"
            
            # Informations disques
            info += f"=== DISQUES ===\n"
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    info += f"Disque {partition.device}:\n"
                    info += f"  Système de fichiers: {partition.fstype}\n"
                    info += f"  Taille totale: {self.format_file_size(usage.total)}\n"
                    info += f"  Utilisé: {self.format_file_size(usage.used)} ({usage.used / usage.total * 100:.1f}%)\n"
                    info += f"  Libre: {self.format_file_size(usage.free)}\n\n"
                except:
                    continue
            
            # Informations réseau
            net_io = psutil.net_io_counters()
            info += f"=== RÉSEAU ===\n"
            info += f"Octets envoyés: {self.format_file_size(net_io.bytes_sent)}\n"
            info += f"Octets reçus: {self.format_file_size(net_io.bytes_recv)}\n\n"
            
            self.system_info.insert(tk.END, info)
            
        except Exception as e:
            self.system_info.insert(tk.END, f"Erreur lors de la récupération des informations: {str(e)}")
    
    def start_performance_monitoring(self):
        """Démarre le monitoring des performances"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.start_monitoring_btn.config(state='disabled')
            self.stop_monitoring_btn.config(state='normal')
            
            # Initialiser les statistiques réseau
            self.last_network_stats = psutil.net_io_counters()
            
            # Démarrer le thread de monitoring
            self.monitoring_thread = threading.Thread(target=self._performance_monitoring_loop)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
    
    def stop_performance_monitoring(self):
        """Arrête le monitoring des performances"""
        self.monitoring_active = False
        self.start_monitoring_btn.config(state='normal')
        self.stop_monitoring_btn.config(state='disabled')
    
    def _performance_monitoring_loop(self):
        """Boucle de monitoring des performances"""
        while self.monitoring_active:
            try:
                # Obtenir les données de performance
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                
                # Calculer le trafic réseau
                current_network = psutil.net_io_counters()
                if self.last_network_stats:
                    sent_speed = (current_network.bytes_sent - self.last_network_stats.bytes_sent) / (1024 * 1024)  # MB/s
                    recv_speed = (current_network.bytes_recv - self.last_network_stats.bytes_recv) / (1024 * 1024)  # MB/s
                else:
                    sent_speed = recv_speed = 0
                
                self.last_network_stats = current_network
                
                # Ajouter les données aux collections
                current_time = time.time()
                self.cpu_data.append(cpu_percent)
                self.memory_data.append(memory_percent)
                self.network_sent_data.append(sent_speed)
                self.network_recv_data.append(recv_speed)
                self.time_data.append(current_time)
                
                # Mettre à jour les graphiques
                self.root.after(0, self._update_performance_graphs)
                
                # Attendre l'intervalle spécifié
                interval = float(self.interval_var.get())
                time.sleep(interval)
                
            except Exception as e:
                print(f"Erreur dans le monitoring: {e}")
                break
    
    def _update_performance_graphs(self):
        """Met à jour les graphiques de performance"""
        if not self.cpu_data:
            return
        
        try:
            # Créer les indices pour l'axe X
            x_indices = list(range(len(self.cpu_data)))
            
            # Effacer les graphiques précédents
            self.cpu_ax.clear()
            self.memory_ax.clear()
            self.network_ax.clear()
            
            # Graphique CPU
            self.cpu_ax.plot(x_indices, list(self.cpu_data), 'b-', linewidth=2, label='CPU')
            self.cpu_ax.set_title('Utilisation CPU (%)', fontweight='bold')
            self.cpu_ax.set_ylim(0, 100)
            self.cpu_ax.grid(True, alpha=0.3)
            self.cpu_ax.set_ylabel('%')
            
            # Graphique Mémoire
            self.memory_ax.plot(x_indices, list(self.memory_data), 'g-', linewidth=2, label='Mémoire')
            self.memory_ax.set_title('Utilisation Mémoire (%)', fontweight='bold')
            self.memory_ax.set_ylim(0, 100)
            self.memory_ax.grid(True, alpha=0.3)
            self.memory_ax.set_ylabel('%')
            
            # Graphique Réseau
            self.network_ax.plot(x_indices, list(self.network_sent_data), 'r-', linewidth=2, label='Envoyé')
            self.network_ax.plot(x_indices, list(self.network_recv_data), 'orange', linewidth=2, label='Reçu')
            self.network_ax.set_title('Trafic Réseau (MB/s)', fontweight='bold')
            self.network_ax.grid(True, alpha=0.3)
            self.network_ax.set_ylabel('MB/s')
            self.network_ax.set_xlabel('Temps')
            self.network_ax.legend()
            
            # Ajuster l'espacement et redessiner
            self.perf_fig.tight_layout()
            self.perf_canvas.draw()
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour des graphiques: {e}")
    
    def create_startup_manager_tab(self):
        """Crée l'onglet de gestion des programmes de démarrage"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="🚀 Démarrage")
        
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(2, weight=1)
        
        # Titre
        title_label = ttk.Label(tab_frame, text="Gestionnaire de Programmes de Démarrage", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Frame pour les contrôles
        controls_frame = ttk.Frame(tab_frame)
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Boutons
        refresh_startup_btn = ttk.Button(controls_frame, text="🔄 Actualiser", 
                                        command=self.refresh_startup_programs)
        refresh_startup_btn.pack(side='left', padx=(0, 5))
        
        self.disable_startup_btn = ttk.Button(controls_frame, text="❌ Désactiver", 
                                             command=self.disable_startup_program, state='disabled')
        self.disable_startup_btn.pack(side='left', padx=5)
        
        self.enable_startup_btn = ttk.Button(controls_frame, text="✅ Activer", 
                                            command=self.enable_startup_program, state='disabled')
        self.enable_startup_btn.pack(side='left', padx=5)
        
        # Frame pour la liste
        list_frame = ttk.LabelFrame(tab_frame, text="Programmes de Démarrage", padding="10")
        list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview pour les programmes de démarrage
        columns = ('Nom', 'Statut', 'Éditeur', 'Chemin')
        self.startup_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configuration des colonnes
        self.startup_tree.heading('Nom', text='Nom du Programme')
        self.startup_tree.heading('Statut', text='Statut')
        self.startup_tree.heading('Éditeur', text='Éditeur')
        self.startup_tree.heading('Chemin', text='Chemin')
        
        self.startup_tree.column('Nom', width=200)
        self.startup_tree.column('Statut', width=100)
        self.startup_tree.column('Éditeur', width=150)
        self.startup_tree.column('Chemin', width=300)
        
        # Scrollbars
        startup_v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.startup_tree.yview)
        startup_h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.startup_tree.xview)
        self.startup_tree.configure(yscrollcommand=startup_v_scrollbar.set, xscrollcommand=startup_h_scrollbar.set)
        
        # Placement
        self.startup_tree.grid(row=0, column=0, sticky='nsew')
        startup_v_scrollbar.grid(row=0, column=1, sticky='ns')
        startup_h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Bind pour la sélection
        self.startup_tree.bind('<<TreeviewSelect>>', self.on_startup_select)
        
        # Zone d'informations
        info_frame = ttk.LabelFrame(tab_frame, text="Informations", padding="10")
        info_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        info_frame.columnconfigure(0, weight=1)
        
        self.startup_info_text = tk.Text(info_frame, height=4, wrap='word', font=('Consolas', 9))
        startup_info_scrollbar = ttk.Scrollbar(info_frame, orient='vertical', command=self.startup_info_text.yview)
        self.startup_info_text.configure(yscrollcommand=startup_info_scrollbar.set)
        
        self.startup_info_text.grid(row=0, column=0, sticky='nsew')
        startup_info_scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Charger les programmes au démarrage
        self.refresh_startup_programs()
    
    def refresh_startup_programs(self):
        """Actualise la liste des programmes de démarrage"""
        def _refresh_thread():
            try:
                self.startup_info_text.delete(1.0, tk.END)
                self.startup_info_text.insert(tk.END, "Analyse des programmes de démarrage...\n")
                
                # Vider la liste actuelle
                for item in self.startup_tree.get_children():
                    self.startup_tree.delete(item)
                
                self.startup_programs = []
                
                if platform.system() == "Windows":
                    # Utiliser wmic pour obtenir les programmes de démarrage
                    try:
                        result = subprocess.run([
                            'wmic', 'startup', 'get', 
                            'Name,Command,Location,User', '/format:csv'
                        ], capture_output=True, text=True, timeout=30)
                        
                        if result.returncode == 0:
                            lines = result.stdout.strip().split('\n')
                            for line in lines[1:]:  # Skip header
                                if line.strip() and ',' in line:
                                    parts = line.split(',')
                                    if len(parts) >= 4:
                                        command = parts[1].strip()
                                        location = parts[2].strip()
                                        name = parts[3].strip()
                                        
                                        if name and command:
                                            program_info = {
                                                'name': name,
                                                'command': command,
                                                'location': location,
                                                'status': 'Activé',
                                                'publisher': 'Inconnu'
                                            }
                                            self.startup_programs.append(program_info)
                    except Exception as e:
                        self.startup_info_text.insert(tk.END, f"Erreur WMIC: {e}\n")
                    
                    # Essayer aussi avec le registre
                    try:
                        import winreg
                        
                        # Clés de registre pour les programmes de démarrage
                        startup_keys = [
                            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
                            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce")
                        ]
                        
                        for hkey, subkey in startup_keys:
                            try:
                                with winreg.OpenKey(hkey, subkey) as key:
                                    i = 0
                                    while True:
                                        try:
                                            name, command, _ = winreg.EnumValue(key, i)
                                            
                                            # Vérifier si ce programme n'est pas déjà dans la liste
                                            exists = any(p['name'] == name for p in self.startup_programs)
                                            if not exists:
                                                program_info = {
                                                    'name': name,
                                                    'command': command,
                                                    'location': 'Registre',
                                                    'status': 'Activé',
                                                    'publisher': 'Inconnu'
                                                }
                                                self.startup_programs.append(program_info)
                                            i += 1
                                        except OSError:
                                            break
                            except Exception:
                                continue
                                
                    except ImportError:
                        self.startup_info_text.insert(tk.END, "Module winreg non disponible\n")
                    except Exception as e:
                        self.startup_info_text.insert(tk.END, f"Erreur registre: {e}\n")
                
                # Mettre à jour l'interface
                self.root.after(0, self._update_startup_display)
                
            except Exception as e:
                self.root.after(0, lambda: self.startup_info_text.insert(tk.END, f"Erreur: {e}\n"))
        
        threading.Thread(target=_refresh_thread, daemon=True).start()
    
    def _update_startup_display(self):
        """Met à jour l'affichage des programmes de démarrage"""
        try:
            # Vider la liste
            for item in self.startup_tree.get_children():
                self.startup_tree.delete(item)
            
            # Ajouter les programmes
            for program in self.startup_programs:
                self.startup_tree.insert('', 'end', values=(
                    program['name'],
                    program['status'],
                    program['publisher'],
                    program['command'][:80] + '...' if len(program['command']) > 80 else program['command']
                ))
            
            # Mettre à jour les informations
            self.startup_info_text.delete(1.0, tk.END)
            self.startup_info_text.insert(tk.END, f"Trouvé {len(self.startup_programs)} programmes de démarrage.\n")
            self.startup_info_text.insert(tk.END, "Sélectionnez un programme pour voir plus de détails.")
            
        except Exception as e:
            self.startup_info_text.insert(tk.END, f"Erreur d'affichage: {e}\n")
    
    def on_startup_select(self, event):
        """Gère la sélection d'un programme de démarrage"""
        selection = self.startup_tree.selection()
        if selection:
            item = selection[0]
            values = self.startup_tree.item(item, 'values')
            
            if values:
                # Trouver le programme correspondant
                program_name = values[0]
                program = next((p for p in self.startup_programs if p['name'] == program_name), None)
                
                if program:
                    # Mettre à jour les informations
                    self.startup_info_text.delete(1.0, tk.END)
                    self.startup_info_text.insert(tk.END, f"Nom: {program['name']}\n")
                    self.startup_info_text.insert(tk.END, f"Statut: {program['status']}\n")
                    self.startup_info_text.insert(tk.END, f"Emplacement: {program['location']}\n")
                    self.startup_info_text.insert(tk.END, f"Commande: {program['command']}")
                    
                    # Activer/désactiver les boutons
                    if program['status'] == 'Activé':
                        self.disable_startup_btn.config(state='normal')
                        self.enable_startup_btn.config(state='disabled')
                    else:
                        self.disable_startup_btn.config(state='disabled')
                        self.enable_startup_btn.config(state='normal')
        else:
            self.disable_startup_btn.config(state='disabled')
            self.enable_startup_btn.config(state='disabled')
    
    def disable_startup_program(self):
        """Désactive un programme de démarrage"""
        selection = self.startup_tree.selection()
        if not selection:
            return
        
        if messagebox.askyesno("Confirmation", 
                              "Êtes-vous sûr de vouloir désactiver ce programme au démarrage?"):
            messagebox.showinfo("Information", 
                               "Fonctionnalité de désactivation en cours de développement.\n"
                               "Pour des raisons de sécurité, utilisez les outils système Windows.")
    
    def enable_startup_program(self):
        """Active un programme de démarrage"""
        selection = self.startup_tree.selection()
        if not selection:
            return
        
        if messagebox.askyesno("Confirmation", 
                              "Êtes-vous sûr de vouloir activer ce programme au démarrage?"):
            messagebox.showinfo("Information", 
                               "Fonctionnalité d'activation en cours de développement.\n"
                               "Pour des raisons de sécurité, utilisez les outils système Windows.")
    
    def create_registry_cleaner_tab(self):
        """Crée l'onglet de nettoyage du registre Windows"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="🔧 Registre")
        
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(2, weight=1)
        
        # Titre
        title_label = ttk.Label(tab_frame, text="Nettoyeur de Registre Windows", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Frame pour les contrôles
        controls_frame = ttk.Frame(tab_frame)
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Boutons
        scan_registry_btn = ttk.Button(controls_frame, text="🔍 Analyser le Registre", 
                                      command=self.scan_registry_issues)
        scan_registry_btn.pack(side='left', padx=(0, 5))
        
        self.clean_registry_btn = ttk.Button(controls_frame, text="🧹 Nettoyer", 
                                            command=self.clean_registry_issues, state='disabled')
        self.clean_registry_btn.pack(side='left', padx=5)
        
        backup_btn = ttk.Button(controls_frame, text="💾 Créer Sauvegarde", 
                               command=self.create_registry_backup)
        backup_btn.pack(side='left', padx=5)
        
        restore_btn = ttk.Button(controls_frame, text="🔄 Restaurer", 
                                command=self.restore_registry_backup)
        restore_btn.pack(side='left', padx=5)
        
        # Frame pour la liste des problèmes
        list_frame = ttk.LabelFrame(tab_frame, text="Problèmes de Registre Détectés", padding="10")
        list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview pour les problèmes de registre
        columns = ('Type', 'Clé', 'Valeur', 'Problème')
        self.registry_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configuration des colonnes
        self.registry_tree.heading('Type', text='Type')
        self.registry_tree.heading('Clé', text='Clé de Registre')
        self.registry_tree.heading('Valeur', text='Valeur')
        self.registry_tree.heading('Problème', text='Description du Problème')
        
        self.registry_tree.column('Type', width=100)
        self.registry_tree.column('Clé', width=300)
        self.registry_tree.column('Valeur', width=150)
        self.registry_tree.column('Problème', width=250)
        
        # Scrollbars
        registry_v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.registry_tree.yview)
        registry_h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.registry_tree.xview)
        self.registry_tree.configure(yscrollcommand=registry_v_scrollbar.set, xscrollcommand=registry_h_scrollbar.set)
        
        # Placement
        self.registry_tree.grid(row=0, column=0, sticky='nsew')
        registry_v_scrollbar.grid(row=0, column=1, sticky='ns')
        registry_h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Zone d'informations
        info_frame = ttk.LabelFrame(tab_frame, text="Informations", padding="10")
        info_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        info_frame.columnconfigure(0, weight=1)
        
        self.registry_info_text = tk.Text(info_frame, height=4, wrap='word', font=('Consolas', 9))
        registry_info_scrollbar = ttk.Scrollbar(info_frame, orient='vertical', command=self.registry_info_text.yview)
        self.registry_info_text.configure(yscrollcommand=registry_info_scrollbar.set)
        
        self.registry_info_text.grid(row=0, column=0, sticky='nsew')
        registry_info_scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Message d'information initial
        self.registry_info_text.insert(tk.END, "⚠️ ATTENTION: Le nettoyage du registre peut affecter le système.\n")
        self.registry_info_text.insert(tk.END, "Créez toujours une sauvegarde avant de nettoyer.\n")
        self.registry_info_text.insert(tk.END, "Cliquez sur 'Analyser le Registre' pour commencer.")
    
    def scan_registry_issues(self):
        """Analyse le registre pour détecter les problèmes"""
        def _scan_thread():
            try:
                self.registry_info_text.delete(1.0, tk.END)
                self.registry_info_text.insert(tk.END, "Analyse du registre en cours...\n")
                
                # Vider la liste actuelle
                for item in self.registry_tree.get_children():
                    self.registry_tree.delete(item)
                
                self.registry_issues = []
                
                if platform.system() == "Windows":
                    try:
                        import winreg
                        
                        # Vérifier les clés de désinstallation orphelines
                        self._check_uninstall_keys(winreg)
                        
                        # Vérifier les extensions de fichiers orphelines
                        self._check_file_extensions(winreg)
                        
                        # Vérifier les entrées de démarrage invalides
                        self._check_startup_entries(winreg)
                        
                        # Vérifier les DLL partagées orphelines
                        self._check_shared_dlls(winreg)
                        
                    except ImportError:
                        self.registry_info_text.insert(tk.END, "Module winreg non disponible\n")
                    except Exception as e:
                        self.registry_info_text.insert(tk.END, f"Erreur lors de l'analyse: {e}\n")
                else:
                    self.registry_info_text.insert(tk.END, "Nettoyage de registre disponible uniquement sur Windows\n")
                
                # Mettre à jour l'interface
                self.root.after(0, self._update_registry_display)
                
            except Exception as e:
                self.root.after(0, lambda: self.registry_info_text.insert(tk.END, f"Erreur: {e}\n"))
        
        threading.Thread(target=_scan_thread, daemon=True).start()
    
    def _check_uninstall_keys(self, winreg):
        """Vérifie les clés de désinstallation orphelines"""
        try:
            uninstall_key = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key) as key:
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                uninstall_string, _ = winreg.QueryValueEx(subkey, "UninstallString")
                                if uninstall_string:
                                    # Vérifier si le fichier de désinstallation existe
                                    uninstall_path = uninstall_string.split('"')[1] if '"' in uninstall_string else uninstall_string.split()[0]
                                    if not os.path.exists(uninstall_path):
                                        self.registry_issues.append({
                                            'type': 'Désinstallation',
                                            'key': f"{uninstall_key}\\{subkey_name}",
                                            'value': 'UninstallString',
                                            'problem': 'Fichier de désinstallation introuvable'
                                        })
                            except FileNotFoundError:
                                pass
                        i += 1
                    except OSError:
                        break
        except Exception as e:
            self.registry_info_text.insert(tk.END, f"Erreur vérification désinstallation: {e}\n")
    
    def _check_file_extensions(self, winreg):
        """Vérifie les extensions de fichiers orphelines"""
        try:
            classes_root = winreg.HKEY_CLASSES_ROOT
            i = 0
            while True:
                try:
                    ext_name = winreg.EnumKey(classes_root, i)
                    if ext_name.startswith('.'):
                        with winreg.OpenKey(classes_root, ext_name) as ext_key:
                            try:
                                prog_id, _ = winreg.QueryValueEx(ext_key, "")
                                if prog_id:
                                    # Vérifier si le ProgID existe
                                    try:
                                        winreg.OpenKey(classes_root, prog_id)
                                    except FileNotFoundError:
                                        self.registry_issues.append({
                                            'type': 'Extension',
                                            'key': ext_name,
                                            'value': 'ProgID',
                                            'problem': f'ProgID "{prog_id}" introuvable'
                                        })
                            except FileNotFoundError:
                                pass
                    i += 1
                    if i > 100:  # Limiter pour éviter une analyse trop longue
                        break
                except OSError:
                    break
        except Exception as e:
            self.registry_info_text.insert(tk.END, f"Erreur vérification extensions: {e}\n")
    
    def _check_startup_entries(self, winreg):
        """Vérifie les entrées de démarrage invalides"""
        try:
            startup_keys = [
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
            ]
            
            for startup_key in startup_keys:
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key) as key:
                        i = 0
                        while True:
                            try:
                                name, command, _ = winreg.EnumValue(key, i)
                                # Extraire le chemin du fichier
                                if command:
                                    file_path = command.split('"')[1] if '"' in command else command.split()[0]
                                    if not os.path.exists(file_path):
                                        self.registry_issues.append({
                                            'type': 'Démarrage',
                                            'key': f"HKCU\\{startup_key}",
                                            'value': name,
                                            'problem': 'Fichier de démarrage introuvable'
                                        })
                                i += 1
                            except OSError:
                                break
                except FileNotFoundError:
                    pass
        except Exception as e:
            self.registry_info_text.insert(tk.END, f"Erreur vérification démarrage: {e}\n")
    
    def _check_shared_dlls(self, winreg):
        """Vérifie les DLL partagées orphelines"""
        try:
            shared_dlls_key = r"Software\Microsoft\Windows\CurrentVersion\SharedDLLs"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, shared_dlls_key) as key:
                i = 0
                while True:
                    try:
                        dll_path, count, _ = winreg.EnumValue(key, i)
                        if not os.path.exists(dll_path):
                            self.registry_issues.append({
                                'type': 'DLL Partagée',
                                'key': shared_dlls_key,
                                'value': dll_path,
                                'problem': 'DLL introuvable sur le disque'
                            })
                        i += 1
                        if i > 50:  # Limiter pour éviter une analyse trop longue
                            break
                    except OSError:
                        break
        except Exception as e:
            self.registry_info_text.insert(tk.END, f"Erreur vérification DLL: {e}\n")
    
    def _update_registry_display(self):
        """Met à jour l'affichage des problèmes de registre"""
        try:
            # Vider la liste
            for item in self.registry_tree.get_children():
                self.registry_tree.delete(item)
            
            # Ajouter les problèmes
            for issue in self.registry_issues:
                self.registry_tree.insert('', 'end', values=(
                    issue['type'],
                    issue['key'][:60] + '...' if len(issue['key']) > 60 else issue['key'],
                    issue['value'][:30] + '...' if len(issue['value']) > 30 else issue['value'],
                    issue['problem']
                ))
            
            # Mettre à jour les informations
            self.registry_info_text.delete(1.0, tk.END)
            if self.registry_issues:
                self.registry_info_text.insert(tk.END, f"Trouvé {len(self.registry_issues)} problèmes de registre.\n")
                self.registry_info_text.insert(tk.END, "⚠️ Créez une sauvegarde avant de nettoyer.")
                self.clean_registry_btn.config(state='normal')
            else:
                self.registry_info_text.insert(tk.END, "Aucun problème de registre détecté.\n")
                self.registry_info_text.insert(tk.END, "Votre registre semble être en bon état.")
                self.clean_registry_btn.config(state='disabled')
            
        except Exception as e:
            self.registry_info_text.insert(tk.END, f"Erreur d'affichage: {e}\n")
    
    def create_registry_backup(self):
        """Crée une sauvegarde du registre"""
        try:
            # Créer le dossier de sauvegarde s'il n'existe pas
            os.makedirs(self.backup_folder, exist_ok=True)
            
            # Nom du fichier de sauvegarde avec timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_folder, f"registry_backup_{timestamp}.reg")
            
            if platform.system() == "Windows":
                # Utiliser regedit pour exporter le registre
                result = subprocess.run([
                    'regedit', '/e', backup_file, 'HKEY_LOCAL_MACHINE\\SOFTWARE'
                ], capture_output=True)
                
                if result.returncode == 0:
                    messagebox.showinfo("Sauvegarde Créée", 
                                       f"Sauvegarde du registre créée avec succès:\n{backup_file}")
                    self.registry_info_text.delete(1.0, tk.END)
                    self.registry_info_text.insert(tk.END, f"Sauvegarde créée: {backup_file}")
                else:
                    messagebox.showerror("Erreur", "Impossible de créer la sauvegarde du registre.")
            else:
                messagebox.showinfo("Information", "Sauvegarde de registre disponible uniquement sur Windows.")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création de la sauvegarde: {e}")
    
    def restore_registry_backup(self):
        """Restaure une sauvegarde du registre"""
        try:
            if not os.path.exists(self.backup_folder):
                messagebox.showwarning("Aucune Sauvegarde", "Aucun dossier de sauvegarde trouvé.")
                return
            
            # Lister les fichiers de sauvegarde
            backup_files = [f for f in os.listdir(self.backup_folder) if f.endswith('.reg')]
            
            if not backup_files:
                messagebox.showwarning("Aucune Sauvegarde", "Aucune sauvegarde trouvée.")
                return
            
            # Sélectionner le fichier de sauvegarde
            backup_file = filedialog.askopenfilename(
                title="Sélectionner une sauvegarde à restaurer",
                initialdir=self.backup_folder,
                filetypes=[("Fichiers de registre", "*.reg")]
            )
            
            if backup_file:
                if messagebox.askyesno("Confirmation", 
                                      "Êtes-vous sûr de vouloir restaurer cette sauvegarde?\n"
                                      "Cette opération peut affecter le système."):
                    messagebox.showinfo("Information", 
                                       "Fonctionnalité de restauration en cours de développement.\n"
                                       "Pour restaurer, double-cliquez sur le fichier .reg sélectionné.")
                    
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la restauration: {e}")
    
    def clean_registry_issues(self):
        """Nettoie les problèmes de registre détectés"""
        if not self.registry_issues:
            messagebox.showwarning("Aucun Problème", "Aucun problème de registre à nettoyer.")
            return
        
        if messagebox.askyesno("Confirmation", 
                              f"Êtes-vous sûr de vouloir nettoyer {len(self.registry_issues)} problèmes?\n"
                              "Cette opération est irréversible sans sauvegarde."):
            messagebox.showinfo("Information", 
                               "Fonctionnalité de nettoyage en cours de développement.\n"
                               "Pour des raisons de sécurité, le nettoyage automatique n'est pas encore activé.\n"
                               "Utilisez les outils système Windows ou un logiciel spécialisé.")
    
    def create_service_manager_tab(self):
        """Crée l'onglet de gestion des services Windows"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="⚙️ Services")
        
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(2, weight=1)
        
        # Titre
        title_label = ttk.Label(tab_frame, text="Gestionnaire de Services Windows", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Frame pour les contrôles
        controls_frame = ttk.Frame(tab_frame)
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Boutons de contrôle
        refresh_services_btn = ttk.Button(controls_frame, text="🔄 Actualiser", 
                                         command=self.refresh_services_list)
        refresh_services_btn.pack(side='left', padx=(0, 5))
        
        self.start_service_btn = ttk.Button(controls_frame, text="▶️ Démarrer", 
                                           command=self.start_selected_service, state='disabled')
        self.start_service_btn.pack(side='left', padx=5)
        
        self.stop_service_btn = ttk.Button(controls_frame, text="⏹️ Arrêter", 
                                          command=self.stop_selected_service, state='disabled')
        self.stop_service_btn.pack(side='left', padx=5)
        
        self.restart_service_btn = ttk.Button(controls_frame, text="🔄 Redémarrer", 
                                             command=self.restart_selected_service, state='disabled')
        self.restart_service_btn.pack(side='left', padx=5)
        
        # Frame pour le filtre
        filter_frame = ttk.Frame(controls_frame)
        filter_frame.pack(side='right')
        
        ttk.Label(filter_frame, text="Filtre:").pack(side='left', padx=(0, 5))
        self.service_filter_var = tk.StringVar()
        self.service_filter_var.trace('w', self.filter_services)
        filter_entry = ttk.Entry(filter_frame, textvariable=self.service_filter_var, width=20)
        filter_entry.pack(side='left')
        
        # Frame pour la liste des services
        list_frame = ttk.LabelFrame(tab_frame, text="Services Windows", padding="10")
        list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview pour les services
        columns = ('Nom', 'Nom d\'affichage', 'État', 'Type de démarrage', 'Description')
        self.services_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configuration des colonnes
        self.services_tree.heading('Nom', text='Nom du Service')
        self.services_tree.heading('Nom d\'affichage', text='Nom d\'Affichage')
        self.services_tree.heading('État', text='État')
        self.services_tree.heading('Type de démarrage', text='Type de Démarrage')
        self.services_tree.heading('Description', text='Description')
        
        self.services_tree.column('Nom', width=150)
        self.services_tree.column('Nom d\'affichage', width=200)
        self.services_tree.column('État', width=100)
        self.services_tree.column('Type de démarrage', width=120)
        self.services_tree.column('Description', width=300)
        
        # Bind pour la sélection
        self.services_tree.bind('<<TreeviewSelect>>', self.on_service_select)
        
        # Scrollbars
        services_v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.services_tree.yview)
        services_h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.services_tree.xview)
        self.services_tree.configure(yscrollcommand=services_v_scrollbar.set, xscrollcommand=services_h_scrollbar.set)
        
        # Placement
        self.services_tree.grid(row=0, column=0, sticky='nsew')
        services_v_scrollbar.grid(row=0, column=1, sticky='ns')
        services_h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Zone d'informations
        info_frame = ttk.LabelFrame(tab_frame, text="Informations du Service", padding="10")
        info_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        info_frame.columnconfigure(0, weight=1)
        
        self.service_info_text = tk.Text(info_frame, height=4, wrap='word', font=('Consolas', 9))
        service_info_scrollbar = ttk.Scrollbar(info_frame, orient='vertical', command=self.service_info_text.yview)
        self.service_info_text.configure(yscrollcommand=service_info_scrollbar.set)
        
        self.service_info_text.grid(row=0, column=0, sticky='nsew')
        service_info_scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Message d'information initial
        self.service_info_text.insert(tk.END, "⚠️ ATTENTION: La modification des services peut affecter le système.\n")
        self.service_info_text.insert(tk.END, "Soyez prudent lors de l'arrêt ou du démarrage des services système.\n")
        self.service_info_text.insert(tk.END, "Cliquez sur 'Actualiser' pour charger la liste des services.")
        
        # Charger les services au démarrage
        self.refresh_services_list()
    
    def refresh_services_list(self):
        """Actualise la liste des services Windows"""
        def _refresh_thread():
            try:
                self.service_info_text.delete(1.0, tk.END)
                self.service_info_text.insert(tk.END, "Chargement des services...\n")
                
                # Vider la liste actuelle
                for item in self.services_tree.get_children():
                    self.services_tree.delete(item)
                
                self.services_list = []
                
                if platform.system() == "Windows":
                    try:
                        # Utiliser psutil pour obtenir les services
                        for service in psutil.win_service_iter():
                            try:
                                service_info = service.as_dict()
                                self.services_list.append({
                                    'name': service_info.get('name', 'N/A'),
                                    'display_name': service_info.get('display_name', 'N/A'),
                                    'status': service_info.get('status', 'N/A'),
                                    'start_type': service_info.get('start_type', 'N/A'),
                                    'description': service_info.get('description', 'Aucune description disponible')[:100]
                                })
                            except Exception:
                                continue
                        
                        # Trier par nom d'affichage
                        self.services_list.sort(key=lambda x: x['display_name'].lower())
                        
                    except Exception as e:
                        self.root.after(0, lambda: self.service_info_text.insert(tk.END, f"Erreur lors du chargement: {e}\n"))
                        return
                else:
                    self.root.after(0, lambda: self.service_info_text.insert(tk.END, "Gestion des services disponible uniquement sur Windows\n"))
                    return
                
                # Mettre à jour l'interface
                self.root.after(0, self._update_services_display)
                
            except Exception as e:
                self.root.after(0, lambda: self.service_info_text.insert(tk.END, f"Erreur: {e}\n"))
        
        threading.Thread(target=_refresh_thread, daemon=True).start()
    
    def _update_services_display(self):
        """Met à jour l'affichage des services"""
        try:
            # Vider la liste
            for item in self.services_tree.get_children():
                self.services_tree.delete(item)
            
            # Appliquer le filtre si nécessaire
            filter_text = self.service_filter_var.get().lower()
            if filter_text:
                self.filtered_services = [
                    service for service in self.services_list
                    if filter_text in service['name'].lower() or 
                       filter_text in service['display_name'].lower() or
                       filter_text in service['description'].lower()
                ]
            else:
                self.filtered_services = self.services_list.copy()
            
            # Ajouter les services filtrés
            for service in self.filtered_services:
                # Couleur selon l'état
                status = service['status']
                tags = ()
                if status == 'running':
                    tags = ('running',)
                elif status == 'stopped':
                    tags = ('stopped',)
                
                self.services_tree.insert('', 'end', values=(
                    service['name'],
                    service['display_name'][:40] + '...' if len(service['display_name']) > 40 else service['display_name'],
                    status.title(),
                    service['start_type'].replace('_', ' ').title(),
                    service['description']
                ), tags=tags)
            
            # Configuration des couleurs
            self.services_tree.tag_configure('running', foreground='green')
            self.services_tree.tag_configure('stopped', foreground='red')
            
            # Mettre à jour les informations
            self.service_info_text.delete(1.0, tk.END)
            self.service_info_text.insert(tk.END, f"Trouvé {len(self.filtered_services)} services.\n")
            if len(self.filtered_services) != len(self.services_list):
                self.service_info_text.insert(tk.END, f"({len(self.services_list)} services au total)\n")
            self.service_info_text.insert(tk.END, "Sélectionnez un service pour voir les options de contrôle.")
            
        except Exception as e:
            self.service_info_text.insert(tk.END, f"Erreur d'affichage: {e}\n")
    
    def filter_services(self, *args):
        """Filtre les services selon le texte saisi"""
        if hasattr(self, 'services_list') and self.services_list:
            self._update_services_display()
    
    def on_service_select(self, event):
        """Gère la sélection d'un service"""
        selection = self.services_tree.selection()
        if selection:
            item = self.services_tree.item(selection[0])
            service_name = item['values'][0]
            service_display_name = item['values'][1]
            service_status = item['values'][2].lower()
            
            # Activer/désactiver les boutons selon l'état
            if service_status == 'running':
                self.start_service_btn.config(state='disabled')
                self.stop_service_btn.config(state='normal')
                self.restart_service_btn.config(state='normal')
            elif service_status == 'stopped':
                self.start_service_btn.config(state='normal')
                self.stop_service_btn.config(state='disabled')
                self.restart_service_btn.config(state='disabled')
            else:
                self.start_service_btn.config(state='disabled')
                self.stop_service_btn.config(state='disabled')
                self.restart_service_btn.config(state='disabled')
            
            # Afficher les informations du service
            self.service_info_text.delete(1.0, tk.END)
            self.service_info_text.insert(tk.END, f"Service sélectionné: {service_display_name}\n")
            self.service_info_text.insert(tk.END, f"Nom technique: {service_name}\n")
            self.service_info_text.insert(tk.END, f"État actuel: {service_status.title()}\n")
            
            # Trouver la description complète
            for service in self.filtered_services:
                if service['name'] == service_name:
                    self.service_info_text.insert(tk.END, f"Description: {service['description']}")
                    break
        else:
            # Aucune sélection
            self.start_service_btn.config(state='disabled')
            self.stop_service_btn.config(state='disabled')
            self.restart_service_btn.config(state='disabled')
    
    def start_selected_service(self):
        """Démarre le service sélectionné"""
        selection = self.services_tree.selection()
        if not selection:
            return
        
        item = self.services_tree.item(selection[0])
        service_name = item['values'][0]
        service_display_name = item['values'][1]
        
        if messagebox.askyesno("Confirmation", 
                              f"Êtes-vous sûr de vouloir démarrer le service:\n{service_display_name}?"):
            messagebox.showinfo("Information", 
                               "Fonctionnalité de contrôle des services en cours de développement.\n"
                               "Pour des raisons de sécurité, utilisez les outils système Windows:\n"
                               "- Services.msc\n"
                               "- Gestionnaire des tâches > Services")
    
    def stop_selected_service(self):
        """Arrête le service sélectionné"""
        selection = self.services_tree.selection()
        if not selection:
            return
        
        item = self.services_tree.item(selection[0])
        service_name = item['values'][0]
        service_display_name = item['values'][1]
        
        if messagebox.askyesno("Confirmation", 
                              f"Êtes-vous sûr de vouloir arrêter le service:\n{service_display_name}?\n\n"
                              "⚠️ L'arrêt de certains services peut affecter le système."):
            messagebox.showinfo("Information", 
                               "Fonctionnalité de contrôle des services en cours de développement.\n"
                               "Pour des raisons de sécurité, utilisez les outils système Windows:\n"
                               "- Services.msc\n"
                               "- Gestionnaire des tâches > Services")
    
    def restart_selected_service(self):
        """Redémarre le service sélectionné"""
        selection = self.services_tree.selection()
        if not selection:
            return
        
        item = self.services_tree.item(selection[0])
        service_name = item['values'][0]
        service_display_name = item['values'][1]
        
        if messagebox.askyesno("Confirmation", 
                              f"Êtes-vous sûr de vouloir redémarrer le service:\n{service_display_name}?"):
            messagebox.showinfo("Information", 
                               "Fonctionnalité de contrôle des services en cours de développement.\n"
                               "Pour des raisons de sécurité, utilisez les outils système Windows:\n"
                               "- Services.msc\n"
                               "- Gestionnaire des tâches > Services")
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

def main():
    """Fonction principale"""
    app = PCOptimizerSuite()
    app.run()

if __name__ == "__main__":
    main()