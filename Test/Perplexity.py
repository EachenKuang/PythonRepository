# -*- encoding: utf-8 -*-

"""
Author: Eachen Kuang
Date:  2017.7.11
Goal: Perplexity
Other:
"""

import logging
from gensim import models
from gensim import corpora
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 增加了一些东西，你看看有什么