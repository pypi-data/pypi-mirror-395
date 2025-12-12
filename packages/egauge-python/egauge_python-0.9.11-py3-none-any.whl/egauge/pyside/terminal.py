#
#   Copyright (c) 2014, 2016-2017, 2020, 2025 eGauge Systems LLC
#       1644 Conestoga St, Suite 2
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
"""Basic terminal emulation for QT."""

import os
import re

from PySide6 import QtCore
from PySide6.QtGui import QCursor, QTextCursor
from PySide6.QtWidgets import QApplication

from . import ansi2html

CLEAR_LINE_PATTERN = re.compile(r".*\033\[2K")
CURSOR_REPORT_PATTERN = re.compile(r"\033\[6n")
# ANSI CSI sequence: ESC [ followed by any number of parameter bytes in
# range 0x30-0x3f, followed by any number of intermediate bytes in
# range 0x20-0x2f, followed by a single final byte in range 0x40-0x74:
INCOMPLETE_ANSI_CSI_PATTERN = re.compile(r"\033(\[([0-?]*[ -/]*)?)?")


def split_keepends(string: str, pattern: re.Pattern) -> list[str]:
    res = []
    while len(string) > 0:
        m = re.search(pattern, string)
        if m:
            last_matched = m.end(0)
            res.append(string[0:last_matched])
            string = string[last_matched:]
        else:
            res.append(string)
            break
    return res


def incomplete_ansi_csi(string: str) -> bool:
    """Return True if the string forms a partial ANSI CSI ESCape sequence,
    False otherwise.

    """
    m = INCOMPLETE_ANSI_CSI_PATTERN.match(string)
    if m is None:
        return False
    return m.end() == len(string)


class Terminal:
    """Provides basic terminal emulation for a QT plain text widget."""

    def __init__(self, plain_text_edit):
        if "FORCE_COLOR" not in os.environ:
            os.environ["FORCE_COLOR"] = "1"

        self.plain_text_edit = plain_text_edit
        self.partial_line = ""

    def write(self, string: str):
        """Write a string to the terminal.

        The string may consist of multiple lines.

        Required arguments:

        string -- The string to write to the terminal.

        """

        if len(string) == 0:
            return

        string = self.partial_line + string
        self.partial_line = ""

        # if the string ends with an incomplete ANSI CSI sequence,
        # hold off processing the partial escape sequence until it's
        # complete but process the text up to that point immediately:
        for m in re.finditer(r"\033", string):
            if incomplete_ansi_csi(string[m.start() :]):
                self.partial_line = string[m.start() :]
                string = string[0 : m.start()]
                break
        if len(self.partial_line) == 0 and string[-1] == "\r":
            # if the string ends with a carriage-return, hold off
            # processing the carriage return until we get the next
            # character:
            self.partial_line = "\r"
            string = string[:-1]

        lines = split_keepends(string, re.compile("(\r\n|\n|\r|\b)"))
        for line in lines:
            # position cursor at end of text (in case someone clicked in
            # the middle of the text):
            cursor = self.plain_text_edit.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.plain_text_edit.setTextCursor(cursor)

            back_space = False
            line_feed = False
            txt = line
            if len(txt) >= 1:
                if txt[-1] == "\b":
                    back_space = True
                    txt = txt[:-1]
                elif txt[-1] == "\r":
                    txt = ""
                    cursor.movePosition(
                        QTextCursor.MoveOperation.StartOfBlock,
                        QTextCursor.MoveMode.KeepAnchor,
                    )
                    cursor.removeSelectedText()
                elif len(txt) >= 2 and txt[-2] == "\r" and txt[-1] == "\n":
                    txt = txt[:-2]
                    line_feed = True
                elif txt[-1] == "\n":
                    txt = txt[:-1]
                    line_feed = True
            txt = CURSOR_REPORT_PATTERN.sub("", txt)
            m = CLEAR_LINE_PATTERN.match(txt)
            if m:
                txt = txt[m.end() :]
                cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
                cursor.movePosition(
                    QTextCursor.MoveOperation.EndOfBlock,
                    QTextCursor.MoveMode.KeepAnchor,
                )
                cursor.removeSelectedText()

            if len(txt) > 0:
                # Unfortunately, the "<pre>" seems to for the font to
                # "Courier New" but without "<pre>" whitespace is not
                # preserved by insertHtml.  Argh...
                # Use qt5ct to configure the "Fixed width" font which will
                # be used for <pre>.
                html = "<pre>" + ansi2html.convert(txt) + "</pre>"
                cursor.insertHtml(html)
            if back_space:
                cursor.deletePreviousChar()
                QApplication.processEvents()
            elif line_feed:
                # Each appendHtml() writes a separate line.  Newline
                # characters are ignored.
                self.plain_text_edit.appendHtml("")
        self.plain_text_edit.centerCursor()

    def flush(self):
        """Flush pending output."""
        QApplication.processEvents(
            QtCore.QEventLoop.ProcessEventsFlag.AllEvents, 1
        )


def test_incomplete_ansi_csi(seq: str):
    print("Testing: " + seq)
    CSI = "\033["
    csi_seq = CSI + seq
    for l in range(len(csi_seq) - 1):
        if not incomplete_ansi_csi(csi_seq[0 : l + 1]):
            print(f"Error: CSI test sequence {seq}, l={l} returned False")
    if incomplete_ansi_csi(csi_seq):
        print(f"Error: CSI test sequence {seq} returned True")


def test():
    if incomplete_ansi_csi("hi there"):
        print('Error: CSI test sequence "hi there" returned True')
    if incomplete_ansi_csi("x\033[s"):
        print('Error: CSI test sequence "xCSIs" returned True')
    test_incomplete_ansi_csi("6n")
    test_incomplete_ansi_csi("16;34H")  # set cursor position
    test_incomplete_ansi_csi("s")  # save cursor position

    import sys

    from PySide6 import QtCore, QtWidgets
    from PySide6.QtCore import QBasicTimer
    from PySide6.QtWidgets import QApplication, QMainWindow

    class Ui_MainWindow:
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("Terminal Test")
            MainWindow.resize(908, 480)
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
            self.verticalLayout.setObjectName("verticalLayout")
            self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
            self.plainTextEdit.setObjectName("plainTextEdit")
            self.plainTextEdit.viewport().setProperty(
                "cursor", QCursor(QtCore.Qt.CursorShape.IBeamCursor)
            )
            self.plainTextEdit.setMouseTracking(False)
            self.plainTextEdit.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            self.plainTextEdit.setAcceptDrops(False)
            self.plainTextEdit.setStyleSheet(
                "background-color: black;\ncolor: white;\n"
            )
            self.plainTextEdit.setLineWidth(1)
            self.plainTextEdit.setUndoRedoEnabled(False)
            self.plainTextEdit.setLineWrapMode(
                QtWidgets.QPlainTextEdit.LineWrapMode.WidgetWidth
            )
            self.plainTextEdit.setReadOnly(True)
            self.plainTextEdit.setTabStopDistance(80)
            self.plainTextEdit.setCursorWidth(16)
            self.plainTextEdit.setBackgroundVisible(False)
            self.plainTextEdit.setCenterOnScroll(False)
            self.verticalLayout.addWidget(self.plainTextEdit)
            MainWindow.setCentralWidget(self.centralwidget)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            pass

    class UI(QMainWindow, Ui_MainWindow):
        def __init__(self):
            QMainWindow.__init__(self)
            self.setupUi(window)

            self.console = Terminal(self.plainTextEdit)
            self.console.write("\033")
            self.console.write("[")
            self.console.write("6")
            self.console.write("n")
            self.console.write("\033[6nHi There!\033[6n\n")

            self.console.write("        \t8 blanks and a tab before me\n")
            self.console.write("8 blanks and a tab after me>        \t")
            self.console.write("<\n")
            self.console.write("8 blanks        \tand a tab\n")

            self.console.write("GOT mo")
            self.console.write("del\r")
            self.console.write("\n")

            self.console.write("Feeling")
            self.console.write(" a ")
            self.console.write("little \033[44mblue\033[0m?\r\n")

            self.console.write("80 columns:\n")
            self.console.write("*" * 80 + "\n")

            self.console.write("132 columns:\n")
            self.console.write("*" * 132 + "\n")

            self.console.write("partial line")
            self.console.write("\nthis should be on a new line\n")

            # test spinner:
            self.console.write("Wait a little: x\bX")

            self.spinner_pos = 0
            self.timer = QBasicTimer()
            self.timer.start(100, self)

        def timerEvent(self, event):
            if event.timerId() != self.timer.timerId():
                super(UI, self).timerEvent(event)

            progress_ch = r"-\|/"[self.spinner_pos % 4]
            self.console.write("\b" + progress_ch)
            self.spinner_pos += 1
            if self.spinner_pos >= 16:
                self.timer.stop()
                self.console.write("\bdone with that...\n")

    app = QApplication(sys.argv)
    window = QMainWindow()
    _ = UI()
    window.show()
    sys.exit(app.exec())
