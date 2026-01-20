import hashlib
from .base import BaseEntry
from deep_translator import GoogleTranslator

class EntryFeature(BaseEntry):
    def __init__(self, entry: BaseEntry):
        self.entry = entry
    def get_content(self): return self.entry.get_content()
    def edit_content(self, text): self.entry.edit_content(text)
    def metadata(self): return self.entry.metadata()

class SecretEntry(EntryFeature):
    def __init__(self, entry, password: str):
        super().__init__(entry)
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.locked = True # Notes start locked

    def verify(self, password: str) -> bool:
        if hashlib.sha256(password.encode()).hexdigest() == self.password_hash:
            self.locked = False
            return True
        return False

    def get_content(self):
        if self.locked: return "******** [LOCKED] ********"
        return self.entry.get_content()

    def metadata(self):
        data = super().metadata()
        data["encrypted"] = True
        return data

class MultilingualEntry(EntryFeature):
    def __init__(self, entry):
        super().__init__(entry)
        self.translations = {}

    def add_language(self, lang_code: str):
        content = self.get_content()
        try:
            translated = GoogleTranslator(source='auto', target=lang_code).translate(content)
            self.translations[lang_code] = translated
            return True
        except: return False