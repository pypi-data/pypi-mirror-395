# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget)
from . import gui_ressources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1164, 730)
        MainWindow.setMinimumSize(QSize(0, 720))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setBaseSize(QSize(0, 0))
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.basicTab = QWidget()
        self.basicTab.setObjectName(u"basicTab")
        self.gridLayout = QGridLayout(self.basicTab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.basic_tab_img_1 = QLabel(self.basicTab)
        self.basic_tab_img_1.setObjectName(u"basic_tab_img_1")
        self.basic_tab_img_1.setPixmap(QPixmap(u":/assets/assets/stripe.png"))
        self.basic_tab_img_1.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout.addWidget(self.basic_tab_img_1, 2, 0, 1, 1)

        self.basic_tab_img_3_title = QLabel(self.basicTab)
        self.basic_tab_img_3_title.setObjectName(u"basic_tab_img_3_title")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.basic_tab_img_3_title.setFont(font)
        self.basic_tab_img_3_title.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.basic_tab_img_3_title, 1, 3, 1, 1)

        self.basic_tab_img_1_cpt = QLabel(self.basicTab)
        self.basic_tab_img_1_cpt.setObjectName(u"basic_tab_img_1_cpt")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.basic_tab_img_1_cpt.sizePolicy().hasHeightForWidth())
        self.basic_tab_img_1_cpt.setSizePolicy(sizePolicy)
        self.basic_tab_img_1_cpt.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout.addWidget(self.basic_tab_img_1_cpt, 3, 0, 1, 1)

        self.basic_tab_desc_frame = QFrame(self.basicTab)
        self.basic_tab_desc_frame.setObjectName(u"basic_tab_desc_frame")
        sizePolicy.setHeightForWidth(self.basic_tab_desc_frame.sizePolicy().hasHeightForWidth())
        self.basic_tab_desc_frame.setSizePolicy(sizePolicy)
        self.basic_tab_desc_frame.setFrameShape(QFrame.NoFrame)
        self.basic_tab_desc_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.basic_tab_desc_frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tutorial_link_btn = QPushButton(self.basic_tab_desc_frame)
        self.tutorial_link_btn.setObjectName(u"tutorial_link_btn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tutorial_link_btn.sizePolicy().hasHeightForWidth())
        self.tutorial_link_btn.setSizePolicy(sizePolicy1)
        self.tutorial_link_btn.setStyleSheet(u"")
        self.tutorial_link_btn.setCheckable(False)
        self.tutorial_link_btn.setFlat(False)

        self.gridLayout_4.addWidget(self.tutorial_link_btn, 3, 1, 1, 1)

        self.documentation_link_btn = QPushButton(self.basic_tab_desc_frame)
        self.documentation_link_btn.setObjectName(u"documentation_link_btn")
        sizePolicy1.setHeightForWidth(self.documentation_link_btn.sizePolicy().hasHeightForWidth())
        self.documentation_link_btn.setSizePolicy(sizePolicy1)
        self.documentation_link_btn.setStyleSheet(u"")
        self.documentation_link_btn.setIconSize(QSize(16, 16))
        self.documentation_link_btn.setAutoRepeatDelay(301)
        self.documentation_link_btn.setFlat(False)

        self.gridLayout_4.addWidget(self.documentation_link_btn, 3, 0, 1, 1)

        self.basic_tab_desc = QLabel(self.basic_tab_desc_frame)
        self.basic_tab_desc.setObjectName(u"basic_tab_desc")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.basic_tab_desc.sizePolicy().hasHeightForWidth())
        self.basic_tab_desc.setSizePolicy(sizePolicy2)
        self.basic_tab_desc.setTextFormat(Qt.RichText)
        self.basic_tab_desc.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.basic_tab_desc.setWordWrap(True)

        self.gridLayout_4.addWidget(self.basic_tab_desc, 2, 0, 1, 2)

        self.basic_3dfin_logo = QLabel(self.basic_tab_desc_frame)
        self.basic_3dfin_logo.setObjectName(u"basic_3dfin_logo")
        sizePolicy1.setHeightForWidth(self.basic_3dfin_logo.sizePolicy().hasHeightForWidth())
        self.basic_3dfin_logo.setSizePolicy(sizePolicy1)
        self.basic_3dfin_logo.setPixmap(QPixmap(u":/assets/assets/3dfin_logo.png"))
        self.basic_3dfin_logo.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.basic_3dfin_logo, 1, 0, 1, 2)


        self.gridLayout.addWidget(self.basic_tab_desc_frame, 0, 2, 1, 2)

        self.basic_tab_img_1_title = QLabel(self.basicTab)
        self.basic_tab_img_1_title.setObjectName(u"basic_tab_img_1_title")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.basic_tab_img_1_title.sizePolicy().hasHeightForWidth())
        self.basic_tab_img_1_title.setSizePolicy(sizePolicy3)
        self.basic_tab_img_1_title.setFont(font)
        self.basic_tab_img_1_title.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.basic_tab_img_1_title, 1, 0, 1, 1)

        self.basic_tab_img_3 = QLabel(self.basicTab)
        self.basic_tab_img_3.setObjectName(u"basic_tab_img_3")
        self.basic_tab_img_3.setPixmap(QPixmap(u":/assets/assets/normalized_cloud.png"))
        self.basic_tab_img_3.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout.addWidget(self.basic_tab_img_3, 2, 3, 1, 1)

        self.basic_form_frame = QFrame(self.basicTab)
        self.basic_form_frame.setObjectName(u"basic_form_frame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.basic_form_frame.sizePolicy().hasHeightForWidth())
        self.basic_form_frame.setSizePolicy(sizePolicy4)
        self.basic_form_frame.setFrameShape(QFrame.NoFrame)
        self.basic_form_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.basic_form_frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lower_limit_lbl = QLabel(self.basic_form_frame)
        self.lower_limit_lbl.setObjectName(u"lower_limit_lbl")

        self.gridLayout_3.addWidget(self.lower_limit_lbl, 6, 0, 1, 1)

        self.number_of_iterations_ht = QLabel(self.basic_form_frame)
        self.number_of_iterations_ht.setObjectName(u"number_of_iterations_ht")

        self.gridLayout_3.addWidget(self.number_of_iterations_ht, 7, 2, 1, 1)

        self.res_cloth_ht = QLabel(self.basic_form_frame)
        self.res_cloth_ht.setObjectName(u"res_cloth_ht")

        self.gridLayout_3.addWidget(self.res_cloth_ht, 8, 2, 1, 1)

        self.upper_limit_in = QLineEdit(self.basic_form_frame)
        self.upper_limit_in.setObjectName(u"upper_limit_in")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.upper_limit_in.sizePolicy().hasHeightForWidth())
        self.upper_limit_in.setSizePolicy(sizePolicy5)
        self.upper_limit_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_3.addWidget(self.upper_limit_in, 5, 1, 1, 1)

        self.export_txt_lbl = QLabel(self.basic_form_frame)
        self.export_txt_lbl.setObjectName(u"export_txt_lbl")
        self.export_txt_lbl.setEnabled(True)
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.export_txt_lbl.sizePolicy().hasHeightForWidth())
        self.export_txt_lbl.setSizePolicy(sizePolicy6)

        self.gridLayout_3.addWidget(self.export_txt_lbl, 2, 0, 1, 1)

        self.lower_limit_in = QLineEdit(self.basic_form_frame)
        self.lower_limit_in.setObjectName(u"lower_limit_in")
        sizePolicy5.setHeightForWidth(self.lower_limit_in.sizePolicy().hasHeightForWidth())
        self.lower_limit_in.setSizePolicy(sizePolicy5)
        self.lower_limit_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_3.addWidget(self.lower_limit_in, 6, 1, 1, 1)

        self.export_txt_rb_1 = QRadioButton(self.basic_form_frame)
        self.export_txt_rb_1.setObjectName(u"export_txt_rb_1")

        self.gridLayout_3.addWidget(self.export_txt_rb_1, 3, 0, 1, 1)

        self.upper_limit_ht = QLabel(self.basic_form_frame)
        self.upper_limit_ht.setObjectName(u"upper_limit_ht")

        self.gridLayout_3.addWidget(self.upper_limit_ht, 5, 2, 1, 1)

        self.res_cloth_in = QLineEdit(self.basic_form_frame)
        self.res_cloth_in.setObjectName(u"res_cloth_in")
        sizePolicy5.setHeightForWidth(self.res_cloth_in.sizePolicy().hasHeightForWidth())
        self.res_cloth_in.setSizePolicy(sizePolicy5)
        self.res_cloth_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_3.addWidget(self.res_cloth_in, 8, 1, 1, 1)

        self.export_txt_rb_2 = QRadioButton(self.basic_form_frame)
        self.export_txt_rb_2.setObjectName(u"export_txt_rb_2")

        self.gridLayout_3.addWidget(self.export_txt_rb_2, 3, 1, 1, 1)

        self.number_of_iterations_lbl = QLabel(self.basic_form_frame)
        self.number_of_iterations_lbl.setObjectName(u"number_of_iterations_lbl")

        self.gridLayout_3.addWidget(self.number_of_iterations_lbl, 7, 0, 1, 1)

        self.lower_limit_ht = QLabel(self.basic_form_frame)
        self.lower_limit_ht.setObjectName(u"lower_limit_ht")

        self.gridLayout_3.addWidget(self.lower_limit_ht, 6, 2, 1, 1)

        self.res_cloth_lbl = QLabel(self.basic_form_frame)
        self.res_cloth_lbl.setObjectName(u"res_cloth_lbl")

        self.gridLayout_3.addWidget(self.res_cloth_lbl, 8, 0, 1, 1)

        self.is_noisy_chk = QCheckBox(self.basic_form_frame)
        self.is_noisy_chk.setObjectName(u"is_noisy_chk")

        self.gridLayout_3.addWidget(self.is_noisy_chk, 1, 0, 1, 1)

        self.z0_name_in = QLineEdit(self.basic_form_frame)
        self.z0_name_in.setObjectName(u"z0_name_in")
        sizePolicy5.setHeightForWidth(self.z0_name_in.sizePolicy().hasHeightForWidth())
        self.z0_name_in.setSizePolicy(sizePolicy5)
        self.z0_name_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_3.addWidget(self.z0_name_in, 4, 1, 1, 1)

        self.z0_name_ht = QLabel(self.basic_form_frame)
        self.z0_name_ht.setObjectName(u"z0_name_ht")

        self.gridLayout_3.addWidget(self.z0_name_ht, 4, 2, 1, 1)

        self.is_normalized_chk = QCheckBox(self.basic_form_frame)
        self.is_normalized_chk.setObjectName(u"is_normalized_chk")

        self.gridLayout_3.addWidget(self.is_normalized_chk, 0, 0, 1, 1)

        self.number_of_iterations_in = QLineEdit(self.basic_form_frame)
        self.number_of_iterations_in.setObjectName(u"number_of_iterations_in")
        sizePolicy5.setHeightForWidth(self.number_of_iterations_in.sizePolicy().hasHeightForWidth())
        self.number_of_iterations_in.setSizePolicy(sizePolicy5)
        self.number_of_iterations_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_3.addWidget(self.number_of_iterations_in, 7, 1, 1, 1)

        self.z0_name_lbl = QLabel(self.basic_form_frame)
        self.z0_name_lbl.setObjectName(u"z0_name_lbl")

        self.gridLayout_3.addWidget(self.z0_name_lbl, 4, 0, 1, 1)

        self.upper_limit_lbl = QLabel(self.basic_form_frame)
        self.upper_limit_lbl.setObjectName(u"upper_limit_lbl")

        self.gridLayout_3.addWidget(self.upper_limit_lbl, 5, 0, 1, 1)


        self.gridLayout.addWidget(self.basic_form_frame, 0, 0, 1, 1)

        self.basic_vert_line = QFrame(self.basicTab)
        self.basic_vert_line.setObjectName(u"basic_vert_line")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.basic_vert_line.sizePolicy().hasHeightForWidth())
        self.basic_vert_line.setSizePolicy(sizePolicy7)
        self.basic_vert_line.setFrameShape(QFrame.Shape.VLine)
        self.basic_vert_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.basic_vert_line, 0, 1, 1, 1)

        self.basic_tab_img_2 = QLabel(self.basicTab)
        self.basic_tab_img_2.setObjectName(u"basic_tab_img_2")
        self.basic_tab_img_2.setPixmap(QPixmap(u":/assets/assets/original_cloud.png"))
        self.basic_tab_img_2.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout.addWidget(self.basic_tab_img_2, 2, 2, 1, 1)

        self.basic_tab_img_2_title = QLabel(self.basicTab)
        self.basic_tab_img_2_title.setObjectName(u"basic_tab_img_2_title")
        self.basic_tab_img_2_title.setFont(font)
        self.basic_tab_img_2_title.setTextFormat(Qt.PlainText)
        self.basic_tab_img_2_title.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.basic_tab_img_2_title, 1, 2, 1, 1)

        self.basic_tab_img_2_cpt = QLabel(self.basicTab)
        self.basic_tab_img_2_cpt.setObjectName(u"basic_tab_img_2_cpt")
        self.basic_tab_img_2_cpt.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.basic_tab_img_2_cpt.setWordWrap(True)

        self.gridLayout.addWidget(self.basic_tab_img_2_cpt, 3, 2, 1, 2)

        self.tabWidget.addTab(self.basicTab, "")
        self.advancedTab = QWidget()
        self.advancedTab.setObjectName(u"advancedTab")
        self.gridLayout_5 = QGridLayout(self.advancedTab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.advanced_tab_img_frame = QFrame(self.advancedTab)
        self.advanced_tab_img_frame.setObjectName(u"advanced_tab_img_frame")
        self.advanced_tab_img_frame.setFrameShape(QFrame.NoFrame)
        self.advanced_tab_img_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.advanced_tab_img_frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.advanced_tab_img_1 = QLabel(self.advanced_tab_img_frame)
        self.advanced_tab_img_1.setObjectName(u"advanced_tab_img_1")
        sizePolicy6.setHeightForWidth(self.advanced_tab_img_1.sizePolicy().hasHeightForWidth())
        self.advanced_tab_img_1.setSizePolicy(sizePolicy6)
        self.advanced_tab_img_1.setPixmap(QPixmap(u":/assets/assets/section_details.png"))
        self.advanced_tab_img_1.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.advanced_tab_img_1, 0, 0, 1, 1)

        self.advanced_tab_img_2 = QLabel(self.advanced_tab_img_frame)
        self.advanced_tab_img_2.setObjectName(u"advanced_tab_img_2")
        sizePolicy6.setHeightForWidth(self.advanced_tab_img_2.sizePolicy().hasHeightForWidth())
        self.advanced_tab_img_2.setSizePolicy(sizePolicy6)
        self.advanced_tab_img_2.setFrameShape(QFrame.NoFrame)
        self.advanced_tab_img_2.setPixmap(QPixmap(u":/assets/assets/sectors.png"))
        self.advanced_tab_img_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.advanced_tab_img_2, 0, 1, 1, 1)

        self.advanced_tab_img_cpt_1 = QLabel(self.advanced_tab_img_frame)
        self.advanced_tab_img_cpt_1.setObjectName(u"advanced_tab_img_cpt_1")
        sizePolicy1.setHeightForWidth(self.advanced_tab_img_cpt_1.sizePolicy().hasHeightForWidth())
        self.advanced_tab_img_cpt_1.setSizePolicy(sizePolicy1)
        self.advanced_tab_img_cpt_1.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.advanced_tab_img_cpt_1.setWordWrap(True)

        self.gridLayout_6.addWidget(self.advanced_tab_img_cpt_1, 1, 0, 1, 1)

        self.advanced_tab_img_cpt_2 = QLabel(self.advanced_tab_img_frame)
        self.advanced_tab_img_cpt_2.setObjectName(u"advanced_tab_img_cpt_2")
        sizePolicy3.setHeightForWidth(self.advanced_tab_img_cpt_2.sizePolicy().hasHeightForWidth())
        self.advanced_tab_img_cpt_2.setSizePolicy(sizePolicy3)
        self.advanced_tab_img_cpt_2.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.advanced_tab_img_cpt_2.setWordWrap(True)

        self.gridLayout_6.addWidget(self.advanced_tab_img_cpt_2, 1, 1, 1, 1)


        self.gridLayout_5.addWidget(self.advanced_tab_img_frame, 4, 0, 1, 3)

        self.advanced_vert_line = QFrame(self.advancedTab)
        self.advanced_vert_line.setObjectName(u"advanced_vert_line")
        self.advanced_vert_line.setFrameShape(QFrame.Shape.VLine)
        self.advanced_vert_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_5.addWidget(self.advanced_vert_line, 0, 1, 1, 1)

        self.advanced_tab_desc_frame = QFrame(self.advancedTab)
        self.advanced_tab_desc_frame.setObjectName(u"advanced_tab_desc_frame")
        self.advanced_tab_desc_frame.setFrameShape(QFrame.NoFrame)
        self.advanced_tab_desc_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.advanced_tab_desc_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.advanced_tab_desc_title = QLabel(self.advanced_tab_desc_frame)
        self.advanced_tab_desc_title.setObjectName(u"advanced_tab_desc_title")
        sizePolicy1.setHeightForWidth(self.advanced_tab_desc_title.sizePolicy().hasHeightForWidth())
        self.advanced_tab_desc_title.setSizePolicy(sizePolicy1)
        self.advanced_tab_desc_title.setFont(font)
        self.advanced_tab_desc_title.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout_4.addWidget(self.advanced_tab_desc_title)

        self.advanced_tab_desc = QLabel(self.advanced_tab_desc_frame)
        self.advanced_tab_desc.setObjectName(u"advanced_tab_desc")
        self.advanced_tab_desc.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.advanced_tab_desc.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.advanced_tab_desc)


        self.gridLayout_5.addWidget(self.advanced_tab_desc_frame, 0, 2, 1, 1)

        self.advanced_form_frame = QFrame(self.advancedTab)
        self.advanced_form_frame.setObjectName(u"advanced_form_frame")
        sizePolicy4.setHeightForWidth(self.advanced_form_frame.sizePolicy().hasHeightForWidth())
        self.advanced_form_frame.setSizePolicy(sizePolicy4)
        self.advanced_form_frame.setFrameShape(QFrame.NoFrame)
        self.advanced_form_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.advanced_form_frame)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.stem_search_diameter_lbl = QLabel(self.advanced_form_frame)
        self.stem_search_diameter_lbl.setObjectName(u"stem_search_diameter_lbl")

        self.gridLayout_7.addWidget(self.stem_search_diameter_lbl, 1, 0, 1, 1)

        self.section_wid_in = QLineEdit(self.advanced_form_frame)
        self.section_wid_in.setObjectName(u"section_wid_in")
        sizePolicy5.setHeightForWidth(self.section_wid_in.sizePolicy().hasHeightForWidth())
        self.section_wid_in.setSizePolicy(sizePolicy5)
        self.section_wid_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_7.addWidget(self.section_wid_in, 5, 1, 1, 1)

        self.section_wid_ht = QLabel(self.advanced_form_frame)
        self.section_wid_ht.setObjectName(u"section_wid_ht")

        self.gridLayout_7.addWidget(self.section_wid_ht, 5, 2, 1, 1)

        self.section_len_in = QLineEdit(self.advanced_form_frame)
        self.section_len_in.setObjectName(u"section_len_in")
        sizePolicy5.setHeightForWidth(self.section_len_in.sizePolicy().hasHeightForWidth())
        self.section_len_in.setSizePolicy(sizePolicy5)
        self.section_len_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_7.addWidget(self.section_len_in, 4, 1, 1, 1)

        self.stem_search_diameter_in = QLineEdit(self.advanced_form_frame)
        self.stem_search_diameter_in.setObjectName(u"stem_search_diameter_in")
        sizePolicy5.setHeightForWidth(self.stem_search_diameter_in.sizePolicy().hasHeightForWidth())
        self.stem_search_diameter_in.setSizePolicy(sizePolicy5)
        self.stem_search_diameter_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_7.addWidget(self.stem_search_diameter_in, 1, 1, 1, 1)

        self.stem_search_diameter_ht = QLabel(self.advanced_form_frame)
        self.stem_search_diameter_ht.setObjectName(u"stem_search_diameter_ht")

        self.gridLayout_7.addWidget(self.stem_search_diameter_ht, 1, 2, 1, 1)

        self.minimum_height_in = QLineEdit(self.advanced_form_frame)
        self.minimum_height_in.setObjectName(u"minimum_height_in")
        sizePolicy5.setHeightForWidth(self.minimum_height_in.sizePolicy().hasHeightForWidth())
        self.minimum_height_in.setSizePolicy(sizePolicy5)
        self.minimum_height_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_7.addWidget(self.minimum_height_in, 2, 1, 1, 1)

        self.maximum_diameter_ht = QLabel(self.advanced_form_frame)
        self.maximum_diameter_ht.setObjectName(u"maximum_diameter_ht")

        self.gridLayout_7.addWidget(self.maximum_diameter_ht, 0, 2, 1, 1)

        self.maximum_diameter_in = QLineEdit(self.advanced_form_frame)
        self.maximum_diameter_in.setObjectName(u"maximum_diameter_in")
        sizePolicy5.setHeightForWidth(self.maximum_diameter_in.sizePolicy().hasHeightForWidth())
        self.maximum_diameter_in.setSizePolicy(sizePolicy5)
        self.maximum_diameter_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_7.addWidget(self.maximum_diameter_in, 0, 1, 1, 1)

        self.maximum_height_in = QLineEdit(self.advanced_form_frame)
        self.maximum_height_in.setObjectName(u"maximum_height_in")
        sizePolicy5.setHeightForWidth(self.maximum_height_in.sizePolicy().hasHeightForWidth())
        self.maximum_height_in.setSizePolicy(sizePolicy5)
        self.maximum_height_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_7.addWidget(self.maximum_height_in, 3, 1, 1, 1)

        self.minimum_height_lbl = QLabel(self.advanced_form_frame)
        self.minimum_height_lbl.setObjectName(u"minimum_height_lbl")

        self.gridLayout_7.addWidget(self.minimum_height_lbl, 2, 0, 1, 1)

        self.section_len_ht = QLabel(self.advanced_form_frame)
        self.section_len_ht.setObjectName(u"section_len_ht")

        self.gridLayout_7.addWidget(self.section_len_ht, 4, 2, 1, 1)

        self.maximum_height_ht = QLabel(self.advanced_form_frame)
        self.maximum_height_ht.setObjectName(u"maximum_height_ht")

        self.gridLayout_7.addWidget(self.maximum_height_ht, 3, 2, 1, 1)

        self.maximum_diameter_lbl = QLabel(self.advanced_form_frame)
        self.maximum_diameter_lbl.setObjectName(u"maximum_diameter_lbl")

        self.gridLayout_7.addWidget(self.maximum_diameter_lbl, 0, 0, 1, 1)

        self.minimum_height_ht = QLabel(self.advanced_form_frame)
        self.minimum_height_ht.setObjectName(u"minimum_height_ht")

        self.gridLayout_7.addWidget(self.minimum_height_ht, 2, 2, 1, 1)

        self.section_wid_lbl = QLabel(self.advanced_form_frame)
        self.section_wid_lbl.setObjectName(u"section_wid_lbl")

        self.gridLayout_7.addWidget(self.section_wid_lbl, 5, 0, 1, 1)

        self.section_len_lbl = QLabel(self.advanced_form_frame)
        self.section_len_lbl.setObjectName(u"section_len_lbl")

        self.gridLayout_7.addWidget(self.section_len_lbl, 4, 0, 1, 1)

        self.maximum_height_lbl = QLabel(self.advanced_form_frame)
        self.maximum_height_lbl.setObjectName(u"maximum_height_lbl")

        self.gridLayout_7.addWidget(self.maximum_height_lbl, 3, 0, 1, 1)


        self.gridLayout_5.addWidget(self.advanced_form_frame, 0, 0, 1, 1)

        self.tabWidget.addTab(self.advancedTab, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_9 = QGridLayout(self.tab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.axis_upstep_ht = QLabel(self.tab)
        self.axis_upstep_ht.setObjectName(u"axis_upstep_ht")

        self.gridLayout_9.addWidget(self.axis_upstep_ht, 13, 6, 1, 1)

        self.axis_upstep_in = QLineEdit(self.tab)
        self.axis_upstep_in.setObjectName(u"axis_upstep_in")
        self.axis_upstep_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.axis_upstep_in, 13, 5, 1, 1)

        self.diameter_proportion_lbl = QLabel(self.tab)
        self.diameter_proportion_lbl.setObjectName(u"diameter_proportion_lbl")

        self.gridLayout_9.addWidget(self.diameter_proportion_lbl, 2, 4, 1, 1)

        self.verticality_thresh_stripe_in = QLineEdit(self.tab)
        self.verticality_thresh_stripe_in.setObjectName(u"verticality_thresh_stripe_in")
        self.verticality_thresh_stripe_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.verticality_thresh_stripe_in, 5, 1, 1, 1)

        self.minimum_points_in = QLineEdit(self.tab)
        self.minimum_points_in.setObjectName(u"minimum_points_in")
        self.minimum_points_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.minimum_points_in, 11, 1, 1, 1)

        self.res_heights_in = QLineEdit(self.tab)
        self.res_heights_in.setObjectName(u"res_heights_in")
        self.res_heights_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.res_heights_in, 16, 1, 1, 1)

        self.point_threshold_lbl = QLabel(self.tab)
        self.point_threshold_lbl.setObjectName(u"point_threshold_lbl")

        self.gridLayout_9.addWidget(self.point_threshold_lbl, 4, 4, 1, 1)

        self.minimum_diameter_lbl = QLabel(self.tab)
        self.minimum_diameter_lbl.setObjectName(u"minimum_diameter_lbl")

        self.gridLayout_9.addWidget(self.minimum_diameter_lbl, 3, 4, 1, 1)

        self.number_of_points_in = QLineEdit(self.tab)
        self.number_of_points_in.setObjectName(u"number_of_points_in")
        self.number_of_points_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.number_of_points_in, 3, 1, 1, 1)

        self.verticality_scale_stems_lbl = QLabel(self.tab)
        self.verticality_scale_stems_lbl.setObjectName(u"verticality_scale_stems_lbl")

        self.gridLayout_9.addWidget(self.verticality_scale_stems_lbl, 12, 0, 1, 1)

        self.expert_vert_line = QFrame(self.tab)
        self.expert_vert_line.setObjectName(u"expert_vert_line")
        self.expert_vert_line.setFrameShape(QFrame.Shape.VLine)
        self.expert_vert_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_9.addWidget(self.expert_vert_line, 0, 3, 18, 1)

        self.axis_downstep_lbl = QLabel(self.tab)
        self.axis_downstep_lbl.setObjectName(u"axis_downstep_lbl")

        self.gridLayout_9.addWidget(self.axis_downstep_lbl, 12, 4, 1, 1)

        self.res_xy_stripe_ht = QLabel(self.tab)
        self.res_xy_stripe_ht.setObjectName(u"res_xy_stripe_ht")
        sizePolicy7.setHeightForWidth(self.res_xy_stripe_ht.sizePolicy().hasHeightForWidth())
        self.res_xy_stripe_ht.setSizePolicy(sizePolicy7)

        self.gridLayout_9.addWidget(self.res_xy_stripe_ht, 1, 2, 1, 1)

        self.res_z_lbl = QLabel(self.tab)
        self.res_z_lbl.setObjectName(u"res_z_lbl")

        self.gridLayout_9.addWidget(self.res_z_lbl, 10, 0, 1, 1)

        self.res_xy_stripe_in = QLineEdit(self.tab)
        self.res_xy_stripe_in.setObjectName(u"res_xy_stripe_in")
        self.res_xy_stripe_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.res_xy_stripe_in, 1, 1, 1, 1)

        self.maximum_d_ht = QLabel(self.tab)
        self.maximum_d_ht.setObjectName(u"maximum_d_ht")

        self.gridLayout_9.addWidget(self.maximum_d_ht, 14, 2, 1, 1)

        self.height_range_lbl = QLabel(self.tab)
        self.height_range_lbl.setObjectName(u"height_range_lbl")

        self.gridLayout_9.addWidget(self.height_range_lbl, 6, 0, 1, 1)

        self.distance_to_axis_in = QLineEdit(self.tab)
        self.distance_to_axis_in.setObjectName(u"distance_to_axis_in")
        self.distance_to_axis_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.distance_to_axis_in, 15, 1, 1, 1)

        self.drawing_circles_lbl = QLabel(self.tab)
        self.drawing_circles_lbl.setObjectName(u"drawing_circles_lbl")
        self.drawing_circles_lbl.setFont(font)
        self.drawing_circles_lbl.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.drawing_circles_lbl, 9, 4, 1, 2)

        self.height_range_in = QLineEdit(self.tab)
        self.height_range_in.setObjectName(u"height_range_in")
        self.height_range_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.height_range_in, 6, 1, 1, 1)

        self.minimum_diameter_ht = QLabel(self.tab)
        self.minimum_diameter_ht.setObjectName(u"minimum_diameter_ht")

        self.gridLayout_9.addWidget(self.minimum_diameter_ht, 3, 6, 1, 1)

        self.p_interval_ht = QLabel(self.tab)
        self.p_interval_ht.setObjectName(u"p_interval_ht")

        self.gridLayout_9.addWidget(self.p_interval_ht, 11, 6, 1, 1)

        self.number_points_section_in = QLineEdit(self.tab)
        self.number_points_section_in.setObjectName(u"number_points_section_in")
        self.number_points_section_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.number_points_section_in, 1, 5, 1, 1)

        self.minimum_points_lbl = QLabel(self.tab)
        self.minimum_points_lbl.setObjectName(u"minimum_points_lbl")

        self.gridLayout_9.addWidget(self.minimum_points_lbl, 11, 0, 1, 1)

        self.number_of_points_ht = QLabel(self.tab)
        self.number_of_points_ht.setObjectName(u"number_of_points_ht")

        self.gridLayout_9.addWidget(self.number_of_points_ht, 3, 2, 1, 1)

        self.res_z_ht = QLabel(self.tab)
        self.res_z_ht.setObjectName(u"res_z_ht")

        self.gridLayout_9.addWidget(self.res_z_ht, 10, 2, 1, 1)

        self.minimum_diameter_in = QLineEdit(self.tab)
        self.minimum_diameter_in.setObjectName(u"minimum_diameter_in")
        self.minimum_diameter_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.minimum_diameter_in, 3, 5, 1, 1)

        self.number_points_section_lbl = QLabel(self.tab)
        self.number_points_section_lbl.setObjectName(u"number_points_section_lbl")

        self.gridLayout_9.addWidget(self.number_points_section_lbl, 1, 4, 1, 1)

        self.number_sectors_in = QLineEdit(self.tab)
        self.number_sectors_in.setObjectName(u"number_sectors_in")
        self.number_sectors_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.number_sectors_in, 6, 5, 1, 1)

        self.axis_downstep_ht = QLabel(self.tab)
        self.axis_downstep_ht.setObjectName(u"axis_downstep_ht")

        self.gridLayout_9.addWidget(self.axis_downstep_ht, 12, 6, 1, 1)

        self.verticality_scale_stripe_ht = QLabel(self.tab)
        self.verticality_scale_stripe_ht.setObjectName(u"verticality_scale_stripe_ht")

        self.gridLayout_9.addWidget(self.verticality_scale_stripe_ht, 4, 2, 1, 1)

        self.diameter_proportion_ht = QLabel(self.tab)
        self.diameter_proportion_ht.setObjectName(u"diameter_proportion_ht")

        self.gridLayout_9.addWidget(self.diameter_proportion_ht, 2, 6, 1, 1)

        self.diameter_proportion_in = QLineEdit(self.tab)
        self.diameter_proportion_in.setObjectName(u"diameter_proportion_in")
        self.diameter_proportion_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.diameter_proportion_in, 2, 5, 1, 1)

        self.maximum_d_lbl = QLabel(self.tab)
        self.maximum_d_lbl.setObjectName(u"maximum_d_lbl")

        self.gridLayout_9.addWidget(self.maximum_d_lbl, 14, 0, 1, 1)

        self.p_interval_lbl = QLabel(self.tab)
        self.p_interval_lbl.setObjectName(u"p_interval_lbl")

        self.gridLayout_9.addWidget(self.p_interval_lbl, 11, 4, 1, 1)

        self.height_normalization_lb = QLabel(self.tab)
        self.height_normalization_lb.setObjectName(u"height_normalization_lb")
        self.height_normalization_lb.setFont(font)
        self.height_normalization_lb.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.height_normalization_lb, 14, 4, 1, 2)

        self.number_sectors_lbl = QLabel(self.tab)
        self.number_sectors_lbl.setObjectName(u"number_sectors_lbl")

        self.gridLayout_9.addWidget(self.number_sectors_lbl, 6, 4, 1, 1)

        self.maximum_dev_in = QLineEdit(self.tab)
        self.maximum_dev_in.setObjectName(u"maximum_dev_in")
        self.maximum_dev_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.maximum_dev_in, 17, 1, 1, 1)

        self.res_xy_stripe_lbl = QLabel(self.tab)
        self.res_xy_stripe_lbl.setObjectName(u"res_xy_stripe_lbl")

        self.gridLayout_9.addWidget(self.res_xy_stripe_lbl, 1, 0, 1, 1)

        self.maximum_d_in = QLineEdit(self.tab)
        self.maximum_d_in.setObjectName(u"maximum_d_in")
        self.maximum_d_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.maximum_d_in, 14, 1, 1, 1)

        self.verticality_scale_stems_ht = QLabel(self.tab)
        self.verticality_scale_stems_ht.setObjectName(u"verticality_scale_stems_ht")

        self.gridLayout_9.addWidget(self.verticality_scale_stems_ht, 12, 2, 1, 1)

        self.minimum_points_ht = QLabel(self.tab)
        self.minimum_points_ht.setObjectName(u"minimum_points_ht")

        self.gridLayout_9.addWidget(self.minimum_points_ht, 11, 2, 1, 1)

        self.res_xy_in = QLineEdit(self.tab)
        self.res_xy_in.setObjectName(u"res_xy_in")
        self.res_xy_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.res_xy_in, 9, 1, 1, 1)

        self.point_distance_in = QLineEdit(self.tab)
        self.point_distance_in.setObjectName(u"point_distance_in")
        self.point_distance_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.point_distance_in, 5, 5, 1, 1)

        self.expert_info_btn = QPushButton(self.tab)
        self.expert_info_btn.setObjectName(u"expert_info_btn")
        sizePolicy5.setHeightForWidth(self.expert_info_btn.sizePolicy().hasHeightForWidth())
        self.expert_info_btn.setSizePolicy(sizePolicy5)
        self.expert_info_btn.setAutoFillBackground(True)
        icon = QIcon()
        icon.addFile(u":/assets/assets/info_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.expert_info_btn.setIcon(icon)
        self.expert_info_btn.setIconSize(QSize(20, 20))
        self.expert_info_btn.setCheckable(False)
        self.expert_info_btn.setFlat(False)

        self.gridLayout_9.addWidget(self.expert_info_btn, 0, 6, 1, 1)

        self.axis_upstep_lbl = QLabel(self.tab)
        self.axis_upstep_lbl.setObjectName(u"axis_upstep_lbl")

        self.gridLayout_9.addWidget(self.axis_upstep_lbl, 13, 4, 1, 1)

        self.verticality_scale_stripe_in = QLineEdit(self.tab)
        self.verticality_scale_stripe_in.setObjectName(u"verticality_scale_stripe_in")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.verticality_scale_stripe_in.sizePolicy().hasHeightForWidth())
        self.verticality_scale_stripe_in.setSizePolicy(sizePolicy8)
        self.verticality_scale_stripe_in.setMaximumSize(QSize(72, 16777215))
        self.verticality_scale_stripe_in.setLayoutDirection(Qt.LeftToRight)
        self.verticality_scale_stripe_in.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.verticality_scale_stripe_in, 4, 1, 1, 1)

        self.res_z_stripe_ht = QLabel(self.tab)
        self.res_z_stripe_ht.setObjectName(u"res_z_stripe_ht")

        self.gridLayout_9.addWidget(self.res_z_stripe_ht, 2, 2, 1, 1)

        self.res_z_in = QLineEdit(self.tab)
        self.res_z_in.setObjectName(u"res_z_in")
        self.res_z_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.res_z_in, 10, 1, 1, 1)

        self.verticality_scale_stripe_lbl = QLabel(self.tab)
        self.verticality_scale_stripe_lbl.setObjectName(u"verticality_scale_stripe_lbl")

        self.gridLayout_9.addWidget(self.verticality_scale_stripe_lbl, 4, 0, 1, 1)

        self.stem_extraction_lbl = QLabel(self.tab)
        self.stem_extraction_lbl.setObjectName(u"stem_extraction_lbl")
        sizePolicy1.setHeightForWidth(self.stem_extraction_lbl.sizePolicy().hasHeightForWidth())
        self.stem_extraction_lbl.setSizePolicy(sizePolicy1)
        self.stem_extraction_lbl.setFont(font)
        self.stem_extraction_lbl.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout_9.addWidget(self.stem_extraction_lbl, 8, 0, 1, 2)

        self.circle_width_in = QLineEdit(self.tab)
        self.circle_width_in.setObjectName(u"circle_width_in")
        self.circle_width_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.circle_width_in, 8, 5, 1, 1)

        self.axis_downstep_in = QLineEdit(self.tab)
        self.axis_downstep_in.setObjectName(u"axis_downstep_in")
        self.axis_downstep_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.axis_downstep_in, 12, 5, 1, 1)

        self.point_threshold_in = QLineEdit(self.tab)
        self.point_threshold_in.setObjectName(u"point_threshold_in")
        self.point_threshold_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.point_threshold_in, 4, 5, 1, 1)

        self.res_xy_lbl = QLabel(self.tab)
        self.res_xy_lbl.setObjectName(u"res_xy_lbl")

        self.gridLayout_9.addWidget(self.res_xy_lbl, 9, 0, 1, 1)

        self.maximum_dev_ht = QLabel(self.tab)
        self.maximum_dev_ht.setObjectName(u"maximum_dev_ht")

        self.gridLayout_9.addWidget(self.maximum_dev_ht, 17, 2, 1, 1)

        self.m_number_sectors_in = QLineEdit(self.tab)
        self.m_number_sectors_in.setObjectName(u"m_number_sectors_in")
        self.m_number_sectors_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.m_number_sectors_in, 7, 5, 1, 1)

        self.res_z_stripe_in = QLineEdit(self.tab)
        self.res_z_stripe_in.setObjectName(u"res_z_stripe_in")
        self.res_z_stripe_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.res_z_stripe_in, 2, 1, 1, 1)

        self.circle_width_ht = QLabel(self.tab)
        self.circle_width_ht.setObjectName(u"circle_width_ht")

        self.gridLayout_9.addWidget(self.circle_width_ht, 8, 6, 1, 1)

        self.circa_lbl = QLabel(self.tab)
        self.circa_lbl.setObjectName(u"circa_lbl")

        self.gridLayout_9.addWidget(self.circa_lbl, 10, 4, 1, 1)

        self.verticality_thresh_stripe_ht = QLabel(self.tab)
        self.verticality_thresh_stripe_ht.setObjectName(u"verticality_thresh_stripe_ht")

        self.gridLayout_9.addWidget(self.verticality_thresh_stripe_ht, 5, 2, 1, 1)

        self.verticality_scale_stems_in = QLineEdit(self.tab)
        self.verticality_scale_stems_in.setObjectName(u"verticality_scale_stems_in")
        self.verticality_scale_stems_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.verticality_scale_stems_in, 12, 1, 1, 1)

        self.maximum_dev_lbl = QLabel(self.tab)
        self.maximum_dev_lbl.setObjectName(u"maximum_dev_lbl")

        self.gridLayout_9.addWidget(self.maximum_dev_lbl, 17, 0, 1, 1)

        self.point_distance_ht = QLabel(self.tab)
        self.point_distance_ht.setObjectName(u"point_distance_ht")

        self.gridLayout_9.addWidget(self.point_distance_ht, 5, 6, 1, 1)

        self.number_of_points_lbl = QLabel(self.tab)
        self.number_of_points_lbl.setObjectName(u"number_of_points_lbl")

        self.gridLayout_9.addWidget(self.number_of_points_lbl, 3, 0, 1, 1)

        self.verticality_thresh_stems_in = QLineEdit(self.tab)
        self.verticality_thresh_stems_in.setObjectName(u"verticality_thresh_stems_in")
        self.verticality_thresh_stems_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.verticality_thresh_stems_in, 13, 1, 1, 1)

        self.verticality_thresh_stems_ht = QLabel(self.tab)
        self.verticality_thresh_stems_ht.setObjectName(u"verticality_thresh_stems_ht")

        self.gridLayout_9.addWidget(self.verticality_thresh_stems_ht, 13, 2, 1, 1)

        self.res_ground_lbl = QLabel(self.tab)
        self.res_ground_lbl.setObjectName(u"res_ground_lbl")

        self.gridLayout_9.addWidget(self.res_ground_lbl, 15, 4, 1, 1)

        self.min_points_ground_lbl = QLabel(self.tab)
        self.min_points_ground_lbl.setObjectName(u"min_points_ground_lbl")

        self.gridLayout_9.addWidget(self.min_points_ground_lbl, 16, 4, 1, 1)

        self.circle_width_lbl = QLabel(self.tab)
        self.circle_width_lbl.setObjectName(u"circle_width_lbl")

        self.gridLayout_9.addWidget(self.circle_width_lbl, 8, 4, 1, 1)

        self.res_heights_ht = QLabel(self.tab)
        self.res_heights_ht.setObjectName(u"res_heights_ht")

        self.gridLayout_9.addWidget(self.res_heights_ht, 16, 2, 1, 1)

        self.res_z_stripe_lbl = QLabel(self.tab)
        self.res_z_stripe_lbl.setObjectName(u"res_z_stripe_lbl")

        self.gridLayout_9.addWidget(self.res_z_stripe_lbl, 2, 0, 1, 1)

        self.res_heights_lbl = QLabel(self.tab)
        self.res_heights_lbl.setObjectName(u"res_heights_lbl")

        self.gridLayout_9.addWidget(self.res_heights_lbl, 16, 0, 1, 1)

        self.res_ground_ht = QLabel(self.tab)
        self.res_ground_ht.setObjectName(u"res_ground_ht")

        self.gridLayout_9.addWidget(self.res_ground_ht, 15, 6, 1, 1)

        self.spacing_lbl = QLabel(self.tab)
        self.spacing_lbl.setObjectName(u"spacing_lbl")

        self.gridLayout_9.addWidget(self.spacing_lbl, 7, 0, 1, 2)

        self.m_number_sectors_lbl = QLabel(self.tab)
        self.m_number_sectors_lbl.setObjectName(u"m_number_sectors_lbl")

        self.gridLayout_9.addWidget(self.m_number_sectors_lbl, 7, 4, 1, 1)

        self.res_ground_in = QLineEdit(self.tab)
        self.res_ground_in.setObjectName(u"res_ground_in")
        self.res_ground_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.res_ground_in, 15, 5, 1, 1)

        self.height_range_ht = QLabel(self.tab)
        self.height_range_ht.setObjectName(u"height_range_ht")

        self.gridLayout_9.addWidget(self.height_range_ht, 6, 2, 1, 1)

        self.verticality_thresh_stripe_lbl = QLabel(self.tab)
        self.verticality_thresh_stripe_lbl.setObjectName(u"verticality_thresh_stripe_lbl")

        self.gridLayout_9.addWidget(self.verticality_thresh_stripe_lbl, 5, 0, 1, 1)

        self.distance_to_axis_lbl = QLabel(self.tab)
        self.distance_to_axis_lbl.setObjectName(u"distance_to_axis_lbl")

        self.gridLayout_9.addWidget(self.distance_to_axis_lbl, 15, 0, 1, 1)

        self.verticality_thresh_stems_lbl = QLabel(self.tab)
        self.verticality_thresh_stems_lbl.setObjectName(u"verticality_thresh_stems_lbl")

        self.gridLayout_9.addWidget(self.verticality_thresh_stems_lbl, 13, 0, 1, 1)

        self.res_xy_ht = QLabel(self.tab)
        self.res_xy_ht.setObjectName(u"res_xy_ht")

        self.gridLayout_9.addWidget(self.res_xy_ht, 9, 2, 1, 1)

        self.distance_to_axis_ht = QLabel(self.tab)
        self.distance_to_axis_ht.setObjectName(u"distance_to_axis_ht")

        self.gridLayout_9.addWidget(self.distance_to_axis_ht, 15, 2, 1, 1)

        self.point_distance_lbl = QLabel(self.tab)
        self.point_distance_lbl.setObjectName(u"point_distance_lbl")

        self.gridLayout_9.addWidget(self.point_distance_lbl, 5, 4, 1, 1)

        self.computing_sections_lbl = QLabel(self.tab)
        self.computing_sections_lbl.setObjectName(u"computing_sections_lbl")
        self.computing_sections_lbl.setFont(font)
        self.computing_sections_lbl.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.computing_sections_lbl, 0, 4, 1, 2)

        self.circa_in = QLineEdit(self.tab)
        self.circa_in.setObjectName(u"circa_in")
        self.circa_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.circa_in, 10, 5, 1, 1)

        self.p_interval_in = QLineEdit(self.tab)
        self.p_interval_in.setObjectName(u"p_interval_in")
        self.p_interval_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.p_interval_in, 11, 5, 1, 1)

        self.stem_id_lbl = QLabel(self.tab)
        self.stem_id_lbl.setObjectName(u"stem_id_lbl")
        sizePolicy1.setHeightForWidth(self.stem_id_lbl.sizePolicy().hasHeightForWidth())
        self.stem_id_lbl.setSizePolicy(sizePolicy1)
        self.stem_id_lbl.setFont(font)
        self.stem_id_lbl.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout_9.addWidget(self.stem_id_lbl, 0, 0, 1, 2)

        self.min_points_ground_in = QLineEdit(self.tab)
        self.min_points_ground_in.setObjectName(u"min_points_ground_in")
        self.min_points_ground_in.setMaximumSize(QSize(72, 16777215))

        self.gridLayout_9.addWidget(self.min_points_ground_in, 16, 5, 1, 1)

        self.number_points_section_ht = QLabel(self.tab)
        self.number_points_section_ht.setObjectName(u"number_points_section_ht")

        self.gridLayout_9.addWidget(self.number_points_section_ht, 1, 6, 1, 1)

        self.point_threshold_ht = QLabel(self.tab)
        self.point_threshold_ht.setObjectName(u"point_threshold_ht")

        self.gridLayout_9.addWidget(self.point_threshold_ht, 4, 6, 1, 1)

        self.number_sectors_ht = QLabel(self.tab)
        self.number_sectors_ht.setObjectName(u"number_sectors_ht")

        self.gridLayout_9.addWidget(self.number_sectors_ht, 6, 6, 1, 1)

        self.m_number_sectors_ht = QLabel(self.tab)
        self.m_number_sectors_ht.setObjectName(u"m_number_sectors_ht")

        self.gridLayout_9.addWidget(self.m_number_sectors_ht, 7, 6, 1, 1)

        self.circa_ht = QLabel(self.tab)
        self.circa_ht.setObjectName(u"circa_ht")

        self.gridLayout_9.addWidget(self.circa_ht, 10, 6, 1, 1)

        self.min_points_ground_ht = QLabel(self.tab)
        self.min_points_ground_ht.setObjectName(u"min_points_ground_ht")

        self.gridLayout_9.addWidget(self.min_points_ground_ht, 16, 6, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.about_txt = QTextBrowser(self.tab_2)
        self.about_txt.setObjectName(u"about_txt")
        self.about_txt.setEnabled(True)

        self.verticalLayout_3.addWidget(self.about_txt)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.bottomFrame = QFrame(self.centralwidget)
        self.bottomFrame.setObjectName(u"bottomFrame")
        sizePolicy1.setHeightForWidth(self.bottomFrame.sizePolicy().hasHeightForWidth())
        self.bottomFrame.setSizePolicy(sizePolicy1)
        self.bottomFrame.setMinimumSize(QSize(0, 0))
        self.bottomFrame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.bottomFrame.setStyleSheet(u"")
        self.bottomFrame.setFrameShape(QFrame.StyledPanel)
        self.bottomFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.bottomFrame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.output_dir_lbl = QLabel(self.bottomFrame)
        self.output_dir_lbl.setObjectName(u"output_dir_lbl")
        sizePolicy1.setHeightForWidth(self.output_dir_lbl.sizePolicy().hasHeightForWidth())
        self.output_dir_lbl.setSizePolicy(sizePolicy1)
        self.output_dir_lbl.setStyleSheet(u"margin:0px;")

        self.gridLayout_2.addWidget(self.output_dir_lbl, 0, 2, 1, 1)

        self.input_file_lbl = QLabel(self.bottomFrame)
        self.input_file_lbl.setObjectName(u"input_file_lbl")
        sizePolicy1.setHeightForWidth(self.input_file_lbl.sizePolicy().hasHeightForWidth())
        self.input_file_lbl.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.input_file_lbl, 0, 0, 1, 1)

        self.input_file_in = QLineEdit(self.bottomFrame)
        self.input_file_in.setObjectName(u"input_file_in")

        self.gridLayout_2.addWidget(self.input_file_in, 1, 0, 1, 1)

        self.output_dir_in = QLineEdit(self.bottomFrame)
        self.output_dir_in.setObjectName(u"output_dir_in")

        self.gridLayout_2.addWidget(self.output_dir_in, 1, 2, 1, 1)

        self.output_dir_btn = QPushButton(self.bottomFrame)
        self.output_dir_btn.setObjectName(u"output_dir_btn")

        self.gridLayout_2.addWidget(self.output_dir_btn, 1, 3, 1, 1)

        self.input_file_btn = QPushButton(self.bottomFrame)
        self.input_file_btn.setObjectName(u"input_file_btn")

        self.gridLayout_2.addWidget(self.input_file_btn, 1, 1, 1, 1)

        self.compute_btn = QPushButton(self.bottomFrame)
        self.compute_btn.setObjectName(u"compute_btn")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.compute_btn.sizePolicy().hasHeightForWidth())
        self.compute_btn.setSizePolicy(sizePolicy9)
        self.compute_btn.setMinimumSize(QSize(150, 0))
        self.compute_btn.setBaseSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(False)
        self.compute_btn.setFont(font1)
        self.compute_btn.setFlat(False)

        self.gridLayout_2.addWidget(self.compute_btn, 1, 6, 1, 2)

        self.horizontalSpacer = QSpacerItem(50, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 4, 1, 2)


        self.verticalLayout.addWidget(self.bottomFrame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tutorial_link_btn.setDefault(False)
        self.compute_btn.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"3DFin", None))
        self.basic_tab_img_1.setText("")
        self.basic_tab_img_3_title.setText(QCoreApplication.translate("MainWindow", u"Height-normalized cloud", None))
        self.basic_tab_img_1_cpt.setText(QCoreApplication.translate("MainWindow", u"Region where one should expect mostly stems.", None))
        self.tutorial_link_btn.setText(QCoreApplication.translate("MainWindow", u"Tutorial", None))
        self.documentation_link_btn.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.basic_tab_desc.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>3DFin implements our algorithm to detect the trees present in a terrestrial point cloud from a forest plot, and compute individual tree parameters: tree height,tree location, diameters along the stem (including DBH), and tree stem axis. The official paper is available <a href=\"https://academic.oup.com/forestry/article/97/4/479/7680458\"><span style=\" text-decoration: underline; color:#0000ff;\">here</span></a></p><p>3DFin is designed to process ground-based data of any kind (TLS, MLS, photogrammetric point clouds...) that can be used in combination with aerial data (ALS, ULS, aerial photogrammetry), but not to be used with aerial data alone.</p><p>Be sure to check the official paper and the documentation, which features detailed explanations on how the program works, and the tutorial by Fabian Fassnacht, which is a great tool to get started using 3DFin</p></body></html>", None))
        self.basic_3dfin_logo.setText("")
        self.basic_tab_img_1_title.setText(QCoreApplication.translate("MainWindow", u"Stripe", None))
        self.basic_tab_img_3.setText("")
        self.lower_limit_lbl.setText(QCoreApplication.translate("MainWindow", u"Strippe Lower Limit", None))
        self.number_of_iterations_ht.setText(QCoreApplication.translate("MainWindow", u"0-5", None))
        self.res_cloth_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.export_txt_lbl.setText(QCoreApplication.translate("MainWindow", u"Format of output tabular data", None))
        self.export_txt_rb_1.setText(QCoreApplication.translate("MainWindow", u"TXT", None))
        self.upper_limit_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.export_txt_rb_2.setText(QCoreApplication.translate("MainWindow", u"XLSX", None))
        self.number_of_iterations_lbl.setText(QCoreApplication.translate("MainWindow", u"Pruning Intensity", None))
        self.lower_limit_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.res_cloth_lbl.setText(QCoreApplication.translate("MainWindow", u"Cloth resolution", None))
        self.is_noisy_chk.setText(QCoreApplication.translate("MainWindow", u"Clean noise on dtm", None))
        self.z0_name_ht.setText("")
        self.is_normalized_chk.setText(QCoreApplication.translate("MainWindow", u"Normalize point cloud", None))
        self.z0_name_lbl.setText(QCoreApplication.translate("MainWindow", u"Normalized height field name", None))
        self.upper_limit_lbl.setText(QCoreApplication.translate("MainWindow", u"Strippe Upper Limit", None))
        self.basic_tab_img_2.setText("")
        self.basic_tab_img_2_title.setText(QCoreApplication.translate("MainWindow", u"Original cloud", None))
        self.basic_tab_img_2_cpt.setText(QCoreApplication.translate("MainWindow", u"3DFin is able to normalize heights automatically, but also allows using already height-normalized point clouds.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.basicTab), QCoreApplication.translate("MainWindow", u"Basic", None))
        self.advanced_tab_img_1.setText("")
        self.advanced_tab_img_2.setText("")
        self.advanced_tab_img_cpt_1.setText(QCoreApplication.translate("MainWindow", u"A) Sections along the stem B) Detail of computed sections showing the distance between them and their width C) Circle fitting to the points of a section", None))
        self.advanced_tab_img_cpt_2.setText(QCoreApplication.translate("MainWindow", u"Several quality controls are implemented to validate the fitted circles, such as measuring the point distribution along the sections.", None))
        self.advanced_tab_desc_title.setText(QCoreApplication.translate("MainWindow", u"Advanced Parameters", None))
        self.advanced_tab_desc.setText(QCoreApplication.translate("MainWindow", u"If the results obtained by just tweaking basic parameters do not meet your expectations, you might want to modify these.\n"
"\n"
"\n"
"\n"
"You can get a brief description of what they do by hovering the mouse over the info icon right before each parameter. However, keep in mind that a thorough understanding is advisable before changing these. For that, you can get a better grasp of what the algorithm does in the attached documentation. You can easily access it through the documentation button in the bottom-right corner.", None))
        self.stem_search_diameter_lbl.setText(QCoreApplication.translate("MainWindow", u"Stem search diameter", None))
        self.section_wid_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.stem_search_diameter_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.maximum_diameter_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.minimum_height_lbl.setText(QCoreApplication.translate("MainWindow", u"Lowest section", None))
        self.section_len_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.maximum_height_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.maximum_diameter_lbl.setText(QCoreApplication.translate("MainWindow", u"Expected maximum diameter", None))
        self.minimum_height_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.section_wid_lbl.setText(QCoreApplication.translate("MainWindow", u"Section width", None))
        self.section_len_lbl.setText(QCoreApplication.translate("MainWindow", u"Distance between sections", None))
        self.maximum_height_lbl.setText(QCoreApplication.translate("MainWindow", u"Highest section", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.advancedTab), QCoreApplication.translate("MainWindow", u"Advanced", None))
        self.axis_upstep_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.diameter_proportion_lbl.setText(QCoreApplication.translate("MainWindow", u"Inner/outer circle proportion", None))
        self.point_threshold_lbl.setText(QCoreApplication.translate("MainWindow", u"Points within inner circle", None))
        self.minimum_diameter_lbl.setText(QCoreApplication.translate("MainWindow", u"Minimum expected diameter", None))
        self.verticality_scale_stems_lbl.setText(QCoreApplication.translate("MainWindow", u"Vicinity radius (verticality computation)", None))
        self.axis_downstep_lbl.setText(QCoreApplication.translate("MainWindow", u"Axis downstep from stripe center", None))
        self.res_xy_stripe_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.res_z_lbl.setText(QCoreApplication.translate("MainWindow", u"(z) voxel resolution", None))
#if QT_CONFIG(tooltip)
        self.res_xy_stripe_in.setToolTip(QCoreApplication.translate("MainWindow", u"helllpqsd^pqsofkqspofjqpo", None))
#endif // QT_CONFIG(tooltip)
        self.maximum_d_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.height_range_lbl.setText(QCoreApplication.translate("MainWindow", u"Vertical Range", None))
#if QT_CONFIG(tooltip)
        self.drawing_circles_lbl.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.drawing_circles_lbl.setText(QCoreApplication.translate("MainWindow", u"Drawing circles and axes", None))
        self.minimum_diameter_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.p_interval_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.minimum_points_lbl.setText(QCoreApplication.translate("MainWindow", u"Minimum points", None))
        self.number_of_points_ht.setText("")
        self.res_z_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.number_points_section_lbl.setText(QCoreApplication.translate("MainWindow", u"Points within section", None))
        self.axis_downstep_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.verticality_scale_stripe_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.diameter_proportion_ht.setText(QCoreApplication.translate("MainWindow", u"[0,1]", None))
        self.maximum_d_lbl.setText(QCoreApplication.translate("MainWindow", u"Maximum distance to tree axis", None))
        self.p_interval_lbl.setText(QCoreApplication.translate("MainWindow", u"Interval at which points are drawn", None))
        self.height_normalization_lb.setText(QCoreApplication.translate("MainWindow", u"Height normalization", None))
        self.number_sectors_lbl.setText(QCoreApplication.translate("MainWindow", u"Number of sectors", None))
        self.res_xy_stripe_lbl.setText(QCoreApplication.translate("MainWindow", u"(x,y) voxel resolution", None))
        self.verticality_scale_stems_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.minimum_points_ht.setText("")
        self.expert_info_btn.setText("")
        self.axis_upstep_lbl.setText(QCoreApplication.translate("MainWindow", u"Axis upstep from stripe center", None))
        self.res_z_stripe_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.verticality_scale_stripe_lbl.setText(QCoreApplication.translate("MainWindow", u"Vicinity radius (verticality computation)", None))
        self.stem_extraction_lbl.setText(QCoreApplication.translate("MainWindow", u"Stem extraction and tree individualization", None))
        self.res_xy_lbl.setText(QCoreApplication.translate("MainWindow", u"(x, y) voxel resolution", None))
        self.maximum_dev_ht.setText(QCoreApplication.translate("MainWindow", u"degrees", None))
        self.circle_width_ht.setText(QCoreApplication.translate("MainWindow", u"centimeters", None))
        self.circa_lbl.setText(QCoreApplication.translate("MainWindow", u"# of points to draw each circle", None))
        self.verticality_thresh_stripe_ht.setText(QCoreApplication.translate("MainWindow", u"(0,1)", None))
        self.maximum_dev_lbl.setText(QCoreApplication.translate("MainWindow", u"Maximum vertical deviation from axis", None))
        self.point_distance_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.number_of_points_lbl.setText(QCoreApplication.translate("MainWindow", u"Number of points", None))
        self.verticality_thresh_stems_ht.setText(QCoreApplication.translate("MainWindow", u"(0,1)", None))
        self.res_ground_lbl.setText(QCoreApplication.translate("MainWindow", u"(x, y) voxel resolution", None))
        self.min_points_ground_lbl.setText(QCoreApplication.translate("MainWindow", u"Minimum number of points", None))
        self.circle_width_lbl.setText(QCoreApplication.translate("MainWindow", u"Circle width", None))
        self.res_heights_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.res_z_stripe_lbl.setText(QCoreApplication.translate("MainWindow", u"(z) voxel resolution", None))
        self.res_heights_lbl.setText(QCoreApplication.translate("MainWindow", u"Voxel resolution for height computation", None))
        self.res_ground_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.spacing_lbl.setText("")
        self.m_number_sectors_lbl.setText(QCoreApplication.translate("MainWindow", u"Number of occupied sectors", None))
        self.height_range_ht.setText("")
        self.verticality_thresh_stripe_lbl.setText(QCoreApplication.translate("MainWindow", u"Verticality threshold", None))
        self.distance_to_axis_lbl.setText(QCoreApplication.translate("MainWindow", u"Distance from axis", None))
        self.verticality_thresh_stems_lbl.setText(QCoreApplication.translate("MainWindow", u"Verticality threshold", None))
        self.res_xy_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.distance_to_axis_ht.setText(QCoreApplication.translate("MainWindow", u"meters", None))
        self.point_distance_lbl.setText(QCoreApplication.translate("MainWindow", u"Maximum point distance", None))
        self.computing_sections_lbl.setText(QCoreApplication.translate("MainWindow", u"Computing sections", None))
        self.stem_id_lbl.setText(QCoreApplication.translate("MainWindow", u"Stem identification within the stripe", None))
        self.number_points_section_ht.setText("")
        self.point_threshold_ht.setText("")
        self.number_sectors_ht.setText("")
        self.m_number_sectors_ht.setText("")
        self.circa_ht.setText("")
        self.min_points_ground_ht.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Expert", None))
        self.about_txt.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<h1 align=\"center\" style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:704;\">3DFin: Forest Inventory</span></h1>\n"
"<h3 align=\"center\" style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:704;\">Copyright \u00a9 2023 Carlos Cabo &amp; Diego Laino</span></h3>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\""
                        " font-family:'Segoe UI'; font-size:9pt;\">This program comes with ABSOLUTELY NO WARRANTY. This is a free software, and you are welcome to redistribute it under certain conditions. </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">See </span><a href=\"#license\"><span style=\" font-family:'Segoe UI'; font-size:9pt; text-decoration: underline; color:#0000ff;\">LICENSE</span></a><span style=\" font-family:'Segoe UI'; font-size:9pt;\"> at the bottom of this tab for further details.</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:9pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style"
                        "=\" font-family:'Segoe UI'; font-size:9pt;\">This software has been developed at the Centre of Wildfire Research of Swansea University (UK) in collaboration  with the Research Institute of Biodiversity (CSIC, Spain) and the Department of Mining Exploitation of the University of Oviedo (Spain). Funding provided by the UK NERC project (NE/T001194/1): </span><span style=\" font-family:'Segoe UI'; font-size:9pt; font-style:italic;\">'Advancing 3D Fuel Mapping for Wildfire Behaviour and Risk Mitigation Modelling' </span><span style=\" font-family:'Segoe UI'; font-size:9pt;\">and by the Spanish Knowledge Generation project (PID2021-126790NB-I00)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:9pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe"
                        " UI'; font-size:9pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:9pt;\"><br /></p>\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" align=\"center\" cellspacing=\"5\" cellpadding=\"5\">\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/assets/assets/csic_logo_1.png\" /></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/assets/assets/spain_logo_1.png\" /></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/assets/assets/nerc_logo_1.png\" /></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top"
                        ":0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/assets/assets/cetemas_logo_1.png\" /></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/assets/assets/uniovi_logo_1.png\" /></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/assets/assets/swansea_logo_1.png\" /></p></td></tr></table>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:9pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:9pt;\"><br /></p>\n"
"<table border=\"0\" style=\""
                        " margin-top:0px; margin-bottom:0px; margin-left:20px; margin-right:20px;\" cellspacing=\"5\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/assets/assets/carlos_pic_1.jpg\" /></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">Carlos Cabo (carloscabo@uniovi.es). Academic position (PCD) in Geomatics Engineering at the University of Oviedo (Department of Mining Exploitation and Prospection -Cartography, Geodetics and Photogrammetry-), and Honorary Appointment at Science and Engineering Faculty, Swansea University. Research fields: Spatial analysis cartography, geomatics.</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src="
                        "\":/assets/assets/diego_pic_1.jpg\" /></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">Diego Laino (diegolainor@gmail.com). Research technician at Biodiversity Research Institute (CSIC-University of Oviedo-Principality of Asturias). PhD student in Natural Resources Engineering at Department of Mining Exploitation, University of Oviedo. Research fields: deep learning, remote sensing, forestry.</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/assets/assets/covadonga_pic_1.jpg\" /></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">Covadonga Prendes (cprendes@cetemas.es). Forest engineer and re"
                        "searcher at CETEMAS (Forest and Wood Technology Research Centre Foundation). Geomatics research group. Research fields: LiDAR, sustainable forestry development, spatial analysis.</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/assets/assets/cris_pic_1.jpg\" /></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">Cristina Santin (c.santin@csic.es). Research fellow at Biodiversity Research Institute (CSIC-University of Oviedo-Principality of Asturias) and Honorary Assoc. Professor at the Biosciences Department of Swansea University. Research fields: environmental impacts of wildfires.</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px"
                        ";\"><img src=\":/assets/assets/stefan_pic_1.jpg\" /></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">Stefan Doerr (s.doerr@swansea.ac.uk). Full Professor at the Geography Department, Swansea University and Director of its Centre for Wildfire Research. Editor-in-Chief: International Journal of Wildland Fire. Research fields: wildfires, landscape carbon dynamics, soils, water quality, ecosystem services.</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/assets/assets/celestino_pic_1.jpg\" /></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">Celestino Ordonez (ordonezcelestino@uniovi.es). Full "
                        "professor at Department of Mining Exploitation -Cartography, Geodetics and Photogrammetry-, University of Oviedo. Main researcher at GEOGRAPH research group. Research fields: Spatial analysis, laser scanning, photogrammetry.</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/assets/assets/tadas_pic_1.jpg\" /></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">Tadas Nikonovas (tadas.nikonovas@swansea.ac.uk). Office Researcher at Centre for Wildfire Research, Geography Department, Swansea University. Research fields: Global fire activity, atmospheric emissions, fire occurrence modelling. </span></p></td></tr></table>\n"
"<h1 align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:"
                        "0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:9pt; font-weight:704;\"><br /></h1>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:9pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"license\"></a><span style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:704;\">L</span><span style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:704;\">icense</span></p>\n"
"<p style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Cou"
                        "rier New','monospace'; font-size:9pt;\">                    GNU GENERAL PUBLIC LICENSE</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">                       Version 3, 29 June 2007</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"> Copyright (C) 2007 Free Software Foundation, Inc. &lt;https://fsf.org/&gt;</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" fo"
                        "nt-family:'Consolas','Courier New','monospace'; font-size:9pt;\"> Everyone is permitted to copy and distribute verbatim copies</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"> of this license document, but changing it is not allowed.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">                            Preamble</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0"
                        "; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  The GNU General Public License is a free, copyleft license for</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">software and other kinds of works.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Co"
                        "urier New','monospace'; font-size:9pt;\">  The licenses for most software and other practical works are designed</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">to take away your freedom to share and change the works.  By contrast,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the GNU General Public License is intended to guarantee your freedom to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">share and change all versions of a program--to make sure it remains free</span></p>\n"
"<p style=\" margin-top:0px;"
                        " margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">software for all its users.  We, the Free Software Foundation, use the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">GNU General Public License for most of our software; it applies also to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">any other work released this way by its authors.  You can apply it to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace';"
                        " font-size:9pt;\">your programs, too.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  When we speak of free software, we are referring to freedom, not</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">price.  Our General Public Licenses are designed to make sure that you</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New'"
                        ",'monospace'; font-size:9pt;\">have the freedom to distribute copies of free software (and charge for</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">them if you wish), that you receive source code or can get it if you</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">want it, that you can change the software or use pieces of it in new</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">free programs, and that you know you can do these things.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margi"
                        "n-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  To protect your rights, we need to prevent others from denying you</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">these rights or asking you to surrender the rights.  Therefore, you have</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">certain responsibilities if you distribute copies of the software, or if</sp"
                        "an></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">you modify it: responsibilities to respect the freedom of others.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  For example, if you distribute copies of such a program, whether</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">gratis or for a"
                        " fee, you must pass on to the recipients the same</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">freedoms that you received.  You must make sure that they, too, receive</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">or can get the source code.  And you must show them these terms so they</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">know their rights.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"
                        " font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Developers that use the GNU GPL protect your rights with two steps:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">(1) assert copyright on the software, and (2) offer you this License</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">giving you legal permission to copy, distribute and/or modify it.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left"
                        ":0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  For the developers' and authors' protection, the GPL clearly explains</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">that there is no warranty for this free software.  For both users' and</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">authors' sake, the GPL requires that modified versions be marked as</span></p>\n"
"<p style=\" margi"
                        "n-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">changed, so that their problems will not be attributed erroneously to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">authors of previous versions.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Some devices are designed to deny users access to install or run</span></p>"
                        "\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">modified versions of the software inside them, although the manufacturer</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">can do so.  This is fundamentally incompatible with the aim of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">protecting users' freedom to change the software.  The systematic</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Cour"
                        "ier New','monospace'; font-size:9pt;\">pattern of such abuse occurs in the area of products for individuals to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">use, which is precisely where it is most unacceptable.  Therefore, we</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">have designed this version of the GPL to prohibit the practice for those</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">products.  If such problems arise substantially in other domains, we</span></p>\n"
"<p style=\" margin-top:0px; margi"
                        "n-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">stand ready to extend this provision to those domains in future versions</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">of the GPL, as needed to protect the freedom of users.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Finally, every program is threatened constantly by software pat"
                        "ents.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">States should not allow patents to restrict development and use of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">software on general-purpose computers, but in those that do, we wish to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">avoid the special danger that patents applied to a free program could</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-"
                        "family:'Consolas','Courier New','monospace'; font-size:9pt;\">make it effectively proprietary.  To prevent this, the GPL assures that</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">patents cannot be used to render the program non-free.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  The precise terms and conditions for copying, distribution and</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-in"
                        "dent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">modification follow.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">                       TERMS AND CONDITIONS</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courie"
                        "r New','monospace'; font-size:9pt;\">  0. Definitions.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  &quot;This License&quot; refers to version 3 of the GNU General Public License.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">"
                        "  &quot;Copyright&quot; also means copyright-like laws that apply to other kinds of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">works, such as semiconductor masks.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  &quot;The Program&quot; refers to any copyrightable work licensed under this</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'"
                        "Consolas','Courier New','monospace'; font-size:9pt;\">License.  Each licensee is addressed as &quot;you&quot;.  &quot;Licensees&quot; and</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">&quot;recipients&quot; may be individuals or organizations.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  To &quot;modify&quot; a work means to copy from or adapt all or part of the work</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; mar"
                        "gin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">in a fashion requiring copyright permission, other than the making of an</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">exact copy.  The resulting work is called a &quot;modified version&quot; of the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">earlier work or a work &quot;based on&quot; the earlier work.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
""
                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  A &quot;covered work&quot; means either the unmodified Program or a work based</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">on the Program.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  To &quot;propagate&quot; a work means to do anything with it "
                        "that, without</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">permission, would make you directly or secondarily liable for</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">infringement under applicable copyright law, except executing it on a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">computer or modifying a private copy.  Propagation includes copying,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-"
                        "family:'Consolas','Courier New','monospace'; font-size:9pt;\">distribution (with or without modification), making available to the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">public, and in some countries other activities as well.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  To &quot;convey&quot; a work means any kind of propagation that enables other</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;"
                        " -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">parties to make or receive copies.  Mere interaction with a user through</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">a computer network, with no transfer of a copy, is not conveying.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  An interactive user interface displays &quot;Appropriate Legal Notices&quot;</span></p>\n"
"<p style"
                        "=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">to the extent that it includes a convenient and prominently visible</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">feature that (1) displays an appropriate copyright notice, and (2)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">tells the user that there is no warranty for the work (except to the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','m"
                        "onospace'; font-size:9pt;\">extent that warranties are provided), that licensees may convey the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">work under this License, and how to view a copy of this License.  If</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the interface presents a list of user commands or options, such as a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">menu, a prominent item in the list meets this criterion.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-botto"
                        "m:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  1. Source Code.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  The &quot;source code&quot; for a work means the preferred form of the work</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text"
                        "-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">for making modifications to it.  &quot;Object code&quot; means any non-source</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">form of a work.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  A &quot;Standard Interface&quot; means an interface that either is an official</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right"
                        ":0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">standard defined by a recognized standards body, or, in the case of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">interfaces specified for a particular programming language, one that</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">is widely used among developers working in that language.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px"
                        "; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  The &quot;System Libraries&quot; of an executable work include anything, other</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">than the work as a whole, that (a) is included in the normal form of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">packaging a Major Component, but which is not part of that Major</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospac"
                        "e'; font-size:9pt;\">Component, and (b) serves only to enable use of the work with that</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">Major Component, or to implement a Standard Interface for which an</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">implementation is available to the public in source code form.  A</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">&quot;Major Component&quot;, in this context, means a major essential component</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-l"
                        "eft:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">(kernel, window system, and so on) of the specific operating system</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">(if any) on which the executable work runs, or a compiler used to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">produce the work, or an object code interpreter used to run it.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p"
                        " style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  The &quot;Corresponding Source&quot; for a work in object code form means all</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the source code needed to generate, install, and (for an executable</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">work) run the object code and to modify the work, including scripts to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Conso"
                        "las','Courier New','monospace'; font-size:9pt;\">control those activities.  However, it does not include the work's</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">System Libraries, or general-purpose tools or generally available free</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">programs which are used unmodified in performing those activities but</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">which are not part of the work.  For example, Corresponding Source</span></p>\n"
"<p style=\" margin-top:0px; marg"
                        "in-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">includes interface definition files associated with source files for</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the work, and the source code for shared libraries and dynamically</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">linked subprograms that the work is specifically designed to require,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9"
                        "pt;\">such as by intimate data communication or control flow between those</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">subprograms and other parts of the work.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  The Corresponding Source need not include anything that users</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier "
                        "New','monospace'; font-size:9pt;\">can regenerate automatically from other parts of the Corresponding</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">Source.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  The Corresponding Source for a work in source code form is that</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New'"
                        ",'monospace'; font-size:9pt;\">same work.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  2. Basic Permissions.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  All rights granted under this License are granted for the term of</sp"
                        "an></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">copyright on the Program, and are irrevocable provided the stated</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">conditions are met.  This License explicitly affirms your unlimited</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">permission to run the unmodified Program.  The output from running a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consola"
                        "s','Courier New','monospace'; font-size:9pt;\">covered work is covered by this License only if the output, given its</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">content, constitutes a covered work.  This License acknowledges your</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">rights of fair use or other equivalent, as provided by copyright law.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-"
                        "indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  You may make, run and propagate covered works that you do not</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">convey, without conditions so long as your license otherwise remains</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">in force.  You may convey covered works to others for the sole purpose</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">of having them make modifications exclusively for you, o"
                        "r provide you</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">with facilities for running those works, provided that you comply with</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the terms of this License in conveying all material for which you do</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">not control copyright.  Those thus making or running the covered works</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span styl"
                        "e=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">for you must do so exclusively on your behalf, under your direction</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">and control, on terms that prohibit them from making any copies of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">your copyrighted material outside their relationship with you.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0"
                        "px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Conveying under any other circumstances is permitted solely under</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the conditions stated below.  Sublicensing is not allowed; section 10</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">makes it unnecessary.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;"
                        " margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  3. Protecting Users' Legal Rights From Anti-Circumvention Law.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  No covered work shall be deemed part of an effective technological</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">measure under any applicable law fulfilling obligations under article</span></p>\n"
"<p s"
                        "tyle=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">11 of the WIPO copyright treaty adopted on 20 December 1996, or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">similar laws prohibiting or restricting circumvention of such</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">measures.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" m"
                        "argin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  When you convey a covered work, you waive any legal power to forbid</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">circumvention of technological measures to the extent such circumvention</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">is effected by exercising rights under this License with respect to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New',"
                        "'monospace'; font-size:9pt;\">the covered work, and you disclaim any intention to limit operation or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">modification of the work as a means of enforcing, against the work's</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">users, your or third parties' legal rights to forbid circumvention of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">technological measures.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; mar"
                        "gin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  4. Conveying Verbatim Copies.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  You may convey verbatim copies of the Program's source code as you</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span s"
                        "tyle=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">receive it, in any medium, provided that you conspicuously and</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">appropriately publish on each copy an appropriate copyright notice;</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">keep intact all notices stating that this License and any</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">non-permissive terms added in accord with section 7 apply to the code;</span></p>\n"
"<p style=\" margin-to"
                        "p:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">keep intact all notices of the absence of any warranty; and give all</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">recipients a copy of this License along with the Program.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  You may charge any price or no price for each copy t"
                        "hat you convey,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">and you may offer support or warranty protection for a fee.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  5. Conveying Modified Source Versions.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p st"
                        "yle=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  You may convey a work based on the Program, or the modifications to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">produce it from the Program, in the form of source code under the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">terms of section 4, provided that you also meet all of these conditions:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas',"
                        "'Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    a) The work must carry prominent notices stating that you modified</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    it, and giving a relevant date.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9"
                        "pt;\">    b) The work must carry prominent notices stating that it is</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    released under this License and any conditions added under section</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    7.  This requirement modifies the requirement in section 4 to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    &quot;keep intact all notices&quot;.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -"
                        "qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    c) You must license the entire work, as a whole, under this</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    License to anyone who comes into possession of a copy.  This</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    License will therefore apply, along with any applicable section 7</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-"
                        "left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    additional terms, to the whole of the work, and all its parts,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    regardless of how they are packaged.  This License gives no</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    permission to license the work in any other way, but it does not</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    invalidate such pe"
                        "rmission if you have separately received it.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    d) If the work has interactive user interfaces, each must display</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    Appropriate Legal Notices; however, if the Program has interactive</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Co"
                        "urier New','monospace'; font-size:9pt;\">    interfaces that do not display Appropriate Legal Notices, your</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    work need not make them do so.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  A compilation of a covered work with other separate and independent</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\""
                        " font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">works, which are not by their nature extensions of the covered work,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">and which are not combined with it such as to form a larger program,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">in or on a volume of a storage or distribution medium, is called an</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">&quot;aggregate&quot; if the compilation and its resulting copyright are not</span></p>\n"
"<p st"
                        "yle=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">used to limit the access or legal rights of the compilation's users</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">beyond what the individual works permit.  Inclusion of a covered work</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">in an aggregate does not cause this License to apply to the other</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New'"
                        ",'monospace'; font-size:9pt;\">parts of the aggregate.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  6. Conveying Non-Source Forms.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  You may convey a covered work in object code fo"
                        "rm under the terms</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">of sections 4 and 5, provided that you also convey the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">machine-readable Corresponding Source under the terms of this License,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">in one of these ways:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospa"
                        "ce'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    a) Convey the object code in, or embodied in, a physical product</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    (including a physical distribution medium), accompanied by the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    Corresponding Source fixed on a durable physical medium</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" fo"
                        "nt-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    customarily used for software interchange.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    b) Convey the object code in, or embodied in, a physical product</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    (including a physical distribution medium), accompanied by a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; "
                        "text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    written offer, valid for at least three years and valid for as</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    long as you offer spare parts or customer support for that product</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    model, to give anyone who possesses the object code either (1) a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    copy of the Corresponding Source for all the software in th"
                        "e</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    product that is covered by this License, on a durable physical</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    medium customarily used for software interchange, for a price no</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    more than your reasonable cost of physically performing this</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cons"
                        "olas','Courier New','monospace'; font-size:9pt;\">    conveying of source, or (2) access to copy the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    Corresponding Source from a network server at no charge.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    c) Convey individual copies of the object code with a copy of the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0p"
                        "x;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    written offer to provide the Corresponding Source.  This</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    alternative is allowed only occasionally and noncommercially, and</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    only if you received the object code with such an offer, in accord</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    with subsection 6b.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin"
                        "-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    d) Convey the object code by offering access from a designated</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    place (gratis or for a charge), and offer equivalent access to the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    Corresponding Source in the same way through the same place a"
                        "t no</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    further charge.  You need not require recipients to copy the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    Corresponding Source along with the object code.  If the place to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    copy the object code is a network server, the Corresponding Source</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-fami"
                        "ly:'Consolas','Courier New','monospace'; font-size:9pt;\">    may be on a different server (operated by you or a third party)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    that supports equivalent copying facilities, provided you maintain</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    clear directions next to the object code saying where to find the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    Corresponding Source.  Regardless of what server hosts the</span></p>\n"
"<p style=\" margin-top:0px"
                        "; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    Corresponding Source, you remain obligated to ensure that it is</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    available for as long as needed to satisfy these requirements.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    e) Convey the object code using peer-to-peer tr"
                        "ansmission, provided</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    you inform other peers where the object code and Corresponding</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    Source of the work are being offered to the general public at no</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    charge under subsection 6d.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas',"
                        "'Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  A separable portion of the object code, whose source code is excluded</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">from the Corresponding Source as a System Library, need not be</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">included in conveying the object code work.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-i"
                        "ndent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  A &quot;User Product&quot; is either (1) a &quot;consumer product&quot;, which means any</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">tangible personal property which is normally used for personal, family,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">or household purposes, or (2) anything designed or sold for incorporation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom"
                        ":0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">into a dwelling.  In determining whether a product is a consumer product,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">doubtful cases shall be resolved in favor of coverage.  For a particular</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">product received by a particular user, &quot;normally used&quot; refers to a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; fo"
                        "nt-size:9pt;\">typical or common use of that class of product, regardless of the status</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">of the particular user or of the way in which the particular user</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">actually uses, or expects or is expected to use, the product.  A product</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">is a consumer product regardless of whether the product has substantial</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-lef"
                        "t:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">commercial, industrial or non-consumer uses, unless such uses represent</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the only significant mode of use of the product.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  &quot;Installation Information&quot; for a User Product means any methods,</span></p>\n"
"<p s"
                        "tyle=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">procedures, authorization keys, or other information required to install</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">and execute modified versions of a covered work in that User Product from</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">a modified version of its Corresponding Source.  The information must</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas'"
                        ",'Courier New','monospace'; font-size:9pt;\">suffice to ensure that the continued functioning of the modified object</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">code is in no case prevented or interfered with solely because</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">modification has been made.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font"
                        "-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  If you convey an object code work under this section in, or with, or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">specifically for use in, a User Product, and the conveying occurs as</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">part of a transaction in which the right of possession and use of the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">User Product is transferred to the recipient in perpetuity or for a</span></p>\n"
"<p style=\" mar"
                        "gin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">fixed term (regardless of how the transaction is characterized), the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">Corresponding Source conveyed under this section must be accompanied</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">by the Installation Information.  But this requirement does not apply</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','mono"
                        "space'; font-size:9pt;\">if neither you nor any third party retains the ability to install</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">modified object code on the User Product (for example, the work has</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">been installed in ROM).</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Couri"
                        "er New','monospace'; font-size:9pt;\">  The requirement to provide Installation Information does not include a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">requirement to continue to provide support service, warranty, or updates</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">for a work that has been modified or installed by the recipient, or for</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the User Product in which it has been modified or installed.  Access to a</span></p>\n"
"<p style=\" margin-top:0px"
                        "; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">network may be denied when the modification itself materially and</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">adversely affects the operation of the network or violates the rules and</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">protocols for communication across the network.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\""
                        "><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Corresponding Source conveyed, and Installation Information provided,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">in accord with this section must be in a format that is publicly</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">documented (and with an implementation available to the public in</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Con"
                        "solas','Courier New','monospace'; font-size:9pt;\">source code form), and must require no special password or key for</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">unpacking, reading or copying.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  7. Additional Terms.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier "
                        "New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  &quot;Additional permissions&quot; are terms that supplement the terms of this</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">License by making exceptions from one or more of its conditions.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">Additional permissions that are applicable to the entire Program shall</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; te"
                        "xt-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">be treated as though they were included in this License, to the extent</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">that they are valid under applicable law.  If additional permissions</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">apply only to part of the Program, that part may be used separately</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">under those permissions, but the entire Program remains governed"
                        " by</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">this License without regard to the additional permissions.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  When you convey a copy of a covered work, you may at your option</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">remove any addi"
                        "tional permissions from that copy, or from any part of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">it.  (Additional permissions may be written to require their own</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">removal in certain cases when you modify the work.)  You may place</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">additional permissions on material, added by you to a covered work,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;"
                        " text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">for which you have or can give appropriate copyright permission.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Notwithstanding any other provision of this License, for material you</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">add to a covered work, you may (if authorized by the copyright holders of</span></p>\n"
"<p style=\" margin-top:0px; margin-"
                        "bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">that material) supplement the terms of this License with terms:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    a) Disclaiming warranty or limiting liability differently from the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    terms of sections 15 and 16 of this License; or</span></"
                        "p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    b) Requiring preservation of specified reasonable legal notices or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    author attributions in that material or in the Appropriate Legal</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    Notices d"
                        "isplayed by works containing it; or</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    c) Prohibiting misrepresentation of the origin of that material, or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    requiring that modified versions of such material be marked in</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New',"
                        "'monospace'; font-size:9pt;\">    reasonable ways as different from the original version; or</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    d) Limiting the use for publicity purposes of names of licensors or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    authors of the material; or</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-fa"
                        "mily:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    e) Declining to grant rights under trademark law for use of some</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    trade names, trademarks, or service marks; or</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier N"
                        "ew','monospace'; font-size:9pt;\">    f) Requiring indemnification of licensors and authors of that</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    material by anyone who conveys the material (or modified versions of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    it) with contractual assumptions of liability to the recipient, for</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    any liability that these contractual assumptions directly impose on</span></p>\n"
"<p style=\" margin-top:0px; margin-bott"
                        "om:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    those licensors and authors.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  All other non-permissive additional terms are considered &quot;further</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">restrictions&quot; within the meaning of section 10.  If the Program as you</span></p>\n"
"<p"
                        " style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">received it, or any part of it, contains a notice stating that it is</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">governed by this License along with a term that is a further</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">restriction, you may remove that term.  If a license document contains</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New'"
                        ",'monospace'; font-size:9pt;\">a further restriction but permits relicensing or conveying under this</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">License, you may add to a covered work material governed by the terms</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">of that license document, provided that the further restriction does</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">not survive such relicensing or conveying.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; m"
                        "argin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  If you add terms to a covered work in accord with this section, you</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">must place, in the relevant source files, a statement of the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">additional terms that apply to those files, or a notice indicating</span></p>\n"
"<p style=\" margin-t"
                        "op:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">where to find the applicable terms.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Additional terms, permissive or non-permissive, may be stated in the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">form of a separately written license, or stated as exceptions;</span></p>"
                        "\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the above requirements apply either way.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  8. Termination.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-ri"
                        "ght:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  You may not propagate or modify a covered work except as expressly</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">provided under this License.  Any attempt otherwise to propagate or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">modify it is void, and will automatically terminate your rights under</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">this License (including any patent"
                        " licenses granted under the third</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">paragraph of section 11).</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  However, if you cease all violation of this License, then your</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">license from a parti"
                        "cular copyright holder is reinstated (a)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">provisionally, unless and until the copyright holder explicitly and</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">finally terminates your license, and (b) permanently, if the copyright</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">holder fails to notify you of the violation by some reasonable means</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-"
                        "indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">prior to 60 days after the cessation.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Moreover, your license from a particular copyright holder is</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">reinstated permanently if the copyright holder notifies you of the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -q"
                        "t-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">violation by some reasonable means, this is the first time you have</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">received notice of violation of this License (for any work) from that</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">copyright holder, and you cure the violation prior to 30 days after</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">your receipt of the notice.</span></p>\n"
"<p "
                        "style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Termination of your rights under this section does not terminate the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">licenses of parties who have received copies or rights from you under</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">this License.  If your"
                        " rights have been terminated and not permanently</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">reinstated, you do not qualify to receive new licenses for the same</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">material under section 10.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"> "
                        " 9. Acceptance Not Required for Having Copies.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  You are not required to accept this License in order to receive or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">run a copy of the Program.  Ancillary propagation of a covered work</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Cour"
                        "ier New','monospace'; font-size:9pt;\">occurring solely as a consequence of using peer-to-peer transmission</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">to receive a copy likewise does not require acceptance.  However,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">nothing other than this License grants you permission to propagate or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">modify any covered work.  These actions infringe copyright if you do</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0"
                        "px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">not accept this License.  Therefore, by modifying or propagating a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">covered work, you indicate your acceptance of this License to do so.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  10. Automatic Licensing of Downstream Recipients.</span></p>\n"
""
                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Each time you convey a covered work, the recipient automatically</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">receives a license from the original licensors, to run, modify and</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">propagate that work, subje"
                        "ct to this License.  You are not responsible</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">for enforcing compliance by third parties with this License.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  An &quot;entity transaction&quot; is a transaction transferring control of an</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Co"
                        "urier New','monospace'; font-size:9pt;\">organization, or substantially all assets of one, or subdividing an</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">organization, or merging organizations.  If propagation of a covered</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">work results from an entity transaction, each party to that</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">transaction who receives a copy of the work also receives whatever</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; marg"
                        "in-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">licenses to the work the party's predecessor in interest had or could</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">give under the previous paragraph, plus a right to possession of the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">Corresponding Source of the work from the predecessor in interest, if</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the predec"
                        "essor has it or can get it with reasonable efforts.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  You may not impose any further restrictions on the exercise of the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">rights granted or affirmed under this License.  For example, you may</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas'"
                        ",'Courier New','monospace'; font-size:9pt;\">not impose a license fee, royalty, or other charge for exercise of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">rights granted under this License, and you may not initiate litigation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">(including a cross-claim or counterclaim in a lawsuit) alleging that</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">any patent claim is infringed by making, using, selling, offering for</span></p>\n"
"<p style=\" margin-top:0px; margin"
                        "-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">sale, or importing the Program or any portion of it.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  11. Patents.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; t"
                        "ext-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  A &quot;contributor&quot; is a copyright holder who authorizes use under this</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">License of the Program or a work on which the Program is based.  The</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">work thus licensed is called the contributor's &quot;contributor version&quot;.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-"
                        "top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  A contributor's &quot;essential patent claims&quot; are all patent claims</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">owned or controlled by the contributor, whether already acquired or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">hereafter acquired, that would be infringed by some manner, permitted</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','mo"
                        "nospace'; font-size:9pt;\">by this License, of making, using, or selling its contributor version,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">but do not include claims that would be infringed only as a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">consequence of further modification of the contributor version.  For</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">purposes of this definition, &quot;control&quot; includes the right to grant</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margi"
                        "n-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">patent sublicenses in a manner consistent with the requirements of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">this License.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Each contributor grants you a non-exclusive, worldwide, royalty-free</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px"
                        "; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">patent license under the contributor's essential patent claims, to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">make, use, sell, offer for sale, import and otherwise run, modify and</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">propagate the contents of its contributor version.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p"
                        " style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  In the following three paragraphs, a &quot;patent license&quot; is any express</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">agreement or commitment, however denominated, not to enforce a patent</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">(such as an express permission to practice a patent or covenant not to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Co"
                        "nsolas','Courier New','monospace'; font-size:9pt;\">sue for patent infringement).  To &quot;grant&quot; such a patent license to a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">party means to make such an agreement or commitment not to enforce a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">patent against the party.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><"
                        "span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  If you convey a covered work, knowingly relying on a patent license,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">and the Corresponding Source of the work is not available for anyone</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">to copy, free of charge and under the terms of this License, through a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">publicly available network server or other readily accessible means,</span></p>"
                        "\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">then you must either (1) cause the Corresponding Source to be so</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">available, or (2) arrange to deprive yourself of the benefit of the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">patent license for this particular work, or (3) arrange, in a manner</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Cour"
                        "ier New','monospace'; font-size:9pt;\">consistent with the requirements of this License, to extend the patent</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">license to downstream recipients.  &quot;Knowingly relying&quot; means you have</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">actual knowledge that, but for the patent license, your conveying the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">covered work in a country, or your recipient's use of the covered work</span></p>\n"
"<p style=\" margin-top:0p"
                        "x; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">in a country, would infringe one or more identifiable patents in that</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">country that you have reason to believe are valid.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  If, pursuant to or in connection with a single transaction or<"
                        "/span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">arrangement, you convey, or propagate by procuring conveyance of, a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">covered work, and grant a patent license to some of the parties</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">receiving the covered work authorizing them to use, propagate, modify</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Conso"
                        "las','Courier New','monospace'; font-size:9pt;\">or convey a specific copy of the covered work, then the patent license</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">you grant is automatically extended to all recipients of the covered</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">work and works based on it.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span styl"
                        "e=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  A patent license is &quot;discriminatory&quot; if it does not include within</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the scope of its coverage, prohibits the exercise of, or is</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">conditioned on the non-exercise of one or more of the rights that are</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">specifically granted under this License.  You may not convey a covered</span></p>\n"
"<p s"
                        "tyle=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">work if you are a party to an arrangement with a third party that is</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">in the business of distributing software, under which you make payment</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">to the third party based on the extent of your activity of conveying</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courie"
                        "r New','monospace'; font-size:9pt;\">the work, and under which the third party grants, to any of the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">parties who would receive the covered work from you, a discriminatory</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">patent license (a) in connection with copies of the covered work</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">conveyed by you (or copies made from those copies), or (b) primarily</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; marg"
                        "in-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">for and in connection with specific products or compilations that</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">contain the covered work, unless you entered into that arrangement,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">or that patent license was granted, prior to 28 March 2007.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p"
                        " style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Nothing in this License shall be construed as excluding or limiting</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">any implied license or other defenses to infringement that may</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">otherwise be available to you under applicable patent law.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New',"
                        "'monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  12. No Surrender of Others' Freedom.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  If conditions are imposed on you (whether by court order, agreement or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">oth"
                        "erwise) that contradict the conditions of this License, they do not</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">excuse you from the conditions of this License.  If you cannot convey a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">covered work so as to satisfy simultaneously your obligations under this</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">License and any other pertinent obligations, then as a consequence you may</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; marg"
                        "in-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">not convey it at all.  For example, if you agree to terms that obligate you</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">to collect a royalty for further conveying from those to whom you convey</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the Program, the only way you could satisfy both those terms and this</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">License would be "
                        "to refrain entirely from conveying the Program.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  13. Use with the GNU Affero General Public License.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Notwithstanding any other provisi"
                        "on of this License, you have</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">permission to link or combine any covered work with a work licensed</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">under version 3 of the GNU Affero General Public License into a single</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">combined work, and to convey the resulting work.  The terms of this</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\""
                        "><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">License will continue to apply to the part which is the covered work,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">but the special requirements of the GNU Affero General Public License,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">section 13, concerning interaction through a network will apply to the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">combination as such.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; mar"
                        "gin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  14. Revised Versions of this License.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  The Free Software Foundation may publish revised and/or new versions of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;"
                        " margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the GNU General Public License from time to time.  Such new versions will</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">be similar in spirit to the present version, but may differ in detail to</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">address new problems or concerns.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px;"
                        " margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Each version is given a distinguishing version number.  If the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">Program specifies that a certain numbered version of the GNU General</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">Public License &quot;or any later version&quot; applies to it, you have the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; fo"
                        "nt-size:9pt;\">option of following the terms and conditions either of that numbered</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">version or of any later version published by the Free Software</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">Foundation.  If the Program does not specify a version number of the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">GNU General Public License, you may choose any version ever published</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin"
                        "-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">by the Free Software Foundation.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  If the Program specifies that a proxy can decide which future</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">versions of the GNU General Public License can be used, that proxy's</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; ma"
                        "rgin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">public statement of acceptance of a version permanently authorizes you</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">to choose that version for the Program.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  Later license versions may give you additional or different</span></p>\n"
"<p style=\" margin-to"
                        "p:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">permissions.  However, no additional obligations are imposed on any</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">author or copyright holder as a result of your choosing to follow a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">later version.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" mar"
                        "gin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  15. Disclaimer of Warranty.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT</span><"
                        "/p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM &quot;AS IS&quot; WITHOUT WARRANTY</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\""
                        " font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">ALL NECESSARY SERVICING, REPAIR OR CORRECTION.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt"
                        "-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  16. Limitation of Liability.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin"
                        "-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\""
                        ">DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">SUCH DAMAGES.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-in"
                        "dent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  17. Interpretation of Sections 15 and 16.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  If the disclaimer of warranty and limitation of liability provided</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-fa"
                        "mily:'Consolas','Courier New','monospace'; font-size:9pt;\">above cannot be given local legal effect according to their terms,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">reviewing courts shall apply local law that most closely approximates</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">an absolute waiver of all civil liability in connection with the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">Program, unless a warranty or assumption of liability accompanies a</span></p>\n"
"<p style=\" margin-top:0px"
                        "; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">copy of the Program in return for a fee.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">                     END OF TERMS AND CONDITIONS</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-ri"
                        "ght:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">            How to Apply These Terms to Your New Programs</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  If you develop a new program, and you want it to be of the greatest</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">possible use to the public, the best way to achieve this is to make it</span></p>\n"
"<p style=\" margin-"
                        "top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">free software which everyone can redistribute and change under these terms.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  To do so, attach the following notices to the program.  It is safest</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">to attach them to the start of e"
                        "ach source file to most effectively</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">state the exclusion of warranty; and each file should have at least</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the &quot;copyright&quot; line and a pointer to where the full notice is found.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Cour"
                        "ier New','monospace'; font-size:9pt;\">    &lt;one line to give the program's name and a brief idea of what it does.&gt;</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    Copyright (C) &lt;year&gt;  &lt;name of author&gt;</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    This program is free software: you can redistribute it and/or modify</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:"
                        "0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    it under the terms of the GNU General Public License as published by</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    the Free Software Foundation, either version 3 of the License, or</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    (at your option) any later version.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0p"
                        "x; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    This program is distributed in the hope that it will be useful,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    but WITHOUT ANY WARRANTY; without even the implied warranty of</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    GNU General Public Licen"
                        "se for more details.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    You should have received a copy of the GNU General Public License</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    along with this program.  If not, see &lt;https://www.gnu.org/licenses/&gt;.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier "
                        "New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">Also add information on how to contact you by electronic and paper mail.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  If the program does terminal interaction, make it output a short</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New',"
                        "'monospace'; font-size:9pt;\">notice like this when it starts in an interactive mode:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    &lt;program&gt;  Copyright (C) &lt;year&gt;  &lt;name of author&gt;</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-inde"
                        "nt:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    This is free software, and you are welcome to redistribute it</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">    under certain conditions; type `show c' for details.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">The hypothetical commands `show w' and `show c' should show the appropriate</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-lef"
                        "t:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">parts of the General Public License.  Of course, your program's commands</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">might be different; for a GUI interface, you would use an &quot;about box&quot;.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  You should also get your employer (if you work as a programme"
                        "r) or school,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">if any, to sign a &quot;copyright disclaimer&quot; for the program, if necessary.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">For more information on this, and how to apply and follow the GNU GPL, see</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">&lt;https://www.gnu.org/licenses/&gt;.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; fo"
                        "nt-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">  The GNU General Public License does not permit incorporating your program</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">into proprietary programs.  If your program is a subroutine library, you</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">may consider it more useful to permit linking proprietary applications with</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; ma"
                        "rgin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">the library.  If this is what you want to do, use the GNU Lesser General</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">Public License instead of this License.  But first, please read</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\">&lt;https://www.gnu.org/licenses/why-not-lgpl.html&gt;.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:9pt;\"><br /></span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"About", None))
        self.output_dir_lbl.setText(QCoreApplication.translate("MainWindow", u"Output Directory", None))
        self.input_file_lbl.setText(QCoreApplication.translate("MainWindow", u"Input File", None))
        self.output_dir_btn.setText(QCoreApplication.translate("MainWindow", u"Select dir", None))
        self.input_file_btn.setText(QCoreApplication.translate("MainWindow", u"Select file", None))
        self.compute_btn.setText(QCoreApplication.translate("MainWindow", u"Compute", None))
    # retranslateUi

