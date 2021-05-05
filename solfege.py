#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#

# SolfegePy - Solfege implementation in Python3.
#   an esoteric language implementation in Python3 (executable)
#
#   github.com/ferhatgec/solfegepy
#

from sys import argv


if len(argv) < 2:
    print('SolfegePy - An esoteric language implementation in Python\n'
        '----\n'
        '--bf : Brainfuck to Solfege codegen')

    exit(1)

from enum import IntEnum
from os import path
from pathlib import Path
from subprocess import run


class SolfegeTokens(IntEnum):
    Do = 0,
    DoSharp = 1,
    Di = 2,
    Re = 3,
    ReSharp = 4,
    Ri = 5,
    Mi = 6,
    MiSharp = 7,
    Fa = 8,
    FaSharp = 9,
    Fi = 10,
    Sol = 11,
    SolSharp = 12,
    Si = 13,
    SiSharp = 14,
    La = 15,
    LaSharp = 16,
    Li = 17,
    Ti = 18,
    # Do
    # Ti
    Te = 19,
    # La
    Le = 20,
    # Sol
    Se = 21,
    # Fa
    # Mi
    Me = 22,
    # Re
    Ra = 23,

    Undefined = 24


tokens = [
    'Do',
    'Do#',
    'Di',
    'Re',
    'Re#',
    'Ri',
    'Mi',
    'Mi#',
    'Fa',
    'Fa#',
    'Fi',
    'Sol',
    'Sol#',
    'Si',
    'Si#',
    'La',
    'La#',
    'Li',
    'Ti',
    'Te',
    'Le',
    'Se',
    'Me',
    'Ra',
    'Lol'
]


class Solfege:
    generated_data = ''
    def __init__(self):
        if not is_bf:
            self.generated_data += '/* lol */\n' \
                         + '#include <stdio.h>\n' \
                         + '#include <stdlib.h>\n' \
                         + '\n\n' \
                        + 'int main(int argc, char** argv) {\n' \
                        + 'unsigned char* ptr = calloc(30000, 1);\n'

        self.print_data = ''
        self.put_data = ''

        self.ti_data = ''

        self.is_statement = False
        self.is_print = False
        self.is_put = False

    @staticmethod
    def tokenize(__token) -> SolfegeTokens:
        index = 0
        for __token__ in tokens:
            if __token__ == __token:
                return SolfegeTokens(index)

            index += 1

        return SolfegeTokens.Undefined

    def codegen(self, re: SolfegeTokens, __ti: str):
        self.ti_data = __ti

        {
            SolfegeTokens.Do: self.do,
            SolfegeTokens.DoSharp: self.dosharp,
            SolfegeTokens.Di: self.di,
            SolfegeTokens.Re: self.re,
            SolfegeTokens.ReSharp: self.resharp,
            SolfegeTokens.Ri: self.ri,
            SolfegeTokens.Mi: self.mi,
            SolfegeTokens.MiSharp: self.misharp,
            SolfegeTokens.Fa: self.fa,
            SolfegeTokens.FaSharp: self.fasharp,
            SolfegeTokens.Fi: self.fi,
            SolfegeTokens.Sol: self.sol,
            SolfegeTokens.SolSharp: self.solsharp,
            SolfegeTokens.Si: self.si,
            SolfegeTokens.SiSharp: self.sisharp,
            SolfegeTokens.La: self.la,
            SolfegeTokens.LaSharp: self.lasharp,
            SolfegeTokens.Li: self.li,
            SolfegeTokens.Ti: self.ti,
            SolfegeTokens.Te: self.te,
            SolfegeTokens.Le: self.le,
            SolfegeTokens.Se: self.se,
            SolfegeTokens.Me: self.me,
            SolfegeTokens.Ra: self.ra,
            SolfegeTokens.Undefined: self.lol
        }[re]()

    def bf_to_solfege(self, re):
        {
            '>': self.bf_do,
            '<': self.bf_re,
            '+': self.bf_mi,
            '-': self.bf_fa,
            '.': self.bf_sol,
            ',': self.bf_la,

            '[': self.bf_statement,
            ']': self.bf_resharp
        }.get(re, self.bf_lol)()

    def bf_do(self):
        self.generated_data += 'Do '

    def bf_re(self):
        self.generated_data += 'Re '

    def bf_mi(self):
        self.generated_data += 'Mi '

    def bf_fa(self):
        self.generated_data += 'Fa '

    def bf_sol(self):
        self.generated_data += 'Sol '

    def bf_la(self):
        self.generated_data += 'La '

    def bf_statement(self):
        self.generated_data += 'Ra Fa# Do# Sol# Mi# '

    def bf_resharp(self):
        self.generated_data += 'Re# '

    def bf_lol(self): pass

    def do(self):
        self.generated_data += '++ptr;\n'

    def dosharp(self):
        if self.is_statement:
            self.generated_data += '*ptr '

    def di(self):
        self.generated_data += ';\n'

    def re(self):
        self.generated_data += '--ptr;\n'

    def resharp(self):
        self.generated_data += '}\n'

    def ri(self):
        self.generated_data += '*ti = 0;\n'

    def mi(self):
        self.generated_data += '++*ptr;\n'

    def misharp(self):
        self.generated_data += '{\n\n'

    def fa(self):
        self.generated_data += '--*ptr;\n'

    def fasharp(self):
        self.generated_data += '('

    def fi(self):
        self.generated_data += 'printf(\"%s\", \"'

        self.is_print = True

    def sol(self):
        self.generated_data += 'putchar(*ptr);\n'

    def solsharp(self):
        self.generated_data += ')'

    def si(self):
        self.generated_data += f'{self.print_data}\");\n'
        self.is_print = False
        self.print_data = ''

    def sisharp(self):
        self.is_put = True

    def la(self):
        self.generated_data += '*ptr = getchar();\n'

    def lasharp(self):
        self.generated_data += self.put_data

        self.put_data = ''

    def li(self):
        if self.is_statement:
            self.generated_data += '}\n'
            self.is_statement = False

            return

        self.is_statement = True
        self.generated_data += 'if'

    def ti(self):
        self.generated_data += 'break;\n'

    def te(self):
        if self.is_statement:
            self.generated_data += '='

    def le(self):
        if self.is_statement:
            self.generated_data += '>'

    def se(self):
        if self.is_statement:
            self.generated_data += '<'

    def me(self):
        if self.is_statement:
            self.generated_data += '!'

    def ra(self):
        self.is_statement = True

        self.generated_data += 'while'

    def lol(self):
        if self.is_print:
            self.print_data += self.ti_data

            self.print_data += ' '


is_bf = False

if argv[1] == '--bf':
    if len(argv) == 3:
        is_bf = True
    else:
        print('Use \'--bf\' argument with Brainfuck file!')
        exit(1)

source_filename = path.splitext(argv[len(argv) - 1])[0]

if not is_bf:
    source_filename += '_solfege.c'
else:
    source_filename += '_lol.solfege'

file = open(argv[len(argv) - 1])
solfege = Solfege()


if Path(source_filename).exists():
    Path(source_filename).unlink()

if not is_bf:
    for line in file.readlines():
        __tokens__ = line.split(' ')

        for token in __tokens__:
            solfege.codegen(solfege.tokenize(token), token)
else:
    for line in file.readlines():
        for character in line:
            if character == '\n' or character == ' ': continue

            solfege.bf_to_solfege(character)

file.close()

if not is_bf: solfege.generated_data += '}'

source = open(source_filename, 'w')
source.write(solfege.generated_data)
source.close()

if Path(source_filename).exists():
    print(f'Successfully wrote to {source_filename}')

    if not is_bf:
        data = run([
            "cc",
            source_filename,
            "-o",
            "solfege_data"
        ])

        if data.stderr:
            print(f'Error : {data.stdout}')
            exit(1)

        run(["./solfege_data"])
