import os
from .base import BaseEntry

class TextEntry(BaseEntry):
    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body

    def get_content(self):
        return self.body

    def edit_content(self, text):
        self.body = text

    def metadata(self):
        return {
            "title": self.title,
            "type": "TEXT"
        }

class FileEntry(BaseEntry):
    def __init__(self, path: str):
        self.path = path
        # Restriction: Only allow text-based "suited" files
        allowed = ('.txt', '.csv', '.md', '.json', '.log')
        if not path.lower().endswith(allowed):
            raise ValueError(f"Unsupported file type! Use: {allowed}")
            
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            self.body = f.read()

    def get_content(self):
        return self.body

    def edit_content(self, text):
        self.body = text
        # Part 3: Live Sync to Physical File
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(text)

    def metadata(self):
        return {
            "type": "FILE",
            "path": self.path,
            "title": os.path.basename(self.path)
        }