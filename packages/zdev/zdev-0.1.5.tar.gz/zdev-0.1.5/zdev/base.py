"""
Basic initialization routines for a Python 3.8+ session
"""
import os
import sys
import json
import shutil
import inspect
import logging
import importlib

from zdev.core import dependencies
from zdev.validio import force_remove
from zdev.core import fileparts


# EXPORTED DATA
IMPORT_PATH = '__imports' # location of user packages/modules (in case of project deployment)
IMPORT_FOLDERS = [
    r'zdev',
    r'zynamon'
    r'dsap',
    r'refdb',
    r'remaster',
    ]


# INTERNAL PARAMETERS & DEFAULTS
_BASE = [
    r'T:\Python', # straight @ home
    r'C:\Users\z00176rb\OneDrive - Siemens Energy\Dev\Python', # NEW SE client @ work
    ]
_ENVIRONMENT = [
    r'ZDevTools',
    r'ZynAMon',
    r'DSAP',
    r'RefDB',
    ]
_DEP_TRACE_LEVEL = 3    # control analysis level of trace-back
_DEP_SET_FLAGS = False  # switch to set flag if module is contained in project folder


def init_logger(name):
    """ Configure a slim logger """
    logging.basicConfig(level=logging.INFO, format='[%(name)s] %(message)s')
    # Note: Set this to a HIGH level? -> otherwise, low-level lib funcs might be affected?!
    #       -> datefmt='%Y-%m-%d %H:%M:%S',
    #       -> format='%(asctime)s [%(levelname)-s] %(name)s : %(message)s',   
    return logging.getLogger(name)


def init_session(root, env=None, verbose=True):
    """ Init routine to set a 'sys.path' environment for a new Python 3.8+ session.

    This function provides initialisation for a new Python console (e.g. IPython in Spyder).
    As such, it may also be employed in a 'startup' file to make all required user-defined 
    modules known for a stand-alone use of a project deployed on any machine other than the
    development host. To this end, the 'root'+'env' folders will be inserted into 'sys.path'.
     
    Args:
        root (str or list): Base folder to be added to 'sys'path' and to act as root path of 
            the environment. If of type list, all entries are treated as potential candidates 
            but only the first one existing will be used. Note that this allows to 
            simultaneously work with different root folders (e.g. private & work machines).
        env (list, optional): List of additional environment folders that shall be appended to
            'sys.path' as combination of "root/env[n]". Defaults to 'None'.
        verbose (bool, optional): Switch to print initialisation progress. Defaults to 'True'.

    Returns:
        track (dict): Dict w/ keys 'root' and 'folders' to check on actual success.
    """
    
    # init
    LOG = init_logger('init-session')
    track = {'base': '', 'folders': []}

    # get proper base folder
    if (type(root) is str):
        base = root
    elif (type(root) is list):
        for base in root:
            if (os.path.isdir(base)):
                if (verbose): LOG.info(f"Using base <{base}>")
                break    
    else:
        raise TypeError(f"Unknown type of root folder") 
    track['base'] = base  

    # ...and add folders to beginning of path
    num_errors = 0
    if (env is not None):
        for n, item in enumerate(env, start=1):
            folder = os.path.join(base, item)
            if (os.path.isdir(folder)):
                if (folder not in sys.path):
                    sys.path.insert(n, folder)
                    if (verbose): LOG.info(f"Added <{folder}> to 'sys.path'")
                    track['folders'].append(folder)
                else:
                    if (verbose): LOG.info(f"Folder <{folder}> was already present in 'sys.path'")
            else:               
                if (verbose): LOG.info(f"Could not include <{folder}> in 'sys.path'")
                num_errors += 1

    # Note: Position '0' is always the current script path or '' in REPL, so add 'root' only at
    # the end in order to have it in position #1 ;)
    if (base not in sys.path):
        sys.path.insert(1, base)

    # completion
    if (num_errors):
        if (verbose): LOG.info(f"Finished w/ {num_errors} ERRORS (check above)")
    else:
        if (verbose): LOG.info(f"Finished SUCCESSFULLY! (ready for work)")
    return track


def project_deploy(folder, main_app=None, main_file=None):
    """ Prepares project in 'folder' for deployment (on another machine).

    This routine supports the process of "packaging" an application as stand-alone item for
    execution on *any other machine* (e.g. where no system Python is present). To this end, 
    all necessary user files are copied to the local 'IMPORT_PATH' and a 'startup.py' file is 
    created to enable a quick initialisation of this environment. If the entry point of the
    application is specified by 'main_app', another BAT-file is generated such that the whole 
    execution can be started in a "single-click manner"! :)

    Note: For more information on the complete deployment see 'auto_deploy.bat'.

    Args:
        folder (str): Location of the project containing all necessary files and sub-folders.
        main_app (str, optional): Application's main function call. Defaults to 'None'. 
        main_file (str, optional): Filename containing the 'main_app'. Defaults to 'None'.

    Returns:
        num_errors (int): Number of encountered errors (if any).
    """

    # step 0: set environment
    back = os.getcwd()
    os.chdir(folder)

    # step 1: create local import folder
    root = os.getcwd()
    dest = os.path.join(root, IMPORT_PATH)
    if (os.path.isdir(dest)):
        print(f"(1) Purging local folder <{dest}>")
        shutil.rmtree(dest, onexc=force_remove)
    else:
        print(f"(1) Creating local folder <{dest}>")
    os.mkdir(dest)

    # step 2: hide folders on development host (to simulate clean environment)
    print(f"(2) Preparing 'sys.path'")
    for item in IMPORT_FOLDERS:
        sub_folder = os.path.join(dest, item)
        if (sub_folder in sys.path):
            sys.path.remove(sub_folder)

    # step 3: check for dependencies in all project files
    print(f"(3) Analysing dependencies")
    dep = dependencies(root, excludes=['venv'], trace_level=_DEP_TRACE_LEVEL,
                       save_dep=(_DEP_TRACE_LEVEL>0), save_req=True, verbose=True)

    # step 4: locate & collect required user files 
    print(f"(4) Collecting non-standard modules (in local import folder)")
    num_errors = 0
    for module in dep['user']:
        print(f"    + locating '{module}'", end='')        

        # decompose pkg/module hierarchy & create sub-folders (if any)
        mod_parts = module.split('.')
        mod_path = os.path.join('', *mod_parts[:-1])
        mod_file = os.path.join(mod_path, mod_parts[-1]+'.py')
        if (not os.path.isdir(os.path.join(dest, mod_path))):
            os.makedirs(os.path.join(dest, mod_path))

        # locate module & copy into import folder
        module_found = False

        # (i) check if directly *within* project
        if (os.path.isfile(os.path.join(root, mod_file))):
            print(" -> in project", end='\n')
            module_found = True
            if (_DEP_SET_FLAGS):
                fh = open(os.path.join(dest, mod_file.strip('.py')+'_isinproject'), 'wt')
                fh.close()
            continue # w/ next module

        # (ii) check for installed packages
        if (not module_found):            
            for loc in sys.path:

                # probe for "editable" installs
                if (loc.endswith('site-packages')):
                    chk = [ item if os.path.isfile(os.path.join(loc, item, 'direct_url.json')) 
                                 else None
                            for item in os.listdir(loc)
                            if item.startswith(mod_parts[0]) ]
                    if (any(chk)):
                        with open(os.path.join(loc, chk[0], 'direct_url.json')) as jf:
                            dump = json.load(jf)
                            edit_root = dump['url'].strip('file:///')
                            src = os.path.join(edit_root, mod_file)
                        print(" -> editable install", end='\n')
                        shutil.copy(src, os.path.join(dest, mod_path))
                        module_found = True  
                        break 
                
                # probe for "normal install" (in *any* location)
                src = os.path.join(loc, mod_file)
                if (os.path.isfile(src)):
                    print(" -> normal install", end='\n')
                    shutil.copy(src, os.path.join(dest, mod_path))
                    module_found = True
                    break
                # Note: This option may also catch files that have been made available by 
                # extending the 'sys.path' to include other user directories as well...
        
        # (iii) finally try if 'import' works? -> if yes: then NO USER MODULE!!! (but "KNOWN", wtf?)
        if (not module_found):
            print(f" -> could NOT be found! (ERROR)", end='\n')
            num_errors += 1            
            try:
                importlib.import_module(module)
                print('\n'+"      (check: module can be imported, so *where* is it?!?)")
            except:
                print('\n'+"      (check: module *cannot* be imported!)")
    
    # cleanup empty folders (i.e. if 'in-project' modules)
    for item in os.listdir(dest):
        sub_folder = os.path.join(dest, item)
        if (os.path.isdir(sub_folder) and (not os.listdir(sub_folder))):
            shutil.rmtree(sub_folder)

    # step 5: create 'startup.py' file for project
    print("(5) Creating Python 'startup' file")
    project_startup_py(folder)

    # step 6: create BAT-file for "one-click" start?
    if (main_app is not None):
        print("(6) Creating BAT-file for ease-of-execution")
        project_startup_bat(folder, main_app, main_file, virtual=False)

    # complete & switch back to initial folder
    if (not num_errors):
        print(f"Finished SUCCESSFULLY (ready for work)") # ...or add a Python virtual env?
    else:
        print(f"Finished with {num_errors} ERRORS! (check above)")

    os.chdir(back)
    return num_errors


def project_startup_py(folder):
    """ Generate a 'startup.py' file in the project's 'folder' to correctly set all imports.

    Args:
        folder (str): Location of the project containing all necessary files and sub-folders.

    Returns:
        --
    """

    # get implementation of "init" function & set actual environment
    func_def = inspect.getsource(init_session)
    func_def = func_def.replace('(root,', '(root=os.path.dirname(__file__),')
    func_def = func_def.replace('env=None', f"env=['{IMPORT_PATH}']")
    
    # create startup file
    with open(os.path.join(folder, 'startup.py'), mode='wt') as sf:
        sf.write('"""\n')
        sf.write(f"Startup file for project '{os.path.normpath(folder).split(os.sep)[-1]}'\n")
        sf.write(f"This file has been *AUTO-GENERATED* and may be overwritten - DO NOT TOUCH!!\n")
        sf.write(f"For details see 'zdev.base.project_startup_py()'.\n")
        sf.write('"""\n')
        sf.write("import os\n")
        sf.write("import sys\n")
        sf.write("import logging\n")
        sf.write("\n")
        sf.writelines( inspect.getsource(init_logger) )
        sf.write("\n")
        sf.writelines( func_def )
        sf.write("\n")
        sf.write("#%% MAIN\n")
        sf.write("if (__name__ == '__main__'):\n")
        sf.write("    print('Initialising project...')\n")
        sf.write("    init_session()\n")
        sf.write("    print('...done - have phun! ;)')\n")
    return


def project_startup_bat(folder, main_app, main_file=None, virtual=False):
    """ Create a BAT-file for a "one-click-execution" at the project's entry point.

    Note that 'main_app' is expected to be a function definition that can be run w/o any 
    further arguments. This can be realised by e.g. resorting to reasonably set default 
    arguments. The created executable BAT-file will be named 'main_app_START.BAT'.
    
    Args:
        folder (str): Project's root folder.
        main_app (str): Function call as the application's entry point.
        main_file (str, optional): Filename containing the 'main_app'. If this is omitted, a
            source file 'main_app.py' is assumed. Defaults to 'None'.
        virtual (bool, optional): Switch to use a virtual environment to start from, otherwise
            a system Python is assumed. Defaults to 'False'. 

    Returns:
        --
    """

    # ensure proper input filename & path
    if (main_file):
        the_file = main_file
    else:
        the_file = main_app
    fpath, fname, _ = fileparts(the_file, relative=True)   
    if (fpath != '.'):
        app_module = os.path.join(fpath, fname)
        app_module = app_module.replace(os.sep, '.')
    else:
        app_module = fname

    # write batch file
    bat_file = os.path.join(folder, fname+'_START.BAT')
    with open(bat_file, mode='wt') as bf:
        bf.write("@ECHO off\n")

        if (virtual): 
            str_start = r'CMD /k "venv\Scripts\activate & '
        else: 
            str_start = r'CMD /k "'        
        
        str_call = f"from startup import *; init_session(); from {app_module} import {main_app}; {main_app}();"

        if (virtual): 
            str_stop = r' & deactivate"'    
        else: 
            str_stop = r' "'

        bf.write(str_start + 'PY -c "' + str_call + '"' + str_stop + '\n')
        bf.write("PAUSE\n")

    return



#===============================================================================================
#===============================================================================================
#===============================================================================================

# #%% MAIN
# if (__name__ == "__main__"):
#     print("Initialising Python...")
#     init_session(root=BASE, env=ENVIRONMENT)
#     from zdev import * # make default package accessible
#     #from zdev.core import *
#     print("...done - have phun! ;)")