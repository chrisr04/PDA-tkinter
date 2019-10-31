from tkinter import Canvas, Scrollbar, PhotoImage, Frame

class PDAImage(Canvas):

    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        super(PDAImage, self).__init__(master=master, **kw)
        self['highlightthickness'] = 0
        # self.propagate(0)  # wont let the scrollbars rule the size of Canvas
        self.imagePDA = self.create_image(165,75, anchor="center", image=self.image, tags='pda')

        # Assign the region to be scrolled 
        # self.config(scrollregion=self.bbox('all'))

        self.focus_set()

    def updateImage(self):
        self.image = PhotoImage(file="img/pda/pda.png")
        self.itemconfigure(self.imagePDA, image = self.image)

class ScrolledFrame(Frame):

    def __init__(self, parent, vertical=True, horizontal=False):
        super().__init__(parent)
        # canvas for inner frame
        self._canvas = Canvas(self, background= "#595959", bd=0, highlightthickness=0,borderwidth=2 ,relief='solid')
        self._canvas.grid(row=0, column=0, sticky='news') # changed

        # create right scrollbar and connect to canvas Y
        self._vertical_bar = Scrollbar(self, orient='vertical', bg="#1c93e8", relief="flat", command=self._canvas.yview)
        if vertical:
            self._vertical_bar.grid(row=0, column=1, sticky='ns')
        self._canvas.configure(yscrollcommand=self._vertical_bar.set)

        # create bottom scrollbar and connect to canvas X
        self._horizontal_bar = Scrollbar(self, orient='horizontal', command=self._canvas.xview)
        if horizontal:
            self._horizontal_bar.grid(row=1, column=0, sticky='we')
        self._canvas.configure(xscrollcommand=self._horizontal_bar.set)

        # inner frame for widgets
        self.inner = Frame(self._canvas,  bg= "#595959")
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