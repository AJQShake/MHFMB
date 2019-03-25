"""
"  extract_data.py
"
"  Desc:    MAIN: Requests from API defined in INI, through context file which also transforms data to CSV
"           Stores return JSON as CSV to 'data' folder 
"
"  Author:  Alex Quigley
"  Ver:     1.0
"  Log:     [20190320] Initial Version
"
"""

# Imports
from support import support as sp
from support import context
from support import station
import requests
import json

# MAIN function to extract data
def extract_data():
  
    # Setup context
    i = 0.1; ts = sp.stamp()
    ctx = context.get()
    row = station.row()
  
    # Create output filename
    output = ctx['fld'] + "DATA_" + ts + ".csv"
    logfile = ctx['log'] + "extraction"

    # Log status
    sp.wl('log', "Created Context, attempting api request..." , logfile)

    try:
      # Request from API
      i = 0.2; raw = requests.get(ctx['api'])
      status = str(raw.status_code)

      # Log
      sp.wl('log', "API Status : " + status , logfile)

      # If status not 200 (ok) then exit
      if not raw.status_code == 200:
        sp.wl('err', "API Access error [" + status + "]")
        exit()

      # log
      sp.wl('log', "Loading to datastore...", logfile)

      # Load JSON data to a dataframe
      i = 0.3; dataframe = json.loads(raw.text)

      # Open output, load dataframe items and write as csv 
      with open(output,'w') as f:
        f.write(row.getHeader())
        for item in dataframe:
          i = 0.4; row.load(item)
          f.write(row.getCSV())
          f.write("\n")

      # Log
      sp.wl('log', "COMPLETE", logfile)

    except:
      msg = str(i) + " Error occured during extraction"
      sp.wl('err', msg, logfile)
      sp.send(ctx['prv'], msg)

# Execute main function
extract_data()
