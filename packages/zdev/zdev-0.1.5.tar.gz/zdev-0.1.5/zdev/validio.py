"""
Validation and (user) I/O-related functions for Python

This module provides helper functions for validating proper input/output types of e.g. strings
and handling of plain text files (e.g. cleaning of doubly-quoted strings).
"""
import os
import re
import sys
import stat

from zdev.indexing import expand_index_str, find_index_str
from zdev.searchstr import S_IDENT_W_DOT, S_SEP_W_DOT, S_BRACKETS, S_SPECIAL


# INTERNAL PARAMETERS & DEFAULTS
_ENCODINGS = ('ascii', 'utf_8', 'utf_16', 'utf_32')


def valid_prec(x, p):
    """ Returns float 'x' with a valid, i.e. fixed, precision 'p'.

    Args:
        x (float): Floating-point number
        p (int): Desired precision w.r.t. number of digits after '.'.

    Returns:
        xf (float): Floating-point number truncated to 'p' fractional digits.
    """
    return float(f'{x:.{p}f}')


def valid_path(path_in):
    """ Validates that proper path separators are applied for 'path_in'.

    Args:
        path_in (str): Original path location string (may contain '\' and/or '/').

    Returns:
        path_out (str): Output path string w/ system-dependent separators.
    """
    if (sys.platform.startswith == 'win'):
        path_out = path_in.replace('/', '\\')
    elif (sys.platform.startswith == 'linux'):
        path_out = path_in.replace('\\', '/')
    else:
        path_out = path_in
    return path_out


def valid_str_string(str_in):
    """ Validates 'str_in' is cleaned of dual quotes (either single ' or double ").

    This function validates that only a single pair of quotes (either ' or ") remains in the
    output 'str_out'. This may be required in circumstances of repeated im-/exporting of data
    to/from files where strings may exhibit a "cluttering" and mixture of quotes. If the input
    is not of type 'str' it will just be passed through.

    Args:
        str_in (str): Input string, possibly w/ multiple-stage quotes.

    Returns:
        str_out (str): Output string w/ clean quotes.
    """
    str_out = str_in
    while ((type(str_in) is str) and ((str_in[0] in ("'",'"')) and (str_in[-1] in ("'",'"')))):
        str_out = str_in[1:-1]
        str_in = str_out
    return str_out


def valid_str_number(s):
    """ Validates input string 's' is *always* mapped to a number.

    Args:
        s (str): Input string that should refer to a number, e.g. "4.77".

    Returns:
        x (float): Output number as 'float'. Will be '0.0' conversion fails, or if 's' is empty.
    """
    try:
        x = float(s)
    except:
        x = 0.0
    return x


def valid_str_name(name, repl_str='_', repl_dict=None, repl_defaults=True, compact=False):
    """ Validates 'name' is "safe" for using as filename (i.e. removes "problematic" chars).

    Args:
        name (str): Original name / identifier string (incl. problematic chars).
        repl_str (str): Replacement string (typically one char) for "problematic" parts of the 
            original. Defaults to underscore, i.e. '_'.
        repl_dict (dict): Dictionary with 'key: value' pairs for fine-tuning of replacements.
            If this is given, this will be executed first, in order to gain precedence.
            Defaults to 'None'.
        repl_defaults (bool, optional): Switch to replace all known, special chars (e.g. dots,
            slahes, brackets etc). Defaults to 'True'.
            Note: In case only the provided 'repl_dict' shall be used, this has to be disabled!
        compact (bool, optional): Switch to delete all remaining whitespace, otherwise 
            'repl_str' will be applied again. Defaults to 'False'.
        

    Returns:
        name_safe (str): Modified name / identifier that can "safely" be used as e.g. filename.

    Examples: For usage w/ replacement by '_' and dict {'°C': 'deg'} and active 'compact':
                input:  "This [is] my/your 100°C hot+stuff;  {extra space}"
                output: "This_is_my_your100deghot_stuff__extraspace_"
    """
    tmp = name
    
    # replace "problematic" (but information-bearing) chars by equivalent strings?
    if (repl_dict is not None):
        for key in repl_dict.keys():
            tmp = tmp.replace(key, repl_dict[key])
    # Note: Examples for this might be {'>=': 'gte'}, {'+': 'plus'} or {'°C': 'degC'}.
    
    # replace default special chars
    if (repl_defaults):        
        tmp = re.sub(S_BRACKETS+'|'+ S_SEP_W_DOT+'|'+S_SPECIAL, repl_str, tmp)
        tmp = tmp.replace('/',repl_str)   # forward dashes "/"
        tmp = tmp.replace('\\',repl_str)  # backward dashes "\"

    # replace any remaining whitespace
    if (compact):
        name_safe = tmp.replace(' ', '')
    else:
        name_safe = tmp.replace(' ', repl_str)

    return name_safe


def valid_elements(collection, prefix='v_', postfix='', tkinter=False):
    """ Extracts only elements w/ valid names from a 'collection'.

    The 'validation' criteria are thereby given by both 'prefix' and/or 'postfix' strings. If
    one or both of these are set to 'None' they are essentially disregarded. In cases where the
    collection refers to tkinter variables (i.e. Boolean/Int/Double/StringVar()), the respective
    '.get()' method is used in order to return the plain values only.

    Args:
        collection (dict): Input data set to be matched against pre-/postfix conditions.
        prefix (str, optional): Required prefix for 'validated' elements. Defaults to 'v_'.
        postfix (str, optional): Required postfix for 'validated' elements. Defaults to ''.
        tkinter (bool, optional): Flag indicating that collection contains tkinter variables.
            Defaults to 'False'.

    Returns:
        elements (dict): Output data set w/ possibly reduced number of 'validated' entries.
    """
    M = len(prefix)
    ## TODO?  N = len(postfix)

    # extraction process
    elements = {}
    for item in collection.keys():
        if (item.startswith(prefix)):
            # TODO: add the postfix requirement!
            #   (how to use 'N'? --> [ :-1-(N-1)]? but then: N=0 --> [ :0] --> will crash!!)
            if (tkinter):
                elements[item[M:]] = collection[item].get()
            else:
                elements[item[M:]] = collection[item]

    return elements


def valid_encoding(text_file):
    """ Checks a 'text_file' for used encoding (by trial & error).

    Args:
        text_file (str): Filename of text-tile to be tested for encoding.

    Returns:
        enc ('str'): Encoding as found in file (i.e. 'utf-8' or else). Defaults to 'None'.
    """

    # check proper encoding ("trial & error")
    matched = False
    for enc in _ENCODINGS:
        fh = open(text_file, mode='rt', encoding=enc)
        try:
            fh.readline()
            fh.seek(0)
            matched = True
            break
        except:
            fh.close()
            continue

    # return only if matched
    if (matched):
        return enc
    else:
        return None


def valid_args(inputs, force_int=False, resolve_idx_str=True):
    """ Validates arguments for function calls.

    This function probes if the input string(s) can be interpreted as float, integer or boolean
    values. The resulting output list contains the same number of elements, however, the
    types of all elements may vary.

    Args:
        inputs (list): List of entries, all of type 'str' (single inputs are promoted to list).
        force_int (bool): Switch for enforcing 'float' to 'int' conversion whenever possible.
            Defaults to 'False'.
        resolve_idx_str (bool): Switch for expanding index strings to sets of integer indices.
            Defaults to 'True'.

    Returns:
        outputs (list): Validated arguments (for function calls) w/ possibly converted types.
    """

    # ensure 'list' type
    if (type(inputs) != list):
        inputs = [inputs]

    # clean strings & map to types (where possible)
    outputs = []
    for item in inputs:
        chk = valid_str_string(item)

        # try to resolve index string?
        if (resolve_idx_str and (find_index_str(chk) != [])):
            arg = expand_index_str(chk)

        else: # try to map all items to standard types

            if (chk == 'True'):
                arg = True
            elif (chk == 'False'):
                arg = False
            elif (chk == 'None'):
                arg = None
            else:
                try:
                    arg = float(chk)
                    if (force_int and arg.is_integer()):
                        arg = int(arg)
                except:
                    try:
                        arg = int(chk)
                    except:
                        arg = chk

        outputs.append( arg )

    return outputs


def force_remove(func, path, excinfo):
    """ Forcibly removes folders even if they are set to "read only".

    Set this function as 'onerror' handling when calling to 'shutil.rmtree()', i.e.:
        > shutil.rmtree(myfolder, onerror=force_remove)

    [ https://stackoverflow.com/questions/1889597/deleting-read-only-directory-in-python ]
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)
    return


def file_clear_strings(text_file, symbol='"', verbose=True):
    """ Clear all strings in all lines of 'text_file' from 'symbol' (i.e. replace by '').

    Since this operation may be quite time consuming for large files (> 100MiB), it operates in
    a "smart" mode, i.e. actual processing is only done if 'symbol' is found in the first line
    of the file. If the screening operation breaks, only the "healthy" part of the file is
    written-back under the original filename, whereas the (corrupted) original is also retained
    for further analysis.

    Args:
        text_file (str): Filename of text-file to be cleaned.
        symbol (str, optional): Symbol that should bve removed through "cleaning". Defaults to
            '"' (double-quotes) as these are the most annoying from CSV-files.
        verbose (bool, optional): Switch to throw status messages & warnings if necessary.
            Defaults to 'True'.

    Returns:
        --
    """
    clean_lines = []
    enc = valid_encoding(text_file)

    # read data from file & clear
    with open(os.path.abspath(text_file), mode='r', encoding=enc) as tf:

        # probe 1st line
        line = tf.readline()
        chk = line.replace(symbol, '')
        if (len(chk) == len(line)):
            if (verbose):
                print(f"Warning: No symbol '{symbol}' found in 1st line of file! (skipping)")
            return

        # screen whole file
        clean_lines.append(chk)
        broken = False
        num_lines = 1
        while (True):
            if ((not num_lines%100000) and verbose):
                print(f"(read {num_lines} lines)")
            try:
                line = tf.readline()
                if (line != ''):
                    clean_lines.append(line.replace(symbol, ''))
                else:
                    break
                num_lines += 1
            except: # !! something is strange in the file :( !!
                broken = True
                print(f'Warning: Error @ line {num_lines-1}!! (writing until "last good")')

    # overwrite file (safely!)
    if (verbose):
        print(f"Overwriting '{text_file}' safely! (using temporary file copy)")
    with open(os.path.abspath(text_file+'_temp'), mode='wt') as tf:
        tf.writelines(clean_lines)
    if (broken):
        os.rename(text_file, text_file+'_ORIG_BROKEN') # keep original for analysis!
    else:
        os.remove(text_file)
    os.rename(text_file+'_temp', text_file)

    return


# ################################################################################################
# #
# # NOTE: The following functions are not used anymore due to the (more) efficient use of the 
# #       standard module "configparser". By this, standard *.ini files can be used in an 
# #       intuitve way, also allowing for commented lines and grouped sections of params:
# #
# #       >>> import configparser as cp
# #       >>> cfg.read(config_file)
# #       >>> cfg.has_section('SEC_NAME') --> returns bool, e.g. to check on futher processing
# #
# ################################################################################################

#_RX_PARAM_LINE = re.compile(S_IDENT_W_DOT+r'\s*=\s*')

# def text_read_params(text_file, rx_param_line=_RX_PARAM_LINE):
#     """ Extracts all parameter variables from 'text_file'.

#     This functions read all available variables from 'text_file', if in the line-wise format:
#     "PARAM = VALUE". Any whitespaces or comments starting by '#' are ignored. By default, no
#     hyphens '-' or colons ':' are allowed in the identifiers/names. In order to lift these
#     restrictions, other identification criteria for parameter lines can be used by setting
#     the regexp 'rx_param_line'.

#     Args:
#         text_file (str): Filename of the text-file from which parameters are to be collected.
#         rx_param_line (:obj:, optional): Search criteria of type 're.Pattern'. Defaults to
#             're.compile(r'[a-zA-Z0-9_.]+\s*=\s*', re.UNICODE)'.

#     Returns:
#         params (dict): Dictionary of all parameter variables found in 'text_file'.
#         num_read (int): Number of read variables (i.e. "len(params)" for convenience).
#     """

#     # init
#     params = {}
#     num_read = 0

#     # extract all parameters
#     with open(os.path.abspath(text_file), mode='rt') as tf:
#         for n, line in enumerate(tf):

#             param_def = _RX_PARAM_LINE.search(line)
#             if (param_def is not None):

#                 # analyse definition
#                 parts = param_def.string.split('=')
#                 name = parts[0].strip()
#                 value = parts[1].split('#')[0].strip() # Note: Trailing omments are removed!

#                 # add parameter & convert value if possible
#                 params[name] = valid_args( value )[0]
#                 num_read += 1

#     return params, num_read


# def text_write_params(text_file, param_vars, verbose=True):
#     """ Creates a text file w/ contents of all "PARAM = VALUE" pairs from 'param_vars'.

#     This function creates a simple text file w/ lines matching all entries of the key/value
#     pairs in 'param_vars' as "PARAM = VALUE". If 'text_file' already exists it will be wiped.

#     Args:
#         text_file (str): Filename of the text-file to which parameters are to be written.
#         param_vars (dict): Set of parameter variables to be written in the text file.
#         verbose (bool, optional): Switch for throwing warnings if necessary. Defaults to 'True'.

#     Returns:
#         num_written (int): Number of actually written parameter variables / lines.
#     """
#     fname = os.path.abspath(text_file)

#     # check if file exist
#     if (os.path.isfile(fname)):
#         if (verbose):
#             print("Warning: Removing existing file <{fname}>!")
#         os.remove(fname)

#     # write parameters to file
#     num_written = 0
#     with open(fname, mode='wt') as tf:
#         for PARAM in param_vars:
#             VALUE = param_vars[PARAM]
#             if ((expand_index_str(VALUE) is not None) or (type(VALUE) == str)):
#                 tf.write(f"{PARAM} = '{VALUE}'\n")
#             else:
#                 tf.write(f"{PARAM} = {VALUE}\n")
#             num_written += 1

#     return num_written


# def text_overwrite_params(text_file, param_vars, addon='', verbose=True):
#     """ Overwrites all matching parameter variables found in 'text_file'.

#     For all keys in 'param_vars', this function searches the corresponding line in the given
#     'text_file' and replaces it by setting the respective entry from 'param_vars'. The expected
#     format is thus: "PARAM = VALUE". If 'addon' is left empty (default), the original file is
#     lost in the process, i.e. backing up is the responsibility of the calling function! Note
#     that any kinds of whitespaces as well as line comments starting by '#' may also be contained
#     in the file.

#     Args:
#         text_file (str): Filename of the text-file in which parameters are to be overwritten.
#         param_vars (dict): Set of parameter variables to be replaced in the text file.
#         addon (str, optional): Addon to the filename of the new file. Defaults to ''.
#         verbose (bool, optional): Switch for throwing warnings if necessary. Defaults to 'True'.

#     Returns:
#         fname_new (str): Filename of "new" (or overwritten) text file.
#         num_written (int): Number of actually written parameter variables.
#     """
#     fname = os.path.abspath(text_file)

#     # prepare new file (or "fake" second I/O stream for operation)
#     if (addon != ''):
#         fname_new = fname+addon
#     else:
#         fname_new = fname+'~'
#     if (os.path.isfile(fname_new)):
#         if (verbose):
#             print("Warning: Removing existing file <{fname_new}>!")
#         os.remove(fname_new)

#     # over-write (matching) text parameters
#     num_written = 0
#     with open(fname, mode='rt') as orig:
#         with open(fname_new, mode='wt') as mod:

#             for line in orig:
#                 found = False

#                 # search & modify respective line...
#                 for p in param_vars.keys():
#                     PARAM = f"{p.upper()}"
#                     if (line.startswith(PARAM)):
#                         VALUE = param_vars[p]
#                         if ((expand_index_str(VALUE) is not None) or (type(VALUE) == str)):
#                             mod.write(f"{PARAM} = '{VALUE}'\n")
#                         else:
#                             mod.write(f"{PARAM} = {VALUE}\n")
#                         found = True
#                         num_written += 1
#                         param_vars.pop(p) # reduce search space (for next 'line')
#                         break

#                 # ...or replicate original one
#                 if (not found):
#                     if (verbose):
#                         print(f"Warning: Parameter {PARAM} not found in file! (skipping)")
#                     mod.write(line)

#     # keep only "new" file
#     os.remove(fname)
#     shutil.copy2(fname_new, fname)

#     return fname_new, num_written
