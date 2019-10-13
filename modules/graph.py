import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

class Graph:

    def __init__(self, transitions,accepted):
        
        self.G = None
        self.transitions = transitions
        self.accepted = accepted

    def initGraph(self,label):

        self.G=nx.MultiDiGraph()

        self.G.graph['edge'] = {'arrowsize': '0.6', 'overlap':False,'color':'black'}
        self.G.graph['graph'] = {'scale': '3', 'rankdir':'LR', 'label':label}
        self.G.graph['node']= {'shape':'circle', 'color':'black'}
        
        for edge in self.transitions:
            self.G.add_edge(edge['from'], edge['to'], label=edge['with'])

        for i in self.accepted:
            n=self.G.node[i]
            n['shape'] ='doublecircle'

        self.A = to_agraph(self.G) 
        self.A.layout('dot')                                                          
        self.A.draw('pda/pda.png')

    def changeState(self,i,a):
        
        a = "q"+str(a)
        i = "q"+str(i)
        self.G.node[a]['color'] = 'black'
        self.G.node[i]['color'] = 'green'

        for i in self.accepted:
            n=self.G.node[i]
            n['shape'] ='doublecircle'

        self.A = to_agraph(self.G) 
        self.A.layout('dot')                                                           
        self.A.draw('pda/pda.png')

    


