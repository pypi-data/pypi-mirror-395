#!/usr/bin/python3
# Copyright (C) 2022 Keyu Tian. All rights reserved.
import argparse
import glob
import os
import re
import sys
from functools import partial

from toolky.core import need_parallelize, mt_thread, CPU_COUNT

__all__ = ['main']


def find(f_name, regex, key_str):
    total_lines = 0
    try:
        # lines = byte_data.decode(chardet.detect(byte_data).get('encoding', 'utf-8')).splitlines()
        with open(f_name, 'r', encoding='utf-8') as fp:
            content = fp.read().strip()
        line_no, line_no_last, matched_line_no = 1, -1, []
        p_last = 0
        for match in regex.finditer(content):
            p_next = match.start()
            line_no += content.count('\n', p_last, p_next)
            p_last = p_next
            if line_no_last != line_no:
                line_no_last = line_no
                matched_line_no.append(line_no)
        line_no += content.count('\n', p_last)
        total_lines = line_no
        if len(matched_line_no) != 0:
            sys.stdout.write(f'`{key_str}\' found in  {f_name:36s}:  [line {str(matched_line_no).strip("[]")}]\n')
    except Exception as e:
        sys.stderr.write(f'[{f_name}: file read err ({type(e)})]\n')
    
    return total_lines


@mt_thread(16)
def mp_find(file_name, regex, key_str):
    return find(file_name, regex, key_str)


def main():
    DIR_IGNORED = {'__pycache__', '__pypackages__', '.git', '.idea'}
    TARGET_POSTFIX = {
        'c', 'cc', 'cpp', 'cxx', 'cs', 'h', 'hpp', 'f', 'for',
        'py', 'pyx', 'java', 'kt', 'm',
        'js', 'ts', 'html', 'css', 'php',
        'yaml', 'sh',
        'json', 'txt', 'md',
    }
    
    desc = 'Search for some texts. [Example:  %(prog)s  "./dir/*.py"  "torch.*fft"  "3\\*3 == 9" ]'
    parser = argparse.ArgumentParser(prog='sea', description=desc)
    parser.add_argument('position', metavar='D/F', type=str, nargs='?', help='directory name or file name to be searched (wildcard * and ** is supported; default: cwd `.`)', default='./')
    parser.add_argument('keys', metavar='K', type=str, nargs='+', help='keys to search (wildcard * is supported)')
    parser.add_argument('-mp', '--mp', action='store_true', help='with multiprocessing')
    parser.add_argument('-nr', '--nr', action='store_true', help='not recursively')
    args = parser.parse_args()
    
    gg = partial(glob.glob, recursive=not args.nr)
    ggi = partial(glob.iglob, recursive=not args.nr)
    
    if args.position == '/':
        raise AttributeError('search from the root would be too costly!')
    
    dirs_and_files, keys = gg(os.path.expanduser(args.position)), args.keys
    
    files = set()
    for df in dirs_and_files:
        if os.path.isdir(df) and df not in DIR_IGNORED:
            f = filter(os.path.isfile, ggi(os.path.join(df, '**', '*')))
            files.update(set(f))
        elif os.path.isfile(df):
            files.add(df)
    
    files = sorted(filter(lambda fname: (fname.split('.')[-1].lower() in TARGET_POSTFIX) and (os.path.getsize(fname) < 256 * 1024), files))
    key_str = ' | '.join(keys)
    
    t_keys = []
    rand = 'p17tsz9'
    for key in keys:
        key = key.replace(f'\\*', rand)
        for ch in ['\\', '.', '^', '$', '*', '+', '?', '[', ']', '|', '{', '}', '(', ')']:
            key = key.replace(ch, '\\' + ch)
        key = key
        t_keys.append(key)
    ks = [f'(.*{tk.replace("*", ".*").replace(rand, f"\\*")})' for tk in t_keys]
    regex = re.compile('|'.join(ks))
    
    mp = args.mp or need_parallelize(len(files), 100)
    if mp:
        lines = mp_find([(f, regex, key_str) for f in files])
    else:
        lines = [find(f, regex, key_str) for f in files]
    
    print(f'\n[in {args.position}] #files: {len(files)}, #lines: {sum(lines)}' + (f' (w/ mt{CPU_COUNT})' if mp else ''))


if __name__ == '__main__':
    main()
