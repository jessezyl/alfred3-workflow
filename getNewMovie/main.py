#!/usr/bin/env python
# encoding: utf-8
# main.py created by Jesse
# 16/8/8 18:14

import sys, config
from workflow import Workflow

if __name__ == u'__main__':
    wf = Workflow()
    sys.exit(wf.run(config.main))
    # config.main('{query}')

