# Form implementation generated from reading ui file '/Users/pinxun/Documents/MindX/PTI/HTLO-PTI03/PTI_VinhPhat_HaoNan/ui/item.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 550)
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 61))
        self.label.setText("")
        self.label.setObjectName("label")
        self.lbl_name = QtWidgets.QLabel(parent=Form)
        self.lbl_name.setGeometry(QtCore.QRect(0, 410, 291, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl_name.setFont(font)
        self.lbl_name.setObjectName("lbl_name")
        self.lbl_image = QtWidgets.QLabel(parent=Form)
        self.lbl_image.setGeometry(QtCore.QRect(0, 0, 300, 400))
        self.lbl_image.setStyleSheet("border: 2px solid white;\n"
"border-radius: 5px;")
        self.lbl_image.setText("")
        self.lbl_image.setScaledContents(True)
        self.lbl_image.setObjectName("lbl_image")
        self.btn_edit = QtWidgets.QPushButton(parent=Form)
        self.btn_edit.setGeometry(QtCore.QRect(0, 440, 121, 41))
        self.btn_edit.setObjectName("btn_edit")
        self.btn_delete = QtWidgets.QPushButton(parent=Form)
        self.btn_delete.setGeometry(QtCore.QRect(170, 440, 121, 41))
        self.btn_delete.setObjectName("btn_delete")
        self.btn_detail = QtWidgets.QPushButton(parent=Form)
        self.btn_detail.setGeometry(QtCore.QRect(80, 490, 121, 41))
        self.btn_detail.setObjectName("btn_detail")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lbl_name.setText(_translate("Form", "TextLabel"))
        self.btn_edit.setText(_translate("Form", "Edit"))
        self.btn_delete.setText(_translate("Form", "Delete"))
        self.btn_detail.setText(_translate("Form", "Detail"))
