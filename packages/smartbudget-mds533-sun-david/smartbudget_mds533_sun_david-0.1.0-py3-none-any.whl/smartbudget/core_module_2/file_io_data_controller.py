"""
FileIoDataStorageController
---------------------------

Enhanced for Step 3:
    - Robust error handling with try/except
    - Uses custom SmartBudgetError for controlled failures
    - Prevents crashes on missing files, bad JSON, IO failures
"""

from smartbudget.entity.income import Income
from smartbudget.entity.expense import Expense
from smartbudget.entity.base_record import SmartBudgetError

from smartbudget.file_io_module_3 import (
    save_to_json,
    load_from_json,
    file_exists,
    list_files,
    delete_file,
    clear_json,
)


class FileIoDataStorageController:
    """High-level controller for SmartBudget's file-based storage operations."""

    # --------------------------------------------------------
    # Clear primary data file
    # --------------------------------------------------------
    def clear_data(self):
        try:
            confirm = input("⚠ Are you sure you want to CLEAR ALL DATA? (y/n): ").lower()
            if confirm == "y":
                try:
                    clear_json()
                    print("✔ All records have been cleared.\n")
                except Exception as e:
                    raise SmartBudgetError(f"Failed to clear records.json: {e}")
            else:
                print("❌ Cancelled.\n")

        except Exception as e:
            print(f"❌ Error in clear_data: {e}")

    # --------------------------------------------------------
    # Save current records to user-specified file
    # --------------------------------------------------------
    def save_data(self):
        try:
            filename = input("Enter filename to save (e.g., backup.json): ").strip()

            if not filename:
                raise SmartBudgetError("Filename cannot be empty.")

            if filename == "records.json":
                print("❌ Cannot save to system file.\n")
                return

            # Overwrite prompt
            if file_exists(filename):
                overwrite = input("⚠ File exists. Overwrite? (y/n): ").lower()
                if overwrite != "y":
                    print("❌ Save cancelled.\n")
                    return

            try:
                data = load_from_json("records.json")
            except Exception as e:
                raise SmartBudgetError(f"Failed to read records.json: {e}")

            try:
                save_to_json(data, filename)
            except Exception as e:
                raise SmartBudgetError(f"Failed to save backup file '{filename}': {e}")

            print(f"✔ Records saved to {filename}\n")

        except SmartBudgetError as e:
            print(f"❌ Save error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error in save_data: {e}")

    # --------------------------------------------------------
    # Load backup file into memory
    # --------------------------------------------------------
    def load_data(self, incomes: list, expenses: list):
        try:
            filename = input("Enter filename to load: ").strip()

            if not filename:
                raise SmartBudgetError("Filename cannot be empty.")

            if not file_exists(filename):
                print("❌ File not found.\n")
                return

            try:
                loaded_records = load_from_json(filename)
            except Exception as e:
                raise SmartBudgetError(f"Failed to load JSON from '{filename}': {e}")

            # Populate income/expense lists
            try:
                for record in loaded_records:
                    if isinstance(record, Income):
                        incomes.append(record)
                    elif isinstance(record, Expense):
                        expenses.append(record)
            except Exception as e:
                raise SmartBudgetError(f"Error processing loaded records: {e}")

            print(f"\n✔ Loaded {len(loaded_records)} records from '{filename}'\n")
            for rec in loaded_records:
                print(" -", rec.describe())
            print()

        except SmartBudgetError as e:
            print(f"❌ Load error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error in load_data: {e}")

    # --------------------------------------------------------
    # Display available backup files
    # --------------------------------------------------------
    def show_files(self):
        try:
            print("\nFiles in 'files/' directory:")

            try:
                files = [f for f in list_files() if f != "records.json"]
            except Exception as e:
                raise SmartBudgetError(f"Failed to list files: {e}")

            if not files:
                print(" (No user files found)")
            else:
                for f in files:
                    print(" -", f)
            print()

        except SmartBudgetError as e:
            print(f"❌ File listing error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error in show_files: {e}")

    # --------------------------------------------------------
    # Delete user-selected backup file
    # --------------------------------------------------------
    def delete_backup_file(self):
        try:
            filename = input("Enter filename to delete: ").strip()

            if not filename:
                raise SmartBudgetError("Filename cannot be empty.")

            if filename == "records.json":
                print("❌ Cannot delete system file.\n")
                return

            try:
                result = delete_file(filename)
            except Exception as e:
                raise SmartBudgetError(f"File deletion failed: {e}")

            if result:
                print(f"✔ Deleted '{filename}'\n")
            else:
                print("❌ File not found.\n")

        except SmartBudgetError as e:
            print(f"❌ Delete error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error in delete_backup_file: {e}")
