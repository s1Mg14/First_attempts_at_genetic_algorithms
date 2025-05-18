import random as rnd
import Agent
import Genome

# хяйнлши нрбер
ANSWER = str(input("ANSWER: "))

# йнмярюмрш
COUNT_OF_AGENTS = int(input("COUNT_OF_AGENTS: "))
GENERATION_THRESHOLD = 1500

AC = Agent.AgentController(COUNT_OF_AGENTS, ANSWER)

generation_counter = 0

while (generation_counter < GENERATION_THRESHOLD):
    if AC.check_answer() == True:
        break
    AC.update()
    generation_counter+=1

print(f"ANSWER: {ANSWER}")