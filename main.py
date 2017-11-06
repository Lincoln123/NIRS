import pdf_convecter as pd
import sourse_search as ss
import algorythm as al
import my_db

'''

for id in ss.search_for_targetgroups():
    ss.parse_groups(id)

pd.pdf_2_clean_txt('./input', './output') #directories for base files
pd.pdf_2_clean_txt('./input2', './output2') # directories for processed files

for file in pd.os.listdir('./output2'):
    # better use "with open?"
    text = open('./output2/' + file, 'r')
    al.tf_idf(text)
    text.close()
'''
X_base = al.tf_idf('./output/file')

for file in pd.os.listdir('./output2'):
    with open(file,'r'):
        matches = 0
        X_test = al.tf_idf(file)
        for word in X_test.keys():
            if word == baseword for baseword in X_base.keys():
                matches += 1
        #вынос вердикта
        #и занесение в бд
        print(matches // len(X_test.keys) * 100,'%', file)
