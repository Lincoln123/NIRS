"""
This module transforms pdf files into txt files with normalyzing words
textract module transforms pdf into txt
pymorphy2 is needed to normalyze words
sqlite3 for deal with database
"""


import textract
import pymorphy2
import re
import os
import sqlite3


def pdf_2_clean_txt(input_directory, output_directory):

    con = sqlite3.connect('./Texts_db.sqlite')
    cursor = con.cursor()
    morph = pymorphy2.MorphAnalyzer()
    i = 1
    for file in os.listdir(input_directory):
        input_text = textract.process(input_directory+"/"+file)
        input_text = input_text.decode('utf-8').split()

        with open(output_directory + '/' + 'outputfile'+str(i)+'.txt', 'w') as output_file:
            output_path = (output_directory + '/' + 'outputfile' + str(i) + '.txt')
            cursor.execute('SELECT checksum FROM files WHERE filename = ?', (file,))
            checksum = cursor.fetchall()
            if checksum:
                cursor.execute('UPDATE files SET myfilename = ?  WHERE checksum = ?', (output_path, checksum[0][0]))
            for word in input_text:
                word = re.sub("[\W\d\_]", '', word)
                if word != '':
                    output_file.write(morph.parse(word)[0].normal_form + ',')
        i += 1
    con.commit()
    con.close()
    return



