#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2023-09-18 15:22
# @File: main.py
# @Author: YeHwong
# @Email: 598318610@qq.com
# @Version ：1.0.0

import csv, random, sys, os, time, serial, pyqtgraph as pg
from serial.tools import list_ports
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel, QMessageBox
from DaqUI import Ui_MainWindow
from LogSet import Logger


class DAQGraph(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DAQGraph, self).__init__()
        self.port_timer = QTimer(self)
        self.acq_timer = QTimer(self)
        self.send_data_type = 'HEX'
        self.ser = serial.Serial()
        self.pen_color = ''
        self.time_gap = 0.1
        self.index = 0
        self.com_dict = {}
        self.imax = 0.1
        self.data_list = []
        self.time_list = []
        self.daq_log = Logger(base_dir='./DAQ_LOG', level='debug').my_logger
        self.setupUi(self)
        self.com_status = QLabel('串口已关闭')
        self.plot_plt = pg.PlotWidget()
        self.initUI()
        self.port_timer.timeout.connect(self.receive_data)
        self.check_port()
        self.open_close_port()

    def initUI(self):
        self.setWindowTitle('电流采集卡监控')
        self.startButton.clicked.connect(self.start_acq)
        self.refreshButton.clicked.connect(self.check_port)
        self.openButton.clicked.connect(self.open_close_port)
        self.saveButton.clicked.connect(self.clear_plot)
        self.lcdNumber.setSmallDecimalPoint(True)
        self.statusbar.showMessage('实时更新的信息', 0)
        self.statusbar.addPermanentWidget((self.com_status), stretch=0)
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'd')
        self.plot_plt.showGrid(x=True, y=True)
        self.plot_layout.addWidget(self.plot_plt)
        self.plot_plt.setYRange(100, 0)

    def start_acq(self):
        if self.startButton.text() == '开始采集':
            self.index = 1
            self.data_list = []
            self.time_list = []
            self.pen_color = random_color()
            self.acq_timer.timeout.connect(self.get_value)
            self.acq_timer.start(self.time_gap * 1000 - 55)
            self.startButton.setText('停止采集')
            self.saveButton.setEnabled(False)
            self.statusbar.showMessage(f"正在采集{self.comboBox_2.currentText()}", 0)
        else:
            if self.startButton.text() == '停止采集':
                self.acq_timer.stop()
                self.startButton.setText('开始采集')
                self.saveButton.setEnabled(True)
                self.save_data()

    def clear_plot(self):
        self.statusbar.showMessage('正在清除数据，请等待！', 0)
        self.saveButton.setEnabled(False)
        self.lcdNumber.display(0)
        self.plot_plt.clearPlots()
        self.saveButton.setEnabled(True)
        self.statusbar.showMessage('数据清除完成！', 0)

    def get_value(self):
        acq_param = ''
        value = None
        if self.comboBox_2.currentIndex() == 0:
            acq_param = '100300040001C68A'
        else:
            if self.comboBox_2.currentIndex() == 1:
                acq_param = '100300050001974A'
            else:
                if self.comboBox_2.currentIndex() == 2:
                    acq_param = '020300040001C5F8'
                else:
                    self.ser.isOpen() or self.open_close_port()
        receive_data = self.send_data(acq_param)
        if receive_data:
            value = self.dataParse(receive_data)
            self.lcdNumber.display(value)
            self.time_list.append(self.index * self.time_gap)
            self.data_list.append(value)
            self.daq_log.info(f"Get index:{self.index} Value:{value}")
            self.plot_plt.plot().setData((self.time_list), (self.data_list), pen=(self.pen_color))
            self.index += 1
        return value

    def check_port(self):
        port_list = list(list_ports.comports())
        for i in port_list:
            self.daq_log.debug('序号：%s   值：%s' % (port_list.index(i) + 1, i))

        self.comboBox_1.clear()
        for port in port_list:
            self.com_dict['%s' % port[0]] = '%s' % port[1]
            self.comboBox_1.addItem(port[0])

        if len(self.com_dict) == 0:
            self.statusbar.showMessage('无串口')
            self.daq_log.warn('未找到串口！！！')
        else:
            self.statusbar.showMessage(f"串口已刷新，找到{len(self.com_dict)}个串口")

    def open_close_port(self):
        print('按键状态：', self.openButton.text())
        if self.openButton.text() == '打开串口':
            self.ser.port = self.comboBox_1.currentText()
            self.ser.baudrate = 9600
            self.ser.bytesize = 8
            self.ser.parity = 'N'
            self.ser.stopbits = 1
            self.ser.timeout = 1
            self.ser.write_timeout = 0.5
            self.ser.inter_byte_timeout = 0.1
            try:
                self.ser.open()
            except Exception as e:
                try:
                    self.daq_log.info(f"port Error:{str(e)}")
                    self.statusbar.showMessage('串口状态：异常' + self.ser.name)
                finally:
                    e = None
                    del e

            if self.ser.isOpen():
                self.daq_log.info(f"串口打开正常：{self.ser.name}")
                self.statusbar.showMessage('串口状态：已打开' + self.ser.name)
                self.com_status.setText(f"{self.ser.name}已打开")
                self.openButton.setText('关闭串口')
                self.startButton.setEnabled(True)
        elif self.openButton.text() == '关闭串口':
            self.port_timer.stop()
            try:
                self.ser.close()
            except Exception as e:
                try:
                    self.log_print.error(e)
                finally:
                    e = None
                    del e

            if not self.ser.isOpen():
                self.statusbar.showMessage('串口状态：关闭' + self.ser.name)
                self.com_status.setText('串口已关闭')
                self.openButton.setText('打开串口')

    def receive_data(self):
        # TODO --->接收串口数据
        self.data_now = ""
        try:
            num = self.ser.inWaiting()
            if num:
                self.thread().msleep(20)
                while self.ser.inWaiting() > num > 0:
                    num = self.ser.inWaiting()
                    self.log_print.debug('-------------------警告：数据缺失--------------------num:' + str(num))
                    self.thread().msleep(30)
                    self.log_print.debug('-------------------警告：数据缺失--------------------' + str(self.ser.inWaiting()))
                else:
                    if num == self.ser.inWaiting() and num:
                        data = self.ser.read(num)
                        # hex显示
                        if self.hex_check.isChecked():
                            out_s = ''
                            for i in range(0, len(data)):
                                out_s = out_s + '{:02X}'.format(data[i]) + ' '
                            self.daq_log.info("[{0}]接收<---:{1}".format(0, out_s))
                            self.data_now = out_s
                        else:
                            # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                            self.daq_log.info("[{0}]接收<---:{1}".format(0, data.decode('gbk') + '\n'))

        except Exception as e:
            print(e)
        return self.data_now

    def send_data(self, input_data):
        input_s = ''
        acq_data = ''
        if self.ser.isOpen():
            self.ser.setRTS(0)
            if input_data != '':
                if self.send_data_type == 'HEX':
                    input_s = input_data.strip()
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(self, 'wrong data', '请输入十六进制数据，以空格分开!')
                            self.daq_log.warn('请输入十六进制数据，以空格分开!')
                            return
                        else:
                            input_s = input_s[2:].strip()
                            send_list.append(num)

                    input_s = bytes(send_list)
                    ips = ''
                    for i in range(0, len(input_s)):
                        ips = ips + '{:02X}'.format(input_s[i]) + ' '

                    ips = '发送--->:{}'.format(str(ips))
                    self.daq_log.debug(ips)
                else:
                    if self.send_data_type == 'ASCII':
                        input_s = (input_data + '\r\n').encode('utf-8')
                        self.daq_log.info(input_s)
                    else:
                        if self.send_data_type == 'BYTES':
                            input_s = input_data
                        try:
                            self.ser.reset_input_buffer()
                            num = self.ser.write(input_s)
                            time.sleep(0.04)
                            acq_data = self.receive_data()
                        except Exception as e:
                            try:
                                print(e)
                                self.daq_log.error(e)
                            finally:
                                e = None
                                del e

        else:
            QMessageBox.critical(self, 'port Error', '此串口未打开！')
            self.daq_log.warn('串口未打开!')
            self.start_acq()
        return acq_data

    def save_data(self):
        file_dir = './数据保存/'
        file_path = f"{file_dir}{self.comboBox_2.currentText()}.csv"
        if not os.path.exists(file_dir):
            os.makedirs(file_dir, exist_ok=True)
        with open(file_path, 'a+', newline='', encoding='UTF-8') as (csv_file):
            writer = csv.writer(csv_file)
            if not os.path.exists(file_path):
                self.time_list.insert(0, '时间')
            self.data_list.insert(0, f"{self.comboBox_2.currentText()}")
            writer.writerow(self.time_list)
            writer.writerow(self.data_list)
        self.statusbar.showMessage(f"数据保存完成:{file_path}")

    def dataParse(self, input_bytes):
        input_code = int.from_bytes(input_bytes, byteorder='big', signed=False)
        cmd, payload = divmod(input_code >> 16, 65536)
        spots_value = payload * self.imax
        spots_value = round(spots_value, 1)
        return spots_value


def random_color():
    colorArr = [
     "'1'", "'2'", "'3'", "'4'", "'5'", "'6'", "'7'", "'8'", "'9'",
     "'A'", "'B'", "'C'", "'D'", "'E'"]
    color = ''
    for i in range(6):
        color += colorArr[random.randint(0, 13)]

    return '#' + color


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myGraph = DAQGraph()
    myGraph.show()
    sys.exit(app.exec_())
