'''Class to contain functions that operate on a long string 
   (either a **space** separated string or a list of strings) 
   in order to produce substrings with certain characters removed.'''
class StringCleaner(object):
  ''' Currently only allow the possibility of one string
    but use kwargs so in the future the functionality to
    operate on multiple different strings or lists can be added.
    For now throw an error if multiple strings or lists or both
    are supplied.


    Attributes
    -----------
    cur_string - Space separated string
    string_list = List of strings if user supplies it

    Functions
    ---------
    clean(c_func=re.sub,str_pos=-1,*args) - Take a method (ex. re.sub() for regular expressions), position of the argument that will take self.string_list, and then a list of arguments (*args) for that method, then output the string modified by the method.

      Arguments
      ---------
      c_func - the function being used to clean the string
      str_pos - the argument position in the function of the string  
      *args - Other non-string arguments of c_func
  '''

  def __init__(self,**kwargs):
    self.cur_string = ''
    self.string_list = []

    ''' Initialize string depending on kwargs key (`ss` for space
      delimited string, `list` for list of strings). '''
    if(len(kwargs)==0):
      raise Exception('No input string information')
    elif(len(kwargs)==1 and 'ss' in kwargs.keys()):
      if(not(isinstance(kwargs['ss'],str))):
        raise Exception('String type `ss` must be string')
      self.cur_string = kwargs['ss'] 
    elif(len(kwargs)==1 and 'list' in kwargs.keys()):
      if(not(isinstance(kwargs['list'],list))):
        self.string_list = kwargs['list'] 
        self.cur_string = ' '.join(self.string_list)
    else:
      raise Exception('Cannot clean multiple strings')

  '''Use function c_func to clean self.cur_string at str_pos within
      list of arguments args'''
  def clean(self,c_func,str_pos,*args):
    '''Check that input str_pos can be inserted into args'''
    if(str_pos>len(args)):
      raise Exception('Cannot insert string at position %s given list of arguments' % str_pos)
    '''Insert self.cur_string into *args at position str_pos'''
    if(len(args)==0):
      try:
        out_str = c_func(self.cur_string)
        '''Return formatted string'''
        return out_str
      except:
        raise Exception('Function failed with current arguments `%s` with given function' % (args,))
    else:
      a_list = list(args)
      a_list.insert(str_pos,self.cur_string)
      args = tuple(a_list)

      try:
        '''Format string'''
        out_str = c_func(*args)    

        '''Return formatted string'''
        return out_str
      except:
        raise Exception('Function failed with current arguments `%s` with given function' % (args,)) 

