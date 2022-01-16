from PyQt5.QtWidgets import *
from PyQt5.QtGui  import  QIcon , QFont 
import sys
from test import testPhoto

class one(QDialog):
    def __init__(self):
        super().__init__()
        self.fname = None
        self.setWindowTitle('Covid19 Detector')
        self.setWindowIcon(QIcon('detective1.png'))
        self.setGeometry(350,100,500,240)
        self.initwindow()
        self.show()
    def initwindow(self):
        self.vbox=QVBoxLayout()
        self.hbox=QHBoxLayout()
        self.hbox_2=QHBoxLayout()
        self.vbox.setContentsMargins(30,30,30,10)

        #---------------------------------
        label=QLabel('Select a lung x-ray image to analyse : ')
        label.setFont(QFont('bold',11))
  
        #------------------ photo and upload button ------------------------------
        self.hbox.setContentsMargins(10,50,30,30)
        uploadbutton=QPushButton('Upload')
        uploadbutton.setStyleSheet('background-color:grey;max-width:140px;height:25px;text-align:center;margin-left:15px;margin-bottom:10px')
        uploadbutton.clicked.connect(self.upload)
        self.hbox.addWidget(uploadbutton)


        analyseButton=QPushButton('Analyse')
        analyseButton.setStyleSheet('background-color:green;max-width:140px;height:25px;text-align:center;margin-left:15px;margin-bottom:10px')
        analyseButton.clicked.connect(self.analyse)
        self.hbox.addWidget(analyseButton)

        self.label2=QLabel('')
        self.label2.setStyleSheet('color: green')
        self.label2.setFont(QFont('ink free',12))

        self.vbox.addWidget(label)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.label2)
        # self.vbox.addWidget(self.label3)

        self.setLayout(self.vbox)

    def upload(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', 
   '',"Image files (*.jpg *.png *.jpeg *.gif)")[0]
        self.label2.setText(self.fname)

    def analyse(self):
        if(self.fname != None):
            result = testPhoto(self.fname)
            if(result['covid'] > result['normal']):
                self.label2.setText("Patient result: "+"positive (covid19)" + str(result['covid']) + ' %|| ' + str(result['normal']))
                self.label2.setStyleSheet('color: red')
            else :
                self.label2.setText("Type of text: "+"negative (ok)")
                self.label2.setStyleSheet('color: green')

app = QApplication(sys.argv)

win=one()
sys.exit(app.exec_())
