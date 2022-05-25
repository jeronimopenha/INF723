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
        self.drawing_panel = DrawingPanel(self.main_panel)
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
        self.Bind(wx.EVT_SIZE, self.main_frame_on_resize_handler)


    # Events handlers functions
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
            self.drawing_panel.tools = self.tools
            self.Update()

    def about_menu_about_handler(self, event):
        print("main frame about_menu_about_handler")
        event.Skip()

    def main_frame_on_resize_handler(self, event):
        print("main frame main_frame_on_resize")
        event.Skip()

    # ----------------------------------------------------

    def gen_tools(self):
        self.tools = []
        for t in self.db:
            nome = t["Nome"]
            periodico = t["Periodico"]
            impacto = t["Impacto"]
            ano = t["Ano"]
            funcionalidades = t["Funcionalidades"]
            self.tools.append(Tool(nome, periodico, impacto, ano, funcionalidades))

    def init_lists(self):
        to_filter_list = []
        to_emphasis_list = []
        for t in self.tools:
            for f in t.funcionalidades:
                if f not in to_filter_list:
                    to_filter_list.append(f)
            if t.impacto not in to_emphasis_list:
                to_emphasis_list.append(t.impacto)
            if t.periodico not in to_emphasis_list:
                to_emphasis_list.append(t.periodico)
        to_filter_list.sort()
        to_emphasis_list.sort()
        self.filter.Clear()
        self.emphasis.Clear()
        for f in to_filter_list:
            self.filter.Append(f)
        for i in to_emphasis_list:
            self.emphasis.Append(i)

class DrawingPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        self.tools = []
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetBackgroundColour('#ffffff')
        self.Bind(wx.EVT_PAINT, self.on_paint_handler)

    def on_paint_handler(self, event):
        self.SetBackgroundColour('#ffffff')
        pdc = wx.PaintDC(self)
        gc = wx.GCDC(pdc)
        gc.Clear()

        x = 100
        y = 230
        w = 50
        h = 50
        r = 8

        for t in self.tools:
            gc.SetPen(wx.Pen("black", 2))
            #gc.SetBrush(wx.Brush((255, 0, 255, 128)))
            gc.DrawRoundedRectangle(x, y, w, h, r)
            gc.DrawText("Rounded rectangle", int(x + w + 10), int(y + h / 2))
            x = x + 50
            y = y +50


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
