# Amazon Deal Scraper 📊📦

A powerful web scraping project built with Python, Selenium, and BeautifulSoup to extract **real-time Amazon deals** directly from the [Amazon India Deals page](https://www.amazon.in/deals). This tool scrapes product names, prices, discounts, ratings, and review counts — saving them to a CSV for further analysis.

---

## 🔧 Technologies Used

* **Python 3.x**
* **Selenium** – Automates browser interaction
* **BeautifulSoup (bs4)** – Parses HTML content
* **Pandas** – For storing and exporting data

---

## 📁 Project Structure

```
AMAZON_WEB_SCRAPER/
│
├── amazon_deals_scraper.py  # Main scraping script
├── products.csv              # Output file containing scraped product info
└── README.md                 # Project documentation
```

---

## 🚀 How It Works

1. Opens Amazon's Deals Page
2. Scrolls and loads dynamic content
3. Parses HTML using BeautifulSoup
4. Navigates each product link
5. Extracts product title, price, discount, rating, and review count
6. Repeats scroll+parse cycle for extended data
7. Saves everything into a `products.csv` file

---

## 🔹 Fields Scraped

* Product Name
* Price
* Discount
* Number of Ratings
* Rating

---

## 📈 Sample Output (`products.csv`)

| Product Name | Price  | Discount | Num\_Ratings | Ratings |
| ------------ | ------ | -------- | ------------ | ------- |
| ABC Phone    | 11,999 | 35% OFF  | 23,456       | 4.3     |
| XYZ Speaker  | 3,499  | 20% OFF  | 4,900        | 4.0     |

---

## 🌐 Prerequisites

* Google Chrome installed
* ChromeDriver matching your browser version (already configured in script)
* Python 3.x with the following libraries:

  ```bash
  pip install selenium beautifulsoup4 pandas
  ```

---

## ⚖️ Configuration Notes

* Ensure your Chrome binary and chromedriver paths are set correctly in `opt.binary_location` and `Service(...)`.
* Script uses a **visible browser** for easier debugging.

  > You can enable `--headless` mode for background scraping.

---

## 🚄 How to Run

```bash
python amazon_deals_scraper.py
```

> Output will be saved as `products.csv` in the same directory.

---

## 🌱 Future Enhancements

* 🌐 Scrape multiple categories (Electronics, Fashion, etc.)
* 📈 Add historical price tracking
* 📱 Mobile-responsive scraping
* 🎨 GUI with progress bar (Tkinter or Streamlit)

---

## 👤 Author

**Prasanna**
BTech CSE @ IIITDM Kancheepuram
Loves automating boring stuff 

---

## 🤝 Contributing

Pull requests and suggestions are welcome! If you encounter issues, feel free to open an issue or PR.