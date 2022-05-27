import math
import wx


class Tool:
    def __init__(self, attributes: {}, x_m: int = 0, y_m: int = 0, color="BLACK",
                 actual_size: int = 40, final_size: int = 40, time_to_grow: int = 5000, timer_set: int = 1000):
        self.attributes = attributes
        self.x_m = x_m
        self.y_m = y_m
        self.x = 0
        self.y = 0
        self.grow_times = math.ceil(time_to_grow / timer_set)
        self.actual_size = actual_size
        self.final_size = final_size
        self.size_step = math.ceil((final_size - actual_size) / self.grow_times)
        self.color = color

    def draw(self, dc) -> None:
        dc.SetPen(wx.Pen(self.color, 1))
        dc.DrawRoundedRectangle(int(self.x), int(self.y), int(self.actual_size), int(self.actual_size), 2)

    def calc_vectors(self, tools, i: int) -> (int, int):
        dx = dy = 0
        for idx in range(len(tools)):
            if idx == i: continue
            dx = dx +  self.x - tools[idx].x
            dy = dy +  (self.y_m - self.y) - (self.y_m - tools[idx].y)
        return dx, dy

    def calc_new_coords(self, dx: int, dy: int) -> (int, int):
        x = y = 0
        if (self.x - dx) != 0:
            a = (self.y_m - self.y - dy) / (self.x - dx)

            if dx >= 0:
                x = self.x + 1
            else:
                x = self.x - 1
            y = (a * x) + (-1 * a * self.x) + self.y_m - self.y
        else:
            if dy >= 0:
                y = self.y_m - self.y + 1
            else:
                y = self.y_m - self.y - 1
            x = self.x
        return x, self.y_m - round(y)

    def move(self, tools, i: int) -> None:
        dx, dy = self.calc_vectors(tools, i)
        x, y = self.calc_new_coords(dx, dy)
        self.update_size()

        if x < 0:
            x = 0
        elif (x + self.actual_size) > self.x_m:
            x = self.x_m - self.actual_size

        if y < 0:
            y = 0
        elif (y + self.actual_size) > self.y_m:
            y = self.y_m - self.actual_size
        self.x, self.y = x, y

    def update_size(self) -> None:
        if self.x < 0: self.x = 0
        if self.y < 0: self.y = 0
        if (self.x + self.actual_size) > self.x_m: self.x = self.x_m - self.actual_size
        if (self.y + self.actual_size) > self.y_m: self.y = self.y_m - self.actual_size

        if self.actual_size < self.final_size:
            self.actual_size = self.actual_size + self.size_step
            if self.actual_size > self.final_size:
                self.actual_size = self.final_size
        elif self.actual_size > self.final_size:
            self.actual_size = self.actual_size - self.size_step
            if self.actual_size < self.final_size:
                self.actual_size = self.final_size
