# 📊 JobKorea Company Data Scraper

This repository contains Python scripts that automate the process of collecting metadata and company information from **JobKorea** based on a list of company names. It is designed to dynamically extract relevant company details such as type, location, industry, capital, revenue, CEO, and founding date.

## 🧾 Files Overview

- **`jobKorea_sales_dynamic_2.py`**  
  Contains the main scraping logic and a function `get_jobkorea_data` that accepts a list of company names and returns their detailed information by parsing JobKorea’s search and detail pages.

- **`jobKorea_data_6.py`**  
  Reads a CSV file (`enterprise_df_10k_utf8_data.csv`), filters for companies managed by 담당 (=6번 for my own case), extracts their names, and calls the scraping function from the main script. The output is saved to `jobkorea_data_6_0618.csv`.

## 🔍 Features

- **Company Metadata Extraction:**  
  Gathers company type, location, and industry directly from JobKorea's search results.

- **Detail Page Scraping:**  
  Visits individual company pages to extract additional fields like capital, revenue, CEO, and founding date.

- **Error Handling:**  
  Includes basic handling for network issues, missing metadata, and bad responses.

- **Rate Limiting:**  
  Implements random delays between requests (2.5 to 4 seconds) to avoid hitting the site too aggressively.

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/jobkorea-scraper.git
cd jobkorea-scraper
```

### 2. Install dependencies

Make sure you have Python 3.x installed. Then install the required libraries:

```bash
pip install pandas beautifulsoup4 requests
```

### 3. Prepare the Input CSV

Ensure your CSV (`enterprise_df_10k_utf8_data.csv`) contains at least two columns:
- `기업명` (Company Name)
- `담당` (ID)

## 🚀 Usage

### Option 1: Standalone Scraping

You can run the main script directly with a predefined list of companies:

```bash
python jobKorea_sales_dynamic_2.py
```

This will output `jobkorea_data_clean.csv` containing metadata for the hardcoded company list.

### Option 2: Batch Scraping from CSV

To run the full pipeline using filtered input from a CSV:

```bash
python jobKorea_data_6.py
```

This script will:
- Load `enterprise_df_10k_utf8_data.csv`
- Filter for companies with 담당 == '6번'
- Extract job metadata via `get_jobkorea_data`
- Save the output to `jobkorea_data_6_0618.csv`

## 📁 Output Format

Both scripts produce a CSV with the following columns:

| 기업명 | 기업형태 | 지역 | 업종 | 자본금 | 매출액 | 대표자 | 설립일 |
|--------|----------|------|------|--------|--------|--------|--------|

## 📌 Notes

- The scraping logic may break if JobKorea updates its HTML structure.
- Be respectful of target websites’ usage policies when scraping data.
- For production use, consider implementing better error logging and proxy rotation.

## 📄 License

MIT License. Feel free to use, modify, and share under the terms of this license.
