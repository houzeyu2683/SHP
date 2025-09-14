# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based web scraping tool for collecting Taiwan real estate transaction data from the Ministry of Interior's Land Value Reference website (https://lvr.land.moi.gov.tw/). The project name appears to be "SHP" (Sale House Price).

## Architecture

The codebase consists of two main Python scripts:

### Core Components

1. **`dev.py`** - Main web scraping agent with Selenium WebDriver
   - `Agent` class handles browser automation and data extraction
   - Supports 4 different property transaction departments (買賣, 租賃, 預售屋, 新建案)
   - Handles pagination, data parsing with BeautifulSoup, and CSV export
   - Uses Chrome WebDriver with anti-detection measures

2. **`test-open-browser.py`** - Alternative implementation using Playwright
   - Simpler browser automation for testing/development
   - Focuses on form interaction and navigation

### Key Functionality

- **Web Scraping**: Automated form filling for location, date range, and property type selection
- **Data Processing**: Parses HTML tables into structured pandas DataFrames with different schemas for each department
- **Export**: Saves results as CSV files organized by department/city/area/date range
- **Configuration**: Expects `domain.json` file for city/area mappings (not included in repo)

### Data Structure

Each department has different data schemas:
- Department 1 (買賣): 19 fields including 地段位置, 總價, 單價, etc.
- Department 2 (租賃): 20 fields including rental-specific data
- Department 3 (預售屋): 19 fields for pre-construction sales
- Department 4 (新建案): 17 fields for new construction projects

## Dependencies

Required Python packages:
- `selenium` - Browser automation
- `playwright` - Alternative browser automation (test script)
- `beautifulsoup4` (`bs4`) - HTML parsing
- `pandas` - Data processing and CSV export
- `tqdm` - Progress bars
- Standard library: `time`, `os`, `json`, `multiprocessing`

## Running the Scripts

### Main Data Collection
```bash
python dev.py
```

### Browser Testing
```bash
python test-open-browser.py
```

## Configuration Requirements

The main script expects:
1. **`domain.json`** - Configuration file with city/area mappings (create this file based on the structure expected in `dev.py:594-595`)
2. **Chrome WebDriver** - Must be installed and accessible in PATH
3. **Output directory** - `checkpoint/` folder will be created automatically

## Data Output Structure

CSV files are organized as:
```
checkpoint/
├── 1/          # Department 1 (買賣)
├── 2/          # Department 2 (租賃)
├── 3/          # Department 3 (預售屋)
└── 4/          # Department 4 (新建案)
    └── [CITY]/
        └── [AREA]/
            └── [START_YEAR][START_MONTH]-[END_YEAR][END_MONTH].csv
```