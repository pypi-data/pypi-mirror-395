"""
SmartBudget CLI Application Interface
-------------------------------------
"""

from smartbudget.core_module_2.budget_record_controller import BudgetRecordController
from smartbudget.core_module_2.file_io_data_controller import FileIoDataStorageController
from smartbudget.entity.base_record import SmartBudgetError


# ------------------ Create Controller Instances ------------------ #

rec = BudgetRecordController()
sys = FileIoDataStorageController()


# ------------------ UI Menu ------------------ #

def print_menu():
    print("====================================")
    print("       SmartBudget Main Menu        ")
    print("====================================")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. Show Summary")
    print("4. Show Expense Details")
    print("5. Show Income Details")
    print("6. Backup Records to JSON")
    print("7. List Backup Files")
    print("8. Delete Backup File")
    print("9. Reset Records")
    print("10. Show Expense Chart")
    print("0. Exit")
    print("====================================")


# ------------------ Main Application Loop ------------------ #

def run():
    while True:
        try:
            print_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                try:
                    rec.add_income()
                except SmartBudgetError as e:
                    print(f"❌ Failed to add income: {e}")
                except Exception as e:
                    print(f"❌ Unexpected error: {e}")

            elif choice == "2":
                try:
                    rec.add_expense()
                except SmartBudgetError as e:
                    print(f"❌ Failed to add expense: {e}")
                except Exception as e:
                    print(f"❌ Unexpected error: {e}")

            elif choice == "3":
                try:
                    rec.show_summary()
                except Exception as e:
                    print(f"❌ Cannot display summary: {e}")

            elif choice == "4":
                try:
                    rec.show_expense_details()
                except Exception as e:
                    print(f"❌ Cannot show expense details: {e}")

            elif choice == "5":
                try:
                    rec.show_income_details()
                except Exception as e:
                    print(f"❌ Cannot show income details: {e}")

            elif choice == "6":
                try:
                    sys.save_data()
                except Exception as e:
                    print(f"❌ Failed to save data: {e}")

            elif choice == "7":
                try:
                    sys.show_files()
                except Exception as e:
                    print(f"❌ Cannot list files: {e}")

            elif choice == "8":
                try:
                    sys.delete_backup_file()
                except Exception as e:
                    print(f"❌ Failed to delete file: {e}")

            elif choice == "9":
                try:
                    sys.clear_data()
                except Exception as e:
                    print(f"❌ Failed to clear data: {e}")

            elif choice == "10":
                try:
                    rec.show_expense_plot()
                except Exception as e:
                    print(f"❌ Failed to generate expense chart: {e}")

            elif choice == "0":
                print("\nExiting SmartBudget. Goodbye!\n")
                break

            else:
                print("\n❌ Invalid choice. Try again.\n")

        except KeyboardInterrupt:
            print("\n\n⚠ Interrupted by user. Exiting safely...\n")
            break
        except Exception as e:
            print(f"\n❌ Critical error: {e}\n")
            break
