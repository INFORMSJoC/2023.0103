""" This module allows to solve Solomon instances of
Capacitated Vehicle Routing Problem with Time Windows. """

import math
import os
import sys
import getopt
from VRPSolverEasy.src import solver

def read_instance(name: str):
    """ Read an instance in the folder data from a given name """
    path_project = os.path.abspath(os.getcwd())
    with open(name,
              "r", encoding="UTF-8")as file:
        elements = [str(element) for element in file.read().split()]
    file.close()
    return elements


def compute_euclidean_distance(x_i, y_i, x_j, y_j, number_digit=3):
    """Compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                           (y_i - y_j)**2), number_digit)


def compute_one_decimal_floor_euclidean_distance(x_i, y_i, x_j, y_j):
    """Compute the euclidean distance between 2 points from graph"""
    return math.floor(math.sqrt((x_i - x_j)**2 + (y_i - y_j)**2) * 10) / 10


def solve_demo(instance_path,
               solver_name="CLP",
               solver_path="",
               time_resolution=30,
               disableBuiltInHeur=False,
               upper_bound=-1):
    """Return a solution from modelisation"""

    # read instance
    data = read_cvrptw_instances(instance_path)

    # get data
    vehicle_type = data["vehicle_type"]
    depot = data["Points"][0]
    customers = data["Points"][1:]
    links = data["Links"]

    # modelisation of problem
    model = solver.Model()

    # add vehicle type
    model.add_vehicle_type(id=vehicle_type["id"],
                           start_point_id=vehicle_type["start_point_id"],
                           end_point_id=vehicle_type["end_point_id"],
                           capacity=vehicle_type["capacity"],
                           max_number=vehicle_type["max_number"],
                           tw_begin=vehicle_type["tw_begin"],
                           tw_end=vehicle_type["tw_end"],
                           var_cost_dist=vehicle_type["var_cost_dist"],
                           var_cost_time=vehicle_type["var_cost_time"]
                           )
    # add depot
    model.add_depot(id=depot["id"],
                    service_time=depot["service_time"],
                    tw_begin=depot["tw_begin"],
                    tw_end=depot["tw_end"]
                    )

    # add all customers
    for customer in customers:
        model.add_customer(id=customer["id"],
                           service_time=customer["service_time"],
                           tw_begin=customer["tw_begin"],
                           tw_end=customer["tw_end"],
                           demand=customer["demand"]
                           )
    # add all links
    for link in links:
        model.add_link(start_point_id=link["start_point_id"],
                       end_point_id=link["end_point_id"],
                       distance=link["distance"],
                       time=link["time"]
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

    # model.export(instance_path)
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

def read_cvrptw_instances(instance_name):
    """Read literature instances of CVRPTW ("Solomon" format) by giving the name of instance,
        compute lower bound and returns dictionary containing all elements of model"""
    instance_iter = iter(read_instance(instance_name))
    # Instantiate the data problem.
    data = {}

    for i in range(4):
        next(instance_iter)

    max_number_input = int(next(instance_iter))
    capacity_input = int(next(instance_iter))

    for i in range(13):
        next(instance_iter)

    depot_x = float(next(instance_iter))
    depot_y = float(next(instance_iter))
    depot_demand = int(next(instance_iter))
    depot_tw_begin = int(next(instance_iter))
    depot_tw_end = int(next(instance_iter))
    depot_service_time = int(next(instance_iter))
    id_point = 0

    vehicles = []
    # Initialize vehicle type
    vehicle_type = {"id": 1,  # we cannot have an id less than 1
                    "start_point_id": id_point,
                    "end_point_id": id_point,
                    "capacity": capacity_input,
                    "max_number": max_number_input,
                    "tw_begin": depot_tw_begin,
                    "tw_end": depot_tw_end,
                    "service_time": depot_service_time,
                    "var_cost_dist": 1,
                    "var_cost_time": 0
                    }
    index = 0
    time_windows = [(depot_tw_begin, depot_tw_end)]
    service_times = [0]
    for i in range(max_number_input):
        vehicles.append(capacity_input)
        index += 1

    data['vehicle_capacities'] = vehicles
    data['num_vehicles'] = max_number_input
    data['depot'] = 0

    demands = []

    # Initialize the points with depot
    points = [{"x": depot_x,
               "y": depot_y,
               "demand": depot_demand,
               "tw_begin": depot_tw_begin,
               "tw_end": depot_tw_end,
               "service_time": depot_service_time,
               "id": id_point
               }]
    demands.append(depot_demand)
    # Add the customers in the list of points

    while True:
        id_point += 1
        value = next(instance_iter, None)
        if value is None:
            break
        x_coord = float(next(instance_iter))
        y_coord = float(next(instance_iter))
        demand = int(next(instance_iter))
        tw_begin = int(next(instance_iter))
        tw_end = int(next(instance_iter))
        service_time = int(next(instance_iter))
        points.append({"x": x_coord,
                       "y": y_coord,
                       "demand": demand,
                       "tw_begin": tw_begin,
                       "tw_end": tw_end + service_time,
                       "service_time": service_time,
                       "id": id_point})
        demands.append(demand)
        time_windows.append((tw_begin, tw_end))
        service_times.append(service_time)

    data['demands'] = demands
    data['time_windows'] = time_windows
    # compute the links of graph
    links = []
    matrix = [[0 for i in range((len(points)))] for i in range(len(points))]
    matrix_time = [[0 for i in range((len(points)))]
                   for i in range(len(points))]

    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            dist = compute_one_decimal_floor_euclidean_distance(
                point["x"], point["y"], points[j]["x"], points[j]["y"])

            links.append({"start_point_id": point["id"],
                          "end_point_id": points[j]["id"],
                          "distance": dist,
                          "time": dist
                          })
            matrix_time[i][j] = dist + service_times[i]
            matrix_time[j][i] = dist + service_times[j]
            matrix[i][j] = dist
            matrix[j][i] = dist

    data['distance_matrix'] = matrix
    data['time_matrix'] = matrix_time
    upper_bound = 0

    return {"Points": points,
            "vehicle_type": vehicle_type,
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
