# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'signup.ui'
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


class Ui_Signup(object):
    def setupUi(self, Signup):
        if not Signup.objectName():
            Signup.setObjectName("Signup")
        Signup.resize(1280, 720)
        Signup.setStyleSheet("background-color: #17171B;")
        self.widget = QWidget(Signup)
        self.widget.setObjectName("widget")
        self.widget.setGeometry(QRect(0, -250, 1280, 720))
        self.widget.setStyleSheet(
            "background-image: url(:/background/ui/background/login.png);\n"
            "background-repeat: no-repeat; /* Prevents the image from repeating */\n"
            "background-color: none;\n"
            "background-position: center; /* Centers the image */"
        )
        self.password_input = QLineEdit(self.widget)
        self.password_input.setObjectName("password_input")
        self.password_input.setGeometry(QRect(480, 580, 320, 50))
        self.password_input.setStyleSheet(
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
        self.login_title_label.setGeometry(QRect(480, 410, 320, 50))
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
        self.sign_up_button = QPushButton(self.widget)
        self.sign_up_button.setObjectName("sign_up_button")
        self.sign_up_button.setGeometry(QRect(480, 640, 320, 50))
        self.sign_up_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.sign_up_button.setStyleSheet(
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
        self.username_input = QLineEdit(self.widget)
        self.username_input.setObjectName("username_input")
        self.username_input.setGeometry(QRect(480, 520, 320, 50))
        self.username_input.setStyleSheet(
            "QLineEdit {\n"
            "    background-color: #17171B;  /* Background color */\n"
            "    border: 2px solid rgba(52, 51, 67, 255);  /* Default border color */\n"
            "    border-radius: 8px;  /* Rounded corners */\n"
            "    padding: 8px;  /* Padding inside the input box */\n"
            "    color: white;  /* Text color */\n"
            "}\n"
            "\n"
            "QLineEdit:focus {\n"
            "    border: 2px solid rgba(251, 109, 169, 255);  /* Border color on focus (gradient2) */\n"
            "    outline: none;  /* Remove default outline */\n"
            "}\n"
            ""
        )
        self.error_label = QLabel(self.widget)
        self.error_label.setObjectName("error_label")
        self.error_label.setGeometry(QRect(480, 470, 320, 30))
        self.error_label.setStyleSheet(
            "background-color: #f8d7da;\n" "color: #721c24;\n" "border-radius: 4px;\n" "padding: 5px;\n" ""
        )
        self.error_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.eye_icon = QLabel(self.widget)
        self.eye_icon.setObjectName("eye_icon")
        self.eye_icon.setGeometry(QRect(760, 593, 24, 24))
        self.eye_icon.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.eye_icon.setStyleSheet(
            "QLabel {\n" "	image: url(:/icons/ui/icons/eye_closed.png);\n" "	background-color: transparent;\n" "}"
        )

        self.retranslateUi(Signup)

        QMetaObject.connectSlotsByName(Signup)

    # setupUi

    def retranslateUi(self, Signup):
        Signup.setWindowTitle(QCoreApplication.translate("Signup", "Form", None))
        self.password_input.setText("")
        self.password_input.setPlaceholderText(QCoreApplication.translate("Signup", "Password", None))
        self.login_title_label.setText(QCoreApplication.translate("Signup", "SIGN UP", None))
        self.sign_up_button.setText(QCoreApplication.translate("Signup", "Sign Up", None))
        self.username_input.setText("")
        self.username_input.setPlaceholderText(QCoreApplication.translate("Signup", "Username", None))
        self.error_label.setText(
            QCoreApplication.translate("Signup", "\u26a0\ufe0f Incorrect username or password. Try again.\n" "", None)
        )
        self.eye_icon.setText("")

    # retranslateUi
