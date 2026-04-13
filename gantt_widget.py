from PyQt5.QtWidgets import QWidget, QScrollArea
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QRect

CELL_W = 36
ROW_H  = 34
HEADER_H = 24
LABEL_W  = 70

COLORS = [
    "#5b8dd9", "#d97b5b", "#5bbf8a", "#b07bd9",
    "#d9b05b", "#5bc0d9", "#d95b5b", "#7bbf5b",
]


class GanttCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._slots = []          # (name_or_None, start, end)
        self._row_order = []      # process names in appearance order
        self._color_map = {}
        self._color_idx = 0
        self._total_time = 0

    def clear(self):
        self._slots = []
        self._row_order = []
        self._color_map = {}
        self._color_idx = 0
        self._total_time = 0
        self._resize()
        self.update()

    def add_slot(self, process, start: int, end: int):
        name = process.get_name() if process else None
        if name and name not in self._color_map:
            self._color_map[name] = COLORS[self._color_idx % len(COLORS)]
            self._color_idx += 1
        if name and name not in self._row_order:
            self._row_order.append(name)
        self._slots.append((name, start, end))
        self._total_time = end
        self._resize()
        self.update()

    def _resize(self):
        rows = max(len(self._row_order), 1)
        w = LABEL_W + self._total_time * CELL_W + CELL_W
        h = HEADER_H + rows * ROW_H + 4
        self.setMinimumSize(max(w, 300), max(h, HEADER_H + ROW_H + 4))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), QColor("#ffffff"))

        if not self._row_order:
            p.setPen(QColor("#aaaaaa"))
            p.setFont(QFont("Arial", 10))
            p.drawText(self.rect(), Qt.AlignCenter, "Run a simulation to see the Gantt chart")
            return

        self._draw_header(p)
        self._draw_rows(p)
        self._draw_blocks(p)

    def _draw_header(self, p: QPainter):
        p.fillRect(0, 0, self.width(), HEADER_H, QColor("#f5f5f5"))
        p.setPen(QColor("#cccccc"))
        p.drawLine(0, HEADER_H - 1, self.width(), HEADER_H - 1)
        p.setFont(QFont("Arial", 8))
        p.setPen(QColor("#888888"))
        for t in range(self._total_time + 1):
            x = LABEL_W + t * CELL_W
            p.drawLine(x, HEADER_H - 5, x, HEADER_H)
            if t % 5 == 0 or t == 0:
                p.drawText(x - 12, 2, 24, HEADER_H - 6, Qt.AlignCenter, str(t))

    def _draw_rows(self, p: QPainter):
        for i, name in enumerate(self._row_order):
            y = HEADER_H + i * ROW_H
            bg = QColor("#fafafa") if i % 2 == 0 else QColor("#f2f2f2")
            p.fillRect(0, y, self.width(), ROW_H, bg)

            # label
            p.fillRect(0, y, LABEL_W, ROW_H, QColor("#f0f0f0"))
            p.setPen(QPen(QColor("#cccccc"), 0.5))
            p.drawLine(LABEL_W, y, LABEL_W, y + ROW_H)
            p.setPen(QColor("#333333"))
            p.setFont(QFont("Arial", 9))
            p.drawText(8, y, LABEL_W - 10, ROW_H, Qt.AlignVCenter | Qt.AlignLeft, name)

        # grid lines
        p.setPen(QPen(QColor("#e8e8e8"), 0.5))
        rows = len(self._row_order)
        for t in range(self._total_time + 1):
            x = LABEL_W + t * CELL_W
            p.drawLine(x, HEADER_H, x, HEADER_H + rows * ROW_H)

    def _draw_blocks(self, p: QPainter):
        p.setFont(QFont("Arial", 8, QFont.Bold))
        for name, start, end in self._slots:
            w = (end - start) * CELL_W
            x = LABEL_W + start * CELL_W

            if name is None:
                row = 0
                y = HEADER_H
                r = QRect(x + 1, y + 3, w - 2, ROW_H - 6)
                p.fillRect(r, QColor("#eeeeee"))
                p.setPen(QPen(QColor("#cccccc"), 0.5))
                p.drawRect(r)
                p.setPen(QColor("#aaaaaa"))
                p.drawText(r, Qt.AlignCenter, "idle")
            else:
                if name not in self._row_order:
                    continue
                row = self._row_order.index(name)
                y = HEADER_H + row * ROW_H
                color = QColor(self._color_map[name])
                r = QRect(x + 1, y + 3, w - 2, ROW_H - 6)
                light = QColor(color)
                light.setAlpha(80)
                p.fillRect(r, light)
                p.setPen(QPen(color, 1))
                p.drawRect(r)
                if w > 20:
                    p.setPen(color.darker(150))
                    p.drawText(r, Qt.AlignCenter, name)


class GanttChart(QScrollArea):
    """The class the controller and main window interact with."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._canvas = GanttCanvas()
        self.setWidget(self._canvas)
        self.setWidgetResizable(False)
        self.setMinimumHeight(140)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def clear(self):
        self._canvas.clear()

    def add_slot(self, process, start: int, end: int):
        self._canvas.add_slot(process, start, end)
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().maximum())