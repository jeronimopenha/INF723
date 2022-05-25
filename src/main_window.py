import json
import wx


# todo menu events
# todo todos os eventos

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        print("main frame init")
        # basic database information

        self.db = None
        self.tools = []
        self.filtered = []
        self.emphasized = []

        # basic frame configurations
        wx.Frame.__init__(self, *args, **kwargs)
        wx.Frame.SetSize(self, 800, 600)
        wx.Frame.Center(self)

        # main panel
        self.main_panel = wx.Panel(self)

        # box sizers
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        # ------------------------------------------------

        # menus
        self.menu_bar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.about_menu = wx.Menu()

        self.file_menu_open = self.file_menu.Append(wx.ID_OPEN, 'Open File', 'Open a JSON file with database')
        self.file_menu_quit = self.file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        self.about_menu_about = self.about_menu.Append(wx.ID_ABOUT, 'About', 'About Application')

        self.menu_bar.Append(self.file_menu, '&File')
        self.menu_bar.Append(self.about_menu, '&About')
        self.SetMenuBar(self.menu_bar)
        # ------------------------------------------------

        # components
        # Static texts
        self.filter_txt = wx.StaticText(self.main_panel, label="Filter")
        self.emphasis_txt = wx.StaticText(self.main_panel, label="Emphasis")

        # ListBoxes
        self.filter = wx.ListBox(self.main_panel, style=wx.LB_MULTIPLE)
        self.emphasis = wx.ListBox(self.main_panel, style=wx.LB_MULTIPLE)

        # drawing panel
        self.drawing_panel = wx.Panel(self.main_panel)
        self.drawing_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        # ------------------------------------------------

        # layout -----------------------------------------
        # adding the components to the respective boxes
        self.main_sizer.Add(self.drawing_panel, proportion=5, flag=wx.EXPAND | wx.ALL, border=5)
        self.main_sizer.Add(self.right_sizer, proportion=1, flag=wx.ALL | wx.EXPAND)

        self.right_sizer.Add(self.filter_txt, flag=wx.ALL, border=2)
        self.right_sizer.Add(self.filter, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.right_sizer.Add(self.emphasis_txt, flag=wx.ALL)
        self.right_sizer.Add(self.emphasis, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.main_panel.SetSizer(self.main_sizer)
        # ------------------------------------------------

        # Events bidings
        self.Bind(wx.EVT_MENU, self.file_menu_quit_handler, self.file_menu_quit)
        self.Bind(wx.EVT_MENU, self.file_menu_open_handler, self.file_menu_open)
        self.Bind(wx.EVT_MENU, self.about_menu_about_handler, self.about_menu_about)
        self.Bind(wx.EVT_SIZE, self.main_frame_on_resize)

    def file_menu_quit_handler(self, event):
        print("main frame file_menu_quit_handler")
        self.Close()

    def file_menu_open_handler(self, event):
        print("main frame file_menu_open_handler")
        # Create open file dialog
        with wx.FileDialog(self, "Open Tools JSON Files", wildcard="JSON files (*.json)|*.json",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            with open(file_dialog.GetPath(), encoding='utf-8') as db_json:
                self.db = json.load(db_json)
        if self.db is not None:
            self.gen_tools()
            self.init_lists()
            self.draw_tools()

    def gen_tools(self):
        for t in self.db:
            nome = t["Nome"]
            periodico = t["Periodico"]
            impacto = t["Impacto"]
            ano = t["Ano"]
            funcionalidades = t["Funcionalidades"]
            self.tools.append(Tool(nome, periodico, impacto, ano, funcionalidades))

    def init_lists(self):
        for t in self.tools:
            self.filter.Append("teste")

    def draw_tools(self):
        pass

    def about_menu_about_handler(self, event):
        print("main frame about_menu_about_handler")
        event.Skip()

    def main_frame_on_resize(self, event):
        print("main frame main_frame_on_resize")
        event.Skip()


class Tool:
    def __init__(self, nome, periodico, impacto, ano, funcionalidades):
        self.nome = nome
        self.periodico = periodico
        self.impacto = impacto
        self.ano = ano
        self.funcionalidades = funcionalidades
        self.x_i = 0
        self.x_e = 0
        self.y_i = 0
        self.y_e = 0


class DrawingPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetBackgroundColour('#ededed')

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    # -----------------------------------------------------------------------

    def OnPaint(self, event):
        self.SetBackgroundColour('#ffffff')
        """
        ...
        """
        '''
        pdc = wx.PaintDC(self)
        gc = wx.GCDC(pdc)
        gc.Clear()

        #------------
        # Square.
        #------------

        gc.SetPen(wx.Pen("red", 2))
        gc.SetBrush(wx.Brush("yellow"))

        x = 100
        y = 30
        w = 50
        h = 50

        # pt, sz
        # or
        # rect
        # or
        # x, y, width, height
        gc.DrawRectangle(x , y, w, h)
        gc.DrawText("Square", int(x+w+10), int(y+h/2))

        #------------
        # Rectangle.
        #------------

        gc.SetPen(wx.Pen("black", 2))
        gc.SetBrush(wx.Brush((0, 255, 255, 255)))

        x = 100
        y = 130
        w = 100
        h = 50

        # pt, sz
        # or
        # rect
        # or
        # x, y, width, height
        gc.DrawRectangle(x , y, w, h)
        gc.DrawText("Rectangle", int(x+w+10), int(y+h/2))

        #------------
        # Rounded rectangle.
        #------------

        gc.SetPen(wx.Pen("black", 2))
        gc.SetBrush(wx.Brush((255, 0, 255, 128)))

        x = 100
        y = 230
        w = 100
        h = 50
        r = 8

        # pt, sz, radius
        # or
        # rect, radius
        # or
        # x, y, width, height, radius)
        gc.DrawRoundedRectangle(x, y, w, h, r)
        gc.DrawText("Rounded rectangle", int(x+w+10), int(y+h/2))

        #------------
        # Ellipse.
        #------------

        gc.SetPen(wx.Pen("gray", 2))
        gc.SetBrush(wx.Brush("green"))

        x = 100
        y = 330
        w = 100
        h = 50

        # pt, size
        # or
        # rect
        # or
        # x, y, width, height
        gc.DrawEllipse(x, y, w, h)
        gc.DrawText("Ellipse", int(x+w+10), int(y+h/2))

        #------------
        # Circle.
        #------------

        gc.SetPen(wx.Pen("red", 2))
        gc.SetBrush(wx.Brush("#ffc0cb"))

        x = 130
        y = 455
        r = 35

        # pt, radius
        # or
        # x, y, radius
        gc.DrawCircle(x, y, r)
        gc.DrawText("Circle", int(x+45), int(y))

        #------------
        # Line.
        #------------

        gc.SetPen(wx.Pen("purple", 4))

        x1 = 100
        y1 = 545
        x2 = 200
        y2 = 545

        # pt1, pt2
        # or
        # x1, y1, x2, y2
        gc.DrawLine(x1, y1, x2, y2)
        gc.DrawText("Line", int(x+w-10), int(y+80))

        #------------
        # Triangle.
        #------------

        gc.SetPen(wx.Pen("blue", 2))
        gc.SetBrush(wx.Brush((150, 150, 150, 128)))

        points = [(80, 80),
                  (10, 10),
                  (80, 10),
                  (80, 80)
                  ]
        x = 90
        y = 580

        # points, xoffset=0, yoffset=0, fill_style=ODDEVEN_RULE
        gc.DrawPolygon(points, x, y)
        gc.DrawText("Triangle", int(x+w-5), int(y+h/2))
        '''


class MainApp(wx.App):

    def OnInit(self):
        print("main app on init")
        frame = MainFrame(None, title="VISOR")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True


# ---------------------------------------------------------------------------

def main():
    print("main")
    app = MainApp(False)
    app.MainLoop()


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("calling main routine")
    main()
