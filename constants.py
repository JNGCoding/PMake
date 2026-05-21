from typing import Final

VERSION: Final[str] = "1.00b"

HELP: Final[str] = """pmake c/c++ compiler command generator
help section

flags:
_compiler_in_use
_target_extensions
_output_file
_include_subfolders
_optimisation_flag

flag descriptions:
1) _compiler_in_use: string (non null)
brief: specifies which compiler to call ie "gcc" or "g++"
examples:
    e1) _compiler_in_use = gcc
    e2) _compiler_in_use = g++

2) _target_extensions: list (non null)
brief: specifies the extensions which will targeted for compiling
examples:
    e1) _target_extensions = [.c]
    e2) _target_extensions = [.cpp, .c]

3) _output_file: str (nullable)
brief: specifies the output file location and name respective to the root folder (where the .pmake file is located)
default: by default, pmake will generate a main.exe output file in the root folder

examples:
    e1) _output_file = "system application.exe"

4) _include_subfolders: list | str (nullable)
brief: specifies the sub-directories from which the pmake will choose files from, root folder will be always be scanned regardless of _include_subfolders flag
default: by default, _include_subfolders will be "nothing", no sub-directories will scanned

examples:
    e1) _include_subfolders = *
    e2) _include_subfolders = [add, sub, div]
    e3) _include_subfolders = add

5) _optimisation_flag: str (nullable)
brief: specifies any optimisation flag, eg. -O3, -OS to provide to the compiler
default: by default, if not present then no optimisation flags will be given to the compiler

examples:
    e1) _optimisation_flag = -O3
    e2) _optimisation_flag = -O0
"""