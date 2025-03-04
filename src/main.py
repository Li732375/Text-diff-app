import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QTabWidget, QHBoxLayout, QPlainTextEdit
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption
from difflib import Differ


class LineNumberArea(QPlainTextEdit):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setReadOnly(True)
        self.setFixedWidth(68)  # 設定行號區域的寬度
        self.setWordWrapMode(QTextOption.NoWrap) 
        self.setStyleSheet("""
            background-color: #e0e0e0; 
            border: none; 
            font-family: 'Courier New', monospace;
            font-size: 16px;
        """)
        # 移除滾動條
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def updateLineNumbers(self, line_numbers):
        self.setPlainText('\n'.join(line_numbers))


class TextDiffApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Text Diff Checker')
        self.resize(800, 600)

        self.layout = QVBoxLayout()
        self.tabWidget = QTabWidget(self)
        self.layout.addWidget(self.tabWidget)

        # Input Tab
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

        # Diff Tab
        self.diffTab = QWidget()
        self.diffTabLayout = QHBoxLayout()

        self.leftTextEdit = QTextEdit()
        self.leftTextEdit.setReadOnly(True)
        self.leftTextEdit.setLineWrapMode(QTextEdit.NoWrap)

        self.lineNumberArea = LineNumberArea(self)
        self.rightTextEdit = QTextEdit()
        self.rightTextEdit.setReadOnly(True)
        self.rightTextEdit.setLineWrapMode(QTextEdit.NoWrap)

        # **同步滾動**
        self.leftTextEdit.verticalScrollBar().valueChanged.connect(self.syncScroll)
        self.rightTextEdit.verticalScrollBar().valueChanged.connect(self.syncScroll)
        self.lineNumberArea.verticalScrollBar().valueChanged.connect(self.syncScroll)

        # **隱藏滾動條（但保持同步）**
        self.leftTextEdit.verticalScrollBar().setVisible(False)
        self.rightTextEdit.verticalScrollBar().setVisible(False)
        self.lineNumberArea.verticalScrollBar().setVisible(False)

        self.diffTabLayout.addWidget(self.leftTextEdit)
        self.diffTabLayout.addWidget(self.lineNumberArea)
        self.diffTabLayout.addWidget(self.rightTextEdit)

        self.diffTab.setLayout(self.diffTabLayout)
        self.tabWidget.addTab(self.diffTab, "Diff Line Result")

        self.setLayout(self.layout)

    def syncScroll(self, value):
        """同步滾動條"""
        self.leftTextEdit.verticalScrollBar().setValue(value)
        self.rightTextEdit.verticalScrollBar().setValue(value)
        self.lineNumberArea.verticalScrollBar().setValue(value)

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
            if line.startswith('- '):  # 文字只在左側
                leftText.append(line[2:])
                rightText.append('')
                leftLineNumbers.append(str(leftLineNumber))
                rightLineNumbers.append('')
                leftLineNumber += 1
            elif line.startswith('+ '):  # 文字只在右側
                leftText.append('')
                rightText.append(line[2:])
                leftLineNumbers.append('')
                rightLineNumbers.append(str(rightLineNumber))
                rightLineNumber += 1
            elif line.startswith('  '):  # 兩側相同
                leftText.append(line[2:])
                rightText.append(line[2:])
                leftLineNumbers.append(str(leftLineNumber))
                rightLineNumbers.append(str(rightLineNumber))
                leftLineNumber += 1
                rightLineNumber += 1
            elif line.startswith('? '):  # 這是 `Differ` 的標記行，不需處理
                continue

        self.leftTextEdit.setPlainText('\n'.join(leftText))
        self.rightTextEdit.setPlainText('\n'.join(rightText))

        maxLineNumber = max(leftLineNumber, rightLineNumber)
        maxLineNumberLength = len(str(maxLineNumber))

        combinedLineNumbers = []
        for leftLineNumber, rightLineNumber in zip(leftLineNumbers, rightLineNumbers):
            if leftLineNumber == '':
                leftLineNumber = f'{" ":{maxLineNumberLength}s}'
            else:
                leftLineNumber = f"{leftLineNumber:<{maxLineNumberLength}s}"

            if rightLineNumber == '':
                rightLineNumber = f'{" ":{maxLineNumberLength}s}'
            else:
                rightLineNumber = f"{rightLineNumber:>{maxLineNumberLength}s}"

            combinedLineNumbers.append(f"{leftLineNumber}  {rightLineNumber}")

        self.lineNumberArea.updateLineNumbers(combinedLineNumbers)
        self.highlightDifferences(self.leftTextEdit, self.rightTextEdit)

        # 切換到 Diff 結果頁面
        self.tabWidget.setCurrentWidget(self.diffTab)

    def highlightDifferences(self, leftTextEdit, rightTextEdit):
        cursor1 = leftTextEdit.textCursor()
        cursor2 = rightTextEdit.textCursor()

        cursor1.movePosition(QTextCursor.Start)
        cursor2.movePosition(QTextCursor.Start)

        while not cursor1.atEnd() or not cursor2.atEnd():
            cursor1.select(QTextCursor.LineUnderCursor)
            cursor2.select(QTextCursor.LineUnderCursor)

            line1 = cursor1.selectedText() if cursor1.hasSelection() else ""
            line2 = cursor2.selectedText() if cursor2.hasSelection() else ""

            if line1 != line2:
                cursor1.setCharFormat(self.getHighlightFormat(QColor('#FFC9C9')))
                cursor2.setCharFormat(self.getHighlightFormat(QColor('#C9FFC9')))

            cursor1.movePosition(QTextCursor.Down)
            cursor2.movePosition(QTextCursor.Down)

    def getHighlightFormat(self, color):
        fmt = QTextCharFormat()
        fmt.setBackground(color)
        return fmt


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextDiffApp()
    ex.show()
    sys.exit(app.exec_())
