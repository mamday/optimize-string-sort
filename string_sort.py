''' Importing regular expressions package re to use re.sub() 
    https://docs.python.org/2/library/re.html'''
import re
'''Importing Queue.Queue() from package Queue
            https://docs.python.org/3/library/asyncio-queue.html
'''
from Queue import Queue
from string_tools import StringCleaner

class AlphanumericSortableString(object):
  def __init__(self):
    self.num_heap = Queue()
    self.str_heap = Queue()
    self.type_heap = Queue()
    self.cur_string = '' 
  def __str__(self):
    return self.cur_string
  def make_heaps(self,in_string):

  def string_sort(self,in_string):


