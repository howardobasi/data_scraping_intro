#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 22:42:30 2023

@author: howardobasi
"""

import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def retrieve_contact_info(url, depth=2):
    if depth == 0:
        return [], []

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    emails = []
    phone_numbers = []

    # Extract emails from the current page
    email_elements = soup.find_all('a', href=lambda href: href and 'mailto:' in href)
    emails = [email.get_text() for email in email_elements]

    # Extract phone numbers from the current page
    phone_elements = soup.find_all('a', href=lambda href: href and 'tel:' in href)
    phone_numbers = [phone.get_text() for phone in phone_elements]

    # Find related links on the current page
    related_links = soup.select('a[href]')

    # Process each related link
    for link in related_links:
        href = link['href']
        absolute_url = urljoin(url, href)

        # Check if the link contains "contact" or "contact us"
        if 'contact' in absolute_url.lower() or 'contact us' in absolute_url.lower():
            # Extract contact info from the related page
            related_emails, related_phone_numbers = retrieve_contact_info(absolute_url, depth - 1)

            # Combine the extracted information from the related page with the current page
            emails.extend(related_emails)
            phone_numbers.extend(related_phone_numbers)

    return emails, phone_numbers

def extract_contact_info_from_csv(csv_path):
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            website_url = row['URL']
            emails, phone_numbers = retrieve_contact_info(website_url)

            # Process or store the retrieved data as per your requirements
            print("Website:", website_url)
            print("Emails:", emails)
            print("Phone Numbers:", phone_numbers)
            print("")

# Provide the path to your CSV file
csv_file_path = 'tools.csv'

# Call the function to extract contact info from websites listed in the CSV
extract_contact_info_from_csv(csv_file_path)





