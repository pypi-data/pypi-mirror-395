from importlib import import_module

from . import CLI_NAME, MODULE_NAME

# Test target module import
main = import_module(f"{MODULE_NAME}.{CLI_NAME}").main


if __name__ == "__main__":
    main()
