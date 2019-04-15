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

PARAMS_NECESSARY = {
   "OXYGEN_VALVE_LEAK"               : set(["ox_open", "ox_tank_display", "ox_second"]),
   "OXYGEN_VALVE_BLOCK"              : set(["ox_open", "ox_tank_display", "ox_second"]),
   "OXYGEN_VALVE_STUCK_OPEN"         : set(["ox_open", "ox_tank_display", "ox_second", "ni_open"]),
   "NITROGEN_VALVE_LEAK"             : set(["ni_open", "ni_tank_display", "ni_second"]),
   "NITROGEN_VALVE_BLOCK"            : set(["ni_open", "ni_tank_display", "ni_second"]),
   "NITROGEN_VALVE_STUCK_OPEN"       : set(["ni_open", "ni_tank_display", "ni_second", "ox_open"]),
   "OXYGEN_SENSOR_STARTS_UPPER_TH"   : set(["ox_open", "ox_tank_display", "ni_open"]),
   "OXYGEN_SENSOR_STARTS_LOWER_TH"   : set(["ox_open", "ox_tank_display", "ni_open"]),
   "PRESSURE_SENSOR_STARTS_UPPER_TH" : set(["ox_open", "ni_tank_display", "ni_open"]),
   "PRESSURE_SENSOR_STARTS_LOWER_TH" : set(["ox_open", "ni_tank_display", "ni_open"]),
   "MIXER_BLOCK"                     : set(["ni_open", "ox_open", "ox_tank_display", "ox_second", "ni_second", "ni_tank_display", "mixer"])
   }

PARAMS_RELEVANT = set([
   "ni_open", "ox_open", "ox_tank_display", "ox_second", "ni_second", "ni_tank_display", "mixer"
   ])
   
PARAMS_TOTAL = set([
   "ni_open", "ox_open", "co_open", "temp_open", "humid_open", 
   "ox_tank_display", "ox_second", "ni_second", "ni_tank_display", "mixer"
   ])

# Differentiate whether it was a periodic task by the software or an aperiodic task 
# where the operator was doing something.
class EventType():
   PERIODIC  = "CAMS_SYSTEM"
   APERIODIC = "OPERATOR"

# Source descriptions. 
class EventSource():
   A_CAMS_SYSTEM    = "CamsFirst"
   GRAPH_MONITOR    = "graphic_monitor"
   FLOW_MONITOR     = ["ox_tank", "ox_second", "ni_tank", "ni_second", "mixer"]
   POSSIBLE_FLOW    = "possible_flow"
   CONNECTION_CHECK = "connection_check"
   LOGGING_TASK     = "logging_task"
   DETECTOR         = "detector"
   ERROR_GENERATOR  = "ErrorGenerator"
   AFIRA            = "AfiraSystem6"


class EventDesc():
   """
   Abstract class for descriptions corresponding to the
   field valid values for I_EVENT_DESC in the archive. 
   """
   OPEN           = "open"
   ICON_APPEARS   = "icon_appears"
   ICON_CONFIRMED = "confirmed"
   ICON_CLOSED    = "icon_closed"
   PHASE_CHANGE   = "phase changed"
   LOGGING_MISSED = "missed"
   LOGGING_EMPTY  = "empty"
   CO2_WERT       = "CO2_wert"
   ERROR          = "error"
   REPAIR         = "repair"
   DELAYED        = "error + delayed"
   INJECTED       = "injected"


class ErrorState():
   """
   Abstract class for error states corresponding to the
   field valid values for I_ERROR_PHASE in the archive. 
   """
   RED          = "RED"
   RED_REPAIR   = "RED_REPAIR"
   RED_NO_ERROR = "RED_NO_ERROR"
   GREEN        = "GREEN"
   GREEN_ERROR  = "GREEN_ERROR"


class Limits():
   """
   Abstract class for limit constants. 
   """
   # Indexes for limits
   RED_LOW    = 0
   GREEN_LOW  = 1
   GREEN_HIGH = 2
   RED_HIGHT  = 3

   # CO2 limits in ? units
   CO2 = [
      0.1, # RED_LOW
      0.2, # GREEN_LOW
      0.6, # GREEN_HIGH
      0.8  # RED_HIGHT
      ]

   # O2 limits in ? units
   O2 = [
      19.0, # RED_LOW
      19.6, # GREEN_LOW
      20.0, # GREEN_HIGH
      20.5  # RED_HIGHT
      ]

   # Pressure limits in ? units
   P = [
      0.970, # RED_LOW
      0.990, # GREEN_LOW
      1.025, # GREEN_HIGH
      1.040  # RED_HIGHT
      ]

   # Temperature limits in degree Celsius
   T = [
      18.5, # RED_LOW
      19.5, # GREEN_LOW
      22.0, # GREEN_HIGH
      23.0  # RED_HIGHT
      ]

   # Humidity limits in relative percent humidity
   CO2 = [
      36.5, # RED_LOW
      38.0, # GREEN_LOW
      42.0, # GREEN_HIGH
      44.0  # RED_HIGHT
      ]
