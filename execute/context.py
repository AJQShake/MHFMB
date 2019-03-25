"""
"  context.py
"
"  Desc:    Looks at a local settings file for values to determine storage location, 
            api key values and other data
"
"  Author:  Alex Quigley
"  Ver:     1.0
"  Log:     [20190320] Initial Version
"
"""
# Imports
from support import support as sp

# Shorthand for testFile()
def tf(f,e): return testFile(f,e)

# Tests to see if a file INI exists
def testFile(f,e): 
  if not sp.isfile(f): 
    sp.wl('err', str(e)+" File not found ["+f+"]"); exit()
  return f

# Shorthand for getContext()
def get(): return getContext()

# Assigns ini values to a dictionary for ease of access in extract_data file
def getContext():
  try:
    ctx = {}
    i = 0.1; ctx['lcl'] = lcl = tf("settings.ini", i)
    i = 0.2; ctx['fld'] = sp.ri(lcl,'DATA','folder')
    i = 0.3; ctx['log'] = sp.ri(lcl,'LOGS','folder')
    i = 0.4; prv = sp.ri(lcl,'PRIVATE','filename')
    i = 0.5; ctx['prv'] = tf(prv, i)
    i = 0.6; ctx['api'] = sp.ri(prv,'API','url') + sp.ri(prv,'API','key')
    return ctx
  except:
    sp.wl('err', str(i)+" Error creating context"); exit()
