from enum import Enum, unique

# Entry types used in numpy arrays. 
# Changes affect archives globally.
ENTRY_TYPE_STR = 'O'    # Object/string
ENTRY_TYPE_OBJ = 'O'    # Object/string
ENTRY_TYPE_INT = 'i4'   # 32-bit integer
ENTRY_TYPE_LNG = 'i8'   # 64-bit integer
ENTRY_TYPE_FLT = 'f4'   # 32-bit float
ENTRY_TYPE_DBL = 'f8'   # 64-bit double

# Field names to use for addressing archive columns.
# Replacing these with numbers will allow numerical indexing.
I_MET          = 'MET'            # Time since state [seconds]                             
I_OSMET        = 'OSMET'          # Time code of the Operating System [milliseconds]       
I_CABIN_O2     = 'CABIN_O2'       # Oxygen concentration in the cabin air [percent]        
I_CABIN_P      = 'CABIN_P'        # Cabin pressure [bar]                                   
I_CABIN_T      = 'CABIN_T'        # Temperature [degrees Celsius]                          
I_CABIN_CO2    = 'CABIN_CO2'      # Carbon dioxide concentration in cabin air [percent]    
I_CABIN_H      = 'CABIN_H'        # Humidity [percent]                                     
I_TANK_O2      = 'TANK_O2'        # Amount of oxygen supply left. Count down from 30000.   
I_TANK_N2      = 'TANK_N2'        # Amount of nitrogen supply left. Count down from 30000. 
I_EVENT_SOURCE = 'EVENT_SOURCE'   # Event: which part of the system is involved            
I_EVENT_DESC   = 'EVENT_DESC'     # Event: what happened                                   
I_ERROR_PHASE  = 'ERROR_PHASE'    # Error phase (green=no error, red=error)                
I_ID           = 'ID'             # Running number (unique id)                             
I_LOG_TYPE     = 'LOG_TYPE'       # Event: CAMS_SYSTEM (periodic) or OPERATOR (aperiodic)  

# Additional field names for common computations
I_OSMET_FINE   = 'OSMET_FINE'     # 

# Differentiate whether it was a periodic task by the software or an aperiodic task 
# where the operator was doing something.
class EventType():
   PERIODIC  = "CAMS_SYSTEM"
   APERIODIC = "OPERATOR"

# Source descriptions. 
class EventSource():
   A_CAMS_SYSTEM    = "CamsFirst"
   GRAPH_MONITOR    = "graphic_monitor"
   OX_TANK          = "ox_tank"
   OX_SECOND        = "ox_second"
   NI_TANK          = "ni_tank"
   NI_SECOND        = "ni_second"
   MIXER            = "mixer"
   POSSIBLE_FLOW    = "possible_flow"
   CONNECTION_CHECK = "connection_check"
   LOGGING_TASK     = "logging_task"
   DETECTOR         = "detector"
   ERROR_GENERATOR  = "ErrorGenerator"
   AFIRA_LOA_1      = "Afira_loa_1"
   AFIRA_LOA_4      = "Afira_loa_4"
   AFIRA_LOA_6      = "Afira_loa_6"


#D_FLOW = {"HIGH", "MEDIUM", "STANDARD"}

#ox_flow: HIGH
#ox_flow: MEDIUM
#ox_flow: STANDARD

#ox_flow_auto: true
#ox_flow_auto: false
#ox_manual: 1
#ox_manual: 0

#ni_flow: HIGH
#ni_flow: MEDIUM
#ni_flow: STANDARD

#pressure_auto: true
#pressure_auto: false
#pressure_manual: MANUAL_ON_INCREASE
#pressure_manual: MANUAL_OFF

#ox_open
#ni_open
#co_open
#temp_open
#humi_open

class EventDesc():
   OPEN           = "open"
   ICON_APPEARS   = "icon_appears"
   ICON_CONFIRMED = "confirmed"
   ICON_CLOSED    = "icon_closed"
   PHASE_CHANGE   = "phase changed"
   LOGGING_MISSED = "missed"
   LOGGING_EMPTY  = "empty"
   CO2_WERT       = "CO2_wert"
   ERROR          = "error"
   REPAIR         = "repair: + error"
   DELAYED        = "error + delayed"
   INJECTED       = "injected"


# Error state
class ErrorState():
   RED          = "RED"
   RED_REPAIR   = "RED_REPAIR"
   RED_NO_ERROR = "RED_NO_ERROR"
   GREEN        = "GREEN"
   GREEN_ERROR  = "GREEN_ERROR"

class Limits():
   CO2_RED_LOW = 0.1
   CO2_GREEN_LOW = 0.2
   CO2_GREEN_HIGH = 0.6
   CO2_RED_HIGH = 0.8

   O2_RED_LOW = 19.0
   O2_GREEN_LOW = 19.6
   O2_GREEN_HIGH = 20
   O2_RED_HIGH = 20.5

   P_RED_LOW = 0.970
   P_GREEN_LOW = 0.990
   P_GREEN_HIGH = 1.025
   P_RED_HIGH = 1.040

   T_RED_LOW = 18.5
   T_GREEN_LOW = 19.5
   T_GREEN_HIGH = 22.0
   T_RED_HIGH = 23.0

   H_RED_LOW = 36.5
   H_GREEN_LOW = 38.0
   H_GREEN_HIGH = 42.0
   H_RED_HIGH = 44.0