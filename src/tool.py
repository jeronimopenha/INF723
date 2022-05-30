from wx import *
from math import ceil


class Tool:
    def __init__(self, attributes: {}, x: int = 0, y: int = 0, line_color="BLACK", background_color="WHITE",
                 time_to_grow: int = 1000, timer_set: int = 30):
        self.BASE_SIZE = 30
        self.BASE_MOVE_STEP = 5
        self.initialized = False

        self.attributes = attributes
        self.top_x = x
        self.top_y = y
        self.actual_width = self.BASE_SIZE
        self.actual_height = self.BASE_SIZE
        self.line_color = line_color
        self.background_color = background_color
        self.time_to_grow = time_to_grow
        self.timer_set = timer_set
        self.cell = None
        self.emphasis = 0
        self.is_filtered = False
        self.move_return = False
        self.sizing_return = False
        self.drawing = False

    def in_motion(self):
        return self.sizing_return or self.move_return or self.drawing

    def draw(self, dc) -> None:
        if True:
            if True:
                dc.SetPen(Pen(self.line_color, 1))
                dc.DrawRoundedRectangle(int(self.top_x), int(self.top_y), int(self.actual_width),
                                        int(self.actual_height),
                                        2)
            self.drawing = False

    def move_to_cell(self):
        xc, yc = self.cell.top_x, self.cell.top_y
        xp, yp = self.top_x, self.top_y
        in_movement = False
        upsize = True
        if yc == self.cell.y_l and not self.initialized:
            x = xc
            y = yc
            self.top_x = x
            self.top_y = y
            self.initialized = True
            return
        elif xp != xc or yp != yc:
            x, y = self.calc_new_coords()

            if abs(x - xc) < self.BASE_MOVE_STEP:
                x = xc
            if abs(y - yc) < self.BASE_MOVE_STEP:
                y = yc
            self.top_x = x
            self.top_y = y
            in_movement = True
            upsize = False

        self.move_return = in_movement
        if in_movement:
            self.drawing = True
        if self.top_y < 0 or self.top_y > self.cell.y_l:
            upsize = False
        self.update_size(upsize)

    def calc_new_coords(self) -> (int, int):
        y_l = self.cell.y_l
        xp, yp = self.top_x, y_l - self.top_y
        xc, yc = self.cell.top_x, y_l - self.cell.top_y
        x = xp
        y = yp
        dx = (xp - xc)
        dy = (yp - yc)
        if dx != 0:
            a = dy / dx
            if dx > 0:
                x = x - self.BASE_MOVE_STEP
            else:
                x = x + self.BASE_MOVE_STEP
            y = (a * x) + (a * xp * -1) + yp
            y = round(y)
        else:
            if dy > 0:
                y = y - self.BASE_MOVE_STEP
            else:
                y = y + self.BASE_MOVE_STEP
        return x, y_l - y

    def update_size(self, upsize:bool) -> None:
        w_max = self.cell.width
        h_max = self.cell.height
        w_min = self.BASE_SIZE
        h_min = self.BASE_SIZE
        time_step = ceil(self.time_to_grow / self.timer_set)
        w_step = ceil((w_max - w_min) / time_step)
        h_step = ceil((h_max - h_min) / time_step)

        sizing = False
        if upsize:
            if self.actual_width < w_max:
                self.actual_width += w_step
                sizing = True
            if self.actual_height < h_max:
                self.actual_height += h_step
                sizing = True
            if self.actual_width > w_max:
                self.actual_width = w_max
                sizing = True
            if self.actual_height > h_max:
                self.actual_height = h_max
                sizing = True
        else:
            if self.actual_width > w_min:
                self.actual_width -= w_step
                sizing = True
            if self.actual_height > h_min:
                self.actual_height -= h_step
                sizing = True
            if self.actual_width < w_min:
                self.actual_width = w_min
                sizing = True
            if self.actual_height < h_min:
                self.actual_height = h_min
                sizing = True
        self.sizing_return = sizing
        if sizing:
            self.drawing = True
