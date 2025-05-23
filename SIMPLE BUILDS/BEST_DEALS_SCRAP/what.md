# Price Comparison Tool for Mobiles 📱💲

This project is a smart, Python-based tool for comparing prices of electronic products — starting with the **Samsung to Apple.... **. It simplifies the product research phase by checking multiple online platforms and presenting users with the **best available price** based on their selected specifications.

Built to enhance the modern shopper's experience, this tool not only saves time but also ensures you're getting the best deal possible.

---

## 📁 Project Structure

```
PRICE_COMPARISON_TOOL/
│
├── best_deal.py       # Main script for fetching and comparing mobile prices
└── README.md          # Documentation
```

---

## 🚀 Key Features

* **🔹 Product Customization**: Users input specific product details:

  * Brand (e.g., Apple)
  * Model (e.g., iPhone 15)
  * Storage (e.g., 128GB)
  * Color (e.g., Blue)

* **🔹 Price Aggregation**:

  * Fetches price data from major Indian e-commerce platforms:

    * Amazon
    * Flipkart
    * Snapdeal

* **🔹 Smart Comparison**:

  * Displays best price and vendor
  * Shows a table of all available options with pricing
  * Helps users make informed decisions

* **🔹 User-Friendly CLI**:

  * Simple terminal prompts and clean output
  * No fluff — just the numbers you need

---

## 🔧 Tech Stack

* **Python 3.x**
* `requests`, `bs4`, `pandas` (if used internally)
* Web scraping techniques to extract live prices

> Note: Some platforms may require dynamic content handling via Selenium, depending on the page structure.

---

## 🚄 How to Use

### Prerequisites

Install dependencies:

```bash
pip install beautifulsoup4 pandas requests
```

### Run the Tool

```bash
python best_deal.py
```

Follow the prompts to enter your desired product specs. The tool will output:

```bash
Best deal found:
Flipkart – ₹78,999

Other options:
Amazon  – ₹81,499
Snapdeal – ₹80,200
```

---

## 📊 Future Roadmap

* 🌐 Extend support to laptops, TVs, and smartwatches
* ✨ Web UI using Flask or Streamlit
* 🛡️ Caching + price history chart
* 🚀 Telegram/Email alerts when prices drop
* 📈 Scrape more platforms like Croma, Reliance Digital

---

## 👤 Author

**Prasanna**
BTech CSE @ IIITDM Kancheepuram
Explorer of e-commerce automation, scraping, and smart tools.

---

## 🤝 Contributing

Want to help expand this into a fully featured shopping assistant? Fork and PR welcome!

