# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QSizePolicy, QWidget
from src.common.resources import ui_rc


class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName("Login")
        Login.resize(1280, 720)
        Login.setStyleSheet("background-color: #17171B;")
        self.widget = QWidget(Login)
        self.widget.setObjectName("widget")
        self.widget.setGeometry(QRect(0, -250, 1280, 720))
        self.widget.setStyleSheet(
            "background-image: url(:/background/ui/background/login.png);\n"
            "background-repeat: no-repeat; /* Prevents the image from repeating */\n"
            "background-position: center; /* Centers the image */"
        )
        self.username_input = QLineEdit(self.widget)
        self.username_input.setObjectName("username_input")
        self.username_input.setGeometry(QRect(480, 570, 320, 50))
        self.username_input.setStyleSheet(
            "QLineEdit {\n"
            "    background-color: #17171B;  /* Background color */\n"
            "    border: 2px solid rgba(52, 51, 67, 255);  /* Default border color */\n"
            "    border-radius: 8px;  /* Rounded corners */\n"
            "    padding: 8px;  /* Padding inside the input box */\n"
            "    color: white;  /* Text color */\n"
            "    selection-background-color: rgba(52, 51, 67, 255); /* Selection background color */\n"
            "    selection-color: blue;  /* Selected text color */\n"
            "}\n"
            "\n"
            "QLineEdit:focus {\n"
            "    border: 2px solid rgba(251, 109, 169, 255);  /* Border color on focus (gradient2) */\n"
            "    outline: none;  /* Remove default outline */\n"
            "}\n"
            ""
        )
        self.login_title_label = QLabel(self.widget)
        self.login_title_label.setObjectName("login_title_label")
        self.login_title_label.setGeometry(QRect(480, 480, 320, 50))
        self.login_title_label.setBaseSize(QSize(0, 0))
        self.login_title_label.setStyleSheet(
            "QLabel {\n"
            "    color: white;  /* Text color */\n"
            "    font-size: 40px;  /* Font size */\n"
            "	font-weight: bold;  /* Make the font bold */\n"
            "	background-color: transparent;  /* Transparent background */\n"
            "}\n"
            ""
        )
        self.login_title_label.setAlignment(Qt.AlignCenter)
        self.login_button = QPushButton(self.widget)
        self.login_button.setObjectName("login_button")
        self.login_button.setGeometry(QRect(480, 640, 320, 50))
        self.login_button.setStyleSheet(
            "QPushButton {\n"
            "    background-color: qlineargradient(\n"
            "        spread:pad, \n"
            "        x1:0, y1:0, \n"
            "        x2:1, y2:0, \n"
            "        stop:0 rgba(187, 63, 221, 255),  /* gradient1 */\n"
            "        stop:0.5 rgba(251, 109, 169, 255),  /* gradient2 */\n"
            "        stop:1 rgba(255, 159, 124, 255)   /* gradient3 */\n"
            "    );\n"
            "    color: white;  /* Text color */\n"
            "    border: 2px solid rgba(52, 51, 67, 255);  /* Border color */\n"
            "    border-radius: 10px;  /* Rounded corners */\n"
            "    padding: 10px;  /* Padding around text */\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: qlineargradient(\n"
            "        spread:pad, \n"
            "        x1:0, y1:0, \n"
            "        x2:1, y2:0, \n"
            "        stop:0 rgba(207, 83, 241, 255),  /* Slightly lighter gradient1 for hover */\n"
            "        stop:0.5 rgba(255, 129, 189, 255),  /* Slightly lighter gradient2 for hover */\n"
            "        stop:1 rgba(255, 179, 144, 255)   /* Slightly lighter gradient3 for hover */\n"
            "    );\n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    backgro"
            "und-color: qlineargradient(\n"
            "        spread:pad, \n"
            "        x1:0, y1:0, \n"
            "        x2:1, y2:0, \n"
            "        stop:0 rgba(167, 43, 191, 255),  /* Darker gradient1 for pressed state */\n"
            "        stop:0.5 rgba(231, 89, 149, 255),  /* Darker gradient2 for pressed state */\n"
            "        stop:1 rgba(235, 139, 114, 255)   /* Darker gradient3 for pressed state */\n"
            "    );\n"
            "}\n"
            ""
        )
        self.error_label = QLabel(self.widget)
        self.error_label.setObjectName("error_label")
        self.error_label.setEnabled(True)
        self.error_label.setGeometry(QRect(480, 605, 160, 20))
        self.error_label.setStyleSheet(
            "QLabel {\n"
            "    color: red;  /* Text color */\n"
            "    font-size: 16px;  /* Font size */\n"
            "	background-color: transparent;  /* Transparent background */\n"
            "}\n"
            ""
        )

        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)

    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", "Form", None))
        self.username_input.setText("")
        self.username_input.setPlaceholderText(QCoreApplication.translate("Login", "Username", None))
        self.login_title_label.setText(QCoreApplication.translate("Login", "WELCOME", None))
        self.login_button.setText(QCoreApplication.translate("Login", "Login", None))
        self.error_label.setText(QCoreApplication.translate("Login", "Username is required", None))

    # retranslateUi
