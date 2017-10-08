from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import utils.ModelingFunctions as mf; reload(mf)

dialog = None

class CustomTool(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Custom Tools')
        #self.setFixedHeight(285)
        self.setFixedWidth(320)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowStaysOnTopHint)

        self.setLayout(QVBoxLayout())

        modelingToolSection = ToolCategory('MODELING')
        riggingToolSection = ToolCategory('RIGGING')

        button1 = QPushButton("Freeze Transforms")
        button1.clicked.connect(mf.freezeTransforms)
        button2 = QPushButton("Center Pivot")
        button2.clicked.connect(mf.centerPivot)
        button3 = QPushButton("Clear History")
        button3.clicked.connect(mf.clearHistory)
        button4 = QPushButton("Draw Quad Arrow")
        button4.clicked.connect(mf.createQuadArrow)
        button5 = QPushButton("Set Pivot To Origin")
        button5.clicked.connect(mf.setPivotToCenter)

        mirrorTool = MirrorTool()

        modelingToolSection.addWidget(button1)
        modelingToolSection.addWidget(button2)
        modelingToolSection.addWidget(button3)
        modelingToolSection.addWidget(button5)
        modelingToolSection.addWidget(mirrorTool)
        riggingToolSection.addWidget(button4)
        riggingToolSection.addWidget(JointPathTool())

        self.layout().addWidget(modelingToolSection)
        self.layout().addWidget(riggingToolSection)

    def mirrorSelected(self):
        mf.mirrorDuplicate(0)

class ToolCategory(QWidget):
    def __init__(self, name):
        QWidget.__init__(self)

        self.setLayout(QVBoxLayout())

        header_font = QFont()
        header_font.setBold(True)

        header_label = QLabel()
        header_label.setText("   " + name)
        header_label.setFont(header_font)
        header_label.setFrameStyle(QFrame.StyledPanel)

        self.header = QWidget()
        self.header.setLayout(QHBoxLayout())
        self.header.setFixedHeight(30)
        self.header.layout().addWidget(header_label)
        self.header.layout().setContentsMargins(0,0,0,0)

        header_style_sheet = "background-color: rgba(50, 84, 140, 255);\
                              color: rgba(255, 255, 255, 220);"
        header_label.setStyleSheet(header_style_sheet)

        self.layout().addWidget(self.header)

    def addWidget(self, new_widget):
        self.layout().addWidget(new_widget)

class MirrorTool(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.mirrorButton = QPushButton("Mirror Duplicate")
        self.mirrorButton.clicked.connect(self.mirrorSelected)
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.mirrorButton)
        axisLabel = QLabel('Axis:')
        axisLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.layout().addWidget(axisLabel)
        self.mirrorAxis = QComboBox()
        self.mirrorAxis.setFixedWidth(50)
        self.mirrorAxis.addItem('X')
        self.mirrorAxis.addItem('Y')
        self.mirrorAxis.addItem('Z')
        self.layout().addWidget(self.mirrorAxis)
        self.layout().setContentsMargins(0,0,0,0)

    def mirrorSelected(self):
        mf.mirrorDuplicate(self.mirrorAxis.currentIndex())

class JointPathTool(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.createButton = QPushButton("CreateJoints")
        self.createButton.clicked.connect(self.createJoints)
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.createButton)
        numberLabel = QLabel('Number of joints:')
        numberLabel.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.layout().addWidget(numberLabel)
        self.numberBox = QSpinBox()
        self.numberBox.setMinimum(0)
        self.numberBox.setValue(1)
        self.numberBox.setSingleStep(1)
        self.numberBox.setFixedWidth(50)
        self.layout().addWidget(self.numberBox)
        self.layout().setContentsMargins(0,0,0,0)

    def createJoints(self):
        mf.createJointsOnCurve(self.numberBox.value())

def create():
    global dialog
    if dialog is None:
        dialog = CustomTool()
    dialog.show()

def delete():
    global dialog
    if dialog is None:
        return

    dialog.deleteLater()
    dialog = None
