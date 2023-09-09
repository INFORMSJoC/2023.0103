""" This module allows to solve instances of
Heterogeneous Fleet Vehicle Routing Problem """

from VRPSolverEasy.src import solver
import os,sys,getopt
import math

def read_instance(name : str):
    """ Read an instance in the folder data from a given name """
    path_project = os.path.abspath(os.getcwd())
    with open (name,
        "r",encoding="UTF-8" )as file:
        elements = [str(element) for element in file.read().split()]
    file.close()
    return elements

def compute_euclidean_distance(x_i, y_i, x_j, y_j):
    """Compute the euclidean distance between 2 points from graph"""
    return math.sqrt((x_i - x_j)**2 + (y_i - y_j)**2)

def compute_one_decimal_floor_euclidean_distance(x_i, y_i, x_j, y_j):
    """Compute the euclidean distance between 2 points from graph"""
    return math.floor(math.sqrt((x_i - x_j)**2 + (y_i - y_j)**2) * 10) / 10

def solve_demo(instance_path,
               solver_name="CLP",
               solver_path="",
               time_resolution=30,
               disableBuiltInHeur=False,
               upper_bound=-1):
    """return a solution from modelisation"""

    # read instance
    data = read_hfvrp_instances(instance_path)

    # get data
    vehicle_types = data["VehicleTypes"]
    depot = data["Points"][0]
    customers = data["Points"][1:]
    links = data["Links"]

    # modelisation of problem
    model = solver.Model()

    for vehicle_type in vehicle_types:
        # add vehicle type
        model.add_vehicle_type(id=vehicle_type["id"],
                            start_point_id=vehicle_type["start_point_id"],
                            end_point_id=vehicle_type["end_point_id"],
                            capacity=vehicle_type["capacity"],
                            max_number=vehicle_type["max_number"],
                            fixed_cost=vehicle_type["fixed_cost"],
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
                       distance=link["distance"])

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
    #model.export()
    # model.export(instance_path)
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
    #model.solution.export()
    #print(model.parameters.upper_bound)
    return model.solution

def read_hfvrp_instances(instance_name):
    """Read literature instances of HFVRP by giving the name of instance
        and returns dictionary containing all elements of model"""
    instance_iter = iter(read_instance(instance_name))
    vehicles_capacities, vehicles_fixed_costs, vehicles_var_costs = [], [], []
    data = {}
    points = []
    firstRead = next(instance_iter)
    index = 0

    if firstRead == 'NAME': # read XH instances (large instances)
        nb_points, nb_vehicles, max_num_veh = [], [], []
        capacities, fixed_costs, var_costs = [], [], []
        while True:
            element = next(instance_iter)
            if element == "DIMENSION":
                next(instance_iter)  # pass ":"
                nb_points = int(next(instance_iter)) - 1
            elif element == "VEHICLE_KINDS":
                next(instance_iter)  # pass ":"
                nb_vehicles = int(next(instance_iter))
            elif element == "CAPACITIES":
                for k in range(nb_vehicles):
                    capacities.append(int(next(instance_iter)))
            elif element == "FIXED_COSTS":
                for k in range(nb_vehicles):
                    fixed_costs.append(int(next(instance_iter)))
            elif element == "VARIABLE_COSTS":
                for k in range(nb_vehicles):
                    var_costs.append(float(next(instance_iter)))
            elif element == "NUMBER_OF_VEHICLES":
                for k in range(nb_vehicles):
                    max_num_veh.append(int(next(instance_iter)))
            elif element == "EDGE_WEIGHT_TYPE":
                next(instance_iter)  # pass ":"
                element = next(instance_iter)
                if element != "EUC_2D":
                    raise Exception("EDGE_WEIGHT_TYPE : " + element + """
                    is not supported (only EUC_2D)""")
            elif element == "NODE_COORD_SECTION":
                break

        vehicle_types = []
        # Create vehicle types
        for k in range(nb_vehicles):
            vehicle_type = {"id": k+1,  # we cannot have an id less than 1
                    "start_point_id": 0,
                    "end_point_id": 0,
                    "capacity": capacities[k],
                    "max_number": max_num_veh[k],
                    "fixed_cost" : fixed_costs[k],
                    "var_cost_dist": var_costs[k]
                    }
            vehicle_types.append(vehicle_type)

        # create copies of vehicles of the same type to run OR-Tools heuristic
        for k in range(nb_vehicles):
            maxNbVeh = max_num_veh[k]
            vehicles_capacities.extend([capacities[k] for i in range(maxNbVeh)])
            vehicles_fixed_costs.extend([fixed_costs[k] for i in range(maxNbVeh)])
            vehicles_var_costs.extend([var_costs[k] for i in range(maxNbVeh)])
            index += max_num_veh[k]

        id_point = 0
        # Create points
        for current_id in range(nb_points+1):
            point_id = int(next(instance_iter))
            if point_id != current_id + 1:
                raise Exception("Unexpected index")
            x_coord = int(next(instance_iter))
            y_coord = int(next(instance_iter))
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
        for current_id in range(nb_points+1):
            point_id = int(next(instance_iter))
            if point_id != current_id + 1:
                raise Exception("Unexpected index")
            points[current_id]["demand"] = int(next(instance_iter))
            jobs.append(points[current_id]["demand"])
        data["demands"] = jobs

        element = next(instance_iter)
        if element != "DEPOT_SECTION":
            raise Exception("Expected line DEPOT_SECTION")
        next(instance_iter) # pass id depot

        end_depot_section = int(next(instance_iter))
        if end_depot_section != -1:
            raise Exception("Expected only one depot.")

    else: # classic instances format

        nb_points = int(firstRead)
        next(instance_iter) # pass id depot (always 0)
        depot_x = int(next(instance_iter))
        depot_y = int(next(instance_iter))
        depot_demand = int(next(instance_iter))
        id_point = 0

        # Initialize the points with depot
        points.append({"x": depot_x,
                "y": depot_y,
                "demand": depot_demand,
                "id": id_point
                })
        
        jobs = [0]
        for i in range(nb_points):
            id_point += 1
            next(instance_iter) # pass id point (take index)
            x_coord = int(next(instance_iter))
            y_coord = int(next(instance_iter))
            demand = int(next(instance_iter))
            points.append({"x": x_coord,
                    "y": y_coord,
                    "demand": demand,
                    "id": id_point})
            jobs.append(demand) 
        data["demands"] = jobs
        
        nb_vehicles = int(next(instance_iter))
        vehicle_types = []
        
        for k in range(1, nb_vehicles+1):
            capacity = int(next(instance_iter))
            fixed_cost = float(next(instance_iter))
            var_cost_dist = float(next(instance_iter))
            next(instance_iter) # pass min number
            max_number = int(next(instance_iter))
            vehicle_type = {"id": k,  # we cannot have an id less than 1
                    "start_point_id": 0,
                    "end_point_id": 0,
                    "capacity": capacity,
                    "max_number": max_number,
                    "fixed_cost" : fixed_cost,
                    "var_cost_dist": var_cost_dist
                    }
            vehicle_types.append(vehicle_type)
            for i in range(max_number):
                vehicles_capacities.append(capacity)
                vehicles_var_costs.append(var_cost_dist)
                vehicles_fixed_costs.append(fixed_cost)
                index += 1
        
    data['vehicle_capacities'] = vehicles_capacities
    data['var_costs'] = vehicles_var_costs
    data['fixed_costs'] = vehicles_fixed_costs 
    data['num_vehicles'] = index
    data['depot'] = 0

    # compute the links of graph
    links = []
    matrix = [[0 for i in range((len(points)))] for i in range(len(points))]
    nb_link = 0
    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            dist = compute_euclidean_distance(point["x"],
                                              point["y"],
                                              points[j]["x"],
                                              points[j]["y"])

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
            "VehicleTypes": vehicle_types,
            "Links": links
            }

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
    
