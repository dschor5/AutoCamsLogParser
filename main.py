import numpy as np
import os
from AutoCAMS.CAMSArchive import *
from AutoCAMS.CAMSConstants import *

ARCHIVE_DIR = "./Data/"
MISSION_DIR = ["M5_Logs/", "M6_Logs/"]
SUBJECT_DIR = ["S1/", "S2/", "S3/"]

# Key for data anlysis. 
FAULT_TRUE  = 1   # Session has automation fault
FAULT_FALSE = 0   # Session does not have automation fault

SESSION_SCRIPT = {
   # "FILE" : [USER, SESSION, FAULT]
   "ILTPNVVO.xml" : [1, 1, FAULT_TRUE ],   
   "CFUHBYWT.xml" : [1, 2, FAULT_TRUE ],
   "OUIQXVBS.xml" : [1, 3, FAULT_FALSE],
   "KRCMPCEQ.xml" : [1, 4, FAULT_FALSE],
   "TSPPZIKX.xml" : [1, 5, FAULT_FALSE],
   "EXVKJNTX.xml" : [1, 6, FAULT_FALSE],
                       
   "YFZGVYOI.xml" : [2, 1, FAULT_TRUE ],   
   "MGNKYJJK.xml" : [2, 2, FAULT_FALSE],
   "PNASEOYO.xml" : [2, 3, FAULT_FALSE],
   "ZTDVZZCC.xml" : [2, 4, FAULT_FALSE],
   "LEWIZKXY.xml" : [2, 5, FAULT_TRUE ],
   "FJZKQVVD.xml" : [2, 6, FAULT_FALSE],
                       
   "TGSTHKET.xml" : [3, 1, FAULT_FALSE],
   "IDWJKXHM.xml" : [3, 2, FAULT_FALSE],
   "ITFPGVPB.xml" : [3, 3, FAULT_FALSE],
   "YNWKRNSG.xml" : [3, 4, FAULT_TRUE ],
   "SLLQDHKH.xml" : [3, 5, FAULT_TRUE ],
   "PTRUNNFW.xml" : [3, 6, FAULT_FALSE],
}

NUM_SESSIONS = 6

fp  = open("./output.txt", "w")
fps = []
for i in range(0, NUM_SESSIONS):
   fps.append(open("./output_session_" + str(i) + ".txt", "w"))


# Iterate through each mission and subject
for iDir in range(len(MISSION_DIR)):
   for iSubject in range(len(SUBJECT_DIR)):
      
      # Current folder name being processed
      folder = ARCHIVE_DIR + MISSION_DIR[iDir] + SUBJECT_DIR[iSubject]
      
      # Skip missing mission/subject combinations.
      if(False == os.path.exists(folder)):
         continue
      
      # Iterate through all the files in a folder
      for filename in os.listdir(folder):
         
         # Skip invalid files
         if(".txt" not in filename):
            continue
         
         print("- Parsing " + folder + filename)
         
         # Read the archive and determine which file it belongs to. 
         archive = Archive(folder + filename)
         testFile = archive.getScript()
         
         # Skip file if the script name is invalid. 
         if(testFile not in SESSION_SCRIPT):
            print("--- ERROR: File not found.")
            continue
         
         
         # Process current archive and write to general file
         prefix = [iDir] + SESSION_SCRIPT[testFile]
         prefix[1] += (iDir * len(SUBJECT_DIR))       # Make each user unique
         output = archive.parseData(prefix)
         fp.write(output)
         fp.flush()
         
         # Write output to session specific file
         prefix = [iDir, SESSION_SCRIPT[testFile][0]]
         prefix[1] += (iDir * len(SUBJECT_DIR))
         output = archive.parseData(prefix)
         fps[SESSION_SCRIPT[testFile][1]-1].write(output)
         fps[SESSION_SCRIPT[testFile][1]-1].flush()
   
fp.close()
for i in range(0, NUM_SESSIONS):
   fps[i].close()
      
