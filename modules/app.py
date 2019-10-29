import pyttsx3, pyaudio, wave, requests, json, copy
from tkinter import *
from .language import Language
from .state import State
from .pda import PDA
from .stack import Stack
from .tree import ExpressionTree
from .graph import Graph

class PDAImage(Canvas):

    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        super(PDAImage, self).__init__(master=master, **kw)
        self['highlightthickness'] = 0
        self.propagate(0)  # wont let the scrollbars rule the size of Canvas
        self.imagePDA = self.create_image(0,0, anchor=CENTER, image=self.image, tags='pda')

        # Assign the region to be scrolled 
        self.config(scrollregion=self.bbox('all'))

        self.focus_set()

    def updateImage(self):
        self.image = PhotoImage(file="pda/pda.png")
        self.itemconfigure(self.imagePDA, image = self.image)

class ScrolledFrame(Frame):

    def __init__(self, parent, vertical=True, horizontal=False):
        super().__init__(parent)

        # canvas for inner frame
        self._canvas = Canvas(self)
        self._canvas.grid(row=0, column=0, sticky='news') # changed

        # create right scrollbar and connect to canvas Y
        self._vertical_bar = Scrollbar(self, orient='vertical', command=self._canvas.yview)
        if vertical:
            self._vertical_bar.grid(row=0, column=1, sticky='ns')
        self._canvas.configure(yscrollcommand=self._vertical_bar.set)

        # create bottom scrollbar and connect to canvas X
        self._horizontal_bar = Scrollbar(self, orient='horizontal', command=self._canvas.xview)
        if horizontal:
            self._horizontal_bar.grid(row=1, column=0, sticky='we')
        self._canvas.configure(xscrollcommand=self._horizontal_bar.set)

        # inner frame for widgets
        self.inner = Frame(self._canvas)
        self._window = self._canvas.create_window((160, 0), window=self.inner, anchor='nw')

        # autoresize inner frame
        self.columnconfigure(0, weight=1) # changed
        self.rowconfigure(0, weight=1) # changed

        # resize when configure changed
        self.inner.bind('<Configure>', self.resize)
        self._canvas.bind('<Configure>', self.frame_width)

    def frame_width(self, event):
        # resize inner frame to canvas size
        self._canvas.itemconfig(self._window, width = 200)

    def resize(self, event=None): 
        self._canvas.configure(scrollregion=self._canvas.bbox('all'))

class App:

    def __init__(self):

        self.gui = Tk()
        self.gui.title("Pushdown Automaton")
        self.gui.geometry("510x620")
        self.gui.resizable(False,False)
        self.icon = Image("photo", file="python-logo.png")
        self.gui.tk.call('wm','iconphoto',self.gui._w, self.icon)
        self.txtStack = []
        self.G = None
        self.stack = None
        self.evenPDA = None
        self.oddPDA = None
        self.transitions = []
        self.states = []
        self.language = Language("{λ, a, b, c, d, e, f, g, h, i, j, k, l, m, n, ñ, o, p, q, r, s, t, u, v, w, x, y, z}")
        self.currentRegex = StringVar()
        self.word = StringVar()

        self.panel = Frame(self.gui)
        self.panel.pack(fill="both", expand="True")

        self.lblPDA = Label(self.panel, text="Pushdown Automaton", font=('Verdana',20))
        self.lblPDA.grid(row = 0,column=0, columnspan=5, pady=10)

        self.lblWord = Label(self.panel, text="Word:", font=('Verdana',12))
        self.lblWord.grid(row = 1, column=0, pady=10)
        self.txtWord=Entry(self.panel, textvariable = self.word, width="16",font=('Verdana',12))
        self.txtWord.grid(row=1, column=1, pady=10)
        self.txtWord.config(disabledbackground="black", disabledforeground="#03f943", justify="left",highlightbackground="#000000",highlightthickness=1, bd=0)
        self.btnVerifyFast=Button(self.panel, text="fast", font=('Verdana',10), command=lambda:self.runPDA(True))
        self.btnVerifyFast.grid(row=1, column=2)
        self.btnVerifyLow=Button(self.panel, text="slow", font=('Verdana',10), command=lambda:self.runPDA(False))
        self.btnVerifyLow.grid(row=1, column=3)
        self.btnSpeech=Button(self.panel, text="voice", font=('Verdana',10), command=lambda:self.runSpeech())
        self.btnSpeech.grid(row=1, column=4)
        
        img = PhotoImage(file="pda/background.png")
        self.sImage = PDAImage(self.panel, image = img, width=465, height=137, bg="#ffffff")
        self.sImage.grid(row=2, column=0,columnspan=5, padx= 20)
        self.createPDA()
        self.showPDA("odd")

        self.lblStack = Label(self.panel, text="Stack", font=('Verdana',20))
        self.lblStack.grid(row = 3,column=0, columnspan=5, pady=10)

        self.panelStack = ScrolledFrame(self.panel)
        self.panelStack.grid(row = 4,column=0, columnspan=5, pady=10)

        for i in range(10):
            element = Entry(self.panelStack.inner, width=7, state='disabled',font=('Verdana',12))
            element.grid(row = i, column=0, columnspan=5)
            element.config(disabledbackground="white", disabledforeground="#000000", justify="center",highlightbackground="#000000",highlightthickness=1, bd=1)
            self.txtStack.append(element)

        self.lblResult = Label(self.panel, text="", font=('Verdana',11))
        self.lblReader = Label(self.panel, text="", font=('Verdana',11))

        mainloop()

    def showPDA(self,type):
        if type == "odd":
            self.createGraph(self.oddPDA,"Pushdown Automaton Odd Palindrome")
        elif type == "even":
            self.createGraph(self.evenPDA,"Pushdown Automaton Even Palindrome")
        self.sImage.updateImage()


    def createPDA(self):

        # Create the states
        state1 = State(0,"q",False)
        state2 = State(1,"q",False)
        state3 = State(2,"q",True)
        state4 = State(0,"q",False)

        # Add the transitions
        state1.addTransition("a",0)
        state1.addTransition("b",0)
        state1.addTransition("c",0)
        state1.addTransition("d",0)
        state1.addTransition("e",0)
        state1.addTransition("f",0)
        state1.addTransition("g",0)
        state1.addTransition("h",0)
        state1.addTransition("i",0)
        state1.addTransition("j",0)
        state1.addTransition("k",0)
        state1.addTransition("l",0)
        state1.addTransition("m",0)
        state1.addTransition("n",0)
        state1.addTransition("ñ",0)
        state1.addTransition("o",0)
        state1.addTransition("p",0)
        state1.addTransition("q",0)
        state1.addTransition("r",0)
        state1.addTransition("s",0)
        state1.addTransition("t",0)
        state1.addTransition("u",0)
        state1.addTransition("v",0)
        state1.addTransition("w",0)
        state1.addTransition("x",0)
        state1.addTransition("y",0)
        state1.addTransition("z",0)
        state1.addTransition("λ, λ ⟶ λ",1)
        state2.addTransition("a",1)
        state2.addTransition("b",1)
        state2.addTransition("c",1)
        state2.addTransition("d",1)
        state2.addTransition("e",1)
        state2.addTransition("f",1)
        state2.addTransition("g",1)
        state2.addTransition("h",1)
        state2.addTransition("i",1)
        state2.addTransition("j",1)
        state2.addTransition("k",1)
        state2.addTransition("l",1)
        state2.addTransition("m",1)
        state2.addTransition("n",1)
        state2.addTransition("ñ",1)
        state2.addTransition("o",1)
        state2.addTransition("p",1)
        state2.addTransition("q",1)
        state2.addTransition("r",1)
        state2.addTransition("s",1)
        state2.addTransition("t",1)
        state2.addTransition("u",1)
        state2.addTransition("v",1)
        state2.addTransition("w",1)
        state2.addTransition("x",1)
        state2.addTransition("y",1)
        state2.addTransition("z",1)
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
        

    def changeTransitions(self,a,i):
        self.G.changeState(a,i)
        self.sImage.updateImage()

    def animate(self,length, transitions, delay):

        for txt in self.txtStack:
            txt.destroy()
        self.lblReader.grid(row=5, column=0, pady=5, columnspan=2)
        stringStack = []
        for i in range(length+1):
            varElem = StringVar()
            stringStack.append(varElem)
            element = Entry(self.panelStack.inner, width=7, textvariable=varElem, state='disabled',font=('Verdana',12))
            element.grid(row = i, column=0, columnspan=5)
            element.config(disabledbackground="white", disabledforeground="#000000", justify="center",highlightbackground="#000000",highlightthickness=1, bd=1)
            self.txtStack.append(element)

        stringStack[-1].set("#")
        length-=1
        self.changeTransitions(("q0","q0"),("q0","q0"))
        s=1
        i="q0"
        a="q0"
        for t in transitions:
            self.gui.after(s*delay,self.changeTransitions,(i,"q"+str(t['id'])),(a,i))
            if t['push']:
                self.gui.after(s*delay,self.pushStack,stringStack[length],t['letter'])
                length-=1
            else:
                self.gui.after(s*delay,self.popStack,stringStack[length],t['letter'])
                length+=1
            s+=1
            a=i
            i="q"+str(t['id'])
            
    

    def pushStack(self, satckPlace,value):
        self.lblReader.config(text=str("Reader: "+value))
        satckPlace.set(value)

    def popStack(self, satckPlace, value):
        self.lblReader.config(text=str("Reader: "+value))
        satckPlace.set("")

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

            if self.oddPDA.verifyAcceptation() or self.evenPDA.verifyAcceptation():
                self.lblResult.config(text = "Is valid?: YES", fg="green")
                self.sayResutl("the word is valid!")
            else:    
                self.lblResult.config(text = "Is valid?: NO", fg="red")
                self.sayResutl("the word is not valid!")

            self.lblResult.grid(row=5, column=1, pady=5, columnspan=3)

            if velocity:
                self.animate(length, transitions, 500)
            else:
                self.animate(length, transitions, 2000)


    def validateEvenPDA(self, word, l, stack, transitions):
        validWay = False
        if l<len(word):

            if self.evenPDA.currentState == 0:
                if word[l] in "abcdefghijklmnñopqrstuvwxyz":
                    stack.append(word[l])
                    transitions.append({'id':0,'letter':word[l],'push':True})
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
                    transitions.append({'id':1,'letter':word[l],'push':False})
                elif word[l] == "λ":
                    if stack[-1] == "#" and l == len(word)-1:
                        stack.pop()
                        transitions.append({'id':2,'letter':word[l],'push':False})
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
                    transitions.append({'id':0,'letter':l,'push':True})
                elif l == "|":
                    transitions.append({'id':0,'letter':middle,'push':False})
                    self.oddPDA.nexState(1)
            elif self.oddPDA.currentState == 1:
                transitions.append({'id':1,'letter':l,'push':False})
                if l == self.stack.getTop():
                    self.stack.pop()
                    if self.stack.getTop() == "#":
                        transitions.append({'id':2,'letter':l,'push':False})
                        self.oddPDA.nexState(2)
                        self.stack.pop()
                else:
                    break
        return transitions
        

    def sayResutl(self,value):
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.setProperty('volume', 0.9)
        engine.setProperty('voice', 'english+m5')
        engine.say(str(value))
        engine.runAndWait()

    def record_audio(self,RECORD_SECONDS, WAVE_OUTPUT_FILENAME):
        #--------- SETTING PARAMS FOR OUR AUDIO FILE ------------#
        FORMAT = pyaudio.paInt16    # format of wave
        CHANNELS = 2                # no. of audio channels
        RATE = 44100                # frame rate
        CHUNK = 1024                # frames per audio sample
        #--------------------------------------------------------#
    
        # creating PyAudio object
        audio = pyaudio.PyAudio()
    
        # open a new stream for microphone
        # It creates a PortAudio Stream Wrapper class object
        stream = audio.open(format=FORMAT,channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
    
        #----------------- start of recording -------------------#
        print("Listening...")
    
        # list to save all audio frames
        frames = []
    
        for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
            # read audio stream from microphone
            data = stream.read(CHUNK)
            # append audio data to frames list
            frames.append(data)
    
        #------------------ end of recording --------------------#
        print("Finished recording.")
    
        stream.stop_stream()    # stop the stream object
        stream.close()          # close the stream object
        audio.terminate()       # terminate PortAudio
    
        #------------------ saving audio ------------------------#
    
        # create wave file object
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    
        # settings for wave file object
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
    
        # closing the wave file object
        waveFile.close()
    
    def read_audio(self,WAVE_FILENAME):
        # function to read audio(wav) file
        with open(WAVE_FILENAME, 'rb') as f:
            audio = f.read()
        return audio

    def runSpeech(self):
        #

        # Wit speech API endpoint
        API_ENDPOINT = 'https://api.wit.ai/speech'
        
        # Wit.ai api access token
        wit_access_token = 'MFPJN7KJ634XSOFQUPZC3FF2SWOCDFJ4'
        
        AUDIO_FILENAME = "audio/myspeech.wav"
        num_seconds = 3
        
        # record audio of specified length in specified audio file
        self.record_audio(num_seconds, AUDIO_FILENAME)
    
        # reading audio
        audio = self.read_audio(AUDIO_FILENAME)
    
        # defining headers for HTTP request
        headers = {'authorization': 'Bearer ' + wit_access_token,'Content-Type': 'audio/wav'}
    
        # making an HTTP post request
        resp = requests.post(API_ENDPOINT, headers = headers,
                            data = audio)
    
        # converting response content to JSON format
        data = json.loads(resp.content.decode("unicode_escape").encode('latin1').decode('utf8'))
    
        # get text from data
        text = data['_text']

        print(text)
        if text == "rápido":
            self.runPDA(True)
        elif text == "lento":
            self.runPDA(False)

            