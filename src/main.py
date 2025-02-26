import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QTabWidget, QHBoxLayout, QScrollArea, QFrame
from PyQt5.QtGui import QTextCursor, QColor, QFont
from PyQt5.QtCore import Qt
from difflib import Differ

class LineNumberArea(QFrame):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Plain)
        self.setStyleSheet("background-color: #f0f0f0;")

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

class TextDiffApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Text Diff Checker')

        self.layout = QVBoxLayout()

        self.tabWidget = QTabWidget(self)
        self.layout.addWidget(self.tabWidget)

        # Create the input tab
        self.inputTab = QWidget()
        self.inputTabLayout = QVBoxLayout()
        self.textEdit1 = QTextEdit(self)
        self.textEdit1.setPlaceholderText("Enter first text here...")
        self.inputTabLayout.addWidget(self.textEdit1)
        self.textEdit2 = QTextEdit(self)
        self.textEdit2.setPlaceholderText("Enter second text here...")
        self.inputTabLayout.addWidget(self.textEdit2)
        self.compareButton = QPushButton('Compare', self)
        self.compareButton.clicked.connect(self.compareTexts)
        self.inputTabLayout.addWidget(self.compareButton)
        self.inputTab.setLayout(self.inputTabLayout)
        self.tabWidget.addTab(self.inputTab, "Input")

        # Create the diff result tab
        self.diffTab = QWidget()
        self.diffTabLayout = QHBoxLayout()

        self.leftTextEdit = QTextEdit()
        self.leftTextEdit.setReadOnly(True)
        self.leftTextEdit.setLineWrapMode(QTextEdit.NoWrap)

        self.rightTextEdit = QTextEdit()
        self.rightTextEdit.setReadOnly(True)
        self.rightTextEdit.setLineWrapMode(QTextEdit.NoWrap)

        self.leftLineNumberArea = LineNumberArea(self.leftTextEdit)
        self.rightLineNumberArea = LineNumberArea(self.rightTextEdit)

        self.leftScrollArea = QScrollArea()
        self.leftScrollArea.setWidget(self.leftTextEdit)
        self.leftScrollArea.setWidgetResizable(True)
        self.leftScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.rightScrollArea = QScrollArea()
        self.rightScrollArea.setWidget(self.rightTextEdit)
        self.rightScrollArea.setWidgetResizable(True)
        self.rightScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.diffTabLayout.addWidget(self.leftLineNumberArea)
        self.diffTabLayout.addWidget(self.leftScrollArea)
        self.diffTabLayout.addWidget(self.rightLineNumberArea)
        self.diffTabLayout.addWidget(self.rightScrollArea)

        self.diffTab.setLayout(self.diffTabLayout)
        self.tabWidget.addTab(self.diffTab, "Diff Result")

        self.setLayout(self.layout)

    def compareTexts(self):
        text1 = self.textEdit1.toPlainText()
        text2 = self.textEdit2.toPlainText()

        differ = Differ()
        diff = list(differ.compare(text1.splitlines(), text2.splitlines()))

        leftText = []
        rightText = []
        leftLineNumbers = []
        rightLineNumbers = []

        leftLineNumber = 1
        rightLineNumber = 1

        for line in diff:
            if line.startswith('- '):
                leftText.append(line[2:])
                rightText.append('')
                leftLineNumbers.append(str(leftLineNumber))
                rightLineNumbers.append('')
                leftLineNumber += 1
            elif line.startswith('+ '):
                leftText.append('')
                rightText.append(line[2:])
                leftLineNumbers.append('')
                rightLineNumbers.append(str(rightLineNumber))
                rightLineNumber += 1
            elif line.startswith('  '):
                leftText.append(line[2:])
                rightText.append(line[2:])
                leftLineNumbers.append(str(leftLineNumber))
                rightLineNumbers.append(str(rightLineNumber))
                leftLineNumber += 1
                rightLineNumber += 1
            elif line.startswith('? '):
                continue

        self.leftTextEdit.setPlainText('\n'.join(leftText))
        self.rightTextEdit.setPlainText('\n'.join(rightText))

        self.leftLineNumberArea.setPlainText('\n'.join(leftLineNumbers))
        self.rightLineNumberArea.setPlainText('\n'.join(rightLineNumbers))

        self.highlightDifferences(self.leftTextEdit, self.rightTextEdit)

        # Switch to the diff result tab
        self.tabWidget.setCurrentWidget(self.diffTab)

    def highlightDifferences(self, leftTextEdit, rightTextEdit):
        cursor1 = leftTextEdit.textCursor()
        cursor2 = rightTextEdit.textCursor()

        cursor1.movePosition(QTextCursor.Start)
        cursor2.movePosition(QTextCursor.Start)

        while not cursor1.atEnd() and not cursor2.atEnd():
            cursor1.select(QTextCursor.LineUnderCursor)
            cursor2.select(QTextCursor.LineUnderCursor)

            line1 = cursor1.selectedText()
            line2 = cursor2.selectedText()

            if line1 != line2:
                cursor1.setCharFormat(self.getHighlightFormat(QColor('#FFC9C9')))
                cursor2.setCharFormat(self.getHighlightFormat(QColor('#C9FFC9')))

            cursor1.movePosition(QTextCursor.Down)
            cursor2.movePosition(QTextCursor.Down)

    def getHighlightFormat(self, color):
        fmt = QTextCursor().charFormat()
        fmt.setBackground(color)
        return fmt

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextDiffApp()
    ex.show()
    sys.exit(app.exec_())