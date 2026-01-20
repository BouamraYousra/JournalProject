import pymysql
from pymongo import MongoClient
from tkinter import messagebox


class DatabaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._instance.mysql = None
            cls._instance.mongo = None
            cls._instance._init_connections()
        return cls._instance

    def _init_connections(self):
        try:
            client = MongoClient(
                "mongodb://localhost:27017", serverSelectionTimeoutMS=2000
            )
            self.mongo = client["journal"]
            client.admin.command("ping")
        except Exception as e:
            messagebox.showerror(
                "Database Error", f"MongoDB connection failed: {e}"
            )

        try:
            self.mysql = pymysql.connect(
                host="localhost",
                user="root",
                password="root",
                database="journal_db",
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
        except Exception as e:
            messagebox.showerror(
                "Database Error", f"MySQL Connection failed: {e}"
            )

    def get_all_titles(self):
        if not self.mysql:
            return []
        try:
            self.mysql.ping(reconnect=True)
            with self.mysql.cursor() as cur:
                query = "SELECT id, title FROM entries"
                cur.execute(query)
                return cur.fetchall()

        except Exception:
            return []

    def save_metadata(self, meta: dict):
        self.mysql.ping(reconnect=True)
        with self.mysql.cursor() as cur:
            if meta.get("id"):
                query = (
                    "UPDATE entries SET title=%s, type=%s, password_hash=%s, "
                    "file_path=%s WHERE id=%s"
                )
                values = (
                    meta["title"],
                    meta["type"],
                    meta["password_hash"],
                    meta["file_path"],
                    meta["id"],
                )
                cur.execute(query, values)
                return meta["id"]
            else:
                query = (
                        "INSERT INTO entries (title,"
                        " type,password_hash, file_path)"
                        " VALUES (%s, %s, %s, %s)"
                    )

                values = (
                    meta["title"],
                    meta["type"],
                    meta["password_hash"],
                    meta["file_path"],
                )
                cur.execute(query, values)
                return cur.lastrowid

    def save_content(self, note_id, content: str, translations: dict = None):
        if self.mongo is not None:
            self.mongo.entries.update_one(
                {"_id": str(note_id)},
                {"$set": {
                    "body": content,
                    "translations": translations or {}
                    }},
                upsert=True,
            )

    def get_full_note(self, note_id):
        if self.mongo is None:
            return None
        return self.mongo.entries.find_one({"_id": str(note_id)})

    def delete_note(self, note_id):
        if self.mysql:
            try:
                self.mysql.ping(reconnect=True)
                with self.mysql.cursor() as cur:
                    cur.execute(
                        "DELETE FROM entries WHERE id = %s", (note_id,)
                    )
            except Exception as e:
                print(f"SQL Delete Error: {e}")

        if self.mongo is not None:
            self.mongo.entries.delete_one({"_id": str(note_id)})
