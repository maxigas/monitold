#!/usr/bin/python3
# linedump.py

# Linedump is a format for visualising monitoring information as a line of chars.
# It is designed to be easy to parse for both humans and machines.
# It can be used for simple shell programs, interactive CLI applications or in logs.

# Default linedump format:
#
# - A linedump is a string with a predetermined number of chars
# - New linedumps are made up of placeholder chars for "undefined"
# - Each char represents a state
# - Chars are added one by one to a given position
# - If all chars are added the linedump is printed to standard output
# - Each char has a corresponding key
# - Key can be invoked to get details about the state described by char
# - Keys are ASCII printable characters, 33 to 126 (93 total)

# Default character format:
#
# _ => Undefined: Placeholder
# . => Good: Host is up to date
# ! => Bad: Host is outdated
# ? => Unknown: Host cannot be analysed
# ¿ => Unreachable: Host cannot be reached


def keypos(x):
    "Multimethod for resolving key to pos or pos to key."""
    # DEBUG:
    # print("Keypos:", x)
    if isinstance(x, str) and len(x) is 1: return ord(x) - 33
    elif isinstance(x, int): return chr(x + 33)
    else: return False


def linedumpkeys(linedump):
    """Expects a linedump string and returns a string of corresponding keys"""
    assert (len(linedump) < 126), "Linedumps are maximum 126 char long."
    return "".join([keypos(x) for x in range(len(linedump))])


def newlength(length=1):
    """Define a closure that stores the length of the linedump."""
    return lambda: length


def newlinedump():
    """Gather characters and if all are set, print them on a line."""
    chars = "_"*length()
    
    def linedump(char, pos=False):
        nonlocal chars
        # If position is not supplied then take the first placeholder's:
        pos = pos if pos else chars.find("_")
        # If abstract values are supplied, turn them into canonical chars:
        if not isinstance(char, str):
            if char is True: char = "."
            elif char is False: char = "!"
            else: char = "?"
        # Replace character at pos in chars with char:
        chars = chars[0:pos] + char + chars[pos+1:]
        # Debug:
        print("DEBUG:", chars)
        # If there are no placeholders left, print linedump:
        if not "_" in chars: print(chars); print(linedumpkeys(chars))

    return linedump
