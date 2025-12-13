"""
Helpers for common tasks in digital signal processing & data analytics development
"""
import numpy as np

from zdev.ccnx import *
from zdev.libdsp import LIBDSP_FILE, call_signature


# INTERNAL PARAMETERS & DEFAULTS
_FS = 25000     # default sampling frequency [Hz]
_TS = (1./_FS)  # default sampling intervals [s] (since coupled to _FS --> 40usec)


def timeline(spec, Ts=_TS):
    """ Creates a discrete-time reference vector using equi-distant sampling. 
    
    Args:
        spec (number|2-tuple): Specification for the time vector to create. Either end-point 
            of timeline (i.e. int|float) or 2-tuple denoting the interval [start,stop].  
        Ts (float, optional): Sampling resolution of the reference vector. Defaults to '_TS'. 
    
    Returns:
        t (np.ndarray): Created time reference vector.  
    """    
    if ((type(spec) == np.float64) or (type(spec) == float) or (type(spec) == int)):
        t = np.arange(spec, step=Ts, dtype=np.float64)
    elif ((type(spec) == list) and (len(spec) == 2)):
        t = np.arange(start=spec[0], stop=spec[1], step=Ts, dtype=np.float64)
    else:
        print(f"Wrong timeline format '{spec}' specified!")
        t = None
    return t


def signal(t, f, A=1.0, shift=0.0, mode='sin', show_phase=False):
    """ Creates (oscillating) signals based on frequency 'f', amplitude 'A' and phase 'shift'.
    
    Note: Multi-tonal signals of the same 'mode' can be generated as well when providing lists 
    of parameters for frequency, amplitude and phase-shift. In this case, 'show_phase' refers 
    to the fundamental frequency only (i.e. first entry in 'f'). For more complex signals using 
    different modes, outputs of this function have to be superimposed.
    
    Args:
        t (float or ndarray): Time reference for the signal to be created. Typically, this will 
            specify the desired duration, but may also be an existing vector.
        f (float or list): Frequency(ies) of the signal. 
        A (float or list, optional): Amplitude(s) of the signal. Defaults to 1.
        shift (float or list, optional): Phase shift(s) of the signal [deg]. Defaults to 0.0.
        mode (str, optional): Type of signal to be created. The following options are available:
            'sin'/'cos':    Real-valued sinusoidal.
            'phasor':       Complex-valued sinusoidal (in two axes).
            'rect':         Rectangular wave (real-valued).
            'saw':          Sawtooth wave, i.e. ramp-upwards (real-valued).
            'tri':          Triangular wave (real-valued).
            Defaults to 'cos'.
        show_phase (bool, optional): Switch for exporting the (wrapped) phase of the signal as 
            well. Defaults to 'False'.       
        
    Returns:
        x (ndarray): Generated signal w/ length determined by 't'.
        px (ndarray, optional): (Fundamental) phase of signal (if applicable).            
    """   
   
    # ensure time reference is array
    try: 
        len(t)
    except:
        t = timeline(t)
    Ts = t[1]-t[0]
    
    # ensure matching length of parameters
    if ((type(f) is int) or (type(f) is float) or (type(f) is np.float64)):
        f = [f,]
    if ((type(A) is int) or (type(A) is float) or (type(A) is np.float64)):
        A = [A,]
    if ((type(shift) is int) or (type(shift) is float) or (type(shift) is np.float64)):
        shift = [shift,]
    C = min([len(f),len(A),len(shift)])
    
    # init output
    if (mode != 'phasor'):
        x = np.zeros_like(t)
    else:
        x = np.zeros_like(t) + 1j*np.zeros_like(t)
    
    # generate signal by additive synthesis of all frequency components
    for c in range(C):
        
        # configure cycle period [s] & number of samples in cycle [int] 
        Tc = 1/f[c]
        Nc = int(Tc/Ts)
        
        # configure phase    
        wt = 2*np.pi*f[c] * t
        phi = np.deg2rad(shift[c])
        N_phi = int(Nc*shift[c]/360.0)
        phase = wt + phi
                 
        # create frequency component
        if (mode == 'sin'):
            xc = np.sin(phase)            
        elif (mode == 'cos'):
            xc = np.cos(phase)            
        elif (mode == 'phasor'):
            xc = (np.cos(phase) + 1j*np.sin(phase))   
        elif (mode == 'rect'):
            xc = np.sign( np.sin(phase) )        
        elif (mode == 'saw'):
            ascender = np.arange(N_phi, N_phi+len(t), dtype=np.float64)        
            xc = (2/Nc) * edge(ascender, np.array([-(Nc/2),+(Nc/2)]), mode='wrap')        
        elif (mode == 'tri'):   
            ascender = np.arange(N_phi, N_phi+len(t), dtype=np.float64)
            wrapper = edge(ascender, [-(Nc/4),+(3*Nc/4)], mode='wrap')
            xc = (4/Nc) * edge(wrapper, [-(Nc/4),+(Nc/4)], mode='bounce')
        else:      
            print(f"Unknown signal type '{mode}' specified!")
            return None
        
        # scale amplitude & keep fundamental phase
        x += A[c] * xc
        if (c == 0):
            px = phase
    
    # finalise phase
    if (show_phase):
        px = edge(px, [-np.pi,+np.pi], mode='wrap')
        return x, px
    else:
        return x
    
    
def signal_3ph(t, f, A=1.0, phi=0.0, rot=[0,-120,-240], bal=[1,1,1]):
    """ Creates a 3-phase signal w/ common time 't' and frequency 'f'.
    
    This convenience function allows the creation of 3-phase signals as e.g. required for 
    electrical power simulations in one go. Besides the inter-rotation of the phases, imbalance 
    in the individual amplitudes may also be modelled easily (if desired).
    
    Args:
        t (ndarray or float): Time reference for the signal to be created. Typically, this will 
            be an existing vector, but may also specify the duration (= end time).
        f (float): Nominal frequency common to the 3-phase signal.
        A (float): Nominal amplitude of the 3-phase signal.
        phi (float, optional): Phase shift for all phases [deg]. Defaults to 0.
        rot (3-tuple, optional): Inter-rotation of the three phases [deg], i.e. angular 
            difference between sinusoidals. Defaults to [0,-120,-240]. 
        bal (3-tuple, optional): Possible imbalancing of the phase amplitudes. Defaults to 
            "perfect balance", i.e. [1,1,1].
            
    Returns:
        rst (ndarray): Resulting 3-phase signal w/ shape (len(t),3).
    """                
    rst = np.zeros(shape=(3,len(t)))  
    for p in range(3):
        rst[p,:] = signal(t, f, A=A*bal[p], shift=(phi+rot[p]), mode='cos')              
    return rst


def noise(t, mx=0.0, sx=1.0, mode='Gauss'):
    """ Creates a noise signal for reference time 't' w/ given PDF 'mode'.    
    
    Args:
        t (ndarray or float): Time reference for the noise to be created. Typically, this will 
            be an existing vector, but may also specify the duration (= end time).
        mx (float, optional): Mean / center of PDF. Defaults to 0.
        sx (float, optional): Standard deviation of PDF. Defaults to 1.
        mode (str, optional): Type of probability density function (PDF) w/ options:           
            'Gauss':    Normal distribution
            'Laplace':  Super-Gaussian, i.e. higher probability of both small & large values
            'uniform':  Constant over unit interval [0,1]
            Defaults to 'Gauss'.
                
    Returns:
        n (ndarray): Generated noise w/ length determined by 't'.

    Examples: Definition of PDFs:
                                             1                 (X-mx)^2
        Gaussian (normal):  fx(X)  =  --------------- * e^( -  -------- )
                                      sqrt(2*pi*sx^2)           2*sx^2
    
                                       1              |X-mx|
        Laplacian:          fx(X)  =  ----  *  e^( -  ------ )
                                      2*sx              sx
    
                                       1
        Uniform:            fx(X)  =  ----    for  mx-sx < x < mx+sx  (else fx(X) == 0)
                                      2*sx
    """
    
    # consistency check
    if ((type(t) == float) or (type(t) == int)):
        t = timeline(t, Ts=_TS)
       
    # generate noise
    if (mode == 'Gauss'):
        n = np.random.normal(mx, sx, size=t.shape)
    elif (mode == 'Laplace'):
        n = np.random.laplace(mx, sx, size=t.shape)
    elif (mode == 'uniform'):
        n = np.random.uniform((mx-sx), (mx+sx), size=t.shape)
    else:        
        pass # TODO: add more PDFs?
    
    return n


def synth(t, mode, f0, fs=_FS, phi=0.0):
    """ Synthesizes a signal --> actually a "unit-test" for libDSP!???? """    
    # ensure time reference is array     
    try: 
        len(t)
    except:
        Ts = (1./fs)
        print(f"before timeline: {Ts}")
        t = timeline(t, Ts=(1./fs))
    Ts = t[1]-t[0]
    fs = 1./Ts
    print(f"Ts = {Ts} --> fs = {fs}")        
    
    # init
    y = np.zeros_like(t)    
    DLL = open_lib(LIBDSP_FILE)
    func, enum = call_signature(DLL, 'oscillator_mod')
    
    # amplitude modulation (cycle around 1.0)
    Amod = 1.0 * np.ones_like(t)
    Amod = 1.0 + 0.3*signal(t, f=4.0, mode='sin')  
    
    # frequency modulation (sweep: f0 --> 2*f0)
    fmod = f0 * np.ones_like(t)
    N = int(0.3*fs)
    fpatch = (f0/N) * np.arange(0,2*N)
    fmod[N:3*N] += fpatch     # sweep: f0 --> 2*f0
    
    # phase modulation
    phimod = phi * np.ones_like(t)
                
    func, enum = call_signature(DLL, 'oscillator_mod')  
    rc = func(y, enum[0][mode], f0, phi, Ts, len(t), Amod, fmod, phimod)
   
    close_lib(DLL)    
    return y
    
    

#-----------------------------------------------------------------------------------------------
# Python implementations of "nonlinear signal operations"
#   --> faster C implementations by "libDSP" exist as "_ffc" ("fast from C")
#-----------------------------------------------------------------------------------------------

def edge(x, limits, mode='stick', ffc=True):
    """ Applies (nonlinear) edge-handling operations on signal 'x'. 
    
    Args:
        x (np.ndarray): Input signal to be limited in desired mode.
        limits (2-tuple): Edge boundaries as interval [lo,hi]. Note that this also allows for 
            an asymmetric limitation.
        mode (str, optional): Desired behaviour when encountering the boundaries w/ options 
            'stick'|'bounce'|'wrap'. Defaults to 'stick'.
        ffc (bool, optional): Switch to "fast-from-C" (ffc) implementation. Defaults to 'True'.
            
    Returns:
        xe (np.ndarray): Limited ouput signal w/ same shape as input 'x'.
    """
    xe = np.zeros_like(x)    
    
    if (ffc): # C implementation     
        DLL = open_lib(LIBDSP_FILE, verbose=False)
        func, enum = call_signature(DLL, 'edge')
        rc = func(xe, x, len(x), np.array(limits), enum[0][mode])
        close_lib(DLL, verbose=False)
        return xe
   
    else: # Python implementation        
        hi = limits[1]
        lo = limits[0]
        num_cycles = 0
        for k, xk in enumerate(x):            
            if (mode == 'stick'):
                if (xk > hi):
                    xk = hi
                elif (xk < lo):
                    xk = lo                    
            elif (mode == 'bounce'):
                if (xk > hi):
                    xk = hi - np.abs(xk-hi)
                if (xk < lo):
                    xk = lo + np.abs(xk-lo)              
            elif (mode == 'wrap'):
                xk -= num_cycles*(hi-lo)
                if (xk > hi):
                    xk -= (hi-lo)
                    num_cycles += 1
                elif (xk < lo):
                    xk += (hi-lo)
                    num_cycles -= 1                    
            else:
                print("Unknown mode specified! (aborting)")
                return                
            xe[k] = xk        
        return xe


def phase_wrap(x):
    """ Forces input 'x' to interval [-pi, +pi) by 'wrapping' it. """
    return edge(x, limits=[-np.pi,+np.pi], mode='wrap')


def origin(x, width=0.3, mode='deadzone', ffc=True):
    """ Applies modification of signal 'x' inside band of 'width' around x=0.
    
    Args:
        x (np.ndarray): Input signal to be modified around its origin.
        width (float): One-sided width of zone/band around 0 for which to suppress the signal.
        mode (str, optional): Decision how 'xd' continues outside this area w/ options 
            'deadzone'|'deadband'. Defaults to 'deadzone'.
        ffc (bool, optional): Switch to "fast-from-C" (ffc) implementation. Defaults to 'True'.
            
    Returns:
        xd (np.ndarray): Modified ouput signal w/ same shape as input 'x'.
    """   
    xd = np.zeros_like(x)
    
    if (ffc): # C implementation        
        DLL = open_lib(LIBDSP_FILE, verbose=False)
        func, enum = call_signature(DLL, 'origin')       
        rc = func(xd, x, len(x), width, enum[0][mode])      
        close_lib(DLL, verbose=False)
        return xd
   
    else: # Python implementation       
        for k, xk in enumerate(x):            
            if (mode == 'deadzone'):
                if (abs(xk) < width):
                    xd[k] = 0.0
                else:
                    xd[k] = xk                    
            elif (mode == 'deadband'):
                if (abs(xk) < width):
                    xd[k] = 0.0
                else:
                    xd[k] = xk - np.sign(xk)*width                    
            else:
                print(f"Unknown dead-set mode '{mode}'! (aborting)")
                return None      
        return xd


def quant(x, num_bits, Amax=1.0, mode='midrise', ffc=True):
    """ Applies quantisation of signal 'x' acc. to quantiser 'mode'.
    
    Args:
        x (np.ndarray): Input signal to be modified around its origin.
        num_bits (int): Number of bits used for amplitude resolution. The resulting number of 
            levels is ~ 2**num_bits.
        Amax (float, optional): Maximum (absolute) amplitude to consider. Exceedings signal 
            values are mapped to max/min quantisation level.
        mode (str, optional): Quantiser mode w/ options 'midrise'|'midtread'|'trunc'. Defaults 
            to 'midrise'.
        ffc (bool, optional): Switch to "fast-from-C" (ffc) implementation. Defaults to 'True'.
            
    Returns:
        xq (np.ndarray): Quantised ouput signal w/ same shape as input 'x'.    
    """
    xq = np.zeros_like(x)
    
    if (ffc): # C implementation
        DLL = open_lib(LIBDSP_FILE, verbose=False)
        func, enum = call_signature(DLL, 'quant')       
        rc = func(xq, x, len(x), num_bits, Amax, enum[0][mode])      
        close_lib(DLL, verbose=False)
        return xq
    
    else: # Python implementation
        num_levels = 2**num_bits
        q = 2 * Amax / num_levels  
        for k, xk in enumerate(x):
            xk = edge([xk], limits=[-Amax,+(Amax-q/2)], mode='stick', ffc=False)            
            if (mode == 'midrise'): # = num_levels
                n = np.floor( xk/q ) + 0.5
            elif (mode == 'midtread'): # = num_levels+1
                n = np.floor( (xk/q) + 0.5 )
            elif (mode == 'trunc'): # num_levels-1
                if (xk < 0):
                    n = np.floor( (xk/q) + 1)
                else:
                    n = np.ceil( (xk/q) - 1)                    
            else:
                print(f"Unknown quantisation mode '{mode}'! (aborting)")
                return None           
            xq[k] = n*q        
        return xq



# def tdf_plain_py(x, h):
#     """ todo """
#     L = len(x)
#     N = len(h)
#     # y = np.zeros_like(x)
#     y = np.zeros(L+N)
    
#     for k in range(N):
#         for n in range(1+k):
#             # if (k == N-1):
#             #     print(f"(1) k == N-1 --> final index n = {n}")
#             y[k] += x[k-n] * h[n]

#     for k in range(N,L):
#         for n in range(N):
#             # if (k == L-1):
#             #     print(f"(2) k == L-1 --> final index n = {n}")
#             y[k] += x[k-n] * h[n]
            
#     for k in range(L,L+N):
#         # print(f"(3) k = {k}...")
#         for n in range((k-(L-1)),N):
#             # if (k >= L+N-3):
#             #     print(f"   --> (3) --> indices n = {n}")
#             y[k] += x[k-n] * h[n]
            
#     return y
