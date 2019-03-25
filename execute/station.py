"""
"  station.py
"
"  Desc:    ROW CLASS: Loads and manipules dictionary elements to output clean csv data
"
"  Author:  Alex Quigley
"  Ver:     1.0
"  Log:     [20190320] Initial Version
"
"""

# Imports
import json

class row:

  def __init__(
    self=None, id=None, contract=None, name=None, addr=None, geo=None, 
    bank=None, bonus=None, status=None, update=None, conn=None, overflow=None, 
    shape=None, totalst=None, mainst=None, overflowst=None
  ):

    self.id = id;  self.contract = contract; self.name = name
    self.addr = addr; self.bank = bank; self.bonus = bonus; self.status = status; self.update = update 
    self.conn = conn;  self.shape = shape; self.overflowst = overflowst
    self.mainst = mainst; self.m_cap = 0; self.m_bikes = 0; self.m_stands = 0
    self.totalst = totalst; self.t_cap = 0; self.t_bikes = 0; self.t_stands = 0
    self.overflow = overflow; self.o_cap = 0; self.o_bikes = 0; self.o_stands = 0
    self.geo = geo; self.lat = None; self.lng = None
    
  # Return CSV data as a string
  def getCSV(self):

    s = self.contract.lower()
    s = s + "," + self.status.lower()
    s = s + "," + str(self.id)
    s = s + "," + self.update
    s = s + "," + self.conn
    s = s + "," + self.overflow
    s = s + "," + str(self.t_cap)
    s = s + "," + str(self.t_bikes)
    s = s + "," + str(self.t_stands)
    s = s + "," + str(self.m_cap)
    s = s + "," + str(self.m_bikes)
    s = s + "," + str(self.m_stands)
    s = s + "," + str(self.o_cap)
    s = s + "," + str(self.o_bikes)
    s = s + "," + str(self.o_stands)

    return s

  # Provides header info
  def getHeader(self):
    return "contract,status,id,update,conn,overflow,t_cap,t_bikes,t_stands,m_cap,m_bikes,m_stands,o_cap,o_bikes,o_stands\n"
      
  # Accepts a dictionary (need to add error handling and testing)
  def load(self, element):

    self.contract = element['contractName']
    self.id = element['number']
    self.name = element['name']
    self.addr = element['address']
    self.geo = element['position']
    self.status = element['status']
    self.update = element['lastUpdate']
    self.totalst = element['totalStands']
    self.mainst = element['mainStands']
    self.bank = 'T' if element['banking'] else 'F'
    self.bonus = 'T' if element['bonus'] else 'F'
    self.conn = 'T' if (element['connected']) else 'F'
    self.overflow = 'T' if element['overflow'] else 'F'
    self.overflowst = element['overflowStands']
    self.shape = "none" if not element['shape'] else str(element['shape'])

    while self.totalst and self.mainst:
      self.t_cap = self.totalst['capacity'] 
      self.t_bikes = self.totalst['availabilities']['bikes'] 
      self.t_stands = self.totalst['availabilities']['stands'] 
      self.m_cap = self.mainst['capacity'] 
      self.m_bikes = self.mainst['availabilities']['bikes'] 
      self.m_stands = self.mainst['availabilities']['stands'] 
      break

    while self.geo:
      self.lat = self.geo['latitude'] 
      self.lng = self.geo['longitude']
      break
    
    if self.overflowst:
      self.o_cap = self.overflowst['capacity']
      self.o_bikes = self.overflowst['availabilities']['bikes'] 
      self.o_stands = self.overflowst['availabilities']['stands'] 
    else:
      self.o_cap = self.o_bikes = self.o_stands = 0

    
    
