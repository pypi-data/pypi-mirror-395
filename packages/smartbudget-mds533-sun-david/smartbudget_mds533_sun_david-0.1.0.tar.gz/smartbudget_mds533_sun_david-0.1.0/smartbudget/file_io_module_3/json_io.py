"""
JSON input/output helpers for SmartBudget.
"""

import json
import os
from smartbudget.file_io_module_3.file_utils import FILES_DIR, ensure_files_dir
from smartbudget.entity.income import Income
from smartbudget.entity.expense import  Expense
from smartbudget.entity.base_record import RecordBase

DEFAULT_FILENAME = "records.json"

def save_to_json(records, filename=DEFAULT_FILENAME):
    """Save to files/filename."""
    ensure_files_dir()
    path = os.path.join(FILES_DIR, filename)

    data = [r.to_dict() for r in records]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_from_json(filename=DEFAULT_FILENAME):
    """Load from files/filename. Returns list of RecordBase objects."""
    ensure_files_dir()
    path = os.path.join(FILES_DIR, filename)


    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        return []


    with open(path, "r", encoding="utf-8") as f:
       raw = json.load(f)

    objects = []
    for item in raw:
        if item.get("type") == "Income":
            obj = Income(item["name"], item["amount"], item.get("source", "未知"))
        elif item.get("type") == "Expense":
            obj = Expense(item["name"], abs(item["amount"]), item.get("category", "未知"))
        else:
            obj = RecordBase(item["name"], item["amount"])

        objects.append(obj)

    return objects


def append_to_json(new_records, filename=DEFAULT_FILENAME):
    """Append new_records to files/filename."""
    existing = load_from_json(filename)
    all_records = existing + new_records
    save_to_json(all_records, filename)

def clear_json(filename=DEFAULT_FILENAME):
    """Clear all records in the given JSON file."""
    ensure_files_dir()
    path = os.path.join(FILES_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)

    return True

