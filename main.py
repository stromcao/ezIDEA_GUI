import os
import json
import json_return as jr
import improve_code as ic
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
        # 从 SourceText 中获取文本内容并写入到临时文件
        temp_script_path = "temp_script.py"
        with open(temp_script_path, "w", encoding="utf-8") as temp_file:
            temp_file.write(self.ui.SourceText.toPlainText())
        # 调用 review 函数并传递文件路径
        self.process_review(temp_script_path)

    def process_review(self, file_path):
        # 这里处理传入的 Python 文件路径
        print(f"Reviewing file: {file_path}")
        jr.handle_uploaded_file(file_path)
        # 读取生成的 `temp_script_result.json` 文件
        with open("temp_script_result.json", "r", encoding="utf-8") as json_file:
            result_data = json.load(json_file)

        # 获取 SourceText 内容并按行分割
        source_lines = self.ui.SourceText.toPlainText().splitlines()
        error_lines = [error["error_line"] for error in result_data["Error(s)"]]

        # 清空 ReviewText 并按行写入内容，同时标记 error_line
        self.ui.ReviewText.clear()
        for line_number, line_content in enumerate(source_lines, start=1):
            cursor = self.ui.ReviewText.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            # 设置文本格式为默认黑色或错误行的红色
            line_format = QTextCharFormat()
            if line_number in error_lines:
                line_format.setForeground(QColor("red"))
            else:
                line_format.setForeground(QColor("green"))

            # 插入行内容并应用颜色格式
            cursor.insertText(line_content.rstrip() + '\n', line_format)

            # 将光标设置为文本的末尾
            self.ui.ReviewText.setTextCursor(cursor)

    def append_colored_line(self, text_edit, text, color_format):
        # 创建光标并插入有颜色的文本行
        cursor = text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text + '\n', color_format)
        text_edit.setTextCursor(cursor)

    def modify(self):
        file_path = "temp_script.py"
        # 调用 ic.improve_code 函数生成 temp_script_improved.json
        ic.improve_code(file_path)

        # 检查 JSON 文件是否生成
        json_path = "temp_script_improved.json"
        if not os.path.exists(json_path):
            print("Error: Improved JSON result file not found.")
            return

        # 读取 temp_script_improved.json 文件
        with open(json_path, "r", encoding="utf-8") as json_file:
            improved_data = json.load(json_file)

        # 获取所有改进项
        improved_items = {item["error_line"]: item["improved_result"] for item in improved_data["improved_items"]}

        # 获取 temp_script.py 的原始内容并进行行替换
        with open(file_path, "r", encoding="utf-8") as script_file:
            script_lines = script_file.readlines()

        # 清空 ModifyText 并逐行插入修改后的内容
        self.ui.ModifyText.clear()
        for line_number, line_content in enumerate(script_lines, start=1):
            cursor = self.ui.ModifyText.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)

            # 检查是否在改进项中
            line_format = QTextCharFormat()
            line_format.setForeground(QColor("green"))  # 设置绿色

            if line_number in improved_items:
                cursor.insertText(improved_items[line_number] + '\n', line_format)
            else:
                cursor.insertText(line_content.rstrip() + '\n', line_format)

            # 将光标设置为文本的末尾
            self.ui.ModifyText.setTextCursor(cursor)

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()