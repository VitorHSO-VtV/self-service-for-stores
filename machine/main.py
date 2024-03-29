from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
from pix_generator import *
from kivy.app import App
import functions as fc
import os

tot = 0
where_eat = 0
screen = 0


class Manager(ScreenManager):
    pass


class InitScreen(Screen):
    def on_enter(self, *args):
        fc.clear_file('manager_files/cart.txt')
        fc.clear_file('manager_files/invoice_items.txt')
        fc.clear_file('manager_files/item_note.txt')
        fc.clear_file('manager_files/finalized_invoice.txt')

        global tot
        tot = 0
        global where_eat
        where_eat = 0
        global screen
        screen = 0

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

    def on_tools_button_press(self):
        Clock.schedule_once(self.notify_pressed, 5)

    def on_tools_button_release(self):
        Clock.unschedule(self.notify_pressed)

    def notify_pressed(self, dt):
        print("Botão pressionado por 5 segundos")


class WhereEat(Popup):
    def to_stay(self):
        self.dismiss()
        fc.append_line('manager_files/invoice_items.txt', 'Comer Aqui')

    def to_go(self):
        self.dismiss()
        fc.append_line('manager_files/invoice_items.txt', 'Para Levar')


class BuyScreen(Screen):
    def on_pre_leave(self):
        fade_out = Animation(opacity=0, duration=0.5)
        fade_out.start(self.ids.BuyScreen)

    def on_pre_enter(self, *args):
        super().on_enter(*args)
        global screen
        self.ids.Class_Buy1.clear_widgets()
        self.ids.Class_Buy2.clear_widgets()
        classes = os.listdir(f'templates/classes_normal')
        sub_classes = os.listdir(f'templates/{classes[screen].replace(".png", "")}_normal')

        for sub_classe in range(0, len(sub_classes) - 1, 2):
            self.ids.Class_Buy2.add_widget(
                SubClassCreate(text1=classes[screen].replace('.png', ''), sub_classe1=sub_classes[sub_classe],
                               text2=classes[screen].replace('.png', ''),
                               sub_classe2=sub_classes[sub_classe + 1]))

        if len(sub_classes) % 2 != 0:
            self.ids.Class_Buy2.add_widget(
                SCCodd(text1=classes[screen].replace('.png', ''), sub_classe1=sub_classes[len(sub_classes) - 1]))

        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.ids.BuyScreen)

        for classe in range(0, len(classes)):
            self.ids.Class_Buy1.add_widget(
                ClassCreate(text=classes[classe].replace('.png', ''),
                            image_source=f'templates/classes_normal/{classes[classe]}', s_id=classe))

        self.ids.CartBar.clear_widgets()
        items = fc.read_lines('manager_files/cart.txt')

        for item in range(0, len(items), 2):
            self.ids.CartBar.add_widget(CartConstruct(items[item], float(items[item + 1])))

        global where_eat
        if where_eat == 0:
            where_eat = 1
            WhereEat().open()

    @staticmethod
    def on_cart_button_release():
        app = App.get_running_app()
        app.root.transition.duration = 1.0
        app.root.transition.direction = 'up'
        app.root.current = 'CarScreen'

    def trigger_buy_screen(self, btn1_text):
        self.ids.Class_Buy2.clear_widgets()
        sub_classes = os.listdir(f'templates/{btn1_text}_normal')

        for sub_classe in range(0, len(sub_classes) - 1, 2):
            self.ids.Class_Buy2.add_widget(
                SubClassCreate(text1=btn1_text, sub_classe1=sub_classes[sub_classe], text2=btn1_text,
                               sub_classe2=sub_classes[sub_classe + 1]))

        if len(sub_classes) % 2 != 0:
            self.ids.Class_Buy2.add_widget(SCCodd(text1=btn1_text, sub_classe1=sub_classes[len(sub_classes) - 1]))


class CartConstruct(BoxLayout):
    def __init__(self, text, price, **kwargs):
        super().__init__(**kwargs)
        self.ids.item.text = text
        self.text = text
        self.price = price

    def remove_self(self):
        parent_layout = self.parent
        if parent_layout:
            parent_layout.remove_widget(self)
            fc.remove_line('manager_files/cart.txt', self.text + '\n')
            fc.remove_line('manager_files/cart.txt', str(self.price) + '\n')
            fc.remove_line('manager_files/invoice_items.txt', self.text + '\n')
            global tot
            tot -= self.price
            print(tot)

    def duplicate_self(self):
        parent_layout = self.parent
        if parent_layout:
            parent_layout.add_widget(CartConstruct(text=self.text, price=self.price))
            fc.append_line('manager_files/cart.txt', self.text)
            fc.append_line('manager_files/cart.txt', self.price)
            fc.append_line('manager_files/invoice_items.txt', self.text)
            global tot
            tot += self.price
            print(tot)


class ClassCreate(BoxLayout):
    def __init__(self, text='', image_source='', s_id=None, **kwargs):
        super().__init__(**kwargs)
        anim = Animation(pos_hint={'center_x': 0.5}, duration=0.5)
        anim.start(self.ids.btn1)
        self.s_id = s_id
        self.text = text
        self.ids.btn1.background_normal = image_source
        self.ids.btn1.background_down = image_source.replace('normal', 'down')
        self.ids.btn1.bind(on_release=self.on_button_release)

    def on_button_release(self, *args):
        global screen
        screen = self.s_id
        app = App.get_running_app()
        app.root.get_screen('BuyScreen').trigger_buy_screen(self.text.lower())


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
    item_screen.name_and_class(f'{text} - {sub_classe.replace(".png", "")}: ')
    app = App.get_running_app()
    app.root.transition.duration = 1.0
    app.root.transition.direction = 'up'
    app.root.current = 'ItemScreen'


class SCCodd(BoxLayout):
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
        self.price = None
        self.name_class = None
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
            lista = fc.read_lines(image_path.replace('.png', '.txt').replace('normal', 'text'))
            print(f'Linhas do arquivo de texto: {lista}')
            self.price = lista[0]
            if len(lista) >= 3:
                for element in range(1, len(lista)):
                    self.add_list_create(lista[element])
        except Exception as e:
            print(f'Erro ao processar arquivos: {e}')

    def name_and_class(self, name_class):
        self.name_class = name_class

    def on_add_to_cart_button_release(self):
        try:
            global tot
            tot += float(self.price)
            fc.append_line('manager_files/cart.txt', f'{self.name_class}R${self.price.replace(".", ",")}')
            fc.append_line('manager_files/cart.txt', float(self.price))
            fc.append_line('manager_files/invoice_items.txt', f'{self.name_class}R${self.price.replace(".", ",")}')
            items = fc.read_lines('manager_files/item_note.txt')

            for item in items:
                fc.append_line('manager_files/invoice_items.txt', f'...{item}...')

            app = App.get_running_app()
            app.root.transition.duration = 1.0
            app.root.transition.direction = 'down'
            app.root.current = 'BuyScreen'

        except AttributeError:
            print('object has no attribute price')
        except Exception as e:
            print(f'Error: {e}')

    @staticmethod
    def on_back_button_release():
        app = App.get_running_app()
        app.root.transition.duration = 1.0
        app.root.transition.direction = 'down'
        app.root.current = 'BuyScreen'

    def add_list_create(self, text):
        try:
            self.ids.Add.add_widget(ListCreate(text=text))
            print(f'ListCreate adicionado com texto: {text}')
        except Exception as e:
            print(f'Erro ao adicionar ListCreate: {e}')

    def on_pre_enter(self, *args):
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.ids.ItemScreen)

    def on_pre_leave(self, *args):
        anim = Animation(opacity=0, duration=0.5)
        anim.start(self.ids.ItemScreen)
        fc.clear_file('manager_files/item_note.txt')


class ListCreate(BoxLayout):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        fc.append_line('manager_files/item_note.txt', text)
        self.ids.item1.text = f'[b][color=000000]{text}[/color]'
        self.text = text
        self.yn = 0

    def on_item_add(self):
        if self.yn == 0:
            fc.remove_line('manager_files/item_note.txt', self.text + '\n')
            self.yn = 1
            self.ids.item1.canvas.before.clear()
            with self.ids.item1.canvas.before:
                Color(0.85, 0, 0, 0.8)
                Rectangle(pos=self.ids.item1.pos, size=self.ids.item1.size)
        else:
            fc.append_line('manager_files/item_note.txt', self.text)
            self.yn = 0
            self.ids.item1.canvas.before.clear()
            with self.ids.item1.canvas.before:
                Color(0.85, 0.85, 0.85, 1)
                Rectangle(pos=self.ids.item1.pos, size=self.ids.item1.size)

    def on_pre_enter(self):
        self.background_color = (0.85, 0.85, 0.85, 1)


class CarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    def on_pre_enter(self, *args):
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.ids.CarScreen)

        self.ids.invoice.clear_widgets()
        items = fc.read_lines('manager_files/cart.txt')

        for item in range(0, len(items), 2):
            self.ids.invoice.add_widget(CartConstruct(items[item], float(items[item + 1])))

    def on_pre_leave(self, *args):
        anim = Animation(opacity=0, duration=0.5)
        anim.start(self.ids.CarScreen)

    @staticmethod
    def on_back_button_release():
        app = App.get_running_app()
        app.root.transition.duration = 1.0
        app.root.transition.direction = 'down'
        app.root.current = 'BuyScreen'

    def on_finalize_purchase(self):
        invoice_information_store = fc.read_lines('manager_files/invoice_information_store.txt')

        for information in invoice_information_store:
            fc.append_line('manager_files/finalized_invoice.txt', information)

        items = fc.read_lines('manager_files/invoice_items.txt')

        for item in items:
            fc.append_line('manager_files/finalized_invoice.txt', item)

        global tot
        fc.append_line('manager_files/finalized_invoice.txt', f'Total: R${"{:.2f}".format(tot).replace(".", ",")}')

        password = fc.read_lines('manager_files/password.txt')
        for pas in password:
            fc.append_line('manager_files/finalized_invoice.txt', pas)

        password_now = int(password[0].replace('-------------------SENHA-', '').replace('-------------------', ''))
        password_now += 1

        if password_now == 1000:
            password_now = 100

        fc.clear_file('manager_files/password.txt')
        fc.append_line('manager_files/password.txt', f'-------------------SENHA-{password_now}-------------------')

        fc.text_to_pdf('manager_files/finalized_invoice.txt', 'manager_files/invoice.pdf')

        app = App.get_running_app()
        app.root.transition.duration = 1.0
        app.root.transition.direction = 'up'
        app.root.current = 'PayScreen'


class PayScreen(Screen):
    def on_pre_enter(self, *args):
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.ids.PayScreen)

    def on_pixqr(self, *args):
        payload = Payload('VITOR H DOS S OLIPIA', '+5548988180197', '0.01', 'SAO JOSE', '***', 'manager_files')
        payload.generate_payload()
        app = App.get_running_app()
        app.root.transition.duration = 1.0
        app.root.transition.direction = 'up'
        app.root.current = 'PixScreen'

    def on_pre_leave(self, *args):
        anim = Animation(opacity=0, duration=0.5)
        anim.start(self.ids.PayScreen)


class PixScreen(Screen):
    def on_pre_enter(self, *args):
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.ids.PixScreen)
        self.ids.qrcode.source = 'manager_files/pixqrcode.png'

    def on_pre_leave(self, *args):
        anim = Animation(opacity=0, duration=0.5)
        anim.start(self.ids.PixScreen)

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
