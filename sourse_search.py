"""
This module receives vk api's methods by vk module
Searches for groups by keyword in vk.com, we want to check the content
And finally parses our groups for all pdf documents with following downloading and registring in database
sqlite3 for deal with database
hashlib for calculating hash of the content of each file
"""


import vk
import urllib.request as ur
import sqlite3
import hashlib
import os


def get_api():
    api = vk.API(vk.Session(access_token=
                            '5516984b37b462038fd3b0d87d3693c23210e4349de700e6770741125cf0534a3c4ee26f82eec914a1df6'))
    return api


def search_for_targetgroups():
    search_request = get_api().groups.search(q='иу8')  # q = keyword in api request
    group_id = list()
    for groups in search_request[1::]:

        if groups.get('is_closed') == 0:
            group_id.append(groups.get('gid'))
            
        else:
            continue
            
    return group_id


def parse_groups(group_id):
    
    con = sqlite3.connect('./Texts_db.sqlite')
    cursor = con.cursor()

    try:
        documents = get_api().docs.get(owner_id='-' + str(group_id))
        for doc in documents[1::]:
            if doc.get('ext') == 'pdf':
                filename = str(doc.get('title'))
                ur.urlretrieve(doc.get('url'), './input2/' + filename)
                with open('./input2/' + filename, 'rb') as f:
                    checksum = hashlib.sha256(f.read()).hexdigest()
                t = (group_id, filename, checksum)
                cursor.execute('SELECT gid,filename FROM files WHERE checksum = ?', (checksum,))
                list_of_correlations = cursor.fetchall()
                if list_of_correlations:
                    os.remove('./input2/' + filename)
                    for i in list_of_correlations:
                        if i[0] != group_id or i[1] != filename:
                            cursor.execute('INSERT INTO files (gid,filename,checksum) VALUES(?,?,?)', t)
                else:
                    cursor.execute('INSERT INTO files (gid,filename,checksum) VALUES(?,?,?)', t)

    except vk.exceptions.VkAPIError:
        print('Access denied: group docs is disabled.', group_id)

    try:
        wall = get_api().wall.get(owner_id = '-' + str(group_id))
        for wall_docs in wall[1::]:
            if wall_docs.get('attachment') is not None and wall_docs.get('attachment').get('type') == 'doc' \
                                                and wall_docs.get('attachment').get('doc').get('ext') == 'pdf':
                filename = str(wall_docs.get('attachment').get('doc').get('title'))
                ur.urlretrieve(wall_docs.get('attachment').get('doc').get('url'), './input2/' + filename)
                with open('./input2/' + filename, 'rb') as f:
                    checksum = hashlib.sha256(f.read()).hexdigest()
                t = (group_id, filename, checksum)
                cursor.execute('SELECT gid,filename FROM files WHERE checksum = ?', (checksum,))
                list_of_correlations = cursor.fetchall()
                if list_of_correlations:
                    os.remove('./input2/' + filename)
                    for i in list_of_correlations:
                        if i[0] != group_id or i[1] != filename:
                            cursor.execute('INSERT INTO files (gid,filename,checksum) VALUES(?,?,?)', t)
                else:
                    cursor.execute('INSERT INTO files (gid,filename,checksum) VALUES(?,?,?)', t)

    except vk.exceptions.VkAPIError:
        print('Access denied: wall is disabled.', group_id)
    con.commit()
    con.close()
    return


