import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QTabWidget, QHBoxLayout, QPlainTextEdit, QScrollArea, QSizePolicy
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QFont, QTextOption
from PyQt5.QtCore import Qt
from difflib import Differ

class TextDiffApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Text Diff Checker')
        self.resize(800, 600)

        mainlayout = QVBoxLayout(self) # 主佈局
        self.tabWidget = QTabWidget() # 分頁組
        self.initUI_Tab1()
        self.initUI_Tab2()
        self.tabWidget.setTabEnabled(1, False)  # 預設隱藏 Diff Tab

        mainlayout.addWidget(self.tabWidget)
        self.setLayout(mainlayout)

    def initUI_Tab1(self):
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

    def initUI_Tab2(self):
        # Diff Tab
        self.leftTextEdit = QPlainTextEdit()
        self.leftTextEdit.setReadOnly(True)
        self.leftTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.leftTextEdit.setFont(QFont("Courier New", 10))
        self.leftTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.rightTextEdit = QPlainTextEdit()
        self.rightTextEdit.setReadOnly(True)
        self.rightTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.rightTextEdit.setFont(QFont("Courier New", 10))
        self.rightTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.lineNumberArea = QPlainTextEdit()
        self.lineNumberArea.setReadOnly(True)
        self.lineNumberArea.setFont(QFont("Courier New", 10))
        self.lineNumberArea.setStyleSheet("background-color: #e0e0e0;")
        self.lineNumberArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.lineNumberArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 行號區域填充區
        self.lineNumberSpacer = QWidget()
        self.lineNumberSpacer.setFixedHeight(0)  # 初始高度設為 0
        self.lineNumberSpacer.setStyleSheet("background-color: #e0CCe0;")
        self.lineNumberSpacer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # 建立行號區域的垂直佈局
        self.lineNumberVLayout = QVBoxLayout()
        # 加入行號區域
        self.lineNumberVLayout.addWidget(self.lineNumberArea)
        self.lineNumberVLayout.addWidget(self.lineNumberSpacer)

        # 建立垂直佈局
        self.diffHLayout = QHBoxLayout()
        # 加入水平佈局
        self.diffHLayout.addWidget(self.leftTextEdit)
        self.diffHLayout.addLayout(self.lineNumberVLayout)
        self.diffHLayout.addWidget(self.rightTextEdit)

        # 建立捲動區
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setAlignment(Qt.AlignTop)
        # 加入捲動區
        self.scrollArea.setLayout(self.diffHLayout)
        
        # 加入 tab 頁
        self.tabWidget.addTab(self.scrollArea, "Diff Line Result")

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

        # 動態調整行號區域寬度
        self.lineNumberArea.setFixedWidth(50 + ((maxWidth - 1) * 20))
        self.lineNumberSpacer.setFixedWidth(50 + ((maxWidth - 1) * 20))
        
        # 產生行號內容
        combinedLineNumbers = [
            f"{left:<{maxWidth}s}  {right:>{maxWidth}s}"
            for left, right in zip(leftLineNumbers, rightLineNumbers)
        ]

        self.lineNumberArea.setPlainText('\n'.join(combinedLineNumbers))

        # 自動調整高度
        numLines = max(len(leftText), len(rightText))
        lineHeight = 20  # 依據字型調整
        Height = (numLines + 3) * lineHeight
        self.leftTextEdit.setFixedHeight(Height)
        self.rightTextEdit.setFixedHeight(Height)
        print('TextEdit Height: ', Height)

        lineHeight = 20  # 依據字型調整
        Height = (numLines + 1) * lineHeight
        self.lineNumberArea.setFixedHeight(Height)

        """ fontMetrics = self.leftTextEdit.fontMetrics()
        lineHeight = fontMetrics.lineSpacing()  # 取得適當的行高
        Height = numLines * lineHeight
        self.lineNumberArea.setFixedHeight(Height) """
        print('lineNumberArea Height: ', Height)
        print('combinedLineNumbers: ', combinedLineNumbers)

        # 設定填充區，使總高度與 leftTextEdit 對齊
        #self.lineNumberSpacer.setFixedHeight(self.leftTextEdit.height() - Height - 10)

        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setCurrentWidget(self.scrollArea)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextDiffApp()
    ex.show()
    sys.exit(app.exec_())