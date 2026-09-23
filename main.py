import json


#-----------------------------------------------------------------------------------------------------
#   Function name :  LoadData
#   Description :    It Reads and parses the JSON input file
#   Parameter :      FilePath(Str)
#   Return :         Data(Dictionary)
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------

def LoadData(filePath):
    
    try:
        fobj = open(filePath, "r")
        
        data = json.load(fobj)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found {filePath}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Invalid File format....")
    
    

data = LoadData("base_case.json")

print(data)


#-----------------------------------------------------------------------------------------------------
#   Function name :  CalculateDistance
#   Description :    It Calculates the Euclidean distance between two coordinate points
#   Parameter :      Point1(List), Point2(List)
#   Return :         Distance(Float)
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------


def CalculateDistance(point1 , point2 ):
    