import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Précompile les motifs suspects
SUSPICIOUS_PATTERNS = [
    (re.compile(r'/\*[^*]*$'), "Commentaire CSS probablement non fermé"),
    (re.compile(r'content:\s*/'), "Propriété content: contient / sans guillemets"),
    (re.compile(r'content:\s*[^\";\']+$'), "content: sans guillemets ou fin de ligne incorrecte"),
    (re.compile(r'url\([^\'\")]*$'), "url( sans fermeture de parenthèse ou guillemets"),
    (re.compile(r'^/\*.*$'), "Début de commentaire non fermé"),
    (re.compile(r'[\s;]content:\s*/;'), "content: /; suspect"),
]

IGNORED_DIRS = {"node_modules", "build", ".git", "__pycache__"}

class CSSCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Détecteur d'erreurs CSS")
        self.root.geometry("920x550")
        self.project_dir = None

        # Frame principal avec scrollbar
        table_frame = tk.Frame(root)
        table_frame.pack(expand=True, fill="both", pady=(5, 0))

        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Fichier", "Ligne", "Erreur"),
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse"
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("Fichier", text="Fichier")
        self.tree.heading("Ligne", text="Ligne")
        self.tree.heading("Erreur", text="Erreur détectée")
        self.tree.column("Fichier", width=350)
        self.tree.column("Ligne", width=60, anchor="center")
        self.tree.column("Erreur", width=480)
        self.tree.pack(expand=True, fill="both")

        # Menu contextuel pour copier le chemin + ligne
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Copier chemin complet", command=self.copy_selected_path)

        self.status_label = tk.Label(root, text="Aucun dossier sélectionné", anchor="w")
        self.status_label.pack(fill="x")

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.open_btn = tk.Button(button_frame, text="📁 Choisir un dossier", command=self.choose_folder)
        self.open_btn.pack(side="left", padx=10)

        self.scan_btn = tk.Button(button_frame, text="📂 Scanner le dossier", command=self.scan_files, state="disabled")
        self.scan_btn.pack(side="left")

    def show_context_menu(self, event):
        # Sélectionne l'item sous le curseur avant d'afficher menu
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_selected_path(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        fichier, ligne, erreur = item['values']
        chemin_complet = f"{fichier} : ligne {ligne}"
        self.root.clipboard_clear()
        self.root.clipboard_append(chemin_complet)
        messagebox.showinfo("Copié", f"Chemin copié dans le presse-papier :\n{chemin_complet}")

    def choose_folder(self):
        folder = filedialog.askdirectory(title="Sélectionne ton dossier React")
        if folder:
            self.project_dir = folder
            self.status_label.config(text=f"Dossier sélectionné : {folder}")
            self.scan_btn.config(state="normal")
            self.tree.delete(*self.tree.get_children())

    def log_error(self, file_path, line_num, message):
        rel_path = os.path.relpath(file_path, self.project_dir)
        self.tree.insert("", "end", values=(rel_path, line_num, message))

    def scan_files(self):
        if not self.project_dir:
            messagebox.showwarning("Aucun dossier", "Veuillez d'abord sélectionner un dossier.")
            return

        self.tree.delete(*self.tree.get_children())
        self.status_label.config(text="🔎 Analyse en cours...")
        self.root.update_idletasks()

        total_css = 0
        total_errors = 0

        for dirpath, dirnames, filenames in os.walk(self.project_dir):
            dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]

            for file in filenames:
                if not file.endswith(".css"):
                    continue

                total_css += 1
                full_path = os.path.join(dirpath, file)

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        for idx, line in enumerate(f):
                            for pattern, desc in SUSPICIOUS_PATTERNS:
                                if pattern.search(line.strip()):
                                    total_errors += 1
                                    self.log_error(full_path, idx + 1, desc)
                except Exception as e:
                    self.log_error(full_path, "-", f"Erreur de lecture : {e}")

        self.status_label.config(
            text=f"✅ {total_css} fichiers CSS scannés | ⚠️ {total_errors} erreurs détectées"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = CSSCheckerApp(root)
    root.mainloop()
