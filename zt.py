import os
from datetime import datetime
import pandas as pd

# Specify the directory you want to pull files from
directory = 'data/'

# List to store CSV file names and their modification times
csv_file_list = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    print(filename)

# xlsx
df = pd.read_excel(directory+'ATP Donor Report Rework.xlsx', header=6)