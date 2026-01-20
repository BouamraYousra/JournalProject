import customtkinter as ctk


class EditorView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_entry = ctk.CTkEntry(
            self, placeholder_text="Entry title"
        )
        self.title_entry.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.textbox = ctk.CTkTextbox(self)
        self.textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.save_btn = ctk.CTkButton(self, text="💾 Save")
        self.save_btn.grid(row=2, column=0, pady=10)
