import pyttsx3, pyaudio, wave, requests, json
from tkinter import *
from .language import Language
from .state import State
from .pda import PDA
from .stack import Stack
from .tree import ExpressionTree
from .graph import Graph

class ScrollableImage(Canvas):

    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self['highlightthickness'] = 0
        self.propagate(0)  # wont let the scrollbars rule the size of Canvas
        self.create_image(0,0, anchor=CENTER, image=self.image, tags='dfa')

        # Assign the region to be scrolled 
        self.config(scrollregion=self.bbox('all'))

        self.focus_set()

class App:

    def __init__(self):

        self.gui = Tk()
        self.gui.geometry("510x500")
        self.icon = Image("photo", file="python-logo.png")
        self.gui.tk.call('wm','iconphoto',self.gui._w, self.icon)
        self.txtStack = []
        self.G = None
        self.stack = None
        self.automata = []
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
        self.lblResult = Label(self.panel, text="", font=('Verdana',11))
    
        self.sImage = ScrollableImage(self.panel)
        self.showPDA()

        self.lblStack = Label(self.panel, text="Stack", font=('Verdana',20))
        self.lblStack.grid(row = 3,column=0, columnspan=5, pady=10)

        # self.lbxStack = Listbox(self.panel, width=7)
        # self.lbxStack.grid(row = 2, column =6, padx=20)

        mainloop()

    def showPDA(self):
        self.createPDA()
        self.createGraph()
        self.drawPDA()


    def createPDA(self):

        # Create the states
        state1 = State(0,"q",False)
        state2 = State(1,"q",False)
        state3 = State(2,"q",True)

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
        state1.addTransition("∈, ∈ ⟶ ∈",1)
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
        state2.addTransition("∈, # ⟶ ∈",2)

        self.automata = PDA([state1,state2,state3])

    def createGraph(self):
        dGraphTr = []
        accepted = []
        for s in self.automata.states:
            if s.accepted:
                accepted.append("q"+str(s.id))
            for key,value in s.transitions.items():
                if s.id != value:
                    dGraphTr.append({'from':str("q"+str(s.id)) ,'to':str("q"+str(value)),'with':key})
        
        overlapping = self.automata.verifyOverlapping()

        if overlapping:
            for n in overlapping:
                dGraphTr.append({'from':str("q"+str(n['id'])),'to':str("q"+str(n['id'])),'with':n['label']})
                
        self.G = Graph(dGraphTr,accepted)
        self.G.initGraph()


    def drawPDA(self):
        self.sImage.destroy()
        img = PhotoImage(file="pda/pda.png")
        self.sImage = ScrollableImage(self.panel, image = img, width=img.width()+10, height=img.height(), bg="#ffffff")
        self.sImage.grid(row=2, column=0,columnspan=5, padx= 20)

    def changeTransitions(self,i,a):
        self.G.changeState(i,a)
        self.drawPDA()

    def animate(self,length, transitions, delay):

        for txt in self.txtStack:
            txt.destroy()

        stringStack = []
        for i in range(4,length+4):
            varElem = StringVar()
            stringStack.append(varElem)
            element = Entry(self.panel, width=7, textvariable=varElem, state='disabled',font=('Verdana',12))
            element.grid(row = i, column=0, columnspan=5)
            element.config(disabledbackground="white", disabledforeground="#000000", justify="center",highlightbackground="#000000",highlightthickness=1, bd=1)
            self.txtStack.append(element)

        stringStack[-1].set("#")
        length-=1
        self.changeTransitions(0,0)
        s=1
        i=0

        for t in transitions:
            self.gui.after(s*delay,self.changeTransitions,t['id'],i)
            if t['push']:
                length-=1
                self.gui.after(s*delay,self.pushStack,stringStack[length],t['letter'])
            else:
                self.gui.after(s*delay,self.popStack,stringStack[length])
                length+=1
            s+=1
            i=t['id']
    

    def pushStack(self, satckPlace,value):
        satckPlace.set(value)

    def popStack(self, satckPlace):
        satckPlace.set("")

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
        stream = audio.open(format=FORMAT,channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
    
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
        headers = {'authorization': 'Bearer ' + wit_access_token,
                'Content-Type': 'audio/wav'}
    
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

    def runPDA(self, velocity):
        transitions=[]
        length = len(self.word.get())
        middle = int((length+1)/2)-1
        self.G.initGraph()
        self.automata.nexState(0)
        self.stack = Stack()
        self.stack.push("#")
        if self.language.verifyComposition(self.word.get()):
            for i,l in enumerate(self.word.get()):
                if self.automata.currentState == 0:
                    if l in "abcdefghijklmnñopqrstuvwxyz":
                        if i == middle:
                            self.automata.nexState(1)
                            if length%2==0:
                                self.stack.push(l)
                                transitions.append({'id':0,'letter':l,'push':True})
                        else:
                            self.stack.push(l)
                            transitions.append({'id':0,'letter':l,'push':True})
                elif self.automata.currentState == 1:
                    transitions.append({'id':1,'letter':l,'push':False})
                    if l == self.stack.getTop():
                        self.stack.pop()
                        if self.stack.getTop() == "#":
                            transitions.append({'id':2,'letter':l,'push':False})
                            self.automata.nexState(2)
                            self.stack.pop()
                    else:
                        break

            if self.automata.verifyAcceptation():
                self.lblResult.config(text = "Is valid?: YES", fg="green")
                self.sayResutl("the word is valid!")
            else:    
                self.lblResult.config(text = "Is valid?: NO", fg="red")
                self.sayResutl("the word is not valid!")
            self.lblResult.grid(row=length+5, column=0, pady=10, columnspan=5)

            if velocity:
                self.animate(length, transitions, 500)
            else:
                self.animate(length, transitions, 2000)
            