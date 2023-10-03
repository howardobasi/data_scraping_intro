#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 18:59:09 2023

@author: howardobasi
"""

import os
import json
import csv
from haralyzer import HarParser

# Set the folder path where the HAR files are located
folder_path = '/Users/howardobasi/Desktop/Coding scripts'

# Get a list of all HAR files in the folder
har_files = [file for file in os.listdir(folder_path) if file.endswith('.har')]

for har_file_name in har_files:
    # Load the HAR file
    har_file_path = os.path.join(folder_path, har_file_name)
    har_parser = HarParser.from_file(har_file_path)

    # Extract the website URLs from the "text" field under the "content" key
    urls = []
    for entry in har_parser.har_data['entries']:
        response = entry.get('response', {})
        content = response.get('content', {}).get('text')
        if content is not None:
            try:
                data = json.loads(content)
                page = data.get('data', {}).get('page', {})
                websites = page.get('websites', [])
                urls.extend(websites)
            except (json.JSONDecodeError, AttributeError, KeyError):
                pass

    # Generate the CSV file name based on the HAR file name
    csv_file_name = os.path.splitext(har_file_name)[0] + '.csv'
    csv_file_path = os.path.join(folder_path, csv_file_name)

    # Convert the data to CSV
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['URL'])
        for url in urls:
            writer.writerow([url])

    print("Conversion completed successfully!")
