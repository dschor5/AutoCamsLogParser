import numpy as np
import matplotlib.pyplot as plt
from .CAMSConstants import *

class Archive(np.ndarray):

   # Definition of field types
   TYPE_KEYS = [
      (I_MET,          ENTRY_TYPE_INT), 
      (I_OSMET,        ENTRY_TYPE_LNG), 
      (I_CABIN_O2,     ENTRY_TYPE_FLT), 
      (I_CABIN_P,      ENTRY_TYPE_FLT), 
      (I_CABIN_T,      ENTRY_TYPE_FLT), 
      (I_CABIN_CO2,    ENTRY_TYPE_FLT), 
      (I_CABIN_H,      ENTRY_TYPE_FLT), 
      (I_TANK_O2,      ENTRY_TYPE_FLT), 
      (I_TANK_N2,      ENTRY_TYPE_FLT), 
      (I_EVENT_SOURCE, ENTRY_TYPE_STR), 
      (I_EVENT_DESC,   ENTRY_TYPE_OBJ), 
      (I_ERROR_PHASE,  ENTRY_TYPE_STR), 
      (I_ID,           ENTRY_TYPE_INT), 
      (I_LOG_TYPE,     ENTRY_TYPE_STR)  
   ]  

   def __new__(cls, filename, max_rows=None):
      
      # Converter functions to interpret string fields read.
      # All the fields need to be decoded for UTF-8 character sets 
      # before they are parsed and evaluated in the array.
      # String  - decoding only.
      toStr = lambda x: x.decode('utf-8')
      # Object  - treat as string. Allows flexibility for later.
      toObj = lambda x: x.decode('utf-8')
      # Integer - Type cast to an integer.
      toInt = lambda x: int(x.decode('utf-8')) 
      # Float   - Type cast, then change from European to American
      #           notation for decimals before casting the value. 
      toDbl = lambda x: float(x.decode('utf-8').replace(',', '.'))
         
      # Map converter functions for each field.
      # Matches variable types defined in TYPE_KEYS.
      converters = {
         I_MET          : toInt, 
         I_OSMET        : toInt,
         I_CABIN_O2     : toDbl,
         I_CABIN_P      : toDbl,
         I_CABIN_T      : toDbl,
         I_CABIN_CO2    : toDbl,
         I_CABIN_H      : toDbl,
         I_TANK_O2      : toDbl,
         I_TANK_N2      : toDbl,
         I_EVENT_SOURCE : toStr,
         I_EVENT_DESC   : toObj,
         I_ERROR_PHASE  : toStr,
         I_ID           : toInt,
         I_LOG_TYPE     : toStr
         }
      
      # List of names for each column.
      names = list(converters.keys())
      
      # Constants used in parsing the file.
      delimChar   = ';'
      commentChar = '#'

      # Read file 
      array = np.genfromtxt(
         fname          = filename,          # File name to get archive.                \
         names          = names,             # Assign column names                      \
         dtype          = Archive.TYPE_KEYS, # Variable type for each field             \
         delimiter      = delimChar,         # Delimiter within archive                 \
         converters     = converters,        # Convert data using lambda functions      \
         comments       = commentChar,       # Discard comment lines                    \
         loose          = False,             # Raise errors if invalid values are read. \
         max_rows       = max_rows           # Maximum number of rows to read from file.\
         )
         
      # Define the array and add the internal parameters.
      obj = array.view(cls)
      obj.__filename = filename
      obj.__script = None
      obj.__parseDesc = False
      return obj


   def __array_finalize__(self, obj):
      if obj is None: 
         return
      self.__filename = getattr(obj, '__filename', None)
      self.__script = getattr(obj, '__script', None)
      self.__parseDesc = getattr(obj, '__parseDesc', None)


   def getScript(self):
      if(None == self.__script):
         try:
            with open(self.__filename, "r") as fp:
               line          = fp.readline().strip()
               scriptPath    = line.split(':')[-1]
               scriptName    = scriptPath.split('\\')[-1]
               self.__script = scriptName
         except IOError:
            raise Exception("Could not read file: ", self.__filename)
      result = self.__script
      return self.__script
   
   def getPeriodic(self):
      return self[...][self[I_LOG_TYPE] == ENTRY_TYPE_PERIODIC]
      
   def getAperiodic(self):
      return self[...][self[I_LOG_TYPE] == ENTRY_TYPE_APERIODIC]
      
   def getMetRange(self):
      startTime = None
      endTime   = None
      if(len(self) > 0):
         startTime = self[I_MET][0]
         endTime   = self[I_MET][-1]
      return (startTime, endTime)
      
   def parseDescription(self):
      if(False == self.__parseDesc):
         pass
      
   def getConnectionCheck(self):
      checks = self[...][self[I_EVENT_SOURCE] == S_CONNECTION_CHECK]
      appear = checks[I_EVENT_DESC] == "icon_appears"
      
      a = checks[appear==True]
      b = checks[appear==False]
      
      
      if(len(a) > len(b)):
         alen = len(a)-1
      blen = len(b)
      
      print(alen)
      print(blen)
      
      print(checks[0:blen][[I_MET, I_OSMET]])
      
      r = checks[0:blen][I_OSMET] - checks[0:alen][I_OSMET]
      return r


        
   def plotCabinInfo(self, o2=True, p=True, t=False, co2=True, h=False, tank=True):
   
      currPlot = (o2 + p + t + co2 + h + tank) * 100 + 10
   
      metRange = list(self.getMetRange())
   
      fig = plt.figure()
      
      if(True == o2):
         currPlot += 1
         plt.subplot(currPlot)      
         plt.plot(self[I_MET], self[I_CABIN_O2], 'b')
         plt.plot(metRange, [LIMIT_O2_RED_LOW,    LIMIT_O2_RED_LOW],    'r--')
         plt.plot(metRange, [LIMIT_O2_RED_HIGH,   LIMIT_O2_RED_HIGH],   'r--')
         plt.plot(metRange, [LIMIT_O2_GREEN_LOW,  LIMIT_O2_GREEN_LOW],  'g--')
         plt.plot(metRange, [LIMIT_O2_GREEN_HIGH, LIMIT_O2_GREEN_HIGH], 'g--')
         plt.xlim(metRange)

      
      if(True == p):
         currPlot += 1
         plt.subplot(currPlot)
         plt.plot(self[I_MET], self[I_CABIN_P], 'r')
         plt.plot(metRange, [LIMIT_P_RED_LOW,    LIMIT_P_RED_LOW],    'r--')
         plt.plot(metRange, [LIMIT_P_RED_HIGH,   LIMIT_P_RED_HIGH],   'r--')
         plt.plot(metRange, [LIMIT_P_GREEN_LOW,  LIMIT_P_GREEN_LOW],  'g--')
         plt.plot(metRange, [LIMIT_P_GREEN_HIGH, LIMIT_P_GREEN_HIGH], 'g--')
         plt.xlim(metRange)

      
      if(True == t):
         currPlot += 1
         plt.subplot(currPlot)
         plt.plot(self[I_MET], self[I_CABIN_T], 'r')
         plt.plot(metRange, [LIMIT_T_RED_LOW,    LIMIT_T_RED_LOW],    'r--')
         plt.plot(metRange, [LIMIT_T_RED_HIGH,   LIMIT_T_RED_HIGH],   'r--')
         plt.plot(metRange, [LIMIT_T_GREEN_LOW,  LIMIT_T_GREEN_LOW],  'g--')
         plt.plot(metRange, [LIMIT_T_GREEN_HIGH, LIMIT_T_GREEN_HIGH], 'g--')
         plt.xlim(metRange)

      
      if(True == co2):
         currPlot += 1
         plt.subplot(currPlot)
         plt.plot(self[I_MET], self[I_CABIN_CO2], 'r')
         plt.plot(metRange, [LIMIT_CO2_RED_LOW,    LIMIT_CO2_RED_LOW],    'r--')
         plt.plot(metRange, [LIMIT_CO2_RED_HIGH,   LIMIT_CO2_RED_HIGH],   'r--')
         plt.plot(metRange, [LIMIT_CO2_GREEN_LOW,  LIMIT_CO2_GREEN_LOW],  'g--')
         plt.plot(metRange, [LIMIT_CO2_GREEN_HIGH, LIMIT_CO2_GREEN_HIGH], 'g--')
         plt.xlim(metRange)

      
      if(True == h):
         currPlot += 1
         plt.subplot(currPlot)
         plt.plot(self[I_MET], self[I_CABIN_H], 'r')
         plt.plot(metRange, [LIMIT_H_RED_LOW,    LIMIT_H_RED_LOW],    'r--')
         plt.plot(metRange, [LIMIT_H_RED_HIGH,   LIMIT_H_RED_HIGH],   'r--')
         plt.plot(metRange, [LIMIT_H_GREEN_LOW,  LIMIT_H_GREEN_LOW],  'g--')
         plt.plot(metRange, [LIMIT_H_GREEN_HIGH, LIMIT_H_GREEN_HIGH], 'g--')
         plt.xlim(metRange)
      
      if(True == tank):
         currPlot += 1
         plt.subplot(currPlot)
         plt.plot(self[I_MET], self[I_TANK_O2], 'r')
         plt.plot(self[I_MET], self[I_TANK_N2], 'b')
         plt.xlim(metRange)
         
      return fig
   
