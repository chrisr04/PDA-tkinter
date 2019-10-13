class PDA:

    def __init__(self,states):
        self.states = states
        self.currentState=0

    def addState(self,state):
        self.states.append(state)

    def getCurrentState(self):
        for s in self.states:
            if s.id == self.currentState:
                return s

    def nexState(self,id):
        self.currentState = id

    def verifyAcceptation(self):
        return self.states[self.currentState].accepted

    def verifyOverlapping(self):
        overlapping = []
        label = ""
        for s in self.states:
            for key,value in s.transitions.items():
                if s.id == 0:
                    label="a-z, λ ⟶ a-z"
                else:
                   label="a-z, a-z ⟶ λ" 
            if label != "":
                overlapping.append({'label':label,'id':s.id})
                label = ""
        return overlapping



    