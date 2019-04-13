#!/usr/bin/env python3

import io
import os
import sys
import argparse
import shutil

inc_chars = ['{', '(']
dec_chars = ['}', ')']

def format_file(fpi, fpo, indent_str):
    line_num = 0
    indent_level = 0
    for line in fpi:
        stripped_line = str.lstrip(line)
        if stripped_line[0] in dec_chars and indent_level > 0:
            indent_level -= 1

        # if the line line begins with a dot it needs to be unformatted
        if stripped_line[0] != '.':
            fpo.write((indent_level*indent_str) + stripped_line)
        else:
            fpo.write(stripped_line)
        
        if line[-2] in inc_chars:
            indent_level += 1
        line_num += 1
    return line_num

def main():
    parser = argparse.ArgumentParser(description='Format .glyphs files')
    parser.add_argument('inputfile', type=str, 
        help='the input file to process')
    parser.add_argument('-o', dest='outputfile', metavar='FILE | -',
        help='where to write the output, use - for STDOUT')
    indentation_type = parser.add_mutually_exclusive_group()
    indentation_type.add_argument('-s', dest='indent', metavar='SPACES', type=int, default=2,
        help='use SPACES number of spaces for indentation')
    indentation_type.add_argument('-t', dest='indent', action='store_const', const=-1,
        help='use tabs for indentation')
    args = parser.parse_args()

    inputfile = args.inputfile
    print('Formatting "', inputfile, '"', file=sys.stderr, end='', sep='')
    
    if args.outputfile == '-':
        outputfile = sys.stdout
        print('to STDOUT', file=sys.stderr, end='', sep='')
    elif args.outputfile == None:
        outputfile = inputfile + '.tmp'
    else:
        outputfile = args.outputfile
        print('to "', outputfile, '"', file=sys.stderr, end='', sep='')
    print('... ', file=sys.stderr, end='', sep='')

    if args.indent == -1:
        indent_str = '\t'
    else:
        indent_str = ' '*args.indent

    with open(inputfile, 'r', 1, 'UTF-8') as fpi:
        with open(outputfile, 'w', 1, 'UTF-8') as fpo:
            line_num = format_file(fpi, fpo, indent_str)
            print(str(line_num), 'lines processed.', file=sys.stderr)
    if args.outputfile == None:
        os.remove(inputfile)
        shutil.move(outputfile, inputfile)



if __name__ == "__main__":
    main()