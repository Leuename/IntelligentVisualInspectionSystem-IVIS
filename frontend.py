"""
Purpose: Houses the auto-generated PyQt6 layout classes defining the visual structure of the IVIS application.
Classes:
- Ui_MainWindow(object): Translates Qt Designer UI properties to fully-functional PyQt6 widgets and geometries.
Functions/Methods:
- Ui_MainWindow.setupUi: Generates all structural UI elements (frames, buttons, placeholders, sizes) precisely.
- Ui_MainWindow.retranslateUi: Configures the texts, tooltips, and translations for all UI interactables.
Workflows/Interactions:
- Completely static definition. Used exclusively by `backend.py` via instantiation to render the core visual interface.
"""
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import resources

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(2080, 1098)
        MainWindow.setMinimumSize(QSize(2080, 1090))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(2080, 1090))
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(-10, -10, 1941, 1051))
        self.frame.setStyleSheet(u"#frame{\n"
"	background-color:white;\n"
"	 border-top: none;\n"
"}")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 101))
        self.widget.setStyleSheet(u"background-color: #27296c;")
        self.gridLayout_8 = QGridLayout(self.widget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_23 = QLabel(self.widget)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setPixmap(QPixmap(u":/white_logo.png"))

        self.gridLayout_8.addWidget(self.label_23, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.label_24 = QLabel(self.widget)
        self.label_24.setObjectName(u"label_24")
        font = QFont()
        font.setFamilies([u"Poppins"])
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet(u"color:white;")
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_24, 0, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 0, 3, 1, 1)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.gridLayout_9 = QGridLayout(self.widget_4)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.close = QPushButton(self.widget_4)
        self.close.setObjectName(u"close")
        self.close.setMinimumSize(QSize(25, 25))
        self.close.setMaximumSize(QSize(25, 25))
        self.close.setStyleSheet(u"border:none;\n"
"")
        icon = QIcon()
        icon.addFile(u":/close_button_white.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.close.setIcon(icon)
        self.close.setIconSize(QSize(18, 18))

        self.gridLayout_9.addWidget(self.close, 0, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_3, 1, 1, 1, 1)

        self.minimize = QPushButton(self.widget_4)
        self.minimize.setObjectName(u"minimize")
        self.minimize.setMinimumSize(QSize(25, 25))
        self.minimize.setMaximumSize(QSize(25, 25))
        self.minimize.setStyleSheet(u"border:none;\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/minimize_whitepng.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimize.setIcon(icon1)
        self.minimize.setIconSize(QSize(18, 18))

        self.gridLayout_9.addWidget(self.minimize, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.widget_4, 0, 4, 1, 1)


        self.gridLayout_12.addWidget(self.widget, 0, 0, 1, 2)

        self.strip = QWidget(self.frame)
        self.strip.setObjectName(u"strip")
        self.strip.setMinimumSize(QSize(740, 350))
        self.strip.setMaximumSize(QSize(740, 16777215))
        self.strip.setStyleSheet(u"#strip{\n"
"    border-left: 4px solid #27296c;\n"
"    border-right: 4px solid #27296c;\n"
"    border-bottom: 5px solid #27296c;\n"
"    border-top: none;\n"
"    border-radius: 4px;\n"
"    background: white;\n"
"}\n"
"")
        self.verticalLayout_4 = QVBoxLayout(self.strip)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, -1, -1)
        self.current_qlabel = QLabel(self.strip)
        self.current_qlabel.setObjectName(u"current_qlabel")
        self.current_qlabel.setMinimumSize(QSize(750, 40))
        self.current_qlabel.setMaximumSize(QSize(750, 50))
        font1 = QFont()
        font1.setFamilies([u"Poppins"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.current_qlabel.setFont(font1)
        self.current_qlabel.setStyleSheet(u"#current_qlabel{\n"
"        background-color: #27296c;   \n"
"        color: white;\n"
"        font-weight: bold;\n"
"        font-size: 14pt;\n"
"        padding: 6px 10px;\n"
"        border: none;\n"
"        border-bottom: none;         \n"
"        border-top-left-radius: 1px;\n"
"        border-top-right-radius: 1px;\n"
"		border-radius:60px;\n"
"}\n"
"\n"
"")
        self.current_qlabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_4.addWidget(self.current_qlabel)

        self.widget_23 = QWidget(self.strip)
        self.widget_23.setObjectName(u"widget_23")
        self.widget_23.setMinimumSize(QSize(0, 0))
        self.widget_23.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_11 = QGridLayout(self.widget_23)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.widget_68 = QWidget(self.widget_23)
        self.widget_68.setObjectName(u"widget_68")
        self.widget_68.setMinimumSize(QSize(250, 30))
        self.widget_68.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_20 = QHBoxLayout(self.widget_68)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(-1, 0, 0, 0)
        self.label_78 = QLabel(self.widget_68)
        self.label_78.setObjectName(u"label_78")
        self.label_78.setMinimumSize(QSize(100, 30))
        self.label_78.setMaximumSize(QSize(100, 30))
        font2 = QFont()
        font2.setFamilies([u"Poppins"])
        font2.setPointSize(15)
        font2.setBold(True)
        self.label_78.setFont(font2)

        self.horizontalLayout_20.addWidget(self.label_78)

        self.operator_lineEdit = QLineEdit(self.widget_68)
        self.operator_lineEdit.setObjectName(u"operator_lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.operator_lineEdit.sizePolicy().hasHeightForWidth())
        self.operator_lineEdit.setSizePolicy(sizePolicy)
        self.operator_lineEdit.setMinimumSize(QSize(167, 30))
        self.operator_lineEdit.setMaximumSize(QSize(16777215, 30))
        font3 = QFont()
        font3.setFamilies([u"Poppins"])
        font3.setPointSize(12)
        self.operator_lineEdit.setFont(font3)

        self.horizontalLayout_20.addWidget(self.operator_lineEdit)


        self.gridLayout_11.addWidget(self.widget_68, 2, 0, 1, 1)

        self.widget_69 = QWidget(self.widget_23)
        self.widget_69.setObjectName(u"widget_69")
        self.widget_69.setMinimumSize(QSize(0, 0))
        self.widget_69.setMaximumSize(QSize(16777215, 70))
        self.verticalLayout_15 = QVBoxLayout(self.widget_69)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.widget_70 = QWidget(self.widget_69)
        self.widget_70.setObjectName(u"widget_70")
        self.widget_70.setMinimumSize(QSize(0, 0))
        self.widget_70.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_35 = QHBoxLayout(self.widget_70)
        self.horizontalLayout_35.setSpacing(0)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(9, 0, 0, 0)
        self.label_82 = QLabel(self.widget_70)
        self.label_82.setObjectName(u"label_82")
        self.label_82.setMinimumSize(QSize(120, 0))
        self.label_82.setMaximumSize(QSize(120, 16777215))
        self.label_82.setFont(font2)

        self.horizontalLayout_35.addWidget(self.label_82)

        self.good_unit_label = QLabel(self.widget_70)
        self.good_unit_label.setObjectName(u"good_unit_label")
        self.good_unit_label.setMinimumSize(QSize(0, 0))
        self.good_unit_label.setMaximumSize(QSize(16777215, 16777215))
        self.good_unit_label.setFont(font3)
        self.good_unit_label.setMargin(-1)
        self.good_unit_label.setIndent(-3)

        self.horizontalLayout_35.addWidget(self.good_unit_label)


        self.verticalLayout_15.addWidget(self.widget_70)

        self.widget_71 = QWidget(self.widget_69)
        self.widget_71.setObjectName(u"widget_71")
        self.widget_71.setMinimumSize(QSize(0, 0))
        self.widget_71.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_26 = QHBoxLayout(self.widget_71)
        self.horizontalLayout_26.setSpacing(0)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(-1, 0, 0, 0)
        self.label_73 = QLabel(self.widget_71)
        self.label_73.setObjectName(u"label_73")
        self.label_73.setMinimumSize(QSize(110, 0))
        self.label_73.setMaximumSize(QSize(110, 16777215))
        self.label_73.setFont(font2)

        self.horizontalLayout_26.addWidget(self.label_73)

        self.bad_unit_label_2 = QLabel(self.widget_71)
        self.bad_unit_label_2.setObjectName(u"bad_unit_label_2")
        self.bad_unit_label_2.setMinimumSize(QSize(0, 0))
        self.bad_unit_label_2.setMaximumSize(QSize(16777215, 16777215))
        self.bad_unit_label_2.setFont(font3)
        self.bad_unit_label_2.setMargin(-1)
        self.bad_unit_label_2.setIndent(-3)

        self.horizontalLayout_26.addWidget(self.bad_unit_label_2)


        self.verticalLayout_15.addWidget(self.widget_71)


        self.gridLayout_11.addWidget(self.widget_69, 1, 0, 1, 1)

        self.widget_72 = QWidget(self.widget_23)
        self.widget_72.setObjectName(u"widget_72")
        self.widget_72.setMinimumSize(QSize(0, 0))
        self.widget_72.setMaximumSize(QSize(16777215, 70))
        self.verticalLayout_12 = QVBoxLayout(self.widget_72)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.widget_73 = QWidget(self.widget_72)
        self.widget_73.setObjectName(u"widget_73")
        self.widget_73.setMinimumSize(QSize(0, 0))
        self.widget_73.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_27 = QHBoxLayout(self.widget_73)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(-1, 0, 0, 0)
        self.label_74 = QLabel(self.widget_73)
        self.label_74.setObjectName(u"label_74")
        self.label_74.setMinimumSize(QSize(0, 0))
        self.label_74.setMaximumSize(QSize(16777215, 16777215))
        self.label_74.setFont(font2)

        self.horizontalLayout_27.addWidget(self.label_74)

        self.magazine_to = QLineEdit(self.widget_73)
        self.magazine_to.setObjectName(u"magazine_to")
        self.magazine_to.setMinimumSize(QSize(0, 0))
        self.magazine_to.setMaximumSize(QSize(16777215, 16777215))
        self.magazine_to.setFont(font3)

        self.horizontalLayout_27.addWidget(self.magazine_to)


        self.verticalLayout_12.addWidget(self.widget_73)

        self.widget_74 = QWidget(self.widget_72)
        self.widget_74.setObjectName(u"widget_74")
        self.widget_74.setMinimumSize(QSize(250, 30))
        self.widget_74.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_36 = QHBoxLayout(self.widget_74)
        self.horizontalLayout_36.setSpacing(0)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(-1, 0, 0, 0)
        self.label_83 = QLabel(self.widget_74)
        self.label_83.setObjectName(u"label_83")
        self.label_83.setMinimumSize(QSize(90, 30))
        self.label_83.setMaximumSize(QSize(180, 30))
        self.label_83.setFont(font2)

        self.horizontalLayout_36.addWidget(self.label_83)

        self.magazine_from = QLineEdit(self.widget_74)
        self.magazine_from.setObjectName(u"magazine_from")
        self.magazine_from.setMinimumSize(QSize(0, 0))
        self.magazine_from.setMaximumSize(QSize(16777215, 16777215))
        self.magazine_from.setFont(font3)

        self.horizontalLayout_36.addWidget(self.magazine_from)


        self.verticalLayout_12.addWidget(self.widget_74)


        self.gridLayout_11.addWidget(self.widget_72, 0, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.widget_23)


        self.gridLayout_12.addWidget(self.strip, 3, 1, 1, 1)

        self.dev_status = QWidget(self.frame)
        self.dev_status.setObjectName(u"dev_status")
        self.dev_status.setMinimumSize(QSize(720, 350))
        self.dev_status.setMaximumSize(QSize(741, 16777215))
        self.dev_status.setStyleSheet(u"#dev_status{\n"
"    border-left: 4px solid #27296c;\n"
"    border-right: 4px solid #27296c;\n"
"    border-bottom: 5px solid #27296c;\n"
"    border-top: none;\n"
"    border-radius: 4px;\n"
"    background: white;\n"
"}\n"
"")
        self.verticalLayout_3 = QVBoxLayout(self.dev_status)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, -1, -1)
        self.device_status = QLabel(self.dev_status)
        self.device_status.setObjectName(u"device_status")
        self.device_status.setMinimumSize(QSize(750, 40))
        self.device_status.setMaximumSize(QSize(750, 50))
        self.device_status.setFont(font1)
        self.device_status.setStyleSheet(u"#device_status {\n"
"        background-color: #27296c;   \n"
"        color: white;\n"
"        font-weight: bold;\n"
"        font-size: 14pt;\n"
"        padding: 6px 10px;\n"
"        border: none;\n"
"        border-bottom: none;         \n"
"        border-top-left-radius: 1px;\n"
"        border-top-right-radius: 1px;\n"
"		border-radius:60px;\n"
"}\n"
"\n"
"")
        self.device_status.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.device_status)

        self.widget_22 = QWidget(self.dev_status)
        self.widget_22.setObjectName(u"widget_22")
        self.widget_22.setMinimumSize(QSize(0, 0))
        self.widget_22.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_6 = QGridLayout(self.widget_22)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_5 = QLabel(self.widget_22)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(20, 49))
        font4 = QFont()
        font4.setFamilies([u"Poppins"])
        font4.setPointSize(12)
        font4.setBold(True)
        self.label_5.setFont(font4)

        self.gridLayout_6.addWidget(self.label_5, 0, 0, 1, 1)

        self.one = QLabel(self.widget_22)
        self.one.setObjectName(u"one")
        self.one.setFont(font4)
        self.one.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.one, 0, 1, 1, 1)

        self.label_10 = QLabel(self.widget_22)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font4)

        self.gridLayout_6.addWidget(self.label_10, 2, 0, 1, 1)

        self.label_12 = QLabel(self.widget_22)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font4)

        self.gridLayout_6.addWidget(self.label_12, 4, 0, 1, 1)

        self.label_13 = QLabel(self.widget_22)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font4)

        self.gridLayout_6.addWidget(self.label_13, 3, 0, 1, 1)

        self.label_6 = QLabel(self.widget_22)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font4)

        self.gridLayout_6.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_16 = QLabel(self.widget_22)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMaximumSize(QSize(20, 16777215))
        self.label_16.setFont(font4)

        self.gridLayout_6.addWidget(self.label_16, 0, 2, 1, 1)

        self.six = QLabel(self.widget_22)
        self.six.setObjectName(u"six")
        self.six.setFont(font4)
        self.six.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.six, 0, 3, 1, 1)

        self.seven = QLabel(self.widget_22)
        self.seven.setObjectName(u"seven")
        self.seven.setFont(font4)
        self.seven.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.seven, 1, 3, 1, 1)

        self.label_18 = QLabel(self.widget_22)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font4)

        self.gridLayout_6.addWidget(self.label_18, 1, 2, 1, 1)

        self.label_20 = QLabel(self.widget_22)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font4)

        self.gridLayout_6.addWidget(self.label_20, 2, 2, 1, 1)

        self.eight = QLabel(self.widget_22)
        self.eight.setObjectName(u"eight")
        self.eight.setFont(font4)
        self.eight.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.eight, 2, 3, 1, 1)

        self.label_21 = QLabel(self.widget_22)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font4)

        self.gridLayout_6.addWidget(self.label_21, 3, 2, 1, 1)

        self.nine = QLabel(self.widget_22)
        self.nine.setObjectName(u"nine")
        self.nine.setFont(font4)
        self.nine.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.nine, 3, 3, 1, 1)

        self.label_22 = QLabel(self.widget_22)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font4)

        self.gridLayout_6.addWidget(self.label_22, 4, 2, 1, 1)

        self.ten = QLabel(self.widget_22)
        self.ten.setObjectName(u"ten")
        self.ten.setFont(font4)
        self.ten.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.ten, 4, 3, 1, 1)

        self.two = QLabel(self.widget_22)
        self.two.setObjectName(u"two")
        self.two.setFont(font4)
        self.two.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.two, 1, 1, 1, 1)

        self.three = QLabel(self.widget_22)
        self.three.setObjectName(u"three")
        self.three.setFont(font4)
        self.three.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.three, 2, 1, 1, 1)

        self.four = QLabel(self.widget_22)
        self.four.setObjectName(u"four")
        self.four.setFont(font4)
        self.four.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.four, 3, 1, 1, 1)

        self.five = QLabel(self.widget_22)
        self.five.setObjectName(u"five")
        self.five.setFont(font4)
        self.five.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.five, 4, 1, 1, 1)


        self.verticalLayout_3.addWidget(self.widget_22)


        self.gridLayout_12.addWidget(self.dev_status, 1, 1, 1, 1)

        self.live_camera = QLabel(self.frame)
        self.live_camera.setObjectName(u"live_camera")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.live_camera.sizePolicy().hasHeightForWidth())
        self.live_camera.setSizePolicy(sizePolicy1)
        self.live_camera.setMinimumSize(QSize(1174, 925))
        self.live_camera.setMaximumSize(QSize(1174, 925))
        self.live_camera.setStyleSheet(u"QLabel {\n"
"    border: 2px solid black;      \n"
"    border-radius: 5px;           \n"
"    padding: 5px;                 \n"
"}\n"
"")

        self.gridLayout_12.addWidget(self.live_camera, 1, 0, 3, 1)

        self.ini_frame = QFrame(self.frame)
        self.ini_frame.setObjectName(u"ini_frame")
        self.ini_frame.setMinimumSize(QSize(0, 0))
        self.ini_frame.setMaximumSize(QSize(741, 80))
        self.ini_frame.setStyleSheet(u"#ini_frame{\n"
"    border-left: 4px solid #27296c;\n"
"    border-right: 4px solid #27296c;\n"
"    border-bottom: 5px solid #27296c;\n"
"	border-top:5px solid #27296c;\n"
"    border-radius: 4px;\n"
"    background: white;\n"
"}\n"
"")
        self.ini_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ini_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.ini_frame)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.action_button = QPushButton(self.ini_frame)
        self.action_button.setObjectName(u"action_button")
        self.action_button.setMinimumSize(QSize(41, 41))
        self.action_button.setMaximumSize(QSize(41, 41))
        font5 = QFont()
        font5.setFamilies([u"Poppins"])
        font5.setPointSize(20)
        self.action_button.setFont(font5)
        self.action_button.setStyleSheet(u"border:none;")
        icon2 = QIcon()
        icon2.addFile(u":/play.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon2.addFile(u":/pause.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
        icon2.addFile(u":/pause.png", QSize(), QIcon.Mode.Active, QIcon.State.On)
        self.action_button.setIcon(icon2)
        self.action_button.setIconSize(QSize(32, 32))
        self.action_button.setCheckable(True)

        self.gridLayout_10.addWidget(self.action_button, 0, 0, 1, 1)

        self.export_button = QPushButton(self.ini_frame)
        self.export_button.setObjectName(u"export_button")
        self.export_button.setMinimumSize(QSize(51, 41))
        self.export_button.setMaximumSize(QSize(51, 41))
        self.export_button.setFont(font5)
        self.export_button.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-top: 8px;\n"
"    padding-bottom: 5px;\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u":/export.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.export_button.setIcon(icon3)
        self.export_button.setIconSize(QSize(46, 46))
        self.export_button.setCheckable(True)

        self.gridLayout_10.addWidget(self.export_button, 0, 2, 1, 1)

        self.delete_button = QPushButton(self.ini_frame)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setMinimumSize(QSize(41, 41))
        self.delete_button.setMaximumSize(QSize(41, 41))
        self.delete_button.setFont(font5)
        self.delete_button.setStyleSheet(u"border:none;")
        icon4 = QIcon()
        icon4.addFile(u":/delete (1).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.delete_button.setIcon(icon4)
        self.delete_button.setIconSize(QSize(41, 41))
        self.delete_button.setCheckable(True)

        self.gridLayout_10.addWidget(self.delete_button, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.ini_frame, 2, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_23.setText("")
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"INTELLIGENT VISUAL INSPECTION SYSTEM", None))
        self.close.setText("")
        self.minimize.setText("")
        self.current_qlabel.setText(QCoreApplication.translate("MainWindow", u" Current Strip Status", None))
        self.label_78.setText(QCoreApplication.translate("MainWindow", u"Operator:", None))
        self.label_82.setText(QCoreApplication.translate("MainWindow", u"Good Units:", None))
        self.good_unit_label.setText("")
        self.label_73.setText(QCoreApplication.translate("MainWindow", u"Bad Units:", None))
        self.bad_unit_label_2.setText("")
        self.label_74.setText(QCoreApplication.translate("MainWindow", u"Magazine to:", None))
        self.label_83.setText(QCoreApplication.translate("MainWindow", u"Magazine From:", None))
        self.device_status.setText(QCoreApplication.translate("MainWindow", u"Device Status", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.one.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.six.setText("")
        self.seven.setText("")
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.eight.setText("")
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.nine.setText("")
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.ten.setText("")
        self.two.setText("")
        self.three.setText("")
        self.four.setText("")
        self.five.setText("")
        self.live_camera.setText("")
        self.action_button.setText("")
        self.export_button.setText("")
        self.delete_button.setText("")

