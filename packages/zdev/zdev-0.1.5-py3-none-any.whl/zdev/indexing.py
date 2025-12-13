"""
Indexing-related functions for Python

This module contains pure functions for common tasks of "indexing".
In particular, it offers helpers to...
    ...get indices of list elements matching arbitrary conditions
    ...get integer-valued signal segments (-> [idx, runlength, value])
    ...get index from string & use MATLAB-style range expansion (e.g. '[A1:A2,...,M,...,Z1:Z2]')
    ...convert indices to alphabetic representation (e.g. Excel cols)
    ...compute required digits or get positions from (any-base) integers
    ...perform a "file-goto" w/ different modes (e.g. tag to find / # occurrences / # of lines)
"""
import re
import numpy as np

from zdev.searchstr import *


# INTERNAL PARAMETERS & DEFAULTS
_RX_INDEX = re.compile(S_INTEGER)
_RX_INDEX_RANGE = re.compile(S_INTEGER+':'+S_INTEGER)
_RX_INDEX_STRING = re.compile(r'\[{1}[0-9:, ]*\]{1}')
_ALPHABET = ('A','B','C','D','E','F','G','H','I','J','K','L','M',
             'N','O','P','Q','R','S','T','U','V','W','X','Y','Z')


def find_index(x, condition=None):
    """ Retrieves all indices of 'x' where a certain 'condition' is met.

    This is a convenience routine to find the indices of list elements meeting a certain
    condition. If none is given, the routine will only accept 'True' or positive values. Note
    that the same effect could be realised by: 'condition = (lambda x: x > 0)'. If the input is
    not a list, it will be expanded.

    Args:
        x (list): Input array of int/float from which indices are to be found.
        condition (:expr:, optional): Functional expression taking values from 'x' as arguments.
            Defaults to 'None'.

    Returns:
        idx (list): All indices where 'x' meets the 'condition'.
    """

    # expand to list (if required)
    if ((type(x) is int) or
        (type(x) is float) or (type(x) is np.float32) or (type(x) is np.float64)):
        x = [x,]

    # create index array
    if (condition is None):
        idx = [n for (n, val) in enumerate(x) if ((val is True) or (val > 0))]
    else:
        idx = [n for (n, val) in enumerate(x) if condition(val)]

    return idx


def find_index_str(any_str):
    """ Extracts all "index strings" from an arbitrary string.

    This function retrieves all "index strings" from the input 'any_str'. All index strings
    must reside within rectangular brackets '[' ... ']' and may only contain:
        + integer indices
        + commas ',',
        + colons ':' (for expansion)
        + whitespaces
    Further processing usually involves subsequent expansion by "expand_index_str()".

    Args:
        any_str (str): Any arbitrary input string.

    Returns:
        idx_str (list): List of all index strings found (if any).
    """
    idx_str = _RX_INDEX_STRING.findall(any_str)
    return idx_str


def find_segments(x, min_length=1, values=[], sort=False):
    """ Retrieves runlength analysis on (integer-valued) signal 'x'.

    This function analyses 'x' according to consecutive segments of same value. It returns
    information on the whole partitioning, i.e. starting index, runlength (= number of instants
    w/o altering signal value) and the actual value, for all segments in the signal. The output
    may further be restricted to include only segments w/ minimum length and/or desired values.
    Moreover, outputs could also be sorted from longest to shortest. Note that applying this
    function is only reasonable if 'x' contains only 'int' values!

    Args:
        x (list or np.array): Input signal to be analysed.
        min_length (int, optional): Minimum runlength for addition to outputs. Defaults to '1'.
        value (list, optional): List of desired signal values to analyse for. Defaults to '[]'.
        sort (bool, optional): Switch for sorting the output from longest to shortest runlength.
            Defaults to 'False'.

    Returns:
        valid_segments (list): All segments that have been identified and "validated" (w.r.t.
            any optional restrictions), format: [[ idx, runlength, val ],]
    """

    # find alterations in signals value (disregarding sign)
    dx = np.zeros(len(x))
    dx[1:] = np.diff(x)
    alterations = find_index( np.abs(dx) )

    # determine starting positions of segments
    num_segments = 1+len(alterations)
    seg_idx = np.zeros(num_segments)
    seg_idx[0] = 0 # to make it explicit ;)
    seg_idx[1:] = alterations

    # store partitioning information
    all_segments = []
    if (alterations != []):

        # determine "runlength" for each segment
        seg_length = np.zeros(num_segments)
        seg_length[:-1] = np.diff(seg_idx)
        seg_length[-1] = len(x) - seg_idx[-1]

        # complement information by adding signal value for each segment
        for n, length in enumerate(seg_length):
            idx = int(seg_idx[n])
            run = int(length)
            val = x[idx]
            all_segments.append([idx, run, val])

    else:
        # constant signal
        all_segments.append([0, len(x), x[0]])

    # enforce minimum length of segments
    if (min_length > 1):
        long_segments = [seg for seg in all_segments if (seg[1] >= min_length)]
    else:
        long_segments = all_segments

    # consider only specific signal values
    if (len(values) > 0):
        valid_segments = [seg for seg in long_segments if (seg[2] in values)]
    else:
        valid_segments = long_segments

    # sort results (w.r.t. to length)?
    if (sort):
        valid_segments.sort(key=(lambda item: item[1]))

    return valid_segments


def expand_index_str(idx_str):
    """ Expands an "index string" to a set of monotonically increasing integers.

    This is motivated by the well-known MATLAB-style array indexing, where distinct values are
    separated by commas ',' and can be combined with "START:STOP" ranges. However, it should
    be noted that STOP here is INCLUDED in the set - as opposed to standard Python behaviour!

    Args:
        idx_str (str): Index string as e.g. retrieved by "find_index_str()".

    Returns:
        idx_set (list): List of monotonically increasing integers referred to by 'idx_str'. Note
            that this is not an actual 'set' but a 'list' in order to ensure a sorted output!

    Example:
        idx_str:       '1,3:6,42,15,64,77:80,10,97:98'
        --> idx_set:  [ 1,3,4,5,6,10,15,42,64,77,78,79,80,97,98 ]
    """
    try:
        # step 1: get ALL numbers first (i.e. single numbers and starts/stops of ranges)
        idx = [int(n) for n in _RX_INDEX.findall(idx_str)]

        # step 2: expand index ranges & and include intermediate numbers
        for range_str in _RX_INDEX_RANGE.findall(idx_str):
            start, stop = re.findall(S_INTEGER, range_str)
            if (int(start) <= int(stop)):
                for n in range(int(start), int(stop)+1):
                    idx.append(int(n))
            else:
                continue # irregular range specified (i.e. start > stop!)

        # step 3: make unique (i.e. "convert" to set) & sort
        idx_set = list(set(idx))
        idx_set.sort()

        return idx_set

    except:
        return None


def convert_index_alphabetic(idx_in, inverse=False, alphabet=_ALPHABET):
    """ Converts an integer index to alphabetic strings 'A' to 'ZZZZ...'.

    This function can be used for indexing related to e.g. Microsoft Excel sheets. If the
    'inverse' flag is set, a backward conversion is applied (e.g. from 'AF' to 32). In addition,
    a case-specific 'alphabet' can be used if necessary.

    Args:
        idx_in (int or str): Input index (type depending on fwd/bwd conversion).
        inverse (bool, optional): Flag for backward conversion (i.e. 'str' to 'int'). Defaults
            to 'False'.
        alphabet (tuple, optional): Symbol set used for alphabetic strings. Defaults to 'ABC'.

    Returns:
        idx_out (str or int): Output index (type depending on fwd/bwd conversion).
    """
    A = len(alphabet)

    if (not inverse):

        # consistency check
        if ((type(idx_in) != int) or (idx_in <= 0)):
            print(f"Error: Given index {idx_in} cannot be converted to 'alphabetic' index!")
            return -1

        # determine required length (for Excel-style concatention)
        Nc = get_num_digits(idx_in, base=A, concatenate=True)

        # determine numerical indices for all postions
        n = (1+Nc)*[-1]
        for p in range(Nc,1,-1):

            # strip lower bases from index
            reduce = 0
            for k in range(p,1,-1):
                reduce += A**(k-2)

            # calculate index
            n[p] = int( np.floor((idx_in-reduce) / A**(p-1)) )
            idx_in -= n[p] * A**(p-1)

        n[1] = idx_in

        # assign alphabetical elements (= characters)
        idx_out = ''
        for p in range(Nc,0,-1):
            idx_out += alphabet[ n[p]-1 ]

    else: # (inverse is True)

        # determine given length (of Excel-style index)
        Nc = len(idx_in)

        # sum-up all integer indices
        idx_out = 0
        for p in range(Nc,0,-1):
            n = 1 + alphabet.index(idx_in[Nc-p])
            idx_out += n * A**(p-1)

    return idx_out


def get_num_digits(N, base=10, concatenate=False):
    """ Determines number of digits required to represent 'N' in the given 'base'.

    This function helps to get the number of required digits in order to fully represent the
    number 'N' in a certain 'base' (default: 10). The special 'concatenate' flag is required
    for symbol strings with growing length and no hidden symbol for leading '0'.

    Args:
        N (int): Number for which "digit length" is to be determined
        base (int, optional): Base of number representation (i.e. cardinality of symbol set).
            Defaults to '10'.
        concatenate (bool, optional): Flag for growing-length strings (e.g. Excel style).
            Defaults to 'False'.

    Returns:
        num_digits (int): Number of required digits.

    Example:
        Excel string as representation w/ 'base = 26' and 'concatenate = True':
            26      --> 'A, B, C ... Z'
            26**2   --> 'AA, AB, AC ... AZ | BA, BB, ... BZ |   ...   | ZA ... ZZ'
            26**3   --> 'AAA, AAB, ... AAZ | BAA, ..., BZZ | CAA   ...   || ZZA ... ZZZ'
            ...
    """

    num_digits, N_max = 1, base

    while (N > N_max):
        num_digits += 1
        if (concatenate):
            N_max += base**num_digits
        else:
            N_max = base**num_digits

    return num_digits


## TODO: have a conversion from base 1 to base 2 for a given number?


def get_digit(N, d, base=10):
    """ Decomposes integer number 'N' and retrieves desired digit 'd'.

    This function extracts the digit value at a certain position 'd' of the considered number
    'N' in 'base' representation. Note that the position 'd' is interpreted here as counting
    from left-to-right. Per default a decimal 'base' is assumed.

    Args:
        N (int): Number from which the digit is to be extracted.
        d (int): Digit position (counting from left=max to right=0).
        base (int, optional): Base of considered representation. Defaults to '10'.

    Returns:
        digit (int): Value / digit at position 'd' (from interval [0,base-1])
    """

    # check on number of digits
    num_digits = get_num_digits(N, base)
    if ((d <= 0) or (d > num_digits)):
        print(f"Warning: Position #{d} exceeds number of digits contained in '{N}'! ({num_digits})")
        return -1

    # decompose into "residuals"
    res = (1+num_digits)*[0]
    res[num_digits] = N
    for p in range(num_digits-1,0,-1):
        res[p] = res[p+1] % (base**p)

    # extract desired digit
    digit = int( (res[1+num_digits-d] - res[num_digits-d]) / base**(num_digits-d) )

    # Note: Implementation is done via a "residuals" buffer w/ an initial placeholder in order
    #       to use a regular 1-based indexing.
    #       Example:  'N = 2475' and extracting 'd = 3':
    #       --> res = [ 0, 5, 75, 475, 2475 ]   --> 3rd position: (75 - 5) / 10^1   --> 7

    return digit


def file_goto(tf, feature, mode='tag', nextline=True, backwards=False):
    """ Allows ease of navigation for text-based files.

    This function provides some standard means of line-based navigation within text-files by
    advancing the file-pointer 'tf' according to some 'feature'. Depending on the chosen 'mode'
    this can by specified by distinct strings ('tag'), specific symbols and a required number
    of occurrences ('parts') or simply by a certain number of lines to consume.

    Args:
        tf (:obj:): 'TextIOWrapper' object (file-pointer) of w/ text-read permission.
        feature (int, str or 2-tuple): Criteria to look for in the file. This argument depends
            on the 'mode' setting.
        mode (str, optional): Mode of file navigation (see examples below). Defaults to 'tag'.
        nextline (bool, optional): Switch for positioning the file-pointer to the next line
            after navigation. Defaults to 'True'.

    Returns:
        pos (int): File-pointer position where the 'feature' is (first) matched. This can then
            be used with the ".seek()" method.
        consumed (int): Lines consumed before 'feature' was found. (Note: Actual line # after
            call should be +1 or +2 if 'nextline = True').

    Example:
        mode = 'tag'        --> feature is a markup string (e.g. 'CXMAP: ')
        mode = 'parts'      --> feature is a 2-tuple (str & num occurrences, e.g. ('->', 3))
        mode = 'not_parts'  --> feature is a 2  ### TODO ###
        mode = 'lines'      --> feature is the number of lines to be skipped (e.g. 16)
    """

    # init
    start = tf.tell()
    pos = start
    consumed = 0
    consumed_bytes = 0

    # search operation
    if (mode == 'tag'):
        for line in iter(tf.readline,''):
            if (line.startswith(feature)):
                pos = tf.tell()
                break
            else:
                consumed += 1
                consumed_bytes += len(line)

    elif (mode == 'parts'):
        for line in iter(tf.readline,''):
            parts = line.split(feature[0])
            if (len(parts) > feature[1]):
                pos = tf.tell()
                break
            else:
                consumed += 1
                consumed_bytes += len(line)

    elif (mode == 'not_parts'):
        for line in iter(tf.readline,''):
            parts = line.split(feature[0])
            if (len(parts) > feature[1]):
                consumed += 1
                consumed_bytes += len(line)
            else:
                pos = tf.tell()
                break

    # Note: Use 'iter()' (rather than 'for item in file') so as to keep 'ftell()'!

    elif (mode == 'lines'):
        for n in range(feature):
            line = tf.readline()
            pos = tf.ftell()
            consumed += 1
            consumed_bytes += len(line)

    # adjustments
    if (pos == start):
        return None
    else:
        if (nextline is False):
            pos -= len(line)
            tf.seek(pos, 0)

    return pos, consumed, consumed_bytes
