# Upload 173
import datetime
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
import filecmp
import os
import random
import sys


class NoWitError(Exception):
    pass


def init(path):
    current_dir = os.path.join(path, '.wit')
    sub_folders = ('images', 'staging_area')
    if not os.path.exists(current_dir):
        os.mkdir(current_dir)
        for folder in sub_folders:
            os.mkdir(os.path.join(current_dir, folder))


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


def check_wit():
    src = os.getcwd()
    dir_list = src.split(os.sep)
    wit_marker = False
    counter = len(dir_list)
    for _ in range(counter):
        dir_list = os.path.join(dir_list[0] + os.sep, *dir_list[1:])
        check_dir = os.path.join(dir_list, '.wit')
        if os.path.isdir(check_dir):
            wit_marker = True
            wit_dir = check_dir
        dir_list = dir_list.split(os.sep)
        dir_list.pop(-1)
    return wit_marker, wit_dir


def commit(message):
    if check_wit()[0]:
        id_notes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        commit_id = ''
        for _ in range(40):
            commit_id += random.choice(id_notes)
        dst_dir = os.path.join(check_wit()[1], 'images', commit_id)
        os.mkdir(dst_dir)
        first_commit = False
        ref_file = os.path.join(check_wit()[1], 'references.txt')
        if not os.path.isfile(ref_file):
            first_commit = True
            with open(ref_file, 'w') as file:
                pass
        if first_commit:
            parent_text = 'None'
        else:
            with open(ref_file, 'r') as file:
                old_data = file.readline()
                parent_text = old_data[5:-1]
        with open(f'{dst_dir}.txt', 'w') as file:
            text_for_file = f'parent={parent_text}\ndate={datetime.datetime.now().ctime()}\nmessage={message}'
            file.write(text_for_file)
        src_dir = os.path.join(check_wit()[1], 'staging_area')
        copy_tree(src_dir, dst_dir)
        with open(ref_file, 'w') as file:
            to_write = f'HEAD={commit_id}\nmaster={commit_id}'
            file.write(to_write)
        return 'Commit created.'
    return 'Commit not created due to not ".wit" folder in any of the parent folders.'


def status():
    wit = check_wit()
    if wit[0]:
        ref_file = os.path.join(check_wit()[1], 'references.txt')
        with open(ref_file, 'r') as file:
            data = file.readline()
        last_commit_id = data[5:-1]
        staging_area = os.path.join(wit[1], 'staging_area')
        last_commit = os.path.join(wit[1], 'images', last_commit_id)
        changes_to_be_commited = filecmp.dircmp(staging_area, last_commit).left_only
        changes_not_to_be_commited = filecmp.dircmp(staging_area, last_commit).diff_files
        untracked_files = filecmp.dircmp(staging_area, last_commit).right_only
        return f'''Last commit:
        {last_commit_id}

        Changes to be committed:
        {changes_to_be_commited}

        Changes not staged for commit:
        {changes_not_to_be_commited}

        Untracked files:
        {untracked_files}'''
    return 'No ".wit" folder in any of the parent folders.'


if len(sys.argv) > 1 and sys.argv[1] == 'init':
    init(os.getcwd())

if len(sys.argv) > 2 and sys.argv[1] == 'add':
    print(add(sys.argv[2]))

if len(sys.argv) > 2 and sys.argv[1] == 'commit':
    print(commit(sys.argv[2]))

if len(sys.argv) > 1 and sys.argv[1] == 'status':
    print(status())