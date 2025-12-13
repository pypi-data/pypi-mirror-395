import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from deciml.deciml import *
del globals()["algbra"], globals()["galgbra"], globals()["os"], globals()["sys"]
from deciml.deciml import algbra as alg, galgbra as galg
