from tkinter import *

import copy
 
from tabulate import tabulate


def AND(input1, input2):
    return input1&input2
    
def OR(input1, input2):
    return input1|input2
 
def NOT(input):
    if input == 0:
        return 1
    if input == 1:
        return 0
 
def XOR(input1, input2):
    return input1^input2
 
def XNOR(input1, input2):
    return NOT(XOR(input1, input2))
 
def NOR(input1, input2):
    return NOT(OR(input1, input2))
 
def NAND(input1, input2):
    return NOT(AND(input1, input2))
 
class Window:
    def __init__(self):
        self.root = Tk() # root widget (window)
        self.root.geometry("1920x1080")
        self.root.title("Logic Circuit Simulator")
        #self.logo = PhotoImage(file='9a6793bcadbf993c49cecb43d395ffcf8b5dd87eb0fd023631faf6457c140fdc.png')
 
        #self.root.iconphoto(False, self.logo)
 
 
    # tool section
        self.toolFrame = LabelFrame(self.root, text="Tools", width=100, height=500)
        #self.toolFrame.config(bg="lightgrey")
        self.toolFrame.grid(row=0, column=1, padx=5, pady=5)
        
        #lucio
        self.lucioFrame = Frame(self.toolFrame, width=100, height=100)
        self.lucioFrame.grid(row=0, column=0, padx=5, pady=5)
        #self.lucio = PhotoImage(file='Spray_L 3Fcio_Pixel.png')
        #self.lucioLabel = Label(self.lucioFrame, image=self.lucio)
        #self.lucioLabel.grid(row=0, column=0, padx=5, pady=5)
 
    # workFrame 
        self.workFrame = Frame(self.root, width=1500, height=550)
        self.workFrame.grid(row=0, column=0, padx=5, pady=5)
 
        #actual visual frame (the circuit goes in here) within workFrame
        self.visualFrame = LabelFrame(self.workFrame, text="Workspace", width=1800, height=500)
        self.visualFrame.config(bg="lightgrey")
        self.visualFrame.grid(row=1, column=0, padx=5, pady=5)
 
        #options bar frame 
        self.optionsLabelFrame = LabelFrame(self.workFrame, text="Options", width= 1515, height=30)
        self.optionsLabelFrame.config(bg="lightgrey")
        self.optionsLabelFrame.grid(row=0, column=0, padx=5, pady=5)
 
        #canvas (workspace) within visual frame
        self.workspace = Canvas(self.visualFrame, bg="lightgrey", width=1730, height=900)
        self.workspace.grid(row=0, column=0, padx=5, pady=5)
 
        #list of gates present in circuit (gate objects) 
        self.gatesAndIcons = []
 
        # solve, truth table, Boolean within options bar frame
        solveButton = Button(self.optionsLabelFrame, text="Solve circuit", command=lambda:self.getCircuitOutput(), relief="groove")
        truthButton = Button(self.optionsLabelFrame, text="Generate truth table", command=lambda:self.formatOutputForTruthTable(), relief="groove")
        booleanButton = Button(self.optionsLabelFrame, text="Generate Boolean Expression", command=lambda:self.formatOutputForBooleanExpression(), relief="groove")
 
 
        solveButton.grid(row=0, column=0, padx=5, pady=5)
        truthButton.grid(row=0, column=2, padx=5, pady=5)
        booleanButton.grid(row=0, column=4, padx=5, pady=5)
 
 
        #gates buttons within gates section within tool frame
        orButton = Button(self.toolFrame, text="OR", command=lambda:self.createOrGate(), relief="groove")
        andButton = Button(self.toolFrame, text="AND", command=lambda:self.createAndGate(), relief="groove")
        notButton = Button(self.toolFrame, text="NOT", command=lambda:self.createNotGate(), relief="groove")
        norButton = Button(self.toolFrame, text="NOR", command=lambda:self.createNorGate(), relief="groove")
        nandButton = Button(self.toolFrame, text="NAND", command=lambda:self.createNandGate(), relief="groove")
        xorButton = Button(self.toolFrame, text="XOR", command=lambda:self.createXorGate(), relief="groove")
        xnorButton = Button(self.toolFrame, text="XNOR", command=lambda:self.createXnorGate(), relief="groove")
 
        orButton.grid(row=2, column=0, padx=5, pady=5)
        andButton.grid(row=4, column=0, padx=5, pady=5)
        notButton.grid(row=6, column=0, padx=5, pady=5)
        norButton.grid(row=8, column=0, padx=5, pady=5)
        nandButton.grid(row=10, column=0, padx=5, pady=5)
        xorButton.grid(row=12, column=0, padx=5, pady=5)
        xnorButton.grid(row=14, column=0, padx=5, pady=5)
 
        #inputs buttons within gates section within tool frame
        constantOnButton = Button(self.toolFrame, text="Constant: On", command=lambda:self.createConstantOn(), relief="groove")
        constantOffButton = Button(self.toolFrame, text="Constant: Off", command=lambda:self.createConstantOff(), relief="groove")
 
        constantOnButton.grid(row=16, column=0, padx=5, pady=5)
        constantOffButton.grid(row=18, column=0, padx=5, pady=5)
 
        self.firstSelectedObject = None
        self.secondSelectedObject = None
 
        #output button within toolframe
        lightbulbButton = Button(self.toolFrame, text="Output", command=lambda:self.createLightbulb(), relief="groove")
 
        lightbulbButton.grid(row=20, column=0, padx=5, pady=5)
 
        self.constantList = []
 
        self.constantCounter = 0
 
        self.connectedGates = []
        self.lines = []
 
        self.IMAGE_PATH = "gate pictures/"
 
 
    def getNumOfInputs(self):
        return len(self.constantList)
 
    def showGatesAndIconsList(self):
        return self.gatesAndIcons
 
    def createLines(self):
        # delete all existing lines
        for i in self.lines:
            self.workspace.delete(i)
 
        for i in self.connectedGates:
            
 
            # if first thing is a constant and second is a not gate
            if (type(i[0]) in [constantOff, constantOn]) and (type(i[1]) == notGate):
                line = self.workspace.create_line(i[0].getOutputCoords()[0], i[0].getOutputCoords()[1], i[1].getInputCoords()[0], i[1].getInputCoords()[1], width = 2)
                self.workspace.tag_lower(line)
                self.lines.append(line)
 
            # elif first thing is a constant and second is any other gate
            elif (type(i[0]) in [constantOff, constantOn]) and (type(i[1]) in [orGate, andGate, norGate, nandGate, xorGate, xnorGate]):
                # check second gates inputs, to see which one is free
 
                # there is a connection between item 1 and item 2
                # use item 1's output and whichever of item 2's inputs is free in terms of lines on the canvas
                # or rather, draw a line where there is a direct link between the output of the previous and input of the next
 
                # two possible connected gates: one output to input1, one output to input2
                
 
                if i[1].getInput1() == i[0].getOutput():
                    line = self.workspace.create_line(i[0].getOutputCoords()[0], i[0].getOutputCoords()[1], i[1].getInput1Coords()[0], i[1].getInput1Coords()[1], width = 2)
                    self.workspace.tag_lower(line)
                    self.lines.append(line)
                    #print("\nline to input1")
 
                elif i[1].getInput2() == i[0].getOutput():
                    line = self.workspace.create_line(i[0].getOutputCoords()[0], i[0].getOutputCoords()[1], i[1].getInput2Coords()[0], i[1].getInput2Coords()[1], width = 2)
                    self.workspace.tag_lower(line)
                    self.lines.append(line)
                    #print("\nline to input2")
 
            elif type(i[0]) in [orGate, andGate, norGate, nandGate, xorGate, xnorGate, notGate, constantOff, constantOn] and type(i[1]) == lightbulb:
 
                if i[1].getInput() == i[0].getOutput():
                    line = self.workspace.create_line(i[0].getOutputCoords()[0], i[0].getOutputCoords()[1], i[1].getInputCoords()[0], i[1].getInputCoords()[1], width = 2)
                    self.workspace.tag_lower(line)
                    self.lines.append(line)
                    #print(i[0].getOutput(), i[1].getInput())
                    #print("\nline to input")
 
 
            elif type(i[0]) == notGate and type(i[1]) == notGate:
                if i[1].getInput() == i[0].getOutput():
                    line = self.workspace.create_line(i[0].getOutputCoords()[0], i[0].getOutputCoords()[1], i[1].getInputCoords()[0], i[1].getInputCoords()[1], width = 2)
                    self.workspace.tag_lower(line)
                    self.lines.append(line)
                    #print("\nline to input")
 
 
            elif type(i[0]) == notGate:
 
 
                if i[1].getInput1() == i[0].getOutput():
                    line = self.workspace.create_line(i[0].getOutputCoords()[0], i[0].getOutputCoords()[1], i[1].getInput1Coords()[0], i[1].getInput1Coords()[1], width = 2)
                    self.workspace.tag_lower(line)
                    self.lines.append(line)
                    #print("\nline to input1")
 
                elif i[1].getInput2() == i[0].getOutput():
                    line = self.workspace.create_line(i[0].getOutputCoords()[0], i[0].getOutputCoords()[1], i[1].getInput2Coords()[0], i[1].getInput2Coords()[1], width = 2)
                    self.workspace.tag_lower(line)
                    self.lines.append(line)
                    #print("\nline to input2")
 
            elif type(i[1]) == notGate:
 
                if i[1].getInput() == i[0].getOutput():
                    line = self.workspace.create_line(i[0].getOutputCoords()[0], i[0].getOutputCoords()[1], i[1].getInputCoords()[0], i[1].getInputCoords()[1], width = 2)
                    self.workspace.tag_lower(line)
                    self.lines.append(line)
                    #print("\nline to input")
 
 
            elif (type(i[0]) in [orGate, andGate, norGate, nandGate, xorGate, xnorGate]) and (type(i[1]) in [orGate, andGate, norGate, nandGate, xorGate, xnorGate]):
                if i[1].getInput1() == i[0].getOutput():
                    line = self.workspace.create_line(i[0].getOutputCoords()[0], i[0].getOutputCoords()[1], i[1].getInput1Coords()[0], i[1].getInput1Coords()[1], width = 2)
                    self.workspace.tag_lower(line)
                    self.lines.append(line)
                    #print("\nline to input1")
 
                elif i[1].getInput2() == i[0].getOutput():
                    line = self.workspace.create_line(i[0].getOutputCoords()[0], i[0].getOutputCoords()[1], i[1].getInput2Coords()[0], i[1].getInput2Coords()[1], width = 2)
                    self.workspace.tag_lower(line)
                    self.lines.append(line)
                    #print("\nline to input2")
 
    def setSelectedIcon(self, gate): 
 
        input1Flag = False
        input2Flag = False
 
        tempObject = None
        for i in self.gatesAndIcons:
            if gate == i[0]:
                tempObject = i[0]
 
 
 
        if self.firstSelectedObject == None and type(tempObject) != lightbulb: # make this variable None when the line has been made  
            self.firstSelectedObject = tempObject
 
 
        else:
            if tempObject == self.firstSelectedObject:
                self.secondSelectedObject = None
 
            elif type(tempObject) == lightbulb:
                if tempObject.getInput() == None:
                    self.secondSelectedObject = tempObject
                    self.secondSelectedObject.setInput(self.firstSelectedObject.getOutput()) 
 
                    
                else:
                    self.firstSelectedObject = None
        
            elif type(tempObject) in [constantOff, constantOn]:
                self.firstSelectedObject = None
                self.secondSelectedObject = None
 
            elif (type(self.firstSelectedObject) in [constantOff, constantOn]) and (type(tempObject) in [orGate, andGate, norGate, nandGate, xorGate, xnorGate]):
                if tempObject.getInput1() == None:
                    self.secondSelectedObject = tempObject
                    if type(self.firstSelectedObject) == constantOff:
                        self.secondSelectedObject.setInput1(self.firstSelectedObject.getOutput())
                        input1Flag = True
 
                    else:
                        self.secondSelectedObject.setInput1(self.firstSelectedObject.getOutput())
                        input1Flag = True
 
 
                elif tempObject.getInput2() == None:
                    self.secondSelectedObject = tempObject
                    if type(self.firstSelectedObject) == constantOff:
                        self.secondSelectedObject.setInput2(self.firstSelectedObject.getOutput())
                        input2Flag = True
 
                    else:
                        self.secondSelectedObject.setInput2(self.firstSelectedObject.getOutput())
                        input2Flag = True
 
                else:
                    self.firstSelectedObject = None
 
            elif (type(self.firstSelectedObject) in [constantOff, constantOn]) and (type(tempObject) == notGate):
                if tempObject.getInput() == None:
                    self.secondSelectedObject = tempObject
                    if type(self.firstSelectedObject) == constantOff:
                        self.secondSelectedObject.setInput(self.firstSelectedObject.getOutput())
                        
                    else:
                        self.secondSelectedObject.setInput(self.firstSelectedObject.getOutput())
 
 
                else:
                    self.firstSelectedObject = None
 
 
            elif type(self.firstSelectedObject) == notGate and type(tempObject) == notGate:
                if tempObject.getInput() == None:
                    self.secondSelectedObject = tempObject
                    self.secondSelectedObject.setInput(self.firstSelectedObject.getOutput())
 
                else:
                    self.firstSelectedObject = None
            
            elif type(self.firstSelectedObject) == notGate:
 
                if tempObject.getInput1() == None:
                    self.secondSelectedObject = tempObject
                    self.secondSelectedObject.setInput1(self.firstSelectedObject.getOutput())
                    input1Flag = True
                
                elif tempObject.getInput2() == None:
                    self.secondSelectedObject = tempObject
                    self.secondSelectedObject.setInput2(self.firstSelectedObject.getOutput())
                    input2Flag = True
 
                else:
                    self.firstSelectedObject = None
 
 
 
            elif (type(self.firstSelectedObject) in [orGate, andGate, norGate, nandGate, xorGate, xnorGate]) and (type(tempObject) == notGate):
                if tempObject.getInput() == None:
                    self.secondSelectedObject = tempObject
                    self.secondSelectedObject.setInput(self.firstSelectedObject.getOutput())
 
                    
 
                else:
                    self.firstSelectedObject = None
 
            
 
            elif (type(self.firstSelectedObject) in [orGate, andGate, norGate, nandGate, xorGate, xnorGate]) and (type(tempObject) in [orGate, andGate, norGate, nandGate, xorGate, xnorGate]):
                if tempObject.getInput1() == None:
                    self.secondSelectedObject = tempObject
                    self.secondSelectedObject.setInput1(self.firstSelectedObject.getOutput())
                    input1Flag = True
 
 
                elif tempObject.getInput2() == None:
                    self.secondSelectedObject = tempObject
                    self.secondSelectedObject.setInput2(self.firstSelectedObject.getOutput())
                    input2Flag = True
 
 
                else:
                    self.firstSelectedObject = None
                
 
            if self.firstSelectedObject != None and self.secondSelectedObject != None: # check for duplicates as well !!!!!!!
                if ([self.firstSelectedObject, self.secondSelectedObject] not in self.connectedGates) and ([self.secondSelectedObject, self.firstSelectedObject] not in self.connectedGates):
                    if input1Flag == True:
                        self.connectedGates.append([self.firstSelectedObject, self.secondSelectedObject, "input1"])
 
                    elif input2Flag == True:
                        self.connectedGates.append([self.firstSelectedObject, self.secondSelectedObject, "input2"])
                    
                    else:
                        self.connectedGates.append([self.firstSelectedObject, self.secondSelectedObject])
                    
                    
                    print("connected gates ", self.connectedGates)
 
 
                    self.updateConnections()
                    self.createLines()
 
 
            #and then
                self.firstSelectedObject = None
                self.secondSelectedObject= None
 
    def updateConnections(self):
        for i in self.connectedGates:
            try:
                if i[2] == "input1":
                    i[1].setInput1(i[0].getOutput())
                
                elif i[2] == "input2":
                    i[1].setInput2(i[0].getOutput())
 
            except:
                i[1].setInput(i[0].getOutput())
 
    def getConstantCounter(self):
        return str(self.constantCounter)
    
    def circuitExecution(self, operation):
        def postorder(root):
            if root is None:
                return
 
            # traverse left subtree
            postorder(root.leftChild)
 
            # traverse right subtree
            postorder(root.rightChild)
            
            x = root.data
            postorderOutput.append(x)
 
        def insert(root, newValue):
            if root is None:
                root = BinaryTreeNode(newValue)
 
                if (type(newValue[0]) == tuple) and ((type(newValue[1]) != tuple)):
                    root.leftChild = insert(root.leftChild, newValue[0])
                
                elif (type(newValue[0]) != tuple) and (type(newValue[1]) == tuple):
                    root.leftChild = insert(root.leftChild, newValue[1])
 
                elif (type(newValue[0]) == tuple) and (type(newValue[1]) == tuple):
                    root.leftChild = insert(root.leftChild, newValue[0])
                    root.rightChild = insert(root.rightChild, newValue[1])
 
                return root
            
        postorderOutput = [] # output of postorder
 
        inputOperation = operation
        #all adjustments to inital input made to this variable, knock on effect will be had
 
        root = insert(None, inputOperation) # make a confirm button to run these lines /// they initialise the tree
        postorder(root)
 
 
        
            
        opsToExecuteStack = Stack()
 
        for i in range(len(postorderOutput) - 1, -1, -1): # so order of items in stack is simplest at the top and most complex at the bottom
            opsToExecuteStack.push(postorderOutput[i])
 
        # EXECUTE OPS
        reusableResults = {} # save operation and results in pairs, swap if key(embedded operation) is found
 
        def executeOp(operation):
            if len(operation) == 3: # 2 inputs, 1 gate
                if ((operation[0]) in reusableResults) and ((operation[1]) in reusableResults):
                    result = operation[2](reusableResults[operation[0]], reusableResults[operation[1]])
                    reusableResults[operation] = result
                    answer = result
 
                elif (operation[0]) in reusableResults:
                    result = operation[2](reusableResults[operation[0]], operation[1])
                    reusableResults[operation] = result
                    answer = result
 
                elif (operation[1]) in reusableResults:
                    result = operation[2](operation[0], reusableResults[operation[1]])
                    reusableResults[operation] = result
                    answer = result
 
                else:
                    result = operation[2](operation[0], operation[1])
                    reusableResults[operation] = result
                    answer = result
 
            if len(operation) == 2: # 1 input, 1 gate
                if type(operation[0]) != tuple: # save simplest to dictionaries
                    result = operation[1](operation[0])
                    reusableResults[operation] = result
                    answer = result
                
                else:
                    #     #[[A,B, AND], NOT]]
                    if (type(operation[0]) == tuple):
                        result = operation[1](reusableResults[operation[0]])
                        reusableResults[operation] = result
                        answer = result
 
        def execution():
            for i in range(opsToExecuteStack.size, 0, -1):
                executeOp(opsToExecuteStack.popFromStack())
 
            answer = reusableResults.popitem()
            finalAnswer = "Output: " + str(answer[1])
            
            return finalAnswer
 
        finalAnswer = execution()
 
        return finalAnswer
 
    def formatCircuitOutput(self, output):
        return tuple(self.formatCircuitOutput(i) if isinstance(i, list) else i for i in output)
 
    def formatOutputForCircuitExecution(self, lst):
 
        def changeConstantsToValues(l):
            for n, i in enumerate(l):
                if type(i) is list:
                    l[n] = changeConstantsToValues(l[n])
                elif type(i) is str:
                    if i[:10] == "constantOn":
                        l[n] = 1
                    elif i[:11] == "constantOff":
                        l[n] = 0
            return l
 
 
        return self.formatCircuitOutput(changeConstantsToValues(lst))
    
    def getCircuitOutput(self):
        print("\nGET CIRCUIT OUTPUT SECTION")
        
        # if connected gates is empty throw error
        if len(self.connectedGates) == 0:
 
            self.newWindow = Toplevel(self.root)
            self.newWindow.geometry("270x30")
            self.newWindow.title("Invalid Circuit")
            self.ErrorLabel = Label(self.newWindow, text="No connections have been made")
            self.ErrorLabel.grid(row=0, column=0, padx=5, pady=5)
 
 
        else:
            outputCounter = 0
            for i in self.connectedGates:
                if type(i[1]) == lightbulb:
                    outputCounter = outputCounter + 1
                    
            
 
            if outputCounter == 1:
                for i in self.connectedGates:
                    if type(i[1]) == lightbulb:
                        output = i[0].getOutput() # original output im dealing with
                        lightbulbObject = i[1]
 
                for i in self.gatesAndIcons:
                    if i[0] == lightbulbObject:
                        lightbulbobjectlist = i
 
 
                # making a copy of the list
                temp = copy.deepcopy(output)
 
 
 
                # change the output icon if true or false
 
                print("before")
                if self.circuitExecution(self.formatOutputForCircuitExecution(temp)) == "Output: 1":
                    print("1")
                    
                    
 
                    x = lightbulbobjectlist.pop()
 
                    self.workspace.delete(x.image_obj)
                    del x
                    coords = lightbulbobjectlist[0].getInputCoords()
                    print(type(coords))
                    x = coords[0]
                    y = coords[1] - 41
                    lightbulbobjectlist.append(CreateCanvasObject(self.workspace, "lightbulb_changed - Copy.png", x, y, lightbulbobjectlist[0]))
 
                    print(self.gatesAndIcons)
 
                else:
                    x = lightbulbobjectlist.pop()
 
                    self.workspace.delete(x.image_obj)
                    del x
                    coords = lightbulbobjectlist[0].getInputCoords()
                    print(type(coords))
                    x = coords[0]
                    y = coords[1] - 41
                    lightbulbobjectlist.append(CreateCanvasObject(self.workspace, "lightbulb_default.png", x, y, lightbulbobjectlist[0]))
 
 
                print(self.circuitExecution(self.formatOutputForCircuitExecution(temp)))
 
 
                print("past")
 
                print("\npre formatted output", output)
 
                print("\npre formatted temp", temp)
 
 
                        
                print("\nformatted temp", self.formatOutputForCircuitExecution(temp)) # turns all the constantx and constanty into 1s and 0s
 
 
 
                print("\noriginal temp", temp)
 
                print("original output", output)
 
 
            elif outputCounter > 1:
                self.newWindow = Toplevel(self.root)
                self.newWindow.geometry("270x30")
                self.newWindow.title("Error")
                self.ErrorLabel = Label(self.newWindow, text="Too many outputs. Only one output is accepted.")
                self.ErrorLabel.grid(row=0, column=0, padx=5, pady=5)
 
                self.output = None
 
            else:
                self.newWindow = Toplevel(self.root)
                self.newWindow.geometry("270x30")
                self.newWindow.title("Error")
                self.ErrorLabel = Label(self.newWindow, text="No outputs detected.")
                self.ErrorLabel.grid(row=0, column=0, padx=5, pady=5)
 
                self.output = None
 
    def formatOutputForTruthTable(self):
            # if connected gates is empty throw error
            if len(self.connectedGates) == 0:
                #print("not happening son")
                self.newWindow = Toplevel(self.root)
                self.newWindow.geometry("270x30")
                self.newWindow.title("Invalid Circuit")
                self.ErrorLabel = Label(self.newWindow, text="No connections have been made")
                self.ErrorLabel.grid(row=0, column=0, padx=5, pady=5)
 
            else:
                if self.getNumOfInputs() in [2,3]:
                    print("\nTRUTH TABLE SECTION")
 
                    def findConstantInList(l, find, replaceWith):
                        for n, i in enumerate(l):
                            if i == find:
                                l[n] = replaceWith
                            elif type(i) is list:
                                l[n] = findConstantInList(l[n], find, replaceWith)
                                
                        return l
 
                    outputCounter = 0
                    for i in self.connectedGates:
                        if type(i[1]) == lightbulb:
                            outputCounter = outputCounter + 1
                            
                    if outputCounter == 1:
                        for i in self.connectedGates:
                            if type(i[1]) == lightbulb:
                                output = i[0].getOutput() # original output im dealing with
 
                    temp = copy.deepcopy(output)
                    print("old temp", temp)
 
                    letterCount = 64
                    for i in self.constantList:
                        print(i)
                        print(i.getOutput())
 
                        letterCount += 1
 
                        temp = findConstantInList(temp, i.getOutput(), chr(letterCount))
                        print(temp)
 
                    print("new temp", temp)
                    
 
                    truthInput = self.formatCircuitOutput(temp)
                    print("truth table input", truthInput)
 
 
                    self.getTruthTableOutput(truthInput)
 
                else:
                    self.newWindow = Toplevel(self.root)
                    self.newWindow.geometry("270x30")
                    self.newWindow.title("Lack of/Too many inputs")
                    self.ErrorLabel = Label(self.newWindow, text="Truth tables are limited to 2 or 3 inputs")
                    self.ErrorLabel.grid(row=0, column=0, padx=5, pady=5)
 
    def getTruthTableOutput(self, truthInput):
            print("truth table output section")
            print(self.getNumOfInputs())
            def postorderTruth(root):
                if root is None:
                    return
 
                # traverse left subtree
                postorderTruth(root.leftChild)
 
                # traverse right subtree
                postorderTruth(root.rightChild)
                
                x = root.data
                postorderOutputForTruthTable.append(x)
 
            def insert(root, newValue):
                if root is None:
                    root = BinaryTreeNode(newValue)
 
                    if (type(newValue[0]) == tuple) and ((type(newValue[1]) != tuple)):
                        root.leftChild = insert(root.leftChild, newValue[0])
                    
                    elif (type(newValue[0]) != tuple) and (type(newValue[1]) == tuple):
                        root.leftChild = insert(root.leftChild, newValue[1])
 
                    elif (type(newValue[0]) == tuple) and (type(newValue[1]) == tuple):
                        root.leftChild = insert(root.leftChild, newValue[0])
                        root.rightChild = insert(root.rightChild, newValue[1])
 
                    return root
 
            postorderOutputForTruthTable = []
 
            rootTruth = insert(None, truthInput)
            postorderTruth(rootTruth)
 
            truthTable = TruthTable(self.getNumOfInputs(), postorderOutputForTruthTable)
 
            table = truthTable.getTable()
            
 
            self.newWindow = Toplevel(self.root)
            self.newWindow.geometry("270x30")
            self.newWindow.title("Truth Table")
            self.ErrorLabel = Label(self.newWindow, text=(tabulate(table)), font=('Consolas', 12), anchor='w', justify=LEFT)
            self.ErrorLabel.grid(row=0, column=0, padx=5, pady=5)
        
    def formatOutputForBooleanExpression(self):
            # if connected gates is empty throw error
            if len(self.connectedGates) == 0:
                self.newWindow = Toplevel(self.root)
                self.newWindow.geometry("270x30")
                self.newWindow.title("Invalid Circuit")
                self.ErrorLabel = Label(self.newWindow, text="No connections have been made")
                self.ErrorLabel.grid(row=0, column=0, padx=5, pady=5)
 
            else:
                if self.getNumOfInputs() in [2,3]:
                    print("\nBOOLEAN SECTION")
 
                    def findConstantInList(l, find, replaceWith):
                        for n, i in enumerate(l):
                            if i == find:
                                l[n] = replaceWith
                            elif type(i) is list:
                                l[n] = findConstantInList(l[n], find, replaceWith)
                                
                        return l
 
                    outputCounter = 0
                    for i in self.connectedGates:
                        if type(i[1]) == lightbulb:
                            outputCounter = outputCounter + 1
                            
                    if outputCounter == 1:
                        for i in self.connectedGates:
                            if type(i[1]) == lightbulb:
                                output = i[0].getOutput() # original output im dealing with
 
                    temp = copy.deepcopy(output)
                    print("old temp", temp)
                    letterCount = 64
                    for i in self.constantList:
                        print(i)
                        print(i.getOutput())
 
                        letterCount += 1
 
                        temp = findConstantInList(temp, i.getOutput(), chr(letterCount))
                        print(temp)
 
                    print("new temp", temp)
                    
 
                    truthInput = self.formatCircuitOutput(temp)
                    print("truth table input", truthInput)
 
 
                    self.getBooleanExpression(truthInput)
 
                else:
                    self.newWindow = Toplevel(self.root)
                    self.newWindow.geometry("270x30")
                    self.newWindow.title("Lack of/Too many inputs")
                    self.ErrorLabel = Label(self.newWindow, text="Boolean expressions are limited to 2 or 3 inputs")
                    self.ErrorLabel.grid(row=0, column=0, padx=5, pady=5)
 
    def getBooleanExpression(self, truthInput):
        print("boolean output section")
 
        def postorderTruth(root):
            if root is None:
                return
 
            # traverse left subtree
            postorderTruth(root.leftChild)
 
            # traverse right subtree
            postorderTruth(root.rightChild)
            
            x = root.data
            postorderOutputForTruthTable.append(x)
 
        def insert(root, newValue):
            if root is None:
                root = BinaryTreeNode(newValue)
 
                if (type(newValue[0]) == tuple) and ((type(newValue[1]) != tuple)):
                    root.leftChild = insert(root.leftChild, newValue[0])
                
                elif (type(newValue[0]) != tuple) and (type(newValue[1]) == tuple):
                    root.leftChild = insert(root.leftChild, newValue[1])
 
                elif (type(newValue[0]) == tuple) and (type(newValue[1]) == tuple):
                    root.leftChild = insert(root.leftChild, newValue[0])
                    root.rightChild = insert(root.rightChild, newValue[1])
 
                return root
 
        postorderOutputForTruthTable = []
 
        rootTruth = insert(None, truthInput)
        postorderTruth(rootTruth)
 
        truthTable = TruthTable(self.getNumOfInputs(), postorderOutputForTruthTable)
 
        table = truthTable.getTable()
        boolean = (table[0][-1])
 
        self.newWindow = Toplevel(self.root)
        self.newWindow.geometry("270x30")
        self.newWindow.title("Boolean Expression")
        self.ErrorLabel = Label(self.newWindow, text=str(boolean))
        self.ErrorLabel.grid(row=0, column=0, padx=5, pady=5)
 
    def runWindow(self):
        return self.root.mainloop()
 
    def deleteObject(self, gate, image_obj):
        print("\nDELETE OBJECT SECTION")
 
        print("gate object to delete", gate)
        outputToDelete = gate.getOutput()
        print("output to delete", outputToDelete)
 
        def resetInput(l):
            if l == outputToDelete:
                l = None
            else:
                for n, i in enumerate(l):
                    if i == outputToDelete:
                        l[n] = None
                    elif type(i) is list:
                        l[n] = resetInput(l[n])
                    
                return l
                
        for i in self.connectedGates:
            resetInput(i[0].getOutput())
                
        for i in self.connectedGates:
            try:
 
                if i[2] == "input1":
                    i[1].setInput1(resetInput(i[0].getOutput()))
                    print("NBJBGSJGHSBGHLBGLHGBHJSGDSBGJHEGBLJRDGBJKLDHGBJKDBGHLKD")
                elif i[2] == "input2":
                    i[1].setInput2(resetInput(i[0].getOutput()))
                    
            except:
                i[1].setInput(resetInput(i[1].getInput()))
 
        for i in range(len(self.connectedGates)):
            if gate in self.connectedGates[i]:
                self.connectedGates.pop(i)
 
        
 
        #delete gate from gates and icons lsit
        for i in range(0, len(self.gatesAndIcons)):
            if self.gatesAndIcons[i][0] == gate:
                self.gatesAndIcons.pop(i)
                break
 
        # delete constants from constant list if applicable
        if type(gate) in [constantOff, constantOn]:
            for i in range(0, len(self.constantList)):
                if self.constantList[i] == gate:
                    self.constantList.pop(i)
 
        # delete canvas object and delete gate object
        
        self.workspace.delete(image_obj)
 
        print("deleted")
 
        print("\n", self.connectedGates)
        print("new connected gates")
        for i in self.connectedGates:
            try:
                if i[2] == "input1":
                    print("\noutput of first gate and input1 of gate = ", i[1].getInput1())
                    print("output of gate = ", i[1].getOutput())
 
                elif i[2] == "input2":
                    print("\noutput of second gate and input2 of gate = ", i[1].getInput2())
                    print("output of gate = ", i[1].getOutput())
            except:
                print("\noutput of first gate and input of gate = ", i[1].getInput())
                print("output of gate = ", i[1].getOutput())
 
        self.createLines()
 
    def createOrGate(self):
        orGateObject = orGate()
        orIconObject = CreateCanvasObject(self.workspace, "or.png", 865, 450, orGateObject)
 
        self.gatesAndIcons.append([orGateObject, orIconObject])
        self.constantCounter = self.constantCounter + 1
 
    def createAndGate(self):
        andGateObject = andGate()
        andIconObject = CreateCanvasObject(self.workspace, "and.png", 865, 450, andGateObject)
 
        self.gatesAndIcons.append([andGateObject, andIconObject])
        self.constantCounter = self.constantCounter + 1
 
    def createNotGate(self):
        notGateObject = notGate()
        notIconObject = CreateCanvasObject(self.workspace, "not.png", 865, 450, notGateObject)
 
        self.gatesAndIcons.append([notGateObject, notIconObject])
        self.constantCounter = self.constantCounter + 1
 
    def createNorGate(self):
        norGateObject = norGate()
        norIconObject = CreateCanvasObject(self.workspace, "nor.png", 865, 450, norGateObject)
 
        self.gatesAndIcons.append([norGateObject, norIconObject])
        self.constantCounter = self.constantCounter + 1
 
    def createNandGate(self):
        nandGateObject = nandGate()
        nandIconObject = CreateCanvasObject(self.workspace, "nand.png", 865, 450, nandGateObject)
 
        self.gatesAndIcons.append([nandGateObject, nandIconObject.getIcon(), nandIconObject])
        self.constantCounter = self.constantCounter + 1
 
    def createXorGate(self):
        xorGateObject = xorGate()
        xorIconObject = CreateCanvasObject(self.workspace, "xor.png", 865, 450, xorGateObject)
 
        self.gatesAndIcons.append([xorGateObject, xorIconObject])
        self.constantCounter = self.constantCounter + 1
 
    def createXnorGate(self):
        xnorGateObject = xnorGate()
        xnorIconObject = CreateCanvasObject(self.workspace, "xnor.png", 865, 450, xnorGateObject)
 
        self.gatesAndIcons.append([xnorGateObject, xnorIconObject])
        self.constantCounter = self.constantCounter + 1
 
    def createConstantOn(self): # do first
        constantOnObject = constantOn()
        constantOnIconObject = CreateCanvasObject(self.workspace, "constant_on.png", 865, 450, constantOnObject)
        self.gatesAndIcons.append([constantOnObject, constantOnIconObject])
        self.constantList.append(constantOnObject)
        self.constantCounter = self.constantCounter + 1
 
    def createConstantOff(self):
        constantOffObject = constantOff()
        constantOffIconObject = CreateCanvasObject(self.workspace, "constant_off.png", 865, 450, constantOffObject)
        self.gatesAndIcons.append([constantOffObject, constantOffIconObject])
        self.constantList.append(constantOffObject)
        self.constantCounter = self.constantCounter + 1
 
    def createLightbulb(self):
        lightbulbObject = lightbulb()
        outputIconObject = CreateCanvasObject(self.workspace, "lightbulb_default.png", 865, 450, lightbulbObject)
        self.gatesAndIcons.append([lightbulbObject, outputIconObject])
        self.constantCounter = self.constantCounter + 1
 
 
class CreateCanvasObject(object):
    def __init__(self, canvas, image_name, xpos, ypos, gateObject): #  the canvas, picture and its startiing co-ordinates are passed through as parameters
        self.canvas = Window.workspace # self explanatory
        self.image_name = image_name # self explanatory
        self.xpos, self.ypos = xpos, ypos # self explanatory
        self.image_path = Window.IMAGE_PATH
 
        self.gateObject = gateObject
 
        self.tk_image = PhotoImage(
            file="{}{}".format(self.image_path, image_name)) # makes the icon a tkinter PhotoImage, PhotoImage takes the file path "Project programs/gate pictures/" and name "or.png"
        self.image_obj= self.canvas.create_image(xpos, ypos, anchor=CENTER, image=self.tk_image) # creates the image on the canvas and places it at the co-ords
        
 
        self.canvas.tag_bind(self.image_obj, '<Button1-Motion>', self.move) # binds mouse action, when clicked and dragged. passes the mouse action as an event
        self.canvas.tag_bind(self.image_obj, '<ButtonRelease-1>', self.release) # binds mouse action to release
 
        self.canvas.tag_bind(self.image_obj, '<Double-Button-1>', self.makeSelected)
 
        self.canvas.tag_bind(self.image_obj, '<Button-2>', self.delete)
 
        self.move_flag = False
 
    def move(self, event): # <Button1-Motion> passed through as event
        if self.move_flag: # starts as false, the picture is moving
            new_xpos, new_ypos = event.x, event.y # takes the picture to where the event ends, so where you moved to last
             
            self.canvas.move(self.image_obj,
                new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos) # says to canvas to move the picture the difference between the end and starting points (end co-ords - start co-ords)
             
            ####### change i/o port positions here
 
            # all but NOT
            
            if type(self.gateObject) == notGate:
                self.gateObject.inputCoords[0] = (new_xpos-self.mouse_xpos) + self.gateObject.inputCoords[0]
                self.gateObject.inputCoords[1] = (new_ypos-self.mouse_ypos) + self.gateObject.inputCoords[1] 
                self.gateObject.outputCoords[0] = (new_xpos-self.mouse_xpos) + self.gateObject.outputCoords[0] 
                self.gateObject.outputCoords[1] = (new_ypos-self.mouse_ypos) + self.gateObject.outputCoords[1] 
                Window.createLines()
                
 
 
            elif type(self.gateObject) == lightbulb:
                self.gateObject.inputCoords[0] = (new_xpos-self.mouse_xpos) + self.gateObject.inputCoords[0]
                self.gateObject.inputCoords[1] = (new_ypos-self.mouse_ypos) + self.gateObject.inputCoords[1] 
                Window.createLines()
 
            
            elif (type(self.gateObject) == constantOff) or (type(self.gateObject) == constantOn):
                self.gateObject.outputCoords[0] = (new_xpos-self.mouse_xpos) + self.gateObject.outputCoords[0]
                self.gateObject.outputCoords[1] = (new_ypos-self.mouse_ypos) + self.gateObject.outputCoords[1]
                Window.createLines()
 
            else:
                self.gateObject.input1Coords[0] = (new_xpos-self.mouse_xpos) + self.gateObject.input1Coords[0] 
                self.gateObject.input1Coords[1] = (new_ypos-self.mouse_ypos) + self.gateObject.input1Coords[1] 
                self.gateObject.input2Coords[0] = (new_xpos-self.mouse_xpos) + self.gateObject.input2Coords[0] 
                self.gateObject.input2Coords[1] = (new_ypos-self.mouse_ypos) + self.gateObject.input2Coords[1] 
                self.gateObject.outputCoords[0] = (new_xpos-self.mouse_xpos) + self.gateObject.outputCoords[0] 
                self.gateObject.outputCoords[1] = (new_ypos-self.mouse_ypos) + self.gateObject.outputCoords[1] 
                Window.createLines()
                
 
 
            self.mouse_xpos = new_xpos # set the events final co-ords as the new starting co-ords
            self.mouse_ypos = new_ypos
        else: # if self.move_flag is False so the picture is not moving
            self.move_flag = True # then we set it to true, so the move flag is set to true when click on the picture for the first time
            self.canvas.tag_raise(self.image_obj) # moves the current picture to the top layer, so if you overlay one picture on top of the other you wont grab the one 'underneath' (which is the one that was already there beforehand)
            self.mouse_xpos = event.x # # set the events final co-ords as the new starting co-ords
            self.mouse_ypos = event.y # mouse x pos and y pos are attributes and thus can be called for the change of the line
            #print(self.mouse_xpos, self.mouse_ypos)
            
    def release(self, event):
        self.move_flag = False # this says that when released, the picture is not moving
 
    def makeSelected(self, event):
        Window.setSelectedIcon(self.gateObject)
 
    def getIcon(self):
        return self.tk_image
    
    def delete(self, event):
        Window.deleteObject(self.gateObject, self.image_obj)
 
 
 
class gate:
    def __init__(self):
        self._input1 = None
        self._input2 = None
        
 
        self.input1Coords = [816, 433]
        self.input2Coords = [816, 466]
        self.outputCoords = [914, 450]
 
    def setInput1(self, input):
        self._input1 = input
 
    def setInput2(self, input):
        self._input2 = input
 
    def getInput1(self):
        return self._input1
    
    def getInput2(self):
        return self._input2   
    
    def getInput1Coords(self):
        return self.input1Coords
    
    def getInput2Coords(self): 
        return self.input2Coords
    
    def getOutputCoords(self):
        return self.outputCoords
 
 
class orGate(gate):
    def __init__(self):
        super().__init__()
 
 
    def getOutput(self):
        return [self._input1, self._input2, OR]
 
class andGate(gate):
    def __init__(self):
        super().__init__()
 
    def getOutput(self):
        return [self._input1, self._input2, AND]
 
class notGate:
    def __init__(self):
        self._input = None
 
        self.inputCoords = [816, 450]
        self.outputCoords = [914, 450]
 
    def setInput(self, input):
        self._input = input
 
    def getInput(self):
        return self._input
 
    def getOutput(self):
        return [self._input, NOT]
    
    def getInputCoords(self):
        return self.inputCoords
    
    def getOutputCoords(self):
        return self.outputCoords
    
class norGate(gate):
    def __init__(self):
        super().__init__()
 
    def getOutput(self):
        return [self._input1, self._input2, NOR]
 
class nandGate(gate):
    def __init__(self):
        super().__init__()
 
    def getOutput(self):
        return [self._input1, self._input2, NAND]
 
class xorGate(gate):
    def __init__(self):
        super().__init__()
 
    def getOutput(self):
        return [self._input1, self._input2, XOR]
 
class xnorGate(gate):
    def __init__(self):
        super().__init__()
 
    def getOutput(self):
        return [self._input1, self._input2, XNOR]
 
 
class constant:
    def __init__(self):
        self.outputCoords = [895, 450]
 
    def getOutput(self):
        return self.output
    
    def getOutputCoords(self):
        return self.outputCoords
 
class constantOn(constant):
    def __init__(self):
        super().__init__()
        self.output = str("constantOn" + Window.getConstantCounter())
 
class constantOff(constant):
    def __init__(self):
        super().__init__()
        self.output = str("constantOff" + Window.getConstantCounter())
 
 
class lightbulb:
    def __init__(self):
        self.input = None
 
        self.inputCoords = [865, 491]
 
    def setInput(self, input):
       self.input = input
 
    def getInput(self):
        return self.input
 
    def getOutput(self):
        return self.input
 
    def getInputCoords(self):
        return self.inputCoords
 
# TREE
class BinaryTreeNode:
    def __init__(self, data):
        self.data = data
        self.leftChild = None
        self.rightChild = None
 
class Stack:
    def __init__(self):
        self.stack = []
        self.size = 0
 
    def isEmpty(self):
        if self.size == 0:
            return True
        else:
            return False
 
    def push(self, newItem):
        self.stack.append(newItem)
        self.size += 1
 
    def popFromStack(self):
        if self.isEmpty() == False:
            x = self.stack.pop()
            self.size += -1
            return x
 
        else:
            return None
 
    def peek(self):
        if self.isEmpty() == False:
            return self.stack[-1] 
        else:
            return None
 
class TruthTable:
    def __init__(self, numOfInputs, postorderOutputForTruthTable):
        self.numOfInputs = numOfInputs
        self.postorderOutputForTruthTable = postorderOutputForTruthTable
 
        self.truthTable = []
        self.formatDict = {}
 
        self.initialiseList()
        self.truthResults()
 
        
 
    def initialiseList(self):
        # x-axis = number of inputs + num of gates/operations e.g NOT A, A OR B etc.
        # y-axis = 2^num of the inputs   (+ labels of what the operation? e.g AB etc.)
 
        for i in range(2**self.numOfInputs + 1): # for now + 1 to show labels, this should be resolved in gui perhaps or just delete top list in truth table for truth table to boolean algebra conversion
            emptyList = []
            for j in range(self.numOfInputs + (len(self.postorderOutputForTruthTable))):
                emptyList.append(None)
 
            self.truthTable.append(emptyList)
 
        self.truthTable[0][0] = 'A'
        if self.numOfInputs == 3:
            for i in range(len(self.postorderOutputForTruthTable)):
                label = self.formatOperationsforTruthTable(self.postorderOutputForTruthTable[i])
                self.truthTable[0][i+3] = label
 
            self.truthTable[0][1] = 'B'
            self.truthTable[0][2] = 'C'
 
            # column A
            for i in range(1, 5):
                self.truthTable[i][0] = 0
 
            for i in range(5, 9):
                self.truthTable[i][0] = 1
 
            # column B
            for i in range(1,3):
                self.truthTable[i][1] = 0
 
            for i in range(3,5):
                self.truthTable[i][1] = 1
 
            for i in range(5,7):
                self.truthTable[i][1] = 0
 
            for i in range(7,9):
                self.truthTable[i][1] = 1
 
            #column C
            zeroFlag = False
            for i in range(1,9):
                if zeroFlag == False:
                    self.truthTable[i][2] = 0
                    zeroFlag = True
                else:
                    self.truthTable[i][2] = 1
                    zeroFlag = False
 
        else:
            for i in range(len(self.postorderOutputForTruthTable)):
                label = self.formatOperationsforTruthTable(self.postorderOutputForTruthTable[i])
                self.truthTable[0][i+2] = label
            
            self.truthTable[0][1] = 'B'
            # column A
            for i in range(1, 3):
                self.truthTable[i][0] = 0
 
            for i in range(3, 5):
                self.truthTable[i][0] = 1
 
            # column B
            zeroFlag = False
            for i in range(1,5):
                if zeroFlag == False:
                    self.truthTable[i][1] = 0
                    zeroFlag = True
                else:
                    self.truthTable[i][1] = 1
                    zeroFlag = False
 
    def checkDict(self, operation):
        if len(operation) == 3:
            if ((operation[0]) in self.formatDict) and ((operation[1]) in self.formatDict):
                return self.formatDict[operation[0]], self.formatDict[operation[1]]
                
            elif (operation[0]) in self.formatDict:
                return self.formatDict[operation[0]], operation[1]
 
            elif (operation[1]) in self.formatDict:
                return operation[0], self.formatDict[operation[1]]
                
            else:
                return None, None
 
        else:
            if (operation[0]) in self.formatDict:
                return self.formatDict[operation[0]]
            
            else:
                return None
 
    def formatOperationsforTruthTable(self, operation):
        if len(operation) == 3:
            if operation[2] == AND:
                dictReturn1, dictReturn2 = self.checkDict(operation)
                if dictReturn1 != None:
                    formattedOutput = '(' + str(dictReturn1) + '•' + str(dictReturn2) + ')'
                    self.formatDict[operation] = formattedOutput
                    return formattedOutput
                    
                else:
                    formattedOutput = '(' + str(operation[0]) + '•' + str(operation[1]) + ')'
                    self.formatDict[operation] = formattedOutput
                    return formattedOutput
 
            elif operation[2] == OR:
                dictReturn1, dictReturn2 = self.checkDict(operation)
                if dictReturn1 != None:
                    formattedOutput = '(' + str(dictReturn1) + '+' + str(dictReturn2) + ')'
                    self.formatDict[operation] = formattedOutput
                    return formattedOutput
                    
                else:
                    formattedOutput = '(' + str(operation[0]) + '+' + str(operation[1]) + ')'
                    self.formatDict[operation] = formattedOutput
                    return formattedOutput
 
            elif operation[2] == XOR:
                dictReturn1, dictReturn2 = self.checkDict(operation)
                if dictReturn1 != None:
                    formattedOutput = '(' + str(dictReturn1) + '⊕ ' + str(dictReturn2) + ')'
                    self.formatDict[operation] = formattedOutput
                    return formattedOutput
                    
                else:
                    formattedOutput = '(' + str(operation[0]) + '⊕ ' + str(operation[1]) + ')'
                    self.formatDict[operation] = formattedOutput
                    return formattedOutput
 
            elif operation[2] == NOR:
                dictReturn1, dictReturn2 = self.checkDict(operation)
                if dictReturn1 != None:
                    formattedOutput = '(' + 'NOT' + '(' + str(dictReturn1) + '+' + str(dictReturn2) + ')' + ')'
                    self.formatDict[operation] = formattedOutput
                    return formattedOutput
                    
                else: # (NOT(A+B))
                    formattedOutput = '(' + 'NOT' + '(' + str(operation[0]) + '+' + str(operation[1]) + ')' + ')'
                    self.formatDict[operation] = formattedOutput
                    return formattedOutput
            
            elif operation[2] == NAND:
                dictReturn1, dictReturn2 = self.checkDict(operation)
                if dictReturn1 != None:
                    formattedOutput = '(' + 'NOT' + '(' + str(dictReturn1) + '•' + str(dictReturn2) + ')' + ')'
                    self.formatDict[operation] = formattedOutput
                    return formattedOutput
                    
                else:
                    formattedOutput = '(' + 'NOT' + '(' + str(operation[0]) + '•' + str(operation[1]) + ')' + ')'
                    self.formatDict[operation] = formattedOutput
                    return formattedOutput
 
        else:
            dictReturn = self.checkDict(operation)
            if dictReturn != None:
                formattedOutput = '(' + 'NOT' + '(' + str(dictReturn) + ')' + ')'
                self.formatDict[operation] = formattedOutput
                return formattedOutput
                    
            else:
                formattedOutput = '(' + 'NOT' + '(' + str(operation[0]) + ')' + ')'
                self.formatDict[operation] = formattedOutput
                return formattedOutput
 
    def truthResults(self):
        for i in range(len(self.postorderOutputForTruthTable)):
            if self.numOfInputs == 3: # A, B, C
                for j in range(1, len(self.truthTable)):
                    if len(self.postorderOutputForTruthTable[i]) == 3: # 2 inputs, 1 gate
 
                        if ((self.postorderOutputForTruthTable[i])[0] == 'A') and ((self.postorderOutputForTruthTable[i])[1] == 'B'):
                            Aindex = self.truthTable[0].index('A')
                            Bindex = self.truthTable[0].index('B')
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][Aindex], self.truthTable[j][Bindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'A') and ((self.postorderOutputForTruthTable[i])[1] == 'C'):
                            Aindex = self.truthTable[0].index('A')
                            Cindex = self.truthTable[0].index('C')
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][Aindex], self.truthTable[j][Cindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'B') and ((self.postorderOutputForTruthTable[i])[1] == 'A'):
                            Bindex = self.truthTable[0].index('B')
                            Aindex = self.truthTable[0].index('A')
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][Bindex], self.truthTable[j][Aindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'B') and ((self.postorderOutputForTruthTable[i])[1] == 'C'):
                            Bindex = self.truthTable[0].index('B')
                            Cindex = self.truthTable[0].index('C')
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][Bindex], self.truthTable[j][Cindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'C') and ((self.postorderOutputForTruthTable[i])[1] == 'A'):
                            Cindex = self.truthTable[0].index('C')
                            Aindex = self.truthTable[0].index('A')
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][Cindex], self.truthTable[j][Aindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'C') and ((self.postorderOutputForTruthTable[i])[1] == 'B'):
                            Cindex = self.truthTable[0].index('C')
                            Bindex = self.truthTable[0].index('B')
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][Cindex], self.truthTable[j][Bindex])
 
                        elif (type((self.postorderOutputForTruthTable[i])[0]) == tuple) and (type((self.postorderOutputForTruthTable[i])[1]) == tuple):
                            leftSideIndex = self.truthTable[0].index(self.formatOperationsforTruthTable((self.postorderOutputForTruthTable[i])[0]))
                            rightSideIndex = self.truthTable[0].index(self.formatOperationsforTruthTable((self.postorderOutputForTruthTable[i])[1]))
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][leftSideIndex], self.truthTable[j][rightSideIndex])
 
                        elif type((self.postorderOutputForTruthTable[i])[0]) == tuple:
                            leftSideIndex = self.truthTable[0].index(self.formatOperationsforTruthTable((self.postorderOutputForTruthTable[i])[0]))
                            rightSideIndex = self.truthTable[0].index(((self.postorderOutputForTruthTable[i])[1]))
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][leftSideIndex], self.truthTable[j][rightSideIndex])
 
                        elif type((self.postorderOutputForTruthTable[i])[1]) == tuple:
                            leftSideIndex = self.truthTable[0].index((self.postorderOutputForTruthTable[i])[0])
                            rightSideIndex = self.truthTable[0].index(self.formatOperationsforTruthTable((self.postorderOutputForTruthTable[i])[1]))
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][(self.postorderOutputForTruthTable[i])[1]], self.truthTable[j][rightSideIndex])
 
                    else: # 1 input, 1 gate
                        if ((self.postorderOutputForTruthTable[i])[0] == 'A'):
                            Aindex = self.truthTable[0].index('A')
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[1])(self.truthTable[j][Aindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'B'):
                            Bindex = self.truthTable[0].index('B')
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[1])(self.truthTable[j][Bindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'C'):
                            Cindex = self.truthTable[0].index('C')
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[1])(self.truthTable[j][Cindex])
 
                        elif (type((self.postorderOutputForTruthTable[i])[0]) == tuple):
                            leftSideIndex = self.truthTable[0].index(self.formatOperationsforTruthTable((self.postorderOutputForTruthTable[i])[0]))
                            self.truthTable[j][i+3] = ((self.postorderOutputForTruthTable[i])[1])(self.truthTable[j][leftSideIndex])
 
            else: #A, B
                for j in range(1, len(self.truthTable)):
                    if len(self.postorderOutputForTruthTable[i]) == 3: # 2 inputs, 1 gate
 
                        if ((self.postorderOutputForTruthTable[i])[0] == 'A') and ((self.postorderOutputForTruthTable[i])[1] == 'B'):
                            Aindex = self.truthTable[0].index('A')
                            Bindex = self.truthTable[0].index('B')
                            self.truthTable[j][i+2] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][Aindex], self.truthTable[j][Bindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'A') and ((self.postorderOutputForTruthTable[i])[1] == 'C'):
                            Aindex = self.truthTable[0].index('A')
                            Cindex = self.truthTable[0].index('C')
                            self.truthTable[j][i+2] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][Aindex], self.truthTable[j][Cindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'B') and ((self.postorderOutputForTruthTable[i])[1] == 'A'):
                            Bindex = self.truthTable[0].index('B')
                            Aindex = self.truthTable[0].index('A')
                            self.truthTable[j][i+2] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][Bindex], self.truthTable[j][Aindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'B') and ((self.postorderOutputForTruthTable[i])[1] == 'C'):
                            Bindex = self.truthTable[0].index('B')
                            Cindex = self.truthTable[0].index('C')
                            self.truthTable[j][i+2] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][Bindex], self.truthTable[j][Cindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'C') and ((self.postorderOutputForTruthTable[i])[1] == 'A'):
                            Cindex = self.truthTable[0].index('C')
                            Aindex = self.truthTable[0].index('A')
                            self.truthTable[j][i+2] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][Cindex], self.truthTable[j][Aindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'C') and ((self.postorderOutputForTruthTable[i])[1] == 'B'):
                            Cindex = self.truthTable[0].index('C')
                            Bindex = self.truthTable[0].index('B')
                            self.truthTable[j][i+2] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][Cindex], self.truthTable[j][Bindex])
 
                        elif (type((self.postorderOutputForTruthTable[i])[0]) == tuple) and (type((self.postorderOutputForTruthTable[i])[1]) == tuple):
                            leftSideIndex = self.truthTable[0].index(self.formatOperationsforTruthTable((self.postorderOutputForTruthTable[i])[0]))
                            rightSideIndex = self.truthTable[0].index(self.formatOperationsforTruthTable((self.postorderOutputForTruthTable[i])[1]))
 
                            self.truthTable[j][i+2] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][leftSideIndex], self.truthTable[j][rightSideIndex])
 
                        elif type((self.postorderOutputForTruthTable[i])[0]) == tuple:
                            leftSideIndex = self.truthTable[0].index(self.formatOperationsforTruthTable((self.postorderOutputForTruthTable[i])[0]))
                            rightSideIndex = self.truthTable[0].index(((self.postorderOutputForTruthTable[i])[1]))
                            self.truthTable[j][i+2] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][leftSideIndex], self.truthTable[j][rightSideIndex])
 
                        elif type((self.postorderOutputForTruthTable[i])[1]) == tuple:
                            leftSideIndex = self.truthTable[0].index((self.postorderOutputForTruthTable[i])[0])
                            rightSideIndex = self.truthTable[0].index(self.formatOperationsforTruthTable((self.postorderOutputForTruthTable[i])[1]))
                            self.truthTable[j][i+2] = ((self.postorderOutputForTruthTable[i])[2])(self.truthTable[j][(self.postorderOutputForTruthTable[i])[1]], self.truthTable[j][rightSideIndex])
 
                    else: # 1 input, 1 gate
                        if ((self.postorderOutputForTruthTable[i])[0] == 'A'):
                            Aindex = self.truthTable[0].index('A')
                            self.truthTable[j][i+2] = ((self.postorderOutputForTruthTable[i])[1])(self.truthTable[j][Aindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'B'):
                            Bindex = self.truthTable[0].index('B')
                            self.truthTable[j][i+2] = ((self.postorderOutputForTruthTable[i])[1])(self.truthTable[j][Bindex])
 
                        elif ((self.postorderOutputForTruthTable[i])[0] == 'C'):
                            Cindex = self.truthTable[0].index('C')
                            self.truthTable[j][i+2] = ((self.postorderOutputForTruthTable[i])[1])(self.truthTable[j][Cindex])
 
    def getTable(self):
        return self.truthTable
 
 
 
 
Window = Window()
Window.runWindow()



