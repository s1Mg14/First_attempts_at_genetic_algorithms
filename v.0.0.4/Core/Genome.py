import random as rnd

ALPHABET = "qwertyuiopasdfghjklzxcvbnm QWERTYUIOPASDFGHJKLZXCVBNM!?,.`'\"-1234567890"

class Genome():
    def __init__(self, length, parent1=None, parent2=None):
        self.genome = []
        if (parent1 == None or parent2 == None):
            self.create_genome(length)
        else:
            #self.genome = self.inheritance(parent1, parent2)
            self.genome = self.mutate(self.inheritance(parent1, parent2))

    def create_genome(self, length):
        self.genome = [rnd.choice(alphabet) for i in range(length)]

    def inheritance(self, parent1, parent2):
        crossover_point1 = rnd.randint(1, len(parent1.genome) - 1)
        crossover_point2 = rnd.randint(crossover_point1, len(parent1.genome))
    
        child_genome = (
            parent1.genome[:crossover_point1] +
            parent2.genome[crossover_point1:crossover_point2] +
            parent1.genome[crossover_point2:]
        )
        return child_genome

    def mutate(self, genome, probability=0.01):
        for i in range(len(genome)):
            if (rnd.random() <= probability):
                genome[i] = rnd.choice(alphabet)

        return genome