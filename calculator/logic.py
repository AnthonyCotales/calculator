#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Logic:
    def __init__(self):
        self._inputs = []
        self._memory = None
        self._new_input = False
        self._error = 'error'
        self._digits = 13

    def evaluate_expression(self, expression: str) -> str:
        try:
            result = eval(expression)

            if len(str(result)) > self._digits:
                if '.' in str(result):
                    decimal = str(result).index('.') + 1
                    ndigits = self._digits - decimal
                    result = round(result, ndigits)
                else:
                    raise

            if str(result).endswith('.0'):
                result = int(result)
                
            return str(result)
        
        except Exception:
            return self._error
        
    def square_root(self, number: str) -> str:
        if number.startswith('-'):
            number = number[1:]
        return self.evaluate_expression(f'{number} ** 0.5')
    
    def get_percentage(self, whole, percent) -> str:
        return self.evaluate_expression(f'({percent} / 100) * {whole}')
    
    def reset_inputs(self) -> None:
        self._inputs.clear()
        self._new_input = False

    @property
    def reverse_map(self) -> dict:
        return {value: key for key, value in self.mapping.items()}
        
    @property
    def mapping(self) -> dict:
        buttons = [
            'c', 'ce', 'mrc', 'm-', 'm+',
            '7', '8', '9', '%', 'sqrt',
            '4', '5', '6', '*', '/',
            '1', '2', '3', '+', '-',
            '0', '.', '+/-', '='
        ]
        mapping = {}
        for i, button in enumerate(buttons, start=1):
            mapping[f'button_{i}'] = button
        return mapping

