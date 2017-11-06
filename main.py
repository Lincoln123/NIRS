import pdf_convecter as pd
import sourse_search as ss
import algorythm as al
import my_db as db



for id in ss.search_for_targetgroups():
    ss.parse_groups(id)

pd.pdf_2_clean_txt('./input', './output') #directories for base files
pd.pdf_2_clean_txt('./input2', './output2') # directories for processed files

for file in pd.os.listdir('./output2'):
    # better use "with open?"
    text = open('./output2/' + file, 'r')
    al.tf_idf(text)
    text.close()
with open('./output/outputfile1.txt', 'r') as base_file:
    base_file = list(base_file.read().split(','))
    X_base = al.tf_idf(base_file)
    con = db.sqlite3.connect('./Texts_db.sqlite')
    cursor = con.cursor()
    for file in pd.os.listdir('./output2'):
        filename = './output2/' + file
        with open(filename, 'r') as file:
            X_test = al.tf_idf(list(file.read().split(',')))
            matches = len(set(X_base) & set(X_test))
            score = matches / len(X_test.keys())
            print(score)
            if score > 0.5:
                cursor.execute('UPDATE files SET status = "Bad" WHERE newfilename = ?', (filename,))
            else:
                cursor.execute('UPDATE files SET status = "Good" WHERE newfilename = ?', (filename,))
        #вынос вердикта
        #и занесение в бд
con.commit()
con.close()

