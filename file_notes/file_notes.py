# -*- encoding: utf-8 -*-
"""
@File    :   file_notes.py
@Time    :   2022/09/15 16:15:21
@Author  :   jiangjiajia
"""

import os
import json
import time

from file_notes.huepy import *

note_file = '.file_notes'


def read_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as fn:
        data = json.load(fn)
    return data


def write_json(file_path, json_data):
    with open(file_path, 'w', encoding='utf-8') as fn:
        fn.write(json.dumps(json_data, ensure_ascii=False, indent=2))


def formatTime(atime):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(atime))


def convert_size(size):
    if size < 1024:
        return str(round(size, 1)) + 'B'
    elif 1024 <= size < 1024 * 1024:
        return str(round(size / 1024, 1)) + 'K'
    elif 1024 * 1024 <= size < 1024 * 1024 * 1024:
        return str(round(size / (1024 * 1024), 1)) + 'M'
    elif 1024 * 1024 * 1024 <= size < 1024 * 1024 * 1024 * 1024:
        return str(round(size / (1024 * 1024 * 1024), 1)) + 'G'
    else:
        return str(round(size / (1024 * 1024 * 1024 * 1024), 1)) + 'T'


def get_file_stat(file):
    file_info = os.stat(file)
    return {
        'size': convert_size(file_info.st_size),
        'mtime': formatTime(file_info.st_mtime)
    }


def get_now_files():
    word_dir = os.getcwd()
    files = []
    for file in os.scandir(word_dir):
        files.append(file)
    return files


def get_extra_num(content):
    extra_num = 0
    for char in content:
        if u'\u0391' <= char <= u'\uffe5':
            extra_num += 1
    return extra_num


def get_content_len(content):
    return len(content) + get_extra_num(content)


def adjust_len(content, max_len=40):
    if get_content_len(content) <= max_len:
        return content
    else:
        return content[:max_len - 3 - get_extra_num(content)] + '...'


def adjust_type(content, type):
    if type == 'file':
        return content
    elif type == 'dir':
        return lblue(content)
    elif type == 'deled':
        return italic(red(content))
    else:
        return content


def print_info(file_info):
    """
    {
        'name': '',
        'size': '',
        'mtime': '',
        'note': '',
        'type': 'file/dir/deled'
    }
    """
    # import pdb;pdb.set_trace()
    name = adjust_len(file_info['name'], 40)
    size = adjust_len(file_info['size'], 6)
    mtime = adjust_len(file_info['mtime'], 20)
    note = adjust_len(file_info['note'], 60)

    name = name.ljust(40 - get_extra_num(name), ' ')
    size = size.rjust(6 - get_extra_num(size), ' ')
    mtime = mtime.rjust(20 - get_extra_num(mtime), ' ')
    note = note.ljust(60 - get_extra_num(note), ' ')

    name = adjust_type(name, file_info['type'])
    size = adjust_type(size, file_info['type'])
    mtime = adjust_type(mtime, file_info['type'])
    note = adjust_type(note, file_info['type'])

    print('{}  {}  {}  {}'.format(name, size, mtime, note))


def show_files_info(file_notes, files):
    had_show = []
    files = sorted(files, key=lambda x: x.name)
    for file in files:
        file_info = {}
        file_info['name'] = file.name
        file_info['size'] = convert_size(file.stat().st_size)
        file_info['mtime'] = formatTime(file.stat().st_mtime)
        file_info['note'] = file_notes.get(file.name, '')
        file_info['type'] = 'file' if file.is_file() else 'dir'
        had_show.append(file.name)
        print_info(file_info)
    for name, note in file_notes.items():
        if name not in had_show:
            file_info = {}
            file_info['name'] = '[Deleted]' + name
            file_info['size'] = '--'
            file_info['mtime'] = '--'
            file_info['note'] = note
            file_info['type'] = 'deled'
            print_info(file_info)


def show_list():
    files = get_now_files()
    files = [file for file in files if not file.name.startswith('.') and file.name != note_file]
    file_notes = read_json(note_file)
    show_files_info(file_notes, files)


def show_list_all():
    files = get_now_files()
    files = [file for file in files if file.name != note_file]
    file_notes = read_json(note_file)
    show_files_info(file_notes, files)


def add_note(file_or_dir, note):
    file_or_dir = file_or_dir.rstrip('/')
    files = get_now_files()
    file_notes = read_json(note_file)
    if file_or_dir not in [file.name for file in files]:
        print('[{}] not exit, please check the input.'.format(file_or_dir))
        return
    if file_or_dir in file_notes.keys():
        print('[{}] already has a note.'.format(file_or_dir))
        return
    file_notes[file_or_dir] = note
    for file in files:
        if file.name == file_or_dir:
            file_info = {}
            file_info['name'] = file.name
            file_info['size'] = convert_size(file.stat().st_size)
            file_info['mtime'] = formatTime(file.stat().st_mtime)
            file_info['note'] = file_notes.get(file.name, '')
            file_info['type'] = 'file' if file.is_file() else 'dir'
            print_info(file_info)
            break
    write_json(note_file, file_notes)


def update_note(file_or_dir, note):
    file_or_dir = file_or_dir.rstrip('/')
    files = get_now_files()
    file_notes = read_json(note_file)
    if file_or_dir not in [file.name for file in files]:
        print('[{}] not exit, please check the input.'.format(file_or_dir))
        return
    file_notes[file_or_dir] = note
    for file in files:
        if file.name == file_or_dir:
            file_info = {}
            file_info['name'] = file.name
            file_info['size'] = convert_size(file.stat().st_size)
            file_info['mtime'] = formatTime(file.stat().st_mtime)
            file_info['note'] = file_notes.get(file.name, '')
            file_info['type'] = 'file' if file.is_file() else 'dir'
            print_info(file_info)
            break
    write_json(note_file, file_notes)


def delete_note(file_or_dir):
    file_or_dir = file_or_dir.rstrip('/')
    files = get_now_files()
    file_notes = read_json(note_file)
    if file_or_dir not in [file.name for file in files] and file_or_dir not in file_notes.keys():
        print('[{}] not exit, please check the input.'.format(file_or_dir))
        return
    if file_notes.pop(file_or_dir, None):
        print('delete [{}]\'s note'.format(file_or_dir))
    else:
        print('thers is no [{}]\'s note.'.format(file_or_dir))
    write_json(note_file, file_notes)
