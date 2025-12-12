# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'expert_dlg.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QSizePolicy, QTextBrowser, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(581, 392)
        Dialog.setModal(True)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(230, 350, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.textBrowser = QTextBrowser(Dialog)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 10, 561, 331))
        self.textBrowser.setInputMethodHints(Qt.ImhNone)
        self.textBrowser.setFrameShadow(QFrame.Sunken)
        self.textBrowser.setOpenExternalLinks(True)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"About expert parameters", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:700;\">Are you sure you know what these do?</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Before modifying these, you should read the documentation and the references listed below for a deep understading of what the algorithm does.</p>\n"
"<p style=\" margin-top:12px"
                        "; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">References:</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Cabo, C., Ordonez, C., Lopez-Sanchez, C. A., &amp; Armesto, J. (2018). Automatic dendrometry: Tree detection, tree height and diameter estimation using terrestrial laser scanning. International Journal of Applied Earth Observation and Geoinformation, 69, 164\u2013174. <a href=\"https://doi.org/10.1016/j.jag.2018.01.011\"><span style=\" text-decoration: underline; color:#0000ff;\">10.1016/j.jag.2018.01.011</span></a></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Ester, M., Kriegel, H.-P., Sander, J., &amp; Xu, X. (1996). A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise. www.aaai.org</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px"
                        "; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Prendes, C., Cabo, C., Ordo\u00f1ez, C., Majada, J., &amp; Canga, E. (2021). An algorithm for the automatic parametrization of wood volume equations from Terrestrial Laser Scanning point clouds: application in Pinus pinaster. GIScience and Remote Sensing, 58(7), 1130\u20131150. <a href=\"https://doi.org/10.1080/15481603.2021.1972712\"><span style=\" text-decoration: underline; color:#0000ff;\">10.1080/15481603.2021.1972712</span></a></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Zhang, W., Qi, J., Wan, P., Wang, H., Xie, D., Wang, X., &amp; Yan, G. (2016). An easy-to-use airborne LiDAR data filtering method based on cloth simulation. Remote Sensing, 8(6). <a href=\"10.3390/rs8060501\"><span style=\" text-decoration: underline; color:#0000ff;\">https://doi.org/10.3390/rs8060501</span></a></p></body></html>", None))
    # retranslateUi

