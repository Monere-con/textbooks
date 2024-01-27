import os
from os import listdir
import re
from bs4 import BeautifulSoup

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

for file in listdir():
    if os.path.splitext(file)[1] == '.fb2':
        with open(file, encoding='utf-8') as book:
            text = book.read()
            soup = BeautifulSoup(text, 'xml')
            p_text = soup.find_all('p')
            for line in p_text:
                line.string = replace_text(line.text)
            file_name = os.path.splitext(file)[0]
            with open(file_name + '_replaced.fb2', 'w', encoding='utf-8') as new_book:
                new_book.write(str(soup))
