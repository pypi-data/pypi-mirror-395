"""
Helper functions for testing the development of new features, especially for subprocesses, 
dispatching or multiprocessing.
"""
import os
import sys
import json
import time
import numpy as np


# INTERNAL PARAMETERS & DEFAULTS
_SIZE = 5000
_EXPONENT = 3


def _diag_count(N, p):
    """ Basic "diagonal" counter routine for all "test_XXX()" functions. """ 
    res = 0
    for n in range(int(N)):
         res += sum(k**p for k in range(n))
    return res


def _set_flag(flag_file, message):
    """ Basic routine to set a 'flag_file' w/ defined 'message'. """    
    with open(flag_file, 'wt') as ff:
        ff.write(f"[finished @ {time.strftime('%Y-%m-%d %H:%M:%S')}]\n\n")
        ff.write(f"{message}\n")
    return


#------------------------------------------------------------------------------


def test_func():
    """ Simple test function w/o arguments. """
    res = _diag_count(_SIZE, _EXPONENT)
    print(f"'test_func':")
    print(f" + diag-count for 1 to {_SIZE} w/ power {_EXPONENT} --> {res}")
    return res


def test_func_1arg(N):
    """ Simple test function w/ single argument. """
    res = _diag_count(N, _EXPONENT)
    print(f"'test_func_1arg':")
    print(f" + diag-count for 1 to {N} w/ power {_EXPONENT} --> {res}")
    return res


def test_func_2args(N, p):
    """ Simple test function w/ two (scalar) arguments. """
    res = _diag_count(N, p)
    print(f"'test_func_2args':")
    print(f" + diag-count for 1 to {N} w/ power {p} --> {res}")
    return res


def test_func_arrays(x1, x2, N=None, P=2):
    """ Simple test function w/ arrays and two (named) parameters for element-wise mult. """
    y = np.zeros_like(x2)
    if (N is None):
        N = len(x2)
    for n in range(N):
        y[n] = (x1[n] * x2[n]) ** P   
    return y, (x1[:N], x2[:N])


def test_func_args_kwargs(*args, **kwargs):
    """ Simple test function w/ *args and **kwargs handling. 
    
    args    = "N, p" or only "N" (then, 'p'=2 per default)
    kwargs  = "{'msg': some_String}" (any other keys are neglected)    
    """
   
    # decode args / kwargs
    N = args[0]
    if (len(args) > 1):
        p = args[1]
    else:
        p = _EXPONENT    
    if ('msg' in kwargs.keys()):
        final_msg = kwargs['msg']
    else:
        final_msg = 'Äpfel'
        
    # usual computation
    res = _diag_count(N, p)
    print(f"'test_func_args_kwargs':")
    print(f" + diag-count for 1 to {N} w/ power {p} = {res}")
    print(f" + and finally I say: {final_msg}! ;)")
    
    return res


def test_func_and_out_file(N=_SIZE, p=_EXPONENT, flag_base='z_result', cnt=None):
    """  ... """
    
    # usual computation
    res =  test_func_args_kwargs(N, p, msg='Done & set a flag!')      
    
    # configure & write flag
    if (cnt is None):
        flag_file = os.path.join(os.getcwd(), flag_base+'.flag') 
    else:
        flag_file = os.path.join(os.getcwd(), flag_base+f'_{cnt}.flag')    
    _set_flag(flag_file, res)

    return res


def test_talker(N=30, pause=0.3):
    """ Verbose function, talking 'N' times every 'pause' sec (e.g. for capturing 'stdout'). """
    res = 0
    for n in range(N):
        print(f"'test_talker': speaking for the {n}th time! ({res:.2f} sec elapsed)")
        time.sleep(pause)
        res += pause
    return res


# TODO: add a function to "testing" module, that relies on (one or more) instantiated objects
#       --> how to pass these to separate workers in the calls?
#       --> do we need to use de/serialisation (i.e. pickle)?
#


#===============================================================================================
#===============================================================================================
#===============================================================================================

#%% MAIN (= test script)
if (__name__ == "__main__"): 
    """ Test script call w/ *args & **kwargs provided in JSON-file as 'sys.argv[1]'.
    
    Example:
        Step 1: Startup Python CLI  >>> 'python'
        Step 2: Set environment     >>> 'from testing import *'
        Step 3: Call script         >>> 'testing args.json'
         
        This call the main function of "testing" where the arguments are actually put in "args.json":
            args.json = { 'args': [1000,3], 'kwargs': {'ID': 4, 'flag': 'Python_test.flag'} }
    """
          
    print(f"Test script (__name__ == '__main__') from module 'testing' entered...")
    
    # read arguments from file
    if (len(sys.argv) > 1):
        the_file = sys.argv[1]
        the_folder = os.path.dirname(the_file)
        with open(the_file) as jf:
            all_inputs = json.load(jf)
    else:
        all_inputs = {
            'args': [_SIZE, _EXPONENT],
            'kwargs': {'msg': 'Done & set a flag!', 'ID': 0} } 
      
    res = test_func_and_out_file(*all_inputs['args'], 
                                 flag_base='z_result', cnt=all_inputs['kwargs']['ID'])
       
    # # log output fo tile
    # file_log = os.path.join(the_folder, 'logfile_'+time.strftime("_%H_%M_%S")+'.txt')   
    # with open(file_log, 'wt') as tf:       
    #     tf.write(f"My result? --> {res}\n")
    #     tf.write("\n")
    #     tf.write("My input parameters?\n")
    #     tf.write(f"--> args:    {arguments['args']}  --> ok?\n")
    #     tf.write(f"--> kwargs:  {arguments['kwargs']}  --> ok?\n")          
               
          
# 
# python -c "import startup; from zutils.testing import *; test_func_and_flag();"
#
