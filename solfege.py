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

from enum import IntEnum
from os import path
from pathlib import Path
from subprocess import run
from sys import argv


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
    generated_data = '/* lol */\n' \
                     + '#include <stdio.h>\n' \
                     + '#include <stdlib.h>\n' \
                     + '\n\n' \
                     + 'int main(int argc, char** argv) {\n' \
                     + 'unsigned char* ptr = calloc(30000, 1);\n'

    def __init__(self):
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


if len(argv) < 2:
    exit(1)

source_filename = f"{path.splitext(argv[len(argv) - 1])[0]}_solfege.c"
file = open(argv[len(argv) - 1])
solfege = Solfege()

if Path(source_filename).exists():
    Path(source_filename).unlink()

for line in file.readlines():
    __tokens__ = line.split(' ')

    for token in __tokens__:
        solfege.codegen(solfege.tokenize(token), token)

solfege.generated_data += '}'

source = open(source_filename, 'w')
source.write(solfege.generated_data)
source.close()

if Path(source_filename).exists():
    print(f'Successfully wrote to {source_filename}')

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
