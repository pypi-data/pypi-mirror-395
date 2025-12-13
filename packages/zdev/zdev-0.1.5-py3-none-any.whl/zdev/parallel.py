
"""
Routines for convenient handling of (multi-core) parallel processing

As preferred option, the function 'parallel_processing()' serves as a convenience function to 
Python's standard routines from the 'multiprocessing' package and its 'Pool()' method. It 
provides improved feedback through several "progress bar" implementations (class 'Progress'). 
As 2nd option, even more control over the concurrent execution of processes is achieved when 
using a driving timer object (class 'TimerCycle') to periodically check for the remaining 
workload to be executed (managed by class 'Dispatcher'). In this way, each job is exactly 
assigned to one of the CPU cores in the allowed range.
"""
import os
import time
import psutil
import shutil
import logging
import threading
import subprocess
import multiprocessing


# INTERNAL PARAMETERS & DEFAULTS
_BASE_DIR = os.path.join('C:\\Users', os.getenv('USERNAME'), '_X_') # Note: Assuming Windows OS!
_CPU_MARGIN = 2             # number of CPUs *NOT* to be used (in order to keep responsiveness!)
_POLLING_CYCLE = 0.200      # duration [s] between two polling events
_PROGRESS_CYCLE = 3.000     # duration [s] before display is updated (unless in 'bar' mode!)
_PROGRESS_MODE = 'ETA'      # default progess mode ('bar'|'pulse'|'ETA'|:any_char:)
_BAR_SYMBOL = '='           # symbol to be used in 'bar' mode
_BAR_LENGTH = 64            # length of progress bar (i.e. full length if 'bar', else per line)
_MAX_LIFETIME = 24*3600     # maximum runtime [s] before quitting the jobs (default)
_DEBUG = True               # switch [bool] to keep job completion reports in exchange folder


class Progress:
    """ Progress class w/ different modes for updating progress information. """    
   
    def __init__(self, num_total, mode='*', cycle=_PROGRESS_CYCLE):
        """ Initialises 'Progress' object w/ specified display 'mode'.
        
        This object gives information on the progress of any process that can be described by a 
        measured 'lifetime' and an integer counter of 'completed' operations (see ".update()").
        It directly prints out this progress, so it should be used in CLI/ASCII contexts.
        
        Args:
            num_total (int): Total number of jobs in the processing routine.
            mode (str, optional): Mode of display w/options 'bar'|'ETA'|'pulse'|:char:. See 
                examples below for explanation. Defaults to '*'. 
            cycle (float, optional): Duration [s] between two periodic display updates. This can
                be used to modify settings acc. to the average duration of the monitored
                operations. Defaults to '_PROGRESS_CYCLE'.
                Note: This setting is *not effective* if for the 'bar'! This will only update 
                after completion of each job.
                 
        Returns:
            --
            
        Examples for 'mode': 
            
            (i) Event-based updates:                
            'bar'   --> "[=========                ]"  
                    --> Completion bar w/ defined extents, increased after each completed job
            
            (ii) Cyclic updates:                
            'ETA'   --> "ETA ~ 19 mins 44 sec"
                    --> Estimated duration of remaining jobs, only works for ~ const workload
                    
            'pulse' --> "...processing... [14:32:15]"
                    --> Simple "heartbeat" / "still alive" indicator
            
            '*'     --> "************"
                    --> Progress bar w/ any 1-char symbol (unlimited length)            
        """
        self.mode = mode            # 'bar'|'ETA'|'pulse'|any 1-symbol char ('.' / '*' / etc.)
        self.cycle = cycle          # duration [s] between regular updates (if applicable)
        self.num_jobs = num_total   # number of total jobs (for scaling)
        self.num_completed = 0      # number of completed tasks         
        self.lifetime = 0.0         # total lifetime [s] of processing        
        self.estimate = -1          # estimated for remaining time (if applicable)        
        self.bar = 0                # length of progress bar (if applicable)
        return
        
    
    def update(self, lifetime, completed):
        """ Prints regular output, either according to cycle or due to completion. 
        
        Args:
            lifetime (float): Measured time since start of running process.
            completed (int): Counter indicating the total number of completed operations.
            
        Returns:
            --      
        """
         
        # simple mode with "0-100% bar"
        if (self.mode == 'bar'):            
            print("\r", end='', flush=True)            
            now = int(float(completed)/float(self.num_jobs) * _BAR_LENGTH)
            msg = '['+_BAR_SYMBOL*now+' '*(_BAR_LENGTH-now)+']'
            print(msg, end='', flush=True)
            if (now >= _BAR_LENGTH):
                print("", flush=True)
            
        else: # advanced mode with cyclic display
            
            # regular update (if no new completions)
            if (completed == self.num_completed):
                time_passed = lifetime - self.lifetime
                if (time_passed < self.cycle):
                    return # not yet... ;)
                else:                    
                    if (self.mode.upper() == 'ETA'):
                        if (self.estimate > 0):
                            message = f"ETA ~ {duration_str(max(self.estimate-lifetime,0))}"
                        else:
                            message = "ETA - no sufficient data (waiting for completions)"
                        print("\r"+message, end='', flush=True) # in-place update
                    elif (self.mode == 'pulse'):
                        message = time.strftime("...processing... [%H:%M:%S]")
                        print("\r"+message, end='', flush=True)
                    else:
                        print(self.mode, end='', flush=True)
                        if (self.bar%_BAR_LENGTH == _BAR_LENGTH-1): 
                            print("", flush=True)
                        self.bar += 1
                
            # update due to process completion
            else:           
                if (self.mode.upper() == 'ETA'):
                    self.estimate = lifetime * (self.num_jobs/completed) # FIXME: use averaging?
                elif (self.mode == 'pulse'):
                    pass     
                else:
                    self.bar = 0            
                message = f"{completed} / {self.num_jobs} jobs completed --> [{100.*(completed/self.num_jobs):3.1f}%]"
                print("\r"+message, end='\n', flush=True)
            
        # update internals
        self.lifetime = lifetime
        self.num_completed = completed
        
        return
    
    
    def close(self):
        """ Closes 'Progress' object. """
        # print("")
        return


#-----------------------------------------------------------------------------------------------


class Dispatcher:
    """ Setup & management of multi-job dispatch. """    
    
    def __init__(self, N, func, param_args, param_kwargs, env=None, prog_mode=None,
                 prog_cycle=_PROGRESS_CYCLE):
        """ Initialise job administration & work environment.

        At least one of the parameter variations (i.e. '_args' or 'kwargs') has to be a list w/
        length >= 2. The other variations then either have to match this length (i.e. the number
        of variations) or have to be a single variant. In the latter case, these parameters are
        considered static and are thus "broadcasted" for all variations of the 1st list.
        
        Args:
            N (int): Number of "workers" used for dispatching.
            func (:obj:): Function to be called for each job.
            param_args (list of lists): Parameter variations by positional args. This reflects 
                the total workload that is to be dispatched.
            param_kwargs (list of dicts): Parameter variations by kwargs. Again, this reflects 
                the actual workload.
            env (list, optional): List of string entries to be executed first in order to define
                the environment for the 'func' workers. Defaults to 'None'.
            prog_mode (str, optional): Display mode provided by class 'Progress' (see details).
                Defaults to 'None' (i.e. only dispatches are protocolled). 
            prog_cycle (float, optional): Updating speed for display (if applicable, i.e. only 
                if 'mode' is not 'None'). Defaults to '_PROGRESS_CYCLE'.
            debug (bool, optional): 
                
        Returns:
            --
        """
        
        # determine number of CPU cores to be used
        N_avail = psutil.cpu_count() - _CPU_MARGIN
        self.N_workers = min(N, N_avail)
        
        # attributes
        self.base = _BASE_DIR
        self.env_str = ''
        self.num_jobs = -1
        self.num_jobs_left = 0
        self.num_dispatched = 0
        self.num_loaded = 0
        self.num_completed = 0
        self.time_started = time.perf_counter()
        self.time_alive = 0.0
        self.is_fully_dispatched = False
        self.is_fully_loaded = False
        
        # members
        self.func = func
        self.worker = []
        self.worker_state = []
        for th in range(self.N_workers):
            self.worker.append( {'sub': None, 'proc': None} )
            self.worker_state.append( 0 )
        self.progress = None
            
        print(f":::: Dispatcher w/ {self.N_workers} workers ::::")
        
        # configure workload (i.e. distribute parameter variations)  
        if (len(param_kwargs) < 2): # i.e. kwargs is either '{}' or single dict                
            self.workload_args = param_args
            self.workload_kwargs = []
            for var in range(len(self.workload_args)):
                self.workload_kwargs.append( param_kwargs[0] )
        elif (len(param_args) < 2): # i.e. args is either '[]' or single list                
            self.workload_kwargs = param_kwargs
            self.workload_args = []
            for var in range(len(self.workload_kwargs)):
                self.workload_args.append( param_args[0] )
        elif (len(param_args) == len(param_kwargs)):
            self.workload_args = param_args
            self.workload_kwargs = param_kwargs        
        else:
            print("Dispatch variations in 'args' & 'kwargs' do NOT match! (aborting)")
            return        
        self.num_jobs = len(self.workload_args)
        self.num_jobs_left = self.num_jobs        
            
        # reset exchange folder (i.e. ensure it exists & is empty)
        if (os.path.isdir(self.base)):
            shutil.rmtree(self.base)
            print("Purged exchange folder")            
        os.mkdir(self.base)
        print(f"Created exchange folder <{self.base}>")
            
        # set up environment for workers      
        self.env_str = ''
        if (env is not None):
            for item in env:
                self.env_str += item+'; '
        self.env_str += 'import time; '
        self.env_str += 'from dsap.parallel import write_flag; '
        
        ## TODO: how to use *instantiated* objects in subproc calls? 
        ##       --> use add another PREP str?
        ##       --> e.g. command / location to load pickled (?) objects from?
        
        # init progress display
        if (prog_mode is not None):
            self.progress = Progress(self.num_jobs, prog_mode, prog_cycle)        
            
        print(f"All work scheduled => {self.num_jobs} jobs")        
        return


    def step(self, parent):
        """ Cylic step function for the dispatch.
        
        Args:
            parent(TimerCycle): Outer timer object for cyclic calls to the "step()".  
            
        Returns:
            --
        """
           
        # monitor current state
        for th in range(self.N_workers):
            if (self.worker_state[th]):
                worker_flag = os.path.join(self.base, flag_file_str(th))
                if (os.path.isfile(worker_flag)):
                    self.num_completed += 1
                    self.worker_state[th] = 0
                    if (_DEBUG):
                        with open(worker_flag) as wf:
                            job_no = wf.readline().split('\n')[0]
                        debug_file = os.path.join(self.base, f'job_{job_no}.txt')
                        os.rename(worker_flag, debug_file)
                    else:
                        os.remove(worker_flag)
                    if (self.progress is None):
                        print(f"Worker #{th} --> job #{self.num_completed} has finished")
                        print(f"{self.loading_str()}")                          
        self.num_loaded = sum(self.worker_state)       
        
        # updates on progress
        if (self.progress is not None):
            self.time_alive = time.perf_counter() - self.time_started
            self.progress.update(self.time_alive, self.num_completed)       
            
        # completed?      
        if ((self.num_jobs_left == 0) and (self.num_loaded == 0)):
            print(f"All work completed ==> {self.num_completed}/{self.num_jobs} successful!")
            parent.cancel(reason='internal', dur=time.perf_counter()-parent.timer_start)
            self.close()
            
        # fully loaded?
        if (not self.is_fully_loaded):
            if (self.num_loaded == self.N_workers):
                self.is_fully_loaded = True
                if (self.progress is None):
                    print(f"Fully loaded on {self.N_workers} cores! (skip & wait)")
                return    
        else: # (self.is_fully_loaded):
            if (self.num_loaded == self.N_workers):
                return
            else:
                self.is_fully_loaded = False # reset flag        
                
        # dispatch cycle
        if (self.num_jobs_left):            
            
            # get next job
            job_args = self.workload_args.pop(0)
            job_kwargs = self.workload_kwargs.pop(0)
            self.num_jobs_left -= 1
            
            # select next free thread
            for th in range(self.N_workers):                
                if (self.worker_state[th] == 0):
                    self.num_dispatched += 1
                    
                    # create job w/ "flag" signalling after completion
                    job_str = f"args = {job_args}; kwargs = {job_kwargs}; "
                    call_str = f"res = {self.func}(*args, **kwargs); "                   
                    flag_str = f"write_flag(r'{os.path.join(self.base, flag_file_str(th))}', {self.num_dispatched}, {self.func}, {job_args}, {job_kwargs}, res); "
                    
                    # start process & assign dedicated CPU core
                    commands = [ 'python', '-c', self.env_str + job_str + call_str + flag_str ]
                    self.worker[th]['sub'] = subprocess.Popen( commands, text=True,
                                                               stdin=subprocess.PIPE,
                                                               stdout=subprocess.PIPE,
                                                               stderr=subprocess.PIPE )
                    pid = self.worker[th]['sub'].pid
                    self.worker[th]['proc'] = psutil.Process( pid )                 
                    self.worker[th]['proc'].cpu_affinity( [self.N_workers-th-1] )
                    self.worker[th]['proc'].nice(-10)        
                    self.worker_state[th] = 1
                    if (self.progress is None):
                        print(f"Dispatched job #{self.num_dispatched} ({self.num_jobs_left} left) --> worker #{th} (PID: {pid})")
                        print(f"{self.loading_str()}")
                    break # assign only 1 worker per cycle
            
                else:                    
                    continue # check for next free slot       
            
        else:
            if (not self.is_fully_dispatched):
                self.is_fully_dispatched = True
                if (self.progress is None):
                    print("All jobs have been dispatched! (waiting for remaining to complete)")                      
       
        return
    
   
    def loading_str(self):
        """ Shows string illustrating the current worker loading. """
        tmp = '[ '
        for th in range(self.N_workers):
            if (self.worker_state[th]):
                tmp += 'x '
            else:
                tmp += '. '
        tmp += ']'
        return tmp
    
    
    def close(self):
        """ Closes the dispatcher object. """
        if (not _DEBUG):
            shutil.rmtree(self.base, ignore_errors=True)
            print("Removed exchange folder")
        dur = time.perf_counter() - self.time_started
        print(f":::: Dispatcher finished :::: (lived for {duration_str(dur)})")
        return


#-----------------------------------------------------------------------------------------------


class TimerCycle:
    """ Cyclic timer w/ desired execution cycle and lifetime. """

    def __init__(self, cycle=_POLLING_CYCLE, end_of_life=_MAX_LIFETIME, 
                 name=None, verbose=False):
        """ Initialises 'TimerCycle' object. 
        
        Args:
            cycle (float, optional): Duration [s] between two cyclic executions. Defaults to
               '_POLLING_CYCLE'.
            end_of_life (float, optional): Lifetime [s] after which any remaining jobs will be 
                cancelled. Defaults to '_MAX_LIFETIME'.
            name (str, optional): Name for the cycler object. Default to 'None'.
            verbose (bool, optional): Switch for status messages. Defaults to 'False'.
            
        Returns:
            --        
        """
        
        # attributes        
        self.cycle = cycle        
        self.end_of_life = end_of_life
        self.name = name
        self.num_cycles = 0
        self.max_cycles = int(self.end_of_life/self.cycle)        
        self.is_verbose = verbose
        self.is_assigned = False
        self.is_running = False
        
        # members
        self.timer_obj = None
        self.timer_lock = threading.Lock()
        self.timer_start = 0
        
        if (self.is_verbose):
            print(f"TimerCycle '{self.name}' created")
        return
    
    
    def assign(self, func, *args, **kwargs):
        """ Assign callback function and associated args / kwargs. """
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.is_assigned = True
        if (self.is_verbose):
            print(f"<{self.name}>: Assigned function '{self.func}'")
        return
    
    
    def start(self):
        """ Mimics standard thread 'start' method. """
        if (not self.is_assigned):
            if (self.is_verbose):
                print(f"Function not yet assigned for TimerCycle <{self.name}>!")
            return
        else:
            if (self.is_verbose):
                print(f"<{self.name}>: Started")
            self.schedule()
            self.timer_start = time.perf_counter()
            self.is_running = True            
        return
    
    
    def schedule(self):
        """ Schedules the next timer cycle & keeps count on number of passed cycles. """                   
        self.num_cycles += 1
        if (self.num_cycles <= self.max_cycles):
            self.timer_obj = threading.Timer(self.cycle, self.run, *self.args, **self.kwargs)
            self.timer_obj.start()
        else:
            self.cancel(reason='lifetime', dur=time.perf_counter()-self.timer_start)
        return
    
    
    def run(self, *args, **kwargs):
        """ Executes assigned callback, then re-schedules timer. """        
        try:
            self.func(*args, *kwargs)
            # myres = self.func(*args, *kwargs) # TODO: how to include returns here?
        except:
            # print(f"<{self.name}>: Exception while running '{self.func.__name__}'")
            logging.exception(f"<{self.name}>: Exception in running thread!")
        finally:            
            with self.timer_lock: # will MAGICALLY break the loop 
                if (self.is_running):
                    self.schedule()
        return
    
    
    # def join(self):
    #     """ Mimics standard thread 'join' method. """
    #     self.timer_obj.join()       
    #     return
    
    
    def wait(self):
        """ Waits until 'TimerCycle' is cancelled by assigned 'func'. """
        while (self.is_running):
            time.sleep(_POLLING_CYCLE)
        return
    
    
    def cancel(self, reason='stop', dur=None):
        """ Mimics standard thread 'cancel()' method. """    
        with self.timer_lock:
            if (self.timer_obj is not None):
                self.timer_obj.cancel()
                if (self.is_verbose):                    
                    if (reason == 'internal'):
                        print(f"<{self.name}>: Completed by assigned function")
                    elif (reason == 'lifetime'):
                        print(f"<{self.name}>: Reached end-of-life! (after {self.end_of_life} sec)")
                    else: # (reason == 'stop'):
                        print(f"<{self.name}>: Stopped") 
                    if (dur is not None):
                        print(f"(lived for {self.num_cycles} cycles / {duration_str(dur)})")  
            self.is_running = False 
        return


#-----------------------------------------------------------------------------------------------
# MODULE FUNCTIONS
#-----------------------------------------------------------------------------------------------
# [https://stackoverflow.com/questions/36172101/designate-specific-cpu-for-a-process-python-multiprocessing]
 
def parallel_processing(N, func, args, prog_mode=_PROGRESS_MODE, prog_cycle=_PROGRESS_CYCLE, 
                        end_of_life=_MAX_LIFETIME):
    """ Performs 'N' parallel executions of 'func' w/ all 'args' variations.
    
    This provides an elaborated monitoring for a 'multiprocessing.Pool()'. In particular, 
    several different choices for 'progress' estimators and a lifetime limitation are 
    implemented. 

    Args:
        N (int): Number of CPU cores to be used.
        func (str): Name of function to be parallelised. Its signature needs to
            match the items exposed in 'args'.
        args (list): List of input arguments for each call to 'func'. As calls 
            w/ more than one arguments are supported, each item itself needs to
            be of type 'list'.
        prog_mode (str, optional): Display mode provided by class 'Progress' (see details).
                Defaults to 'None' (i.e. only dispatches are protocolled). 
        prog_cycle (float, optional): Updating speed for display (if applicable, i.e. only if
            'mode' is not 'None'). Defaults to '_PROGRESS_CYCLE'.
        end_of_life (int, optional): Duration [s] after which execution will be 
            forcefully stopped.
        
    Returns:
        num_success (int): Number of successfully completed operations.
        N_used (int): Number of actually used cores. May be less than 'N' due
            to availability as indicated by 'multiprocessing.cpu_count()' and 
            internally set margin.
    """    
    
    # determine number of CPU cores to be used
    N_avail = multiprocessing.cpu_count() - _CPU_MARGIN
    N_used = min(N, N_avail)
    
    # create pool of workers
    pool = multiprocessing.Pool(processes=N_used, initializer=None, initargs=(), maxtasksperchild=None) 
    print(f":::: Pool w/ {N_used} workers ::::", flush=True)
          
    # dispatch work
    t0 = time.perf_counter()
    state = pool.starmap_async(func, args, chunksize=1) #callback(), error_callback() ?
    num_jobs = len(args)      
    pool.close()
    print(f"All work dispatched => {num_jobs} jobs", flush=True)
           
    # monitor main cycle (work is managed in the background by "multiprocessing" routines)  
    lifetime = 0.0
    progress = Progress(num_jobs, prog_mode, prog_cycle)
    while (state.ready() is False):
        
        # wait for next cycle
        time.sleep(_POLLING_CYCLE)    
        lifetime += _POLLING_CYCLE        
        if (lifetime > end_of_life):
            print(f"Maximum lifetime exceeded! (aborting after {end_of_life} sec)", flush=True)          
            break    
        
        # monitor current state
        num_completed = num_jobs - state._number_left        
        progress.update(lifetime, num_completed)         
        
    print("", flush=True)
    
    # capture overall success       
    if (lifetime <= end_of_life):
        try:
            result = state.get()
            success = [True if (r is None) else False for r in result]
            if any(result):
                print("Check results!!! (some return value != None)", flush=True)
            else:
                print(f"All work completed => {len(success)} of {num_jobs} jobs successful!", flush=True)
        except:
            success = []
            pass #fixme: wtf?!?!?
    else:
        success = []
        
    # clean-up pool of workers
    try: 
        pool.close()        
    except:
        print("Pool could not finish properly!", flush=True)
        pool.terminate()
        
    print(f":::: Pool finished :::: (lived for {duration_str(time.perf_counter()-t0)})", flush=True)
    print("", flush=True)
        
    return len(success), N_used

 
def duration_str(seconds, max_unit='hours', sep='_', short_units=False, full_pattern=False):
    """ Returns given time interval in 'seconds' by an appropriate string representation.
    
    Depending on measured input 'seconds' (provided by, e.g., 'time.perf_counter()'), this
    function returns an appropriate string representation. That is, the format may be as "slim"
    as e.g. "2 hours" unless a 'full_pattern' is requested anyway. In comparison, the result in
    the latter case would read "2 hours 0 mins 0 secs".
    
    Supported units are (enforcing consistency for units years & months): 
        + years (y)     --> 365 days
        + months (mt)   -->  30 days
        + weeks (w)     -->   7 days
        + days (d)      -->  24 hours
        + hours (h)     -->  60 mins
        + mins (m)      -->  60 secs
        + secs (s)    
        
    Args:
        seconds (int): Duration, i.e. # seconds that have been passed since a certain event.        
        max_unit (str, optional): Defines maximum time unit to check for. Defaults to 'hours'.
        sep (str, optional): Separator between string parts, tpyically spaces or underscores.
            Defaults to '_' (underscore).
        short_units (bool, optional): Switch for using abbreviated time units instead of longer
            names, e.g. 'm' instead of 'mins'. Defaults to 'False'.
        full_pattern (bool, optional): Switch for always representing the duration up to the
            'max_unit' even if not required, i.e. if 'seconds' are les. Defaults to 'False'.
            
    Returns:
        dur_str (str): Proper representation of 'seconds' (e.g. for 'print()').
        
    Examples:   
        duration_str(15*60)
        >>> '15_mins'
        duration_str(260342, max_unit='weeks', sep=' ', short_units=True, full_pattern=True)
        >>> '0w 3d 0h 19m 2s'
    """  
    unit_split = [[ 31536000, 'y',  'years' ],
                  [  2592000, 'mt', 'months'],
                  [   604800, 'w',  'weeks' ],
                  [    86400, 'd',  'days'  ],
                  [     3600, 'h',  'hours' ],
                  [       60, 'm',  'mins'  ],
                  [        1, 's',  'secs'  ]]
    units = [x[2] for x in unit_split]
    
    # init 
    seconds = int(seconds) 
    if (not seconds):
        return 'no time'
    na = units.index(max_unit)
    if (short_units):
        nu = 1
        sep_units = '' # no separator for short units!
    else:
        nu = 2
        sep_units = sep
    
        
    # analyse w.r.t. maximum desired units
    analysis = []
    rest = seconds
    for n in range(len(unit_split)):
        if (n >= na):
            analysis.append( divmod(rest, unit_split[n][0]) )
            rest = analysis[-1][1]
        else:
            analysis.append((0, rest))
    
    # create string parts
    str_parts = []  
    for n in range(na, len(unit_split)):
        if (full_pattern or (analysis[n][0] > 0)):
            str_parts.append( f'{analysis[n][0]:d}'+sep_units+f'{unit_split[n][nu]}' )
        else: # part not required
            str_parts.append('') 
         
    # create overall string
    dur_str = ''
    for item in str_parts:
        if (full_pattern or (item != '')):
            dur_str += item + sep
    if (len(sep)): # remove trailing "sep" (but only if non-empty)
        dur_str = eval(f'dur_str[:-{len(sep)}]')
    
    return dur_str


def flag_file_str(th):
    """ Returns filename of flag-file for worker 'th' (thread). """    
    return f'worker_{th}.flag'
    

def write_flag(flag_file, job_no, job_func, job_args, job_kwargs, job_out):
    """ Writes a small 'flag_file' upon completion of job. """    
    with open(flag_file, 'wt') as ff:
        ff.write(f"{job_no}\n")
        ff.write(f"[finished @ {time.strftime('%Y-%m-%d %H:%M:%S')}]\n\n")
        try:
            ff.write(f"func: {job_func.__name__}\n")            
        except:
            ff.write(f"func: {job_func.func.__name__}\n") # Note: If 'functools.partial' is involved!
        ff.write(f"args:   {job_args}\n")
        ff.write(f"kwargs: {job_kwargs}\n")
        ff.write("\n")       
        try:
            ff.write("results:\n")
            ff.write(f"{job_out}\n")
        except:
            pass # then leave out results (could be arbitrary types & formats!)                
        ff.close()
    return



################################################################################################
# Description of main functions & example usage:
#
#   function 'parallel_processing'  --> automatic parallelisation w/ 'N' processes based on  
#                                       Python's 'multiprocessing' module   
#
#   class 'TimerCycle'  --> class for *any* cyclic actions (bound to 'step()' method)
#   class 'Dispatcher'  --> class for managing the workload (distribution) for a bound routine
#                           'func' in connection w/ TimerCycle
#
#   class 'Progress'    --> class for displaying the progess for both of the above methods 
#                           (or in connection w/ any other separate use)
#
# Usage example (scheme):
#
# The following scheme illustrates which methods are involved from 'TimerCycle' <TC> and 
# 'Dispatcher' <D>. As can be seen, the timer's 'cycle' parameter should be chosen small enough 
# so as to not lose much time between consecutive executions of 'func()'.
# 
#   <TC> start()    schedule()                      schedule()
#   <D>                         func()                          func()
#       | . . . . . | . cycle . | . . exec func . . | . cycle . | . . exec func . . => ...
#   +----------------------------------------------------------------------------------------> 
#                                                                                         time
#
# Usage example (calls):
#
#   # set up the proper "call environment" to make 'func' available for 'Dispatcher' object
#   call_env = ['import sys', 'sys.path.insert(0, r"C:\\MyCode")', 'from mymodule import func']
#
#   # create workload dispatcher object & associate desired job function
#   D = parallel.Dispatcher(N, func, args, kwargs, call_env)
#
#   # create "driving" timer object
#   T = parallel.TimerCycle(name='MASTER')
#
#   # set 'step()' method of dispatcher to be executed in a cyclic manner
#   T.assign(D.step(), [T,])
#
#   # init timer operation & wait for completion (= infinity loop)
#   T.start()
#   T.wait()
#
################################################################################################
