import unittest
from unittest.mock import patch
import smartbudget.core_module_2.app_menu_controller as app_menu


class TestAppMenuController(unittest.TestCase):

    @patch("builtins.input", side_effect=["0"])
    def test_exit(self, mock_input):
        app_menu.run()
        mock_input.assert_called_once()

    # ---------------------------------------------------
    # 1 — add_income
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["1", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.rec.add_income")
    def test_add_income(self, mock_add_income, mock_input):
        app_menu.run()
        mock_add_income.assert_called_once()

    # ---------------------------------------------------
    # 2 — add_expense
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["2", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.rec.add_expense")
    def test_add_expense(self, mock_add_expense, mock_input):
        app_menu.run()
        mock_add_expense.assert_called_once()

    # ---------------------------------------------------
    # 3 — show_summary
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["3", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.rec.show_summary")
    def test_show_summary(self, mock_show_summary, mock_input):
        app_menu.run()
        mock_show_summary.assert_called_once()

    # ---------------------------------------------------
    # 4 — show_expense_details
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["4", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.rec.show_expense_details")
    def test_show_expense_details(self, mock_show_exp, mock_input):
        app_menu.run()
        mock_show_exp.assert_called_once()

    # ---------------------------------------------------
    # 5 — show_income_details
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["5", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.rec.show_income_details")
    def test_show_income_details(self, mock_show_inc, mock_input):
        app_menu.run()
        mock_show_inc.assert_called_once()

    # ---------------------------------------------------
    # 6 — sys.save_data()
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["6", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.FileIoDataStorageController.save_data")
    def test_save_data(self, mock_save, mock_input):
        app_menu.run()
        mock_save.assert_called_once()

    # ---------------------------------------------------
    # 7 — sys.show_files()
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["7", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.FileIoDataStorageController.show_files")
    def test_show_files(self, mock_show_files, mock_input):
        app_menu.run()
        mock_show_files.assert_called_once()

    # ---------------------------------------------------
    # 8 — sys.delete_backup_file()
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["8", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.FileIoDataStorageController.delete_backup_file")
    def test_delete_backup_file(self, mock_delete_file, mock_input):
        app_menu.run()
        mock_delete_file.assert_called_once()

    # ---------------------------------------------------
    # 9 — sys.clear_data()
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["9", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.FileIoDataStorageController.clear_data")
    def test_clear_data(self, mock_clear, mock_input):
        app_menu.run()
        mock_clear.assert_called_once()

    # ---------------------------------------------------
    # 10 — rec.show_expense_plot()
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["10", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.rec.show_expense_plot")
    def test_show_expense_plot(self, mock_plot, mock_input):
        app_menu.run()
        mock_plot.assert_called_once()

    # ---------------------------------------------------
    # invalid options
    # ---------------------------------------------------
    @patch("builtins.input", side_effect=["99", "0"])
    @patch("builtins.print")
    def test_invalid_choice(self, mock_print, mock_input):
        app_menu.run()
        txt = "".join(str(c.args[0]) for c in mock_print.call_args_list)
        self.assertIn("Invalid choice", txt)

    @patch("builtins.input", side_effect=["0"])
    @patch("smartbudget.core_module_2.app_menu_controller.print_menu")
    def test_print_menu_called(self, mock_print_menu, mock_input):
        app_menu.run()
        mock_print_menu.assert_called()

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    @patch("builtins.print")
    def test_keyboard_interrupt(self, mock_print, mock_input):
        app_menu.run()
        output = "".join(str(c.args[0]) for c in mock_print.call_args_list)
        self.assertIn("Interrupted", output)

    @patch("builtins.input", side_effect=["10", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.rec.show_expense_plot", side_effect=Exception("x"))
    @patch("builtins.print")
    def test_show_expense_plot_exception(self, mock_print, mock_plot, mock_input):
        app_menu.run()
        out = "".join(str(c.args[0]) for c in mock_print.call_args_list)
        self.assertIn("Failed to generate expense chart", out)

    @patch("builtins.input", side_effect=["9", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.FileIoDataStorageController.clear_data",
           side_effect=Exception("x"))
    @patch("builtins.print")
    def test_clear_data_exception(self, mock_print, mock_clear, mock_input):
        app_menu.run()
        out = "".join(str(c.args[0]) for c in mock_print.call_args_list)
        self.assertIn("Failed to clear data", out)

    @patch("builtins.input", side_effect=["8", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.FileIoDataStorageController.delete_backup_file",
           side_effect=Exception("x"))
    @patch("builtins.print")
    def test_delete_backup_file_exception(self, mock_print, mock_del, mock_input):
        app_menu.run()
        out = "".join(str(c.args[0]) for c in mock_print.call_args_list)
        self.assertIn("Failed to delete file", out)

    @patch("builtins.input", side_effect=["7", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.FileIoDataStorageController.show_files",
           side_effect=Exception("x"))
    @patch("builtins.print")
    def test_show_files_exception(self, mock_print, mock_show, mock_input):
        app_menu.run()
        out = "".join(str(c.args[0]) for c in mock_print.call_args_list)
        self.assertIn("Cannot list files", out)

    @patch("builtins.input", side_effect=["6", "0"])
    @patch("smartbudget.core_module_2.app_menu_controller.FileIoDataStorageController.save_data",
           side_effect=Exception("x"))
    @patch("builtins.print")
    def test_save_data_exception(self, mock_print, mock_save, mock_input):
        app_menu.run()
        out = "".join(str(c.args[0]) for c in mock_print.call_args_list)
        self.assertIn("Failed to save data", out)
