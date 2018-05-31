import csv as csv

"""
Helper file for ocr.py
Edit to expand functionality beyond just CSVs or to change header name, etc
Todo: un-hardcode from using 'Name' header
Todo: convert to database input rather than csv
Todo: error checking on input type
"""

def fetchNames(dbFileName):
    """
    Return all product names in file
    """
    with open(dbFileName) as csvFile:
        reader = csv.DictReader(csvFile)
        return [(row['UPC'],row['Name']) for row in reader]

def fetchUPCs(dbFileName):
    """
    Return all UPCs in file
    """
    with open(dbFileName) as csvFile:
        reader = csv.DictReader(csvFile)
        return [row['Name'] for row in reader]
