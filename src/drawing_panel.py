from wx import *

class DrawingPanel(Window):
    def __init__(self, parent):
        Window.__init__(self, parent)

        self.tools = []
        self.SetBackgroundStyle(BG_STYLE_CUSTOM)
        self.SetBackgroundColour("WHITE")

        # drawing update drawing_update_timer
        self.drawing_update_timer = Timer(self)
        self.drawing_update_timer.Start(20)

        self.Bind(EVT_PAINT, self.on_paint_handler)
        self.Bind(EVT_SIZE, self.on_size_handler)
        self.Bind(EVT_TIMER, self.on_timer_handler)

        CallLater(200, self.SetFocus)

    # -----------------------------------------------------------------------

    def on_timer_handler(self, event):
        self.update_drawing()

    def on_size_handler(self, event):
        width, height = self.GetClientSize()
        # self._buffer = Bitmap(width, height)

        for t in self.tools:
            t.x_m = width
            t.y_m = height

        self.update_drawing()

    def update_drawing(self):
        self.Refresh()

    def on_paint_handler(self, event):
        dc = BufferedPaintDC(self)
        dc = GCDC(dc)
        dc.Clear()

        dc.SetPen(Pen("WHITE", 1))
        dc.DrawRectangle(0, 0, self.Size[0], self.Size[1])
        for i in range(len(self.tools)):
            self.tools[i].move(self.tools, i)
        for t in self.tools:
            t.draw(dc)

    def tools_sizes(self):
        pass

    def tools_positions(self):
        pass
