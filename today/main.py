#!/usr/bin/env python
# encoding: utf-8
# main.py created by Jesse
# 16/9/12 16:24

import sys, config
from workflow import Workflow

if __name__ == u'__main__':
    wf = Workflow()
    sys.exit(wf.run(config.main))

