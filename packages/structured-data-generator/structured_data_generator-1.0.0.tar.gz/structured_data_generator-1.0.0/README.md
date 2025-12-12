
# 📊 Synthetic Data Generator - Complete Documentation

> **A simple, powerful CLI tool to generate realistic fake data for testing, development, and demonstrations.**

---

## 📋 Quick Navigation

1. [What is This?](#what-is-this)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [How It Works](#how-it-works)
5. [Available Templates](#available-templates)
6. [Step-by-Step Guide](#step-by-step-guide)
7. [Export Options](#export-options)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## What is This?

The **Synthetic Data Generator** is a command-line tool that creates **realistic fake data** for different scenarios:

### 🎯 What Can You Do?

✅ Generate fake user profiles (names, emails, addresses)  
✅ Create e-commerce transaction records  
✅ Generate banking & financial data  
✅ Create healthcare patient records  
✅ Generate IoT sensor readings  
✅ Create product catalogs  
✅ Generate NLP text data  
✅ Create web analytics data  
✅ Generate image metadata  
✅ Create student academic records  

### 🤔 Why Use This?

- **Test your application** with realistic data without using real customer data
- **Database training** - populate your database for demos
- **Development work** - test features with varied data
- **Privacy safe** - all data is fake and synthetic
- **Customize data** - select only the fields you need

---

## Installation

### 📦 What You Need

- **Python 3.7+** installed on your computer
- **pip** (package manager for Python)

### 🔧 Step 1: Install Required Libraries

Open your terminal/command prompt and run:

```bash
pip install pandas faker
```

This installs:
- **pandas** - for working with data tables
- **faker** - for generating realistic fake data

### 🔧 Step 2: Download the Files

Make sure you have these files in the same folder:
- `CLI.py` (the main program)
- `DATA_ENGINE.py` (all data templates)

### ✅ Step 3: Verify Installation

Run this command to check if everything is set up:

```bash
python CLI.py
```

You should see the menu appear. If yes, you're ready to go! 🎉

---

## Getting Started

### ⚡ Quick Start (30 seconds)

```bash
# 1. Open terminal/command prompt
# 2. Go to your project folder
cd /path/to/your/project

# 3. Run the program
python CLI.py

# 4. Follow the menu
```

**That's it!** The program will guide you through everything.

---

## How It Works

### 🔄 The Process (Simple Explanation)

```
Step 1: You choose a TEMPLATE (what kind of data you want)
           ↓
Step 2: You choose SUBCATEGORIES (which fields from that template)
           ↓
Step 3: You enter COUNT (how many rows of data)
           ↓
Step 4: Program generates the fake data
           ↓
Step 5: You save it as CSV or JSON
```

### 📸 Example Workflow

**[INSERT SCREENSHOT: Full CLI menu here]**

---

## Available Templates

### 1️⃣ USER TEMPLATE

Generate fake user/customer profiles.

**What data you get:**
- Full name, username, email, phone
- Address (street, city, state, country)
- Account info (creation date, status)
- Preferences (language, currency)
- Device info (mobile/desktop/tablet)

**Use cases:** Customer databases, user profiles, testing auth systems

---

### 2️⃣ E-COMMERCE TEMPLATE

Generate fake online shopping transactions.

**What data you get:**
- Order ID, transaction date, order status
- Customer info (name, email, phone)
- Product info (name, category, quantity, price)
- Payment details (method, status, transaction ID)
- Shipping info (address, partner, status)
- Device info

**Use cases:** E-commerce websites, order management systems, payment testing

**[INSERT SCREENSHOT: Sample generated e-commerce data]**

---

### 3️⃣ FINANCIAL BANKING TEMPLATE

Generate fake banking transactions.

**What data you get:**
- Account info (ID, type, bank name, IFSC)
- Transaction details (ID, date, type, amount, status)
- Customer info (name, email, PAN number, Aadhaar)
- Card details (type, network, last 4 digits)
- Loan info (type, amount, interest rate, EMI)
- Device info

**Use cases:** Banking apps, financial dashboards, transaction analytics

---

### 4️⃣ HEALTHCARE TEMPLATE

Generate fake medical records.

**What data you get:**
- Patient info (ID, name, age, gender, blood group)
- Medical records (diagnosis, symptoms, severity)
- Doctor info (name, specialization, hospital)
- Appointment details (date, status, type)
- Prescription info (medicine, dosage, duration)
- Billing info (consultation fee, medicine charges)
- Device info

**Use cases:** Hospital systems, telemedicine apps, medical records

**[INSERT SCREENSHOT: Sample healthcare data]**

---

### 5️⃣ IOT SENSOR TEMPLATE

Generate fake IoT sensor readings.

**What data you get:**
- Device info (ID, type, firmware version)
- Location data (latitude, longitude, altitude)
- Sensor readings (temperature, humidity, air quality)
- Network data (signal strength, connection type, IP)
- Battery info (level, health, charging status)
- Timestamp & maintenance info

**Use cases:** IoT dashboards, sensor data analysis, smart home testing

---

### 6️⃣ NLP TEXT TEMPLATE

Generate fake text documents and NLP data.

**What data you get:**
- Text data (sentences, paragraphs, words, keywords)
- Document metadata (title, author, published year)
- NLP annotations (language, sentiment, emotion, toxicity)
- Named Entity Recognition (person, location, organization)
- Text statistics (word count, character count, avg word length)
- Timestamps

**Use cases:** NLP model testing, text analysis, chatbot training

---

### 7️⃣ WEB ANALYTICS TEMPLATE

Generate fake website analytics data.

**What data you get:**
- Session info (session ID, user ID, duration, engagement score)
- Page metrics (URL, time on page, scroll depth, interactions)
- Traffic source (source, medium, campaign, keyword)
- Device & browser info
- Geo data (IP, country, city, timezone)
- Performance data (page load time, DNS lookup, resource count)

**Use cases:** Analytics dashboards, website performance testing, traffic analysis

---

### 8️⃣ IMAGE METADATA TEMPLATE

Generate fake image metadata.

**What data you get:**
- Basic info (filename, format, file size, color mode)
- Dimensions (width, height, aspect ratio, DPI)
- Camera EXIF (camera make, lens, focal length, aperture, ISO)
- Geolocation (latitude, longitude, city, country)
- Tags & labels (primary label, confidence score)
- Color stats (dominant color, brightness, contrast)

**Use cases:** Image database testing, photo library apps, image analysis

---

### 9️⃣ EDUCATION STUDENT TEMPLATE

Generate fake student academic records.

**What data you get:**
- Student profile (ID, name, age, grade level)
- Academic scores (math, science, English, social science, computer)
- Attendance (total classes, classes attended, percentage)
- Behavior & activity (disciplinary actions, sports score, creativity)
- Performance metrics (study hours, homework completion, participation)

**Use cases:** School management systems, student performance dashboards

**[INSERT SCREENSHOT: Sample student data]**

---

### 🔟 PRODUCT CATALOG TEMPLATE

Generate fake product listings.

**What data you get:**
- Basic info (product ID, name, category, brand, description)
- Variants (color, size, material, model number)
- Pricing (price, discount, final price, currency)
- Inventory (stock status, quantity, warehouse location)
- Ratings & reviews (average rating, total reviews, review text)
- Timestamps (release date, last updated)

**Use cases:** E-commerce catalogs, product databases, inventory management

---

## Step-by-Step Guide

### 🚀 Complete Tutorial

#### **Step 1: Start the Program**

```bash
python CLI.py
```

You'll see:
```
-----------------------------
🔥 SYNTHETIC DATA GENERATOR 🔥
-----------------------------

Available Templates:

1. USER TEMPLATE

2. ECOMMERCE TRANSACTION TEMPLATE

3. FINANCIAL BANKING TEMPLATE

... (and more)
```

**[INSERT SCREENSHOT: Initial menu]**

---

#### **Step 2: Select a Template**

When asked:
```
Select a Template (number): 
```

**Type the number** of the template you want. For example:
- Type `1` for User Template
- Type `2` for E-commerce Template

**Example:**
```
Select a Template (number): 2
```

**[INSERT SCREENSHOT: After selecting template]**

---

#### **Step 3: Choose Subcategories**

After selecting, you'll see available subcategories:

```
Available Subcategories:

1. Order Info
2. Customer Info
3. Product Info
4. Payment Info
5. Shipping Info
6. Device Info

Enter Subcategories (comma-separated numbers):
```

**Simple explanation:** Each template has groups of related data fields.

**Example:**
```
Enter Subcategories (comma-separated numbers): 1,2,3
```

This means: "I want Order Info, Customer Info, and Product Info"

**💡 Pro Tip:** 
- Type `1,2,3,4,5,6` for ALL fields
- Type `1,3,5` for only some fields
- Pick only what you need!

**[INSERT SCREENSHOT: Subcategory selection]**

---

#### **Step 4: Enter Number of Rows**

```
Enter number of rows to generate: 
```

**Simple:** How many fake records do you want?

**Examples:**
```
Enter number of rows to generate: 100
```

Creates 100 rows of fake data.

**Timing guide:**
- 100 rows = ~1-2 seconds
- 1,000 rows = ~5-10 seconds  
- 10,000 rows = ~30-60 seconds

---

#### **Step 5: Optional Seed (Skip if Unsure)**

```
Enter Seed (press Enter to skip):
```

**What is a seed?** It makes the data reproducible (same fake data every time).

**Simple usage:**
- **Skip it (press Enter)** = Different data each time
- **Enter a number** (like `42`) = Same data every time with that number

**Example:**
```
Enter Seed (press Enter to skip): 42
```

**[INSERT SCREENSHOT: Seed option]**

---

#### **Step 6: Data Generated!**

You'll see:
```
✅ DATA GENERATED SUCCESSFULLY!
==============================
 SUMMARY 

* Template: ECOMMERCE TRANSACTION TEMPLATE
⏱ Time Taken: 2.45 seconds
* Rows Generated: 100
* Columns Generated: 18
* Seed: 42
==============================
```

Great! Your data is ready.

---

#### **Step 7: Choose Export Option**

```
Select what you want to do next:

1. Preview data (first 5 rows)
2. Save as CSV
3. Save as JSON
4. Exit

Enter options (comma-separated):
```

**You can pick multiple options!**

---

## Export Options

### 📥 Option 1: Preview Data

**What it does:** Shows you the first 5 rows in your terminal.

**Use case:** Quick check before saving.

**Example output:**
```
S.no. Order ID    Customer Name Customer Email        Total Amount
1     a1b2c3d4   John Doe      john@example.com      15,500
2     e5f6g7h8   Jane Smith    jane@example.com      8,200
3     i9j0k1l2   Bob Johnson   bob@example.com       25,000
...
```

---

### 💾 Option 2: Save as CSV

**What it does:** Saves data as an Excel-compatible CSV file.

**How to use:**
```
Enter CSV file name: my_orders
```

This creates: `my_orders.csv`

**Open it:** 
- Double-click to open in Excel/Sheets
- Use in Python with: `pd.read_csv('my_orders.csv')`

**When to use:** 
- ✅ For Excel/spreadsheet work
- ✅ For uploading to most tools
- ✅ For data analysis in Excel

**[INSERT SCREENSHOT: CSV file in Excel]**

---

### 🔗 Option 3: Save as JSON

**What it does:** Saves data as JSON format (web-friendly).

**How to use:**
```
Enter JSON file name: my_orders
```

This creates: `my_orders.json`

**Example JSON output:**
```json
[
  {
    "S.no.": 1,
    "Order ID": "a1b2c3d4",
    "Customer Name": "John Doe",
    "Customer Email": "john@example.com",
    "Total Amount": 15500
  },
  {
    "S.no.": 2,
    "Order ID": "e5f6g7h8",
    ...
  }
]
```

**When to use:**
- ✅ For APIs and web services
- ✅ For Python/JavaScript applications
- ✅ For database imports

---

### 🚪 Option 4: Exit

Just closes the program. Simple!

---

## Complete Examples

### 🎓 Example 1: Generate User Profiles

**Goal:** Create 50 fake user profiles for testing

**Steps:**
```
1. Run: python CLI.py
2. Select Template: 1 (USER TEMPLATE)
3. Select Subcategories: 1,2,3,4 (Personal, Address, Account, Preferences)
4. Count: 50
5. Seed: (skip)
6. Export: 2 (Save as CSV)
7. Filename: user_profiles
```

**Result:** `user_profiles.csv` with 50 fake users ✅

**[INSERT SCREENSHOT: User data sample]**

---

### 🛒 Example 2: E-commerce Testing

**Goal:** Create 100 fake orders for testing checkout system

**Steps:**
```
1. Run: python CLI.py
2. Select Template: 2 (ECOMMERCE TRANSACTION TEMPLATE)
3. Select Subcategories: 1,2,3,4,5 (Order, Customer, Product, Payment, Shipping)
4. Count: 100
5. Seed: 123 (reproducible)
6. Export: 1,2 (Preview + Save as CSV)
7. Filename: test_orders
```

**Result:** Preview in terminal + `test_orders.csv` ✅

---

### 🏥 Example 3: Healthcare Testing

**Goal:** Generate 200 patient records for testing medical software

**Steps:**
```
1. Run: python CLI.py
2. Select Template: 4 (HEALTHCARE TEMPLATE)
3. Select Subcategories: 1,2,3,4 (Patient, Medical, Doctor, Appointment)
4. Count: 200
5. Seed: (skip)
6. Export: 3 (Save as JSON)
7. Filename: patient_records
```

**Result:** `patient_records.json` with 200 patients ✅

---

## Troubleshooting

### ❌ Problem: "ModuleNotFoundError: No module named 'pandas'"

**Solution:**
```bash
pip install pandas faker
```

Then try again.

---

### ❌ Problem: Command "python" not recognized

**Solution:**
- You might need to use `python3` instead:
```bash
python3 CLI.py
```

Or on Windows, use full path to Python.

---

### ❌ Problem: "Invalid template selection"

**Reason:** You entered a wrong number or non-existent template.

**Solution:**
- Look at the menu carefully
- Enter a number that's listed (usually 1-10)
- Don't enter letters or special characters

---

### ❌ Problem: Data generation is very slow

**Why:** You're generating too many rows at once.

**Solution:**
- Try smaller numbers first: 10, 50, 100
- Large datasets (100,000+) will take time
- Be patient! It's still much faster than manual entry

---

### ❌ Problem: CSV file won't open in Excel

**Reason:** File might be corrupted or encoding issue.

**Solution:**
```bash
# Regenerate the data
python CLI.py

# Or check if file was saved correctly
# Try opening with a text editor first
```

---

### ❌ Problem: Subcategory selection fails

**Reason:** You entered numbers that don't exist or wrong format.

**Solution:**
- Separate numbers with commas: `1,2,3` ✅
- Don't use spaces: `1, 2, 3` ❌
- Check max number shown in menu

---

## FAQ

### ❓ Is this data real?

**No!** All data is 100% fake and synthetic. It's safe to use anywhere.

---

### ❓ Can I use this for production?

**No.** This is for testing and development only. Never use fake data in real production systems for customers.

---

### ❓ Can I modify the templates?

**Yes!** The templates are in `DATA_ENGINE.py`. You can edit them to add custom fields.

(Advanced topic - ask me if interested!)

---

### ❓ How is fake data generated?

Using a library called **Faker** which creates realistic-looking but fake data using algorithms.

---

### ❓ Why choose JSON over CSV?

**CSV:** Better for Excel, spreadsheets, simple analysis
**JSON:** Better for web APIs, web applications, databases

---

### ❓ Can I generate millions of rows?

**Technically yes, but:**
- Will take time (depends on your computer)
- Might use lots of memory
- Better to generate in batches (100K at a time)

---

### ❓ What if I want different data fields?

You have two options:

**Option 1:** Use only the subcategories you need (select specific fields)

**Option 2:** Modify `DATA_ENGINE.py` to customize templates

---

### ❓ Can I use this offline?

**Yes!** No internet needed once installed. Everything runs on your computer.

---

## Need Help?

### 📞 Common Issues Checklist

- [ ] Did I install pandas and faker?
- [ ] Are `CLI.py` and `DATA_ENGINE.py` in same folder?
- [ ] Did I enter valid template number?
- [ ] Did I enter subcategories correctly (comma-separated)?
- [ ] Did I enter a valid count (number)?
- [ ] Did I check the error message for clues?

---

## Tips & Tricks

### 💡 Pro Tips

1. **Test with small data first**
   ```bash
   # Generate 10 rows first to test
   # If it works, generate 1000
   ```

2. **Use seeds for consistent testing**
   ```bash
   # Same seed = same data every time
   # Good for reproducible tests
   ```

3. **Preview before saving large files**
   ```bash
   # Select option 1 first
   # Check if data looks correct
   # Then save as CSV/JSON
   ```

4. **Combine templates**
   ```bash
   # Generate users (Template 1)
   # Generate orders (Template 2)
   # Connect them manually for realistic data
   ```

5. **Clean up old files**
   ```bash
   # Delete old CSV/JSON files before regenerating
   # Keeps your folder organized
   ```

---

## Advanced: Customize Templates

**(For experienced Python users)**

To add custom fields to a template, edit `DATA_ENGINE.py`:

```python
"New Field": lambda: fake.company(),  # Uses Faker
"Age": lambda: random.randint(18, 65),  # Random number
"ID": lambda: str(uuid.uuid4()),  # Unique ID
```

Then select it in CLI!

---

## Architecture Overview

```
┌─────────────────────────────────────────┐
│         CLI.py (Main Interface)         │
│  - Menu display                         │
│  - User input                           │
│  - Export options                       │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│    DATA_ENGINE.py (All Templates)       │
│  - USER_TEMPLATE                        │
│  - ECOM_TEMPLATE                        │
│  - FINANCIAL_TEMPLATE                   │
│  - HEALTHCARE_TEMPLATE                  │
│  - IOT_SENSOR_TEMPLATE                  │
│  - ... (7 more templates)               │
│  - generate_from_template() function    │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│    External Libraries                   │
│  - Faker (generates fake data)          │
│  - Pandas (data processing)             │
│  - Random (random selections)           │
│  - UUID (unique IDs)                    │
└─────────────────────────────────────────┘
```

---

## File Structure

```
your_project_folder/
├── CLI.py                 ← Run this file
├── DATA_ENGINE.py         ← All templates here
├── user_profiles.csv      ← Generated file (example)
├── test_orders.json       ← Generated file (example)
└── README.md             ← This documentation
```

---

## Version Info

**Current Version:** 1.0  
**Last Updated:** December 2025  
**Python Required:** 3.7+

---

## Support & Feedback

**Having issues?**
1. Check troubleshooting section
2. Check FAQ
3. Review examples
4. Check file structure

---

## License

This tool is free to use for personal, educational, and testing purposes.

---

**Happy data generating! 🚀**

*Made with ❤️ for developers, testers, and data enthusiasts.*
