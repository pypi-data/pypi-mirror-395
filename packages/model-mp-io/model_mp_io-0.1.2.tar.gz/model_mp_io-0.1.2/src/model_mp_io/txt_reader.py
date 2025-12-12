import os

class TxtReader:
    def __init__(self, file_path: str = None):
        """
        Initialize the TxtReader class, read the file path and skip the first line of column names, file_path is not a must parameter. Only CSV files are supported.
        """
        self.file_path = file_path
        self.lines = []
        self.number_buffer = []
        if file_path:
            _, ext = os.path.splitext(file_path)
            if ext.lower() != '.csv':
                raise ValueError("Only CSV files are supported.")
            if not os.path.isfile(file_path):
                raise FileNotFoundError("File not found.")
            with open(file_path, 'r') as f:
                lines = f.readlines()[1:]
            self.lines = lines
        else:
            self.lines = []
        self._original_lines = list(self.lines) if self.lines else []
        self._index = 0

    def read_line(self):
        """
        If there are numbers in number_buffer, they will be joined with commas and returned.
        """
        if self.number_buffer:
            result = ','.join(self.number_buffer)
            self.number_buffer = []  
            return result
        
        if self._original_lines:
            result = self._original_lines[self._index].strip()
            self._index = (self._index + 1) % len(self._original_lines)
            return result

    def add_line(self, lines):
        """
        add a single number to number_buffer
        """
        lines_str = str(lines)
        
        if ',' not in lines_str and lines_str.strip().replace('.', '').replace('-', '').isdigit():
            self.number_buffer.append(lines_str.strip())
        else:
            raise ValueError("Invalid line format. Only single numbers are allowed.")
        return self.lines
    
