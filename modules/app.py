import requests, json, copy
from tkinter import *
from tkinter import messagebox
from .widgets import ScrolledFrame, PDAImage
from .language import Language
from .state import State
from .pda import PDA
from .stack import Stack
from .tree import ExpressionTree
from .graph import Graph
from .audio import Audio

class App:

    def __init__(self):

        self.gui = Tk()
        self.gui.title("Pushdown Automaton")
        self.gui.geometry("510x620")
        self.gui.resizable(False,False)
        self.icon = Image("photo", file="logo.png")
        self.gui.tk.call('wm','iconphoto',self.gui._w, self.icon)
        self.audio = Audio()
        self.txtStack = []
        self.G = None
        self.stack = None
        self.evenPDA = None
        self.oddPDA = None
        self.transitions = []
        self.states = []
        self.language = Language("{λ,a,b,c,d,e,f,g,h,i,j,k,l,m,n,ñ,o,p,q,r,s,t,u,v,w,x,y,z}")
        self.currentRegex = StringVar()
        self.word = StringVar()

        self.panel = Frame(self.gui, bg="#e1e5ed")
        self.panel.pack(fill="both", expand="True")

        self.lblPDA = Label(self.panel, bg="#e1e5ed", text="Pushdown Automaton", font=('Verdana',18,'bold'))
        self.lblPDA.grid(row = 0,column=0, columnspan=5, pady=10)

        self.lblWord = Label(self.panel, bg="#e1e5ed",text="Word:", font=('Verdana',13,'bold'))
        self.lblWord.grid(row = 1, column=0, pady=10)
        self.txtWord=Entry(self.panel, textvariable = self.word, width="16",font=('Verdana',13))
        self.txtWord.grid(row=1, column=1, pady=10, padx=0)
        self.txtWord.config(disabledbackground="black", disabledforeground="#03f943", justify="left",highlightbackground="#000000",highlightthickness=1, bd=0)
        self.btnVerifyFast=Button(self.panel, bg="#1c93e8", fg="#ffffff",relief='flat', text="Fast", font=('Verdana',10,'bold'), command=lambda:self.runPDA(True))
        self.btnVerifyFast.grid(row=1, column=2)
        self.btnVerifyLow=Button(self.panel, bg="#1c93e8", fg="#ffffff",relief='flat',text="Slow", font=('Verdana',10,'bold'), command=lambda:self.runPDA(False))
        self.btnVerifyLow.grid(row=1, column=3)
        icon = PhotoImage(file ="img/microphone.png")
        self.btnSpeech=Button(self.panel, bg="#1c93e8", relief='flat',text="",width="30",height="25", image=icon, font=('Verdana',10), command=lambda:self.runSpeech())
        self.btnSpeech.grid(row=1, column=4)
        
        background = PhotoImage(file="img/background.png")
        self.sImage = PDAImage(self.panel, image = background, width=465, height=137, bg="#e1e5ed")
        self.sImage.grid(row=2, column=0,columnspan=5, padx= 20)
        self.createPDA()
        self.showPDA("odd")

        self.lblStack = Label(self.panel, bg="#e1e5ed", text="Stack", font=('Verdana',18,'bold'))
        self.lblStack.grid(row = 3,column=0, columnspan=5, pady=10)

        self.panelStack = ScrolledFrame(self.panel)
        self.panelStack.grid(row = 4,column=0, columnspan=5, pady=10)

        # for i in range(0):
        #     element = Entry(self.panelStack.inner, width=7, state='disabled',font=('Verdana',12))
        #     element.grid(row = i, column=0, columnspan=5)
        #     element.config(disabledbackground="white", disabledforeground="#000000", justify="center",highlightbackground="#000000",highlightthickness=1, bd=1)
        #     self.txtStack.append(element)

        self.lblResult = Label(self.panel, bg="#e1e5ed", text="", font=('Verdana',11,'bold'))
        self.lblReader = Label(self.panel, bg="#e1e5ed", text="", font=('Verdana',11,'bold'))

        mainloop()

    def createPDA(self):

        # Create the states
        state1 = State(0,"q",False)
        state2 = State(1,"q",False)
        state3 = State(2,"q",True)
        state4 = State(0,"q",False)

        # Add the transitions
        for l in "abcdefghijklmnñopqrstuvwxyz":
            state1.addTransition(l,0)
            state2.addTransition(l,1)

        state1.addTransition("λ, λ ⟶ λ",1)
        state2.addTransition("λ, # ⟶ λ",2)

        self.evenPDA = PDA([copy.copy(state1),state2,state3])
        state4.transitions = state1.transitions.copy()
        state4.deleteTransition("λ, λ ⟶ λ")
        state4.addTransition("|, λ ⟶ λ",1)
        self.oddPDA = PDA([state4,state2,state3])

    def createGraph(self,pda,title):
        dGraphTr = []
        accepted = []
        for s in pda.states:
            if s.accepted:
                accepted.append("q"+str(s.id))
            for key,value in s.transitions.items():
                if s.id != value:
                    dGraphTr.append({'from':str("q"+str(s.id)) ,'to':str("q"+str(value)),'with':key})
        
        overlapping = pda.verifyOverlapping()

        if overlapping:
            for n in overlapping:
                dGraphTr.append({'from':str("q"+str(n['id'])),'to':str("q"+str(n['id'])),'with':n['label']})
                
        self.G = Graph(dGraphTr,accepted)
        self.G.initGraph(title)

    def showPDA(self,type):
        if type == "odd":
            self.createGraph(self.oddPDA,"Pushdown Automaton Odd Palindrome")
        elif type == "even":
            self.createGraph(self.evenPDA,"Pushdown Automaton Even Palindrome")
        self.sImage.updateImage()

    def validateEvenPDA(self, word, l, stack, transitions):

        validWay = False
        if l<len(word):
            if self.evenPDA.currentState == 0:
                if word[l] in "abcdefghijklmnñopqrstuvwxyz":
                    stack.append(word[l])
                    transitions.append({'id':0,'letter':word[l],'push':True,'change':False})
                elif word[l] == "λ":
                    self.evenPDA.nexState(1)
                    validWay, transitionsAux = self.validateEvenPDA(word,l+1,stack.copy(),transitions.copy())
                    if not validWay:
                        self.evenPDA.nexState(0)
                    else:
                        transitions = transitionsAux 
                        return validWay, transitions 
            elif self.evenPDA.currentState == 1:
                if  word[l] != "λ" and word[l] == stack[-1]:
                    stack.pop()
                    transitions.append({'id':1,'letter':word[l],'push':False,'change':False})
                elif word[l] == "λ":
                    if stack[-1] == "#" and l == len(word)-1:
                        stack.pop()
                        transitions.append({'id':2,'letter':"λ",'push':False,'change':False})
                        self.evenPDA.nexState(2)
                        return True, transitions
                else:
                    return False, []
            validWay, transitions = self.validateEvenPDA(word,l+1, stack,transitions)

        return validWay, transitions

    def validateOddPDA(self,word, transitions, middle):

        for l in word:
            if self.oddPDA.currentState == 0:
                if l in "abcdefghijklmnñopqrstuvwxyz":
                    self.stack.push(l)
                    transitions.append({'id':0,'letter':l,'push':True,'change':False})
                elif l == "|":
                    transitions.append({'id':1,'letter':middle,'push':False,'change':True})
                    self.oddPDA.nexState(1)
            elif self.oddPDA.currentState == 1:
                if l == self.stack.getTop():
                    transitions.append({'id':1,'letter':l,'push':False,'change':False})
                    self.stack.pop()
                    if self.stack.getTop() == "#":
                        transitions.append({'id':2,'letter':l,'push':False,'change':False})
                        self.oddPDA.nexState(2)
                        self.stack.pop()
                else:
                    break
        return transitions

    def runPDA(self, velocity):
        transitions=[]
        length = len(self.word.get())
        middle = int((length+1)/2)-1
        self.oddPDA.nexState(0)
        self.evenPDA.nexState(0)
        self.stack = Stack()
        self.stack.push("#")
        if self.language.verifyComposition(self.word.get()):
            if length%2==0:
                self.showPDA("even")
                word = ""
                for l in self.word.get():
                    word += l+"λ" 
                transitions = self.validateEvenPDA(word,0,['#'],[])[1]
            else:
                self.showPDA("odd")
                word = list(self.word.get())
                lmiddle = word[middle]
                word[middle]="|"
                transitions = self.validateOddPDA(word,transitions, lmiddle)
            result = ""
            if self.oddPDA.verifyAcceptation() or self.evenPDA.verifyAcceptation():
                result = "The word is valid!"
                # self.lblResult.config(text = "Is valid?: YES", fg="green")
                # self.audio.sayResutl("the word is valid!")
            else:
                result = "the word is not valid!"
                # self.lblResult.config(text = "Is valid?: NO", fg="red")
                # self.audio.sayResutl("the word is not valid!")

            self.lblReader.grid(row=5, column=0, pady=5, columnspan=2)
            self.lblResult.grid(row=5, column=2, pady=5, columnspan=2)

            if velocity:
                self.animate(length, transitions, 500, result)
            else:
                self.animate(length, transitions, 2000, result)    

    def changeTransitions(self,a,i):
        self.G.changeState(a,i)
        self.sImage.updateImage()
            
    def pushStack(self, satckPlace,value):
        satckPlace.set(value)

    def popStack(self, satckPlace):
        satckPlace.set("")

    def showReader(self,value):
        self.lblReader.config(text=str("Head Reader: "+value))


    def animate(self,length, transitions, delay, result):

        # clear old stack
        for txt in self.txtStack:
            txt.destroy()

        # creating stack
        stringStack = []
        for i in range(length+1):
            varElem = StringVar()
            element = Entry(self.panelStack.inner, width=7, textvariable=varElem, state='disabled',font=('Verdana',12))
            element.grid(row = i, column=0, columnspan=5)
            element.config(disabledbackground="white", disabledforeground="#000000", justify="center",highlightbackground="#000000",highlightthickness=1, bd=1)
            self.txtStack.append(element)
            stringStack.append(varElem)

        stringStack[-1].set("#")
        self.changeTransitions(("q0","q0"),("q0","q0"))
        s=1
        i="q0"
        a="q0"
        for t in transitions:
            self.gui.after(s*delay,self.changeTransitions,(i,"q"+str(t['id'])),(a,i))
            if t['push']:
                length-=1
                self.gui.after(s*delay,self.pushStack,stringStack[length],t['letter'])
                self.gui.after(s*delay,self.showReader,t['letter'])
            else:
                if t['change']:
                    self.gui.after(s*delay,self.showReader,t['letter'])
                else:
                    if length<len(stringStack):
                        self.gui.after(s*delay,self.showReader,t['letter'])
                        self.gui.after(s*delay,self.popStack,stringStack[length])
                        length+=1
            s+=1
            a=i
            i="q"+str(t['id'])
        self.gui.after((s-1)*delay,messagebox.showinfo,"Message",result)
        self.gui.after(s*delay,self.audio.sayResutl,result)
        

    def runSpeech(self):
        #
        # Wit speech API endpoint
        API_ENDPOINT = 'https://api.wit.ai/speech'
        
        # Wit.ai api access token
        wit_access_token = 'MFPJN7KJ634XSOFQUPZC3FF2SWOCDFJ4'
        
        AUDIO_FILENAME = "audio/myspeech.wav"
        num_seconds = 3
        
        # record audio of specified length in specified audio file
        self.audio.record_audio(num_seconds, AUDIO_FILENAME)
    
        # reading audio
        voice = self.audio.read_audio(AUDIO_FILENAME)
    
        # defining headers for HTTP request
        headers = {'authorization': 'Bearer ' + wit_access_token,'Content-Type': 'audio/wav'}
    
        # making an HTTP post request
        resp = requests.post(API_ENDPOINT, headers = headers, data = voice)
    
        # converting response content to JSON format
        data = json.loads(resp.content.decode("unicode_escape").encode('latin1').decode('utf8'))
    
        # get text from data
        text = data['_text']

        print(text)
        if text == "rápido":
            self.runPDA(True)
        elif text == "lento":
            self.runPDA(False)

            