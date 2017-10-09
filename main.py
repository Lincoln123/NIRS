import pdf_convecter as pd
import sourse_search as ss
import algorythm as al



for id in ss.search_for_targetgroups():
    ss.parse_groups(id)

pd.pdf_2_clean_txt('./input2', './output2') # directories for processed files

for file in pd.os.listdir('./output2'):
    # better use "with open?"
    text = open('./output2/' + file, 'r')
    al.tf_idf(text)
    text.close()