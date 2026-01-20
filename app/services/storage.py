from app.models.concrete import TextEntry, FileEntry
from app.models.features import SecretEntry


class StorageFactory:

    @staticmethod
    def create(entry_type: str, data: dict):
        if entry_type == "TEXT":
            return TextEntry(**data)
        if entry_type == "FILE":
            return FileEntry(**data)
        raise ValueError("Unknown entry type")

    @staticmethod
    def secure(entry, password: str):
        return SecretEntry(entry, password)
