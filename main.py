
"""
main.py
Made by Team Shire Peasants 3
"""

import csv
import sys
import copy
import datetime
import numpy as np
from code.algorithms import twist, randomize, greedy, breadthfirst, eha, ehaplus, hillclimb, generalfunctions
from code.classes import lattice, element
from code.visualisation import visualise

if __name__ == '__main__':
    TwoD_moves = [1, -1, 2, -2]
    ThreeD_moves = [1, -1, 2, -2, 3, -3]
    protein_string_list = ["HHPHHHPH", "HHPHHHPHPHHHPH", "HPHPPHHPHPPHPHHPPHPH", "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP",
                            "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH", "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP",
                            "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC", "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH",
                            "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH", "PPHPPPHPPPHPHHHHPHPHPHPHH", "HHPPHPPHPPHPPHPPHPPHPPHH",
                            "PPHHHPHHHPPPHPHHPHHPPHPHHHHPHPPHHHHHPHPHHPPHHP", "PPHPPHHPPHHPPPPPHHHHHHHHHHPPPPPPHHPPHHPPHPPHHHHH",
                            "PPHHHPHHHHHHHHPPPHHHHHHHHHHPHPPPHHHHHHHHHHHHPPPPHHHHHHPHHPHP"]

    # Checks if the correct number of arguments have been given
    if len(sys.argv) != 5:

        # Prints operation explanation if one requires it
        if len(sys.argv) == 2 and sys.argv[1] == "help":
            print("Select any of the following algorithms:\n'random', 'twist', 'greedy', 'breadth', 'pull' and 'eha'")
            print("Select any of the following string numbers:")
            for i in range(len(protein_string_list)):
                print(f"{i}: {protein_string_list[i]}")
            print("Number of iterations:\nAny number higher than 0 will work.\nWhen you select 1 or higher some statistical results will be displayed.")
            print("Dimension:\nType '2' for 2D and '3' for 3D.")
        else:
            print("usage: python main.py algorithm string_nr iterations dimension\nFor more information type 'python main.py help'")

        sys.exit(1)

    # Asks user if they want the list and graphical result for the best found solution
    want_list_graph = input("Would you like a list and graph of the best found solution? (y/n)\n")

    algorithm = sys.argv[1]
    iterations = int(sys.argv[3])
    dimension = int(sys.argv[4])
    algorithms = ["random", "twist", "greedy", "breadth", "pull", "eha"]

    # Checks if data_structure is available
    if algorithm not in algorithms:
        print("You must choose either 'random', 'twist', 'greedy', 'breadth', 'pull', 'eha'")
        sys.exit(1)

    # Checks to see if given index corresponds to a protein string
    if int(sys.argv[2]) < 0 or int(sys.argv[2]) > 13:
        print("Choose a string number between 0 and 13.")
        sys.exit(1)
    protein_string = protein_string_list[int(sys.argv[2])]

    # Checks if iterations is above 0
    if iterations <= 0:
        print("You must choose a positive number.")
        sys.exit(1)

    if dimension == 2:
        moves = TwoD_moves
    elif dimension == 3:
        moves = ThreeD_moves
    else:
        print("You must choose '2' for 2D or '3' for 3D.")
        sys.exit(1)

    # Sets up list, dictionary and matrix for given protein string
    test_lattice = lattice.Lattice(protein_string)
    test_lattice.load_dict()
    test_lattice.load_matrix()
    test_lattice.load_TwoD_matrix()
    test_lattice.load_list()

    state_list = []
    stability_list = []

    ## -- Start algorithms --
    if algorithm == "twist":
        border_size = float(input("Enter a size restriction (in chain lengths) between 0-1. Default is 0.5\n"))

        if (border_size < 0) or (border_size > 1):
            border_size = 0.5

        for i in range(iterations):

            chain, stability = twist.twist(test_lattice, moves, border_size)
            stability_list.append(stability)
            state_list.append(chain)

            # reset the lattice
            test_lattice = lattice.Lattice(protein_string)
            test_lattice.load_list()

    if algorithm == "random":
        for i in range(iterations):
            random_list, stability = randomize.sarw_dict(test_lattice, moves)
            state_list.append(random_list)
            stability_list.append(stability)

            # reset the lattice
            test_lattice = lattice.Lattice(protein_string)
            test_lattice.load_list()

    if algorithm == "breadth":
        test_lattice_breadth = lattice.Lattice(protein_string)
        element_P = element.Element("P")
        element_H = element.Element("H")
        element_C = element.Element("C")

        for i in range(iterations):
            result_states, stabilities = breadthfirst.bfs(test_lattice_breadth, element_P, element_H, element_C, moves)
            if len(result_states) != 0:
                best_state_iteration, best_stability_iteration = generalfunctions.get_best_state(stabilities, result_states)
                state_list.append(best_state_iteration)
                stability_list.append(best_stability_iteration)
            test_lattice_breadth = lattice.Lattice(protein_string)

        # generalfunctions.write_to_worksheet(stability_list, int(sys.argv[2]), algorithm)

    if algorithm == "greedy":
        # Start iterations of greedy algorithm
        for i in range(iterations):
            greedy_state, stability = greedy.greedy_dict(test_lattice, moves)

            # append states and stability to lists
            state_list.append(greedy_state)
            stability_list.append(stability)

            # reset the lattice
            test_lattice = lattice.Lattice(protein_string)
            test_lattice.load_list()

    if algorithm == "eha":
        while len(stability_list) < iterations:
            stability, chain = ehaplus.ehaplus(test_lattice, moves, 5)
            if len(stability_list) == 0:
                stability_list.append(stability)
                state_list.append(chain)
            elif stability < min(stability_list) / 2:
                stability_list.append(stability)
                state_list.append(chain)

            # reset the lattice
            test_lattice = lattice.Lattice(protein_string)
            test_lattice.load_list()

    if algorithm == "pull":

        # Gets random solution and stability
        random_solution, random_stability = randomize.sarw_dict(test_lattice, moves)

        for i in range(iterations):
            solution, stability = hillclimb.pullmove(random_solution, random_stability)
            state_list.append(solution)
            stability_list.append(stability)

        # generalfunctions.write_to_worksheet(stability_list, int(sys.argv[2]), algorithm)

    # Calculates best found state and stability
    best_state, best_stability = generalfunctions.get_best_state(stability_list, state_list)
    #print(stability_list)
    #print(state_list)

    # If 2 or more iterations are selected, it will print stability statistics
    if iterations >= 2:
        print(generalfunctions.list_stats(stability_list, algorithm))

    # If y or yes is selected the user will get a list and graph of the best found solution
    if want_list_graph == "y" or want_list_graph == "yes":
        print(best_state)
        visualise.chain_list_3Dplot(best_state, best_stability)
