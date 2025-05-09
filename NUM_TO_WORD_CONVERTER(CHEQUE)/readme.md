# Number to Text Converter 🧽🔤

A simple yet powerful Python project that converts numerical values into their corresponding textual (word-based) representations.

This utility is especially useful in:

* 🧾 Cheque generation
* 💰 Receipt printing
* 📄 Invoice generation
* 🌐 Applications requiring International or Indian numbering systems

---

## 📁 Project Structure

```
NUM_TO_WORD_CONVERTER(CHEQUE)/
│
├── num_to_text_(INTL).py    # International Numbering System (million, billion, etc.)
├── num_to_text_(IND_SYS).py # Indian Numbering System (lakh, crore, etc.)
└── README.md                # Project documentation
```

---

## 🔧 How It Works

* Accepts a numeric input from the user (integers only).
* Converts the number to its textual form.
* Two modes:

  * **International System** (`num_to_text_(INTL).py`)
  * **Indian System** (`num_to_text_(IND_SYS).py`)

---

## 🚀 Getting Started

### ✅ Prerequisites

* Python 3.x must be installed (no external libraries required)

---

### 🖥️ For Windows

Open **Command Prompt** or **PowerShell**, then run:

```bash
python --version
python num_to_text_(INTL).py
python num_to_text_(IND_SYS).py
```

> ⚠️ Use `python` instead of `python3` unless you've configured Python 3 explicitly with that alias.

---

### 🐧 For Linux

Open a **terminal**, then run:

```bash
python3 --version
python3 num_to_text_(INTL).py
python3 num_to_text_(IND_SYS).py
```

---

### 🍎 For macOS

Open the **Terminal**, then run:

```bash
python3 --version
python3 num_to_text_(INTL).py
python3 num_to_text_(IND_SYS).py
```

---

## 💡 Example

**Input:**

```
Enter a number: 1234567
```

**Output (International System):**

```
One million two hundred thirty-four thousand five hundred sixty-seven
```

**Output (Indian System):**

```
Twelve lakh thirty-four thousand five hundred sixty-seven
```

---

## ✨ Features

* ✅ Written in pure Python (no dependencies)
* 🧠 Handles large numbers gracefully
* 🧱 Modular code structure
* 💻 CLI-driven and user-friendly
* 🔌 Easy to integrate into larger applications

---

## 🌱 Future Ideas

* 🪹 Add support for decimal values (e.g., rupees and paise)
* 🌍 Support for multiple languages (localization)
* 📦 Package as a pip-installable module
* 🖼️ GUI version using Tkinter
* 🌐 Web version using Flask

---

## 👤 Author

**Prasanna**
BTech CSE @ IIITDM Kancheepuram

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
If you'd like to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit your changes (`git commit -am 'Add feature xyz'`)
4. Push to the branch (`git push origin feature-xyz`)
5. Open a pull request

---


