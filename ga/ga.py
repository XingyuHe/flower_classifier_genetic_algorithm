import tensorflow as tf
import numpy as np
from individual import *


class GAWorker(object):

    def __init__(self, argmap):
        """
        Parameters
        ----------
        argmap should contains the following parameters:
            1. shape (shape of an individual)
            2. population_size
            3. initializer
            4. error_function
            5. truncation_size
            6. mutation_power
            7. max_generation
        """

        self.argmap = argmap
        self.population = []
        self.initialize_population()

    def evolve(self):
        """
        Parameters
        ----------
        argmap should contains the following parameters:
            1. shape (shape of an individual)
            2. population_size
            3. initializer
            4. error_function
            5. truncation_size
            6. mutation_power
            7. max_generation
            8. standard
        """

        max_generation = self.argmap["max_generation"]
        population_size = self.argmap["population_size"]
        mutation_power = self.argmap["mutation_power"]
        truncation_size = self.argmap["truncation_size"]

        population = []
        elite = None
        for g in range(max_generation):
            # g stands for generation
            for i in range(population_size - 1):
                # i stands for individual
                if g == 0:
                    child = Individual(self.argmap)
                    population.append(child)
                else:
                    # select the top T individual
                    parent = population[np.random.randint(0, truncation_size)]
                    child = self.mutate_individual(parent)
                # evaluate individual
                self.evaluate_inidvidual(child)

            if g != 1:
                population.append(Individual(self.argmap))
            else:
                population.append(elite)

            # sort individual by error
            population.sort(key=lambda x: x.error)
            elite = population[0]


    def mutate_individual(self, individual):
        """This function mutates one individual"""
        pass


    def evaluate_inidvidual(self, individual):
        """This function evaluates the error of one individual"""
        error_fn = self.argmap["error_fn"]
        individual.error = error_fn(individual.value)


    def select_individual(self, individual):
        """This function determines whether an individual should be selected
        for reproduction."""
        pass