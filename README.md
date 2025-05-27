
<h1 align="center">🚗 DriveTracker</h1>

<p align="center">
  A Python-based desktop application to log and track your drives efficiently.<br>
  Built with <b>Tkinter</b> for GUI and <b>SQLite3</b> for local data storage.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" />
  <img src="https://img.shields.io/badge/GUI-Tkinter-green" />
  <img src="https://img.shields.io/badge/Database-SQLite3-lightgrey" />
</p>

---

## 📌 Table of Contents

- [✨ Features](#-features)
- [📸 Screenshots](#-screenshots)
- [🛠️ Tech Stack](#-tech-stack)
- [⚙️ Installation](#-installation)
- [🧑‍💻 Git & GitHub Deployment](#-git--github-deployment)
- [📁 Folder Structure](#-folder-structure)
- [📈 Future Improvements](#-future-improvements)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👨‍💻 Author](#-author)

---

## ✨ Features

- 📝 Add new driving logs (date, purpose, distance, etc.)
- 🧾 View all drive records in a scrollable list
- 🔍 Search/filter trips by keywords
- 🗑️ Delete unwanted entries
- 🧰 Edit and update existing records
- 💾 All data stored locally using SQLite3
- 🎯 Lightweight GUI built with Tkinter

---

## 📸 Screenshots

> Add screenshots here for better presentation

```bash
📷 Screenshot 1 - Main UI
📷 Screenshot 2 - Add New Drive
📷 Screenshot 3 - View Records
```

> You can upload image files and reference them here using `![Alt text](path/to/image)`

---

## 🛠️ Tech Stack

| Component     | Technology |
|---------------|------------|
| Language      | Python 3.x |
| GUI Framework | Tkinter    |
| Database      | SQLite3    |
| IDE Used      | PyCharm    |

---

## ⚙️ Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/milanbhimani04/DriveTracker.git
cd DriveTracker
```

### Step 2: Set up Virtual Environment (Optional but Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### Step 3: Install Requirements (if any)
> This project doesn't use external libraries for now, but for future updates, use:
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python drive_tracker.py
```

---

## 🧑‍💻 Git & GitHub Deployment

Here’s how you can upload your PyCharm project to GitHub:

### ✅ Initialize Git (if not already)
```bash
git init
```

### ✅ Add your files
```bash
git add .
```

### ✅ Commit your changes
```bash
git commit -m "Initial commit"
```

### ✅ Connect to GitHub repo
```bash
git remote add origin https://github.com/milanbhimani04/DriveTracker.git
```

### ✅ Push your code
```bash
git branch -M master
git push -u origin master
```

---

## 📁 Folder Structure

```
DriveTracker/
├── drive_tracker.py       # Main GUI application
├── database.db            # SQLite3 database (auto-created on first run)
├── README.md              # Project documentation
├── .gitignore             # Git ignore file (optional)
```

---

## 📈 Future Improvements

- [ ] Export data as PDF/CSV
- [ ] Add login system (user-based tracking)
- [ ] Enhance UI with customTkinter or PyQt
- [ ] Mobile app version using Kivy

---

## 🤝 Contributing

Contributions are welcome!  
If you find any issues or want to enhance this project:

1. Fork the repo 🍴
2. Create a new branch 🛠️
3. Commit your changes 💾
4. Push and submit a PR 🚀

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Milan Bhimani**  
📫 [GitHub Profile](https://github.com/milanbhimani04)
