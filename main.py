from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor
from PySide6.QtUiTools import QUiLoader

class Stats:
    def __init__(self):

        self.ui = QUiLoader().load('ui/GUI.ui')

        self.ui.ReviewButton.clicked.connect(self.review)
        self.ui.ModifyButton.clicked.connect(self.modify)

    def review(self):
        # 从 SourceText 读取内容
        source_text = self.ui.SourceText.toPlainText()
        lines = source_text.split('\n')

        # 清空 ReviewText
        self.ui.ReviewText.clear()

        cursor = self.ui.ReviewText.textCursor()

        # 遍历行并插入到 ReviewText 中
        for i, line in enumerate(lines):
            if i == 1:  # 第二行
                char_format = QTextCharFormat()
                char_format.setForeground(QColor('red'))  # 设置红色
                cursor.setCharFormat(char_format)
                cursor.insertText(line + '\n')  # 插入第二行并设置为红色
                cursor.setCharFormat(QTextCharFormat())  # 恢复默认格式
            else:
                cursor.insertText(line + '\n')  # 插入其他行

    def modify(self):
        info = self.ui.SourceText.toPlainText()
        self.insertPlainText(info)
        print(info)

    def highlight_second_line(self):
        # 获取 SourceText 的内容
        source_text = self.sourceText.toPlainText()
        lines = source_text.split('\n')

        if len(lines) >= 2:
            second_line = lines[1]  # 获取第二行

            # 清空 ReviewText
            self.reviewText.clear()

            # 使用 QTextCursor 和 QTextCharFormat 在 ReviewText 中标记第二行为红色
            cursor = self.reviewText.textCursor()
            cursor.insertText(lines[0] + '\n')  # 插入第一行

            # 设置红色格式
            char_format = QTextCharFormat()
            char_format.setForeground(QColor('red'))

            cursor.setCharFormat(char_format)
            cursor.insertText(second_line + '\n')  # 插入第二行并设置为红色

            # 恢复默认格式
            cursor.setCharFormat(QTextCharFormat())
            if len(lines) > 2:
                cursor.insertText('\n'.join(lines[2:]))  # 插入后面的行


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()