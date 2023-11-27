""" This module allows to solve Augerat et al. instances of
Capacitated Vehicle Routing Problem """

from VRPSolverEasy.src import solver
import os,sys,getopt
import math
import numpy as np

def read_instance(name : str):
    """ Read an instance in the folder data from a given name """
    path_project = os.path.abspath(os.getcwd())
    with open (name,
        "r",encoding="UTF-8" )as file:
        elements = [str(element) for element in file.read().split()]
    file.close()
    return elements

def compute_euclidean_distance(x_i, y_i, x_j, y_j,number_digit=3):
    """Compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2), number_digit)

def solve_demo(instance_path,
               solver_name="CLP",
               solver_path="",
               time_resolution=30,
               disableBuiltInHeur=False,
               upper_bound=-1):
    """return a solution from modelisation"""

    # read instance
    data = read_cvrp_instances(instance_path)

    # get data
    vehicle_type = data["VehicleTypes"]
    depot = data["Points"][0]
    customers = data["Points"][1:]
    links = data["Links"]

    # modelisation of problem
    model = solver.Model()

    # add vehicle type
    model.add_vehicle_type(id=vehicle_type["id"],
                           start_point_id=vehicle_type["start_point_id"],
                           end_point_id=vehicle_type["end_point_id"],
                           max_number=vehicle_type["max_number"],
                           capacity=vehicle_type["capacity"],
                           var_cost_dist=vehicle_type["var_cost_dist"]
                           )

    # add depot
    model.add_depot(id=depot["id"])

    # add all customers
    for customer in customers:
        model.add_customer(id=customer["id"],
                           demand=customer["demand"]
                           )
    # add all links
    for link in links:
        model.add_link(start_point_id=link["start_point_id"],
                       end_point_id=link["end_point_id"],
                       distance=link["distance"]
                       )

    # set parameters
    if disableBuiltInHeur:
        model.set_parameters(time_limit=time_resolution, solver_name=solver_name, 
                            heuristic_used=False)
        print('Built-in heuristic is disabled')
    else:
        model.set_parameters(time_limit=time_resolution, solver_name=solver_name, 
                            heuristic_used=True)
        print('Built-in heuristic is enabled')

    if upper_bound != -1:
        model.parameters.upper_bound = upper_bound

    ''' If you have cplex 22.1 installed on your laptop windows you have to specify
        solver path'''
    if (solver_name == "CPLEX" and solver_path != ""):
        model.parameters.cplex_path = solver_path

    # solve model
    model.solve()

    if model.solution.is_defined :
        path_instance_name = instance_path.split(".")[0]
        name_instance = path_instance_name.split("\\")[
            len(path_instance_name.split("\\"))-1]
        print('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n'.format(
                "instance_name","solver_name","ext_heuristic",
                "solution_value",
                "solution_time",
                "best_lb",
                "root_lb",
                "root_time",
                "nb_branch_and_bound_nodes",
                "status"
                ), end='')
        print('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n'.format(
            instance_path,solver_name,False if upper_bound == -1 else True,
            model.solution.value,
            model.statistics.solution_time,
            model.statistics.best_lb,
            model.statistics.root_lb,
            model.statistics.root_time,
            model.statistics.nb_branch_and_bound_nodes,
            model.status
            ))

    # export the result
    # model.solution.export(instance_name.split(".")[0] + "_result")

    return model.solution

def read_cvrp_instances(instance_name):
    """Read literature instances from CVRPLIB by giving the name of instance
       and returns dictionary containing all elements of model"""

    instance_iter = iter(read_instance(instance_name))
    points = []
    id_point = 0
    dimension_input = -1
    capacity_input = -1
    # Instantiate the data problem.
    data = {}

    while True:
        element = next(instance_iter)
        if element == "DIMENSION":
            next(instance_iter)  # pass ":"
            dimension_input = int(next(instance_iter))
        elif element == "CAPACITY":
            next(instance_iter)  # pass ":"
            capacity_input = int(next(instance_iter))
        elif element == "EDGE_WEIGHT_TYPE":
            next(instance_iter)  # pass ":"
            element = next(instance_iter)
            if element != "EUC_2D":
                raise Exception("EDGE_WEIGHT_TYPE : " + element + """
                is not supported (only EUC_2D)""")
        elif element == "NODE_COORD_SECTION":
            break

    # Initialize vehicle type
    vehicle_type = {"id": 1,  # we cannot have an id less than 1
                    "start_point_id": id_point,
                    "end_point_id": id_point,
                    "capacity": capacity_input,
                    "max_number": dimension_input,
                    "var_cost_dist": 1
                    }

    vehicles = []
    index = 0
    for i in range(dimension_input):
        vehicles.append(capacity_input)

    data['vehicle_capacities'] = vehicles
    data['vehicle_capacity'] = capacity_input
    data['num_vehicles'] = dimension_input
    data['depot'] = 0

    # Create points
    for current_id in range(dimension_input):
        point_id = int(next(instance_iter))
        if point_id != current_id + 1:
            raise Exception("Unexpected index")
        x_coord = float(next(instance_iter))
        y_coord = float(next(instance_iter))
        points.append({"x": x_coord,
                        "y": y_coord,
                        "demand": -1,
                        "id": id_point})
        id_point += 1

    element = next(instance_iter)
    if element != "DEMAND_SECTION":
        raise Exception("Expected line DEMAND_SECTION")
    jobs = []
    # Get the demands
    for current_id in range(dimension_input):
        point_id = int(next(instance_iter))
        if point_id != current_id + 1:
            raise Exception("Unexpected index")
        demand = int(next(instance_iter))
        points[current_id]["demand"] = demand
        jobs.append(demand)
    
    data['demands'] = jobs

    element = next(instance_iter)
    if element != "DEPOT_SECTION":
        raise Exception("Expected line DEPOT_SECTION")
    next(instance_iter) # pass id depot

    end_depot_section = int(next(instance_iter))
    if end_depot_section != -1:
        raise Exception("Expected only one depot.")

    # Compute the links of graph
    links = []
    nb_link = 0
    matrix = [[0 for i in range((len(points)))] for i in range(len(points))]
    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            dist = compute_euclidean_distance(point["x"],
                                                    point["y"],
                                                    points[j]["x"],
                                                    points[j]["y"],
                                                    0)
            links.append({"name": "L" + str(nb_link),
                          "start_point_id": point["id"],
                          "end_point_id": points[j]["id"],
                          "distance": dist
                          })

            matrix[i][j] = dist
            matrix[j][i] = dist

            nb_link += 1
    
    data['distance_matrix'] = matrix

    return {"Points": points,
            "VehicleTypes": vehicle_type,
            "Links": links}

def main(argv):
    instance_path = ''
    solver_name = ''
    solver_path = ''
    disableBuiltInHeur = False
    time_resolution = 30
    upper_bound = -1
    opts, args = getopt.getopt(argv,"i:s:u:b:e:p:")
   
    for opt, arg in opts:
        if opt == "-i":
            instance_path = arg
        elif opt == "-s":
            solver_name = arg
        elif opt == "-u":
            upper_bound = float(arg)
        elif opt == "-b":
            disableBuiltInHeur = arg == "yes"
        elif opt == "-e":
            time_resolution = float(arg)
        if opt in ["-p"]:
            solver_path = arg

    solve_demo(instance_path, solver_name, solver_path, time_resolution, disableBuiltInHeur, upper_bound)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
