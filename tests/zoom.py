import wx
import wx.lib.scrolledpanel as scrolledpanel


class ImagePanel(scrolledpanel.ScrolledPanel):

    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN
                 ):

        super().__init__(parent, id, pos, size, style=style)

        self.bmpImage = wx.StaticBitmap(self, wx.ID_ANY)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.bmpImage, proportion=1, flag=wx.ALL|wx.EXPAND)
        self.SetSizer(sizer)

        self.bitmap = None  # loaded image in bitmap format
        self.image = None   # loaded image in image format
        self.aspect = None  # loaded image aspect ratio
        self.zoom = 1.0     # zoom factor

        self.blank = wx.Bitmap(1, 1)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)

        self.SetupScrolling()

        # wx.lib.inspection.InspectionTool().Show()

    def OnSize(self, event):
        """When panel is resized, scale the image to fit"""
        self.ScaleToFit()
        event.Skip()

    def OnMouseWheel(self, event):
        """zoom in/out on CTRL+scroll"""
        m = wx.GetMouseState()

        if m.ControlDown():
            delta = 0.1 * event.GetWheelRotation() / event.GetWheelDelta()
            self.zoom = max(1, self.zoom + delta)
            self.ScaleToFit()

        event.Skip()

    def Load(self, file: str) -> None:
        """Load the image file into the control for display"""
        #self.bitmap = wx.Bitmap(file, wx.BITMAP_TYPE_ANY)
        self.bitmap = wx.Bitmap(1920,1080)
        temp_dc = wx.MemoryDC()
        temp_dc.SelectObject(self.bitmap)
        #temp_dc.SetBackground(wx.Brush("WHITE"))
        temp_dc.DrawRectangle(0, 0, self.bitmap.Size[0], self.bitmap.Size[0])
        temp_dc.SetBrush(wx.Brush("PINK"))
        temp_dc.SetPen(wx.Pen("BLACK", 2))
        temp_dc.DrawCircle(100,100,50)
        temp_dc.DrawCircle(300, 100, 50)
        temp_dc.DrawRectangle(600,300, 50,50)
        self.image = wx.Bitmap.ConvertToImage(self.bitmap)
        self.aspect = self.image.GetSize()[1] / self.image.GetSize()[0]
        self.zoom = 1.0

        self.bmpImage.SetBitmap(self.bitmap)

        self.ScaleToFit()

    def Clear(self):
        """Set the displayed image to blank"""
        self.bmpImage.SetBitmap(self.blank)
        self.zoom = 1.0

    def ScaleToFit(self) -> None:
        """
        Scale the image to fit in the container while maintaining
        the original aspect ratio.
        """
        if self.image:

            # get container (c) dimensions
            cw, ch = self.GetSize()

            # calculate new (n) dimensions with same aspect ratio
            nw = cw
            nh = int(nw * self.aspect)

            # if new height is too large then recalculate sizes to fit
            if nh > ch:
                nh = ch
                nw = int(nh / self.aspect)

            # Apply zoom
            nh = int(nh * self.zoom)
            nw = int(nw * self.zoom)

            # scale the image to new dimensions and display
            image = self.image.Scale(nw, nh)
            self.bmpImage.SetBitmap(image.ConvertToBitmap())
            self.Layout()

            if self.zoom > 1.0:
                self.ShowScrollBars = True
                self.SetupScrolling()
            else:
                self.ShowScrollBars = False
                self.SetupScrolling()


if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None)
    panel = ImagePanel(frame)
    frame.SetSize(800, 625)
    frame.Show()
    panel.Load('/home/jeronimo/Pictures/29z94ec.jpg')
    app.MainLoop()

'''
import wx
import wx.lib.scrolledpanel as scrolledpanel


class ImagePanel(scrolledpanel.ScrolledPanel):

    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN
                 ):

        super().__init__(parent, id, pos, size, style=style)

        self.bmpImage = wx.StaticBitmap(self, wx.ID_ANY)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.bmpImage, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)

        self.bitmap = None  # loaded image in bitmap format
        self.image = None   # loaded image in image format
        self.aspect = None  # loaded image aspect ratio
        self.zoom = 1.0     # zoom factor

        self.blank = wx.Bitmap(1, 1)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)

        self.SetupScrolling()

        # wx.lib.inspection.InspectionTool().Show()

    def OnSize(self, event):
        """When panel is resized, scale the image to fit"""
        self.ScaleToFit()
        event.Skip()

    def OnMouseWheel(self, event):
        """zoom in/out on CTRL+scroll"""
        m = wx.GetMouseState()

        if m.ControlDown():
            delta = 0.1 * event.GetWheelRotation() / event.GetWheelDelta()
            self.zoom = max(1, self.zoom + delta)
            self.ScaleToFit()

        event.Skip()

    def Load(self, file: str) -> None:
        """Load the image file into the control for display"""
        self.bitmap = wx.Bitmap(file, wx.BITMAP_TYPE_ANY)
        self.image = wx.Bitmap.ConvertToImage(self.bitmap)
        self.aspect = self.image.GetSize()[1] / self.image.GetSize()[0]
        self.zoom = 1.0

        self.bmpImage.SetBitmap(self.bitmap)

        self.ScaleToFit()

    def Clear(self):
        """Set the displayed image to blank"""
        self.bmpImage.SetBitmap(self.blank)
        self.zoom = 1.0

    def ScaleToFit(self) -> None:
        """
        Scale the image to fit in the container while maintaining
        the original aspect ratio.
        """
        if self.image:

            # get container (c) dimensions
            cw, ch = self.GetSize()

            # calculate new (n) dimensions with same aspect ratio
            nw = cw
            nh = int(nw * self.aspect)

            # if new height is too large then recalculate sizes to fit
            if nh > ch:
                nh = ch
                nw = int(nh / self.aspect)

            # Apply zoom
            nh = int(nh * self.zoom)
            nw = int(nw * self.zoom)

            # scale the image to new dimensions and display
            image = self.image.Scale(nw, nh)
            self.bmpImage.SetBitmap(image.ConvertToBitmap())
            self.Layout()

            if self.zoom > 1.0:
                self.ShowScrollBars = True
                self.SetupScrolling()
            else:
                self.ShowScrollBars = False
                self.SetupScrolling()


if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None)
    panel = ImagePanel(frame)
    frame.SetSize(800, 625)
    frame.Show()
    panel.Load('/home/jeronimo/Pictures/29z94ec.jpg')
    app.MainLoop()
'''