# Upload 177
import datetime
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
import filecmp
import os
import random
import shutil
import sys

import graphviz


class NoWitError(Exception):
    pass


def init(path):
    current_dir = os.path.join(path, '.wit')
    sub_folders = ('images', 'staging_area')
    if not os.path.exists(current_dir):
        os.mkdir(current_dir)
        for folder in sub_folders:
            os.mkdir(os.path.join(current_dir, folder))
    ref_file = os.path.join(check_wit()[1], 'references.txt')
    active_file = os.path.join(check_wit()[1], 'activated.txt')
    with open(ref_file, 'r') as file:
        master_data = file.readlines()[1][7:]
    with open(active_file, 'w') as file:
            file.write(master_data)


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
    wit_dir = None
    for _ in range(counter):
        dir_list = os.path.join(dir_list[0] + os.sep, *dir_list[1:])
        check_dir = os.path.join(dir_list, '.wit')
        if os.path.isdir(check_dir):
            wit_marker = True
            wit_dir = check_dir
        dir_list = dir_list.split(os.sep)
        dir_list.pop(-1)
    return wit_marker, wit_dir


def commit(message, from_merge=False):
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
            if not from_merge:
                with open(ref_file, 'r') as file:
                    old_data = file.readline()
                    parent_text = old_data[5:-1]
            else:
                parent_text = from_merge
        with open(f'{dst_dir}.txt', 'w') as file:
            text_for_file = f'parent={parent_text}\ndate={datetime.datetime.now().ctime()}\nmessage={message}'
            file.write(text_for_file)
        src_dir = os.path.join(check_wit()[1], 'staging_area')
        copy_tree(src_dir, dst_dir)
        active_file = os.path.join(check_wit()[1], 'activated.txt')
        with open(active_file, 'r') as file:
            active_branch = file.read()
            if active_branch == parent_text:
                with open(ref_file, 'r') as file:
                    old_data = file.readlines()
                new_line = old_data[-1][:old_data[-1].index('=') + 1] + commit_id
                to_write = [old_data[0], old_data[1], new_line]
                with open(ref_file, '2') as file:
                    file.writelines(to_write)
        with open(ref_file, 'r') as file:
            master_line = file.readlines()[1]
            three_lines = False
            if len(file.readlines()) == 3:
                three_lines = True
                last_line = file.readlines()[2]
        with open(ref_file, 'w') as file:
            if not three_lines:
                to_write = f'HEAD={commit_id}\n{master_line}'
            else:
                to_write = f'HEAD={commit_id}\n{master_line}\n{last_line}'
            file.write(to_write)
        return 'Commit created.'
    return 'Commit not created due to not ".wit" folder in any of the parent folders.'


def status():
    wit = check_wit()
    if wit[0]:
        ref_file = os.path.join(wit[1], 'references.txt')
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


def checkout(commit_id):
    wit = check_wit()
    if wit[0]:
        ref_file = os.path.join(wit[1], 'references.txt')
        with open(ref_file, 'r') as file:
            data = file.readlines()
        if (not os.path.exists(os.path.join(wit[1], 'images', commit_id)) and data[-1][:data[-1].index('=') == commit_id]):
            commit_id = data[-1][data[-1].index('=') + 1:]
        active_file = os.path.join(check_wit()[1], 'activated.txt')
        to_write = data[-1][:data[-1].index('=')]
        with open(active_file, 'w') as file:
            file.write(to_write)
        last_commit_id = data[0][5:-1]
        staging_area = os.path.join(wit[1], 'staging_area')
        current_commit = os.path.join(wit[1], 'images', last_commit_id)
        changes_to_be_commited = filecmp.dircmp(staging_area, current_commit).left_only
        changes_not_to_be_commited = filecmp.dircmp(staging_area, current_commit).diff_files
        if changes_to_be_commited == [] and changes_not_to_be_commited == []:
            if commit_id.lower() == 'master':
                commit_id = data[1][7:-1]
            if os.path.exists(os.path.join(wit[1], 'images', commit_id)):
                for cont in os.listdir(os.path.join(wit[1], 'images', commit_id)):
                    shutil.copy((os.path.join(wit[1], 'images', commit_id, cont)), (os.path.join(wit[1], cont)))
                with open(ref_file, 'w') as file:
                    to_write = f'HEAD={commit_id}\n{data[1]}'
                    file.write(to_write)
                shutil.rmtree(staging_area)
                os.mkdir(staging_area)
                for cont in os.listdir(os.path.join(wit[1], 'images', commit_id)):
                    shutil.copy((os.path.join(wit[1], 'images', commit_id, cont)), staging_area)
                return 'Checkout successful.'
            else:
                return 'Checkout not possible since commit can not be found.'
        else:
            return 'Checkout not possible due to unsaved changes.'
    return 'No ".wit" folder in any of the parent folders.'


def graph():
    wit = check_wit()
    if wit[0]:
        graph_dots = []
        ref_file = os.path.join(wit[1], 'references.txt')
        with open(ref_file, 'r') as file:
            data = file.readline()
        head = data[5:-1]
        current_commit = head
        next_dot = True
        while next_dot:
            graph_dots.append(current_commit)
            with open(os.path.join(wit[1], 'images', current_commit) + '.txt', 'r') as commit_file:
                parent_commit = commit_file.readline()[7:-1]
            if parent_commit == 'None':
                next_dot = False
            else:
                current_commit = parent_commit
        commits_graph = graphviz.Digraph(comment='Commits Graph')
        graph_edges = []
        for commit in graph_dots:
            commits_graph.node(f'{commit}', f'{commit}')
        for i in range(len(graph_dots) - 1):
            graph_edges.append(f'{graph_dots[i]}{graph_dots[i + 1]}')
        print(graph_edges)
        for edge in graph_edges:
            commits_graph.edge(edge[:40], edge[40:], constraint='false')
        commits_graph.render(os.path.join(wit[1], 'Commits Graph.gv'), view=True)
        return 'Commits graph created.'
    return 'No ".wit" folder in any of the parent folders.'


def branch(name):
    wit = check_wit()
    if wit[0]:
        ref_file = os.path.join(wit[1], 'references.txt')
        with open(ref_file, 'r') as file:
            data = file.read()
        data += '\n'
        data += f'{name}={data[5:45]}'
        with open(ref_file, 'w') as file:
            file.write(data)
        return f'{name} branch created.'
    return 'No ".wit" folder in any of the parent folders.'


def merge(branch_name):
    wit = check_wit()
    if wit[0]:
        head_dots = []
        ref_file = os.path.join(wit[1], 'references.txt')
        with open(ref_file, 'r') as file:
            data = file.readline()
        head = data[5:-1]
        current_commit = head
        next_dot = True
        while next_dot:
            head_dots.append(current_commit)
            with open(os.path.join(wit[1], 'images', current_commit) + '.txt', 'r') as commit_file:
                parent_commit = commit_file.readline()[7:-1]
            if parent_commit == 'None':
                next_dot = False
            else:
                current_commit = parent_commit
        branch_dots = []
        ref_file = os.path.join(wit[1], 'references.txt')
        with open(ref_file, 'r') as file:
            data = file.readlines()
        if branch_name == data[-1][:data[-1].index('=')]:
            branch = data[-1][data[-1].index('=') + 1:]
            current_commit = branch
            next_dot = True
            while next_dot:
                branch_dots.append(current_commit)
                with open(os.path.join(wit[1], 'images', current_commit) + '.txt', 'r') as commit_file:
                    parent_commit = commit_file.readline()[7:-1]
                if parent_commit == 'None':
                    next_dot = False
                else:
                    current_commit = parent_commit
            mutual_base = ''
            branch_dots = branch_dots[::-1]
            for branch_dot in branch_dots:
                if branch_dot in head_dots:
                    mutual_base = branch_dot
                break
            diff_files = filecmp.dircmp(os.path.join(wit[1], 'images', branch), os.path.join(wit[1], 'images', mutual_base)).diff_files
            for cont in diff_files:
                shutil.copy((os.path.join(wit[1], 'images', branch, cont)), (os.path.join(wit[1], 'staging_area')))
            with open(os.path.join(wit[1], 'images', branch) + '.txt', 'r') as file:
                    old_data = file.readline()
                    first_parent = old_data[5:-1]
            with open(os.path.join(wit[1], 'images', mutual_base) + '.txt', 'r') as file:
                    old_data = file.readline()
                    second_parent = old_data[5:-1]
            commit(f'{branch_name} was commited.', f'{first_parent}, {second_parent}')

    return 'No ".wit" folder in any of the parent folders.'


if len(sys.argv) > 1 and sys.argv[1] == 'init':
    init(os.getcwd())

if len(sys.argv) > 2 and sys.argv[1] == 'add':
    print(add(sys.argv[2]))

if len(sys.argv) > 2 and sys.argv[1] == 'commit':
    print(commit(sys.argv[2]))

if len(sys.argv) > 1 and sys.argv[1] == 'status':
    print(status())

if len(sys.argv) > 2 and sys.argv[1] == 'checkout':
    print(checkout(sys.argv[2]))

if len(sys.argv) > 1 and sys.argv[1] == 'graph':
    print(graph())

if len(sys.argv) > 2 and sys.argv[1] == 'branch':
    print(branch(sys.argv[2]))

if len(sys.argv) > 2 and sys.argv[1] == 'merge':
    print(merge(sys.argv[2]))