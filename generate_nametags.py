#!/usr/bin/env python
import os
import sys
import csv
import fitz

font_file = "NanumSquareNeo-dEb.ttf"

def _capitalize(text, exceptions=['of', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'with', 'from', 'by', 'as', 'into', 'onto', 'than']):
    # capitalize first letter of each word, except English prepositions
    words = text.split(' ')
    for i in range(len(words)):
        if i == 0 or words[i] not in exceptions:
            words[i] = words[i][0].capitalize() + words[i][1:]
    return ' '.join(words)

def _insert_text_centered(page, text, y, size, fontname="hebo", color=None):
    if text[0].isascii() and text[0].isalpha():
        measurefont = "hebo"
        ratio = 1.1
    else:
        measurefont = "korea"
        ratio = 0.95
    text_length = fitz.get_text_length(text, fontname=measurefont, fontsize=size)*ratio
    while text_length > page.rect.width - 20:
        size -= 1
        text_length = fitz.get_text_length(text, fontname=measurefont, fontsize=size)*ratio
    page.insert_text((page.rect.width/2 - text_length/2, y), text, size, fontname=fontname, color=color)

def generate_nametags(csv_path, options):
    doc = fitz.open()
    doc_template = fitz.open(os.path.join('nametag.pdf'))
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        registrations = list(reader)
    
    for name, institute in registrations:
        doc.insert_pdf(doc_template)
        page = doc[-1]
        page.clean_contents()
        
        page.insert_font(fontfile=font_file, fontname="custom")
        
        _insert_text_centered(page, _capitalize(name, exceptions=[]), 150, 50, fontname="custom")
        _insert_text_centered(page, _capitalize(institute), 200, 25, fontname="custom")
                
    doc.save('nametags.pdf')
    doc.close()

def main():
    options = {"nobg": False}
    generate_nametags("nametags.csv", options)

if __name__ == '__main__':
    main()
