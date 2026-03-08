from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import resources

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 770)
        MainWindow.setMinimumSize(QSize(1280, 770))
        MainWindow.setMaximumSize(QSize(1280, 770))
        MainWindow.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        MainWindow.setWindowFlag(Qt.FramelessWindowHint)
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(-10, 40, 1321, 741))
        self.frame_3.setStyleSheet(u"#frame_3{\n\tborder:none;\n}")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget_1 = QWidget(self.frame_3)
        self.widget_1.setObjectName(u"widget_1")
        self.verticalLayout = QVBoxLayout(self.widget_1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.icon = QLabel(self.widget_1)
        self.icon.setObjectName(u"icon")
        self.icon.setPixmap(QPixmap(u":/420(1).png"))
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.icon)

        self.ivis = QLabel(self.widget_1)
        self.ivis.setObjectName(u"ivis")
        font = QFont()
        font.setFamilies([u"Poppins"])
        font.setPointSize(60)
        font.setBold(True)
        self.ivis.setFont(font)
        self.ivis.setStyleSheet(u"color: #27296c;")
        self.ivis.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.ivis)
        self.ivis.move(self.ivis.x(), self.ivis.y() + 300)

        self.ivis_word = QLabel(self.widget_1)
        self.ivis_word.setObjectName(u"ivis_word")
        self.ivis_word.setMinimumSize(QSize(653, 44))
        self.ivis_word.setMaximumSize(QSize(1000, 44))
        font1 = QFont()
        font1.setFamilies([u"Poppins"])
        font1.setPointSize(24)
        font1.setBold(True)
        self.ivis_word.setFont(font1)
        self.ivis_word.setStyleSheet(u"color: #27296c;")
        self.ivis_word.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.ivis_word)

        self.quote = QLabel(self.widget_1)
        self.quote.setObjectName(u"quote")
        self.quote.setMinimumSize(QSize(653, 28))
        self.quote.setMaximumSize(QSize(1000, 28))
        font2 = QFont()
        font2.setFamilies([u"Poppins"])
        font2.setPointSize(13)
        font2.setBold(False)
        font2.setItalic(True)
        self.quote.setFont(font2)
        self.quote.setStyleSheet(u"color: #27296c;")
        self.quote.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.verticalLayout.addWidget(self.quote)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.gridLayout.addWidget(self.widget_1, 0, 0, 1, 1)

        self.widget_2 = QWidget(self.frame_3)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(1300, 40))
        self.widget_2.setMaximumSize(QSize(1300, 45))
        self.widget_2.setStyleSheet(u"background-color: #27296c;")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.widget_2)
        self.label_5.setObjectName(u"label_5")
        font3 = QFont()
        font3.setFamilies([u"Poppins"])
        font3.setBold(True)
        font3.setItalic(False)
        self.label_5.setFont(font3)
        self.label_5.setStyleSheet(u"color: white;")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_5)

        self.horizontalSpacer = QSpacerItem(800, 19, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_7 = QLabel(self.widget_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font3)
        self.label_7.setStyleSheet(u"color: white;")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_7)

        self.gridLayout.addWidget(self.widget_2, 1, 0, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(30, 20, 240, 71))
        self.label_6.setPixmap(QPixmap(u":/240.png"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.icon.setText("")
        self.ivis.setText(QCoreApplication.translate("MainWindow", u"IVIS", None))
        self.ivis_word.setText(QCoreApplication.translate("MainWindow", u"                                         Intelligent Visual Inspection System", None))
        self.quote.setText(QCoreApplication.translate("MainWindow", u"                                                        Empowering Semiconductor Quality through Intelligent Detection", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Developed by FJMM for Fastech Synergy Philippines, Inc.", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"                \u00a9 2025", None))
        self.label_6.setText("")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.splash_done = False
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    def check_and_close():
        if getattr(app, 'splash_done', False):
            MainWindow.close()
            poller.stop()

    poller = QTimer()
    poller.timeout.connect(check_and_close)
    poller.start(120)

    sys.exit(app.exec())
