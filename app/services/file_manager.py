import csv
import json
import os


class FileManager:
    @staticmethod
    def export_to_txt(filepath, title, body, translations):
        """Saves note and translations into a structured text file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("--- JOURNAL ENTRY ---\n")
                f.write(f"TITLE: {title}\n")
                f.write("-" * 20 + "\n")
                f.write("CONTENT:\n")
                f.write(f"{body}\n")
                f.write("-" * 20 + "\n")
                f.write("METADATA_TRANSLATIONS:\n")
                f.write(
                    json.dumps(translations, ensure_ascii=False)
                )
            return True

        except Exception as e:
            print(f"TXT Export Error: {e}")
            return False

    @staticmethod
    def export_to_csv(filepath, title, body, translations):
        """Saves note and translations into a CSV row."""
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Main_Body", "Translations_JSON"])
                writer.writerow(
                    [
                        title,
                        body,
                        json.dumps(translations, ensure_ascii=False)
                    ]
                )
            return True
        except Exception as e:
            print(f"CSV Export Error: {e}")
            return False

    @staticmethod
    def import_from_file(filepath):
        """returns (title, body, translations_dict)."""
        try:
            if filepath.endswith('.csv'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    row = next(reader)
                    return (
                        row['Title'],
                        row['Main_Body'],
                        json.loads(row['Translations_JSON'])
                    )
            else:  # Handle TXT
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "METADATA_TRANSLATIONS:" in content:
                        parts = content.split("METADATA_TRANSLATIONS:\n")
                        header_body = parts[0]
                        translations = json.loads(parts[1])

                        # Extract title and body from header_body
                        lines = header_body.splitlines()
                        title = lines[1].replace("TITLE: ", "").strip()
                        body_start = header_body.find("CONTENT:\n") + 9
                        body_end = header_body.find(
                            "\n--------------------",
                            body_start
                        )
                        body = header_body[body_start:body_end].strip()
                        return title, body, translations
                    else:
                        # Standard plain text file
                        title = os.path.basename(filepath).split('.')[0]
                        return title, content, {}
        except Exception as e:
            raise Exception(f"File parsing failed: {e}")
