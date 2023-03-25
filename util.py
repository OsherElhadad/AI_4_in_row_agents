import os
import inspect
import sys

def default(str):
    return str + ' [Default: %default]'

def parseAgentArgs(str):
    if str == None:
        return {}
    pieces = str.split(',')
    opts = {}
    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
        else:
            key, val = p, 1
        opts[key] = val
    return opts


def readCommand(argv):
    """
    Processes the command used to run connect4 from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python connect4.py <options>
    EXAMPLES:   python connect4.py
                    - starts an interactive game
              
    """
    parser = OptionParser(usageStr)

    parser.add_option('-m', '--gameMode', dest='gameMode', type='int',
                      help=default('the GAMES mode to play, 1- player vs. AI, 2- player vs. player'), metavar='MODE', default=2)
    parser.add_option('-d', '--depth', dest='depth', type='int',
                      help=default('the max depth to explore the minmax tree'), metavar='DEPTH', default=3)
    parser.add_option('-g', '--graphics', action='store_true', dest='graphics',
                      help='Display output as graphics', default=True)
    parser.add_option('-a', '--agent', type='str', dest='agent',
                      help=default('Agent type to be play as AI agent'), default="Random")


    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()

    # Choose an agent

    agentType = loadAgent(options.agent)
    agent = agentType(**{"depth": options.depth})  # Instantiate agent with agentArgs

    args['gameMode'] = options.gameMode
    args['agent'] = agent
    args['graficMode'] = options.graphics

    return args



def loadAgent(agent):
    # Looks through all pythonPath Directories for the right module,
    pythonPathStr = os.path.expandvars("$PYTHONPATH")
    if pythonPathStr.find(';') == -1:
        pythonPathDirs = pythonPathStr.split(':')
    else:
        pythonPathDirs = pythonPathStr.split(';')
    pythonPathDirs.append('.')

    for moduleDir in pythonPathDirs:
        if not os.path.isdir(moduleDir):
            continue
        moduleNames = [f for f in os.listdir(
            moduleDir) if f.endswith('gents.py')]
        for modulename in moduleNames:
            try:
                module = __import__(modulename[:-3])
            except ImportError:
                continue
            if agent in dir(module):
                return getattr(module, agent)
    raise Exception('The agent ' + agent +
                    ' is not specified in any *Agents.py.')



def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" %
          (method, line, fileName))
    sys.exit(1)

def lookup(name, namespace):
    """
    Get a method or class from any imported module from its name.
    Usage: lookup(functionName, globals())
    """
    dots = name.count('.')
    if dots > 0:
        moduleName, objName = '.'.join(
            name.split('.')[:-1]), name.split('.')[-1]
        module = __import__(moduleName)
        return getattr(module, objName)
    else:
        modules = [obj for obj in list(namespace.values()) if str(
            type(obj)) == "<type 'module'>"]
        options = [getattr(module, name)
                   for module in modules if name in dir(module)]
        options += [obj[1]
                    for obj in list(namespace.items()) if obj[0] == name]
        if len(options) == 1:
            return options[0]
        if len(options) > 1:
            raise Exception('Name conflict for %s')
        raise Exception('%s not found as a method or class' % name)

import signal
import time


class TimeoutFunctionException(Exception):
    """Exception to raise on a timeout"""
    pass


class TimeoutFunction:
    def __init__(self, function, timeout):
        self.timeout = timeout
        self.function = function

    def handle_timeout(self, signum, frame):
        raise TimeoutFunctionException()

    def __call__(self, *args, **keyArgs):
        # If we have SIGALRM signal, use it to cause an exception if and
        # when this function runs too long.  Otherwise check the time taken
        # after the method has returned, and throw an exception then.
        if hasattr(signal, 'SIGALRM'):
            old = signal.signal(signal.SIGALRM, self.handle_timeout)
            signal.alarm(self.timeout)
            try:
                result = self.function(*args, **keyArgs)
            finally:
                signal.signal(signal.SIGALRM, old)
            signal.alarm(0)
        else:
            startTime = time.time()
            result = self.function(*args, **keyArgs)
            timeElapsed = time.time() - startTime
            if timeElapsed >= self.timeout:
                self.handle_timeout(None, None)
        return result


_ORIGINAL_STDOUT = None
_ORIGINAL_STDERR = None
_MUTED = False


class WritableNull:
    def write(self, string):
        pass


def mutePrint():
    global _ORIGINAL_STDOUT, _ORIGINAL_STDERR, _MUTED
    if _MUTED:
        return
    _MUTED = True

    _ORIGINAL_STDOUT = sys.stdout
    #_ORIGINAL_STDERR = sys.stderr
    sys.stdout = WritableNull()
    #sys.stderr = WritableNull()


def unmutePrint():
    global _ORIGINAL_STDOUT, _ORIGINAL_STDERR, _MUTED
    if not _MUTED:
        return
    _MUTED = False

    sys.stdout = _ORIGINAL_STDOUT
    #sys.stderr = _ORIGINAL_STDERR
