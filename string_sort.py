''' Importing regular expressions package re to use re.sub() 
    https://docs.python.org/2/library/re.html'''
import re
'''Import sys to get access to command line inputs
   https://docs.python.org/2/library/sys.html
'''
import sys
'''Importing Queue.Queue() (a normal queue) and Queue.PriorityQueue(), which implements a sorted queue using the heapq module, from package Queue
  https://docs.python.org/2/library/queue.html
'''
from Queue import Queue,PriorityQueue
import string
from string_tools import StringCleaner

class AlphanumericSortableString(object):

  def __init__(self,in_string):
    self.num_heap = PriorityQueue()
    self.str_heap = PriorityQueue()
    self.type_heap = Queue()
    self.cur_string = StringCleaner(ss=in_string) 
    self.a_chars = set(string.lowercase+string.uppercase) 
    self.n_chars = set([0,1,2,3,4,5,6,7,8,9])

  def __str__(self):
    return self.cur_string

  def is_alpha(self,it_string):
    for num in self.n_chars:
      if(str(num) in it_string):
        return False,it_string.find(str(num))
    for let in self.a_chars:
      if(let in it_string):
        return True,None
    return None,None 

  def dash_case(self,it_string):
    new_it=''
    it_alpha,n_pos = self.is_alpha(it_string)
    if(it_alpha!=None and not(it_alpha)):
      new_it = StringCleaner(ss=it_string[n_pos-1:]) 
      m_string=''

      if(it_string[n_pos-2]=='-'):
        m_string='-'
      new_it.clean(re.sub,2,'[^0-9]','') 
      new_it = m_string+str(new_it)

    if(it_alpha): 
      new_it = StringCleaner(ss=it_string)
      new_it.clean(re.sub,2,'[^a-zA-Z]','')
      new_it = str(new_it)
    return new_it

  def make_heaps(self):
    for it in str(self.cur_string).split():
      it_alpha,n_pos = self.is_alpha(it)
      if('-' in it):
        it = self.dash_case(it) 
      if(it_alpha):
        self.str_heap.put(it)
        self.type_heap.put('word')
      if(it_alpha!=None and not(it_alpha)):
        self.num_heap.put(it)
        self.type_heap.put('number')

  def sort(self):
    '''Use regular expressions package re to remove everything
       but numbers 0-9 and lower case and capital letters a-z,
       keeping spaces and dashes (in case of negative numbers)
        which will be cleaned in a later step''' 
    out_string = ''
    self.cur_string.clean(re.sub,2,'[^a-zA-Z0-9- ]','') 

    self.make_heaps()

    while(not self.type_heap.empty()):

      if(len(out_string)>0):
        out_string=out_string+' '

      cur_type = self.type_heap.get()

      if(cur_type=='word'):
        out_string=out_string+self.str_heap.get()
      elif(cur_type=='number'):
        out_string=out_string+self.num_heap.get()

    return out_string

def main():
  in_name = sys.argv[1]
  out_name = sys.argv[2]

  in_str = open(in_name).readlines()[0]
  out_str = AlphanumericSortableString(in_str).sort() 

  out_file = open(out_name,'w')
  out_file.write(out_str)

if __name__=="__main__":
  main() 
