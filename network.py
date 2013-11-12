import random, math

'''=======================
  Class network:
      class network is a fully connected recurrent neural network
      that uses Fourier elements as its primary transfer function
      between neurons.

  input: (int, int, int)
      input layer neuron count, hidden layer neuron count, output layer neuron count

    functions:
        run(inputList, itterations) - execute several steps in a row
        mutate(mu) - mutates by ammount mu (gaussian spread)
        step(inputsList) - walk forward one step
        setOutput() - private method
        stepLayer(layer) - private method

=========================='''

class network:
    def  __init__(self, inputLayer, hiddenLayer, outputLayer):
        self.inputLayer = list()
        self.hiddenLayer = list()
        self.outputLayer = list()
        self.inputToHiddenSynapses = list()
        self.hiddenToHiddenSynapses = list()
        self.hiddenToOutputSynapses = list()
        self.output = list()
        self.error = 10**10
        for iL in range(inputLayer):  ## build input neurons
            self.inputLayer.append(self.neuron())
        for hL in range(hiddenLayer): ## build hidden neurons
            self.hiddenLayer.append(self.neuron())
        for oL in range(outputLayer): ## build output neurons
            self.outputLayer.append(self.neuron())
        for iL in self.inputLayer:
            for hL in self.hiddenLayer:  ## build input synapses
                self.inputToHiddenSynapses.append(self.synapse(iL,hL))
                iL.synapseList.append(self.inputToHiddenSynapses[-1])
        for hL1 in self.hiddenLayer:
            for hL2 in self.hiddenLayer: ## build hidden synapses
                self.hiddenToHiddenSynapses.append(self.synapse(hL1,hL2))
                hL1.synapseList.append(self.hiddenToHiddenSynapses[-1])
        for hL in self.hiddenLayer:
            for oL in self.outputLayer:  ## build output synapses
                self.hiddenToOutputSynapses.append(self.synapse(hL1,oL))
                hL.synapseList.append(self.hiddenToOutputSynapses[-1])
                
    def stepLayer(self, layer):
        for n in layer: #for each neuron in the input layer
            if n.testCharge():
                for s in n.synapseList:
                    s.fire() ## execute a synapse
                n.charge = 0
            n.reuptake()
        return layer
    
    def step(self,inputList):
        for i in range(len(inputList)): ## set input layer to inputList
            self.inputLayer[i].charge = inputList[i]
        self.inputLayer  = self.stepLayer(self.inputLayer)
        self.hiddenLayer = self.stepLayer(self.hiddenLayer)
        self.outputLayer = self.stepLayer(self.outputLayer)
        self.setOutput()

    def run(self,inputList,itterations):
        for i in range(itterations):
            self.step(inputList)
            
    def setOutput(self):
        self.output = list()
        for n in self.outputLayer:
            self.output.append(n.charge)
            
    def mutate(self,mu):
        for n in self.inputLayer:
            n.mutate(mu)
        for n in self.hiddenLayer:
            n.mutate(mu)
        for n in self.outputLayer:
            n.mutate(mu)
        for s in self.inputToHiddenSynapses:
            s.mutate(mu)
        for s in self.hiddenToHiddenSynapses:
            s.mutate(mu)
        for s in self.hiddenToOutputSynapses:
            s.mutate(mu)

    class neuron:
        def __init__(self):
            self.threshold,self.inbox,self.charge,self.synapseList = 0,0,0,list()
        def testCharge(self):
            if abs(self.charge) >= abs(self.threshold):
                return True
            else:
                return False
        def reuptake(self):##add to ready to fire queue
            self.charge += self.inbox
            self.inbox = 0
        def mutate(self, mu):
            self.threshold = random.gauss(self.threshold,mu)

    class synapse:
        def __init__(self,neuron1,neuron2):
            self.a,self.b,self.c,self.neuron1,self.neuron2 = 0,0,0,neuron1,neuron2
        def fire(self):
            self.neuron2.inbox += self.a*math.cos(self.b*self.neuron1.charge+self.c)
        def mutate(self, mu):
            self.a,self.b,self.c = random.gauss(self.a,mu),random.gauss(self.b,mu),random.gauss(self.c,mu)

