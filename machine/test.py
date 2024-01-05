from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class Screen(BoxLayout):
    pass


class Test(App):
    def build(self):
        return Screen()


if __name__ == '__main__':
    Test().run()
