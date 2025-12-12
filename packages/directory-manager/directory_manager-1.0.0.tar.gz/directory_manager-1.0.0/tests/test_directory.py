import pytest
from pathlib import Path
from typing import List, Union
from pandas import DataFrame
from directory_manager.directory import *

@pytest.fixture(scope="session")
def current_directory():
    app = Directory()
    yield app
    del app


class TestDirectory:
    def test_add_str(self, current_directory : Directory):
        current_directory.add_directories("sub_dir")
        assert "sub_dir" in current_directory

    def test_add_obj(self, current_directory : Directory):
        sub_dir_2 = Directory("sub_dir_2")
        current_directory.add_directories(sub_dir_2)
        assert sub_dir_2 in current_directory
    
    def test_get_sub(self, current_directory : Directory):
        sub_dir = current_directory.get_directory("sub_dir")
        assert sub_dir is not None
        assert sub_dir == "sub_dir"
    
    def test_remove_sub(self, current_directory : Directory):
        current_directory.remove_directory("sub_dir_2")
        assert "sub_dir_2" not in current_directory
        assert len(current_directory) == 1
    
    def test_rename_sub(self, current_directory : Directory):
        sub_dir = current_directory["sub_dir"]
        assert sub_dir is not None
        sub_dir.rename("renamed_sub_dir")
        assert "renamed_sub_dir" == sub_dir
        assert Path("renamed_sub_dir") == sub_dir
        assert Path("renamed_sub_dir") in current_directory
    
    def test_add_new_layer(self, current_directory : Directory):
        current_directory.add_directories("renamed_sub_dir/deep_sub_dir")
        assert "deep_sub_dir" in current_directory
        assert len(current_directory) == 2
    
    def test_clear(self, current_directory : Directory):
        current_directory.clear()
        assert len(current_directory) == 0

class TestFileParser:
    def test_init(self, current_directory : Directory):
        file_1 = FileParser("file.txt")
        file_2 = TextParser("file.txt")
        current_directory.add_files(file_1, file_2)
        assert file_1 is file_2
        assert len(current_directory) == 1
    
    def test_text_file(self, current_directory : Directory):
        file : TextParser = TextParser("temp.txt")
        file.add_line("foo")
        assert file.read(False) == "foo"
        file.overwrite_content("better foo")
        assert file.read(False) == "better foo"
        current_directory.add_files(file)
        assert "temp.txt" in current_directory
    
    def test_json_file(self, current_directory : Directory):
        file : JsonParser = JsonParser("data.json")
        file["name"] = "john"
        file["email"] = "bigjohn@example.com"
        assert file["name"] == "john"
        current_directory.add_files(file)
        assert Path("data.json") in current_directory
    
    def test_csv_file(self, current_directory : Directory):
        file : CsvParser = CsvParser("products.csv")
        file.add_row(["make", "fuel_type", "num_of_doors"])
        file.add_row(["bmw", "gas", 4])
        file.add_row(["chevrolet", "gas", 4])
        file.add_row(["mercedes-benz", "diesel", 4])
        file.set_index("make")
        current_directory.add_files(file)
        file.add_column("body_style", ["sedan", "hatchback", "wagon"])
        assert file["bmw", "fuel_type"] == "gas"
        assert file in current_directory
        assert file[3, "body_style"] == "wagon"

    def test_xlsx_files(self, current_directory : Directory):
        workbook : WorkbookParser = WorkbookParser("data.xlsx")
        sheet = workbook.workbook.active
        sheet.title = "HOWLEESHEET"
        data : List[List[Union[str, int]]] = [["Header_1", "Header_2", "Header_3"],
                                       [10, 20, 30],
                                       [40, 50, 60],
                                       [70, 80, 90],]
        for row in data:
            sheet.append(row)
        assert sheet["A2"].value == 10
        assert sheet["B4"].value == 80

        data_frame : ExcelParser = ExcelParser("df.xlsx")
        data_frame.data = DataFrame(data=data[1:], columns=data[0])
        assert data_frame.data["Header_3"][1] == 60

        current_directory.add_files("data/data.xlsx", "data/df.xlsx")
        assert workbook in current_directory
        assert data_frame in current_directory
        assert len(current_directory) == 7

class TestPathManager:
    def test_split(self):
        path = Path("path/to/trip")
        short_path, name = PathManager.split(path)
        assert short_path == Path("path/to")
        assert name == "trip"

    def test_strip(self):
        path = Path("path/to/file(1).txt")
        stripped_name, n = PathManager.strip(path)
        assert stripped_name == "file.txt"
        assert n == 1

        path = "file(notadigit).txt"
        stripped_name, n = PathManager.strip(path)
        assert stripped_name == "file.txt"
        assert n == -1

        path = "file.txt"
        stripped_name, n = PathManager.strip(path)
        assert stripped_name == "file.txt"
        assert n == -1
    
    @pytest.mark.parametrize("parent, child, return_root, expected",
                             [(Path("part1"), Path("part2"), True, Path("part1/part2")),
                              (Path("part1"), Path("part2"), False, Path("part2")),

                              (Path("part1"), Path("part1/part2"), True, Path("part1/part2")),
                              (Path("part1"), Path("part1/part2"), False, Path("part2")),

                              (Path("part1/part2"), Path("part2"), True, Path("part2/part2")),
                              (Path("part1/part2"), Path("part2"), False, Path("part2")),

                              (Path("part1/part2"), Path("part1"), True, Path("part2/part1")),
                              (Path("part1/part2"), Path("part1"), False, Path("part1")),

                              (Path("part1/part2/part3"), Path("part2/part3"), True, Path("part3/part2/part3")),
                              (Path("part1/part2/part3"), Path("part2/part3"), False, Path("part2/part3")),

                              (Path("part1/part2/part3/part4"), Path("part2/part3"), True, Path("part4/part2/part3")),
                              (Path("part1/part2/part3/part4"), Path("part2/part3"), False, Path("part2/part3")),

                              (Path("part1/part2/part3"), Path("part3/part4"), True, Path("part3/part4")),
                              (Path("part1/part2/part3"), Path("part3/part4"), False, Path("part4")),

                              (Path("part1/part2/part3"), Path("part2/part4/part3"), True, Path("part3/part2/part4/part3")),
                              (Path("part1/part2/part3"), Path("part2/part4/part3"), False, Path("part2/part4/part3")),

                              (Path("part1/part2/part3"), Path("part1/part2/part3/part4"), True, Path("part3/part4")),
                              (Path("part1/part2/part3"), Path("part1/part2/part3/part4"), False, Path("part4")),
                              ])
    def test_set(self, parent, child, return_root, expected):
        new_child_path = PathManager.set(parent=parent, child=child, return_root=return_root)
        assert new_child_path == expected

    @pytest.mark.parametrize("parent, child, expected",
                             [(Path("part1"), Path("part2"), Path("part1/part2")),
                              (Path("part1"), Path("part1/part2"), Path("part1/part2")),
                              (Path("part1/part2"), Path("part2"), Path("part1/part2/part2")),
                              (Path("part1/part2"), Path("part1"), Path("part1/part2/part1")),
                              (Path("part1/part2/part3"), Path("part2/part3"), Path("part1/part2/part3/part2/part3")),
                              (Path("part1/part2/part3/part4"), Path("part2/part3"), Path("part1/part2/part3/part4/part2/part3")),
                              (Path("part1/part2/part3"), Path("part3/part4"), Path("part1/part2/part3/part4")),
                              (Path("part1/part2/part3"), Path("part2/part4/part3"), Path("part1/part2/part4/part3")),
                              (Path("part1/part2/part3"), Path("part1/part2/part3/part4"), Path("part1/part2/part3/part4")),
                              ])
    def test_join_paths(self, parent, child, expected):
        new_child_path = PathManager.join_paths(parent=parent, child=child)
        assert new_child_path == expected

    @pytest.mark.parametrize("original_path, new_path, expected",
                             [(Path("part1/part2/part3"), Path("part2/part3"), True),
                              (Path("part1/part2"), Path("part0/part1/part2"), True),
                              (Path("part1"), Path("part3/part2/part1"), True),
                              (Path("part1/part2/part3"), Path("part3"), True),
                              (Path("part1/part2/part3"), Path("part2/part3/part4"), False),
                              (Path("part1/part2/part3"), Path("part1/part2"), False),
                             ])
    def test_relative(self, original_path, new_path, expected):
        assert PathManager.relative(original_path, new_path) == expected

    @pytest.mark.parametrize("parent, child, True_if_same, expected",
                             [(Path("part1"), Path("part2"), True, False),
                              (Path("part1"), Path("part1/part2"), True, True),
                              (Path("part1/part2"), Path("part2"), True, False),
                              (Path("part1/part2/part3"), Path("part2/part3"), True, False),
                              (Path("part1/part2/part3/part4"), Path("part2/part3"), True, False),
                              (Path("part1/part2/part3"), Path("part3/part4"), True, False),
                              (Path("part1/part2/part3"), Path("part1/part2/part4"), True, False),
                              (Path("part1/part2/part3"), Path("part2/part3"), False, False),
                              (Path("part1/part2/part3"), Path("part1/part2/part3/part4"), True, True),
                              ])
    def test_is_subpath(self, parent, child, True_if_same, expected):
        new_child_path = PathManager.is_subpath(parent=parent, child=child, True_if_same=True_if_same)
        assert new_child_path == expected