import wx

from src.main_window import MainFrame


class MainApp(wx.App):

    def OnInit(self):
        frame = MainFrame(None, title="VISOR")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

#---------------------------------------------------------------------------

def main():
    app = MainApp(False)
    app.MainLoop()

#---------------------------------------------------------------------------

if __name__ == "__main__" :
    main()