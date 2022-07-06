# pip install pyqt6
# pip install pyqt-tools

import sys
import numpy as np
from PIL import Image
import scipy.ndimage as nd
from scipy import misc

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MainForm(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Picture Transformer'
        self.width = 500
        self.height = 400
        self.image = Image.fromarray(misc.ascent())
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        aboutAction = QAction("&Info",self)
        aboutAction.triggered.connect(self.popWindow)
        fileAction = QAction("&Save As...",self)
        fileAction.triggered.connect(self.saveFile)
        
        menubar = self.menuBar()
        fileOption = menubar.addMenu('&File')
        fileOption.addAction(fileAction)
        aboutOption = menubar.addMenu('&About')
        aboutOption.addAction(aboutAction)
        
        self.m = PlotCanvas(self, data=self.image, width=3.7, height=3.5)
        self.m.move(110,30)


        button = QPushButton('Upload Image', self)
        button.setToolTip('Upload Image')
        button.move(10,30)
        button.resize(90,30)
        button.clicked.connect(self.image_upload)

        buttonFlipR = QPushButton('Flip →', self)
        buttonFlipR.setToolTip('Flip image to the right')
        buttonFlipR.move(55,60)
        buttonFlipR.resize(45,30)
        buttonFlipR.clicked.connect(self.flipR)

        buttonFlipL = QPushButton('Flip ←', self)
        buttonFlipL.setToolTip('Flip image to the left')
        buttonFlipL.move(10,60)
        buttonFlipL.resize(45,30)
        buttonFlipL.clicked.connect(self.flipL)

        buttonMirH = QPushButton('Mirror -',self)
        buttonMirH.setToolTip('Mirror image horisontaly')
        buttonMirH.move(10,90)
        buttonMirH.resize(45,30)
        buttonMirH.clicked.connect(self.mirrorH)

        buttonMirV = QPushButton('Mirror |',self)
        buttonMirV.setToolTip('Mirror image verticaly')
        buttonMirV.move(55,90)
        buttonMirV.resize(45,30)
        buttonMirV.clicked.connect(self.mirrorV)


        line = QFrame(self)
        line.setGeometry(15,130,80,2)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        label = QLabel(self)
        label.setText("Choose a filter:")
        label.move(18,130)

        self.combo = QComboBox(self)
        self.combo.setFixedSize(90,20)
        self.combo.addItems(['gaussian_filter','prewitt','sobel','color inversion','gamma','single color'])
        self.combo.currentIndexChanged.connect(self.selectionChange)
        self.combo.move(10,160)

        self.spinbox = QDoubleSpinBox(self)
        self.spinbox.setValue(3)
        self.spinbox.move(50,185)
        self.spinbox.resize(50,20)
        
        self.spinlabel = QLabel(self)
        self.spinlabel.setText("Sigma:")
        self.spinlabel.setGeometry(12,185,40,20)

        self.radioStatus = "R"
        self.radio1 = QRadioButton("R",self)
        self.radio1.setChecked(True)
        self.radio1.move(10,180)
        self.radio1.toggled.connect(lambda: self.btnstate(self.radio1))
        self.radio1.hide()

        self.radio2 = QRadioButton("G",self)
        self.radio2.move(40,180)
        self.radio2.toggled.connect(lambda: self.btnstate(self.radio2))
        self.radio2.hide()

        self.radio3 = QRadioButton("B",self)
        self.radio3.move(70,180)
        self.radio3.toggled.connect(lambda: self.btnstate(self.radio3))
        self.radio3.hide()

        buttonApply = QPushButton('Apply', self)
        buttonApply.setToolTip('Apply filter to Image')
        buttonApply.move(10,210)
        buttonApply.resize(90,30)
        buttonApply.clicked.connect(self.transform)

        self.show()

    def image_upload(self):
        self.path, _ = QFileDialog.getOpenFileName(self, 'Open File', './', "Image (*.png *.jpg *jpeg)")
        if self.path:
            self.image = Image.open(self.path)
            self.m.data = self.image
            self.m.plot()

    def flipR(self):
        if self.image:
            matrix = np.array(self.image)
            matrix = np.rot90(matrix,3)
            self.image = Image.fromarray(matrix)
            self.m.data = Image.fromarray(matrix)
            self.m.plot()

    def flipL(self):
        if self.image:
            matrix = np.array(self.image)
            matrix = np.rot90(matrix)
            self.image = Image.fromarray(matrix)
            self.m.data = Image.fromarray(matrix)
            self.m.plot()

    def mirrorH(self):
        if self.image:
            matrix = np.array(self.image)
            matrix = np.flipud(matrix)
            self.image = Image.fromarray(matrix)
            self.m.data = Image.fromarray(matrix)
            self.m.plot()

    def mirrorV(self):
        if self.image:
            matrix = np.array(self.image)
            matrix = np.fliplr(matrix)
            self.image = Image.fromarray(matrix)
            self.m.data = Image.fromarray(matrix)
            self.m.plot()

    def selectionChange(self):
        transform = self.combo.currentText()
        if transform == "gaussian_filter":
            self.spinbox.show()
            self.spinbox.setValue(3)
            self.spinlabel.setText('Sigma:')
            self.spinlabel.show()
            self.radio1.hide()
            self.radio2.hide()
            self.radio3.hide()
        elif transform == "gamma":
            self.spinbox.setValue(1)
            self.spinbox.show()
            self.spinlabel.setText('Coef:')
            self.spinlabel.show()
            self.radio1.hide()
            self.radio2.hide()
            self.radio3.hide()
        elif transform == "single color":
            self.spinbox.hide()
            self.spinlabel.hide()
            self.radio1.show()
            self.radio2.show()
            self.radio3.show()
        else:
            self.spinbox.hide()
            self.spinlabel.hide()
            self.radio1.hide()
            self.radio2.hide()
            self.radio3.hide()

    def btnstate(self,b):
        if b.isChecked() == True:
            self.radioStatus = b.text()

    def transform(self):
        if self.image:
            transform = self.combo.currentText()
            if transform == "gaussian_filter":
                filter = nd.gaussian_filter(np.array(self.image),self.spinbox.value())
                self.image = Image.fromarray(filter)
                self.m.data = Image.fromarray(filter)
                self.m.plot()
            if transform == "prewitt":
                filter = nd.prewitt(np.array(self.image))
                self.image = Image.fromarray(filter)
                self.m.data = Image.fromarray(filter)
                self.m.plot()
            if transform == "sobel":
                filter = nd.sobel(np.array(self.image))
                self.image = Image.fromarray(filter)
                self.m.data = Image.fromarray(filter)
                self.m.plot()
            if transform == "color inversion":
                im_i = np.array(self.image)
                filter = 255 - im_i
                self.image = Image.fromarray(filter)
                self.m.data = Image.fromarray(filter)
                self.m.plot()
            if transform == "gamma":
                im = np.array(self.image)
                filter = 255.0 * (im / 255.0)**float(self.spinbox.value())
                self.image = Image.fromarray(np.uint8(filter))
                self.m.data = Image.fromarray(np.uint8(filter))
                self.m.plot()
            if transform == "single color":
                im = np.array(self.image)
                if len(im.shape)==3:
                    im_R = im.copy()

                    im_R[:, :, (1, 2)] = 0
                    im_G = im.copy()
                    im_G[:, :, (0, 2)] = 0
                    im_B = im.copy()
                    im_B[:, :, (0, 1)] = 0

                    #im_RGB = np.concatenate((im_R, im_G, im_B), axis=1)

                    if self.radioStatus == "R":
                        self.image = Image.fromarray(im_R)
                        self.m.data = Image.fromarray(im_R)
                        self.m.plot()
                    if self.radioStatus == "G":
                        self.image = Image.fromarray(im_G)
                        self.m.data = Image.fromarray(im_G)
                        self.m.plot()
                    if self.radioStatus == "B":
                        self.image = Image.fromarray(im_B)
                        self.m.data = Image.fromarray(im_B)
                        self.m.plot()
                else:
                    print('Only for RGB images!')


    def popWindow(self):
        self.form2 = QWidget()
        self.ui2 = Ui_Form()
        self.ui2.setupUi(self.form2)
        self.form2.show() 

    def saveFile(self):
        name = QFileDialog.getSaveFileName(self, 'Save File', "newFile", "Image (*.png *.jpg *jpeg)")
        self.image.save(name[0])


class Ui_Form(object):

    def setupUi(self, Form:QWidget):
        Form.setObjectName("Form")
        Form.setFixedSize(250, 100)
        Form.setWindowTitle("About")

        Form.label = QLabel(Form)
        Form.label.setText("Picture Transformer V 1.00")
        Form.label.setFont(QFont('Arial', 11))
        Form.label.move(30,30)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, data=None, width=3.5, height=3.5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.data = data
        self.axes.axis('off')
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()


    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if self.data:
            ax.imshow(self.data)
        ax.axis('off')
        self.draw()


app = QApplication(sys.argv)
window = MainForm()
app.exec()