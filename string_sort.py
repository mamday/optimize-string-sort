''' Importing regular expressions package re to use re.sub() 
    https://docs.python.org/2/library/re.html'''
import re
'''Import sys to get access to command line inputs
   https://docs.python.org/2/library/sys.html
'''
import sys
'''Importing Queue.Queue() (a normal queue) and Queue.PriorityQueue(),
   which implements a sorted queue using the heapq module, from package Queue
   https://docs.python.org/2/library/queue.html
'''
from Queue import Queue,PriorityQueue
'''https://docs.python.org/3/library/string.html'''
import string
'''My class that lets me do basically any operation on a string. 
   https://github.com/mamday/production-quality-string-sort/blob/master/string_tools.py'''
from string_tools import StringCleaner

class AlphanumericSortableString(object):
  ''' AlphanumericSortableString is a class that takes an input of a list
    of words and integers separated by spaces (expecting that non-alphanumeric
    characters which are not spaces may exist inside the words and the numbers).
    It filters the words and integers and then uses a PriorityQueue to sort
    them. Finally it places sorted words and integers back in the string,
    making sure to put integers where integers were and strings where strings
    were before
    
    Attributes
    ----------
    self.num_heap - PriorityQueue for integers in the string
    self.str_heap - PriorityQueue for words in the string
    self.type_heap - Queue (unsorted) for type 'word' or 'number' of a 
    position in the string
    self.cur_string - The string that is being sorted/cleaned
    self.a_chars - The set of all upper and lower case alphanumeric characters
    self.n_chars - The set of all numbers 

    Functions
    ---------
    __init__(self,in_string) - Initializes function with self.cur_string=in_string

    __str__(self) - Prints self.cur_string for `print AlphanumericSortableString(in_string)

    is_alpha(self,it_string) - Determines if it_string is a word, a number,
    or neither. If it is a number it also outputs the position of the first
    number in the string. 

    dash_case(self,it_string) - Parses strings that contain a '-' character.
    If the string contains a number, and the '-' comes before the first number,
    the '-' is kept and then the string is cleaned of '-' characters. If the
    string contains letters then the string is just cleaned of '-' characters. 

    make_heaps(self) - Separates the cleaned and parsed words and integers
    into a two heaps,self.str_heap and self.num_heap respectively, and keeps
    track of their positions with self.type_heap

    sort(self) - Takes a string separated list of words containing words and
    integers (with some possible non alphanumeric characters embedded inside)
    and returns a string that has both words and integers sorted, but still
    in positions that were originally occupied by their same type 
  '''
  def __init__(self,in_string):
    self.num_heap = PriorityQueue()
    self.str_heap = PriorityQueue()
    self.type_heap = Queue()
    self.cur_string = StringCleaner(ss=in_string) 
    self.a_chars = set(string.lowercase+string.uppercase) 
    self.n_chars = set(map(str,[0,1,2,3,4,5,6,7,8,9]))

  def __str__(self):
    return self.cur_string

  def is_alpha(self,it_string):
    min_pos = 9999 
    for ind,char in enumerate(it_string):
      '''Determine if there are any numbers in it_string, then find the first
       occurence of a number.'''
      if(char in self.n_chars):
        if(ind<min_pos):        
          min_pos=ind

      '''Determine if there are any letters in it_string'''
      if(char in self.a_chars):
        return True,None

    '''Return None for both if neither letters or numbers are found'''
    if(min_pos<9999):
      return False,min_pos
    else:
      return None,None 

  def dash_case(self,it_string):
    new_it=''

    '''Determine if it_string is a word or an integer, and if it is an integer,
    find the location of the first number at n_pos'''
    it_alpha,n_pos = self.is_alpha(it_string)

    '''If it_string is a number, keep the number starting at the first numeric
    character, and filter out all non-numeric characters, then add a '-'
    character if it comes right before the first numeric character'''
    if(it_alpha!=None and not(it_alpha)):
      new_it = StringCleaner(ss=it_string[n_pos:]) 
      m_string=''

      if(it_string[n_pos-1]=='-'):
        m_string='-'
      new_it.clean(re.sub,2,'[^0-9]','') 
      new_it = m_string+str(new_it)

    '''If it_string is a word, filter out the dashes, then return the string'''
    if(it_alpha): 
      new_it = StringCleaner(ss=it_string)
      new_it.clean(re.sub,2,'[^a-zA-Z]','')
      new_it = str(new_it)

    return new_it

  def make_heaps(self):
    '''Make list of strings, separated by spaces, then iterate over them'''
    for it in str(self.cur_string).split():
      '''Determine if the current string it is a word or an integer. Ignore 
         any non-word, non-integer entries''' 
      it_alpha,n_pos = self.is_alpha(it)

      '''Deal with case where '-' is in the string''' 
      if('-' in it):
        it = self.dash_case(it) 

      '''If it is a word, put it on the word heap and add 'word to the type 
      heap''' 
      if(it_alpha):
        self.str_heap.put(it)
        self.type_heap.put('word')

      '''If it is an integer, put it on the integer heap and add 'word to the
         type heap''' 
      if(it_alpha!=None and not(it_alpha)):
        self.num_heap.put(int(it))
        self.type_heap.put('number')

  def sort(self):
    '''Use regular expressions package re to remove everything
       but numbers 0-9 and lower case and capital letters a-z,
       keeping spaces and dashes (in case of negative numbers)
        which will be cleaned in a later step''' 
    out_string = ''
    self.cur_string.clean(re.sub,2,'[^a-zA-Z0-9- ]','') 

    '''Create the type,word and integer heaps'''
    self.make_heaps()

    '''Pop off all types, then add either a word or integer to the output
       string based on the type'''
    while(not self.type_heap.empty()):
      '''Separate words and integers by a space'''
      if(len(out_string)>0):
        out_string=out_string+' '

      cur_type = self.type_heap.get()

      if(cur_type=='word'):
        out_string=out_string+self.str_heap.get()
      elif(cur_type=='number'):
        out_string=out_string+str(self.num_heap.get())

    self.cur_string = out_string

def main():
  '''Get name of input and output files from command line input. 
     Ex: python string_sort.py test.txt out.txt 
     -> in_name=test.txt, out_name=out.txt'''
  in_name = sys.argv[1]
  out_name = sys.argv[2]

  '''Get the string from the file as in_str. Then sort it with 
   AlphanumericSortableString().sort(), setting out_str equal to the result'''
  in_str = open(in_name).readlines()[0]
  out_str = AlphanumericSortableString(in_str.strip())
  out_str.sort() 

  '''Write the sorted string to the output file'''
  out_file = open(out_name,'w')
  out_file.write(str(out_str))

if __name__=="__main__":
  main()

'''Tests using the pytest package that will be automatically run by running:
   py.test string_sort.py'''
def test_sort_capitals():
  out_str = AlphanumericSortableString('a Big interior Cat')
  out_str.sort()
  out_str=str(out_str)
  assert out_str=='Big Cat a interior'

def test_num_nonalphanumeric():
  out_str = AlphanumericSortableString('-*$89%7##4')
  out_str.sort()
  out_str=str(out_str)
  assert out_str=='-8974'

def test_word_nonalphanumeric():
  out_str = AlphanumericSortableString('unl&''""imited')
  out_str.sort()
  out_str=str(out_str)
  assert out_str=='unlimited'

def test_word_dashes():
  out_str = AlphanumericSortableString('am*---erica')
  out_str.sort()
  out_str=str(out_str)
  assert out_str=='america'

def test_num_dashes():
  out_str = AlphanumericSortableString('-95-9!$')
  out_str.sort()
  out_str=str(out_str)
  assert out_str=='-959'

def test_basic_function():
  out_str = AlphanumericSortableString('-95-9!$ am*---erica 45 -9 unl&''""imited free 89%7##4 bread sticks -95-9!$')
  out_str.sort()
  out_str=str(out_str)
  assert out_str=='-959 america -959 -9 bread free 45 sticks unlimited 8974'

 
 
