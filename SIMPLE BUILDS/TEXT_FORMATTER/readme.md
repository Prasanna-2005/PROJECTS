# Column Justified Text Formatter 📄🔄

This project transforms raw text files into **neatly formatted, column-justified text**, ideal for creating aligned documents, terminal reports, or printable formats. It takes a plain text input and distributes its content across multiple justified columns, maintaining visual alignment and readability.

---

## 📁 Project Structure

```
TEXT_FORMATTER/
│
├── justify_text.py      # Main script for formatting text
├── input.txt            # Sample input text
├── output.txt           # Justified output file
└── README.md            # Documentation
```

---

## 🚀 Key Features

* 🔹 **Multi-Column Formatting**

  * Accepts a number of columns (e.g., 2, 3, 4)
  * Splits and aligns the text evenly across all columns

* 🔹 **Justified Alignment**

  * Ensures that each line within a column is left and right justified, mimicking newspaper-style alignment

* 🔹 **Plain Text Input/Output**

  * Easily integrates with other CLI tools or document pipelines

* 🔹 **Custom Column Widths**

  * Adjustable width support depending on output medium (terminal or file)

* 🔹 **Writes Output to File**

  * Final justified text is saved to `output.txt` for persistence and portability

---

## 🚄 How to Run

```bash
# Windows/Linux/Mac
python justify_text.py
ENTER VALID FILE NAME (TXT FILES):: input.txt 
ENTER NO OF COLUMNS: 3
Formatted output written to 'justified_output.txt'
```

This formats `input.txt` into **3 justified columns** and writes the result to `output.txt`.

---

## 🔧 Requirements

* **Python 3.x**
* No external libraries required – just standard Python string manipulation

---

## 🌱 Applications

* Terminal-based document previews
* CLI-generated newsletters or reports
* Printing formatted text
* PDF pre-processing tools

---

## 👤 Author

**Prasanna**
BTech CSE @ IIITDM Kancheepuram
Enjoys solving layout challenges

---

## 🤝 Contributing

Ideas for auto-detecting optimal column count or wrapping strategies? Contributions are welcome.
