import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QTabWidget, QHBoxLayout, QPlainTextEdit, QScrollArea
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QFont
from PyQt5.QtCore import Qt
from difflib import Differ

class TextDiffApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Text Diff Checker')
        self.resize(800, 600)

        layout = QVBoxLayout(self)
        self.tabWidget = QTabWidget()

        # Input Tab
        self.inputTab = QWidget()
        inputTabLayout = QVBoxLayout(self.inputTab)

        self.textEdit1 = QTextEdit()
        self.textEdit1.setPlaceholderText("Enter first text here...")
        self.textEdit1.setStyleSheet("font-size: 16px;")

        self.textEdit2 = QTextEdit()
        self.textEdit2.setPlaceholderText("Enter second text here...")
        self.textEdit2.setStyleSheet("font-size: 16px;")

        self.compareButton = QPushButton('Compare')
        self.compareButton.clicked.connect(self.compareTexts)

        inputTabLayout.addWidget(self.textEdit1)
        inputTabLayout.addWidget(self.textEdit2)
        inputTabLayout.addWidget(self.compareButton)
        self.tabWidget.addTab(self.inputTab, "Input")

        # Diff Tab
        self.diffTab = QWidget()
        diffTabLayout = QVBoxLayout(self.diffTab)
        self.tabWidget.addTab(self.diffTab, "Diff Line Result")
        self.tabWidget.setTabEnabled(1, False)  # 預設隱藏 Diff Tab

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.diffContainer = QWidget()
        self.diffLayout = QHBoxLayout(self.diffContainer)

        self.leftTextEdit = QPlainTextEdit()
        self.leftTextEdit.setReadOnly(True)
        self.leftTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.leftTextEdit.setFont(QFont("Courier New", 10))
        self.leftTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.lineNumberArea = QPlainTextEdit()
        self.lineNumberArea.setReadOnly(True)
        self.lineNumberArea.setFont(QFont("Courier New", 10))
        self.lineNumberArea.setStyleSheet("background-color: #e0e0e0;")
        self.lineNumberArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.rightTextEdit = QPlainTextEdit()
        self.rightTextEdit.setReadOnly(True)
        self.rightTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.rightTextEdit.setFont(QFont("Courier New", 10))
        self.rightTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.diffLayout.addWidget(self.leftTextEdit)
        self.diffLayout.addWidget(self.lineNumberArea)
        self.diffLayout.addWidget(self.rightTextEdit)

        self.diffContainer.setLayout(self.diffLayout)
        self.scrollArea.setWidget(self.diffContainer)
        diffTabLayout.addWidget(self.scrollArea)

        layout.addWidget(self.tabWidget)

    def compareTexts(self):
        text1, text2 = self.textEdit1.toPlainText(), self.textEdit2.toPlainText()
        differ = Differ()
        diff = list(differ.compare(text1.splitlines(), text2.splitlines()))

        leftText, rightText, leftLineNumbers, rightLineNumbers = [], [], [], []

        for line in diff:
            if line.startswith('- '):
                leftText.append(line[2:])
                rightText.append('')
                leftLineNumbers.append(str(len(leftLineNumbers) + 1))
                rightLineNumbers.append('')
            elif line.startswith('+ '):
                leftText.append('')
                rightText.append(line[2:])
                leftLineNumbers.append('')
                rightLineNumbers.append(str(len(rightLineNumbers) + 1))
            elif line.startswith('  '):
                leftText.append(line[2:])
                rightText.append(line[2:])
                leftLineNumbers.append(str(len(leftLineNumbers) + 1))
                rightLineNumbers.append(str(len(rightLineNumbers) + 1))

        self.leftTextEdit.setPlainText('\n'.join(leftText))
        self.rightTextEdit.setPlainText('\n'.join(rightText))

        # 差異行色彩強調
        cursor1, cursor2 = self.leftTextEdit.textCursor(), self.rightTextEdit.textCursor()
        cursor1.movePosition(QTextCursor.Start)
        cursor2.movePosition(QTextCursor.Start)

        while not cursor1.atEnd() and not cursor2.atEnd():
            cursor1.movePosition(QTextCursor.StartOfBlock)
            cursor2.movePosition(QTextCursor.StartOfBlock)
            cursor1.select(QTextCursor.BlockUnderCursor)
            cursor2.select(QTextCursor.BlockUnderCursor)

            if cursor1.selectedText() != cursor2.selectedText():
                format1, format2 = QTextCharFormat(), QTextCharFormat()
                format1.setBackground(QColor('#FFC9C9'))
                format2.setBackground(QColor('#C9FFC9'))
                cursor1.mergeCharFormat(format1)
                cursor2.mergeCharFormat(format2)

            cursor1.movePosition(QTextCursor.NextBlock)
            cursor2.movePosition(QTextCursor.NextBlock)

        # 找出最大數值的字元寬度
        maxWidth = max(map(len, leftLineNumbers + rightLineNumbers), default = 1)

        # 動態調整字元寬度
        self.lineNumberArea.setFixedWidth(50 + ((maxWidth - 1) * 20))
        
        # 產生行號內容
        combinedLineNumbers = [
            f"{left:<{maxWidth}s}  {right:>{maxWidth}s}"
            for left, right in zip(leftLineNumbers, rightLineNumbers)
        ]
        self.lineNumberArea.setPlainText('\n'.join(combinedLineNumbers))

        # 自動調整高度
        numLines = max(len(leftText), len(rightText))
        lineHeight = 20  # 依據字型調整
        newHeight = (numLines + 3) * lineHeight
        self.leftTextEdit.setFixedHeight(newHeight)
        self.rightTextEdit.setFixedHeight(newHeight)

        lineHeight = 22  # 依據字型調整
        newHeight = (numLines - 2) * lineHeight + 0
        self.lineNumberArea.setFixedHeight(newHeight - 0)
        
        # 顯示 Diff Tab
        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setCurrentWidget(self.diffTab)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextDiffApp()
    ex.show()
    sys.exit(app.exec_())
