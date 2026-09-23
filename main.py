import json


#-----------------------------------------------------------------------------------------------------
#   Function name :  load_data
#   Description :    It Reads and parses the JSON input file
#   Parameter :      FilePath(Str)
#   Return :         Data(Dictionary)
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------

def load_data(filePath):
    
    try:
        fobj = open(filePath, "r")
        
        data = json.load(fobj)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found {filePath}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Invalid File format....")
    
    

# data = load_data("base_case.json")

# print(data)


#-----------------------------------------------------------------------------------------------------
#   Function name :  CalculateDistance
#   Description :    It Calculates the Euclidean distance between two coordinate points
#   Parameter :      Point1(List), Point2(List)
#   Return :         Distance(Float)
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------

