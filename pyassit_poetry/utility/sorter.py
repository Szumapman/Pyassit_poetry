import os
import shutil
import re
from pathlib import Path
from datetime import datetime


class FileSorter:
    def __init__(self) -> None:
        if not Path.exists(Path.home().joinpath("PyAssist")):
            os.mkdir(Path.home().joinpath("PyAssist"))
        self.report_file_path = Path.home().joinpath("PyAssist/sort_report.txt")
        print(self.report_file_path)

        # auxiliary dictionaries to store data on processed files
        self.extensions = {
            "images": set(),
            "documents": set(),
            "audio": set(),
            "video": set(),
            "archives": set(),
            "unsorted": set(),
        }
        self.paths = {
            "images": [],
            "documents": [],
            "audio": [],
            "video": [],
            "archives": [],
            "unsorted": [],
        }

    def _sort_folder(self, path: str):
        """
        The method sorts files in the directory given as an argument and recursively its subdirectories (excluding excluded e.g. documents).
        Empty directories are deleted.
        File names are normalized (all characters other than letters and numbers and _ ) are replaced with: _ .
        If a file or directory with the given name already exists, the character _n (where n is the next number) is added to the name.
        Files with specified extensions are moved to appropriate (created as needed) directories in the directory in which they are located
        (e.g., files with .doc extensions are moved to the documents folder, files with .zip extensions are moved to the archives directory, etc.)
        Files with unknown extensions are not moved, but have a normalized name.
        Archives, after being moved to the archives directory, are unzipped to the directory with the name of the archive being unzipped
        (without the extension).
        For each directory, the function saves in the report file (whose name is passed as the second argument), the results of its work.

        Directories to which files with given extensions are moved:
        images -> .jpeg | .png | .jpg | .svg
        video -> .avi | .mp4 | .mov | .mkv
        documents -> .doc | .docx | .txt | .pdf | .xlsx | .pptx
        audio -> .mp3 | .ogg | .wav | .amr
        archives -> .zip | .gz | .tar

        :param path: string with path to directory to be sorted
        :type path: str
        :param report_file_path: name of report file
        :type report_file_path: str
        :raise FileNotFoundError: if source path lead to non-existing directory
        :raise NotADirectoryError: if source path lead to file
        :raise FileExistsError: if too many files versions (over 1 000 000) exists in folder
        """
        # list of files and directories located in a given directory
        files = list(os.scandir(path))
        for file in files:
            # I check if it's a directory, if so I normalize its name and recursively call the sort_folde function
            if file.is_dir():
                # removal of empty directoriesw
                temp_list = list(os.scandir(file.path))
                if len(temp_list) == 0:
                    os.rmdir(file.path)
                # skip directories which are excluded from sorting
                if not file.name in [
                    "images",
                    "video",
                    "documents",
                    "audio",
                    "archives",
                ]:
                    dir_name = self._normalize(file.name)
                    dir_path = os.path.join(path, dir_name)  # Path(path, dir_name)
                    # I check if there was a change in the directory name after using the normalize function, and if so I move the contents to the directory with the new name
                    if dir_name != file.name:
                        # I check if a directory does not already exist that would conflict with the new name, if so I add a numbered version
                        for entry in files:
                            if dir_name == entry.name:
                                dir_path = self._set_dest_path(
                                    os.path.join(path, dir_name)
                                )

                        # I move the contents of the renamed directory
                        try:
                            os.renames(os.path.join(path, file.name, dir_path))
                        except FileExistsError:
                            print(
                                f"Directory {dir_name} has not been copied, because too many directories with that name already exist."
                            )
                            continue

                    # recursive function call for non-empty directories
                    self._sort_folder(dir_path)

            # file operations
            else:
                file_name, ext = os.path.splitext(file.name)
                file_name = self._normalize(file_name)
                file_type = ""
                match ext:
                    case ".jpeg" | ".png" | ".jpg" | ".svg":
                        file_type = "images"
                    case ".avi" | ".mp4" | ".mov" | ".mkv":
                        file_type = "video"
                    case ".doc" | ".docx" | ".txt" | ".pdf" | ".xlsx" | ".pptx":
                        file_type = "documents"
                    case ".mp3" | ".ogg" | ".wav" | ".amr":
                        file_type = "audio"
                    case ".zip" | ".gz" | ".tar":
                        file_type = "archives"
                        # archive is immediately extracted to the folder: archives/"archive name without extension"
                        shutil.unpack_archive(
                            os.path.join(path, file.name),
                            os.path.join(path, file_type, file_name),
                        )
                    case _:
                        file_type = "unsorted"

                # I move files (except those with unaccounted-for extensions) to the appropriate directories
                if file_type != "unsorted":
                    dest_path = self._set_dest_path(
                        os.path.join(path, file_type), file_name, ext
                    )
                    try:
                        os.renames(os.path.join(path, file.name), dest_path)
                    except FileExistsError:
                        print(
                            f"File {file_name}{ext} has not been copied, because too many files with that name already exist in the destination directory."
                        )
                        continue

                # adds information about the paths of processed files and their extensions to dicts paths and extensions
                if self.paths.get(file_type) != None:
                    temp_list = self.paths.get(file_type)
                    if file_type == "unsorted":
                        temp_list.append(os.path.join(path, file_type, file.name))
                    else:
                        temp_list.append(
                            f"{os.path.join(path, file_type, file.name)} has moved to: {dest_path}"
                        )
                    self.paths.update({file_type: temp_list})
                if self.extensions.get(file_type) != None:
                    temp_set = self.extensions.get(file_type)
                    temp_set.add(ext)
                    self.extensions.update({file_type: temp_set})

        self._create_report(path)

    def _normalize(self, name: str) -> str:
        """
        The function normalizes the passed string so that Polish characters are converted to Latin characters,
        and characters other than Latin letters, digits and _ , are converted to _ .

        :param name: The variable with string to normalize
        :type name: str
        :rtype: str
        """
        # Auxiliary dict for the translate() function
        polish_chars = {
            ord("ą"): "a",
            ord("Ą"): "A",
            ord("ć"): "c",
            ord("Ć"): "C",
            ord("ę"): "e",
            ord("Ę"): "E",
            ord("ł"): "l",
            ord("Ł"): "L",
            ord("ń"): "n",
            ord("Ń"): "N",
            ord("ó"): "o",
            ord("Ó"): "O",
            ord("ś"): "s",
            ord("Ś"): "Ś",
            ord("ź"): "z",
            ord("Ż"): "Z",
            ord("ż"): "z",
            ord("Ż"): "Z",
        }
        # I change Polish characters to Latin equivalents on the basis of dict: polish_chars
        normalized_name = name.translate(polish_chars)
        # I change other disallowed characters in the name to the _ character
        normalized_name = re.sub(r"\W+", "_", normalized_name)
        return normalized_name

    def _set_dest_path(self, path: str, file_name: str, ext="") -> str:
        """
        A helper function for creating file and directory names.

        :param path: Path to directory
        :type path: str
        :param file_name: Destination directory/file (without extension) name
        :type file_name: str
        :param ext: The extension for file or empty for directory
        :type ext: str
        :rtype: str
        """
        # I check if the given file / directory does not already exist in dest_folder
        full_file_name = f"{file_name}{ext}"
        if os.path.exists(os.path.join(path, full_file_name)):
            # if the file / directory already exists in subsequent versions in dest_folder adds to its name "_n" where i is the first free number from 1 to 1000000
            for i in range(1, 1000000):
                if not os.path.exists(f"{path}{file_name}_{i}{ext}"):
                    file_name += f"_{i}"
                    break
        full_file_name = f"{file_name}{ext}"
        return os.path.join(path, full_file_name)

    def _create_report(self, path: str):
        """
        The function saves a report with the extensions and files used.

        :param extensions: dict where keys are file categories and values are set with extensions used
        :type extensions: dict
        :param paths: dictionary where the keys are file categories and the values are a list of file paths on which sorting was performed
        :type paths: dict
        :param path: path to the directory on which sorting is performed
        :type path: str
        :param report_file_path: the name of the file to which the report is saved
        :type report_file_path: Path
        """
        now = datetime.now()
        with open(self.report_file_path, "a") as fo:
            fo.write(
                f"{3*'>'} Activity report for directory: {path} - {now.strftime('%Y-%m-%d %H:%M:%S')}:\n"
            )

            # I check to see if there will be information in the given directory to write in the report
            contain_data_to_report = False
            for value in self.extensions.values():
                if len(value) > 0:
                    contain_data_to_report = True
            # if there is data to record I save it
            if contain_data_to_report:
                fo.write(f"Extensions of checked files by category:\n")
                no_transfered_data = True
                for key, values in self.extensions.items():
                    if len(values) > 0:
                        no_transfered_data = False
                        values = list(values)
                        fo.write(f"{key}: {' | '.join(values)};\n")
                if no_transfered_data:
                    fo.write(f"{3*'-'}")
                fo.write(f"\nFiles sorted by category:\n")
                for key, values in self.paths.items():
                    if len(values) > 0:
                        no_transfered_data = False
                        fo.write(f"{key}:\n")
                        for value in values:
                            fo.write(f"{value};\n")
                if no_transfered_data:
                    fo.write(f"{3*'-'}")
                fo.write(f"\n{20*'-'}\n\n")
            else:
                fo.write("Nothing to sort.\n")

    def sort(self, path: str):
        if not os.path.exists(os.path.dirname(path)) or not os.path.isdir(path):
            return f'"{path}" is not a proper folder path, try again.'
        # the name of the file to which the report is saved (the report is saved in the main folder of sorted directory)
        self._sort_folder(path)
        return f"I've sorted your files in {path}.\nReport file is here: {self.report_file_path}"
