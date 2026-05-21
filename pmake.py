import sys
import os
from flags import Config
from maker import CompilerExecutor
import constants as consts

config_commands: list[str] = []

argc: int = len(sys.argv)

f: str | None = None

index: int = 1
while index < argc:
    arg = sys.argv[index]

    if arg == "--help" or arg == "--h":
        print(consts.HELP)

    elif arg == "--version" or arg == "--v":
        print(f"pmake c/c++ compiler command generator, version = {consts.VERSION}")

    elif arg == "-f":
        if index + 1 < argc:
            f = sys.argv[index + 1]
            index += 1
        else:
            raise IndexError("expected argument but none was found")

    elif arg == "-pm":
        if index + 1 < argc:
            config_commands.append(sys.argv[index + 1])
            index += 1
        else:
            raise IndexError("expected argument but none was found")

    index += 1

if f is not None:
    CompilerExecutor(Config.CreateConfig(f, *config_commands))()
else:
    print(".pmake file not specified, exiting....")
