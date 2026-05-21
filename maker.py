from typing import * # pyright: ignore[reportWildcardImportFromLibrary]
from flags import Config
import os
import sys

def get_last_index_of(path: str, delim: str) -> int:
    """
    Get the last index of the delimeter provided in the path
    """

    for index, char in enumerate(path[::-1]):
        if char == delim:
            return len(path) - index - 1
    return -1

def clean_path(path: str) -> str:
    """
    Clean any path errors, if available and return the cleaned path
    """

    return path.strip().replace("/", "\\")

class CompilerExecutor(object):
    """
    Instead of loading all of the work load on the Config class, This class
    is responsible for the actual conversion of the C/C++ project to .exe file
    """

    @override
    def __init__(self, compilerConfig: Config) -> None:
        self.config: Config = compilerConfig
        print(self.config)

        self.execute_string: str = ""

    @final
    def __add_flag(self, key: str) -> None:
        value: str = self.__get_flag(key)
        self.__add_value(value)

    @final
    def __add_value(self, value: str) -> None:        
        if len(self.execute_string) == 0:
            self.execute_string += value
        else:
            if self.execute_string[-1] != " ":
                self.execute_string += " " + value

    @final
    def __get_flag(self, key: str) -> str:
        value: str | None = self.config.getFlag(key)
        if value is not None:
            return value # type: ignore
        else:
            raise ValueError(f"\"{key}\" config key is not provided within the config")
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.__add_flag("_compiler_in_use")

        if self.config.isAvailable("_optimisation_flag"):
            self.__add_flag("_optimisation_flag")

        includefiles: List[str] = []

        parent_path: str = self.config.getVars()["root"]
        paths: Iterator = os.walk(parent_path)

        include_folders: str = "nothing"

        if self.config.isAvailable("_include_subfolders"):
            include_folders = self.__get_flag("_include_subfolders")

        #*--------------------------------------------------------------------------------*#
        def match_extensions(file: str) -> bool:
            file_ext_index = get_last_index_of(file, ".")
            file_extension: str = file[file_ext_index:] if file_ext_index >= 0 else ""
            return file_extension in self.__get_flag("_target_extensions")
        #*--------------------------------------------------------------------------------*#

        if isinstance(include_folders, str):
            if include_folders == "nothing":
                for file in (steps := next(paths))[2]:
                    if match_extensions(file):
                        includefiles.append(f"\"{steps[0]}\\{file}\"")

            elif include_folders == "everything":
                for steps in paths:
                    for file in steps[2]:
                        if match_extensions(file):
                            includefiles.append(f"\"{steps[0]}\\{file}\"")

            else:
                for file in (steps := next(paths))[2]:
                    if match_extensions(file):
                        includefiles.append(f"\"{steps[0]}\\{file}\"")

                try:
                    folder: str = ""
                    while (folder := next(paths))[0] != clean_path(f"{parent_path}\\{include_folders}"):
                        pass

                    for file in (steps := folder)[2]:
                        if match_extensions(file):
                            includefiles.append(f"\"{steps[0]}\\{file}\"")
                except StopIteration:
                    print(f"warning: include directory '{include_folders}' not found")
                except:
                    print("internal unknwown fatal error, exiting...")
                    sys.exit(0)


        elif isinstance(include_folders, list):
            for file in (steps := next(paths))[2]:
                if match_extensions(file):
                    includefiles.append(f"\"{steps[0]}\\{file}\"")

            folders_seen: List[str] = []
            
            for steps in paths:
                if steps[0] in [clean_path(f"{parent_path}\\{folder}") for folder in include_folders]:
                    folders_seen.append(steps[0])

                    for file in steps[2]:
                        if match_extensions(file):
                            includefiles.append(f"\"{steps[0]}\\{file}\"")

            for folder in include_folders:
                if clean_path(f"{parent_path}\\{folder}") not in folders_seen:
                    print(f"warning: include directory '{folder}' not found")
        else:
            raise TypeError(f"\"_include_subfolders\" value is neither a string nor list")

        for file in includefiles:
            self.__add_value(clean_path(file))
        
        self.__add_value("-o")
        self.__add_value( clean_path(f"\"{parent_path}\\{self.__get_flag("_output_file")}\"") ) if self.config.isAvailable("_output_file") else self.__add_value(f"\"{parent_path}\\main.exe\"")
        
        print(self.execute_string)
        os.system(self.execute_string)

        return self.execute_string