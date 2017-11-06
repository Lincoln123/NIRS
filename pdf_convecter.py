import textract
import pymorphy2
import re
import os
import sqlite3

def pdf_2_clean_txt(in_directory, out_directory):

    '''
    this func converts text from pdf to txt file with normalizing words
    :param indirectory: директория в которой лежат исходные данные (либо откуда брать проверяемые)
    :param outdirectory: директория для размещения переработанных файлов (исходный/загруженные)
    :return:
    '''

    con = sqlite3.connect('./Texts_db.sqlite')
    cursor = con.cursor()
    morph = pymorphy2.MorphAnalyzer()
    i = 1

    for file in os.listdir(in_directory):

        in_text = textract.process(in_directory+"/"+file)
        in_text = in_text.decode('utf-8').split()

        with open(out_directory + '/' + 'outputfile'+str(i)+'.txt', 'w') as f_out:
            t = ((out_directory + '/' + 'outputfile' + str(i) + '.txt'), file)
            cursor.execute('SELECT checksum FROM files WHERE filename = ?', (t[1],))
            check_sum = cursor.fetchall()
            if check_sum:
            #print(check_sum)
            #print(type(check_sum))
                cursor.execute('UPDATE files SET newfilename = ?  WHERE checksum = ?', (t[0], check_sum[0][0]))
            for word in in_text:
                word = re.sub("[\W\d\_]", '', word)
                if word != '':
                    f_out.write(morph.parse(word)[0].normal_form+', ')
        i += 1
    con.commit()
    con.close()
    return




if __name__ == '__main__':
    pdf_2_clean_txt('./input', './output')



'''
morph = pymorphy2.MorphAnalyzer()

in_text = textract.process("testpdf.pdf")

in_text = in_text.decode('utf-8').split()
out_text = list()
for word in in_text:
    word = re.sub("[\W]", '', word)
    if word != '':
        out_text.append(morph.parse(word)[0].normal_form)

    #print(word)
    #print((f))
#out_text = [_ for _ in out_text if _ !='']
print(out_text)
'''




