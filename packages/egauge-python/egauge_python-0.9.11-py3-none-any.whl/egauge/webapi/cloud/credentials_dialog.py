#
#   Copyright (c) 2021-2022, 2024 eGauge Systems LLC
#     1644 Conestoga St, Suite 2
#     Boulder, CO 80301
#     voice: 720-545-9767
#     email: dave@egauge.net
#
#   All rights reserved.
#
#   This code is the property of eGauge Systems LLC and may not be
#   copied, modified, or disclosed without any prior and written
#   permission from eGauge Systems LLC.
#
from PySide6.QtWidgets import QDialog

from .gui.credentials_dialog import Ui_Credentials_Dialog

# pyright: reportIncompatibleVariableOverride = false
#
# Unfortunately, we need the above because PySide automatically
# defines a Signal called `accepted` but the users of this dialog
# expected that property to be a bool indicating whether or not the
# user clicked the "OK" button.
#


class CredentialsDialog(QDialog, Ui_Credentials_Dialog):
    @property
    def accepted(self) -> bool:
        return self.user_accepted

    def __init__(self, parent, failed):
        self.username = None
        self.user_accepted = False
        self.password = None
        self.token = ""
        super().__init__(parent)
        self.setupUi(self)
        if failed:
            prompt = "Login failed. " + self.prompt_label.text()
            self.prompt_label.setText(prompt)
        self.username_lineEdit.setFocus()

    def exec(self) -> int:
        self.user_accepted = False
        return super().exec()

    def accept(self):
        super().accept()
        self.user_accepted = True
        self.username = self.username_lineEdit.text()
        self.password = self.password_lineEdit.text()
        self.token = self.token_lineEdit.text()


# Alias for backwards-compatibility.  Please use CredentialsDialog in
# new code.
Credentials_Dialog = CredentialsDialog
