from typing import * # pyright: ignore[reportWildcardImportFromLibrary]
import os

class Config(object):
    """
    Parses a pmake file and creates a config object for `CompilerExecutor` object
    to process on and form a command string later to be executed by
    """
    
    @override
    def __init__(self, read_from_file: str | None = None, *args) -> None:
        self.__flags: Final[dict[str, Any]] = {}
        self.__vars: Final[dict[str, Any]] = {}
        self.__argv: Final[tuple[str]] = args
        self.__argc: Final[int] = len(args)
        self.rff: Optional[str] = read_from_file

    @final
    def __expect(self, words: Sequence[str], index: int, next_word: str, if_not_found_callback: Callable, if_found_callback: Callable) -> bool:
        if words[index + 1] != next_word:
            if_not_found_callback()
            return False
        else:
            if_found_callback()
            return True
        
    @final
    def __iterate_list(self, word: str) -> Optional[list]:
        if word[0] != "[":
            raise Exception("Invalid Syntax!, '[' not found!")

        if word[-1] != "]":
            raise Exception("Invalid Syntax!, ']' not found!")
        
        resultant_list: list[str] = []
        dummy_str: str = ""
        for char in word[1:]:
            if char == ",":
                resultant_list.append(dummy_str.strip())
                dummy_str = ""
            elif char == "]":
                resultant_list.append(dummy_str.strip())
                break
            else:
                dummy_str += char

        return resultant_list

    @final
    def __iterate_string(self, word: str) -> Optional[str]:
        try:
            result: Any = word[1 : -1]
            if not isinstance(result, str):
                raise Exception(f"Failed to parse: {word}, Expected DataType: list, Found: {type(word)}")
            else:
                return result
        except Exception as e:
            print(f"Exception:\n{e}")

    @final
    def __iterate_word(self, word: str) -> Optional[str]:
        return word

    @final
    def __iterate_variable(self, word: str) -> Optional[str]:
        if word[1] == "[":
            end_index = 0
            if (end_index := word.find("]")) == -1:
                raise Exception(f"Invalid Syntax: Didn't found ']' in {word}")
            
            value: str | None = self.__vars.get(word[2 : end_index])
            if value is not None:
                return value + word[end_index + 1 : len(word)]
            else:
                raise Exception(f"Variable {word} not defined!")
        else:
            raise Exception(f"Invalid Syntax: Didn't found '[' in {word}")
        
    @final
    def __throw_error(self, exc: str) -> None:
        raise Exception(f"pmake generator parsing error: {exc}")

    @final
    def __parse_line(self, words) -> None:
        if words[0].find("comment", 0, 7) != -1:
            return

        if self.__expect(words, 0, "=", lambda: self.__throw_error("invalid operand found, not '='"), lambda: None):
            if words[0][0] == "#":
                self.__vars[words[0][1:]] = words[2]
            else:
                result: Any = ""

                match words[2][0]:
                    case "[":
                        result = self.__iterate_list(words[2])

                    case "\"":
                        result = self.__iterate_string(words[2])

                    case "$":
                        result = self.__iterate_variable(words[2])

                    case "*":
                        result = "everything"

                    case "~":
                        result = "nothing"

                    case _:
                        result = self.__iterate_word(words[2])

                self.__flags[words[0]] = result

    @final
    def parse(self) -> Self:
        if self.rff is not None:
            fdata: str = ""
            if self.rff is not None:
                with open(self.rff, "r") as file:
                    self.__vars["root"] = os.path.dirname(os.path.abspath(self.rff))
                    fdata = file.read()
            else:
                raise RuntimeError("No pmake file inputted!")
            
            for line in fdata.split("\n"):
                words: list[str] = [word.strip() for word in line.strip().partition("=")]
                if line == "": continue
                self.__parse_line(words)
        
            for arg in self.__argv:
                words: list[str] = [word.strip() for word in arg.strip().partition("=")]
                if arg == "": continue
                self.__parse_line(words)
        else:
            for arg in self.__argv:
                words: list[str] = [word.strip() for word in arg.strip().partition("=")]
                if arg == "": continue
                self.__parse_line(words)

        return self

    @final
    def isAvailable(self, key: str) -> bool:
        return self.__flags.get(key) is not None
    
    @final
    def getFlag(self, key: str) -> (str | None):
        return self.__flags.get(key)
    
    @final
    def getFlags(self) -> dict:
        return self.__flags.copy()
    
    @final
    def getVars(self) -> dict:
        return self.__vars.copy()
    
    def __str__(self) -> str:
        return f"""Config(
    self.argc = {self.__argc}
    self.argv = {self.__argv}
    self.flags = {self.__flags}
    self.vars = {self.__vars}
)
""".strip()
    
    @classmethod
    def CreateConfig(cls, read_from_file: str | None = None, *args) -> Self:
        """
        Creates a fully prepared Config object with arguments parsed
        """
        config = cls(read_from_file, *args)
        config.parse()
        return config
    
    def __call__(self) -> Self:
        return self.parse()