import sys
from . import UAMT
def run():
 try:
  if hasattr(UAMT, 'main'): UAMT.main()
 except: pass