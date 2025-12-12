# 📦 SmartBudget — Python Household Budgeting Package

SmartBudget is a modular Python package for recording incomes and expenses, performing financial analysis, generating visual insights, and saving/loading data using JSON.  
It demonstrates clean software architecture, object-oriented programming, testing with unittest, and collaborative Git workflows.

---

# 📁 Submission Notes (DATA 533 – Step 1)

All deliverables such as project description, pre-presentation slides, final presentation slides, and demo video are stored in:

```
docs/
```

---

# 📁 Project Structure

```
project/
│
├── files/
│   └── records.json
│
├── smartbudget/
│   ├── __init__.py
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── insights.py
│   │   └── summary.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── controller_menu.py
│   │   ├── controller_records.py
│   │   └── controller_system.py
│   │
├── entity/
│   │   ├── __init__.py
│   │   ├── base_record.py
│   │   ├── constants.py
│   │   ├── expense.py
│   │   └── income.py
│   │
├── io/
│   │   ├── __init__.py
│   │   ├── json_io.py
│   │   └── file_utils.py
│
├── tests/
│   ├── test_base_record.py
│   ├── test_income_expense.py
│   ├── test_summary.py
│   ├── test_insights.py
│   └── test_suite.py
│
├── main.py
├── Function_Guide_Reference.md
└── README.md
```

---

# ✨ Features Overview

## 🧱 1. Entity Models (`entity/`)

### `RecordBase`

- validation for name  
- validation for amount  
- shared fields & methods  
- `to_dict()` for JSON  
- `show()` for UI display  

### `Income` / `Expense`

Both inherit from `RecordBase`:

- `Income(name, amount, source)`  
- `Expense(name, amount, category)` (stored as negative)

Override:

- `describe()`  
- `to_dict()`  

---

# 🎯 2. Controllers (`core/`)

### `budget_record_controller.py`

- show summary  
- show income/expense details 
- add income  
- add expense  
- show_expense_plot 

### `file_io_data_controller.py`

- save JSON backup  
- load backup  
- list files  
- delete file  
- reset records  

### `app_menu_controller.py`

- menu UI  
- user routing  
- main program loop  

---

# 📊 3. Analysis Tools (`analysis/`)

The analysis module offers a set of lightweight yet expressive helper functions designed to summarize financial activity, highlight key patterns, and support quick diagnostic checks of a user’s records, all without imposing additional structure or altering the underlying data objects.

- **summary.py**
  - `total_income()`
  - `total_expenses()`
  - `budget_balance()`

- **insights.py**
  - `income_details()`
  - `expense_details()`
  - `plot_expense_by_category()`
  - `_load_split()`

These functions provide the analytical backbone of SmartBudget, allowing users to perform structured aggregation, generate interpretable summaries, and create visual outputs, all while leaving the core data objects and storage structures untouched.

---

# 💾 4. JSON IO (`io/`)

### `json_io.py`
Handles all JSON-based data interactions:

- `save_to_json()` 
   Serializes Income/Expense objects and writes them to a JSON file.
   
- `append_to_json()`  
   Appends a single financial record to an existing JSON file.
   
- `load_from_json()`
   Loads data from a JSON file and reconstructs Income/Expense objects.
   
- `clear_json()` 
   Resets a JSON file by deleting all stored records.

### `file_utils.py`
Provides foundational file-management utilities:

- `file_exists()`  
   Checks whether a file exists.
   
- `list_files()`
   Lists all JSON backup files stored inside the /files/ directory.
   
- `delete_file()`  
   Deletes a specified backup file.

---

# 🚀 Running SmartBudget

Run:

```
python main.py
```

Menu:

```
1. Add Income
2. Add Expense
3. Show Summary
4. Show Expense Details
5. Show Income Details
6. Backup Records to JSON
7. List Backup Files
8. Delete File
9. Records Reset
10. Show Expense Chart
0. Exit
```

---

# 🗂 Example JSON Output

```json
[
    {
        "name": "Salary",
        "amount": 5000,
        "source": "Company A",
        "type": "Income"
    },
    {
        "name": "Rent",
        "amount": -1200,
        "category": "Housing",
        "type": "Expense"
    }
]
```

---

# 🧪 Unit Testing (DATA 533 – Step 2)

All Step 2 requirements satisfied.

## ✔ Test Coverage

Tests cover:

- entity classes  
- JSON I/O  
- summary calculations  
- insights and plotting logic  
- controller functions  

Each test class includes:

- ≥ 2 test cases  
- ≥ 4 assertions per case  
- lifecycle methods:  
  - `setUpClass`  
  - `setUp`  
  - `tearDown`  
  - `tearDownClass`  

## ✔ Test Suite

```
tests/test_suite.py
```

Runs all tests.

Run all tests:

```
python -m unittest discover tests
```

Or:

```
python tests/test_suite.py
```

---

# 🤝 GitHub Collaboration (Step 2 Requirement)

- GitHub repo created  
- collaborator added  
- both members cloned repo  
- each used separate branches  
- test code developed independently  
- pull requests completed  
- merged into `main`  
- Git history shows equal contribution  

---

# 🌟 Project Highlights

- modular package design  
- object-oriented entity models  
- JSON persistence  
- clean separation of logic layers  
- analysis chart with matplotlib  
- full unittest suite  
- proper collaboration workflow  


---

# 📘 Summary

SmartBudget is a complete, well-designed Python budgeting application that fulfills all requirements for DATA 533:

✔ modular architecture  
✔ OOP with inheritance  
✔ JSON persistence  
✔ analysis + plotting  
✔ unittest suite  
✔ GitHub workflow  
✔ documentation + presentation ready  
