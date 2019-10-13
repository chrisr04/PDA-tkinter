class State:

    def __init__(self, id, name, accepted):
        self.id = id
        self.name = name
        self.transitions = {}
        self.accepted = accepted

    def __str__(self):
        return "{0}{1}".format(self.name,self.id)

    def addTransition(self,way,id):
        self.transitions[way] = id

    def deleteTransition(self,way):
        del self.transitions[way]
    