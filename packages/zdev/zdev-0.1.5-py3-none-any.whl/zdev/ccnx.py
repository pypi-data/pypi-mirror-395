"""
Routines for a simplified access to C-type libraries (DLLs) in Python (a.k.a. "C-core nexus" ;)

This module provides functions to map Python calls to the underlying C functions w/ optional 
type conversion & shape hinting.
"""
import os
import numpy as np
import ctypes as ct

from zdev.core import fileparts
from zdev.libdsp import c_complex #, c_polar, c_array


# INTERNAL PARAMETERS & DEFAULTS
_DTYPE_INT      = {                    8: np.int64,   4: np.int32,   2: np.int16,  1: np.int8 }
_DTYPE_FLOAT    = {                    8: np.float64, 4: np.float32, 2: np.float16 }
_DTYPE_COMPLEX  = { 16: np.complex128, 8: np.complex64 } 


def open_lib(libname, verbose=False):
    """ Loads C-type dynamic link library (DLL) 'libname'.
    
    Args:
        libname (str): Filename of C-type dynamic link library (DLL).
        verbose (bool, optional): Switch for status messages. Defaults to 'True'.
        
    Returns:
        libobj (:obj:): Handle to openend DLL or 'None' if not successful.
    """   
    fpath, fname, fext = fileparts(libname)   
    if (fext == 'dll'):
        libobj = ct.cdll.LoadLibrary(os.path.join(fpath, fname+'.dll'))
        if (verbose and (libobj is not None)):
            print(f"Loaded C-type library <{libobj._name}>")
        return libobj
    elif (fext == 'lib'):
        pass # TODO: seems to make no sense, or can static libs be bound to runtime Python?
    else:
        if (verbose):
            print("Given filename <{libname}> is no valid library!")
        return None     
    
   
def close_lib(libobj, verbose=False):
    """ Closes openend DLL represented by handle 'libobj'.  
    
    Args:
        libobj (:obj:): Handle to C-type DLL in use.
        verbose (bool, optional): Switch for status messages. Defaults to 'True'.
        
    Returns:
        --
    """      
    libname = libobj._name
    dh = ct.c_void_p(libobj._handle)   
    ct.windll.kernel32.FreeLibrary(dh)
    del libobj
    if (verbose):
        print(f"Closed C-type library <{libname}>")
    return


def test_lib(libobj):
    """ Calls self-tests on library (if supported). """    
    test_name = map_func_safe(libobj, 'DllName', ct.c_int, [ct.POINTER(ct.c_char)])
    test_version = map_func_safe(libobj, 'DllVersion', ct.c_double, [ct.c_int])
    lib_name = ct.create_string_buffer(32) 
    try:
        test_name(lib_name)
        lib_ver = test_version(0)
        print(lib_name[:-1])
        print(lib_ver)
    except:
        print("No tests possible")
    return      
 

def map_func(libobj, funcname, restype, argtypes):
    """ Maps function 'funcname' from DLL 'libobj' according to given call signature.
    
    Args:
        libobj (:obj:): Handle to C-type DLL in use.
        funcname (str): Name of function to be mapped to Python object name.
        restype (:obj:): C-dtype of returned function output.
        argtypes (list of :obj:): List of C-dtypes of all required function input arguments.
           
    Returns: 
        func (:obj:): Handle to DLL function.    
    """
    try:
        func = libobj.__getattr__(funcname)
    except AttributeError:
        print(f"Function '{funcname}' could not be mapped!")
        return None
    else:
        func.restype = restype
        func.argtypes = argtypes
    return func


def map_func_safe(libobj, funcname, restype, argtypes, resprot=None, argprot=[]):
    """ Maps function 'funcname' from DLL 'libobj' in a "safe" way (incl. shape information).

    This variant can be used to enforce "protections" on the function call by imposing shape
    restrictions on the arguments. Even if such requirements are not known (beforehand), THIS
    FUNCTION SHOULD BE PREFERRED WHEN WORKING WITH NUMPY, AS IT CONNECTS THE C-FUNCTION I/O TO
    NATIVE NUMPY ARRAYS!
        
    Args:
        libobj (:obj:): Handle to C-type DLL in use.
        funcname (str): Name of function to be mapped to Python object name.
        restype (:obj:): C-dtype of returned function output.
        argtypes (list of :obj:): List of C-dtypes of all required function input arguments.
        resprot (int or tuple): Shape enforced on the return argument. Defaults to 0.
        argprot (list of shapes, optional): List of shapes enforced on arguments of the call.
            Defaults to empty list '[]'. Ignored for elements that are 'None' or less than 1.
            
    Returns: 
        func (:obj:): Handle to DLL function.    
    """
    func = libobj.__getattr__(funcname)
    
    # return argument
    if (resprot is not None): 
        if (restype == ct.POINTER(c_complex)):
            func.restype = np.ctypeslib.ndpointer(dtype=_DTYPE_COMPLEX[ct.sizeof(c_complex)],
                                                  shape=resprot)        
        elif (restype == ct.POINTER(ct.c_double)):
            func.restype = np.ctypeslib.ndpointer(dtype=_DTYPE_FLOAT[ct.sizeof(ct.c_double)],
                                                  shape=resprot)
        elif (restype == ct.POINTER(ct.c_int)):
            func.restype = np.ctypeslib.ndpointer(dtype=_DTYPE_INT[ct.sizeof(ct.c_int)],
                                                  shape=resprot)
        else:
            pass # should not occur?
    else:
        func.restype = restype       
            
    # input arguments
    tmp = []
    for idx, arg in enumerate(argtypes):
        
        # directly convert array connection...
        if ((argprot == []) or (argprot[idx] is None) or (argprot[idx] < 1)):            
            if (arg == ct.POINTER(c_complex)):
                tmp.append(np.ctypeslib.ndpointer(dtype=_DTYPE_COMPLEX[ct.sizeof(c_complex)]))
            elif (arg == ct.POINTER(ct.c_double)):
                tmp.append(np.ctypeslib.ndpointer(dtype=_DTYPE_FLOAT[ct.sizeof(ct.c_double)]))
            elif (arg == ct.POINTER(ct.c_int)):
                tmp.append(np.ctypeslib.ndpointer(dtype=_DTYPE_INT[ct.sizeof(ct.c_int)]))
            else:
                tmp.append(arg)        
                
        # ...or apply array protection?
        else: 
            if (arg == ct.POINTER(c_complex)):
                tmp.append(np.ctypeslib.ndpointer(dtype=_DTYPE_COMPLEX[ct.sizeof(c_complex)],
                                                  shape=argprot[idx]))
            elif (arg == ct.POINTER(ct.c_double)):
                tmp.append(np.ctypeslib.ndpointer(dtype=_DTYPE_FLOAT[ct.sizeof(ct.c_double)], 
                                                  shape=argprot[idx]))
            elif (arg == ct.POINTER(ct.c_int)):
                tmp.append(np.ctypeslib.ndpointer(dtype=_DTYPE_INT[ct.sizeof(ct.c_int)], 
                                                  shape=argprot[idx]))
            else:
                tmp.append(arg)
                
    func.argtypes = tmp    
    return func


def is_c_dtype(x):
    """ Checks if 'x' is a C-dtype, i.e. if it is matches a 'ctypes' pattern. 
    
    Args:
        x (:obj:): Input object.        
        
    Returns:
        (bool): 'True' or 'False' depending on type of 'x'.
    """ 
    chk = str( type(x) )
    if ( (chk.rfind('_ctypes') >= 0) or 
         (chk.rfind('.c_') >= 0) or 
         (chk.startswith("<class 'c_")) ):
        return True
    else:
        return False
    

def py2c(x):
    """ Converts NumPy array 'x' w/ proper target type (convenient use for C-calls).
        
    Args:
        x (np.ndarray): Input array for conversion. The 'dtype' is determined automatically.
        
    Returns:
        xc (:obj:): Array cast as C-dtype (to be used with mapped library function).
    """ 
    if (not is_c_dtype(x)):
        if (x.dtype == 'complex128'):
            return x.ctypes.data_as(ct.POINTER(c_complex))
        elif (x.dtype == 'float64'):
            return x.ctypes.data_as(ct.POINTER(ct.c_double))        
        elif (x.dtype == 'int32'):
            return x.ctypes.data_as(ct.POINTER(ct.c_int))
        else: # (x.dtype == 'float32')? --> not supported by 'libDSP'!
            return x      
    else:
        return x # wtf? ;)
    
    
# #%% c2py
# def c2py(x, shape):
#     """ Converts C-dtype array 'xc' w/ known 'shape' for use as NumPy array.
    
#     Args:
#         xc (:obj:): Input array as C-dtype for conversion.
#         shape (int or tuple): Shape parameters for proper memory access (e.g. '100' or '(100,)'
#                or N-tuple like '(8,6,3)').
            
#     Returns:
#         x (np.ndarray): NumPy array w/ proper dimensions and shape.
#     """  
#     if (is_c_dtype(x)):
#         return np.ctypeslib.as_array(x, shape)
#     else: # assume NumPy array already?
#         return x

 

#-----------------------------------------------------------------------------------------------
# BASIC STRUCTURES (see "libdsp" --> "dsp.h" for requirements)
#-----------------------------------------------------------------------------------------------
        
# #%% c_complex (struct)
# class c_complex(Structure):
#     """ Provide native 'complex' data type as for Python's builtin dtype. """    
#     _fields_ = [
#         ('re', ct.c_double),
#         ('im', ct.c_double)
#         ]
    
#     def __init__(self, a, b):
#         self.re = a
#         self.im = b        
#         return
    
#     def __repr__(self): # in assignment
#         if (self.im >= 0):
#             return f"({self.re:{_PREC_COMPLEX}} + {self.im:{_PREC_COMPLEX}}j)"
#         else:
#             return f"({self.re:{_PREC_COMPLEX}} - {np.abs(self.im):{_PREC_COMPLEX}}j)"
        
#     def __str__(self): # for 'print'
#         if (self.im >= 0):
#             return f"({self.re:{_PREC_COMPLEX}} + {self.im:{_PREC_COMPLEX}}j)"
#         else:
#             return f"({self.re:{_PREC_COMPLEX}} - {np.abs(self.im):{_PREC_COMPLEX}}j)"
        
#     # def __getitem__(self, item):         # required?
#     #     return (self.re, self.im)[item]
    
#     def __setitem__(self, item, value):
#         self.re[item] = value[0]
#         self.im[item] = value[1]
#         return





#===============================================================================================
# Notes:
# 
#   (1) For the C-DLLs, the '__cdecl' calling convention is assumed!
#   [ https://docs.microsoft.com/de-de/cpp/cpp/cdecl?view=vs-2019 ]
#
#   (2) 'import ctypes as ct' exposes:
#   + all basic C-dtypes such as 'c_char', 'c_int', 'ct.c_double', ...
#   + class 'Structure' to model C structs (requires '_fields_' as 2-tuples: (name, dtype) )
#   + DLL-handling submodules (i.e. 'cdll' & 'windll')
#   [ https://docs.python.org/3.7/library/ctypes.html ]
#   [ https://docs.python.org/3/library/ctypes.html#calling-functions ]
#   [ https://yizhang82.dev/python-interop-ctypes ]
#
#   (3) Information on CPython memory layout:
# 
#   BYTES_ARENA = 256 * 1024    # CPython "arena" = contiguous block of memory (~ system "page")
#   BYTES_POOL  =   4 * 1024    # CPython "pool" = collection of "blocks" of same "size class"
#
#   "Blocks" are based on "size classes"
#   BLOCK_NUM_CLASSES = 64    # i.e. idx = 0, ..., 63
#   BLOCK_CHUNK_SIZE  = 8     # i.e. aligned to 8-byte chunks
#
#   Hence...
#   BYTES_BLOCK_MIN = 1* BLOCK_CHUNK_SIZE    
#   BYTES_BLOCK_MAX = BLOCK_NUM_CLASSES * BLOCK_CHUNK_SIZE
#
#   [ https://realpython.com/python-memory-management ]
#
#   (4) Cython ?#
#   [ https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html ]
#
#===============================================================================================
