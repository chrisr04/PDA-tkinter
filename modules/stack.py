class Stack:

    def __init__(self):
        self.__memory=[]

    def __str__(self):
        return "{0}".format(self.__memory)

    def push(self,data):
        self.__memory.append(data)

    def pop(self):
        self.__memory.pop()

    def getTop(self):
        return self.__memory[-1]