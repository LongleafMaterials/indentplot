# -*- coding: utf-8 -*-
"""
Object for grouping indentation test data.

@author: Fletcher
"""

# Test data object storing:
#   xml - as-parsed data with tabular data (from curves) stored in dataframes
#   txt_file - path to tabular results text file from Bruker software
#   results - condensed results as a dataframe
class TestData:
    def __init__(self, xml, txt_file):
        self.xml = xml
        self.txt_file = txt_file
        
        # Create dataframe of header data for each indent point
        def parse_header(self):
            import pandas as pd
            import re
            xml = self.xml
            
            # Create list of test IDs
            test_ids = list(xml.keys())
            
            # Create dataframe from test headers
            header_df = pd.DataFrame.from_dict({k:v for k, v in zip(test_ids, [xml[v]['header'] for v in list(xml.keys())])}, orient='index')
            
            # Process numeric columns to remove units from entries and change to numeric format
            # Compile regex expression for identifying numeric columns with units
            r = re.compile(r'(-*\d+\S*[\d]*[e+]*)[ ]*(.*)')
            
            cols = header_df.columns
            new_col_names = {}
            for c in cols:
                # Process column if value format is <number> <units>
                first_row = header_df[c].iloc[0]
                if (type(first_row) == str) and (len(re.findall(r, first_row)) > 0):
                    # Skip date column
                    if ('Time Stamp' in c) or (':' in first_row):
                        continue
                    new_col_names[c] = c + ' (' + re.findall(r, header_df[c].iloc[0])[0][1] + ')'
                    values = [re.findall(r, v)[0][0] for v in header_df[c]]
                    header_df[c] = values
                    header_df[c] = pd.to_numeric(header_df[c])
                
            # Rename all columns                
            header_df.rename(columns=new_col_names, inplace=True)
           
            return header_df
        self.header = parse_header(self)
    
        # Create dataframe with condensed test results
        # NOTE: Attempt to process this from the data itself as alternative to software output
        def parse_results(self):
            import pandas as pd
            import re
            import io
            txt_file = self.txt_file
            
            # Read text file
            txt = open(txt_file).read()
            
            # Remove spaces from end of each line in text file
            txt = '\n'.join([t.rstrip() for t in txt.split('\n')])
            
            # Convert text to dataframe
            processed_data = pd.read_table(io.StringIO(txt), sep=' ', header=None)
            processed_data.columns = ['test file name', 'hc (nm)', 'Er (GPa)', 'H (GPa)']
            processed_data = processed_data.dropna()

            # Set test designation as index
            new_index = [''.join(t.split('.')[:-1]) for t in processed_data['test file name']]
            processed_data.index = new_index
            
            # Add coordinate columns            
            coord_columns = [c for c in self.header.columns if ('Stage' in c) and ('Scratch' not in c)]
            processed_data = processed_data.join(self.header[coord_columns], how='outer')
            
            # Change index to indentation number
            index = processed_data.index
            new_index = []
            pattern = r'.*(\d{4}).*'
            r = re.compile(pattern)
            for i in index:
                indent_number = int(re.findall(r, i)[0])
                new_index.append(indent_number)
            processed_data.index = new_index
            
            # Remove whitespace from beginning or end of column names
            processed_data.columns = [c.lstrip().rstrip() for c in processed_data.columns]
            
            
            return processed_data
        self.results = parse_results(self)


