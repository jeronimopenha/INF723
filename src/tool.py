from wx import *


class Tool:
    def __init__(self, attributes: {}, x: int = 0, y: int = 0, line_color="BLACK", background_color="WHITE",
                 time_to_grow: int = 1000, timer_set: int = 20):
        self.BASE_SIZE = 50
        self.BASE_MOVE_STEP = 5

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

    def draw(self, dc) -> None:
        if self.move_to_cell():
            dc.SetPen(Pen(self.line_color, 1))
            dc.DrawRoundedRectangle(int(self.top_x), int(self.top_y), int(self.actual_width), int(self.actual_height),
                                    2)

    def move_to_cell(self):
        xc, yc = self.cell.top_x, self.cell.top_y
        xp, yp = self.top_x, self.top_y
        up_size=True
        if xp != xc or yp != yc:
            up_size = False
            x, y = self.calc_new_coords()

            if abs(x - xc) < self.BASE_MOVE_STEP:
                x = xc
            if abs(y - yc) < self.BASE_MOVE_STEP:
                y = yc
            self.top_x = x
            self.top_y = y

        self.update_size(up_size)
        if self.top_y < 0 or self.top_y > self.cell.y_l:
            return False
        return True

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

    def update_size(self, upsize) -> None:
        w_max = self.cell.width
        h_max = self.cell.height
        w_min = self.BASE_SIZE
        h_min = self.BASE_SIZE
        time_step = self.time_to_grow // self.timer_set
        w_step = w_max//w_min
        h_step = h_max // h_min

        if upsize:
            if self.actual_width < w_max:
                self.actual_width += w_step
            if self.actual_height < h_max:
                self.actual_height += h_step
            if self.actual_width >= w_max:
                self.actual_width = w_max
            if self.actual_height >= h_max:
                self.actual_height = h_max
        else:
            if self.actual_width > w_min:
                self.actual_width -= w_step
            if self.actual_height > h_min:
                self.actual_height -= h_step
            if self.actual_width <= w_min:
                self.actual_width = w_min
            if self.actual_height <= h_min:
                self.actual_height = h_min
