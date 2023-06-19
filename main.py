import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QScrollArea
from PyQt5.QtGui import QPixmap, QPainter, QPalette, QColor, QBrush
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from translate import Translator

class TranslationThread(QThread):
    translation_completed = pyqtSignal(str)

    def __init__(self, text, src_lang, dest_lang):
        super().__init__()
        self.text = text
        self.src_lang = src_lang
        self.dest_lang = dest_lang

    def run(self):
        translator = Translator(from_lang=self.src_lang, to_lang=self.dest_lang)
        translation = translator.translate(self.text)
        self.translation_completed.emit(translation)

class TranslationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('翻译菌')
        self.layout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        self.input_label = QLabel('请输入要翻译的文本：')
        self.input_text = QTextEdit()
        self.translate_btn = QPushButton('翻译')
        self.toggle_btn = QPushButton('切换语言')
        self.scroll_area = QScrollArea()  # 创建滚动区域
        self.scroll_area.setWidgetResizable(True)  # 设置滚动区域大小可调整

        # 设置样式
        self.setStyleSheet("""
        QLabel {
            font-size: 30px;
            color: black;
        }
        QTextEdit {
            font-size: 30px;
            padding: 10px;
            color: black;
            background-color: rgba(0, 0, 0, 0);
            border: none;
        }
        QPushButton {
            font-size: 30px;
            padding: 10px 20px;
            background-color: #FF69B4;
            color: black;
        }
        QLabel#resultLabel {
            font-size: 30px;
            padding: 10px;
            background-color: rgba(255, 105, 180, 100);
            border-radius: 5px;
        }
        """)

        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_text)
        self.layout.addWidget(self.translate_btn)
        self.layout.addWidget(self.toggle_btn)
        self.layout.addWidget(self.scroll_area)  # 使用滚动区域显示结果
        self.translate_btn.clicked.connect(self.start_translation)
        self.toggle_btn.clicked.connect(self.toggle_language)

        self.setLayout(self.layout)

        self.src_lang = 'en'  # 源语言
        self.dest_lang = 'zh'  # 目标语言

        # 设置窗口背景图片
        palette = self.palette()
        background_image = QPixmap('qwm.jpg')
        palette.setBrush(self.backgroundRole(), QBrush(background_image))
        self.setPalette(palette)

    def start_translation(self):
        text = self.input_text.toPlainText()
        self.translation_thread = TranslationThread(text, self.src_lang, self.dest_lang)
        self.translation_thread.translation_completed.connect(self.display_translation)
        self.translate_btn.setEnabled(False)  # 禁用翻译按钮，避免重复点击
        self.translation_thread.start()

    def display_translation(self, translation):
        result_label = QLabel(translation)  # 创建一个标签用于显示翻译结果
        result_label.setWordWrap(True)  # 自动换行
        self.scroll_area.setWidget(result_label)  # 将结果标签放入滚动区域中
        self.translate_btn.setEnabled(True)  # 启用翻译按钮

    def toggle_language(self):
        self.src_lang, self.dest_lang = self.dest_lang, self.src_lang
        self.toggle_btn.setText('切换语言 ({})'.format(self.dest_lang))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TranslationApp()
    window.resize(600, 800)  # 调整窗口大小
    window.show()
    sys.exit(app.exec_())
