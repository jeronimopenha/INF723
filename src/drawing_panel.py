import random

from wx import *
import wx.lib.scrolledpanel as scrolled
from math import ceil
from src.cell import Cell


class DrawingPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        Window.__init__(self, parent)

        self.parent = parent

        # constants
        self.cell_width = 230
        self.cell_height = 70
        self.hor_total_free_space_min = 0.2
        self.vertical_gap = 30
        self.min_needed_width = 1100

        # ---------
        self.showed_cells = []
        self.origin_cells = []
        self.tools = []
        self.filter = []
        self.emphasis = []

        self.w_w = 0
        self.w_h = 0
        self.i_w = 0
        self.i_h = 0

        # self.SetBackgroundStyle(BG_STYLE_CUSTOM)
        # self.SetBackgroundColour("WHITE")

        self.bmpImage = StaticBitmap(self, ID_ANY)
        sizer = BoxSizer(VERTICAL)
        sizer.Add(self.bmpImage, proportion=1, flag=ALL | EXPAND)
        self.SetSizer(sizer)

        self.ShowScrollBars = False

        # background bitmap
        self.bitmap = None  # loaded image in bitmap format
        self.image = None  # loaded image in image format
        self.aspect = None  # loaded image aspect ratio
        self.zoom = 1.0  # zoom factor

        # drawing update drawing_update_timer
        self.drawing_update_timer = Timer(self)
        self.drawing_update_timer.Start(30)

        self.SetupScrolling()

        self.Bind(EVT_PAINT, self.on_paint_handler)
        self.Bind(EVT_SIZE, self.on_size_handler)
        self.Bind(EVT_TIMER, self.on_timer_handler)
        self.Bind(EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.Bind(EVT_KEY_UP, self.key_up_handler)

        CallLater(200, self.SetFocus)

    # -----------------------------------------------------------------------

    # event_handlers
    def key_up_handler(self, event):
        keycode = event.GetUnicodeKey()
        print(keycode)
        if keycode == 90: #
            self.zoom = 1.0
            self.update_drawing()
        event.Skip()

    def on_timer_handler(self, event):
        self.update_drawing()
        event.Skip()

    def on_size_handler(self, event):
        self.w_w, self.w_h = self.GetClientSize()
        self.reset_drawing_base()
        event.Skip()

    def OnMouseWheel(self, event):
        m = GetMouseState()

        if m.ControlDown():
            delta = 0.1 * event.GetWheelRotation() / event.GetWheelDelta()
            self.zoom = max(1, self.zoom + delta)
            self.ScaleToFit()

        event.Skip()

    def on_paint_handler(self, event):
        dc = MemoryDC()
        dc.SelectObject(self.bitmap)
        dc.Clear()

        dc.SetBrush(Brush("WHITE"))
        dc.SetPen(Pen("BLACK", 2))
        dc.DrawRectangle(0, 0, self.i_w, self.i_h)
        #dc.SetBrush(Brush("LIGHT BLUE"))
        for c in self.showed_cells:
            #dc.SetBrush(Brush("LIGHT BLUE"))
            dc.DrawRectangle(c.top_x, c.top_y, c.width, c.height)
        dc.SetBrush(Brush("LIGHT BLUE"))
        for tool in self.tools:
            tool.draw(dc)
        self.image = Bitmap.ConvertToImage(self.bitmap)
        self.aspect = self.image.GetSize()[1] / self.image.GetSize()[0]
        # self.zoom = 1.0

        self.bmpImage.SetBitmap(self.bitmap)

        self.ScaleToFit()
        event.Skip()

    # -----------------------------------------------------------------------

    def reset_drawing_base(self):
        self.i_w = self.w_w
        # verify the image minimum needed width
        if self.w_w < self.min_needed_width:
            self.i_w = self.min_needed_width

        # verify the needed height to show all is_filtered tools
        max_cells_per_line = self.i_w * (1 - self.hor_total_free_space_min) // self.cell_width
        # TODO
        # needed_lines = ceil(len(self.filter) / max_cells_per_line)
        needed_lines = ceil(len(self.tools) / max_cells_per_line)
        min_needed_height = needed_lines * self.cell_height + needed_lines * self.vertical_gap + self.vertical_gap

        self.i_h = self.w_h if min_needed_height < self.w_h else min_needed_height

        if self.bitmap is None:
            self.bitmap = Bitmap(self.i_w, self.i_h)
        elif self.bitmap.Size != (self.i_w, self.i_h):
            self.bitmap = Bitmap(self.i_w, self.i_h)

        free_horizontal_space = self.i_w - (max_cells_per_line * self.cell_width)
        horizontal_gap = free_horizontal_space // max_cells_per_line

        cells_per_line = max_cells_per_line
        self.showed_cells.clear()

        for i in range(len(self.tools)):
            # waiting_cells_qty = len(self.tools) - i + 1
            # if waiting_cells_qty < max_cells_per_line:
            #    cells_per_line = waiting_cells_qty
            #    horizontal_gap = free_horizontal_space // cells_per_line

            l = i // cells_per_line
            c = i % cells_per_line

            x = c * self.cell_width + c * horizontal_gap + horizontal_gap // 2
            y = l * self.cell_height + l * self.vertical_gap + self.vertical_gap // 2

            cell = Cell(int(x), int(y), self.cell_width, self.cell_height, self.i_w, self.i_h)
            self.showed_cells.append(cell)

        for i in range(int(max_cells_per_line)):
            l = i // cells_per_line
            c = i % cells_per_line

            x = c * self.cell_width + c * horizontal_gap + horizontal_gap // 2
            y = self.i_h + 10

            cell = Cell(int(x), int(y), self.cell_width, self.cell_height, self.i_w + 5, self.i_h + 5)
            self.origin_cells.append(cell)

        self.set_cells_to_tools()

    def set_cells_to_tools(self):
        for t in self.tools:
            t.is_filtered = False
            for f in self.filter:
                for f_t in t.attributes["filter"]:
                    if f_t == f:
                        t.is_filtered = True
                        break
        i = 0
        for tool in self.tools:
            if tool.is_filtered:
                tool.cell = self.showed_cells[i]
                i = i + 1
            else:
                tool.cell = self.origin_cells[random.randint(0, len(self.origin_cells) - 1)]

    def update_drawing(self):
        self.Refresh()

    def set_tools(self, tools):
        self.tools = tools
        self.reset_drawing_base()

    def set_filter(self, filter):
        self.filter = filter
        self.reset_drawing_base()
        # for tool in self.tools:
        #    r = random.randint(0, len(self.origin_cells) - 1)
        #    tool.top_x = self.origin_cells[r].top_x
        #    tool.top_y = self.origin_cells[r].top_y

    def tools_sizes(self):
        pass

    def tools_positions(self):
        pass

    def ScaleToFit(self) -> None:
        if self.image:

            # get container (c) dimensions
            cw, ch = self.w_w, self.w_h  # self.GetSize()

            # calculate new (n) dimensions with same aspect ratio
            nw = cw
            nh = int(nw * self.aspect)

            # if new height is too large then recalculate sizes to fit
            if nh >= ch:
                nh = ch - 20
                nw = int(nh / self.aspect)

            # Apply zoom
            nh = int(nh * self.zoom)
            nw = int(nw * self.zoom)

            # scale the image to new dimensions and display
            image = self.image.Scale(nw, nh)
            self.bmpImage.SetBitmap(image.ConvertToBitmap())
            # self.Layout()

            if self.zoom > 1.0:
                self.ShowScrollBars = True
                self.SetupScrolling()
            else:
                self.ShowScrollBars = False
                self.SetupScrolling()
