import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QTabWidget, QHBoxLayout, QPlainTextEdit, QScrollArea, QLabel
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption
from difflib import Differ

class TextDiffApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Text Diff Checker')
        self.resize(800, 600)

        self.mainlayout = QVBoxLayout()
        self.tabWidget = QTabWidget(self)

        # Input Tab
        self.inputTab = QWidget()
        self.inputTabLayout = QVBoxLayout()

        self.textEdit1 = QTextEdit(self)
        self.textEdit1.setPlaceholderText("Enter first text here...")
        self.textEdit1.setStyleSheet("font-size: 20px;")
        self.inputTabLayout.addWidget(self.textEdit1)

        self.textEdit2 = QTextEdit(self)
        self.textEdit2.setPlaceholderText("Enter second text here...")
        self.textEdit2.setStyleSheet("font-size: 20px;")
        self.inputTabLayout.addWidget(self.textEdit2)

        self.compareButton = QPushButton('Compare', self)
        self.compareButton.clicked.connect(self.compareTexts)
        self.inputTabLayout.addWidget(self.compareButton)

        self.inputTab.setLayout(self.inputTabLayout)
        self.tabWidget.addTab(self.inputTab, "Input")

        # Diff Tab
        self.diff_tab = QWidget()
        diff_tab_layout = QVBoxLayout(self.diff_tab)
        self.tabWidget.addTab(self.diff_tab, "Diff Line Result")
        self.tabWidget.setTabEnabled(1, False)  # 預設隱藏 Diff Tab

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        container = QWidget()
        self.diffTabLayout = QHBoxLayout(container)

        # 左側程式碼
        self.leftTextEdit = QPlainTextEdit()
        self.leftTextEdit.setReadOnly(True)
        self.leftTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.leftTextEdit.setFont(QFont("Courier New", 10))

        # 行號區域
        self.lineNumberArea = QPlainTextEdit()
        self.lineNumberArea.setReadOnly(True)
        self.lineNumberArea.setFixedWidth(70)
        self.lineNumberArea.setFont(QFont("Courier New", 10))
        self.lineNumberArea.setStyleSheet("background-color: #e0e0e0;")
        self.lineNumberArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用垂直捲動

        # 右側程式碼
        self.rightTextEdit = QPlainTextEdit()
        self.rightTextEdit.setReadOnly(True)
        self.rightTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.rightTextEdit.setFont(QFont("Courier New", 10))

        self.diffTabLayout.addWidget(self.leftTextEdit)
        self.diffTabLayout.addWidget(self.lineNumberArea)
        self.diffTabLayout.addWidget(self.rightTextEdit)

        scroll_area.setWidget(container)
        diff_tab_layout.addWidget(scroll_area)
        self.diff_tab.setLayout(diff_tab_layout)

        self.mainlayout.addWidget(self.tabWidget)
        self.setLayout(self.mainlayout)
    
    def compareTexts(self):
        text1 = self.textEdit1.toPlainText()
        text2 = self.textEdit2.toPlainText()

        differ = Differ()
        diff = list(differ.compare(text1.splitlines(), text2.splitlines()))

        leftText = []
        rightText = []
        leftLineNumbers = []
        rightLineNumbers = []

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
            elif line.startswith('? '):
                continue

        self.leftTextEdit.setPlainText('\n'.join(leftText))
        self.rightTextEdit.setPlainText('\n'.join(rightText))

        # 計算行號最大寬度
        maxLineNumberLength = max(len(str(len(leftLineNumbers))), 
                                  len(str(len(rightLineNumbers))))

        # 調整行號對齊方式
        combinedLineNumbers = []
        for leftLineNumber, rightLineNumber in zip(leftLineNumbers, rightLineNumbers):
            leftLineNumber = f"{leftLineNumber:<{maxLineNumberLength}s}" if leftLineNumber else " " * maxLineNumberLength
            rightLineNumber = f"{rightLineNumber:>{maxLineNumberLength}s}" if rightLineNumber else " " * maxLineNumberLength
            combinedLineNumbers.append(f"{leftLineNumber}  {rightLineNumber}")

        self.lineNumberArea.setPlainText('\n'.join(combinedLineNumbers))

        self.highlightDifferences(self.leftTextEdit, self.rightTextEdit)

        '''
        # 計算最小不需要滾動的高度
        min_height = max(
            self.leftTextEdit.document().size().height(),
            self.rightTextEdit.document().size().height(),
            self.lineNumberArea.document().size().height()
        ) + 10  # 加上一些 padding，避免擠壓

        # 設定每個區域的最小高度
        self.leftTextEdit.setMinimumHeight(min_height)
        self.rightTextEdit.setMinimumHeight(min_height)
        self.lineNumberArea.setMinimumHeight(min_height)
        '''
        
        # 啟用 Diff Tab 並切換到 Diff 頁面
        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setCurrentWidget(self.diff_tab)


    def highlightDifferences(self, leftTextEdit, rightTextEdit):
        cursor1 = leftTextEdit.textCursor()
        cursor2 = rightTextEdit.textCursor()

        cursor1.movePosition(QTextCursor.Start)
        cursor2.movePosition(QTextCursor.Start)

        while not cursor1.atEnd() and not cursor2.atEnd():
            cursor1.movePosition(QTextCursor.StartOfBlock)
            cursor2.movePosition(QTextCursor.StartOfBlock)

            cursor1.select(QTextCursor.BlockUnderCursor)
            cursor2.select(QTextCursor.BlockUnderCursor)

            line1 = cursor1.selectedText()
            line2 = cursor2.selectedText()

            if line1 != line2:
                format1, format2 = QTextCharFormat(), QTextCharFormat()
                format1.setBackground(QColor('#FFC9C9'))
                format2.setBackground(QColor('#C9FFC9'))

                cursor1.mergeCharFormat(format1)
                cursor2.mergeCharFormat(format2)

            cursor1.movePosition(QTextCursor.NextBlock)
            cursor2.movePosition(QTextCursor.NextBlock)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextDiffApp()
    ex.show()
    sys.exit(app.exec_())
