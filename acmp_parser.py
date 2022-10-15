#######################################################################
##                      github.com/Woxerss                           ##
##               ACMP Task Parser by Aptem Maleev                    ##
##   Парсит задачу с ACMP и делает из нее Assignment для onlinegdb   ##
#######################################################################

id = 1                              # ID задачи на ACMP

language = 'python'                 # Язык программирования

eval_method = 'auto_grade'          # Метод проверки 'auto'/'auto_grade'
testcase_visible = 1                # Тесткейсы видны сдающим 0/1

enable_grade = 1                    # Выставление оценок 0/1
enable_late_submission = 1          # Поздняя сдача

editor_copy_paste = 1               # Копирование в окне ввода кода

url = f'https://acmp.ru/index.asp?main=task&id_task={id}'

#######################################################################
#######################################################################

import os
import bs4
import json
import requests

from bs4 import BeautifulSoup

superscript_map = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
    "7": "⁷", "8": "⁸", "9": "⁹", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
    "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
    "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
    "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
    "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
    "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
    "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
    "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
    "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾"}

subscript_map = {
    "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆",
    "7": "₇", "8": "₈", "9": "₉", "a": "ₐ", "b": "♭", "c": "꜀", "d": "ᑯ",
    "e": "ₑ", "f": "բ", "g": "₉", "h": "ₕ", "i": "ᵢ", "j": "ⱼ", "k": "ₖ",
    "l": "ₗ", "m": "ₘ", "n": "ₙ", "o": "ₒ", "p": "ₚ", "q": "૧", "r": "ᵣ",
    "s": "ₛ", "t": "ₜ", "u": "ᵤ", "v": "ᵥ", "w": "w", "x": "ₓ", "y": "ᵧ",
    "z": "₂", "A": "ₐ", "B": "₈", "C": "C", "D": "D", "E": "ₑ", "F": "բ",
    "G": "G", "H": "ₕ", "I": "ᵢ", "J": "ⱼ", "K": "ₖ", "L": "ₗ", "M": "ₘ",
    "N": "ₙ", "O": "ₒ", "P": "ₚ", "Q": "Q", "R": "ᵣ", "S": "ₛ", "T": "ₜ",
    "U": "ᵤ", "V": "ᵥ", "W": "w", "X": "ₓ", "Y": "ᵧ", "Z": "Z", "+": "₊",
    "-": "₋", "=": "₌", "(": "₍", ")": "₎"}

def del_edge_line_feeds(data: str) -> str:
    while(data.startswith('\n') or data.startswith('\r')):
        data = data[1:]
    while(data.endswith('\n') or data.endswith('\r')):
        data = data[:-1]
    return data

def convert_tag_to_text(tag: bs4.element.Tag) -> str:
    data = ""
    for content in tag.contents:
        if (type(content) == bs4.element.NavigableString):
            data += content
        if (type(content) == bs4.element.Tag):
            if (content.name == 'sup'):
                data += superscript_map[content.text]
            elif (content.name == 'sub'):
                data += subscript_map[content.text]
            elif 1:
                raise ValueError(f'Неизвестный тэг внутри текста! Задача: {id}  Тэг: {content.name}')
    return data


#########################################
##            Data Parser              ##
#########################################
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36", "content-type": "text"}

response = requests.get(url, timeout=30, headers=headers)

response.encoding = 'windows-1251'
soup = BeautifulSoup(response.text, 'lxml')

data = soup.find_all('p', attrs={'class':'text'})

# Title
title = soup.find('title').text.split('. ')[1]

# Task
task = convert_tag_to_text(data[0])
task = del_edge_line_feeds(task)

# Input data
input_data = convert_tag_to_text(data[1])
input_data = del_edge_line_feeds(input_data)

# Output data
output_data = convert_tag_to_text(data[2])
output_data = del_edge_line_feeds(output_data)

# Example tables
table = soup.find('table', attrs={'class':'main'})
rows = table.find_all('tr')
data = []
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])


#########################################
##       HTML description Builder      ##
#########################################
line_feed = '<p><br></p>'
text_start = '<p>'
text_end = '</p>'
text_bold_start = '<p><b>'
text_bold_end = '</b></p>'

table_start = '<table class=\"table table-bordered\"><tbody>'
table_end = '</tbody>\n</table>'

table_row_start = '<tr>'
table_row_end = '</tr>'

table_chunk_start = '<td>'
table_chunk_end = '</td>'

table_chunk_stroke_start = '<p>'
table_chunk_stroke_end = '</p>'

content = ''
# Task
content += text_bold_start + 'Условие задачи' + text_bold_end
content += text_start + task + text_end
content += line_feed

# Input data
content += text_bold_start + 'Входные данные' + text_bold_end
content += text_start + input_data + text_end
content += line_feed

# Output data
content += text_bold_start + 'Выходные данные' + text_bold_end
content += text_start + output_data + text_end
content += line_feed

# Examples
content += text_bold_start + 'Примеры' + text_bold_end
content += table_start

# Example table
data[0] = ['0', '<b>INPUT</b>', '<b>OUTPUT</b>']

for row in data:
    content += table_row_start
    
    # First column
    content += table_chunk_start
    strokes = row[1].split('\n')
    for r in strokes:
        content += table_chunk_stroke_start
        content += r
        content += table_chunk_stroke_end
    content += table_chunk_end
    
    # Second column
    content += table_chunk_start
    strokes = row[2].split('\n')
    for r in strokes:
        content += table_chunk_stroke_start
        content += r
        content += table_chunk_stroke_end
    content += table_chunk_end

    content += table_row_end

content += table_end


#########################################
##       JSON Assignment Builder       ##
#########################################
assignment_dict = {}
assignment_dict['version']: 1
assignment_dict['assignment'] = {}
assignment_dict['assignment']['title'] = title
assignment_dict['assignment']['content'] = content
assignment_dict['assignment']['language'] = language
assignment_dict['assignment']['code_template'] = ''
assignment_dict['assignment']['modal_solution'] = ''
assignment_dict['assignment']['eval_method'] = eval_method
assignment_dict['assignment']['enable_grade'] = enable_grade
assignment_dict['assignment']['enable_late_submission'] = enable_late_submission
assignment_dict['assignment']['editor_copy_paste'] = editor_copy_paste
assignment_dict['assignment']['testcase_visible'] = testcase_visible
assignment_dict['assignment']['code_template_readonly_ranges'] = "[]"
assignment_dict['assignment']['testcases'] = []
i = 0
for row in data[1:]:
    assignment_dict['assignment']['testcases'].append({
        "input": row[1],
        "output": row[2],
        "name": f"ex_{i}",
        "match_type": "F",
        "grade_point": 1
    })

path = os.getcwd()

with open(f"{path}/acmp_{id}.json", "w", encoding="utf-8") as file:
    json_str = json.dumps(assignment_dict, ensure_ascii=False)
    json_str = json_str[:1] + '"version": 1, ' + json_str[1:]
    file.write(json_str)
          

# print(f'Title: {title}')
# print(f'Task: {task}')
# print(f'Input data: {input_data}')
# print(f'Output data: {output_data}')

