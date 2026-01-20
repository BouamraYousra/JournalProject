import hashlib
import arabic_reshaper
from bidi.algorithm import get_display
import customtkinter as ctk
from tkinter import messagebox, simpledialog, filedialog
from .editor_view import EditorView
from app.services.database import DatabaseService
from app.services.storage import StorageFactory
from app.services.file_manager import FileManager
from app.models.features import MultilingualEntry

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Journal Project - RTL & Sync Fixed")
        self.geometry("1200 text_color")
        self.geometry("1200x850")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.db = DatabaseService()
        self.current_entry = None
        self.current_note_id = None 
        self.temp_pwd_hash = None 
        self.current_file_path = None 

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        ctk.CTkLabel(self.sidebar, text="📓 My Journal", font=("Arial", 22, "bold")).pack(pady=30)
        ctk.CTkButton(self.sidebar, text="📋 All Notes", command=self.show_list_page).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="➕ Add Note", command=self.show_add_page).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📥 Import & Link", fg_color="#27ae60", command=self.import_note).pack(pady=10, padx=20)

        # --- Main Container ---
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.create_list_page()
        self.create_editor_page()
        self.show_list_page()

    def create_list_page(self):
        self.list_page = ctk.CTkFrame(self.container, fg_color="transparent")
        search_frame = ctk.CTkFrame(self.list_page, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 20))
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search Title...", height=45)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.refresh_list_ui)

        self.scroll_frame = ctk.CTkScrollableFrame(self.list_page, label_text="Notes Collection")
        self.scroll_frame.pack(fill="both", expand=True)

    def create_editor_page(self):
        self.editor_page = ctk.CTkFrame(self.container, fg_color="transparent")
        self.editor_view = EditorView(self.editor_page)
        self.editor_view.pack(fill="both", expand=True)
        self.editor_view.save_btn.configure(command=self.save_flow, text="💾 Save & Sync")

        ctk.CTkLabel(self.editor_page, text="Stored Translations:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(15, 0))
        self.trans_box = ctk.CTkTextbox(self.editor_page, height=130, fg_color="#1a1a1a", text_color="#ffffff", font=("Arial", 14))
        self.trans_box.pack(fill="x", pady=(5, 10))

        btn_row = ctk.CTkFrame(self.editor_page, fg_color="transparent")
        btn_row.pack(fill="x", pady=5)
        ctk.CTkButton(btn_row, text="🔒 Security", fg_color="#7e1919", width=90, command=self.add_security).pack(side="left", padx=5)
        ctk.CTkButton(btn_row, text="🌐 Translate", fg_color="#1e3a5f", width=90, command=self.add_translation).pack(side="left", padx=5)
        ctk.CTkButton(btn_row, text="📤 Export", fg_color="#2c3e50", width=90, command=self.export_note).pack(side="left", padx=5)
        ctk.CTkButton(btn_row, text="🗑️ Delete", fg_color="#444444", width=90, command=self.delete_current).pack(side="right", padx=5)

    def show_list_page(self):
        self.current_note_id = None
        self.editor_page.grid_forget()
        self.list_page.grid(row=0, column=0, sticky="nsew")
        self.refresh_list_ui()

    def show_add_page(self):
        self.current_note_id = None
        self.current_file_path = None
        self.temp_pwd_hash = None
        self.current_entry = StorageFactory.create("TEXT", {"title": "", "body": ""})
        self.list_page.grid_forget()
        self.editor_page.grid(row=0, column=0, sticky="nsew")
        self.refresh_editor_ui()

    def refresh_list_ui(self, event=None):
        for widget in self.scroll_frame.winfo_children(): widget.destroy()
        query = self.search_entry.get().lower()
        notes = self.db.get_all_titles() 
        for note in notes:
            if query in note['title'].lower():
                btn = ctk.CTkButton(self.scroll_frame, text=f" {note['title']}", anchor="w", 
                                    height=45, fg_color="#2b2b2b", 
                                    command=lambda nid=note['id']: self.load_note_to_edit(nid))
                btn.pack(fill="x", pady=3)

    def load_note_to_edit(self, note_id):
        self.db.mysql.ping(reconnect=True)
        with self.db.mysql.cursor() as cur:
            cur.execute("SELECT title, password_hash, file_path FROM entries WHERE id = %s", (note_id,))
            record = cur.fetchone()

        if record and record['password_hash']:
            pwd = simpledialog.askstring("Security", f"Enter password:", show="*")
            if not pwd or hashlib.sha256(pwd.encode()).hexdigest() != record['password_hash']:
                messagebox.showerror("Error", "Incorrect Password")
                return
        
        data = self.db.get_full_note(note_id)
        self.current_note_id = note_id
        self.temp_pwd_hash = record['password_hash'] if record else None
        self.current_file_path = record['file_path'] if record else None

        title = record['title'] if record else "Untitled"
        body = data['body'] if data else ""
        self.current_entry = StorageFactory.create("TEXT", {"title": title, "body": body})
        
        if data and "translations" in data:
            self.current_entry = MultilingualEntry(self.current_entry)
            self.current_entry.translations = data["translations"]

        self.list_page.grid_forget()
        self.editor_page.grid(row=0, column=0, sticky="nsew")
        self.refresh_editor_ui()

    def save_flow(self):
        ui_title = self.editor_view.title_entry.get()
        ui_body = self.editor_view.textbox.get("1.0", "end-1c")
        if not ui_title: return

        try:
            # 1. Update Database
            meta = {"id": self.current_note_id, "title": ui_title, "type": "TEXT", 
                    "password_hash": self.temp_pwd_hash, "file_path": self.current_file_path}
            self.current_note_id = self.db.save_metadata(meta)
            
            # 2. Sync UI to Internal Object
            if self.current_entry:
                base_note = self.current_entry.entry if hasattr(self.current_entry, 'entry') else self.current_entry
                base_note.title = ui_title
                self.current_entry.edit_content(ui_body)
                
                # Update existing translations with new content
                if isinstance(self.current_entry, MultilingualEntry):
                    langs = list(self.current_entry.translations.keys())
                    for lang in langs:
                        self.current_entry.add_language(lang)
            
            trans = self.current_entry.translations if isinstance(self.current_entry, MultilingualEntry) else {}
            self.db.save_content(self.current_note_id, ui_body, trans)
            
            if self.current_file_path:
                FileManager.export_to_txt(self.current_file_path, ui_title, ui_body, trans)

            # 3. Final UI Refresh
            self.refresh_editor_ui()
            self.title(f"Journal - Saved {ui_title}")
            
        except Exception as e: 
            messagebox.showerror("Error", f"Save failed: {e}")

    def add_translation(self):
        if not self.current_entry: return
        ui_title = self.editor_view.title_entry.get()
        ui_body = self.editor_view.textbox.get("1.0", "end-1c")
        
        if not isinstance(self.current_entry, MultilingualEntry): 
            self.current_entry = MultilingualEntry(self.current_entry)
        
        lang = simpledialog.askstring("Translate", "Language Code (e.g., ar, fr, es):")
        if lang:
            base_note = self.current_entry.entry if hasattr(self.current_entry, 'entry') else self.current_entry
            base_note.title = ui_title
            self.current_entry.edit_content(ui_body)
            
            if self.current_entry.add_language(lang):
                self.refresh_editor_ui()

    def refresh_editor_ui(self):
        self.editor_view.title_entry.configure(state="normal")
        self.editor_view.textbox.configure(state="normal")
        
        self.editor_view.title_entry.delete(0, 'end')
        self.editor_view.textbox.delete("1.0", 'end')
        self.trans_box.configure(state="normal")
        self.trans_box.delete("1.0", "end")
        
        if self.current_entry:
            base_note = self.current_entry.entry if hasattr(self.current_entry, 'entry') else self.current_entry
            
            self.editor_view.title_entry.insert(0, base_note.title)
            self.editor_view.textbox.insert("1.0", self.current_entry.get_content())
            
            if isinstance(self.current_entry, MultilingualEntry):
                for lang, text in self.current_entry.translations.items():
                    display_text = text
                    
                    # --- ARABIC FIX ---
                    if lang.lower() == 'ar':
                        reshaped_text = arabic_reshaper.reshape(text)
                        display_text = get_display(reshaped_text)
                    
                    self.trans_box.insert("end", f"[{lang.upper()}]\n{display_text}\n\n")
        
        self.trans_box.configure(state="disabled")

    def add_security(self):
        pwd = simpledialog.askstring("Security", "Password:", show="*")
        if pwd: self.temp_pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
        else: self.temp_pwd_hash = None

    def delete_current(self):
        if not self.current_note_id: return
        if messagebox.askyesno("Delete", "Delete this note?"):
            self.db.delete_note(self.current_note_id)
            self.show_list_page()

    def export_note(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if file_path:
            ui_title = self.editor_view.title_entry.get()
            ui_body = self.editor_view.textbox.get("1.0", "end-1c")
            trans = self.current_entry.translations if isinstance(self.current_entry, MultilingualEntry) else {}
            FileManager.export_to_txt(file_path, ui_title, ui_body, trans)
            if messagebox.askyesno("Link", "Link to this file for future auto-updates?"):
                self.current_file_path = file_path
                self.save_flow()

    def import_note(self):
        file_path = filedialog.askopenfilename(filetypes=[("Data files", "*.txt *.csv")])
        if file_path:
            try:
                title, body, trans = FileManager.import_from_file(file_path)
                meta = {"title": title, "type": "TEXT", "password_hash": None, "file_path": file_path}
                new_id = self.db.save_metadata(meta)
                self.db.save_content(new_id, body, trans)
                self.show_list_page()
            except Exception as e: messagebox.showerror("Error", str(e))