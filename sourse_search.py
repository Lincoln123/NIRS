import vk
import urllib.request as ur
import sqlite3
import hashlib
import os

def get_api():
    '''
    get timeless access token and converts vk api methods
    :return:
    '''
    api = vk.API(vk.Session(
        access_token=
        '5516984b37b462038fd3b0d87d3693c23210e4349de700e6770741125cf0534a3c4ee26f82eec914a1df6'))
    return api


def search_for_targetgroups():
    '''
    this func is looking for groups with keywords
    '''

    search_request = get_api().groups.search(q='иу8')  # q = keyword
    gr_id = list()
    for groups in search_request[1::]:

        if groups.get('is_closed') == 0:
            gr_id.append(groups.get('gid'))
        else:
            continue
    return gr_id


def parse_groups(group_id):
    '''

    use this func to download sources from targeting groups
    :param group_id:
    :return:
    '''
    con = sqlite3.connect('./Texts_db.sqlite')
    cursor = con.cursor()

    try:

        docs = get_api().docs.get(owner_id = '-' + str(group_id))

        for doc in docs[1::]:

            # save pdfs from group docs to directory
            if doc.get('ext') == 'pdf':
                fname = str(doc.get('title'))
                ur.urlretrieve(doc.get('url'), './input2/' + fname)
                with open('./input2/' + fname, 'rb') as f:
                    check_sum = hashlib.sha256(f.read()).hexdigest()
                #проверка на совпадение в таблице
                t = (group_id, fname, check_sum)
                cursor.execute('SELECT gid,filename FROM files WHERE checksum = ?', (t[2],))
                list_of_correlations = cursor.fetchall()
                if list_of_correlations:
                    os.remove('./input2/' + fname)
                    #удалить файл
                    for i in list_of_correlations:
                        if i[0] != group_id or i[1] != fname:
                            cursor.execute('INSERT INTO files (gid,filename,checksum) VALUES(?,?,?)',t)
                else:
                    cursor.execute('INSERT INTO files (gid,filename,checksum) VALUES(?,?,?)', t)
                con.commit()

    except vk.exceptions.VkAPIError:
        print('Access denied: group docs is disabled.')

    try:
        wall = get_api().wall.get(owner_id = '-' + str(group_id))  # .attachments(type = doc)
        for wall_docs in wall[1::]:
            # save pdfs from wall to directory
            if wall_docs.get('attachment') is not None and wall_docs.get('attachment').get('type') == 'doc' \
                    and wall_docs.get('attachment').get('doc').get('ext') == 'pdf':
                fname = str(wall_docs.get('attachment').get('doc').get('title'))
                ur.urlretrieve(wall_docs.get('attachment').get('doc').get('url'), './input2/' + fname)
                with open('./input2/' + fname, 'rb') as f:
                    check_sum = hashlib.sha256(f.read()).hexdigest()
                t = (group_id, fname, check_sum)
                cursor.execute('SELECT gid,filename FROM files WHERE checksum = ?', (t[2],))
                list_of_correlations = cursor.fetchall()
                if list_of_correlations:
                    os.remove('./input2/' + fname)
                    for i in list_of_correlations:
                        if i[0] != group_id or i[1] != fname:
                            cursor.execute('INSERT INTO files (gid,filename,checksum) VALUES(?,?,?)',t)
                else:
                    cursor.execute('INSERT INTO files (gid,filename,checksum) VALUES(?,?,?)',t)
                con.commit()
    except vk.exceptions.VkAPIError:
        print('Access denied: wall is disabled.')
    con.close()
    return


