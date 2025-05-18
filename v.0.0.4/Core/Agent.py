

import math
import Genome
import random as rnd

class AgentController():
    def __init__(self, count_of_agent, answer):
        self.answer = answer
        self.ID_of_population = 0
        self.max_of_population = count_of_agent
        self.main_population = []
        self.intermediate_population = []
        self.general_fitness = self.calculate_general_fitness()
        self.spawn_start_population(len(answer), count_of_agent)


    def update(self):
        if (self.ID_of_population % 100 == 0):
            print(f"BEST AGENT OF {self.ID_of_population} - {self.main_population[0].genome} - {self.main_population[0].hamming_distance}")
        self.ID_of_population+=1
        self.calculate_general_fitness()
        self.create_intermediate_population()
        self.create_new_population()

    def check_answer(self):
        for agent in self.main_population:
            if agent.hamming_distance == 0:
                print(f"ANSWER FOUND! - GENERATION:{self.ID_of_population}"\
                    f"\nBEST AGENT - {self.main_population[0].genome}"\
                    f"\nHAMMING DISTANCE - {self.main_population[0].hamming_distance}")
                return True
        return False


    def spawn_start_population(self, genome_length, count_of_agent):
        for _ in range(count_of_agent):
            self.main_population.append(Agent(genome_length, self.answer))


    def calculate_general_fitness(self):
        sum_fitness = 0
        for agent in self.main_population:
            sum_fitness += agent.calculate_fitness()
            
        return sum_fitness


    def create_intermediate_population(self):
        tournament_size = max(2, int(0.02 * len(self.main_population)))
        while (len(self.intermediate_population)) < self.max_of_population:
            tournament = rnd.sample(self.main_population, tournament_size)
            winner = min(tournament, key=lambda agent: agent.hamming_distance)
            self.intermediate_population.append(winner)
        self.main_population.clear()


    def create_new_population(self):
        while len(self.main_population) < self.max_of_population:
            parent1 = rnd.choice(self.intermediate_population)
            parent2 = rnd.choice(self.intermediate_population)
            child = parent1.reproduce(parent2)
            self.main_population.append(child)
        self.main_population.sort(key=lambda agent: agent.hamming_distance)
        self.intermediate_population.clear()


class Agent():
    def __init__(self, genome_length, answer, parent1=None, parent2=None):
        self.genome = Genome.Genome(genome_length, parent1, parent2).genome
        self.answer = answer
        self.hamming_distance = self.calculate_fitness()


    def calculate_fitness(self):
        errors = 0
        for i in range(len(self.genome)):
            if self.genome[i] != self.answer[i]:
                errors+=1   

        return errors

    def reproduce(self, partner):
        return Agent(len(self.genome), self.answer, self, partner)
