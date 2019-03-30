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
ENTRY_TYPE_PERIODIC  = "CAMS_SYSTEM"
ENTRY_TYPE_APERIODIC = "OPERATOR"




S_A_CAMS_SYSTEM    = "ACamsSystem"
S_GRAPH_MONITOR    = "graphic_monitor"
S_OX_TANK          = "ox_tank"
S_OX_SECOND        = "ox_second"
S_NI_TANK          = "ni_tank"
S_NI_SECOND        = "ni_second"
S_MIXER            = "mixer"
S_POSSIBLE_FLOW    = "possible_flow"
S_CONNECTION_CHECK = "connection_check"
S_LOGGING_TASK     = "logging_task"
S_DETECTOR         = "detector"
S_ERROR_GENERATOR  = "ErrorGenerator"
S_AFIRA_LOA_1      = "Afira_loa_1"
S_AFIRA_LOA_4      = "Afira_loa_4"
S_AFIRA_LOA_6      = "Afira_loa_6"


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

D_OPEN           = "open"
D_ICON_APPEARS   = "icon_appears"
D_ICON_CONFIRMED = "confirmed"
D_ICON_CLOSED    = "icon_closed"
D_ICON_MISSED    = "missed"
D_CO2_WERT       = "CO2_wert"
D_ERROR          = "error"
D_REPAIR         = "repair: + error"
D_DELAYED        = "error + delayed"


# Error state
E_RED   = "RED"
E_GREEN = "GREEN"

LIMIT_CO2_RED_LOW = 0.1
LIMIT_CO2_GREEN_LOW = 0.2
LIMIT_CO2_GREEN_HIGH = 0.6
LIMIT_CO2_RED_HIGH = 0.8

LIMIT_O2_RED_LOW = 19.0
LIMIT_O2_GREEN_LOW = 19.6
LIMIT_O2_GREEN_HIGH = 20
LIMIT_O2_RED_HIGH = 20.5

LIMIT_P_RED_LOW = 0.970
LIMIT_P_GREEN_LOW = 0.990
LIMIT_P_GREEN_HIGH = 1.025
LIMIT_P_RED_HIGH = 1.040

LIMIT_T_RED_LOW = 18.5
LIMIT_T_GREEN_LOW = 19.5
LIMIT_T_GREEN_HIGH = 22.0
LIMIT_T_RED_HIGH = 23.0

LIMIT_H_RED_LOW = 36.5
LIMIT_H_GREEN_LOW = 38.0
LIMIT_H_GREEN_HIGH = 42.0
LIMIT_H_RED_HIGH = 44.0