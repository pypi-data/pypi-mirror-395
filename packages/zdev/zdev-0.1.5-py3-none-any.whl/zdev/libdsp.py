"""
Simple-to-use interface to C-code functions provided in the accompanying DLL.

Note that the library "libDSP.dll" is expected to be opened as a DLL object already prior to 
retrieving information on the function signatures.
"""
import os
import numpy as np
import ctypes as ct


# EXPORTED DATA
LIBDSP_FILE = os.path.join(os.path.dirname(__file__), 'libDSP.dll')

# INTERNAL PARAMETERS & DEFAULTS
_PREC_COMPLEX = '.3f'
_PREC_POLAR = _PREC_COMPLEX   


#-----------------------------------------------------------------------------------------------
# STRUCTURES
#-----------------------------------------------------------------------------------------------

class c_complex(ct.Structure):
    """ Provide native 'complex' data type as for Python's builtin dtype. """    
    _fields_ = [
        ('re', ct.c_double),
        ('im', ct.c_double)
        ]
    
    def __init__(self, a, b):
        self.re = a
        self.im = b        
        return
    
    def __repr__(self): # in assignment
        if (self.im >= 0):
            return f"({self.re:{_PREC_COMPLEX}} + {self.im:{_PREC_COMPLEX}}j)"
        else:
            return f"({self.re:{_PREC_COMPLEX}} - {np.abs(self.im):{_PREC_COMPLEX}}j)"
        
    def __str__(self): # for 'print'
        if (self.im >= 0):
            return f"({self.re:{_PREC_COMPLEX}} + {self.im:{_PREC_COMPLEX}}j)"
        else:
            return f"({self.re:{_PREC_COMPLEX}} - {np.abs(self.im):{_PREC_COMPLEX}}j)"
        
    # def __getitem__(self, item): # required?
    #     return (self.re[item], self.im[item])
    
    # def __setitem__(self, item, value): # required?
    #     self.re[item] = value[0]
    #     self.im[item] = value[1]
    #     return
    

class c_polar(ct.Structure):
    """ Provide native 'polar' data type as for Python's builtin dtype. """    
    _fields_ = [
        ('mag', ct.c_double),
        ('phs', ct.c_double)
        ]
    
    def __init__(self, a, b):
        self.mag = a
        self.phs = b
        return
    
    def __repr__(self):
        return f"{self.mag:{_PREC_POLAR}} * e^j({self.phs/np.pi:{_PREC_POLAR}}*pi)"

    def __str__(self):
        return f"{self.mag:{_PREC_POLAR}} * e^j({self.phs/np.pi:{_PREC_POLAR}}*pi)"
    
    # def __setitem__(self, item, value):
    #     self.mag[item] = value[0]
    #     self.phs[item] = value[1]
    #     return   


class c_array(ct.Structure):
    """ Provide native 'array' dtype w/ size & dimension as implemented in 'libDSP'. """   
    _fields_ = [ 
        ('D', ct.c_int), 
        ('N', ct.POINTER(ct.c_int)), 
        ('S', ct.POINTER(ct.c_int)),
        ('at', ct.POINTER(ct.c_double)) 
        ]
    
    def __init__(self, x): # x == np.ndarray type!
    
        if (type(x) == np.ndarray): # convert from NumPy type
            self.D = x.ndim
            self.N = (ct.c_int * self.D)()
            self.S = (ct.c_int * self.D)()
            N_total = 1
            for d in range(self.D):
                self.N[d] = x.shape[d]
                self.S[d] = 1
                N_total *= self.N[d]
                for l in range(d,self.D-1):
                    self.S[d] *= self.N[l]
            self.at = (ct.c_double * N_total)()
            for n in range(N_total):
                self.at[n] = x.data[n]
        
        else: # construct directly
            self.D = x[0]
            self.N = (ct.c_int * self.D)()
            self.S = (ct.c_int * self.D)()
            N_total = 1
            for d in range(self.D):
                self.N[d] = x[1][d]
                self.S[d] = 1
                N_total *= self.N[d]
                for l in range(d,self.D-1):
                    self.S[d] *= self.N[l]
            self.at = (ct.c_double * N_total)()
            for n in range(self.N[0]):
                self.at[n] = x[2][n]
                         
        return


    
#-----------------------------------------------------------------------------------------------
# LIBRARY FUNCTION MAPPING (see all "*.h" of "libDSP.dll" for details)
#-----------------------------------------------------------------------------------------------

# Q: How to auto-update / import this from 'dsp.h' ??? --> would be cool! :)
# Q: can we use somewhow "if (name in contents):" ? --> automatic creation of functions?

def call_signature(DLL, name):
    """ Retrieves proper function call signature for C-level routines.
    
    Args:
        name (str): Function name in Python. This is npt required to match the C function name! 
            
    Returns:
        func (:obj:): Function pointer w/ proper signature of arguments.
        enum (list): List of dictionaries representing C-style ENUMs (if required for setting
            different function modes / options).
    """ 
    from zdev.ccnx import map_func_safe    
    func = None
    enum = []
    
    if (name == 'DUMMY'):
        func = map_func_safe(DLL, name, ct.c_int, ct.c_double) # have only 'elif' branches ;)       
        
    #---------------------------
    # filtering.h
    #---------------------------
        
    elif (name == 'convolve'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.POINTER(ct.c_double), ct.c_int, ct.c_int] )
        
    elif (name == 'filterFIR'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.POINTER(ct.c_double), ct.c_int] )
            
    elif (name == 'TDF'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.POINTER(ct.c_double), ct.c_int] )
        
    elif (name == 'FDF'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.POINTER(ct.c_double), ct.c_int] )
   
    elif (name == 'avgN'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.c_int] ) 
        
    #---------------------------
    # nonlinear.h
    #---------------------------
        
    elif (name == 'edge'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.POINTER(ct.c_double), ct.c_int] )
        enum.append( { 'stick': 0, 'bounce': 1, 'wrap': 2 } )
        
    elif (name == 'wrap_phase'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int] )
           
    elif (name == 'origin'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.c_double, ct.c_int] )
        enum.append( { 'deadzone': 0, 'deadband': 1 } )
   
    elif (name == 'quant'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.c_int, ct.c_double, ct.c_int] )
        enum.append( { 'midrise': 0, 'midtread': 1, 'trunc': 2 } )        
             
    #---------------------------
    # power.h
    #---------------------------
        
    elif (name == 'power_1ph'):        
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(c_complex), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.c_double, ct.c_double] )
         
    elif (name == 'clarke'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(c_complex), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int] )
    
    elif (name == 'park'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(c_complex), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int,
             ct.c_double, ct.c_double, ct.c_double] )        
            
    #--------------------------------------------------------------------------
    # signal.h
    #--------------------------------------------------------------------------
                
    elif (name == 'oscillator'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.c_int, ct.c_double, ct.c_double, ct.c_double, ct.c_int] )
        enum.append( { 'sin': 0, 'rect': 1, 'saw': 2, 'tri': 3 } )
        
    elif (name == 'oscillator_mod'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.c_int, ct.c_double, ct.c_double, ct.c_double, ct.c_int, 
             ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double)] )
        enum.append( { 'sin': 0, 'rect': 1, 'saw': 2, 'tri': 3 } )
        
    #--------------------------------------------------------------------------
    # transform.h
    #--------------------------------------------------------------------------
    
    elif (name == 'FFT'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(c_complex), ct.POINTER(c_complex), ct.c_int, ct.c_int] )
        enum.append( { 'radix-none': 0, 'radix-2': 1, 'radix-4': 2 } )
    
    elif (name == 'FFT_real'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(c_complex), ct.POINTER(ct.c_double), ct.c_int, ct.c_int] )
        enum.append( { 'radix-none': 0, 'radix-2': 1, 'radix-4': 2 } )
    
    elif (name == 'IFFT'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(c_complex), ct.POINTER(c_complex), ct.c_int, ct.c_int] )
        enum.append( { 'radix-none': 0, 'radix-2': 1, 'radix-4': 2 } )
        
    elif (name == 'IFFT_real'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(c_complex), ct.c_int, ct.c_int] )
        enum.append( { 'radix-none': 0, 'radix-2': 1, 'radix-4': 2 } )
        
    elif (name == 'FFT_radix2'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(c_complex), ct.POINTER(c_complex), ct.c_int] )
    
    elif (name == 'IFFT_radix2'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(c_complex), ct.POINTER(c_complex), ct.c_int] )
        
    elif (name == 'FFT_radix4'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(c_complex), ct.POINTER(c_complex), ct.c_int] )
    
    elif (name == 'IFFT_radix4'):
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(c_complex), ct.POINTER(c_complex), ct.c_int] ) 
        
        
    elif (name == 'FFTRadix2Fwd'): #### OLD IMPLEMENTATUION #####
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.c_int] ) 
        
    elif (name == 'FFTRadix2Inv'): #### OLD IMPLEMENTATUION #####
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.c_int] )

    elif (name == 'FFTRadix4Fwd'): #### OLD IMPLEMENTATUION #####
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.c_int] ) 
        
    elif (name == 'FFTRadix4Inv'): #### OLD IMPLEMENTATUION #####
        func = map_func_safe( DLL, name, ct.c_int,
            [ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.c_int, ct.c_int] )        
        
    else:
        print(f"Error: Function {name} not contained in 'libDSP.dll'! (aborting)")
        
    return func, enum
