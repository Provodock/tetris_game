import random
import os
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.image import AsyncImage, Image
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label
from random import randint, uniform

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.slider import Slider
from kivy.core.window import Window
import subprocess


from kivy.core.audio import SoundLoader
from kivy.clock import Clock

class MusicPlayer:
    def __init__(self):
        self.music = SoundLoader.load('music1.mp3')
        self.music.bind(on_stop=self.play_music)
        self.load_settings()

    def play_music(self, *args):
        if self.music.state != 'play':
            self.music.play()

    def load_settings(self):
        try:
            from settings import MUSIC_VOLUME
            self.music.volume = MUSIC_VOLUME
        except ImportError:
            self.music.volume = 0.5


#Основне вікно
class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        Window.fullscreen = 'auto'
        layout_img = BoxLayout(orientation='vertical', spacing=30, padding=(25, 10,330, 500))
        self.img = AsyncImage(source="sourses/tetris.png", size_hint=(1.2, 1.2), allow_stretch=True)
        layout = BoxLayout(orientation='vertical', spacing=30, padding=(10, 250, 10, 250))
        self.btn1 = Button(text='Один гравець', on_press=self.player1, size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn2 = Button(text='Пара граців', on_press=self.player2, size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn3 = Button(text='Налаштування', on_press=self.options, size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn4 = Button(text='Інше', on_press=self.other, size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn5 = Button(text='Вихід', on_press=self.exit, size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.figures = [f for f in os.listdir('sourses/figures') if f.endswith('.png')]
        Clock.schedule_interval(self.Falling, 1/3)
        layout.add_widget(self.btn1)
        layout.add_widget(self.btn2)
        layout.add_widget(self.btn3)
        layout.add_widget(self.btn4)
        layout.add_widget(self.btn5)
        layout_img.add_widget(self.img)
        self.add_widget(layout_img)
        self.add_widget(layout)

    def player1(self, instance):
        self.manager.current = 'page1'

    def player2(self, instance):
        self.manager.current = 'page2'

    def options(self, instance):
        self.manager.current = 'page3'

    def other(self, instance):
        self.manager.current = 'page4'

    def exit(self, instance):
        App.get_running_app().stop()

    def Falling(self, *args):
        figure_path = os.path.join('sourses/figures', random.choice(self.figures))
        image = Image(source=figure_path)
        image.center_x = randint(-1000, Window.width )
        image.y = Window.height
        image.rotation = uniform(-45, 45)
        anim = Animation(center_y=-100, duration=5)
        anim.start(image)
        self.add_widget(image)
        return image

#Вікно одного грвця
class Page1(Screen):
    def __init__(self, **kwargs):
        super(Page1, self).__init__(**kwargs)
        layout_img = BoxLayout(orientation='vertical', spacing=30, padding=(25, 10, 330, 500))
        self.img = AsyncImage(source="sourses/tetris.png", size_hint=(1.2, 1.2), allow_stretch=True)
        layout = BoxLayout(orientation='vertical', spacing=30, padding=(10, 250, 10, 250))
        self.lbl1 = Label(text='Оберіть складність гри:', size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn1 = Button(text='Дитина', on_press=self.level1, size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn2 = Button(text='Школяр', on_press=self.level2,  size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn3 = Button(text='Студент', on_press=self.level3, size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn4 = Button(text='Прошарений', on_press=self.level4, size_hint=(None, None), size=(170, 50),  pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn5 = Button(text="Пам'ятаю часи...", on_press=self.level5, size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout_mbtn = BoxLayout(orientation='vertical', spacing=10, padding=(10, 500, 10, 10))
        mbtn = Button(text='До головної', on_press=self.go_to_main_page, size_hint=(None, None), size=(135, 30), pos_hint={'center_x': 0.9, 'center_y': 0.5})
        layout.add_widget(self.lbl1)
        layout.add_widget(self.btn1)
        layout.add_widget(self.btn2)
        layout.add_widget(self.btn3)
        layout.add_widget(self.btn4)
        layout.add_widget(self.btn5)
        layout_img.add_widget(self.img)
        layout_mbtn.add_widget(mbtn)
        self.add_widget(layout_img)
        self.add_widget(layout)
        self.add_widget(layout_mbtn)


    def go_to_main_page(self, instance):
        self.manager.current = 'main'

    def level1(self, instance):
        print()

    def level2(self, instance):
        print()

    def level3(self, instance):
        print()

    def level4(self, instance):
        print()

    def level5(self, instance):
        print()

#В теорії вікно двох граців
class Page2(Screen):
    def __init__(self, **kwargs):
        super(Page2, self).__init__(**kwargs)
        layout_1 = GridLayout(cols=2, spacing=10, padding=(100, 250, 10, 10))
        label_1 = Label(text='Введіть x:', size_hint=(None, None), size=(170, 30))
        self.inp1 = TextInput(multiline=False, size_hint=(None, None), size=(170, 30))
        label_2 = Label(text='Введіть y:', size_hint=(None, None), size=(170, 30))
        self.inp2 = TextInput(multiline=False, size_hint=(None, None), size=(170, 30))
        label_3 = Label(text='Введіть z:', size_hint=(None, None), size=(170, 30))
        self.inp3 = TextInput(multiline=False, size_hint=(None, None), size=(170, 30))

        layout_2 = GridLayout(cols=1, spacing=10, padding=(550, 250, 10, 10))
        self.label_5 = Label(text='', size_hint=(None, None), size=(170, 30))
        self.label_6 = Label(text='', size_hint=(None, None), size=(170, 30))
        self.label_7 = Label(text='', size_hint=(None, None), size=(170, 30))

        layout = BoxLayout(orientation='vertical', spacing=30, padding=(10, 200, 10, 150))
        self.label_4 = Label(text='', size_hint=(None, None), size=(340, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        btn1 = Button(text='Отримати результат', on_press=self.get_result, size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        btn2 = Button(text='Зчитати з файлу', on_press=self.read_file, size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout_mbtn = BoxLayout(orientation='vertical', spacing=10, padding=(10, 500, 10, 10))
        mbtn = Button(text='До головної', on_press=self.go_to_main_page, size_hint=(None, None), size=(135, 30), pos_hint={'center_x': 0.9, 'center_y': 0.5})
        layout_1.add_widget(label_1)
        layout_1.add_widget(self.inp1)
        layout_1.add_widget(label_2)
        layout_1.add_widget(self.inp2)
        layout_1.add_widget(label_3)
        layout_1.add_widget(self.inp3)
        layout_2.add_widget(self.label_5)
        layout_2.add_widget(self.label_6)
        layout_2.add_widget(self.label_7)
        layout.add_widget(self.label_4)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout_mbtn.add_widget(mbtn)
        self.add_widget(layout_1)
        self.add_widget(layout_2)
        self.add_widget(layout)
        self.add_widget(layout_mbtn)

    def get_result(self, instance):
        try:
            x = float(self.inp1.text)
            y = float(self.inp2.text)
            z = float(self.inp3.text)
            if x==0  or z==0:
                self.label_4.text = 'Будь ласка, введіть числа відмінні від нуля'
                self.label_5.text = ''
                self.label_6.text = ''
                self.label_7.text = ''
            else:
                if x > 0:
                    y1 = (123 * (x ** 3) + 124 * (y ** 4)) / (125 * (z ** 5))
                    self.label_5.text = 'Ваш результат: Y = ' + str(y1)
                elif x <= 0:
                    self.label_5.text = 'Число не більше 0'
                if y > 0:
                    y2 = (123 * (y ** 3) + 124 * (z ** 4)) / (125 * (x ** 5))
                    self.label_6.text = 'Ваш результат: Y = ' + str(y2)
                elif y <= 0:
                    self.label_6.text = 'Число не більше 0'
                if z > 0:
                    y3 = (123 * (z ** 3) + 124 * (y ** 4)) / (125 * (x ** 5))
                    self.label_7.text = 'Ваш результат: Y = ' + str(y3)
                elif z <= 0:
                    self.label_7.text = 'Число не більше 0'
                self.label_4.text = ''
        except ValueError:
            self.label_4.text = 'Будь ласка, введіть числа'

    def read_file(self, instance):
        f = open(r"D:/Python/Code/2.txt", "r", encoding="cp1051")
        s = f.read()
        f.close()
        f = s.split(' ')
        x = float(f[0])
        y = float(f[1])
        z = float(f[2])
        if x > 0:
            y1 = (123 * (x ** 3) + 124 * (y ** 4)) / (125 * (z ** 5))
            self.label_5.text = 'Ваш результат: Y = ' + str(y1)
        elif x <= 0:
            self.label_5.text = 'Число не більше 0'
        if y > 0:
            y2 = (123 * (y ** 3) + 124 * (z ** 4)) / (125 * (x ** 5))
            self.label_6.text = 'Ваш результат: Y = ' + str(y2)
        elif y <= 0:
            self.label_6.text = 'Число не більше 0'
        if z > 0:
            y3 = (123 * (z ** 3) + 124 * (y ** 4)) / (125 * (x ** 5))
            self.label_7.text = 'Ваш результат: Y = ' + str(y3)
        elif z <= 0:
            self.label_7.text = 'Число не більше 0'
        self.label_4.text = ''

    def go_to_main_page(self, instance):
        self.manager.current = 'main'

class Page3(Screen):
    def __init__(self, **kwargs):
        from settings import MUSIC_VOLUME
        super(Page3, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation='vertical', spacing=25, padding=(30, 30, 30, 30))

        # Налаштування музики та звуку
        music_layout = BoxLayout(orientation='horizontal')
        self.music_slider = Slider(min=0, max=1, value=0.5)
        self.sound_slider = Slider(min=0, max=1, value=0.5)
        music_label = Label(text='Музика')
        sound_label = Label(text='Звуки')
        music_layout.add_widget(music_label)
        music_layout.add_widget(self.music_slider)
        music_layout.add_widget(sound_label)
        music_layout.add_widget(self.sound_slider)
        main_layout.add_widget(music_layout)
        self.music_slider.value = MUSIC_VOLUME
        # Налаштування клавіатури
        keyboard_layout = GridLayout(cols=2, spacing=30, padding=(30, 30, 30, 30))
        keyboard_labels = ['Перевернути фігуру', 'Пересунути вліво', 'Пришвидшити падіння', 'Пауза']
        self.key_inputs = []
        for label_text in keyboard_labels:
            label = Label(text=label_text)
            input_field = TextInput(multiline=False, size_hint=(None, None), size=(170, 30))
            keyboard_layout.add_widget(label)
            keyboard_layout.add_widget(input_field)
            self.key_inputs.append(input_field)
        main_layout.add_widget(keyboard_layout)

        # Кнопки для виходу та підтвердження
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        confirm_button = Button(text='Підтвердити', on_press=self.save_settings)
        exit_button = Button(text='Вихід', on_press=self.go_to_main_page)
        button_layout.add_widget(confirm_button)
        button_layout.add_widget(exit_button)
        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)

         # Запланувати періодичне оновлення гучності музики
        Clock.schedule_interval(self.update_music_volume, 0.1)

    def save_settings(self, instance):
        # Зберігаємо налаштування у файл settings.py
        settings_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(settings_dir, 'settings.py')

        with open(settings_file, 'w') as f:
            f.write(f"MUSIC_VOLUME = {self.music_slider.value}\n")
            f.write(f"SOUND_VOLUME = {self.sound_slider.value}\n")
            f.write("KEYBINDINGS = [\n")
            for input_field in self.key_inputs:
                f.write(f"    '{input_field.text}',\n")
            f.write("]\n")


        # Оновлення гучності музики
        app = App.get_running_app()
        app.music_player.music.volume = self.music_slider.value



    def update_music_volume(self, *args):
        app = App.get_running_app()
        app.music_player.music.volume = self.music_slider.value

    def go_to_main_page(self, instance):
        self.manager.current = 'main'

class Page4(Screen):
    def __init__(self, **kwargs):
        super(Page4, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.139, 0.777, 0.025, 1)
            self.rect = Rectangle(size=(100000, 1000))
        layout_1 = GridLayout(cols=2, spacing=10, padding=(250, 250, 10, 10))
        label_1 = Label(text='Введіть n:', size_hint=(None, None), size=(170, 30))
        self.inp1 = TextInput(multiline=False, size_hint=(None, None), size=(170, 30))
        label_2 = Label(text='Введіть a:', size_hint=(None, None), size=(170, 30))
        self.inp2 = TextInput(multiline=False, size_hint=(None, None), size=(170, 30))
        label_3 = Label(text='Введіть b:', size_hint=(None, None), size=(170, 30))
        self.inp3 = TextInput(multiline=False, size_hint=(None, None), size=(170, 30))
        layout = BoxLayout(orientation='vertical', spacing=30, padding=(10, 10, 10, 150))
        self.label_4 = Label(text='', size_hint=(None, None), size=(340, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        btn1 = Button(text='Отримати результат', on_press=self.get_result, size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        btn2 = Button(text='Зчитати з файлу', on_press=self.read_file, size_hint=(None, None), size=(170, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout_mbtn = BoxLayout(orientation='vertical', spacing=10, padding=(10, 500, 10, 10))
        mbtn = Button(text='До головної', on_press=self.go_to_main_page, size_hint=(None, None), size=(135, 30), pos_hint={'center_x': 0.9, 'center_y': 0.5})
        layout_1.add_widget(label_1)
        layout_1.add_widget(self.inp1)
        layout_1.add_widget(label_2)
        layout_1.add_widget(self.inp2)
        layout_1.add_widget(label_3)
        layout_1.add_widget(self.inp3)
        layout.add_widget(self.label_4)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout_mbtn.add_widget(mbtn)
        self.add_widget(layout_1)
        self.add_widget(layout)
        self.add_widget(layout_mbtn)

    def get_result(self, instance):
        try:
            n = int(self.inp1.text)
            a = int(self.inp2.text)
            b = int(self.inp3.text)
            result=0
            if n>1:
                for i in range(1, n + 1):
                    for j in range(1, n + 1):
                        result += a ** i + b ** j
                self.label_4.text = 'Ваш результат: ' + str(result)
            else:
                self.label_4.text = 'Будь ласка, введіть N більше 1'
        except ValueError:
            self.label_4.text = 'Будь ласка, введіть числа'

    def read_file(self, instance):
        f = open(r"D:/Python/Code/3.txt", "r", encoding="cp1051")
        s = f.read()
        f.close()
        f = s.split(' ')
        n = int(f[0])
        a = int(f[1])
        b = int(f[2])
        result = 0
        if n > 1:
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    result += a ** i + b ** j
            self.label_4.text = 'Ваш результат: ' + str(result)
        else:
            self.label_4.text = 'Будь ласка, введіть N більше 1'

    def go_to_main_page(self, instance):
        self.manager.current = 'main'


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.music_player = MusicPlayer()
        self.music_player.play_music()
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainPage(name='main'))
        sm.add_widget(Page1(name='page1'))
        sm.add_widget(Page2(name='page2'))
        sm.add_widget(Page3(name='page3'))
        sm.add_widget(Page4(name='page4'))

        return sm

if __name__ == '__main__':
    MyApp().run()