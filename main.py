import os
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor
from PySide6.QtUiTools import QUiLoader

class Stats:
    def __init__(self):

        self.ui = QUiLoader().load('ui/GUI.ui')

        # 记录上传文件的路径
        self.uploaded_file_path = None
        # 用来保存临时文件路径
        self.temp_file_name = None

        self.ui.UploadButton.clicked.connect(self.open_file_dialog)
        self.ui.ReviewButton.clicked.connect(self.review)
        self.ui.ModifyButton.clicked.connect(self.modify)

    def open_file_dialog(self):
        # 打开文件选择对话框，设置 options=None 来避免不兼容参数问题
        file_path, _ = QFileDialog.getOpenFileName(None, "Select Python File", "C:\\Users\\Luna\\PycharmProjects", "Python Files (*.py)")
        if file_path:
            self.uploaded_file_path = file_path  # 保存上传的文件路径
            # 读取选中的文件内容并显示在 SourceText 中
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
                self.ui.SourceText.setPlainText(code)  # 将代码显示在 SourceText 中

    def review(self):
        # 获取用户输入的代码
        code = self.ui.SourceText.toPlainText()

        # 如果有上传的文件路径，使用该路径；否则创建临时文件
        if self.uploaded_file_path:
            file_path_to_review = self.uploaded_file_path
        else:
            # 创建临时文件名
            temp_file_name = "temp_script.py"  # 可以根据需要动态生成唯一文件名

            # 将代码写入临时文件
            with open(temp_file_name, 'w', encoding='utf-8') as temp_file:
                temp_file.write(code)  # 写入代码

            file_path_to_review = temp_file_name  # 使用临时文件的路径

        # 调用 review 函数并传递文件路径
        self.process_review(file_path_to_review)

    def process_review(self, file_path):
        # 这里处理传入的 Python 文件路径
        print(f"Reviewing file: {file_path}")

    def modify(self):
        info = self.ui.SourceText.toPlainText()
        self.insertPlainText(info)
        print(info)

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()