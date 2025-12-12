#
#   Copyright (c) 2025 eGauge Systems LLC
#       4805 Sterling Dr, Suite 1
#       Boulder, CO 80301
#       voice: 720-545-9767
#       email: davidm@egauge.net
#
#   All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
"""MainWindow wrapper class to handle unhandled exceptions."""

import sys
import traceback
from pathlib import Path
from typing import Callable

from PySide6.QtWidgets import QDialog, QMainWindow

from .gui.exception_dialog import Ui_Exception_Dialog


class ExceptionDialog(QDialog, Ui_Exception_Dialog):
    def __init__(self, parent, title: str, summary: str, detail: str):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.summaryText.setText(summary)
        self.detailPlainText.setPlainText(detail)
        self.detailPlainText.setVisible(False)
        self.detailButton.clicked.connect(self.show_or_hide_detail)
        self.detail_showing = True
        self.show_or_hide_detail()

    def show_or_hide_detail(self):
        if self.detail_showing:
            self.detailButton.setText("Show Details…")
        else:
            self.detailButton.setText("Hide Details…")
        self.detail_showing = not self.detail_showing
        self.detailPlainText.setVisible(self.detail_showing)


class MainWindow(QMainWindow):
    """A PySide app can extend this class rather than QMainWindow to
    handle unhandled exceptions in a more graceful manner.  By
    default, the original `sys.excepthook` is called and then an error
    dialog box is displayed.  When the dialog box is acknowledged by
    the user, the app will terminate.

    An app can override method `handle_unhandled_exception()` to
    further customize the behavior.

    """

    _mw_orig_excepthook: Callable | None = None
    _mw_prog_name: str | None = None

    def __init__(self, *args, **kwargs):
        self._mw_prog_name = Path(sys.argv[0]).name

        if MainWindow._mw_orig_excepthook is None:
            MainWindow._mw_orig_excepthook = sys.excepthook
            sys.excepthook = self.handle_unhandled_exception

        super().__init__(*args, **kwargs)

    def handle_unhandled_exception(self, exc_type, value, tb):
        """A PySide app may customize this method by extending or
        overriding it.

        """
        if MainWindow._mw_orig_excepthook:
            MainWindow._mw_orig_excepthook(exc_type, value, tb)

        info = exc_type.__name__
        if value and str(value):
            info += ": " + str(value)

        msg = (
            f"Unhandled exception occured:"
            f"<p><font color='#c00'>{info}</font></p>"
        )
        dialog = ExceptionDialog(
            self,
            f"{self._mw_prog_name} error",
            msg,
            "".join(traceback.format_tb(tb)),
        )
        dialog.exec()
        sys.exit(1)
