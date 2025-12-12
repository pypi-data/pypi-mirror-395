import unittest
from unittest.mock import patch
from smartbudget.core_module_2.file_io_data_controller import FileIoDataStorageController
from smartbudget.entity.base_record import SmartBudgetError


def collect_print_output(mock_print):
    """Collect ALL print arguments as output."""
    out = []
    for call in mock_print.call_args_list:
        if call.args:
            out.append(" ".join(str(arg) for arg in call.args))
    return "\n".join(out)



class TestFileIoDataStorageController(unittest.TestCase):

    def setUp(self):
        self.controller = FileIoDataStorageController()

    # --------------------------------------------------------
    # clear_data
    # --------------------------------------------------------
    @patch("smartbudget.core_module_2.file_io_data_controller.clear_json")
    def test_clear_data_yes(self, mock_clear):
        with patch("builtins.input", return_value="y"):
            self.controller.clear_data()
        mock_clear.assert_called_once()

    def test_clear_data_no(self):
        with patch("builtins.input", return_value="n"):
            self.controller.clear_data()

    @patch("smartbudget.core_module_2.file_io_data_controller.clear_json", side_effect=Exception("ERR"))
    @patch("builtins.input", return_value="y")
    def test_clear_data_error(self, mock_input, mock_clear):
        self.controller.clear_data()

    # --------------------------------------------------------
    # save_data
    # --------------------------------------------------------
    @patch("builtins.print")
    def test_save_data_empty_filename(self, mock_print):
        with patch("builtins.input", return_value=""):
            self.controller.save_data()
        out = collect_print_output(mock_print)
        self.assertIn("Save error", out)

    @patch("builtins.print")
    def test_save_data_system_file(self, mock_print):
        with patch("builtins.input", return_value="records.json"):
            self.controller.save_data()
        out = collect_print_output(mock_print)
        self.assertIn("Cannot save to system file", out)

    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=True)
    @patch("builtins.input", side_effect=["backup.json", "n"])
    @patch("builtins.print")
    def test_save_data_overwrite_no(self, mock_print, mock_input, mock_exists):
        self.controller.save_data()
        out = collect_print_output(mock_print)
        self.assertIn("Save cancelled", out)

    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=True)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json", return_value=[{"x": 1}])
    @patch("smartbudget.core_module_2.file_io_data_controller.save_to_json")
    @patch("builtins.input", side_effect=["backup.json", "y"])
    def test_save_data_overwrite_yes(self, mock_input, mock_save, mock_load, mock_exists):
        self.controller.save_data()
        mock_save.assert_called_once()

    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=False)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json", side_effect=Exception("LOAD ERR"))
    @patch("builtins.input", return_value="backup.json")
    @patch("builtins.print")
    def test_save_data_load_error(self, mock_print, mock_input, mock_load, mock_exists):
        self.controller.save_data()
        out = collect_print_output(mock_print)
        self.assertIn("Failed to read", out)

    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=False)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json", return_value=[{"x": 1}])
    @patch("smartbudget.core_module_2.file_io_data_controller.save_to_json", side_effect=Exception("SAVE ERR"))
    @patch("builtins.input", return_value="backup.json")
    @patch("builtins.print")
    def test_save_data_save_error(self, mock_print, mock_input, mock_save, mock_load, mock_exists):
        self.controller.save_data()
        out = collect_print_output(mock_print)
        self.assertIn("Failed to save backup file", out)

    # --------------------------------------------------------
    # load_data
    # --------------------------------------------------------
    @patch("builtins.print")
    def test_load_data_empty_filename(self, mock_print):
        with patch("builtins.input", return_value=""):
            self.controller.load_data([], [])
        out = collect_print_output(mock_print)
        self.assertIn("Load error", out)

    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=False)
    @patch("builtins.input", return_value="nofile.json")
    @patch("builtins.print")
    def test_load_data_file_not_exist(self, mock_print, mock_input, mock_exists):
        self.controller.load_data([], [])
        out = collect_print_output(mock_print)
        self.assertIn("File not found", out)

    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=True)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json", side_effect=Exception("LOAD ERROR"))
    @patch("builtins.input", return_value="bad.json")
    @patch("builtins.print")
    def test_load_data_json_error(self, mock_print, mock_input, mock_load, mock_exists):
        self.controller.load_data([], [])
        out = collect_print_output(mock_print)
        self.assertIn("Failed to load JSON", out)

    # FIXED: Actual behavior → Unexpected error
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=True)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json", return_value=[{"invalid": 1}])
    @patch("builtins.input", return_value="weird.json")
    @patch("builtins.print")
    def test_load_data_bad_records(self, mock_print, mock_input, mock_load, mock_exists):
        self.controller.load_data([], [])
        out = collect_print_output(mock_print)
        self.assertIn("Unexpected error in load_data", out)

    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=True)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json", return_value=[])
    @patch("builtins.input", return_value="ok.json")
    @patch("builtins.print")
    def test_load_data_ok(self, mock_print, mock_input, mock_load, mock_exists):
        incomes, expenses = [], []
        self.controller.load_data(incomes, expenses)
        self.assertEqual(len(incomes), 0)

    # --------------------------------------------------------
    # show_files
    # --------------------------------------------------------
    @patch("smartbudget.core_module_2.file_io_data_controller.list_files", return_value=["a.json", "records.json"])
    @patch("builtins.print")
    def test_show_files(self, mock_print, mock_list):
        self.controller.show_files()
        out = collect_print_output(mock_print)
        self.assertIn("a.json", out)

    @patch("smartbudget.core_module_2.file_io_data_controller.list_files", return_value=[])
    @patch("builtins.print")
    def test_show_files_empty(self, mock_print, mock_list):
        self.controller.show_files()
        out = collect_print_output(mock_print)
        self.assertIn("No user files", out)

    @patch("smartbudget.core_module_2.file_io_data_controller.list_files", side_effect=Exception("ERR"))
    @patch("builtins.print")
    def test_show_files_error(self, mock_print, mock_list):
        self.controller.show_files()
        out = collect_print_output(mock_print)
        self.assertIn("Failed to list files", out)

    # --------------------------------------------------------
    # delete_backup_file
    # --------------------------------------------------------
    @patch("builtins.print")
    def test_delete_backup_empty(self, mock_print):
        with patch("builtins.input", return_value=""):
            self.controller.delete_backup_file()
        out = collect_print_output(mock_print)
        self.assertIn("Delete error", out)

    @patch("builtins.print")
    def test_delete_backup_system_file(self, mock_print):
        with patch("builtins.input", return_value="records.json"):
            self.controller.delete_backup_file()
        out = collect_print_output(mock_print)
        self.assertIn("Cannot delete system file", out)

    @patch("smartbudget.core_module_2.file_io_data_controller.delete_file", return_value=True)
    @patch("builtins.input", return_value="file1.json")
    @patch("builtins.print")
    def test_delete_backup_ok(self, mock_print, mock_input, mock_delete):
        self.controller.delete_backup_file()
        out = collect_print_output(mock_print)
        self.assertIn("Deleted", out)

    @patch("smartbudget.core_module_2.file_io_data_controller.delete_file", return_value=False)
    @patch("builtins.input", return_value="file1.json")
    @patch("builtins.print")
    def test_delete_backup_notfound(self, mock_print, mock_input, mock_delete):
        self.controller.delete_backup_file()
        out = collect_print_output(mock_print)
        self.assertIn("File not found", out)

    @patch("smartbudget.core_module_2.file_io_data_controller.delete_file", side_effect=Exception("ERR"))
    @patch("builtins.input", return_value="file1.json")
    @patch("builtins.print")
    def test_delete_backup_error(self, mock_print, mock_input, mock_delete):
        self.controller.delete_backup_file()
        out = collect_print_output(mock_print)
        self.assertIn("File deletion failed", out)
