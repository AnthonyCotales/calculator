#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from tkinter import messagebox
from calculator import utils
from calculator.app import CalculatorApp


def main():
    complete_files = utils.check_application_files()
    if complete_files:
        install_font = utils.install_calculator_font()
        if not install_font:
            message = 'Please install the PocketCalculator.ttf font'
            messagebox.showinfo('Information', message)
            
        app = CalculatorApp()
        app.run()
    else:
        error_message = 'Please re-install the application'
        messagebox.showwarning('Missing Files', error_message)
        sys.exit()



if __name__ == '__main__':
    main()