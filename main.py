## recurrent Fourier synapse based neural network
## fed through genetic algorithm with PID controlled mutation 
## breeding is based on success of creatures

## IMPORTS
import matplotlib.pyplot as plt
import geneticAlgorithm as ga
import time,math,pid

## CONSTANTS
epochs         = 150
noOfCreatures  = 40
feedbackCycles = 4
hiddenNeurons  = 10
inputNeurons   = 10
outputNeurons  = 10
rangeOfInputs  = 10
p              = pid.PID(.005,.000,.005)

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

def initialize():
    inputs = ga.generateInputs( inputNeurons , rangeOfInputs )
    targets = makeTargets( inputs )
    population = ga.populate( noOfCreatures, inputNeurons, hiddenNeurons, outputNeurons )
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

def evolveToSolution(epochs, population, mu):
    lastTime = 0
    for j in range(epochs):
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

population, inputs, targets, best = initialize()
evolveToSolution(epochs, population, mu)
printFinalSolution(ga.findBestCreature( population ))
