# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 09:45:47 2024

@author: Fletcher
"""

# Test data object storing:
#   xml - as-parsed data with tabular data (from curves) stored in dataframes
#   txt_file - path to tabular results text file from Bruker software
class TestData:
    def __init__(self, xml, txt_file):
        self.xml = xml
        self.txt_file = txt_file
        
        # Create dataframe of header data for each indent point
        def parse_header(self):
            import pandas as pd
            xml = self.xml
            
            # Create list of test IDs
            test_ids = list(xml.keys())
            
            # Create dataframe from test headers
            header_df = pd.DataFrame.from_dict({k:v for k, v in zip(test_ids, [xml[v]['header'] for v in list(xml.keys())])}, orient='index')
            
            return header_df
        self.header = parse_header(self)
    
        # Create dataframe with condensed test results
        # NOTE: Attempt to process this from the data itself as alternative to software output
        def parse_results(self):
            import pandas as pd
            txt_file = self.txt_file
            
            # Convert text to dataframe
            processed_data = pd.read_fwf(txt_file)
            processed_data.columns = ['test file name', 'hc (nm)', 'Er (GPa)', 'H (GPa)']
            processed_data = processed_data.dropna()
            processed_data.reset_index(inplace=True, drop=True)
            
            return processed_data
        self.results = parse_results(self)

# Path to working and data directories
wd = 'N:\\Samples\\Nanoindentation\\'
data_dir = wd + 'Nanoindentation Data\\Raw Data\\'

# Add working directory to PATH environment variable
import sys
sys.path.append(wd)

# Test run
import parse
result = parse.brukerTDM('N:\\Samples\\Nanoindentation\\Nanoindentation Data\\Raw Data\\')

test_object = TestData(result, 
                       'N:\\Samples\\Nanoindentation\\Nanoindentation Data\\Processed Data\\E-beam_W.txt')