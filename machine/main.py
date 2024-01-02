from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.app import App
import functions as fc
import os


tot = 0


class Manager(ScreenManager):
    pass


class InitScreen(Screen):
    def on_enter(self, *args):
        fc.clear_file('manager_files/carrinho.txt')
        fc.clear_file('manager_files/nota_fiscal.txt')
        global tot
        tot = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.manager.transition.duration = 1.0
            self.manager.transition.direction = 'up'
            self.manager.current = 'BuyScreen'


class HomeBar(BoxLayout):
    @staticmethod
    def on_home_button_release():
        app = App.get_running_app()
        app.root.transition.duration = 1.0
        app.root.transition.direction = 'down'
        app.root.current = 'InitScreen'

class BuyScreen(Screen):
    def on_pre_leave(self):
        fade_out = Animation(opacity=0, duration=0.5)
        fade_out.start(self.ids.Class_Buy1)
        fade_out.start(self.ids.Class_Buy2)
        fade_out.start(self.ids.CarBar)

    def on_pre_enter(self, *args):
        super().on_enter(*args)
        self.ids.Class_Buy1.clear_widgets()
        self.ids.Class_Buy2.clear_widgets()
        sub_classes = os.listdir(f'templates/bebidas_normal')
        for sub_classe in range(0, len(sub_classes) - 1, 2):
            self.ids.Class_Buy2.add_widget(
                SubClassCreate(text1='bebidas', sub_classe1=sub_classes[sub_classe], text2='bebidas',
                               sub_classe2=sub_classes[sub_classe + 1]))
        if len(sub_classes) % 2 != 0:
            self.ids.Class_Buy2.add_widget(SCCimpar(text1='bebidas', sub_classe1=sub_classes[len(sub_classes) - 1]))

        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.ids.Class_Buy1)
        anim.start(self.ids.Class_Buy2)
        anim.start(self.ids.CarBar)

        classes = os.listdir('templates/classes_normal')
        for classe in classes:
            self.ids.Class_Buy1.add_widget(
                ClassCreate(text=classe.replace('.png', ''), image_source=f'templates/classes_normal/{classe}'))

        self.ids.CarBar.clear_widgets()
        itens = fc.txt_to_py('manager_files/carrinho.txt')
        for item in range(0, len(itens), 2):
            self.ids.CarBar.add_widget(CarConstruct(itens[item], float(itens[item + 1])))

    def trigger_buy_screen(self, btn1_text):
        self.ids.Class_Buy2.clear_widgets()
        sub_classes = os.listdir(f'templates/{btn1_text}_normal')
        for sub_classe in range(0, len(sub_classes) - 1, 2):
            self.ids.Class_Buy2.add_widget(
                SubClassCreate(text1=btn1_text, sub_classe1=sub_classes[sub_classe], text2=btn1_text,
                               sub_classe2=sub_classes[sub_classe + 1]))
        if len(sub_classes) % 2 != 0:
            self.ids.Class_Buy2.add_widget(SCCimpar(text1=btn1_text, sub_classe1=sub_classes[len(sub_classes) - 1]))


class CarConstruct(BoxLayout):
    def __init__(self, text, price, **kwargs):
        super().__init__(**kwargs)
        self.ids.item.text = text
        self.text = text
        self.price = price
        fc.file_append('manager_files/nota_fiscal.txt', self.text)

    def remove_self(self):
        parent_layout = self.parent
        if parent_layout:
            parent_layout.remove_widget(self)
            fc.remove_line_from_file('manager_files/carrinho.txt', self.text + '\n')
            fc.remove_line_from_file('manager_files/carrinho.txt', str(self.price) + '\n')
            fc.remove_line_from_file('manager_files/nota_fiscal.txt', self.text)
            global tot
            tot -= self.price
            print(tot)

    def duplicate_self(self):
        parent_layout = self.parent
        if parent_layout:
            parent_layout.add_widget(CarConstruct(text=self.text, price=self.price))
            fc.file_append('manager_files/carrinho.txt', self.text)
            fc.file_append('manager_files/carrinho.txt', self.price)
            global tot
            tot += self.price
            print(tot)


class ClassCreate(BoxLayout):
    def __init__(self, text='', image_source='', **kwargs):
        super().__init__(**kwargs)
        anim = Animation(pos_hint={'center_x': 0.5}, duration=0.5)
        anim.start(self.ids.btn1)
        self.ids.btn1.text = text
        self.ids.btn1.background_normal = image_source
        self.ids.btn1.background_down = image_source.replace('normal', 'down')
        self.ids.btn1.bind(on_release=self.on_button_release)

    def on_button_release(self, *args):
        btn1_text = self.ids.btn1.text
        app = App.get_running_app()
        app.root.get_screen('BuyScreen').trigger_buy_screen(btn1_text.lower())


class SubClassCreate(BoxLayout):
    def __init__(self, text1='', sub_classe1='', text2='', sub_classe2='', **kwargs):
        super().__init__(**kwargs)
        anim = Animation(pos_hint={'center_y': 0.5}, duration=0.5)
        anim.start(self.ids.btn2)
        self.ids.btn2.background_normal = f'templates/{text1}_normal/{sub_classe1}'
        self.ids.btn2.background_down = f'templates/{text1}_down/{sub_classe1}'
        self.ids.btn2.bind(on_release=lambda x: on_button_release(text1, sub_classe1))

        anim = Animation(pos_hint={'center_y': 0.5}, duration=0.5)
        anim.start(self.ids.btn3)
        self.ids.btn3.background_normal = f'templates/{text2}_normal/{sub_classe2}'
        self.ids.btn3.background_down = f'templates/{text2}_down/{sub_classe2}'
        self.ids.btn3.bind(on_release=lambda x: on_button_release(text2, sub_classe2))


def on_button_release(text, sub_classe):
    app = App.get_running_app()
    item_screen = app.root.get_screen('ItemScreen')
    item_screen.update_image(f'templates/{text}_normal/{sub_classe}')
    item_screen.name_and_class(f'{text} - {sub_classe.replace('.png', '')}: ')
    app = App.get_running_app()
    app.root.transition.duration = 1.0
    app.root.transition.direction = 'up'
    app.root.current = 'ItemScreen'


class SCCimpar(BoxLayout):
    def __init__(self, text1='', sub_classe1='', **kwargs):
        super().__init__(**kwargs)

        anim = Animation(pos_hint={'center_y': 0.5}, duration=0.5)
        anim.start(self.ids.btn4)
        self.ids.btn4.background_normal = f'templates/{text1}_normal/{sub_classe1}'
        self.ids.btn4.background_down = f'templates/{text1}_down/{sub_classe1}'
        self.ids.btn4.bind(on_release=lambda x: on_button_release(text1, sub_classe1))


class ItemScreen(Screen):
    def __init__(self, **kwargs):
        super(ItemScreen, self).__init__(**kwargs)
        self.ids['food'] = Image()

        with self.canvas:
            Color(1.0, 1.0, 1.0, 1.0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def on_size(self, *args):
        self.rect.size = self.size

    def on_pos(self, *args):
        self.rect.pos = self.pos

    def update_image(self, image_path, *args):
        super().on_enter(*args)

        anim = Animation(opacity=1, pos_hint={'center_y': 0.5, 'top': 0.8}, duration=0.3)
        anim.start(self.ids.item)
        self.ids.food.source = image_path
        self.ids.food.reload()

        self.ids.Add.clear_widgets()

        try:
            lista = fc.txt_to_py(image_path.replace('.png', '.txt').replace('normal', 'text'))
            print(f"Linhas do arquivo de texto: {lista}")
            self.price = lista[0]
            if len(lista) >= 3:
                for element in range(1, len(lista), 2):
                    self.add_list_create(lista[element], lista[element + 1])
        except Exception as e:
            print(f"Erro ao processar arquivos: {e}")

    def name_and_class(self, name_class):
        self.name_class = name_class

    def on_add_to_cart_button_release(self):
        try:
            global tot
            tot += float(self.price)
            fc.file_append('manager_files/carrinho.txt', f'{self.name_class}R${self.price.replace('.', ',')}')
            fc.file_append('manager_files/carrinho.txt', float(self.price))
        except AttributeError:
            print('object has no attribute price')
        except Exception as e:
            print(f'Error: {e}')

    def on_back_button_release(self):
        app = App.get_running_app()
        app.root.transition.duration = 1.0
        app.root.transition.direction = 'down'
        app.root.current = 'BuyScreen'

    def add_list_create(self, text, price):
        try:
            self.ids.Add.add_widget(ListCreate(text=text, price=price))
            print(f"ListCreate adicionado com texto: {text}")
        except Exception as e:
            print(f"Erro ao adicionar ListCreate: {e}")

    def on_pre_enter(self, *args):
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.ids.ItemScreen)

    def on_pre_leave(self, *args):
        anim = Animation(opacity=0, duration=0.5)
        anim.start(self.ids.ItemScreen)


class ListCreate(BoxLayout):
    def __init__(self, text='', price='', **kwargs):
        super().__init__(**kwargs)
        self.ids.item1.text = f'[b][color=000000]{text}[/color] [color=FA2B2B]R${price}[/color][/b]'


class Shopping(App):
    def build(self):
        target_ratio = 210 / 297

        def on_resize(window, width, height):
            current_ratio = width / height

            if current_ratio != target_ratio:
                new_width = height * target_ratio
                Window.size = (new_width, height)

        Window.bind(on_resize=on_resize)
        Window.size = (595, 842)

        return Manager()


if __name__ == '__main__':
    Shopping().run()