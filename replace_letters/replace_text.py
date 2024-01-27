import os
from os import listdir
import re

def replace_text(text):
    replace_dict = {'A': 'А', 'B': 'В', 'E': 'Е',
                    'K': 'К', 'M': 'М', 'O': 'О',
                    'P': 'Р', 'C': 'С', 'T': 'Т',
                    'X': 'Х', 'a': 'а', 'y': 'у',
                    'e': 'е', 'o': 'о', 'x': 'х',
                    'c': 'с', 'p': 'р', 'H': 'Н'} 
    
    def replacer(match):
        word = match.group(0)
        for eng, rus in replace_dict.items():
            word = word.replace(eng, rus)
        return word
    
    pattern = re.compile(r'\b\w*[а-яё]\w*\b', re.I)
    text = pattern.sub(replacer, text)
    return text
