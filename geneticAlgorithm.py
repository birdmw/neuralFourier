import numpy as np
import random
import network
from operator import attrgetter
import copy

def populate( noOfCreatures, inputLayerCount, hiddenLayerCount, outputLayerCount, maxTaylorOrder ):
    population = list()
    for i in range( noOfCreatures ) :
        population.append( network.network(inputLayerCount, hiddenLayerCount, outputLayerCount, maxTaylorOrder) )
    return population

def train( population, inputs, targets, itterationsPerRun ):
    for c in population:
        c.error = 0
        c.run(inputs,  itterationsPerRun)
        for i in range(len(targets)):
            c.error += abs ( targets[ i ] - c.output[i] )
    return population

def prune( population ):
    summation = 0
    deleteMe = list()
    for c in population:
        summation += c.error
    average = summation / len( population )
    for c in population:
        if ( c.error > average ):
            population.remove(c)
    return population

def printErrors(population):
    print "Errors:"
    for c in population:
        print c.error

def repopulateToMax(population, noOfCreatures, inp, hid, outp):
    while ( len( population ) <= noOfCreatures ):
        try:
            mother = weighted_choice ( population )
            father = weighted_choice ( population )
            #mother = random.choice ( population )
            #father = random.choice ( population )
        except UnboundLocalError:
            print "All of the population was eliminated"
        offspring = mate ( mother, father, inp, hid, outp )
        population.append( offspring )
    return population

def weighted_choice(population):
    choices = list()
    highestError=0
    for c in population:
        if (c.error<=10**10):
            highestError = max(c.error,highestError)
    for c in population:
        if (c.error<=10**10):
            choices.append([c,highestError-c.error])
    total = sum(w for c, w in choices)
    r = random.uniform(0,total)
    upto = 0
    for c, w in choices:
        if upto + w > r:
            return c
        upto += w
    #it should not make it here
    choice = random.choice(population)
    #print "choice of:",choice,"with input layer:",choice.inputLayer
    return choice

def mate(mother, father, inp, hid, outp):
    offspring = network.network(inp,hid,outp,random.choice([mother.maxTaylorOrder, father.maxTaylorOrder]))

    for i in range (inp):
        offspring.inputLayer[i].threshold = random.choice ([mother.inputLayer[i].threshold, father.inputLayer[i].threshold])
        offspring.inputLayer[i].x = random.choice ([mother.inputLayer[i].x, father.inputLayer[i].x])
        offspring.inputLayer[i].n = random.choice ([mother.inputLayer[i].n, father.inputLayer[i].n])
    for i in range (hid):
        offspring.hiddenLayer[i].threshold = random.choice ([mother.hiddenLayer[i].threshold, father.hiddenLayer[i].threshold])
        offspring.hiddenLayer[i].x = random.choice ([mother.hiddenLayer[i].x, father.hiddenLayer[i].x])
        offspring.hiddenLayer[i].n = random.choice ([mother.hiddenLayer[i].n, father.hiddenLayer[i].n])
    for i in range (outp):
        offspring.outputLayer[i].threshold = random.choice ([mother.outputLayer[i].threshold, father.outputLayer[i].threshold])
        offspring.outputLayer[i].x = random.choice ([mother.outputLayer[i].x, father.outputLayer[i].x])
        offspring.outputLayer[i].n = random.choice ([mother.outputLayer[i].n, father.outputLayer[i].n])

    for i in range (len(offspring.inputToHiddenSynapses)):
        offspring.inputToHiddenSynapses[i].a = random.choice([mother.inputToHiddenSynapses[i].a, father.inputToHiddenSynapses[i].a])
    for i in range (len(offspring.inputToHiddenSynapses)):
        offspring.inputToHiddenSynapses[i].b = random.choice([mother.inputToHiddenSynapses[i].b, father.inputToHiddenSynapses[i].b])
    for i in range (len(offspring.inputToHiddenSynapses)):
        offspring.inputToHiddenSynapses[i].c = random.choice([mother.inputToHiddenSynapses[i].c, father.inputToHiddenSynapses[i].c])

    for i in range (len(offspring.hiddenToHiddenSynapses)):
        offspring.hiddenToHiddenSynapses[i].a = random.choice([mother.hiddenToHiddenSynapses[i].a, father.hiddenToHiddenSynapses[i].a])
    for i in range (len(offspring.hiddenToHiddenSynapses)):
        offspring.hiddenToHiddenSynapses[i].b = random.choice([mother.hiddenToHiddenSynapses[i].b, father.hiddenToHiddenSynapses[i].b])
    for i in range (len(offspring.hiddenToHiddenSynapses)):
        offspring.hiddenToHiddenSynapses[i].c = random.choice([mother.hiddenToHiddenSynapses[i].c, father.hiddenToHiddenSynapses[i].c])

    for i in range (len(offspring.hiddenToOutputSynapses)):
        offspring.hiddenToOutputSynapses[i].a = random.choice([mother.hiddenToOutputSynapses[i].a, father.hiddenToOutputSynapses[i].a])
    for i in range (len(offspring.hiddenToOutputSynapses)):
        offspring.hiddenToOutputSynapses[i].b = random.choice([mother.hiddenToOutputSynapses[i].b, father.hiddenToOutputSynapses[i].b])
    for i in range (len(offspring.hiddenToOutputSynapses)):
        offspring.hiddenToOutputSynapses[i].c = random.choice([mother.hiddenToOutputSynapses[i].c, father.hiddenToOutputSynapses[i].c])

    return offspring

def mutate( population, mu ):
    for c in population:
        c.mutate(mu)
    return population

def evolve(population, mutationAmmount, inputs, targets, itterationsPerRun, noOfCreatures, inp, hid, outp):
    population = train ( population, inputs, targets, itterationsPerRun )
    population = prune(population)
    population = repopulateToMax(population, noOfCreatures, inp, hid, outp)
    population = mutate(population, mutationAmmount)
    return population

def findBestCreature(population):
    best = population[0]
    for c in population:
        if (c.error < best.error):
            best = c
    return best

def generateInputs( numberOfInputs, rangeOfXaxis ) :
    inputs = np.arange(0,rangeOfXaxis,float(rangeOfXaxis)/float(numberOfInputs))
    return inputs
