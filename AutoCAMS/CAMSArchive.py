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
      
      Return
      ------
         string - XML script name used for this run.
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

      
   def parseData(self, prefix):
      """
      <INSERT DESCRIPTION>
      
      Params
      ------
         prefix - Array with missionId, userId, sessionId, hasFault
      
      Return
      ------
         string - Comma separated metrics extracted for this session.
      """
      COMMA = ","
      
      faultIndex        = 0
      iRed              = None   # Index when fault is introduced
      iGreen            = None   # Index when fault is resolved
      iFirstRepair      = None   # Index when first repair order is sent
      iCorrectRepair    = None   # Index when correct repair order is sent
      faultInjected     = None   # Fault injected into the system
      faultDetected     = None   # Fault detected by AFIRA
      repairOrders      = []     # Repair orders sent
      paramsVerified    = set()  # Set of parameters verified
      conCheckTotalTime = 0      # Total time elapsed for connection checks
      conCheckCount     = 0      # Number of connection checks
      conCheckIndex     = 0      # Index of last connection check
      logTotal          = 0      # Number of log entries entered
      logMissed         = 0      # Number of log entries missed
      
      output = ""
      
      # Iterate through the whole archive
      for i in range(self.size):
         curr = self[i]
         
         # Identify faults inserted
         if(EventSource.AFIRA in curr[I_EVENT_SOURCE] and ":" in curr[I_EVENT_DESC]):
            faultInjected, faultDetected = curr[I_EVENT_DESC].split(":")
            faultIndex += 1
            
         # Identify all repair orders sent
         if(EventDesc.REPAIR in curr[I_EVENT_DESC]):
            temp = curr[I_EVENT_DESC].split(" ")[1]
            if(temp != "task"):
               repairOrders.append(temp)
            
               # Store index of first repair set
               if(len(repairOrders) == 1):
                  iFirstRepair = i
            
            # Store index when correct repair was sent. 
            if(faultInjected is not None and temp == faultInjected):
               iCorrectRepair = i
         
         # Find index of RED (start of fault)
         if(EventDesc.PHASE_CHANGE == curr[I_EVENT_DESC] and ErrorState.RED == curr[I_ERROR_PHASE]):
            iRed = i
            
         # Find index of RED_NO_ERROR (end of fault)
         if(EventDesc.PHASE_CHANGE == curr[I_EVENT_DESC] and ErrorState.RED_NO_ERROR == curr[I_ERROR_PHASE]):
            iGreen = i
         
         # Capture set of all parameters verified while the fault is present. 
         if(iRed is not None):
            if(curr[I_EVENT_SOURCE] in EventSource.FLOW_MONITOR):
               paramsVerified.update([curr[I_EVENT_SOURCE]])
            if(curr[I_EVENT_SOURCE] == EventSource.GRAPH_MONITOR):
               paramsVerified.update([curr[I_EVENT_DESC]])
         
         # Connection checks
         if(iRed is not None):
            if(curr[I_EVENT_SOURCE] == EventSource.CONNECTION_CHECK):
               if(curr[I_EVENT_DESC] == EventDesc.ICON_APPEARS):
                  conCheckIndex = i
               else:
                  conCheckTotalTime += (curr[I_OSMET] - self[conCheckIndex][I_OSMET])
                  conCheckCount += 1
                  
         # Logging tasks
         if(iRed is not None):
            if(curr[I_EVENT_SOURCE] == EventSource.LOGGING_TASK):
               if(curr[I_EVENT_DESC] == EventDesc.LOGGING_MISSED or curr[I_EVENT_DESC] == EventDesc.LOGGING_EMPTY):
                  logMissed += 1
               logTotal += 1
         
         # Find index of GREEN (finished processing fault -> record entry)
         if(EventDesc.PHASE_CHANGE == curr[I_EVENT_DESC] and ErrorState.GREEN == curr[I_ERROR_PHASE]):
            
            # Capture output
            output += COMMA.join(map(str, prefix)) + COMMA
            
            # Fault index
            output += str(faultIndex) + COMMA
            
            # Has fault?
            if(faultInjected == faultDetected):
               output += "0" + COMMA
            else:
               output += "1" + COMMA
               
            # Number of repair orders set
            output += str(len(repairOrders)) + COMMA
            
            # Fault Identification Time (FIT)
            deltaTime = self[iCorrectRepair][I_OSMET] - self[iRed][I_OSMET]
            output += str(deltaTime) + COMMA 
            
            # Automation Verification Time (AVT)
            deltaTime = self[iFirstRepair][I_OSMET] - self[iRed][I_OSMET]
            output += str(deltaTime) + COMMA
            
            # Automation Verification Sampling of Relevant Parameters (AVS-RP)
            limitSet = paramsVerified.intersection(PARAMS_RELEVANT)
            temp = float(len(limitSet)) / len(PARAMS_RELEVANT)
            output += "{0:.3f}".format(temp) + COMMA
            
            # Automation Verification Sampling of Necessary Parameters (AVS-NP)
            limitSet = paramsVerified.intersection(PARAMS_NECESSARY[faultInjected])
            temp = float(len(limitSet)) / len(PARAMS_NECESSARY[faultInjected])
            output += "{0:.3f}".format(temp) + COMMA
            
            # Connection check
            if(conCheckCount > 0):
               output += "{0:.3f}".format(float(conCheckTotalTime) / conCheckCount) + COMMA
            else:
               output += "{0:.3f}".format(0.0) + COMMA
               
            # Logging task
            if(logTotal > 0):
               output += "{0:.3f}".format(float(logTotal - logMissed) / logTotal) + COMMA
            else:
               output += "{0:.3f}".format(0.0) + COMMA
            
            output += "\n"
            
            # Reset all variables
            iRed              = None
            iGreen            = None
            iFirstRepair      = None
            iCorrectRepair    = None
            faultInjected     = None
            faultDetected     = None
            repairOrders      = []  
            paramsVerified    = set()
            conCheckTotalTime = 0
            conCheckCount     = 0
            conCheckIndex     = 0 
            logTotal          = 0
            logMissed         = 0
            
      return output
      