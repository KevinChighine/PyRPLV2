"""
A widget for the spectrum analyzer
"""
import logging
logger = logging.getLogger(name=__name__)
from qtpy import QtCore, QtWidgets
import pyqtgraph as pg
from time import time
import numpy as np
from .base_module_widget import ModuleWidget
from ..attribute_widgets import DataWidget
from ...errors import NotReadyError
from .acquisition_module_widget import AcquisitionModuleWidget


class BasebandAttributesWidget(QtWidgets.QWidget):
    def __init__(self, specan_widget):
        super(BasebandAttributesWidget, self).__init__()
        self.h_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.h_layout)
        aws = specan_widget.attribute_widgets

        self.v_layout1 = QtWidgets.QVBoxLayout()
        self.h_layout.addLayout(self.v_layout1)
        for name in ["display_input1_baseband", "display_input2_baseband"]:
            widget = aws[name]
            specan_widget.attribute_layout.removeWidget(widget)
            self.v_layout1.addWidget(widget)

        self.v_layout2 = QtWidgets.QVBoxLayout()
        self.h_layout.addLayout(self.v_layout2)
        for name in ["input1_baseband", "input2_baseband"]:
            widget = aws[name]
            specan_widget.attribute_layout.removeWidget(widget)
            self.v_layout2.addWidget(widget)

        self.v_layout3 = QtWidgets.QVBoxLayout()
        self.h_layout.addLayout(self.v_layout3)
        for name in ["display_cross_amplitude"]:#, "display_cross_phase"]:
            widget = aws[name]
            specan_widget.attribute_layout.removeWidget(widget)
            self.v_layout3.addWidget(widget)


class IqModeAttributesWidget(QtWidgets.QWidget):
    def __init__(self, specan_widget):
        super(IqModeAttributesWidget, self).__init__()
        self.h_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.h_layout)
        aws = specan_widget.attribute_widgets

        self.v_layout1 = QtWidgets.QVBoxLayout()
        self.h_layout.addLayout(self.v_layout1)
        for name in ["center", "input"]:
            widget = aws[name]
            specan_widget.attribute_layout.removeWidget(widget)
            self.v_layout1.addWidget(widget)


class OtherAttributesWidget(QtWidgets.QWidget):
    def __init__(self, specan_widget):
        super(OtherAttributesWidget, self).__init__()
        self.h_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.h_layout)
        aws = specan_widget.attribute_widgets

        self.v_layout1 = QtWidgets.QVBoxLayout()
        self.h_layout.addLayout(self.v_layout1)
        for name in ["baseband", "acbandwidth"]:
            widget = aws[name]
            specan_widget.attribute_layout.removeWidget(widget)
            self.v_layout1.addWidget(widget)

        self.v_layout2 = QtWidgets.QVBoxLayout()
        self.h_layout.addLayout(self.v_layout2)
        for name in ["span", "window"]:
            widget = aws[name]
            specan_widget.attribute_layout.removeWidget(widget)
            self.v_layout2.addWidget(widget)

        self.v_layout3 = QtWidgets.QVBoxLayout()
        self.h_layout.addLayout(self.v_layout3)
        for name in ["rbw", "display_unit"]:
            widget = aws[name]
            specan_widget.attribute_layout.removeWidget(widget)
            self.v_layout3.addWidget(widget)


class SpecAnWidget(AcquisitionModuleWidget):
    _display_max_frequency = 25  # max 25 Hz framerate
    def init_gui(self):
        """
        Sets up the gui.
        """
        self.ch_col = ('magenta', 'blue', 'green')
        self.last_data = None
        self.init_main_layout(orientation="vertical")
        #self.main_layout = QtWidgets.QVBoxLayout()
        self.module.__dict__['curve_name'] = 'pyrpl spectrum'
        self.init_attribute_layout()

        self.other_widget = OtherAttributesWidget(self)
        self.attribute_layout.addWidget(self.other_widget)

        self.iqmode_widget = IqModeAttributesWidget(self)
        self.attribute_layout.addWidget(self.iqmode_widget)

        self.baseband_widget = BasebandAttributesWidget(self)
        self.attribute_layout.addWidget(self.baseband_widget)


        self.button_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)
        # self.setWindowTitle("Spec. An.")
        #self.win = pg.GraphicsWindow(title="PSD")
        #self.main_layout.addWidget(self.win)

        self.win2 = DataWidget(title='Spectrum')
        self.main_layout.addWidget(self.win2)

        #self.plot_item = self.win.addPlot(title="PSD")
        #self.curve = self.plot_item.plot(pen=self.ch_col[0][0])

        #self.curve2 = self.plot_item.plot(pen=self.ch_col[1][0]) # input2
        # spectrum in
        # baseband
        #self.curve_cross = self.plot_item.plot(pen=self.ch_col[2][0]) #
        # curve for


        super(SpecAnWidget, self).init_gui()

        aws = self.attribute_widgets


        aws['display_input1_baseband'].setStyleSheet("color: %s" %
                                                   self.ch_col[0])
        aws['display_input2_baseband'].setStyleSheet("color: %s" %
                                                   self.ch_col[1])
        aws['display_cross_amplitude'].setStyleSheet("color: %s" %
                                                   self.ch_col[2])
        # Not sure why the stretch factors in button_layout are not good by
        # default...

        self.attribute_layout.addStretch(1)
        self.update_baseband_visibility()

    def update_attribute_by_name(self, name, new_value_list):
        super(SpecAnWidget, self).update_attribute_by_name(name, new_value_list)
        if name in ['running_state']:
            self.update_running_buttons()
        if name in ['baseband']:
            self.update_baseband_visibility()

    def update_baseband_visibility(self):
        self.baseband_widget.setEnabled(self.module.baseband)
        self.iqmode_widget.setEnabled(not self.module.baseband)


    #### def update_rbw_visibility(self):
    ####     self.attribute_widgets["rbw"].widget.setEnabled(not
    #### self.module.rbw_auto)

    def autoscale_x(self):
        """Autoscale pyqtgraph"""
        mini = self.module.frequencies[0]
        maxi = self.module.frequencies[-1]
        self.win2.setRange(xRange=[mini,
                                   maxi])
        # self.plot_item.autoRange()

    def unit_changed(self):
        self.display_curve(self.last_data)
        self.plot_item.autoRange()

    def run_continuous_clicked(self):
        """
        Toggles the button run_continuous to stop or vice versa and starts the acquisition timer
        """

        if str(self.button_continuous.text()).startswith("Run continuous"):
            self.module.continuous()
        else:
            self.module.pause()

    def run_single_clicked(self):
        if str(self.button_single.text()).startswith('Stop'):
            self.module.stop()
        else:
            self.module.single_async()

    def display_curve(self, datas):
        if datas is None:
            return
        x, y = datas

        arr = np.array((datas[0], datas[1][1]))
        self.win2._set_widget_value(datas)

        self.last_data = datas
        freqs = datas[0]
        to_units = lambda x:self.module.data_to_display_unit(x,
                                                  self.module._run_future.rbw)
        if not self.module.baseband: # iq mode, only 1 curve to display
            self.win2._set_widget_value((freqs, to_units(datas[1])))
        else: # baseband mode: data is (spec1, spec2, real(cross), imag(cross))
            spec1, spec2, cross_r, cross_i = datas[1]
            if not self.module.display_input1_baseband:
                spec1 = np.array([np.nan]*len(x))
            if not self.module.display_input2_baseband:
                spec2 = np.array([np.nan]*len(x))
            if not self.module.display_cross_amplitude:
                cross = np.array([np.nan]*len(x))
            else:
                cross = cross_r + 1j*cross_i
            data = (spec1, spec2, cross)
            self.win2._set_widget_value((freqs, data),
                                        transform_magnitude=to_units)
        self.update_current_average()

    def display_curve_old(self, datas):
        """
        Displays all active channels on the graph.
        """
        self.last_data = datas
        freqs = datas[0]
        to_units = lambda x:self.module.data_to_display_unit(x,
                                                  self.module._run_future.rbw)
        if not self.module.baseband: # baseband mode, only 1 curve to display
            self.curve.setData(freqs, to_units(datas[1]))
            self.curve.setVisible(True)
            self.curve2.setVisible(False)
            self.curve_cross.setVisible(False)
        else: # baseband mode: data is (spec1, spec2, real(cross), imag(cross))
            spec1, spec2, cross_r, cross_i = datas[1]
            self.curve.setData(freqs, to_units(spec1))
            self.curve.setVisible(self.module.display_input1_baseband)

            self.curve2.setData(freqs, to_units(spec2))
            self.curve2.setVisible(self.module.display_input2_baseband)

            cross = cross_r + 1j*cross_i
            cross_mod = abs(cross)
            self.curve_cross.setData(freqs, to_units(cross_mod))
            self.curve_cross.setVisible(self.module.display_cross_amplitude)

            # phase still needs to be implemented
        self.update_running_buttons()