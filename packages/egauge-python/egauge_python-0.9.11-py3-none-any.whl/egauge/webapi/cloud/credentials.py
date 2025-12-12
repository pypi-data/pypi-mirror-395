#!/usr/bin/env python3
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
"""This module provides a credentials manager which can ask for
credentials (username, password, second factor) either via a PySide
dialog or by prompting the user via stdout and stdin (i.e., the
terminal).

"""

import getpass

CredentialsDialog = None

try:
    from .credentials_dialog import CredentialsDialog

    have_pyside = True
except (ImportError, ModuleNotFoundError):
    have_pyside = False


class LoginCanceled(Exception):
    """Raised when the user cancels a login request."""


class CredentialsManager:
    def __init__(self, gui_parent=None):
        """Create a credentials manager.  The task of this manager is mainly
        to track if a previous login failed.  The user of this object
        should set the previous_login_failed member to False after the
        credentials have been used successfully.

        If GUI_PARENT is not None, it must be the QT5 (PySide6) parent
        window to use for the dialog.  If it is None, the credentials
        will be requested via standard I/O (getpass).

        """
        self.parent = gui_parent if have_pyside else None
        self.previous_login_failed = False

    def ask(self):
        """Ask for the username, password, and optional token for an eGauge
        cloud API account (eGuard account).  Returns a tuple
        containing a username and password or raises LoginCanceled if
        the user presses the "Cancel" button.

        """
        if self.parent and CredentialsDialog is not None:
            dialog = CredentialsDialog(self.parent, self.previous_login_failed)
            dialog.exec()
            if not dialog.accepted:
                raise LoginCanceled()
            self.previous_login_failed = True
            pwd = "" if dialog.password is None else dialog.password
            if dialog.token is not None:
                pwd += dialog.token
            return (dialog.username, pwd)

        fail_msg = ""
        if self.previous_login_failed:
            fail_msg = "Login failed.  "
        print(fail_msg + "Please enter eGuard credentials.")
        try:
            usr = input("Username: ")
            pwd = getpass.getpass(prompt="Password[+token]: ")
        except (KeyboardInterrupt, EOFError) as e:
            raise LoginCanceled from e
        self.previous_login_failed = True
        return [usr, pwd]


# Alias for backwards-compatibility.  Please use CredentialsManager in
# new code.
Credentials_Manager = CredentialsManager
