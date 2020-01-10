from .element import Element
import numpy as np

"""Creates list or dictionary version of the protein string containing AA (amino acid) element objects"""

class Lattice:
    def __init__(self, element_string):
        self.elements = element_string
        self.lattice_list = []
        self.lattice_dict = {}
        self.matrix = None

    def load_list(self):
        """Takes string and adds element objects to a list"""
        for i in range(len(self.elements)):
            self.lattice_list.append(Element(self.elements[i]))

    def load_dict(self):
        """Takes string and adds element objects to a dictionary, the dictionary key is based on the index"""
        for i in range(len(self.elements)):
            self.lattice_dict[i] = Element(self.elements[i])

    def load_matrix(self):
        """Loads a 3D empty matrix which can be filled with objects, big enough so straight chains don't hit borders"""
        dimension = int(len(self.elements)*2.5)
        self.matrix = np.empty((dimension, dimension, dimension), dtype=object)

    def get_list(self):
        """Returns list of elements"""
        return self.lattice_list

    def get_dict(self):
        """Returns dictionary of elements"""
        return self.lattice_dict

    def get_matrix(self):
        """Returns matrix of elements"""
        return self.matrix

    def __str__(self):
        return self.lattice_list
