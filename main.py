## recurrent sigmoid synapse based neural network
## fed through genetic algorithm with PID controlled mutation
## breeding is based on success of creatures

## IMPORTS
import matplotlib.pyplot as plt
import geneticAlgorithm as ga
import time,math,pid
from multiprocessing import Pool
from functools import partial

## CONSTANTS
epochs         = 50
noOfCreatures  = 40
feedbackCycles = 5
hiddenNeurons  = 15
inputNeurons   = 10
outputNeurons  = 10
rangeOfInputs  = 10
maxTaylorOrder = 3
Kp             = 10
Kd             = 10
Ki             = 10
p              = pid.PID(Kp,Ki,Kd)

## INITITAL VALUES
mu             = 0

## LOCAL FUNCTIONS
def makeTargets(inputs):
    targets  = list()
    for i in inputs:
        if (i>=4) and (i<=6):
            j=1
        else:
            j=0
        targets.append(j)
    return targets

def initialize(maxTaylorOrder):
    inputs = ga.generateInputs( inputNeurons , rangeOfInputs )
    targets = makeTargets( inputs )
    population = ga.populate( noOfCreatures, inputNeurons, hiddenNeurons, outputNeurons, maxTaylorOrder )
    best = ga.findBestCreature( population )
    best.error = 2.0
    plt.ion()
    return population, inputs, targets, best

def displayProgress(epoch, mu, best):
    plt.axis([0,rangeOfInputs,-.5,1.5])
    plt.plot(inputs,targets)
    plt.pause(0.0001)
    plt.axis([0,rangeOfInputs,-.5,1.5])
    plt.plot(inputs,best.output)
    plt.pause(0.0001)
    plt.cla()
    print "mu:", round(mu,6),"error:",round(best.error,6), "epoch:",epoch
    return time.time()

def evolveToSolution(epochs, population, mu, noOfCreatures):
    lastTime = 0
    for j in range(epochs):
        p.Kp = Kp * (1.0-(float(j)/float(epochs)))
        p.Kd = Kd * (1.0-(float(j)/float(epochs)))
        p.Ki = Ki * (1.0-(float(j)/float(epochs)))
        population = ga.evolve( population, mu, inputs, targets, feedbackCycles, noOfCreatures, inputNeurons, hiddenNeurons, outputNeurons)
        best = ga.findBestCreature( population )
        mu = abs(p.update(best.error))

        if (time.time() > lastTime +  .5):
            lastTime = displayProgress(j, mu, best)

def printFinalSolution(best):
    newlist = list()
    print "===================================="
    print "The best approximation"
    print "has an error of:" , best.error
    plt.show(block=False)
    plt.ioff()
    plt.plot(inputs,targets)
    plt.plot(inputs,best.output)
    plt.ylabel('Amplitude')
    plt.xlabel('Time')
    plt.axis('auto')
    plt.legend(('Target','Approximation'))
    plt.show()

if __name__ == '__main__':
    population, inputs, targets, best = initialize(maxTaylorOrder)
    evolveToSolution(epochs, population, mu, noOfCreatures)
    printFinalSolution(ga.findBestCreature( population ))
