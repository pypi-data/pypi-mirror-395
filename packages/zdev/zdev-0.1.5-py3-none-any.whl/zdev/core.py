"""
Development helpers for quick & easy handling of regular tasks
"""
import os
import re
import csv
import sys
import time
import shutil
import numpy as np
import inspect
import datetime as dt
import importlib
import sounddevice as sd
from functools import partial

from zdev.colors import *
from zdev.indexing import file_goto
from zdev.searchstr import S_IDENT_W_DOT_HYP, S_DOC_STR_QUOTES
from zdev.validio import valid_encoding


# EXPORTED DATA
DEP_FILE_TYPES = ('.py', '.pyw') # file types to include for dependency search
DEP_PKG_TYPES = ('builtin', 'known', 'user')  # categories for sorting dependencies
DEP_PKG_BUILTIN = [ # definition of "builtin" packages -> sorted acc. to # chars
    'io', 'os', 're',
    'csv', 'sys',
    'json', 'math', 'stat', 'time', 'uuid',
    #5
    'base64', 'ctypes', 'pickle', 'shutil', 'typing',
    'asyncio', 'inspect', 'logging', 'zipfile',
    'datetime', 'requests', 'winsound',
    'functools', 'importlib', 'itertools', 'threading',    
    'concurrent', 'statistics', 'subprocess', 
    #11
    'configparser',
    #12, #13, #14,
    'multiprocessing',
    #16
    #specials:
    '__future__'
    ]
DEP_PKG_KNOWN = [ # definition of "known" packages -> sorted acc. to # chars
    #2
    'PIL', # pip -> pillow
    'dash', 'h5py',
    'flask', 'numpy', 'pydub', 'PyQt5', 'scipy', 'typer',
    'pandas', 'plotly', 'psutil',
    'pyarrow', 'skimage', # pip -> scikit-image
    'openpyxl', 'psycopg2', 'pydantic', 'tifffile', 
    'soundfile', 'streamlit',
    'matplotlib',
    'sounddevice',
    #12 #13 #14
    'influxdb_client',
    #16
    ]

# INTERNAL PARAMETERS & DEFAULTS
_REQ_FILE = 'requirements.txt'
_DEP_FILE = 'requirements_dependencies.txt'
# regex patterns
_RX_IMPORT = re.compile(r'(?P<tag>import )(?P<module>'+S_IDENT_W_DOT_HYP+r')')
_RX_IMPORT_FROM = re.compile(r'(?P<tag1>from )(?P<module>'+S_IDENT_W_DOT_HYP+r')(?P<tag2> import )')
_RX_WHITESPACE = re.compile(r'\s*')
_RX_QUOTES = re.compile(r'["\']')


def howmany(obj):
    """ Returns number of references inherent to PyObject 'obj' in CPython memory. """
    return sys.getrefcount(obj)


def isint(x, check_all=False):
    """ Returns an 'any-integer-type' indication (also works for arrays). """
    try:
        len(x)
        x = x[0]
    except:
        x
    finally:
        if (type(x) in (int, np.int64, np.int32, np.int16, np.int8)):
            return True
        else:
            return False


def isfloat(x):
    """ Returns an 'any-float-type' indication (also works for arrays). """
    try:
        len(x)
        x = x[0]
    except:
        x
    finally:
        if (type(x) in (float, np.float64, np.float32, np.float16)):
            return True
        else:
            return False


def iscomplex(x):
    """ Returns an 'any-complex-type' indication (also works for arrays). """
    try:
        len(x)
        x = x[0]
    except:
        x
    finally:
        if (type(x) in (complex, np.complex128, np.complex64)):
            return True
        else:
            return False
        

def anyfile(path, base, formats):
    """ Checks if folder 'path' contains a file 'base' in *any* of the acceptable 'formats'.

    Args:
        path (str): Folder location in which to look for files.
        base (str): Base of the filename to which the format/extension will be appended.
        formats (list of str): List of known formats to probe for. In order to robustify this
            helper function, leading '.' (if present) are automatically dealt with.

    Returns:
        fname_existing (str): Full filename of the 1st existing file that matched the
            combination of 'base' + a format from the list.
    """
    if (type(formats) is str):
        formats = [formats]
    for fmt in formats:
        if (fmt.startswith('.')):
            fmt = fmt[1:]
        fname_existing = os.path.join(path, base+'.'+fmt)
        if (os.path.isfile(fname_existing)):
            return fname_existing
    # Note: The same job is done by the following - using abbreviations ;)
    # [ os.path.join(p,b+'.'+f) for f in fmts if (os.path.isfile(os.path.join(p,b+'.'+f))) ][0]
    return None


def fileparts(the_file, relative=False):
    """ Returns path, filename and extension (mimic MATLAB function). """    
    fpath, fname, fext = None, None, None
    if (not relative):
        full_name = os.path.abspath(the_file)
    else:
        full_name = the_file
    if (os.path.isdir(full_name)):
        fpath = full_name
    else:
        fpath = os.path.dirname(full_name)
        filename = os.path.basename(full_name)
        tmp = filename.split('.')[:]    
        if (len(tmp) == 1):
            fname = tmp[0] # Note: 'the_file' was a mere string!
        else: # ...otherwise, ensure any '.' are kept & only last one is seen as extension!
            fname = '.'.join(tmp[:-1])
            fext = tmp[-1]
    return os.path.normpath(fpath), fname, fext


def local_val(x, k, width, mode='avg'):
    """ Computes a local quantity of 'x' around index 'k' with 'width'.

    Args:
        x (list or np.array): Array of samples for which a "local" value should be computed.
        k (int): Current index within 'x' for which a "local" value should be computed.
        width (int): One-sided width of non-causal window around 'x[k]'.
        mode (str, optional): Filtering mode w/ options: 'avg'|'max'|'min'|'sum'|'median'.
            Defaults to 'avg' (= mean).

    Returns:
        val (float): Computed "local" quantity acc. to selected 'mode'.
    """

    # determine valid index range & gather local array
    nlo = max(0, k-width)
    nup = min(k+width, len(x)-1)
    tmp = [x[n] for n in range(nlo,nup+1)]

    # compute quantity
    if (mode == 'avg'):
        return np.mean(tmp)
    elif (mode == 'max'):
        return np.max(tmp)
    elif (mode == 'min'):
        return np.min(tmp)
    elif (mode == 'sum'):
        return np.sum(tmp)
    elif (mode == 'median'):
        return np.median(tmp)   
    else:
        raise NotImplementedError(f"Unknown quantity {mode}")


def filesize(bytes_, binary=True):
    """ Returns string w/ proper file size acc. to https://en.wikipedia.org/wiki/Byte

    Args:
        bytes_ (int): Number of bytes = file size.
        binary (bool, optional): Switch for having binary bases instead of decimal ones (i.e.
            calculating "MiB/GiB/..." instead of "MB/GB/..."). Defaults to 'True'.
    Returns:
        bytes_str (str): Proper string of the file size (to be inserted into text).
    """

    # init
    num_bytes = int(bytes_)
    unit = [ 'Bytes', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y' ]

    # select reference for computations
    if (binary):
        base = 1024
        addon = 'i'
    else:
        base = 1000
        addon = ''

    # create appropriate string representation
    if (num_bytes < base):
        bytes_str = f"{num_bytes} {unit[0]}"
    else:
        order = 0
        while (True):
            order += 1
            if (num_bytes < base**(order+1)):
                res = divmod(num_bytes, base**order)
                bytes_str = f"{res[0]+res[1]/(base**order):.2f} {unit[order]}{addon}B"
                break
            if (order >= len(unit)):
                bytes_str = "more_than_YiB"

    return bytes_str


def storage(payload, num_days=1, downsample=0):
    """ Computes required number of bytes to store 'payload' for a given reference interval.

    The "payload" structure may refer to a set of monitoring data for CBM (condition-based
    maintenance) purposes and is given as dict indicating the number of recorded signals for
    each data type and acquisition rate. In addition, a 'downsample' step can be specified to
    move all signals from their original rate by this amount of intervals w/ lower acquisition
    rate. In this way, a less densly-sampled or aggregated data set (e.g. for more "historic"
    phasess in the past) can be modeled & computed.

    Args:
        payload (dict): Payload of different data types, sampled at different rates.
            Available rates are 'ms'|'sec'|'min'|'hour'|'day'.
            Available dtypes are 'bit'|'byte'|'short'|'int'|'float'|'long'|'double'.
        num_days (int, optional): Reference interval for computations. Defaults to 1 day.
        downsample (int, optional): If desired, specifies the number of sampling intervals to
            shift data acquisition frequency (for all entries). Defaults to 0.

    Returns:
        num_bytes (int): Total number of bytes required for 'payload' within 'num_days'.

    Examples: The following illustrates the computation for a given payload. If desired, the
        result may be converted to a string by using "filesize_str(num_bytes, binary=True)".

        payload = { 'byte':  {'sec': 75, 'min': 250, 'hour': 2000},
                    'int':   {'min': 150, 'hour': 800},
                    'double': {'min': 30, 'hour': 200, 'day': 500} }

        (default, per day)       --> num_bytes =   8216800 ~ 7.84 MiB
        (default, per year)     --> num_bytes = 2999132000 ~ 2.79 GiB
        (downsample=1, per day)  --> num_bytes =    144960 ~ 141.56 KiB
        (downsample=1, per month) --> num_bytes =  52910400 ~ 4.15 MiB

        Note: Since the daily rates for the 'double' data could not be further reduced, the
        latter two examples correspond to the following modified payload:

        payload_downsampled = { 'byte':  {'min': 75, 'hour': 250, 'day': 2000},
                                'int':   {'hour': 150, 'day': 800},
                                'double': {'hour': 30, 'day': 700} }
    """

    # internal settings (all values refer to a daily perspective)
    _RATE = { # 'CCS': 25*1000*60*60*24, # "CCS rate" ~ 40usec (1/(512*f0) == 39.625 us @ 50 Hz)
              'ms':   1000*60*60*24,
              'sec':  60*60*24,
              'min':  60*24,
              'hour': 24,
              'day':   1 }
    _TIMEBASE = list( _RATE.keys() )
    _SIZEOF = { 'double': 8, 'float': 4,
                'long': 8, 'int': 4, 'short': 2,
                'byte': 1, 'bit': (1/8) }
    # Note: A 'bit' is treated separately since it can be "stacked" (i.e. 1 byte = 8 bits)!

    # parse payload & compute daily storage
    all_data = 0
    for dtype in payload.keys():

        for rate in payload[dtype].keys():
            if (payload[dtype][rate] == 0): # ignore/skip empty fields
                continue

            # reduce frequency of data acquisition?
            aq = rate
            if (downsample):
                 idx = _TIMEBASE.index(rate) + downsample
                 if (idx < len(_TIMEBASE)):
                     aq = _TIMEBASE[idx]
                 else:
                     print(f"Warning: Could NOT reduce rate for data '{dtype}' @ '{rate}' (keeping original)")

            # compute storage
            if (dtype == 'bit'):
                req = np.ceil(payload[dtype][rate]*_SIZEOF['bit']) * _SIZEOF['byte'] * _RATE[aq]
            else:
                req = payload[dtype][rate] * _SIZEOF[dtype] * _RATE[aq]
            all_data += req

    # scale to reference interval
    num_bytes = all_data * num_days

    return num_bytes


def showtime(t_slow, t_fast, labels=['slow','fast'], show_factor=True, indent=None):
    """ Compares two processing durations (e.g. 'slow' Python vs. 'fast' C implementation). """

    # compute metrics
    speed_fac = t_slow / t_fast
    gain = 100.0 * (speed_fac-1.0)

    # configure formatting
    L = max([len(labels[0]), len(labels[1])])
    if (indent is not None):
        shift = " "*int(indent)
    else:
        shift = ""
    if (not show_factor):
        if (gain >= 0.0):
            qualifier = "faster"
        else:
            qualifier = "slower"

    # print comparison (speed factor or gain in %)
    if (indent is None):
        print("-"*64)
    print(f"{shift}{labels[0]:{L}} ~ {t_slow:.3e} sec")
    if (show_factor):
        print(f"{shift}{labels[1]:{L}} ~ {t_fast:.3e} sec  ==> speed factor ~ {speed_fac:.2f}")
    else:
        print(f"{shift}{labels[1]:{L}} ~ {t_fast:.3e} sec  ==> {qualifier} by {gain:.0f}%")
    if (indent is None):
        print("-"*64)

    return


def csv_splitter(path, sub_folders=None, split_lines=int(5e5), delete_orig=True, verbose=True):
    """ Parses all 'sub_folders' in 'path' for CSV-files and creates single files (if required).

    This helper may be used in order to make CSV-files created as database dumps more "usable",
    since text editors usually have a size limit for working w/ large files.

    Args:
        path (str): Location of main folder, i.e. where to start the search for CSV-files.
        sub_folders (list of str): Names of all sub-folders to search for CSV-files. Defaults to
            'None', i.e. all subfolders will be traversed.
        split_lines (int, optional): Number of lines after which the CSV-files will be split
            into "parts" , i.e. separate CSV-files with endings "_ptN.csv" (where N indicates a
            running index). Defaults to 500000.
        delete_orig (bool, optional): Switch to remove original (large) CSV-file after
            successful spliting. Defaults to 'True'.
        verbose (bool optional): Switch to show progress information on traversed folders/files.
            Defaults to 'True'.

    Returns:
        --
    """
    back = os.getcwd()
    os.chdir(path)

    # collect available subfolders
    if (sub_folders is None):
        sub_folders = []
        for item in os.listdir(os.getcwd()):
            if (os.path.isdir(item)):
                sub_folders.append(item)

    print(sub_folders)
    print(path)

    # parse all folders
    for sub in sub_folders:
        path_sub = os.path.join(path, sub)
        print(path_sub)
        if (not os.path.isdir(path_sub)):
            continue # skip non-existing folders
        elif (verbose):
            print(f"o Sub-folder '{sub}'")

        # parse all files
        for fname in os.listdir(path_sub):
            if ((not fname.endswith('csv')) or (re.search('_pt[0-9]*.csv', fname) is not None)):
                continue # skip non-CSV files or files that have already been split
            else:
                if (verbose):
                    print(f"  - File: '{fname}'")
                csv_file = os.path.join(path_sub, fname)
                enc = valid_encoding(csv_file)

                # read CSV-file in proper encoding
                with open(csv_file, mode='r', encoding=enc) as tf:

                    # parse format & configuration
                    first_line = tf.readline()
                    tf_format = csv.Sniffer().sniff(first_line)
                    fields = first_line.split(tf_format.delimiter)
                    for n, item in enumerate(fields):
                        fields[n] = item.strip() # clean whitespaces (incl. newline)

                    # if (num_header_lines > 2): #todo: have this as another argument?
                    #     #
                    #     #todo: get also "second_line = tf.readline()"
                    #     #         --> see "ts_import_csv" with "meta = xtools"

                    # create header line
                    line_header = ''
                    for item in fields:
                        line_header += f'{item}{tf_format.delimiter}'
                    line_header = line_header[:-1]+'\n'

                    # copy data of all time-series from file...
                    lines_for_next_split = []
                    num_lines, num_splits = 0, 0
                    m = 1
                    while (True):
                        try:
                            line = tf.readline()
                            if (line == ''): # regular break condition
                                raise

                            # export split file?
                            lines_for_next_split.append(line)
                            if (m == split_lines):
                                num_lines += m
                                num_splits += 1
                                with open(os.path.abspath(csv_file[:-4]+f'_pt{num_splits}.csv'), mode='wt') as sf:
                                    sf.write(line_header)
                                    sf.writelines(lines_for_next_split)
                                # reset
                                lines_for_next_split = []
                                m = 1
                            else:
                                m += 1
                        except:
                            break

                    # write last file (w/ remaining lines)
                    if (num_splits):
                        num_splits += 1
                        with open(os.path.abspath(csv_file[:-4]+f'_pt{num_splits}.csv'), mode='wt') as sf:
                            sf.write(line_header)
                            sf.writelines(lines_for_next_split)
                        if (verbose):
                            print(f"    (split into {num_splits} files)")
                    else:
                        if (verbose):
                            print(f"    (no split necessary, only {m} lines)")

                # remove original file? (only in case of splitting!)
                if ((num_splits >= 1) and delete_orig):
                     os.remove(csv_file)

    return


def massfileop(root, pattern, mode='count', params=[], max_depth=99, dry=True, verbose=0):
    """ Performs mass file operations in 'root' using 'pattern' in a certain 'mode'.

    Args:
        root (str): Base location where to start traversing all subfolders for 'pattern'. Note
            that this requires intermediate and trailing '\\' (e.g. 'C:\\Windows\\').
        pattern (str): Filename or regex pattern to be used for operation.
        mode (str): Operation to be applied to all files matching the search pattern.
            Available options are:
                'count':    simply counts the number of matches (will overwrite 'verbose=0')
                'chmod':    change file's attributes (i.e. read/write permissions)
                'stamp':    update file's time information by "touching" it
                'remove':   delete all matched files (CAUTION: "Dry" run is highly recommended!)
                'rename':   rename filenames of matches acc. to specification in 'params'
                'replace':  replace text in files acc. to specification in 'params'
        params (2-tuple): Additional parameters required, depending on mode of operation, i.e.
                if 'rename':    params = [ orig_fname_part, new_fname_part ]
                if 'replace':   params = [ orig_line_tag, new_line ]
            Defaults to '[]' (i.e. unused).
        max_depth (int, optional): Maximum level of subfolder search, Default to '99'.
        dry (bool, optional): Switch for performing a "dry run" w/o actual changes to the files.
            Defaults to 'True'.
            Note: This should always be used first for testing, such that no harm is done! For
            the more advanced file operations checks on feasibility will still become apparent.
        verbose (int, optional): Mode of status messages where '0 = off', '1 = files' and '2 =
            track all visited folders'. Defaults to '0'.

    Returns:
        result (int/list/None): Depends on 'mode' of operation. Will be an integer if 'count',
            a list of files if 'collect' and 'None' in all other cases.

    Examples: (make sure to set 'dry_run=True' to test first!)

        (1) Some typical use may be to get rid of all 'desktop.ini' files on Windows systems:
            >>> massfileop(r'C:\', 'desktop.ini', mode='remove', dry_run=True)

        (2) Replace parts of header/comment lines in all Python files of a project:
            >>> massfileop('C:\\MyProject', '\\.py', mode='replace', params=['#*old*','#*new*'])

        (3) Replace (parts of the) filename, but only for matching CSV-files:
            >>> massfileop('C:\\MyProject', '\\.csv', mode='rename',
                           params=['#*old*','#*new*'])
    """

    # init
    rx = re.compile(pattern)
    results = []
    num_found = 0
    num_modified = 0

    # feedback on progress
    if (verbose):
        print("-"*64)
        print("Starting MASS-FILE-OPERATION @ "+time.strftime("%H:%M:%S (%Y-%m-%d):"))
        print(f"Looking for '{pattern}' under <{root}>")
        print("")
        print(f"Applying operation '{mode}'...")
        print("")

    # traverse all folders under given root...
    for path, folders, files in os.walk(root): #[:-1]): # Note: remove trailing '\\'?

        path_ = path[:-1] + os.sep
        depth = path_[len(root):].count(os.sep)

        # ... as long as maximum depth is not yet reached...
        if (depth >= (max_depth+1)):
            if (verbose > 1): print(f"Skipping <{os.path.join(path)}> (MAX DEPTH reached!)")
            continue
        else:
            the_folder = os.path.join(path)
            if (verbose > 1): print(f"Entering <{the_folder}>")
            for fname in files:

                # step 1: check if file matches pattern
                if (rx.search(fname) is not None):
                    the_file = os.path.join(the_folder, fname)

                    # register file
                    num_found += 1
                    results.append( the_file )
                    if (verbose > 1): 
                        print(f"  -> Found '{fname}'")
                    elif (verbose):  
                        print(f"  -> Found '{the_file}'")

                    # step 2: (try to) apply selected file operation
                    # simple
                    if (mode in ('count','chmod','stamp','remove')):
                        if (not dry):
                            try:
                                if (mode == 'count'):
                                    pass # do nothing ;)
                                elif (mode == 'chmod'):
                                    os.chmod(the_file, params[0])
                                elif (mode == 'stamp'):
                                    mytime = dt.datetime.now().timestamp()
                                    os.utime(the_file, (mytime,mytime))
                                elif (mode == 'remove'):
                                    os.remove(the_file)
                                num_modified += 1
                            except:
                                print(f"Warning: Could NOT {mode} '{the_file}'!")
                        else:
                            pass # do nothing

                    # advanced (check feasibility)
                    elif (mode in ('rename','replace')):

                        if (mode == 'rename'):
                            try:
                                if (type(params[0]) is re.Pattern): # RegEx replacement
                                    str_old = params[0].search(fname).group()
                                    str_new = params[1]
                                    fname_re = re.sub(str_old, str_new, fname)
                                    # print(str_old, str_new, fname_re)
                                else: # assume simple string replacement
                                    fname_re = re.sub(params[0], params[1], fname)
                                if (fname_re != fname):
                                    if (not dry):
                                        shutil.move(the_file, os.path.join(the_folder,fname_re))
                                        num_modified += 1
                            except:
                                print(f"     Warning: Could NOT {mode} '{the_file}'!")

                        elif (mode == 'replace'):

                            #
                            # TODO: apply 'dry_run' scheme for feasibility testing!
                            #

                            if (not dry):
                                with open(the_file, mode='rt+') as tf:
                                    pos = file_goto(tf, params[0], mode='tag', nextline=False)
                                    if (pos is not None):
                                        tf.seek(pos[0]-1, 0) # -1 / otherwise 1st char is eaten
                                        #time.sleep(0.100)
                                        print(f"tell = {tf.tell()}")
                                        text = tf.readlines()
                                        # breakpoint()
                                        # text[0] = params[1]+'\n'
                                        tmp = text[0]
                                        print(f"pos = {pos} // found tmp as: {tmp}")
                                        text[0] = re.sub(params[0], params[1], tmp)
                                        print(f" --> now it is: {text[0]}")
                                        tf.seek(pos[0], 0)
                                        tf.writelines(text)
                                        num_modified += 1
                            else:
                                pass # do nothing

    # print short summary
    if (verbose):
        print("")
        print(f"Found {num_found} files")
        print(f"Modified {num_modified} files")
        print("-"*64)

    return results


def dependencies(root, excludes=['venv',], trace_level=2, save_req=True, with_version=True,
                 save_analysis=True, list_imports=False, verbose=False):
    """ Lists all dependencies required for files in a given 'root' folder.

    Args:
        root (str): Base location for dependency search (e.g project folder).
        excludes (list, optional): Subfolders in root that should be excluded from the search
            (if any). Defaults to 'venv'.        
        trace_level (int, optional): Control for adding a list of all "requesting files" 
            associated w/ each dependency and to set the number of analysis levels w/ options:
                0 = disable tracking (i.e. no indication w.r.t. origin of requirements)
                1 = only direct tracking
                2 = also analyse DIRECT dependencies of required files
                3 = also analyse INDIRECT dependencies of required files (i.e. "dep-of-dep")
                Defaults to '2'.        
        save_req (bool, optional): Switch for saving 'requirements.txt' for a batch install by
            "pip" (e.g. 'pip install -r %FILE%' or via a FOR-loop). Defaults to 'True'.
        with_version (bool, optional): Switch for adding versions to all required packages.
            Note that this will be in compatibility mode, i.e. using '~=". Defaults to 'True'.
        save_analysis (bool, optional): Switch for saving the whole in-depth dependency analysis
            to 'requirements_dependencies.txt'. Defaults to 'True'.
        list_imports (bool, optional): Switch for extracting a list of all import statements 
            in the source files. Defaults to 'False'.        
        verbose (bool, optional): Switch for status messages on the search. Defaults to 'False'.

    Returns:
        D (dict): Dict with keys from '_DEP_PKG_TYPES' (+ pkg) as well as 'imports' and 'tracing'.
            Note that the latter will only be populated if tracing is activated.
    """

    # init
    root_norm = os.path.normpath(root)
    project_path, project_name, _ = fileparts(root_norm)
    if (project_name is None):
        project = os.path.basename(project_path)
    else:
        project = project_name    
    D = {}
    
    if (verbose):
        print("-"*64)
        print(f"Starting DEPENDENCY analysis for <{project}>...")
        print("")

    # traverse all folders & files in project
    num_folders, num_files = 0, 0
    for path, _, files in os.walk(root_norm):
        path_norm = os.path.normpath(path)
        sub = path_norm.replace(root_norm+os.path.sep, '')

        # respect excludes
        checks = [sub.startswith(tree) for tree in excludes]
        if (any(checks)):
            if (verbose): print(f"o Excluded <{sub}>")
            continue
        else:
            if (verbose): print(f"o Traversing FOLDER <{sub}>")
            num_folders += 1

        # check all relevant files
        for fname in files:
            if (fname.endswith(DEP_FILE_TYPES)):
                full_file = os.path.abspath(os.path.join(path_norm, fname))
                if (verbose): print(f"  + Checking files '{fname}'")
                D = dep_of_file(D, full_file, (trace_level>=1), list_imports, verbose=False)
    
    # trace recursively to 2nd level (= DIRECT dependencies of required files)
    if (trace_level >= 2): 
        if (verbose): 
            print("")
            print(f"o Tracing back to 2nd level...")
        
        # analyse by (temporary) import of direct dependency files
        D2 = {}
        for n, dep_file in enumerate(D['user']):
            if (verbose): print(f"  - Back-tracking own dependencies of '{dep_file}'")
            try:
                the_module = importlib.import_module(dep_file)
                the_file = inspect.getsourcefile(the_module)
                dep_of_file(D2, the_file, False, False, False)
                del the_module
            except: 
                pass #fixme: what to do?
        
        # merge dependencies (i.e. consider *only* additional modules!)
        D['user_L2'] = D2['user']
        for dep in D2['user']:
            if (dep not in D['user']):
                D['user'].append(dep)
            else:
                D['user_L2'].remove(dep)
        del D2        

    # 3rd level = INDIRECT dependencies of required files
    if (trace_level >= 3): 
        if (verbose): 
            print("")
            print(f"o Tracing back to 3rd level...")
        
        # further analyse by (temporary) import of indirect dependency files
        D3 = {}
        for n, dep_file in enumerate(D['user_L2']):
            if (verbose): print(f"  - Back-tracking own dependencies of '{dep_file}'")
            try:
                the_module = importlib.import_module(dep_file)
                the_file = inspect.getsourcefile(the_module)
                dep_of_file(D3, the_file, False, False, False)                
                del the_module
            except:
                pass #fixme: what to do?

        # merge dependencies (i.e. only consider additional modules)
        D['user_L3'] = D3['user']
        for dep in D3['user']:
            if (dep not in D['user']):
                D['user'].append(dep)
            else:
                D['user_L3'].remove(dep)
        del D3    

    # sort modules dependencies & identify packages
    D['builtin'].sort(key=lambda item: item.lower())
    for item in D['builtin']:
        pkg = item.split('.')[0]
        if (pkg not in D['builtin_pkg']): D['builtin_pkg'].append(pkg)
    D['known'].sort(key=lambda item: item.lower())
    for item in D['known']:
        pkg = item.split('.')[0]
        if (pkg not in D['known_pkg']): D['known_pkg'].append(pkg)
    D['user'].sort(key=lambda item: item.lower())
    for item in D['user']:
        pkg = item.split('.')[0]
        if (pkg not in D['user_pkg']): D['user_pkg'].append(pkg)

    # sort import lists and traceback (if any)
    chk = dict(sorted(D['imports'].items(), key=lambda item: item[0].lower()))
    D['imports'] = chk
    for item in D['imports']:
        if (type(item) is list): item.sort(key=lambda item: item.lower())

    chk = dict(sorted(D['tracing'].items(), key=lambda item: item[0].lower()))
    D['tracing'] = chk
    for item in D['tracing']:
        if (type(item) is list): item.sort(key=lambda item: item.lower())
    
    # print summary
    if (verbose):
        print("")
        print("...finished DEPENDENCY analysis!")
        print("")
        print(f"{len(D['builtin'])} BUILTIN modules from {len(D['builtin_pkg'])} packages required:")
        print(f"{D['builtin']}")
        print("")
        print(f"{len(D['known'])} KNOWN modules from {len(D['known_pkg'])} packages required:")
        print(f"{D['known']}")
        print("")
        print(f"{len(D['user'])} USER modules from {len(D['user_pkg'])} packages required:")
        print(f"{D['user']}")
        print("-"*64)

    # save dependency analysis infos to file?
    if (save_analysis):
        with open(os.path.join(project_path, _DEP_FILE), mode='wt') as df:
            df.write("================================================================================\n")
            df.write(f"DEPENDENCY Analysis for <{project}> @ {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            df.write("================================================================================\n")
            df.write("\n")
            df.write("--------------------------------------------------------------------------------\n")
            df.write("SUMMARY:\n")
            df.write(f" o Searched in {num_folders} folders / {num_files} files\n")
            df.write(f" o Found {len(D['builtin'])} builtin modules from {len(D['builtin_pkg'])} packages\n")
            df.write(f" o Found {len(D['known'])} known modules from {len(D['known_pkg'])} packages\n")
            df.write(f" o Found {len(D['user'])} user modules from {len(D['user_pkg'])} packages\n")
            df.write("--------------------------------------------------------------------------------\n")
            df.write("\n")
            df.write("---- BUILTIN modules ------------\n")
            df.write("\n")
            for item in D['builtin']:
                df.write(f"+ {item}\n")
            df.write("\n")
            df.write("---- KNOWN modules --------------\n")
            df.write("\n")
            for item in D['known']:
                df.write(f"+ {item}\n")
            df.write("\n")
            df.write("---- USER modules ---------------\n")
            df.write("\n")
            for item in D['user']:
                df.write(f"+ {item}\n")
            df.write("\n\n\n")
            if (list_imports):
                df.write("--------------------------------------------------------------------------------\n")
                df.write("---- LIST OF IMPORTS (by each source file) -------------------------------------\n")
                df.write("--------------------------------------------------------------------------------\n")               
                for src_file in D['imports']:
                    df.write("\n")
                    df.write(f"<{src_file}>\n")
                    for idx in range(len(D['imports'][src_file])):

                        df.write(f"    #{D['imports'][src_file][idx][1]:-4d}: {D['imports'][src_file][idx][0]}\n")
            else:
                df.write("NO LISTING of imports (from each source file) has been performed.\n")
            df.write("\n\n\n")
            if (trace_level):
                df.write("--------------------------------------------------------------------------------\n")
                df.write(f"---- TRACE-BACK OF DEPENDENCIES (for each requirement, level = {trace_level}) ------------\n")
                df.write("--------------------------------------------------------------------------------\n")
                # Note: i.e. which module/package is required and imported by which source file?
                for dep_file in D['tracing']:
                    df.write("\n")
                    df.write(f"<{dep_file}>\n")
                    for idx in range(len(D['tracing'][dep_file])):
                        df.write(f"    {D['tracing'][dep_file][idx][0]} @ {D['tracing'][dep_file][idx][1]}\n")
            else:
                df.write("NO BACK-TRACING of dependencies (as required by source files) has been performed.\n")
            df.write("\n")

    # store list of package requirements? (e.g. for batch install in virtual environments)
    if (save_req):
        with open(os.path.join(project_path, _REQ_FILE), mode='wt') as rf:
            for req in D['known_pkg']:
                rf.write(f"{req}")
                if (with_version):
                    try:
                        xyz = eval(f"__import__('{req}')")
                        rf.write(f"~={xyz.__version__}")
                        del xyz
                    except:
                        pass                
                rf.write(f"\n")    
    return D


def dep_of_file(D, src_file, trace_back=True, list_imports=False, verbose=False):
    """ Extends container 'D' by all dependencies of 'src_file'.

    This function represents the core analysis routine of for dependencies of Python files.
    Since the container will create all mandatory keys automatically it can be initialised as
    'D = {}' such that this routine can be used for a quick investigation of single source 
    files. See 'dependencies' for more information.

    Args:
        D (dict): Initial container w/ previously collected dependencies (if any).
        src_file (str): Python file to be analysed for its dependencies.
        trace_back (bool, optional): Switch to list the "requesting" files for all dependencies.
            Defaults to 'True'.
        list_imports (bool, optional): Switch for extracting a list of all import statements 
            in the source files. Defaults to 'False'.       
        verbose (bool, optional): Switch for status messages on the search. Defaults to 'False'.

    Returns:
        D (dict): Updated container w/ requirements.    
    """

    # ensure dict keys are already existing
    for key in DEP_PKG_TYPES:
        key2 = f'{key}_pkg'
        if key not in D.keys(): D[key] = []
        if key2 not in D.keys(): D[key2] = [] 
    for key in ('imports', 'tracing'):
        if key not in D.keys():
            D[key] = {}

    if (verbose):
        print("Analysing dependencies of file {src_file}")

    # analyse file & add (new) dependencies
    _, fname, __ = fileparts(src_file)
    with open(src_file, mode='rt') as sf:
        inside_doc_string = False

        for n, line in enumerate(sf.readlines(), start=1):

            # determine indentation level
            indent_level = 0
            whitespace = _RX_WHITESPACE.match(line)
            if (whitespace): indent_level = int(whitespace.end()/4)

            line = line.strip()
            
            # handle & skip doc-strings
            chkdoc = line.split(S_DOC_STR_QUOTES)
            if (chkdoc[0] != line):
                if (not inside_doc_string) and (len(chkdoc) == 2):
                    inside_doc_string = True # entering...
                    if (verbose):
                         print("line #{n:-4d}: entering DOC-string...")
                elif (inside_doc_string):
                    inside_doc_string = False # ...leaving  
                    if (verbose):
                         print("line #{n:-4d}: ...leaving DOC-string")
                # Note: If doc-string is entered & left on the same line, len(chkdoc) would
                # be > 2 and therefore passed on as well.
            if (inside_doc_string):
                continue # w/ next line

            # handle comments
            if (line.find('#') >= 0):
                line = line.split('#')[0] # Note: Comment might be only after some code?
                
            # check for dependency
            dep_type = None
            if (not indent_level): # @ top level
                if (not dep_type):
                    chk = _RX_IMPORT_FROM.match(line)
                    if (chk): dep_type = 'from_import'
                if (not dep_type):
                    chk = _RX_IMPORT.match(line)
                    if (chk): dep_type = 'import'
            else: # @ function/class definitions
                if (not dep_type):
                    chk = _RX_IMPORT_FROM.search(line)
                    if (chk): dep_type = 'from_import_in_func'
                if (not dep_type):
                    chk = _RX_IMPORT.search(line)
                    if (chk): dep_type = 'import_in_func'

            if (not dep_type): 
                continue # w/ next line

            # discard hit if it is within another string!
            before = line[:chk.span()[0]]
            after = line[chk.span()[1]:]
            if (_RX_QUOTES.search(before)):
                if (verbose):   
                    print(f"line #{n:-4d}: discarding hit! (since it is *within* a string expression)")
                continue

            # record new dependency
            mod_name = chk.groupdict()['module']
            pkg_name = mod_name.split('.')[0]
            # pkg_name = mod_name.split('.')[:-1] #fixme: how to deal w/ nested modules?
            
            if (pkg_name in DEP_PKG_BUILTIN):
                if (mod_name not in D['builtin']):
                    D['builtin'].append(mod_name)
            elif (pkg_name in DEP_PKG_KNOWN):
                if (mod_name not in D['known']):
                    D['known'].append(mod_name)
            elif (mod_name not in D['user']):
                D['user'].append(mod_name)

            # extract source file's import lists?
            if (list_imports):
                line_cleaned = line.split('#')[0].strip()
                if (fname not in  D['imports'].keys()):
                    D['imports'][fname] = [(line_cleaned, n),]
                else:
                    D['imports'][fname].append((line_cleaned, n))

            # add source file to list of module-requesting files?
            if (trace_back):
                if (mod_name not in D['tracing'].keys()):
                    D['tracing'][mod_name] = [(src_file, n),]
                else:
                    D['tracing'][mod_name].append((src_file, n))

            # print info about analysis progress
            if (verbose):
                if (dep_type == 'import'):
                    print(f"line #{n:-4d}: depends on module <{mod_name}>")
                elif (dep_type == 'from_import'):
                    print(f"line #{n:-4d}: depends on (parts of) module <{mod_name}>")
                elif (dep_type == 'import_in_func'):
                    print(f"line #{n:-4d}: some function depends on module <{mod_name}>")
                else: # (dep_type == 'from_import_in_func')
                    print(f"line #{n:-4d}: some function depends on (parts of) module <{mod_name}>")

    return D


def quickplay(x, fs=48000, dtype=np.int16, normalise=True, device='default'):
    """ Quickly plays 'x' as an audio signal.

    Args:
        x (array-type): Any array type, will be converted to 'ndarray'.
        fs (float, optional): Sampling rate for playback.
        normalise (bool, optional): Switch for normalising volume. Defaults to 'True'.
        device (str, optional): Playback device. Defaults to 'default'.

    Returns:
        --
    """

    if (type(x) is not np.ndarray):
        x = np.array(x)

    if (normalise):
        x_peak = np.max(np.abs(x))
        xn = x / x_peak
    else:
        xn = x

    if (dtype is None):
        dtype = xn.dtype
        xs = xn
    elif (dtype == np.int16):
        xs = xn * 32767 # 16-bit signed integer
        xs = xs.astype(dtype)

    # PortAudio
    player = sd.OutputStream(samplerate=fs, channels=1, dtype=dtype)
    player.start()
    player.write(xs)

    return

qplay = partial(quickplay, device='default')
