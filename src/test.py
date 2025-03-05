from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPlainTextEdit, QLabel, QScrollArea, QTabWidget, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SideBySideDiffViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Side-by-Side Code Diff Viewer")

        main_layout = QVBoxLayout(self)
        tab_widget = QTabWidget(self)

        # 创建一个新的 QWidget 作为标签页
        diff_tab = QWidget()
        diff_tab_layout = QVBoxLayout(diff_tab)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 设置 QScrollArea 的垂直滚动条策略

        container = QWidget()
        container_layout = QHBoxLayout(container)

        # 行號標示
        line_numbers = "\n".join(str(i) for i in range(1, 53))
        self.line_number = QLabel(line_numbers)
        self.line_number.setFixedWidth(50)
        self.line_number.setAlignment(Qt.AlignRight)
        self.line_number.setFont(QFont("Courier New", 10))
        self.line_number.setContentsMargins(0, 5, 0, 0)  # 设置上边距为 5 像素

        # 左側原始程式碼
        self.left_code = QPlainTextEdit()
        self.left_code.setPlainText("\n".join(f"Line {i}: Old Code New Code New Code New Code" for i in range(1, 51)))
        self.left_code.setReadOnly(True)
        self.left_code.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.left_code.setFont(QFont("Courier New", 10))  # 設定文字尺寸為 10
        self.left_code.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用垂直捲動
        self.left_code.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 允许水平捲動
        
        # 右側修改後的程式碼
        self.right_code = QPlainTextEdit()
        self.right_code.setPlainText("\n".join(f"Line {i}: New Code New Code New Code New Code" for i in range(1, 51)))
        self.right_code.setReadOnly(True)
        self.right_code.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.right_code.setFont(QFont("Courier New", 10))  # 設定文字尺寸為 10
        self.right_code.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用垂直捲動
        self.right_code.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 允许水平捲動

        container_layout.addWidget(self.left_code)
        container_layout.addWidget(self.line_number)
        container_layout.addWidget(self.right_code)

        scroll_area.setWidget(container)
        
        diff_tab_layout.addWidget(scroll_area)
        diff_tab.setLayout(diff_tab_layout)

        # 将 diff_tab 添加到 tab_widget 中
        tab_widget.addTab(diff_tab, "Diff Viewer")

        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    viewer = SideBySideDiffViewer()
    viewer.show()
    sys.exit(app.exec_())
