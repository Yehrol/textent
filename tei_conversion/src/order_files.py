# -----------------------------------------------------------
# Code by: Kelly Christensen
# Python class to organize the file paths in the data directory.
# -----------------------------------------------------------

import re
from collections import namedtuple

class Files:
    def __init__(self, document, filepaths):
        self.d = document
        self.fl = filepaths  # list
        #print("ORDERED: ",self.d)
        #print("ORDERED: ",self.fl)

    def order_files(self):
        File = namedtuple("File", ["num", "filepath"])
        #print(File)
        ordered_files = sorted([File(int(re.search(r"(\d+).xml$", f).group(1)), f)for f in self.fl])
        return ordered_files
