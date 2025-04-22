import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QTabWidget, QHBoxLayout, QPlainTextEdit
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QFont
from PyQt5.QtCore import Qt
from difflib import Differ

class PlainTextPasteEdit(QTextEdit):
    def insertFromMimeData(self, source):
        if source.hasText():
            self.insertPlainText(source.text())
        else:
            super().insertFromMimeData(source)

class TextDiffApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Text Diff Checker')
        self.resize(800, 600)

        mainlayout = QVBoxLayout(self) # 主佈局
        self.tabWidget = QTabWidget() # 分頁組

        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.tabWidget.tabBar().setFont(font)

        self.initUI_Tab1()
        self.initUI_Tab2()
        self.tabWidget.setTabEnabled(1, False)  # 預設隱藏 Diff Tab

        mainlayout.addWidget(self.tabWidget)
        self.setLayout(mainlayout)

    def initUI_Tab1(self):
        # Input Tab
        self.textEdit_Up = PlainTextPasteEdit()
        self.textEdit_Up.setPlaceholderText("Enter first text here...")
        self.textEdit_Up.setStyleSheet("font-size: 18px;")

        self.textEdit_Down = PlainTextPasteEdit()
        self.textEdit_Down.setPlaceholderText("Enter second text here...")
        self.textEdit_Down.setStyleSheet("font-size: 18px;")

        self.compareButton = QPushButton('Compare')
        self.compareButton.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.compareButton.clicked.connect(self.compareTexts)

        self.widget_InputTab = QWidget()

        Vlayout_InputTab = QVBoxLayout(self.widget_InputTab)
        Vlayout_InputTab.addWidget(self.textEdit_Up)
        Vlayout_InputTab.addWidget(self.textEdit_Down)
        Vlayout_InputTab.addWidget(self.compareButton)

        self.tabWidget.addTab(self.widget_InputTab, "Input")
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.widget_InputTab), "輸入要比較的文字")

    def initUI_Tab2(self):
        # Diff Line Tab
        self.pTextEdit_Left = QPlainTextEdit()
        self.pTextEdit_Left.setReadOnly(True)
        self.pTextEdit_Left.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.pTextEdit_Left.setFont(QFont("Courier New", 12))
        self.pTextEdit_Left.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pTextEdit_Left.verticalScrollBar().valueChanged.connect(self.syncScroll)

        self.pTextEdit_Right = QPlainTextEdit()
        self.pTextEdit_Right.setReadOnly(True)
        self.pTextEdit_Right.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.pTextEdit_Right.setFont(QFont("Courier New", 12))
        self.pTextEdit_Right.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pTextEdit_Right.verticalScrollBar().valueChanged.connect(self.syncScroll)

        # 建立水平佈局
        self.Hlayout_DiffLineTab = QHBoxLayout()
        self.Hlayout_DiffLineTab.addWidget(self.pTextEdit_Left)
        self.Hlayout_DiffLineTab.addWidget(self.pTextEdit_Right)

        # 控制水平佈局伸展方向，限制兩個 QTextEdit 視窗寬度延伸
        self.widget_DiffLineTab = QWidget()
        self.widget_DiffLineTab.setLayout(self.Hlayout_DiffLineTab)  # 設定水平佈局
        
        # 加入 tab 頁
        self.tabWidget.addTab(self.widget_DiffLineTab, "Diff Line Result")

        tabTip = "行比對結果" +\
        "\n滾輪：垂直卷軸 " +\
        "\nShfit + 滾輪：兩邊垂直卷軸" +\
        "\nCtrl + 滾輪：內容縮放" +\
        "\nAlt + 滾輪：水平卷軸 "

        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.widget_DiffLineTab), tabTip)

    def compareTexts(self):
        text1, text2 = self.textEdit_Up.toPlainText(), self.textEdit_Down.toPlainText()
        differ = Differ()
        diff = list(differ.compare(text1.splitlines(), text2.splitlines()))
        
        leftText, rightText = [], []
        diffTextpart = []
        prelinesign = ''

        for line in diff:
            if line.startswith('- '):
                prelinesign = line[0]

                if len(line) == 2:
                    leftText.append(' ' * 2)
                else:
                    leftText.append(line[2:])

                rightText.append('')
                diffTextpart.append([0, 0])
            elif line.startswith('+ '):
                prelinesign = line[0]
                leftText.append('')

                if len(line) == 2:
                    rightText.append(' ' * 2)
                else:
                    rightText.append(line[2:])

                diffTextpart.append([0, 0])
            elif line.startswith('  '):
                prelinesign = ''
                leftText.append(line[2:])
                rightText.append(line[2:])
                diffTextpart.append([0, 0])
            elif line.startswith('? '):
                if prelinesign == '-':
                    diffTextpart[-1][0] = line[2:].find(prelinesign)
                    diffTextpart[-1][1] = line[2:].rfind(prelinesign)
                elif prelinesign == '+':
                    diffTextpart[-1][0] = line[2:].find(prelinesign)
                    diffTextpart[-1][1] = line[2:].rfind(prelinesign)

                prelinesign = ''

        self.pTextEdit_Left.setPlainText('\n'.join(leftText))
        self.pTextEdit_Right.setPlainText('\n'.join(rightText))
        
        # 差異行色彩強調
        cursor1, cursor2 = self.pTextEdit_Left.textCursor(), self.pTextEdit_Right.textCursor()
        cursor1.movePosition(QTextCursor.Start)
        cursor2.movePosition(QTextCursor.Start)

        for line1, line2, diffpos in zip(leftText, rightText, diffTextpart):
            cursor1.movePosition(QTextCursor.StartOfBlock)
            cursor2.movePosition(QTextCursor.StartOfBlock)
            cursor1.select(QTextCursor.BlockUnderCursor)
            cursor2.select(QTextCursor.BlockUnderCursor)

            if line1 != line2:
                format1, format2 = QTextCharFormat(), QTextCharFormat()
                format1.setBackground(QColor('#FFDEDE'))  # 紅色背景（整行）
                format2.setBackground(QColor('#C9FFC9'))  # 綠色背景（整行）
                cursor1.mergeCharFormat(format1)
                cursor2.mergeCharFormat(format2)

            # 變更差異字段背景色
            if diffpos != [0, 0]:
                for pos in range(diffpos[0], diffpos[1] + 1):
                    highlight = QTextCharFormat()
                    
                    if line1:
                        cursor1.setPosition(cursor1.block().position() + pos)
                        cursor1.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
                        highlight.setBackground(QColor('#FFABAB'))  # 左區字段背景色
                        highlight.setFontWeight(QFont.Bold)  # 粗體
                        cursor1.mergeCharFormat(highlight)
                    else:
                        cursor2.setPosition(cursor2.block().position() + pos)
                        cursor2.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
                        highlight = QTextCharFormat()
                        highlight.setBackground(QColor('#59FF59'))  # 右區字段背景色
                        highlight.setFontWeight(QFont.Bold)  # 粗體
                        cursor2.mergeCharFormat(highlight)

            cursor1.movePosition(QTextCursor.NextBlock)
            cursor2.movePosition(QTextCursor.NextBlock)

        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setCurrentWidget(self.widget_DiffLineTab)

    def syncScroll(self, value):
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            sender = self.sender()
            if sender == self.pTextEdit_Left.verticalScrollBar():
                self.pTextEdit_Right.verticalScrollBar().setValue(value)
            elif sender == self.pTextEdit_Right.verticalScrollBar():
                self.pTextEdit_Left.verticalScrollBar().setValue(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextDiffApp()
    ex.show()
    sys.exit(app.exec_())
