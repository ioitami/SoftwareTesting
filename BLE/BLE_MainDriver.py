#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import asyncio
import os
import signal
import afl



def read_lines_from_file(filename):
    """
    Reads lines from the specified file and returns a generator.
    """
    with open(filename, "r") as file:
        for line in file:
            yield line.strip()

def write_lines_to_file(filename, lines):
    """
    Appends lines to the specified file.
    """
    with open(filename, "a") as file:
        for line in lines:
            file.write( "\n"+line )
    return lines[0]

def remove_line_from_file(filename, line_to_remove):
    """
    Removes the first occurrence of a specific line from the specified file.
    """
    with open(filename, "r") as file:
        lines = file.readlines()

    with open(filename, "w") as file:
        removed = False
        for line in lines:
            if not removed and line.strip() == line_to_remove:
                removed = True
                continue  # Skip writing the line to remove
            file.write(line)


#HOW THE CODE SHOULD BE RUN
# def main():
#     filename = "filename.txt"  # Predefined filename
#     line_reader = read_lines_from_file(filename)
#     while True:
#         input_line = next(line_reader)
#         print(input_line)
#         mod_input="Test2ed"
#         remove_line_from_file(filename, input_line)  # Remove from file
        
#         write_lines_to_file(filename, [mod_input])  # Write to the same file
#         break



# -----------------------------------------------------------------------------
    
#logging.basicConfig(level=os.environ.get('BUMBLE_LOGLEVEL', 'INFO').upper())
#asyncio.run(main(a))
    
# 1. Read Line (input) from txt file,

filename = ""

line_reader = read_lines_from_file(filename)

while True:
    input_line = next(line_reader)
    print(input_line)
    mod_input="Test2ed"
    remove_line_from_file(filename, input_line)  # Remove from file
    
    write_lines_to_file(filename, [mod_input])  # Write to the same file
    break
# 2. input into run_ble_tester.py

# 3. lcov.info is now created after run_ble_tester finishes running, 
# read that with whatever other code. Then, run 1. again

# asyncio.run(main())
#p.kill()
os._exit(0)