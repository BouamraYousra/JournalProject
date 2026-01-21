# 📓 Journal Management System

A sophisticated Python-based journal application with multilingual support, dual-database architecture, and advanced file handling capabilities. Serves as a mini project for the FTP Training

## ✨ Features

- **📝 Rich Journaling**: Create, edit, and organize journal entries with RTL language support
- **🌐 Multilingual**: Automatic translation using Google Translate API (Arabic, Spanish, French, etc.)
- **🔒 Security**: Password protection with SHA-256 hashing for private entries
- **💾 Hybrid Storage**: MySQL for metadata + MongoDB for content + optional file linking
- **📁 File Operations**: Import/export to TXT, CSV formats with structured metadata
- **🔄 Real-time Sync**: File-linked entries auto-synchronize with physical files
- **🧪 Comprehensive Testing**: Full test suite with pytest (15+ tests)

## 🏗️ Architecture
JournalProject/ <br>
├── app/<br>
│ ├── ui/ # CustomTkinter GUI components<br>
│ │ ├── main_window.py # Main application window <br>
│ │ └── editor_view.py # Entry editor component <br>
│ ├── models/ # Object-oriented design patterns<br>
│ │ ├── base.py # Abstract Base Entry class<br>
│ │ ├── concrete.py # TextEntry, FileEntry implementations <br>
│ │ └── features.py # Decorators: SecretEntry, MultilingualEntry <br>
│ └── services/ # Business logic and data handling <br>
│ ├── database.py # MySQL + MongoDB hybrid database<br>
│ ├── storage.py # StorageFactory (Factory pattern) <br>
│ └── file_manager.py # TXT/CSV import/export operations <br>
├── tests/ # Comprehensive test suite <br>
│ ├── test_logic.py # Model and feature tests<br>
│ └── test_files.py # File operation tests <br>
├── requirements.txt # Dependencies <br>
├── main.py # Application entry point <br>
└── README.md # This file<br>



## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server
- MongoDB
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/[your-username]/JournalProject.git
cd JournalProject ```

### Install dependencies

pip install -r requirements.txt
exit 0

### Database Setup

MySQL:
sql

CREATE DATABASE journal_db;
USE journal_db;

CREATE TABLE entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type ENUM('TEXT', 'FILE') DEFAULT 'TEXT',
    password_hash VARCHAR(64),
    file_path VARCHAR(500)
);

MongoDB:
bash

# MongoDB will create collections automatically
# Ensure MongoDB service is running
sudo systemctl start mongod  # Linux
# or start MongoDB service on Windows/macOS

    Update database credentials in app/services/database.py if needed:

python

# Update with your credentials
self.mysql = pymysql.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="journal_db"
)

    Run the application

bash

python main.py

📚 Course Alignment
Part 3: File & Database Handling ✅

    Multi-format file operations (TXT, CSV with JSON metadata)

    Structured file parsing and validation

    Hybrid database architecture (SQL + NoSQL)

    Error handling and data persistence

    File system synchronization

Part 4: Structured, Modular & OOP ✅

    Abstract Base Classes with concrete implementations

    Design Patterns: Factory, Decorator, Singleton, Strategy

    Clean separation of concerns (UI, Models, Services)

    Inheritance, composition, polymorphism

    Modular and extensible architecture

Part 5: Collaboration & Best Practices ✅

    Comprehensive unit and integration testing (pytest)

    Git workflow with feature branches and pull requests

    Code quality enforcement (flake8, type hints, docstrings)

    Error handling throughout the application

    Professional development practices

🔧 Design Patterns Implemented
Pattern	Implementation	Purpose
Factory	StorageFactory	Create different entry types (TEXT, FILE)
Decorator	EntryFeature → SecretEntry, MultilingualEntry	Add features without modifying base classes
Singleton	DatabaseService	Single instance for database connections
Strategy	Different storage backends	Interchangeable storage methods
Abstract Factory	Entry creation system	Family of related objects
🧪 Testing

Run the comprehensive test suite:
bash

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_logic.py -v
pytest tests/test_files.py -v

# Run with coverage report
pytest --cov=app tests/

# Code quality check
flake8 app/

Test Coverage:

    Model creation and inheritance

    File operations (import/export)

    Database integration

    Security features

    Translation system

    Error handling scenarios

🌐 Multilingual & RTL Support
Supported Languages:

    Right-to-Left: Arabic (with proper character reshaping)

    Left-to-Right: English, Spanish, French, German, etc.

    Automatic Translation: Google Translate API integration

    Translation Caching: Results stored in MongoDB for performance

Arabic Support Details:

    Uses arabic-reshaper for proper character connection

    Uses python-bidi for correct text direction

    Preserves RTL rendering in GUI components

    Handles mixed-direction text correctly

🔒 Security Features

    Password Protection: Individual entries can be password-protected

    SHA-256 Hashing: Passwords are never stored in plaintext

    Locked Content: Protected entries display as "[LOCKED]" until verified

    Secure Storage: Database connections use proper authentication

    File Permissions: Respects OS-level file system permissions

📁 File Operations
Supported Formats:

    TXT: Structured format with embedded JSON metadata section

    CSV: Single-row format with translations as JSON column

    Direct File Linking: .txt, .csv, .md, .json, .log files

Export Format Example (TXT):
text

--- JOURNAL ENTRY ---
TITLE: My Journal Entry
--------------------
CONTENT:
This is the main content of my journal entry.
--------------------
METADATA_TRANSLATIONS:
{"es": "Este es el contenido principal de mi entrada de diario.", "ar": "هذا هو المحتوى الرئيسي لإدخال دفتر اليومية الخاص بي."}

Import/Export Workflow:

    Create entry in application

    Export to TXT or CSV format

    Edit externally if needed

    Import back with all metadata preserved

    Optional: Link to file for auto-synchronization

🗄️ Database Architecture
MySQL (Relational - Metadata)
sql

CREATE TABLE entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type ENUM('TEXT', 'FILE') DEFAULT 'TEXT',
    password_hash VARCHAR(64),
    file_path VARCHAR(500)
);

MongoDB (Document - Content)
json

{
  "_id": "123",  // Matches MySQL ID
  "body": "Journal content text here...",
  "translations": {
    "es": "Texto del contenido del diario aquí...",
    "fr": "Texte de contenu du journal ici...",
    "ar": "نص محتوى اليومية هنا..."
  },
  "created_at": "2025-01-20T10:30:00Z",
  "updated_at": "2025-01-20T11:45:00Z"
}

Hybrid Approach Benefits:

    Fast metadata queries using MySQL relational indexes

    Flexible content storage using MongoDB document model

    Schema evolution without complex migrations

    Data redundancy and backup options

🐛 Troubleshooting
Issue	Solution
MySQL connection failed	Verify credentials in database.py, ensure MySQL service is running
MongoDB connection failed	Start MongoDB service: sudo systemctl start mongod (Linux)
Arabic text not rendering properly	Install required packages: pip install arabic-reshaper python-bidi
Translation API errors	Check internet connection, verify Google Translate API is accessible
File permission errors	Check write permissions in target directory
GUI not launching	Ensure CustomTkinter is installed: pip install customtkinter
Test failures	Ensure all dependencies are installed and databases are running
🤝 Contributing

    Fork the repository

    Create a feature branch: git checkout -b feature/amazing-feature

    Commit changes: git commit -m 'Add amazing feature'

    Push to branch: git push origin feature/amazing-feature

    Submit a Pull Request

Development Workflow:
bash

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest flake8

# Run tests before committing
pytest tests/ -v
flake8 app/

# Commit changes
git add .
git commit -m "Description of changes"
git push origin branch-name

👥 made by 

    [BOUAMRA Yousra]
Course: Programming Fundamentals & Techniques
Academic Year: 2024/2025
Institution: [ESI SBA]
Submission Date: January 2026

Developed as part of the PhD Programming Fundamentals & Techniques Course - Demonstrating integration of File Handling, Object-Oriented Programming, and Software Engineering Best Practices
