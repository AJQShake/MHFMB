"""
"  support.py
"
"  Desc:    INI:  Creates context, message body and sends
"           LOG:  Writes data to a log file
"           SMTP: Creates context, message body and sends email alerts
"           TEST: Tests different function defintions
"
"  Author:  Alex Quigley
"  Ver:     1.0
"  Log:     [20190320] Initial Version
"
"""
# GEN IMPORTS
from os.path import isfile


"""
  ██╗███╗   ██╗██╗
  ██║████╗  ██║██║
  ██║██╔██╗ ██║██║
  ██║██║╚██╗██║██║
  ██║██║ ╚████║██║
  ╚═╝╚═╝  ╚═══╝╚═╝
"""

# IMPORTS
import configparser

# [create] shorthand
def ci(f, h): createINI(f, h)

# Create an empty INI file (overwrites existing)
def createINI(f, h):
  with open(f, 'w') as c: c.write(f"[{h}]")

# Return a ConfigParser Object
def cp():return configparser.ConfigParser()

# [save] shorthand
def wi(f,h,k,v): writeINI(f,h,k,v)

# Save [h] header, [k] key, [v] value to [f] filename
def writeINI(f,h,k,v):
  c=cp(); c.read(f)
  with open(f, 'w') as cfg:
    c[h][k] = v
    c.write(cfg)

# [read] shorthand
def ri(f,h,k): return readINI(f,h,k)

# Read [h] header, [k] key, [v] value to [f] filename
def readINI(f,h,k):
  if isfile(f):
    c=cp(); c.read(f)
    return c[h][k]
  else: return -1

"""
  ██╗      ██████╗  ██████╗
  ██║     ██╔═══██╗██╔════╝
  ██║     ██║   ██║██║  ███╗
  ██║     ██║   ██║██║   ██║
  ███████╗╚██████╔╝╚██████╔╝
  ╚══════╝ ╚═════╝  ╚═════╝
"""

# IMPORTS
from calendar import timegm
from time import gmtime

# Creates and returns EPOCH time in seconds (as STR)
def stamp(): return str(timegm(gmtime()))

# Generates filename for logfile combining [t] type and [f,opt] filename
def gn(t,f=stamp()): return f"{f}.{t}"

# Shorthand of [writeLogfile]
def wl(t, d, f=None): writeLog(t, d, f)

# Writes (append) details to logfile, using [t] type, [d] data, and [f,opt] filename
def writeLog(t, d, f=None):
  if f: f=gn(t, f)
  else: f=gn(t)
  with open(f, 'a+') as file:
    d = stamp() + ": " + d
    file.write(d) 
    file.write('\n')

"""
  ███████╗███╗   ███╗████████╗██████╗
  ██╔════╝████╗ ████║╚══██╔══╝██╔══██╗
  ███████╗██╔████╔██║   ██║   ██████╔╝
  ╚════██║██║╚██╔╝██║   ██║   ██╔═══╝
  ███████║██║ ╚═╝ ██║   ██║   ██║
  ╚══════╝╚═╝     ╚═╝   ╚═╝   ╚═╝
"""
# IMPORTS
import smtplib, ssl

# Get server configuration settings as a dictionary
def setup(f, ts):
  try:
    d = ""; wl('log', "SMTP Setup...", ts)
    if not isfile(f): return wl('err', "Cannot locate initialisation file [{f}]", ts)
    dict =  { 
      'sr' : ri(f,'EMAIL','server'), 
      'pr' : ri(f,'EMAIL','port'), 
      'to' : ri(f,'EMAIL','to'), 
      'fr' : ri(f,'EMAIL','from'), 
      'pw' : ri(f,'EMAIL','password')
    }
    for k,v in dict.items(): wl('log', f" - {k} | {v}", ts)
    wl('log',"SMTP Setup Complete" , ts);  
    return dict
  except:
    wl('log',"SMTP Setup Error Occured", ts)
    wl('err',"SMTP Setup Error", ts)
    return None

# Create a default context
def ctx(): return ssl.create_default_context()

# Create message body
def body(to, m): return f"From: MHFMB\nTo: {to}\nCc: \nSubject: MHFMB SYS ALERT\n\nSYS generated msg:\n\n{m}"
  
# Create SMTP connection using SSL and send email
def send(f, m):
  ts = stamp(); wl('log', f"SMTP Send using {f}", ts)
  try: 
    if isfile(f) == 1:
      s = setup(f, ts)
      with smtplib.SMTP_SSL(s['sr'], s['pr'], context=ctx()) as srv:
        srv.login(s['fr'], s['pw']) 
        srv.sendmail(s['fr'], s['to'], body(s['to'], m))
        srv.quit(); wl('log',"SMTP Alert Sent [{m}]", ts)
        return 1
    wl('log',"Email initialisation file not found", ts); wl('err',"SMTP INI not found \n", ts)
    return None
  except:
    wl('log',"Error occured during SMTP SEND", ts); wl('err',"SMTP Send Error", ts)
    return None
  finally: return 1

"""
████████╗███████╗███████╗████████╗
╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
   ██║   █████╗  ███████╗   ██║
   ██║   ██╔══╝  ╚════██║   ██║
   ██║   ███████╗███████║   ██║
   ╚═╝   ╚══════╝╚══════╝   ╚═╝
"""
# ci('test.ini','TEST'); cp(); wi('test.ini','TEST','filecreated',stamp()); print(ri('test.ini', 'TEST', 'filecreated'))
# wl('TST',"Test data for log")
#ci('test.ini','EMAIL'); 
#wi('test.ini', 'EMAIL', 'server', "smtp.mail.com"); wi('test.ini', 'EMAIL', 'port', "1"); wi('test.ini', 'EMAIL', 'to', "test@email.com")
#wi('test.ini', 'EMAIL', 'from', "donotreply@email.com"); wi('test.ini', 'EMAIL', 'password', "p45sw0r|)")
#setup('test.ini', stamp())
#ctx()
#body('test@email.com',"Test message for email")
#send('test.ini',"Test message for email")

"""
LICENSE:

  The MIT License
  SPDX short identifier: MIT
  
  Copyright <2019> <Alex Quigley>
  
  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
  to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
  and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
  
  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
  
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
  IN THE SOFTWARE.
  
"""

"""
RESOURCES:
  https://docs.python.org/3/library/ssl.html
  https://docs.python.org/3/library/os.path.html
  https://docs.python.org/3/library/configparser.html
  https://docs.python.org/3/library/smtplib.html
  
  https://stackoverflow.com/questions/8884188/how-to-read-and-write-ini-file-with-python3
    
"""
