import builtins
from rich import print as rich_print

# Override Python’s built-in print globally
builtins.print = rich_print
