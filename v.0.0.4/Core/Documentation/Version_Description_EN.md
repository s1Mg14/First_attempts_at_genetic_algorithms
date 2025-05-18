# Version Description (v.0.0.4)
---
## Short description
Version 0.0.4 is an implementation of a genetic algorithm for finding a target string. Key changes:
- Complete refactoring of the architecture
- Transition from life simulation to classical GA
- Removal of the GUI in favor of a console version
- Optimization of memory handling
## Table of Contents
* [*Agent.py*](#agent.py)
	* [*AgentController*](#agentcontroller)
	* [*Agent*](#agent)
* [*Genome.py*](#genome.py)
	* [*Genome*](#genome)
* [*Core.py*](#genome.py)
* [*Addition*](#addition)
	* [*Roadmap*](#roadmap) 
---

## Version structure
| File      |                Classes |
| :-------- | ---------------------: |
| Agent.py  | AgentController, Agent |
| Genome.py |                 Genome |
| Core.py   |            Main script |

## Class Description

---

<div align="center">

### Agent.py

</div>

---
[Back to table of contents](#table-of-contents)
#### AgentController

**The constructor of the AgentController** works according to this algorithm:
* Attributes are passed during creation - **count_of_agent, answer**.
	* **count_of_agent** - number of agents in the population.
	* **answer** - the reference answer you need to find.
* Initializing variables and assigning values, creating an initial population and an intermediate population:\
**Program implementation:**
	```python
	self.answer = answer
	self.ID_of_population = 0
	self.max_of_population = count_of_agent
	self.main_population = []
	self.intermediate_population = []
	self.general_fitness = self.calculate_general_fitness()
	self.spawn_start_population(len(answer), count_of_agent)

| Method                           | Attributes                                | Description                                                                                                                                         | Return value                                        |
| :------------------------------- | :---------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------- |
| update()                         | -                                         | Calls the specified set of commands each iteration of the main loop                                                                                 | -                                                   |
| spawn_start_population()         | genome_length(int)<br>count_of_agent(int) | Creates an initial population of count_of_agent individuals with a genome of genome_length                                                          | -                                                   |
| check_answer()                   | -                                         | Checks if the reference answer is found                                                                                                             | If the answer is found - true<br>Otherwise - false  |
| calculate_general_fitness()      | -                                         | Calculates the total adaptation value of the population<br>But currently not used (to be fixed soon).                                               | Total population adaptability in a given generation |
| create_intermediate_population() | -                                         | Creates an intermediate population of individuals using tournament selection<br>**Before completion, cleans the main population**                   | -                                                   |
| create_new_population()          | -                                         | Creates the main population by crossing random agents from the intermediate population<br>**Before completion, cleans the intermediate population** | -                                                   |

* **create_intermediate_population()** - creates an intermediate population using this algorithm:
	* Agents are selected from the main population in number according to the formula **max(2, int(0.02 * len(self.main_population)))**.
	* The group is sorted by the adaptability of each agent.
	* The best individual is selected and added to the intermediate population.
	* Steps are repeated until a population of the required size is reached.
	* Zeroing in on the core population.\
	**Program implementation:**
	```python
	def create_intermediate_population(self):
	    tournament_size = max(2, int(0.02 * len(self.main_population)))
	    while (len(self.intermediate_population)) < self.max_of_population:
	        tournament = rnd.sample(self.main_population, tournament_size)
	        winner = min(tournament, key=lambda agent: agent.hamming_distance)
	        self.intermediate_population.append(winner)
	    self.main_population.clear()
	
* **create_new_population()** - creates a new main population from the intermediate population using this algorithm:
	* Random agents are selected from the intermediate population.
	* Selected agents are interbred.
	* The offspring is added to the main population.
	* Steps are repeated until the desired population size is reached.
	** The intermediate population is zeroed out. **
	** Program implementation:**
	```python
	def create_new_population(self):
	    while len(self.main_population) < self.max_of_population:
	        parent1 = rnd.choice(self.intermediate_population)
	        parent2 = rnd.choice(self.intermediate_population)
	        child = parent1.reproduce(parent2)
	        self.main_population.append(child)
	    self.main_population.sort(key=lambda agent: agent.hamming_distance)
	    self.intermediate_population.clear()

---
[Back to table of contents](#table-of-contents)
#### Agent
**The constructor of the Agent** class works according to this algorithm:
* Attributes passed at creation are **genome_length, answer, parent1, parent2**.
	* **genome_length** is the length of the agent's genome.
	* **answer** - reference answer.
	* **parent1** - first parent.
	* **parent2** - second parent.
* Genome initialization and storage :
	```python
	self.genome = Genome.Genome(genome_length, parent1, parent2).genome
* Preserving the reference response, for transmission to the next generation (it is worth getting rid of this item and revising it):
	```python
	self.answer = answer
* Calculating the adaptability of an agent:
	```python
	self.hamming_distance = self.calculate_fitness()

| Method              | Attributes     | Description                                                              | Return value                        |
| :------------------ | :------------- | :----------------------------------------------------------------------- | :---------------------------------- |
| calculate_fitness() | -              | Calculates the agent's fitness value                                     | Number of errors (Hamming distance) |
| reproduce()         | partner(Agent) | Creates a new agent based on the genes of the individual and its partner | -                                   |

* **calculate_fitness()** - calculates the adaptability of the agent.
Returns the number of errors (differences from the reference answer) as the Hamming distance. The closer the return value is to zero, the more adaptable the agent is.\
**Program implementation:**
	```python
	def calculate_fitness(self):
	    errors = 0
	    for i in range(len(self.genome)):
	        if self.genome[i] != self.answer[i]:
	            errors+=1   
	
	    return errors
	   
* **reproduce()** - creates a new individual based on the genomes of the parents.
**Program implementation:**
	```python
	def reproduce(self, partner):
    	return Agent(len(self.genome), self.answer, self, partner)

---

<div align="center">

### Genome.py

</div>

---
[Back to table of contents](#table-of-contents)
#### Genome

**The constructor of the Genome** class works according to this algorithm:
* Attributes passed in at creation are **length, parent1, parent2**.
	* **length** - the desired length of the genome.
	* **parent1, parent2** - parents of the new agent. Default is None.
* Check if the agent has parents.
* Если их нет, либо отсутсвует один из них, то создаётся новая особь.
  <br>Иначе вызывается функция **inheritance()** и в неё передаются геномы родителей.
* По необходимости, полученный в предыдущем шаге, геном мутирует с помощью функции **mutate()**.

| Method          | Attributes                           | Description                                                      | Return value         |
| :-------------- | :----------------------------------- | :--------------------------------------------------------------- | :------------------- |
| create_genome() | length(int)                          | Creates a length length genome                                   | -                    |
| inheritance()   | parent1(Agent)<br>parent2(Agent)     | The function of creating a genome from parental genomes          | child_genome(Genome) |
| mutate()        | genome(Genome)<br>probability(float) | Mutation function of each gene with probability(default is 0.01) | genome(Genome)       |

* **inheritance()** - Creates a new genome from the genomes of the parents. Uses two-point crossover.\
**Program implementation:**
	```python
	def inheritance(self, parent1, parent2):
	    crossover_point1 = rnd.randint(1, len(parent1.genome) - 1)
	    crossover_point2 = rnd.randint(crossover_point1, len(parent1.genome))
	
	    child_genome = (
	        parent1.genome[:crossover_point1] +
	        parent2.genome[crossover_point1:crossover_point2] +
	        parent1.genome[crossover_point2:]
	    )
	    return child_genome

* **mutate()** - goes through all the alleles in the genome and changes them with some probability.\
  The default mutation probability is 0.01(10%).\
  Alleles are changed to random alleles from the constant ALPHABET.\
  **Program implementation:**
  ```python
  def mutate(self, genome, probability=0.01):
    for i in range(len(genome)):
        if (rnd.random() <= probability):
            genome[i] = rnd.choice(alphabet)

    return genome
---

<div align="center">

### Core.py

</div>

---
[Back to table of contents](#table-of-contents)
#### Core
**Core.py** - is the main file for starting the algorithm. In it, constants are described, agent controllers are created, the required response, genome length are entered, and the main loop is pierced.

| Constants            | Description                                        |
| :------------------- | :------------------------------------------------- |
| COUNT_OF_AGENTS      | Number of individuals in the population            |
| GENERATION_THRESHOLD | Generation threshold at which the simulation stops |


---
## Addition
[Back to table of contents](#table-of-contents)
#### Purposes of this version:
- [x] Implement a specific fitness function.
- [x] Implement tournament selection.
- [x] Implement a GA for string search.
	- [ ] Optimize this algorithm.
- [ ] Implement roulette selection.
- [ ] Realize the effect of general population fitness.

#### Differences from previous versions:
1. A lot of unnecessary functions are discarded.
2. Removed visualization and pygame.
3. From life simulation the algorithm has been reworked to approximate classical GA.
4. Removed the interface (console only).

#### Roadmap:
1. Realize the search for roots of quadratic equations.
	- [ ] Ralize this task in v.0.0.5 as the main goal
	- [ ] Train the v.0.0.4 algorithm to recognize and solve equations
2. Optimization of the string search algorithm.
