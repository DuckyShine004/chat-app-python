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
from PySide6.QtWidgets import QApplication, QLabel, QScrollArea, QSizePolicy, QWidget
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
        Chat.setStyleSheet("background-color: #0C111D;")
        self.scrollArea = QScrollArea(Chat)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setGeometry(QRect(384, 79, 896, 581))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setStyleSheet(
            "QScrollArea {\n"
            "    border: 2px solid #161B27;  /* Set border thickness and color */\n"
            "    border-radius: 5px;  /* Optional: Add rounded corners */\n"
            "    background-color: transparent;  /* Optional: Set background color to transparent */\n"
            "}\n"
            "\n"
            "QScrollBar:vertical, QScrollBar:horizontal {\n"
            "    background-color: #161B27;  /* Style the scrollbars to match the border */\n"
            "}"
        )
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 892, 577))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QLabel(Chat)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(450, 20, 821, 41))
        self.label.setStyleSheet(
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
        self.label_2.setGeometry(QRect(390, 20, 40, 40))
        self.label_2.setStyleSheet(
            "QLabel {\n" "	image: url(:/icons/ui/icons/user_profile.png);\n" "	background-color: transparent;\n" "}"
        )
        self.label_2.setScaledContents(True)

        self.retranslateUi(Chat)

        QMetaObject.connectSlotsByName(Chat)

    # setupUi

    def retranslateUi(self, Chat):
        Chat.setWindowTitle(QCoreApplication.translate("Chat", "Form", None))
        self.label.setText(QCoreApplication.translate("Chat", "PERSON", None))
        self.label_2.setText("")

    # retranslateUi
