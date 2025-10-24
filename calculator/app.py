#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial
from tkinter import PhotoImage, font
from tkinter import Tk, Canvas, Frame, Label, Entry, Button
from calculator import utils
from calculator.logic import Logic



class CalculatorApp(Logic):
    def __init__(self):
        super().__init__()
        
        self.root = Tk()
        self.images = set()

        self.root.title('Calculator')
        self.root.resizable(False, False)
        self.root.geometry(self.align_to_center())
        self.root.iconphoto(True, self.load_image('iconphoto.png'))

        self.canvas = Canvas(
            master=self.root,
            background='#303030',
            highlightthickness=0
        )
        self.canvas.place(relheight=1, relwidth=1)
        self.canvas.create_image(140, 63, image=self.load_image('image_1.png'))

        self.display_frame = Frame(
            master=self.canvas,
            background='#97B172',
            relief='flat'
        )
        self.display_frame.place(x=20, y=35, width=240, height=56)

        self.memory_label = Label(
            master=self.display_frame,
            font=('Default', 9, 'bold'),
            background=self.display_frame.cget('background')
        )
        self.memory_label.place(relheight=0.33, relwidth=0.08)

        self.operator_label = Label(
            master=self.display_frame,
            font=('Default', 12, 'bold'),
            background=self.display_frame.cget('background')
        )
        self.operator_label.place(rely=0.33, relheight=0.33, relwidth=0.08)

        self.error_label = Label(
            master=self.display_frame,
            font=('Default', 9, 'bold'),
            background=self.display_frame.cget('background')
        )
        self.error_label.place(rely=0.66, relheight=0.33, relwidth=0.08)

        self.display = Entry(
            master=self.display_frame,
            borderwidth=4,
            highlightthickness=0,
            font=self.font,
            relief='flat',
            justify='right',
            background=self.display_frame.cget('background'),
            readonlybackground=self.display_frame.cget('background'),

        )
        self.display.place(relx=0.08, relheight=1, relwidth=0.92)

        self.buttons_frame = Frame(
            master=self.canvas,
            relief='flat',
            background=self.canvas.cget('background')
        )
        self.buttons_frame.place(x=15, y=120, width=250, height=200)

        # Configure a 5x5 grid for the buttons
        for i in range(5):
            self.buttons_frame.rowconfigure(i, weight=1, minsize=40, uniform='a')
            self.buttons_frame.columnconfigure(i, weight=1, minsize=40, uniform='a')
            
        # Create the buttons
        for row in range(5):
            for column in range(5):
                n = (row * 5 + column) + 1
                name = f'button_{n - 1 if n == 25 else n}'

                button = Button(
                    master=self.buttons_frame,
                    name=name,
                    borderwidth=0,
                    highlightthickness=0,
                    relief='flat',
                    cursor='hand2',
                    image=self.load_image(f'{name}.png'),
                    background=self.canvas.cget('background'),
                    activebackground=self.canvas.cget('background'),
                    command=partial(self.on_button_click, button=name)
                )
    
                # Big plus button
                if (row, column) == (3, 3):
                    button.grid(row=row, column=column, rowspan=2)
                # Skip one grid below the plus button
                if (row, column) == (4, 3):
                    button.destroy() # Delete the unused button
                    continue
                
                button.grid(row=row, column=column)

        # Setup double click function for the 'mrc' button
        mrc_button = self.buttons_frame.nametowidget('button_3')
        mrc_button.bind('<Double-Button-1>', lambda _: self.memory_clear())
        
        self.reset_display()
        self.root.update_idletasks()
        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<Control-plus>', lambda _: self.memory_add())
        self.root.bind('<Control-minus>', lambda _: self.memory_subtract())

    def _check_overflow(self, text: str) -> bool:
        """Checks if the text in the entry widget is overflowing."""
        # Get the font configuration of the entry widget
        widget_font = font.Font(font=self.font)
        # Measure the width of the current text
        text_width_pixels = widget_font.measure(text)
        # Get the actual width of the entry widget in pixels
        entry_width_pixels = self.display.winfo_width()

        return text_width_pixels > (entry_width_pixels - 8)
    
    def _edit_display(self, mode, value=None) -> None:
        self.display.config(state='normal')
        match mode:
            case 'reset':
                self.display.delete(0, 'end')
                self.display.insert(0, '0')
            case 'delete':
                index = len(self.display.get()) - 1
                self.display.delete(index, 'end')
            case 'clear':
                self.display.delete(0, 'end')
            case 'insert':
                if value:
                    text = self.display.get() + value
                    if not self._check_overflow(text=text):
                        self.display.insert('end', value)
                    else:
                        self._show_label('error', show=True)
                        if self.operator_on_display():
                            self._show_label('operator', show=False)
        self.display.config(state='readonly')

    def _show_label(self, label, show=True, text=None) -> None:
        match label:
            case 'memory':
                if show:
                    self.memory_label.config(text='M')
                else:
                    self.memory_label.config(text='')
            case 'error':
                if show:
                    self.error_label.config(text='E')
                else:
                    self.error_label.config(text='')
            case 'operator':
                if show and text:
                    self.operator_label.config(text=text)
                else:
                    self.operator_label.config(text='')

    def on_key_press(self, event) -> None:
        button = None
        match event.keysym:
            case 'Insert' | 'Escape' | 'c' | 'C':
                button = 'c'
            case 'Delete' | 'BackSpace':
                button = 'ce'
            case 'Home' | 'm' | 'M':
                button = 'mrc'
            case 'End':
                button = 'mc'
            case 'Prior':
                button = '%'
            case 'Next':
                button = 'sqrt'
            case 'plus' | 'KP_Add':
                button = '+'
            case 'minus' | 'KP_Subtract':
                button = '-'
            case 'asterisk' | 'KP_Multiply':
                button = '*'
            case 'slash' | 'KP_Divide':
                button = '/'
            case 'period' | 'KP_Decimal':
                button = '.'
            case 'Pause':
                button = '+/-'
            case 'Return' | 'KP_Enter':
                button = '='
            case _:
                if event.char.isdigit():
                    button = event.char
        # Prevents error from other key presses
        if button:
            if button == 'mc':
                self.memory_clear()
            else:
                self.on_button_click(self.reverse_map[button])

    def on_button_click(self, button: str) -> None:
        match self.mapping[button]:
            case 'c':
                self.reset_display()
            case button:
                if not self.error_on_display():
                    match button:
                        case 'ce':
                            self.delete_display()
                        case 'mrc':
                            self.memory_recall()
                        case 'm-':
                            self.memory_subtract()
                        case 'm+':
                            self.memory_add()
                        case '%':
                            self.calculate_percentage()
                        case 'sqrt':
                            self.calculate_square_root()
                        case '.':
                            self.insert_decimal_point()
                        case '+/-':
                            self.negate_input()
                        case '=':
                            self.solve_equation()
                        case _:
                            if button.isdigit():
                                self.insert_digit(button)
                            if button in '*/-+':
                                self.set_operation(button)

    def reset_display(self) -> None:
        self._edit_display('reset')
        self._show_label('error', show=False)
        self._show_label('operator', show=False)
        self.reset_inputs()

    def delete_display(self) -> None:
        if self.display.get() != '0':
            self._edit_display('delete')
            # Reset the display if empty
            if not len(self.display.get()) or self.display.get() == '-':
                self._edit_display('reset')

    def memory_recall(self) -> None:
        if self.memory_on_display() and self._memory:
            self._edit_display('clear')
            self._edit_display('insert', value=self._memory)

            if self.operator_on_display():
                self._show_label('operator', show=False)

    def memory_clear(self) -> None:
        self._memory = None
        self._show_label('memory', show=False)

    def memory_subtract(self) -> None:
        if self.memory_on_display() and self._memory:
            if self.display.get() not in '0.':
                expression = f'{self._memory} - {self.display.get()}'
                result = self.evaluate_expression(expression)
                if result != self._error:
                    self._memory = result
    
    def memory_add(self) -> None:
        if self.display.get() != '0':
            if self._memory:
                expression = f'{self._memory} + {self.display.get()}'
                result = self.evaluate_expression(expression)
                if result != self._error:
                    self._memory = result
            else:
                self._memory = self.display.get()
                self._show_label('memory', show=True)

            if self.operator_on_display():
                self._show_label('operator', show=False)

    def insert_digit(self, digit: str) -> None:
        if self._inputs:
            if self._new_input:
                self._edit_display('clear')
                self._new_input = False
            else:
                if self.display.get() == '0':
                    self._edit_display('clear')
        else:
            if self.display.get() == '0':
                self._edit_display('clear')
                
        self._edit_display('insert', value=digit)
            
    def set_operation(self, operator) -> None:
        if not self._inputs:
            if self.display.get().endswith('.'):
                self._edit_display('delete')
            self._inputs.append(self.display.get())
            self._inputs.append(operator)
        else:
            if self._inputs[-1] != operator:
                self._inputs[-1] = operator
            
        self._new_input = True
        
        map = {'*': chr(215), '/': chr(247), '-': chr(8722), '+': '+'}
        self._show_label('operator', show=True, text=map[operator])

    def insert_decimal_point(self) -> None:
        if self._new_input:
            self._edit_display('clear')
            self._edit_display('insert', value='0.')
            self._new_input = False
        else:
            if '.' not in self.display.get():
                self._edit_display('insert', value='.')

    def calculate_percentage(self) -> None:
        if self._inputs and not self._new_input:
            if self.display.get() != '0':
                first_term, operator = self._inputs
                percent = self.display.get()
                second_term = self.get_percentage(first_term, percent)
                
                if operator == '*':
                    result = second_term
                else:
                    if operator not in '-+/':
                        operator = '*'
                    expression = f'{first_term} {operator} {second_term}'
                    result = self.evaluate_expression(expression)
                
                if result == self._error:
                    self._show_label('error', show=True)
                else:
                    self._edit_display('clear')
                    self._edit_display('insert', value=result)
                    
                self._show_label('operator', show=False)
                self.reset_inputs()
                
    def calculate_square_root(self) -> None:
        if not self._inputs:
            if self.display.get() not in '0.':
                result = self.square_root(self.display.get())
                
                if result == self._error:
                    self._show_label('error', show=True)
                else:
                    self._edit_display('clear')
                    self._edit_display('insert', value=result)

    def solve_equation(self):
        if self._inputs:
            if not self._new_input:
                if self.display.get() not in '0.':
                    self._inputs.append(self.display.get())
                    expression = ' '.join(self._inputs)
                    result = self.evaluate_expression(expression)
                    
                    if result == self._error:
                        self._show_label('error', show=True)
                    else:
                        self._edit_display('clear')
                        self._edit_display('insert', value=result)
                        
                    self._show_label('operator', show=False)
                    self.reset_inputs()
            
    def negate_input(self) -> None:
        if self.display.get() not in '0.':
            if '-' in self.display.get():
                value = self.display.get()[1:]
            else:
                value = '-' + self.display.get()
                
            self._edit_display('clear')
            self._edit_display('insert', value=value)
    
    def error_on_display(self) -> bool:
        return bool(self.error_label.cget('text'))
    
    def memory_on_display(self) -> bool:
        return bool(self.memory_label.cget('text'))
    
    def operator_on_display(self) -> bool:
        return bool(self.operator_label.cget('text'))

    def align_to_center(self) -> str:
        width, height = (280, 340)
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 3
        return f"{width}x{height}+{x}+{y}"
    
    def load_image(self, filename: str) -> PhotoImage:
        image = PhotoImage(file=utils.get_image_path(filename))
        self.images.add(image)
        return image
    
    def run(self) -> None:
        self.root.mainloop()

    @property
    def font(self):
        if 'Pocket Calculator' in font.families():
            return ('Pocket Calculator', 27)
        return ('Default', 21)
