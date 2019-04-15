import numpy as np
from AutoCAMS.CAMSArchive import *
from AutoCAMS.CAMSConstants import *

ARCHIVE_DIR = "./SampleData/"

a = Archive(ARCHIVE_DIR + "192.168.0.14_0014.txt")
b = Archive(ARCHIVE_DIR + "130.149.150.152_0012.txt")
c = Archive(ARCHIVE_DIR + "192.168.7.8_0000.txt")

count = 0
faultType = None
repairType = []
startErrorIndex = None
stopErrorIndex  = None

conCheckTotalTime = 0.0
conCheckIndex   = None
conCheckCount   = 0
recording       = False

for i in range(c.size):

   curr = c[i]

   # Find name of fault injected. Note that the system will not 
   # let you inject a fault until the previous one is resolved. 
   # So there is no need to track multiple instances here. 
   if(EventDesc.INJECTED in curr[I_EVENT_DESC]):
      faultType = curr[I_EVENT_DESC].split(" ")[1]

   # Record any repair orders sent
   if(EventDesc.REPAIR in curr[I_EVENT_DESC]):
      temp = curr[I_EVENT_DESC].split(" ")[1]
      if(temp != "task"):
         repairType.append(temp)
         # Store index of the first repair sent. 
         if(len(repairType) == 1):
            repairFirstIndex = i
         # Store index when the correct repair was sent. 
         if(temp == faultType):
            repairFaultIndex = i
   
   # Find index of RED at the start of a fault.
   if(c.isMatch(i, EventSource.A_CAMS_SYSTEM, EventDesc.PHASE_CHANGE, ErrorState.RED)):
      recording = True
      startErrorIndex = i

   # Find index of return to GREEN (normal) after a fault.
   if(c.isMatch(i, EventSource.A_CAMS_SYSTEM, EventDesc.PHASE_CHANGE, ErrorState.GREEN) and startErrorIndex is not None):
      recording = False
      stopErrorIndex = i
      
   # Count parameters sampled
   #if(EventSource.GRAPH_MONITOR == curr[I_EVENT_SOURCE] and 
   if(c.isMatch(i, EventSource.CONNECTION_CHECK, EventDesc.ICON_APPEARS) and True == recording):
      conCheckIndex = i
      conCheckCount += 1
   
   if(c.isMatch(i, EventSource.CONNECTION_CHECK) and curr[I_EVENT_DESC] != EventDesc.ICON_APPEARS and True == recording):
      conCheckTotalTime += (curr[I_OSMET] - c[conCheckIndex][I_OSMET])
      
   # Calculate time diff
   if(startErrorIndex is not None and stopErrorIndex is not None):
      count = count + 1
      print("ENTRY #" + str(count))
      print("- Fault: " + str(faultType))
      print("- Repair: " + str(repairType))
      print("- Time in RED: " + str(c[stopErrorIndex][I_OSMET] - c[startErrorIndex][I_OSMET]))
      print("- Mean Response Time: " + str(conCheckTotalTime / conCheckCount))
   
   
   
   # Reset after processing all variables for a fault
   if(False == recording):   
      startErrorIndex = None
      stopErrorIndex = None
      conCheckIndex = None
      conCheckCount = 0
      repairType = []
      conCheckTotalTime = 0.0
      

