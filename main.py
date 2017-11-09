"""
Just main module, run it to make everything work
"""


import pdf_convecter as pd
import sourse_search as ss
import algorythm as al
import my_db as db


def main():
    for id in ss.search_for_targetgroups():
        ss.parse_groups(id)
    pd.pdf_2_clean_txt('./input', './output')
    pd.pdf_2_clean_txt('./input2', './output2')
    
    with open('./output/outputfile1.txt', 'r') as base_file:
        base_file = list(base_file.read().split(','))
        base_dict = al.tf_idf(base_file)

    con = db.sqlite3.connect('./Texts_db.sqlite')
    cursor = con.cursor()
    for file in pd.os.listdir('./output2'):
        filename = './output2/' + file
        with open(filename, 'r') as file:
            test_dict = al.tf_idf(list(file.read().split(',')))
            matches = len(set(base_dict) & set(test_dict))
            score = matches / len(test_dict.keys())

            if score > 0.5:
                cursor.execute('UPDATE files SET status = "Bad" WHERE myfilename = ?', (filename,))
            else:
                cursor.execute('UPDATE files SET status = "Good" WHERE myfilename = ?', (filename,))

    con.commit()
    con.close()


if __name__ == '__main__':
    main()
