from kivy.app import App
from kivy.uix.label import Label

class ScanApp(App):
    def build(self):
        return Label(text="扫码采集-测试成功")

if __name__ == "__main__":
    ScanApp().run()
