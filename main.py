# (c) 2021 Itai Shek 

from kivy.config import Config

Config.set('graphics', 'width', '285')
Config.set('graphics', 'height', '560')

from random import choice
import string
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty
from kivy.app import App
from kivy import require
require('2.0.0')


class MainWidget(Widget):
    password_value = StringProperty('')
    password_length = NumericProperty(6)
    all_choices = StringProperty('')

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits
    symbols_with = string.punctuation
    symbols_without = ''

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.symbols_without = self.remove_ambiguous_symbols(str_to_remove_from=self.symbols_with)
        self.bind(all_choices=self.on_press_generate_button)
        self.bind(password_length=self.on_press_generate_button)

    @staticmethod
    def remove_ambiguous_symbols(str_to_remove_from):
        ambiguous_symbols = '{}[]()/\\\'"`~,;:.<>'
        for i in ambiguous_symbols:
            str_to_remove_from = str_to_remove_from.replace(i, '')
        return str_to_remove_from

    # add characters to all_choices
    def on_checkbox_active(self):
        choices = ''

        if self.ids.lowercase.active:
            choices += self.lowercase
        if self.ids.uppercase.active:
            choices += self.uppercase
        if self.ids.numbers.active:
            choices += self.numbers
        if self.ids.symbols.active:
            if self.ids.ambiguous.active:
                choices += self.symbols_without
            else:
                choices += self.symbols_with
        if self.ids.custom.active:
            if self.ids.ambiguous.active:
                choices += self.remove_ambiguous_symbols(str_to_remove_from=self.ids.custom_symbols.text)
            else:
                choices += self.ids.custom_symbols.text
            # remove duplicate characters
            choices = ''.join(set(choices))

        self.all_choices = choices

    # get password's length from slider
    def on_value_slider(self, slider):
        self.password_length = slider.value

    # generate password
    def on_press_generate_button(self, *args):
        self.password_value = ''
        if self.all_choices:
            self.password_value = ''.join([choice(self.all_choices) for _ in range(self.password_length)])


class PasswordGenerator(App):
    def build(self):
        self.icon = 'images/icon.png'
        return MainWidget()


if __name__ == '__main__':
    PasswordGenerator().run()
