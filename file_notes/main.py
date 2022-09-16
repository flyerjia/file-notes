# -*- encoding: utf-8 -*-
"""
@File    :   main.py
@Time    :   2022/09/15 16:15:59
@Author  :   jiangjiajia
"""

import sys

from file_notes.file_notes import (
    show_list,
    show_list_all,
    add_note,
    update_note,
    delete_note
)


def main(args=None):
    if not args:
        args = sys.argv[1:]
    if len(args) == 0:
        return show_list()
    if args[0] == '-l':
        return show_list()
    elif args[0] == '-al':
        return show_list_all()
    elif args[0] == '-a':
        if len(args) != 3:
            print('add note: fn -a file_or_dir new_note')
            return -1
        else:
            return add_note(args[1], args[2])
    elif args[0] == '-u':
        if len(args) != 3:
            print('update note: fn -u file_or_dir new_note')
            return -1
        else:
            return update_note(args[1], args[2])
    elif args[0] == '-d':
        if len(args) != 2:
            print('delete note: fn -d file_or_dir')
            return -1
        else:
            return delete_note(args[1])
    else:
        print('command: fn [-l|-al|-a|-u|-d] [file_or_dir] [note]')
        return -1
