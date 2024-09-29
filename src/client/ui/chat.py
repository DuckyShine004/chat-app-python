# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chat.ui'
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
from PySide6.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QScrollArea, QSizePolicy, QWidget
from src.common.resources import ui_rc


class Ui_Chat(object):
    def setupUi(self, Chat):
        if not Chat.objectName():
            Chat.setObjectName("Chat")
        Chat.resize(1280, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Chat.sizePolicy().hasHeightForWidth())
        Chat.setSizePolicy(sizePolicy)
        Chat.setStyleSheet("background-color: #0C111D;\n" "/*background-color: white;")
        self.scrollArea = QScrollArea(Chat)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setGeometry(QRect(384, 79, 896, 581))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setFocusPolicy(Qt.NoFocus)
        self.scrollArea.setStyleSheet(
            "/* ScrollArea */\n"
            "QScrollArea {\n"
            "    border: 2px solid #161B27;  /* Set border thickness and color */\n"
            "    background-color: transparent;  /* Optional: Set background color to transparent */\n"
            "}\n"
            "\n"
            "/* Scrollbar background (track) */\n"
            "QScrollBar:vertical {\n"
            "    background-color: #161B27;  /* Dark background color for the scrollbar track */\n"
            "    width: 8px;  /* Thinner width for the vertical scrollbar */\n"
            "    margin: 0px;  /* Margin around the scrollbar */\n"
            "    border: none; /* No border around the scrollbar */\n"
            "}\n"
            "\n"
            "QScrollBar:horizontal {\n"
            "    background-color: #161B27;  /* Dark background color for the scrollbar track */\n"
            "    height: 8px;  /* Thinner height for the horizontal scrollbar */\n"
            "    margin: 0px;  /* Margin around the scrollbar */\n"
            "    border: none; /* No border around the scrollbar */\n"
            "}\n"
            "\n"
            "/* Scrollbar handle (the draggable part) */\n"
            "QScrollBar::handle:vertical {\n"
            "    background-color: #969696;  /* Custom handle color */\n"
            "    b"
            "order-radius: 4px;  /* Rounded corners */\n"
            "    min-height: 10px;  /* Reduce the minimum height to make the handle smaller */\n"
            "    width: 6px;  /* Make the handle thinner */\n"
            "}\n"
            "\n"
            "QScrollBar::handle:horizontal {\n"
            "    background-color: #969696;  /* Custom handle color */\n"
            "    border-radius: 4px;  /* Rounded corners */\n"
            "    min-width: 10px;  /* Reduce the minimum width to make the handle smaller */\n"
            "    height: 6px;  /* Make the handle thinner */\n"
            "}\n"
            "\n"
            "/* Scrollbar handle on hover */\n"
            "QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {\n"
            "    background-color: #b0b0b0;  /* Slightly lighter color when hovered */\n"
            "}\n"
            "\n"
            "/* Scrollbar handle when pressed */\n"
            "QScrollBar::handle:vertical:pressed, QScrollBar::handle:horizontal:pressed {\n"
            "    background-color: #828282;  /* Darker color when pressed */\n"
            "}\n"
            "\n"
            "/* Top and bottom buttons (arrows) */\n"
            "QScrollBar::add-line, QScrollBar::sub-line {\n"
            "    background: none;  /* No arrows */\n"
            ""
            "    border: none;\n"
            "    width: 0px;\n"
            "    height: 0px;\n"
            "}\n"
            ""
        )
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 892, 577))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.chat_label = QLabel(Chat)
        self.chat_label.setObjectName("chat_label")
        self.chat_label.setGeometry(QRect(460, 20, 821, 40))
        self.chat_label.setStyleSheet(
            "QLabel {\n"
            "    color: white;  /* Text color */\n"
            "    font-size: 32px;  /* Font size */\n"
            "	font-weight: bold;  /* Make the font bold */\n"
            "	background-color: transparent;  /* Transparent background */\n"
            "}\n"
            ""
        )
        self.label_2 = QLabel(Chat)
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QRect(400, 20, 40, 40))
        self.label_2.setStyleSheet(
            "QLabel {\n" "	image: url(:/icons/ui/icons/user_profile.png);\n" "	background-color: transparent;\n" "}"
        )
        self.label_2.setScaledContents(True)
        self.line = QFrame(Chat)
        self.line.setObjectName("line")
        self.line.setGeometry(QRect(384, 0, 20, 80))
        self.line.setStyleSheet(
            "#line {\n"
            "    background-color: transparent; /* Transparent background */\n"
            "    border-left: 2px solid #161B27; /* Vertical line with thickness 3px and color white */\n"
            "}\n"
            ""
        )
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2 = QFrame(Chat)
        self.line_2.setObjectName("line_2")
        self.line_2.setGeometry(QRect(384, 659, 20, 65))
        self.line_2.setStyleSheet(
            "#line_2 {\n"
            "    background-color: transparent; /* Transparent background */\n"
            "    border-left: 2px solid #161B27; /* Vertical line with thickness 3px and color white */\n"
            "}\n"
            ""
        )
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.message_input = QLineEdit(Chat)
        self.message_input.setObjectName("message_input")
        self.message_input.setGeometry(QRect(400, 670, 810, 40))
        self.message_input.setStyleSheet(
            "QLineEdit {\n"
            "    background-color: #161B26; /* Background color for the input box */\n"
            "    border: 1px solid #1F242E; /* Border color */\n"
            "    border-radius: 10px; /* Rounded corners */\n"
            "    padding: 8px; /* Padding inside the input box */\n"
            "    color: white; /* Text color */\n"
            "    font-size: 14px; /* Font size */\n"
            "}\n"
            "\n"
            "QLineEdit:focus {\n"
            "    border: 1px solid #5542F6; /* Border color when focused */\n"
            "}\n"
            ""
        )
        self.send_button = QPushButton(Chat)
        self.send_button.setObjectName("send_button")
        self.send_button.setGeometry(QRect(1220, 670, 40, 40))
        self.send_button.setStyleSheet(
            "QPushButton {\n"
            "	background-color: #5542F6;\n"
            "	background-position: center;  /* Center the image */\n"
            "    	background-repeat: no-repeat;  /* Prevent image from repeating */\n"
            "    	border-radius: 10px;  /* Rounded corners */\n"
            "    	padding: 10px;  /* Padding around text */\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "	background-color: #5F4FF7;\n"
            "	border-radius: 10px;  /* Rounded corners */\n"
            "	padding: 10px;  /* Padding around text */\n"
            "}"
        )
        self.send_icon = QLabel(Chat)
        self.send_icon.setObjectName("send_icon")
        self.send_icon.setEnabled(False)
        self.send_icon.setGeometry(QRect(1230, 680, 20, 20))
        self.send_icon.setStyleSheet(
            "QLabel {\n" "	image: url(:/icons/ui/icons/send.png);\n" "	background-color: transparent;\n" "}"
        )
        self.send_icon.setScaledContents(True)
        self.line_3 = QFrame(Chat)
        self.line_3.setObjectName("line_3")
        self.line_3.setGeometry(QRect(0, 61, 385, 20))
        self.line_3.setStyleSheet(
            "#line_3 {\n"
            "    background-color: transparent; /* Transparent background */\n"
            "    border-bottom: 2px solid #161B27; /* Vertical line with thickness 3px and color white */\n"
            "}"
        )
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_3 = QLabel(Chat)
        self.label_3.setObjectName("label_3")
        self.label_3.setGeometry(QRect(20, 20, 271, 40))
        self.label_3.setStyleSheet(
            "QLabel {\n"
            "    color: white;  /* Text color */\n"
            "    font-size: 32px;  /* Font size */\n"
            "	font-weight: bold;  /* Make the font bold */\n"
            "	background-color: transparent;  /* Transparent background */\n"
            "}\n"
            ""
        )
        QWidget.setTabOrder(self.scrollArea, self.message_input)
        QWidget.setTabOrder(self.message_input, self.send_button)

        self.retranslateUi(Chat)

        QMetaObject.connectSlotsByName(Chat)

    # setupUi

    def retranslateUi(self, Chat):
        Chat.setWindowTitle(QCoreApplication.translate("Chat", "Form", None))
        self.chat_label.setText(QCoreApplication.translate("Chat", "PERSON", None))
        self.label_2.setText("")
        self.message_input.setPlaceholderText(QCoreApplication.translate("Chat", "Type a message", None))
        self.send_button.setText("")
        self.send_icon.setText("")
        self.label_3.setText(QCoreApplication.translate("Chat", "MESSAGES", None))

    # retranslateUi
