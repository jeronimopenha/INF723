import json
import logging
import random

from wx import *

from src.drawing_panel import DrawingPanel
from src.tool import Tool


class MainFrame(Frame):
    def __init__(self, *args, **kwargs):
        print("main frame init")

        # basic database information
        self.db = None

        # basic frame configurations
        Frame.__init__(self, *args, **kwargs)
        Frame.SetSize(self, 1024, 768)
        Frame.Center(self)

        # main panel
        self.main_panel = Panel(self)

        # box sizers
        self.main_sizer = BoxSizer(HORIZONTAL)
        self.right_sizer = BoxSizer(VERTICAL)
        # ------------------------------------------------

        # menus
        self.menu_bar = MenuBar()
        self.file_menu = Menu()
        self.about_menu = Menu()

        self.file_menu_open = self.file_menu.Append(ID_OPEN, 'Open File', 'Open a JSON file with database')
        self.file_menu_quit = self.file_menu.Append(ID_EXIT, 'Quit', 'Quit application')
        self.about_menu_about = self.about_menu.Append(ID_ABOUT, 'About', 'About Application')

        self.menu_bar.Append(self.file_menu, '&File')
        self.menu_bar.Append(self.about_menu, '&About')
        self.SetMenuBar(self.menu_bar)
        # ------------------------------------------------

        # components

        # Static texts
        self.filter_txt = StaticText(self.main_panel, label="Filter")
        self.emphasis_txt = StaticText(self.main_panel, label="Emphasis")

        # ListBoxes
        self.filter = ListBox(self.main_panel, style=LB_MULTIPLE)
        self.emphasis = ListBox(self.main_panel, style=LB_MULTIPLE)

        # drawing panel
        self.drawing_panel = DrawingPanel(self.main_panel)
        self.drawing_panel.SetBackgroundColour(Colour(255, 255, 255))
        # ------------------------------------------------

        # layout -----------------------------------------
        # adding the components to the respective boxes
        self.main_sizer.Add(self.drawing_panel, proportion=5, flag=EXPAND | ALL, border=5)
        self.main_sizer.Add(self.right_sizer, proportion=1, flag=ALL | EXPAND)

        self.right_sizer.Add(self.filter_txt, flag=ALL, border=2)
        self.right_sizer.Add(self.filter, proportion=1, flag=EXPAND | ALL)
        self.right_sizer.Add(self.emphasis_txt, flag=ALL)
        self.right_sizer.Add(self.emphasis, proportion=1, flag=EXPAND | ALL)
        self.main_panel.SetSizer(self.main_sizer)
        # ------------------------------------------------

        # Events bidings
        self.Bind(EVT_MENU, self.file_menu_quit_handler, self.file_menu_quit)
        self.Bind(EVT_MENU, self.file_menu_open_handler, self.file_menu_open)
        self.Bind(EVT_MENU, self.about_menu_about_handler, self.about_menu_about)
        self.Bind(EVT_CLOSE, self.main_frame_on_close_handler)
        self.Bind(EVT_LISTBOX, self.filter_handler, self.filter)

    # Events handlers functions

    def main_frame_on_close_handler(self, event):
        print("main frame on_close_handler")
        self.Destroy()
        exit()

    def file_menu_quit_handler(self, event):
        print("main frame file_menu_quit_handler")
        self.Close()

    def file_menu_open_handler(self, event):
        print("main frame file_menu_open_handler")
        # Create open file dialog
        with FileDialog(self, "Open Tools JSON Files", wildcard="JSON files (*.json)|*.json",
                        style=FD_OPEN | FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == ID_CANCEL:
                return
            with open(file_dialog.GetPath(), encoding='utf-8') as db_json:
                self.db = json.load(db_json)
        if self.db is not None:
            tools = self.gen_tools()
            self.init_lists(tools)
            self.drawing_panel.set_tools(tools)
            f = []
            self.drawing_panel.set_filter(f)

    def about_menu_about_handler(self, event):
        print("main frame about_menu_about_handler")
        event.Skip()

    def filter_handler(self, event):
        f = []
        opts = self.filter.GetStrings()
        for i in self.filter.GetSelections():
              f.append(opts[i])
        self.drawing_panel.set_filter(f)
        event.Skip()

    # ----------------------------------------------------

    def gen_tools(self):
        tools = []
        c = 0
        for t in self.db:
            attributes = {"name": t["name"], "source": t["source"], "impact": t["impact"], "year": t["year"],
                          "filter": t["filter"]}
            tool = Tool(attributes)
            i_w = self.drawing_panel.i_w + 5
            i_h = self.drawing_panel.i_h + 5
            tool.top_x = random.randint(0, i_w)
            tool.top_y = i_h

            c = c+1
            tools.append(tool)
        return tools

    def init_lists(self, tools):
        to_filter_list = []
        to_emphasis_list = []
        for t in tools:
            for f in t.attributes["filter"]:
                if f not in to_filter_list:
                    to_filter_list.append(f)
            if t.attributes["impact"] not in to_emphasis_list:
                to_emphasis_list.append(t.attributes["impact"])
            if t.attributes["source"] not in to_emphasis_list:
                to_emphasis_list.append(t.attributes["source"])
        to_filter_list.sort()
        to_emphasis_list.sort()
        self.filter.Clear()
        self.emphasis.Clear()
        for f in to_filter_list:
            self.filter.Append(f)
        for i in to_emphasis_list:
            self.emphasis.Append(i)


class MainApp(App):

    def OnInit(self):
        logging.info("MAIN: app on init")
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
