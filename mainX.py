import json
import math


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

        fobj.close()

        return data

    except FileNotFoundError:

        raise FileNotFoundError(
            f"Input file not found: {filePath}"
        )

    except json.JSONDecodeError:

        raise ValueError(
            "Invalid JSON file format"
        )


#-----------------------------------------------------------------------------------------------------
#   Function name :  CalculateDistance
#   Description :    It Calculates the Euclidean distance between two coordinate points
#   Parameter :      Point1(List), Point2(List)
#   Return :         Distance(Float)
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------

def CalculateDistance(point1, point2):

    x1 = point1[0]
    y1 = point1[1]

    x2 = point2[0]
    y2 = point2[1]

    distance = math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

    return distance


#-----------------------------------------------------------------------------------------------------
#   Function name :  FindNearestAgent
#   Description :    It Finds the nearest delivery agent to the package warehouse
#   Parameter :      Package(Dictionary), Warehouses(Dictionary), Agents(Dictionary)
#   Return :         AgentId(Str)
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------

def FindNearestAgent(package, warehouses, agents):

    warehouseId = package["warehouse"]

    warehouseLocation = warehouses[warehouseId]

    nearestAgent = None
    shortestDistance = float("inf")

    for agentId in agents:

        agentLocation = agents[agentId]

        distance = CalculateDistance(
            agentLocation,
            warehouseLocation
        )

        if distance < shortestDistance:

            shortestDistance = distance
            nearestAgent = agentId

    return nearestAgent


#-----------------------------------------------------------------------------------------------------
#   Function name :  CalculateDeliveryDistance
#   Description :    It Calculates the total distance travelled for package delivery
#   Parameter :      AgentLocation(List), WarehouseLocation(List), Destination(List)
#   Return :         TotalDistance(Float)
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------

def CalculateDeliveryDistance( agentLocation, warehouseLocation,   destination):

    distanceToWarehouse = CalculateDistance(
        agentLocation,
        warehouseLocation
    )

    distanceToDestination = CalculateDistance(
        warehouseLocation,
        destination
    )

    totalDistance = (
        distanceToWarehouse +
        distanceToDestination
    )

    return totalDistance


#-----------------------------------------------------------------------------------------------------
#   Function name :  InitializeAgentStats
#   Description :    It Initializes delivery statistics for all agents
#   Parameter :      Agents(Dictionary)
#   Return :         AgentStats(Dictionary)
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------

def InitializeAgentStats(agents):

    agentStats = {}

    for agentId in agents:

        agentStats[agentId] = {
            "packages_delivered": 0,
            "total_distance": 0
        }

    return agentStats


#-----------------------------------------------------------------------------------------------------
#   Function name :  AssignPackages
#   Description :    It Assigns each package to the nearest delivery agent
#   Parameter :      Packages(List), Warehouses(Dictionary), Agents(Dictionary)
#   Return :         None
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------

def AssignPackages(packages, warehouses, agents):

    for package in packages:

        nearestAgent = FindNearestAgent(
            package,
            warehouses,
            agents
        )

        package["agent"] = nearestAgent


#-----------------------------------------------------------------------------------------------------
#   Function name :  DeliverPackages
#   Description :    It Simulates delivery of all assigned packages
#   Parameter :      Packages(List), Warehouses(Dictionary), Agents(Dictionary), AgentStats(Dictionary)
#   Return :         None
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------

def DeliverPackages(packages,warehouses,agents,agentStats):

    for package in packages:

        agentId = package["agent"]

        warehouseId = package["warehouse"]

        destination = package["destination"]

        agentLocation = agents[agentId]

        warehouseLocation = warehouses[warehouseId]

        totalDistance = CalculateDeliveryDistance(
            agentLocation,
            warehouseLocation,
            destination
        )

        package["distance"] = totalDistance

        agentStats[agentId]["total_distance"] += totalDistance

        agentStats[agentId]["packages_delivered"] += 1

        agents[agentId] = destination


#-----------------------------------------------------------------------------------------------------
#   Function name :  GenerateReport
#   Description :    It Generates the final delivery report
#   Parameter :      AgentStats(Dictionary)
#   Return :         Report(Dictionary)
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------

def GenerateReport(agentStats):

    report = {}

    bestAgent = None
    bestEfficiency = float("inf")

    for agentId in agentStats:

        packagesDelivered = agentStats[agentId]["packages_delivered"]

        totalDistance = agentStats[agentId]["total_distance"]

        if packagesDelivered > 0:

            efficiency = totalDistance / packagesDelivered

        else:

            efficiency = 0

        report[agentId] = {
            "packages_delivered": packagesDelivered,
            "total_distance": round(totalDistance, 2),
            "efficiency": round(efficiency, 2)
        }

        if packagesDelivered > 0:

            if efficiency < bestEfficiency:

                bestEfficiency = efficiency
                bestAgent = agentId

    report["best_agent"] = bestAgent

    return report


#-----------------------------------------------------------------------------------------------------
#   Function name :  SaveReport
#   Description :    It Saves the delivery report into a JSON file
#   Parameter :      Report(Dictionary), FilePath(Str)
#   Return :         None
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------

def SaveReport(report, filePath):

    try:

        fobj = open(filePath, "w")

        json.dump(
            report,
            fobj,
            indent=4
        )

        fobj.close()

    except OSError:

        raise OSError(
            f"Unable to save report file: {filePath}"
        )


#-----------------------------------------------------------------------------------------------------
#   Function Name :  Main
#   Description :    Executes the FastBox delivery system
#   Date :           23/09/2026
#   Author:          Raviraj Aade
#-----------------------------------------------------------------------------------------------------

def main():

    data = LoadData("test_case_10.json")

    # Get data from JSON
    warehouses = data["warehouses"]

    agents = data["agents"]

    packages = data["packages"]


    # Initialize agent statistics
    agentStats = InitializeAgentStats( agents )


    # Assign packages to nearest agents
    AssignPackages( packages, warehouses, agents )


    # Deliver packages
    DeliverPackages(  packages, warehouses, agents, agentStats  )


    # Generate final report
    report = GenerateReport(  agentStats  )


    # Save report
    SaveReport( report, "report.json"  )


    # Display result
    print("FastBox Delivery Report")
    print("--------------------------------------------------------------------------------------")

    for agentId in agentStats:

        print( agentId, "->", report[agentId]   )

    print("--------------------------------------------------------------------------------------")

    print(
        "Best Agent:",
        report["best_agent"]
    )

    print("Report saved to report.json")


if __name__ == "__main__":

    main()