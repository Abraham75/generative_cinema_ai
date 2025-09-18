"""
script_parser.py - Simple file reader for screenplay text
"""
def parse_script(file_path):
    with open(file_path, 'r') as file:
        return file.read()
