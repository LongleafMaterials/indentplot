# -*- coding: utf-8 -*-
"""
Parse hardness or indentation data from raw machine outputs

Created on Sun Nov 17 09:49:55 2024
@author: Colin Fletcher
"""

class TestData:
    def __init__(self, xml, header, measurements):
        # xml - as-parsed data with tabular data (from curves) stored in dataframes
        # header - dataframe containing all header data
        # measurements - dataframe with test results 
        self.xml = xml
        self.header = header
        self.measurements = measurements

# 
# Parse Bruker nanoindentation data, e.g., from PI 89 SEM Picoindenter
#   https://www.bruker.com/en/products-and-solutions/test-and-measurement/nanomechanical-instruments-for-sem-tem/hysitron-pi-89-sem-picoindenter.html
#
# The following files are produced with each test (i.e., indentation):
#    tdm - XML containing details such as version, instrument model, etc.
#    hld - text file containing raw results
#    tdx - unknown, not readable
#
# Function inputs:
#    data_dir - Path to directory containing the test output file(s)
#
#
def brukerTDM(data_dir):
    import os
    import pandas as pd
    import xmltodict
    
    # Read TDM (XML format) as dictionary
    def readXML(file_name, path, extension):
        file_path = path + file_name + '.' + extension
        try:
            with open(file_path, 'rb') as file:
                d = xmltodict.parse(file)
                d = d['usi:tdm']
        except:
            d = 'XML file not found'
        return d

    # Parse header of TDM
    def parseHeader(file_name, path, extension):
        # Read test result file
        file_path = path + file_name + '.' + extension
        with open(file_path) as f:
            text = f.read()
        
        # Split file by lines
        result = text.split('\n')
        
        # Find line where header ends
        end = [i for i in range(0,len(result)) if result[i][:6] == 'Time_s'][0] - 1
        
        # Retain only header information by dropping everything past last line of header
        header = result[:end]
        
        # Store each test parameter in a dictionary except for segment information
        header_dict = {}
        for h in header:
            k, v = h.split(': ')
            # Skip "segment" rows (will be parsed separately)
            if h[:7] == 'Segment':
                continue
            header_dict[k] = v
        
        ## Process segment information
        # Find lines where segment descriptions begin
        segment = [i for i in range(0,len(result)) if result[i][:12] == 'Segment Time']
        
        # Number of rows for each segment
        num_rows = 8
        
        # Parse segment information
        segments = {}
        for s in segment:
            # Select segment information
            segment_data = header[s:s+num_rows]
            
            # Parse segment details into dictionary
            segment_details = {}
            for sd in segment_data:
                k, v = sd.split(': ')
                segment_details[k] = v.strip()
                
            segments[segment_details['Segment Number']] = segment_details
            
        # Add segment details to header dictionary
        header_dict['Segment Definition'] = segments
        
        return header_dict
    
    # Parse curves from test result file
    def parseData(file_name, path, extension):
        # Read test result file
        file_path = path + file_name + '.' + extension
        with open(file_path) as f:
            text = f.read()
        text = text.split('\n')
        
        # Find lines where test data sections begin
        # Should be 3 sections - approach, drift, test
        start = [i for i in range(0,len(text)) if text[i][:6] == 'Time_s'] 
        
        sections = []
        for i in range(len(start)):
            try:
                end = start[i+1]
            except:
                end = len(text)
            sections.append(text[start[i]:end])
            
        ## Convert sections to tabular form as dataframe
        parsed_data = {'approach': None,
                       'drift': None,
                       'test': None}
        # Define separator
        sep = '\t' # tab
        for section, k in zip(sections, parsed_data.keys()):
            # Split each row into a list of delimited text
            test_data = [s.split(sep) for s in section]
         
            # Create dataframe from split data
            df = pd.DataFrame(test_data[1:], columns=test_data[0])
            df = df.dropna()
            
            # Convert columns to numeric
            for c in df.columns:
                df[c] = pd.to_numeric(df[c])
            
            parsed_data[k] = df
        
        return parsed_data
        
    # Perform parsing operations
    def parse(path):
        # Path to data directory
        #path = 'N:\\Samples\\Nanoindentation\\Nanoindentation Data\\Raw Data\\'
        
        # Get list of tests to parse
        to_parse = [f[:-4] for f in os.listdir(path) if f[-3:] == 'hld']
        to_parse = list(set(to_parse))
        to_parse.sort()
        
        # Create dictionary to store test details
        test_info = {}
        test_headers = {}
        test_data = {}
        for f in to_parse:
            test_info[f] = readXML(f, path, 'tdm')
            test_headers[f] = parseHeader(f, path, 'hld')   
            test_data[f] = parseData(f, path, 'hld')
        
        # Compile data to return
        result = {}
        for k in test_data.keys():
            result[k] = {'info': test_info[k],
                         'header': test_headers[k],
                         'data': test_data[k]}
       
        return result

    # Convert XML data to dataframe
    def xml_to_df(xml):
        col_names = ['test',
                     'info',
                     ]
        dataframe = pd.DataFrame

    return parse(data_dir)