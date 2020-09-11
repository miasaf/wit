# Upload 171
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
import os
import sys


class NoWitError(Exception):
    pass


def add(path):
    src = os.getcwd() + '\\' + path
    dir_list = src.split('\\')
    counter = len(dir_list)
    search_folder = '\\'.join(dir_list)
    sub_path = []
    file_marker = False
    for _ in range(counter):
        if os.path.exists(search_folder + '\\.wit'):
            dst = search_folder + '\\.wit\\staging_area'
            if os.path.isfile(src):
                filename = sub_path.pop(-1)
                file_marker = True
            for folder in sub_path:
                dst = dst + '\\' + folder
                os.mkdir(dst)
            if file_marker:
                copy_file(src, dst + '\\' + filename)
            else:
                copy_tree(src, dst)
            return 'Done'
        else:
            sub_path.insert(0, dir_list.pop(-1))
            search_folder = '\\'.join(dir_list)
    return NoWitError('There\'s no ".wit" folder in none of the parent folders')


if len(sys.argv) > 2 and sys.argv[1] == 'add':
    print(add(sys.argv[2]))