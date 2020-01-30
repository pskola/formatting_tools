#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#tool for preparing atlasquery txt files

import fileinput, sys, re

filename = sys.argv[1]
regex = re.compile(r'<.*>')

with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
    for line in file:
        print(re.sub(regex, '', line))