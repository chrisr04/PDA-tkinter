import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

class Graph:

    def __init__(self, transitions,accepted):
        
        self.G = None
        self.transitions = transitions
        self.accepted = accepted

    def initGraph(self,label):

        self.G=nx.MultiDiGraph()

        self.G.graph['edge'] = {'arrowsize': '0.8', 'overlap':False, 'color':'black'}
        self.G.graph['graph'] = {'scale': '3', 'rankdir':'LR', 'label':str("\t\t\t"+label), 'bgcolor':'#e1e5ed','fontname':'verdana','fontsize':12}
        self.G.graph['node']= {'shape':'circle', 'color':'#3f9de0', 'style':'filled'}
        
        self.G.add_edge("s","q0",label="\t\t")
        for edge in self.transitions:
            self.G.add_edge(edge['from'], edge['to'], label=edge['with'])
        self.G.node["s"]['style']="invis"
        for i in self.accepted:
            n=self.G.node[i]
            n['shape'] ='doublecircle'
            # n['fillcolor'] = 'green'

        self.A = to_agraph(self.G) 
        self.A.layout('dot')                                                          
        self.A.draw('img/pda/pda.png')

    def changeState(self,i,a):
        
        self.G.node[i[0]]['color'] = '#3f9de0'
        self.G.node[i[1]]['color'] = 'green'

        self.G[a[0]][a[1]][0]['color'] = 'black'
        self.G[i[0]][i[1]][0]['color'] = 'green'

        for j in self.accepted:
            n=self.G.node[j]
            n['shape'] ='doublecircle'

        self.A = to_agraph(self.G) 
        self.A.layout('dot')                                                           
        self.A.draw('img/pda/pda.png')

    


