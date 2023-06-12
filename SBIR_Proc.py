# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 19:04:31 2023

@author: Konrad Kucharek
"""

'''
Initial Idea : Website Scraper for SBIR.gov contracts recently awarded.
Pulls Contract Name & ID, Company Name & Address and outputs a .CSV file.

Goal : Overall goal is to discover relatively local "Small Business" 
engineering companies that are potentially hiring.

After Exploring The Site : SBIR.gov award data can be downloaded
with or without award abstracts as a .CSV

New Plan : Download the current award data .CSV file (w/o abstracts),
provide the local filepath, process the file and output a filtered 
version of the file as a .CSV.
'''

# Import Library/s
import pandas as pd

'''
# How to obtain the current up-to-date version of the Award Data file :
# Step 1 : SBIR.gov Award Data URL: https://www.sbir.gov/sbirsearch/award/all
# Step 2 : Click on the following hyperlinked text : "without award abstracts (65MB)."

Alternate Standalone Step : Use The File Download Link : 
https://data.www.sbir.gov/awarddatapublic_no_abstract/award_data_no_abstract.csv

NOTE!!! : Award Data file must not be open when executing SBIR_Proc.py program
'''

# Global variable containing the local path to the data file 
# (hard-coded for ease of development process)
#dataPath = r"C:\Users\koolk\Desktop\award_data_no_abstract.csv"

# Obtain file path from user via console
# Tip : To easily obtain the filepath, hold SHIFT + Right Click on the file, 
# and then click "Copy as path" (Located slightly above the cut/copy options)
dataPath = input("Provide the local filepath to the award_data_no_abstract.csv file : ")

# Imports Data File and prepares for processing
def importer(dataPath):
    # Read the .CSV file into a dataframe
    df = pd.read_csv(dataPath, low_memory=False)
    return df

# Deletes specified column/s
def deleteCol(df):
    # List of names of columns that will be deleted
    cols2delete = [
                    'Duns','HUBZone Owned',
                    'Socially and Economically Disadvantaged', 
                    'Women Owned'
                  ]
    df = df.drop(cols2delete, axis = 'columns')
    return df

# Applies filter/s to specified column. 
# Filter/s listed are kept. Everything else is removed
def filterCol(df):
    df = df[df['Program']=='SBIR']
    df = df[df['State']=='CA']
    
    '''
    Create and populate 2 new columns based on the original Zip column.
    The Zip column includes ZIP+4 codes. By separating the main ZIP code
    from the +4, it abstracts this to where less 5-Digit ZIP codes need to
    be included in zipList in order for them to avoid being filtered out by
    this function.
    '''
    df[['Zip1', 'Zip2']] = df.Zip.str.split('-', expand=True)            
    
    # Filter down to specific ZIP Codes
    #df = df[(df['Zip1']=='92128') | (df['Zip1']=='92064')]

    # List of ZIP Codes to be kept (No need to be any sort of ordered list)
    #zipList = ['92128','92064','92129','92021','92081','92121']
    '''
    Next improvement could be enabling the specification of a min and max 
    range of zipcodes so that, for example, only 92021 and 92129 would need
    to be provided to cover all of the codes in the above list to get results
    identical to the current.
    '''
    # A more scalable, adaptive version of the ZIP code filter
    #df = df[df.Zip1.isin(zipList)]
    
    # Range-based ZIP Code fuctionality
    minZip = input("Enter the minimum ZIP code to include : ")
    maxZip = input("Enter the maximum ZIP code to include : ")
    df = df[(df['Zip1'] >= minZip) & (df['Zip1'] <= maxZip)]
    
    return df

# Create and export the resulting processed .CSV   
def exporter(df):
    # Note that, currenly, the processed .CSV will be exported to the
    # directory wherever this program file is stored on the local machine  
    df.to_csv("award_data_no_abstract_processed.csv")
    print()
    print("Output file has been exported")
    
# --------------------------- Function Management ---------------------------
'''
Function calls [after calling importer()] ordered to optimize/minimize 
processing intensity (size of data, etc.).
'''
def Main():
    file = importer(dataPath)
    res1 = deleteCol(file)
    res2 = filterCol(res1)
    exporter(res2)

# Call Main to run the full program
Main()
