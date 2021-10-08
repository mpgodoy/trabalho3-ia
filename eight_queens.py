from random import random, randint, choices
import matplotlib.pyplot as plt

def getSameLineConflicts(individual):
    dictOfElems = dict()

    for elem in individual:
        if elem in dictOfElems:
            dictOfElems[elem] += 1
        else:
            dictOfElems[elem] = 1    
 
    dictOfElems = { key:value for key, value in dictOfElems.items() if value > 1}

    return len(dictOfElems.keys())

def getDiagonalConflicts(individual):
    conflicts = 0

    for i in range(8):
        leftToGo = 8 - i
        for j in range(8 - leftToGo):
            columnDif = abs(i -j)
            rowDif = abs(individual[i] - individual[j])
            if (rowDif == columnDif):
                conflicts += 1
    
    return conflicts

def evaluate(individual):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 9.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """

    return getDiagonalConflicts(individual) + getSameLineConflicts(individual)


def tournament(participants):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """

    listOfConflicts = []

    for participant in participants:
        listOfConflicts.append(evaluate(participant))

    indexOfBestChoice = listOfConflicts.index(min(listOfConflicts))

    return participants[indexOfBestChoice]

def crossover(parent1, parent2, index):
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """

    elementsOfFirstParent = parent1[:index]
    elementsOfSecondParent = parent2[:index]

    parent1[:index] = elementsOfSecondParent
    parent2[:index] = elementsOfFirstParent

    return parent1[:], parent2[:]


def mutate(individual, m):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """

    if random() >= m:
        return individual[:]

    randomPosition = randint(0, len(individual) - 1)
    randomNumber = randint(1,8)

    individual[randomPosition] = randomNumber

    return individual[:]

def getNonConflicts(individual):
    nonConflicts = 0

    for i in range(8):
        leftToGo = 8 - i
        for j in range(8 - leftToGo):
            columnDif = abs(i -j)
            rowDif = abs(individual[i] - individual[j])
            if (rowDif != columnDif and individual[i] != individual[j]):
                nonConflicts += 1
    
    return nonConflicts

    
def fitness(element):
    return tournament()
    #return getNonConflicts(element)

def selecao(population, k):
    p1 = tournament(choices(population=population, k=k))
    p2 = tournament(choices(population=population, k=k))

    return p1, p2

def run_ga(g, n, k, m, e):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:bool - se vai haver elitismo
    :return:list - melhor individuo encontrado
    """

    maxNumberOfConflicts = []
    minNumberOfConflicts = []
    averageNumberOfConflicts = []

    population = []

    for i in range (n):
        newSample = []
        for j in range(8):
            newSample.append(randint(1,8))
        population.append(newSample)
        
    for i in range(g):
        thisGenerationConflicts = []
        newPopulation = []
        
        if (e):
            newPopulation.append(tournament(population))

        while len(newPopulation) < n:
            p1, p2 = selecao(population, k)

            o1, o2 = crossover(p1, p2, randint(0, 7))

            o1 = mutate(o1, m)
            o2 = mutate(o2, m)

            newPopulation.extend([o1, o2])

        population = newPopulation[:]

        for element in population:
            conflict = evaluate(element)

            thisGenerationConflicts.append(conflict)
        
        maxNumberOfConflicts.append(max(thisGenerationConflicts))
        minNumberOfConflicts.append(min(thisGenerationConflicts))
        averageNumberOfConflicts.append(sum(thisGenerationConflicts) / n)
    
    plt.plot([i for i in range(g)], maxNumberOfConflicts, color="red", label="max conflitos")
    plt.plot([i for i in range(g)], minNumberOfConflicts, color="blue", label="min conflitos")
    plt.plot([i for i in range(g)], averageNumberOfConflicts, color="green", label="media conflitos")
    plt.legend()

    plt.xlabel('geracoes')
    plt.ylabel('conflitos')

    plt.title('Oito rainhas')

    plt.show()

    return tournament(population)

if __name__ == '__main__':
    print(evaluate(run_ga(5000, 100, 2, 0.05, True)))
