# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exception_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractScrollArea, QApplication, QDialog,
    QDialogButtonBox, QFrame, QHBoxLayout, QLayout,
    QPlainTextEdit, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_Exception_Dialog(object):
    def setupUi(self, Exception_Dialog):
        if not Exception_Dialog.objectName():
            Exception_Dialog.setObjectName(u"Exception_Dialog")
        Exception_Dialog.setWindowModality(Qt.WindowModal)
        Exception_Dialog.resize(410, 210)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Exception_Dialog.sizePolicy().hasHeightForWidth())
        Exception_Dialog.setSizePolicy(sizePolicy)
        icon = QIcon()
        iconThemeName = u"default"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Mode.Normal, QIcon.State.Off)

        Exception_Dialog.setWindowIcon(icon)
        Exception_Dialog.setSizeGripEnabled(True)
        Exception_Dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(Exception_Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.summaryText = QTextEdit(Exception_Dialog)
        self.summaryText.setObjectName(u"summaryText")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.summaryText.sizePolicy().hasHeightForWidth())
        self.summaryText.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(11)
        self.summaryText.setFont(font)
        self.summaryText.setFrameShape(QFrame.NoFrame)
        self.summaryText.setFrameShadow(QFrame.Plain)
        self.summaryText.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.summaryText.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.summaryText)

        self.detailPlainText = QPlainTextEdit(Exception_Dialog)
        self.detailPlainText.setObjectName(u"detailPlainText")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.detailPlainText.sizePolicy().hasHeightForWidth())
        self.detailPlainText.setSizePolicy(sizePolicy2)
        self.detailPlainText.setMinimumSize(QSize(0, 0))
        self.detailPlainText.setStyleSheet(u"font-family: Courier; font-size: 12px;")
        self.detailPlainText.setFrameShadow(QFrame.Sunken)
        self.detailPlainText.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.detailPlainText.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.detailPlainText.setReadOnly(True)

        self.verticalLayout.addWidget(self.detailPlainText)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.detailButton = QPushButton(Exception_Dialog)
        self.detailButton.setObjectName(u"detailButton")

        self.horizontalLayout.addWidget(self.detailButton)

        self.buttonBox = QDialogButtonBox(Exception_Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy3)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Exception_Dialog)
        self.buttonBox.rejected.connect(Exception_Dialog.reject)
        self.buttonBox.accepted.connect(Exception_Dialog.accept)

        QMetaObject.connectSlotsByName(Exception_Dialog)
    # setupUi

    def retranslateUi(self, Exception_Dialog):
        Exception_Dialog.setWindowTitle(QCoreApplication.translate("Exception_Dialog", u"Unhandled Exception Error", None))
        self.detailPlainText.setPlaceholderText("")
        self.detailButton.setText(QCoreApplication.translate("Exception_Dialog", u"Show Details", None))
    # retranslateUi

