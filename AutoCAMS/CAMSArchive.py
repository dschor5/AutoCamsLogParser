import numpy as np
from .CAMSConstants import *

class Archive(np.ndarray):

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

      # Read file 
      array = np.genfromtxt(
         fname          = filename,     # File name to get archive.                \
         names          = names,        # Assign column names                      \
         dtype          = TYPE_KEYS,    # Variable type for each field             \
         delimiter      = delimChar,    # Delimiter within archive                 \
         converters     = converters,   # Convert data using lambda functions      \
         comments       = commentChar,  # Discard comment lines                    \
         loose          = False,        # Raise errors if invalid values are read. \
         max_rows       = max_rows      # Maximum number of rows to read from file.\
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
      """
      Get the script from AutoCAMS used to control when the 
      faults were added within the simulaiton.
      """
      
      # Cache result
      if(None == self.__script):
         try:
            # Open the file, read the first line, parse it, and extract the name.
            with open(self.__filename, "r") as fp:
               line          = fp.readline().strip()
               scriptPath    = line.split(':')[-1]
               scriptName    = scriptPath.split('\\')[-1]
               self.__script = scriptName.strip()
         except IOError:
            # Catch errors if it fails to open the file.
            raise Exception("Could not read file: ", self.__filename)
      return self.__script
   
   
   def getPeriodic(self):
      """ 
      Get all periodic entries in the archive.
      
      Periodic entries are defined as those that are logged 
      automatically by the system at 1Hz. In contrast, 
      aperiodic entries are those from user interactions.
      
      Return
      ------
         NpArray with periodic entries only      
      """
      return self[...][self[I_LOG_TYPE] == ENTRY_TYPE_PERIODIC]
    
      
   def getAperiodic(self):
      """ 
      Get all aperiodic entries in the archive.
      
      Aperiodic entries are those caused by user interactions. 
      In contrast, periodic entries are logged at 1Hz by the system.
      
      Return
      ------
         NpArray with aperiodic entries only
      """
      return self[...][self[I_LOG_TYPE] == ENTRY_TYPE_APERIODIC]

      
   def getMetRange(self):
      """
      Get the MET range for the file. 
      
      A touple containing (None, None) is returned if the archive
      is too short and did not contain any entries. 
      
      Return
      ------
         touple - MET for start and end time.
      """
      startTime = None
      endTime   = None
      if(len(self) > 0):
         startTime = self[I_MET][0]
         endTime   = self[I_MET][-1]
      return (startTime, endTime)

      
   def getConnectionCheck(self):
      return self[...][self[I_EVENT_SOURCE] == S_CONNECTION_CHECK]

   
