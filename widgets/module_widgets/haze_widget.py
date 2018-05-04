"""
A widget for the haze modules
"""
from .base_module_widget import ModuleWidget

from qtpy import QtCore, QtWidgets
import pyqtgraph as pg

class HazeWidget(ModuleWidget):


    def init_gui(self):
        self.init_main_layout(orientation="vertical")
        #self.main_layout = QtWidgets.QVBoxLayout()
        #self.setLayout(self.main_layout)
        self.init_attribute_layout()
        for prop in ['p']: #, 'd']:
            self.attribute_widgets[prop].widget.set_log_increment()
        # can't avoid timer to update ival

        # self.timer_ival = QtCore.QTimer()
        # self.timer_ival.setInterval(1000)
        # self.timer_ival.timeout.connect(self.update_ival)
        # self.timer_ival.start()

        #self.attribute_layout.addStretch(1)
        #tailLene1 =100
        #tailLene2 =140
        #tailWidthe=2
        #headLens=40
        #teta1=15
        #teta2=teta1+90
        #self.setWindowTitle("Axis")
        #self.win = pg.GraphicsWindow(title="Axis")
        #self.plot_item = self.win.addPlot(title="Axis")
        #self.plot_item.showGrid(x=True, y=True)
        #self.main_layout.addWidget(self.win, stretch=1)

        # p = self.win.addPlot(row=0, col=0)
        #e1 = pg.ArrowItem(angle=-teta1, tipAngle=10, baseAngle=0, headLen=headLens, tailLen=tailLene1-headLens, tailWidth=tailWidthe, pen=None, brush='w')
        #e2 = pg.ArrowItem(angle=-teta2, tipAngle=10, baseAngle=0, headLen=headLens, tailLen=tailLene2-headLens, tailWidth=tailWidthe, pen=None, brush='w')

        #e1.setPos(0,0)
        #e2.setPos(0,0)
        #self.plot_item.addItem(e1)
        #self.plot_item.addItem(e2)
