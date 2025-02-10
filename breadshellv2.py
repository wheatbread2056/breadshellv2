#!/usr/bin/python

# TODO
# - make this work without ANY dependencies
# - same thing for colors
# - remove bloat!
# - make small
# - make it actally good

failed_imports = []

# IMPORT ALL DEPENDENCIES --initial

# built-in libraries sometimes
# hard fix
WSL = False
import os
import time
import datetime
# import random <-- commenting this is going to break some things but core functionality will still work
import subprocess
# Replacement for getpass module (literally stolen code)
def getuser():
    """Get the username from the environment or password database.

    First try various environment variables, then the password
    database.  This works on Windows as long as USERNAME is set.
    Any failure to find a username raises OSError.

    .. versionchanged:: 3.13
        Previously, various exceptions beyond just :exc:`OSError`
        were raised.
    """

    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
        user = os.environ.get(name)
        if user:
            return user

    try:
        import pwd
        return pwd.getpwuid(os.getuid())[0]
    except (ImportError, KeyError) as e:
        raise OSError('No username set in the environment') from e
import socket

# the point of this code is to install the modules if the user doesn't already have them installed

DISABLE_COLORS = False
DEFAULT_SETTINGS = True
LEGACY_PROMPT = True # just uses prompt() which was used in every version before 1.0
# legacy prompt is gonna have to be enabled for now because i cant figure out whats wrong.

# import getkey - required for autocompletion + command history
try:
    from getkey import getkey, keys
except:
    try:
        os.system('pip install getkey --break-system-packages')
        from getkey import getkey, keys
    except:
        failed_imports.append('getkey')
        LEGACY_PROMPT = True


# makes sure that bash shell is used
os.environ['SHELL'] = '/bin/bash'

# version number and other information --version
version = '1.0-dev5c'
versiontype = 3 # 1 = release, 2 = prerelease, 3 = development, 4 = early development
versiontext = 'bshv2 0.1' # add for stuff like "bugtesting preview" or "private beta", appended to version in parentheses. example: 1.1-pre7c (Private Beta)
devnote = 'ultra debloated'

# define colors --customization
if DISABLE_COLORS == True:
    # empty classes so there's no undefined "c.red undefined" errors
    class c:
        red = ''
        yellow = ''
        green = ''
        blue = ''
        magenta = ''
        cyan = ''
        white = ''
        black = ''
        r = ''
        b = ''
        i = ''
        e = ''
        u = ''

    class bc:
        red = ''
        yellow = ''
        green = ''
        blue = ''
        magenta = ''
        cyan = ''
        white = ''
        black = ''
        r = ''

else:
    # foreground colors
    class c:
        red = '\033[31m'
        yellow = '\033[33m'
        green = '\033[32m'
        blue = '\033[34m'
        magenta = '\033[35m'
        cyan = '\033[36m'
        white = '\033[37m'
        black = '\033[30m'
        b = '\033[1m' # bold
        i = '\033[3m' # italic
        u = '\033[4m' # underline
        e = '\033[0m' # end
        r = '\033[39m' # resets color to default

    # background colors
    class bc:
        red = '\033[41m'
        yellow = '\033[43m'
        green = '\033[42m'
        blue = '\033[44m'
        magenta = '\033[45m'
        cyan = '\033[46m'
        white = '\033[47m'
        black = '\033[40m'
        r = '\033[49m' # resets color to default
    
user = getuser()
    
# now time to load settings --settings
try:
    settingsdir = f'/home/{user}/.config/breadshell'
except:
    settingsdir = '/home/user/.config/breadshell'
settingspath = settingsdir+'/settings.ini'
# read the settings and return all key/value pairs
def read_settings():
    global DEFAULT_SETTINGS
    config = {}
    # create the file if it doesn't already exist
    try:
        with open(settingspath, 'a') as file:
            file.close()
    except:
        try:
            os.mkdir(settingsdir)
        except:
            DEFAULT_SETTINGS = True
        try:
            with open(settingspath, 'a') as file:
                file.close()
        except:
            DEFAULT_SETTINGS = True
    if DEFAULT_SETTINGS == False:
        with open(settingspath, 'r') as file:
            for line in file:
                # skip empty lines and comment lines
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=',1)
                    # remove quotes
                    value = value.strip('"').strip("'")
                    config[key] = value
            file.close()
        return config

if DEFAULT_SETTINGS == False:
    settings = read_settings()

# overwrite the settings and add new values
def add_settings(key, value):
    if value == True or value == False:
        settings[key] = str(value)
    else:
        settings[key] = value
    # write to the file
    if DEFAULT_SETTINGS == False:
        with open(settingspath, 'w') as file:
            for key, value in settings.items():
                file.write(f'{key}={value}\n')
            file.close()

# remove a setting (broken idk why)
def remove_settings(key1):
    # write to the file
    if DEFAULT_SETTINGS == False:
        with open(settingspath, 'w') as file:
            for key, value in settings.items():
                if not key1 == key:
                    file.write(f'{key}={value}\n')
            file.close()

# generate default settings
# changed in bshv2 to have MY defaults because they are simply better
defaultSettings = {
    'loginColor': 'red',
    'dirColor': 'white',
    'textColor': 'r',
    'pointerColor': 'r',
    'pointerChar': '$:',
    'showLogin': 'True',
    'showDir': 'True',
    'showPointer': 'True',
    'showHost': 'False',
    'clearOnBoot': 'True', # does nothing anymore.
    'shortenDir': 'True',
    'dirType': '0',
}
temp1494861 = 0 # what is this for? i have no idea
# checks for settings (kinda sucks but it works)
if DEFAULT_SETTINGS == False:
    for setting in defaultSettings:
        try:
            temp1494861 = settings[setting]
        except:
            add_settings(setting,defaultSettings[setting])
else:
    settings = defaultSettings.copy()

# settings friendly names
friendlySettings = {
    'loginColor': 'Username Color',
    'dirColor': 'Directory Color',
    'textColor': 'Text Color',
    'pointerColor': 'Pointer Color',
    'pointerChar': 'Pointer Character',
    'showLogin': 'Show Current User',
    'showDir': 'Show Current Directory',
    'showPointer': 'Show Pointer',
    'showHost': 'Show Hostname',
    'clearOnBoot': 'Clear On Boot',
    'shortenDir': 'Shorten User Directory',
    'dirType': 'not implemented', # add this later
    'h_version': 'Installed Version',
}

# settings types and their valid options
# any setting with a type not defined will just be 'any'
types = {
    'color': ['default', 'red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'white', 'black'],
    'texteffect': ['none', 'bold', 'italic', 'underline'],
    'bool': ['true', 'false', 't', 'f'],
    'str': 'any',
    'num': 'any',
}

settingtypes = {
    'loginColor': 'color',
    'dirColor': 'color',
    'textColor': 'color',
    'pointerColor': 'color',
    'pointerChar': 'str',
    'showLogin': 'bool',
    'showDir': 'bool',
    'showPointer': 'bool',
    'showHost': 'bool',
    'clearOnBoot': 'bool',
    'shortenDir': 'bool',
    'dirType': 'num', # add this later
}

boolTranslation = {
    'true': True,
    'false': False,
    't': True,
    'f': False
}

# clear console
if settings['clearOnBoot'] == 'True':
    os.system('clear')

# check if breadshell is installed --installcheck
try:
    currentdir = os.getcwd()
    scriptdir = os.path.dirname(__file__)

    # if this doesn't work, it will give an error, which is how this works
    os.chdir('/usr/src/breadshell')
    os.chdir(currentdir)
    
    if scriptdir == '/usr/src/breadshell':
        installed = True
        runfrominstall = True

    else:
        print(f'{c.red}you are running breadshell from a file, even though breadshell is installed{c.r}')
        installed = True
        runfrominstall = False

    # change back to the previous directory
    os.chdir(currentdir)

except:
    print(f'{c.red}breadshell is not installed, or an error has occured when loading{c.r}')
    installed = False
    runfrominstall = False

# set version if installed
if runfrominstall == True:
    add_settings('h_version', version)

# basic functions
    
# returns yellow error
def throwerror(msg='An unknown error has occured'):
    print(f'{c.yellow}{msg}{c.r}')

# returns red error and exits to prevent corruption or something
def fatalerror(msg='A fatal error has occured, exiting immediately',force_exit=1):
    print(f'{c.red}{msg}{c.r}')
    if force_exit == 1:
        exit()

# utility scripts --utilities

def startu_colortester():
    # random colors+chars for 256 characters
    chars = '`1234567890-=~!@#$%^&*()_+qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
    str = ''
    for i in range(4096):
        a = random.randint(0,len(chars)-1)
        char = chars[a]

        # define colors by lists instead of classes
        foregroundColors = [c.red,c.yellow,c.green,c.blue,c.cyan,c.magenta,c.white,c.black,c.r]
        backgroundColors = [bc.red,bc.yellow,bc.green,bc.blue,bc.cyan,bc.magenta,bc.white,bc.black,bc.r]
        # get random item in the lists
        b = foregroundColors[random.randint(0,len(foregroundColors)-1)]
        # used _c here since c is already used for the main colors class
        _c = backgroundColors[random.randint(0,len(foregroundColors)-1)]

        # add it to the main string
        str=str+b+_c+char

    # +c.r+bc.r is needed to reset the colors
    print(str+c.r+bc.r)

# utility launcher (totally not just modified game launcher)

def utillauncher():
    globalversion = '0.3.2'
    # list amount of games here
    #------------------- NOTE: add 'networktest' utility when finished -------------
    utilities = ['colortester','calculator','python','assistant','networktest']
    versions = ['1.1','1.1','1.0','0.1.1','0.3']

    print(f'breadshell utilities {globalversion}')
    print(f'please select the utility you would like to start ({len(utilities)} found):')

    i = 1
    for utility in utilities:
        print(f'{c.yellow}{i} - {utility} {c.cyan}{versions[i-1]}{c.r}')
        i += 1

    print(f'{c.yellow}exit - exit')

    # fixes crashing bug (major) - added in 1.0-dev1a, fixed in 1.0-dev1b (another minor bug appeared)
    def selection(utilities):
        try:
            utility = input(f'{c.cyan}butils{c.r} {settings["pointerChar"]} ')
        except:
            pass
        try:
            if utility == 'exit':
                main()
            else:
                try:
                    if utilities[int(utility)-1] in utilities:
                        print(f'Starting {utilities[int(utility)-1]}...')
                        exec(f'startu_{utilities[int(utility)-1]}()')
                except:
                    if utility == None or utility == '' or utility.lower == 'exit':
                        pass
                    else:
                        throwerror('Invalid utility.')
        except:
            pass
    selection(utilities)

badStart = False

def reportBadStart(a): # legacy fix introduced around 0.4 to prevent wsl from instantly crashing
    global badStart
    if not badStart:
        throwerror(f'an error occurred: {a}')
        throwerror('username will default to \'user\' to fix compatibility issues')
        badStart = True

if WSL == 1:
    throwerror('Note: Bold and italic text effects are not supported when using the Windows Terminal. Use real Linux or an X Server when possible.')

if DEFAULT_SETTINGS == True:
    throwerror(f'{settingspath.replace(f"/home/{user}", "~")} couldn\'t be generated, default settings will be used. Settings will not save.')

if LEGACY_PROMPT == True:
    throwerror('Legacy fallback prompt is enabled. Command history will not work and functionality will be limited.')

# start of program, shown when opening the file
if not versiontext == '' and not versiontext == None:
    vt = f' ({c.cyan}{versiontext}{c.r})'
else:
    vt = ''

def color(col):
    global c
    return c.__getattribute__(c, col)

cmdhistory = []
historycur = -2
os.system('clear')
throwerror('[bshv2] settings were force-disabled along with the command history')
print(f'version {c.cyan}{version}{c.r}{vt}, latest login {c.magenta}{datetime.datetime.now()}{c.r}')
print(f'type {c.yellow}bhelp{c.r} for a list of custom commands.')
# main loop
def main():
    global cmdhistory
    while True:
        # generate the line

        tempcmd = ""
        if settings['showLogin'] == 'True':
            try:
                tempcmd += f"{color(settings['loginColor'])}{user}@{socket.gethostname()}{c.r} "
                if not settings['showHost'] == 'True':
                    tempcmd = tempcmd.split('@')[0]+f'{c.r} '
            except Exception as e:
                reportBadStart(e)
                tempcmd += f"{color(settings['loginColor'])}user@{socket.gethostname()}{c.r} "
                if not settings['showHost'] == 'True':
                    tempcmd = tempcmd.split('@')[0]+f'{c.r} '

        if settings['showDir'] == 'True':
            if settings['shortenDir'] == 'True':
                tempcmd += f"{color(settings['dirColor'])}{os.getcwd()}{c.r} ".replace(f'/home/{user}', '~')
            else:
                tempcmd += f"{color(settings['dirColor'])}{os.getcwd()}{c.r} "

        if settings['showPointer'] == 'True':
            tempcmd += f"{color(settings['pointerColor'])}{settings['pointerChar']} {c.r}"

        tempcmd += color(settings['textColor'])

        # main input (user@hostname path/to/directory > command typed in) --main
        if LEGACY_PROMPT == True: # pre 1.0, only used as fallback
            try:
                cmd = input(tempcmd)
                cmdargs = cmd.split(' ')
            except Exception as e:
                fatalerror('An error has occured: '+str(e))
        else:
            buffer = ''
            print(tempcmd, end='')
            while True:
                key = getkey()
                
                if key == keys.ENTER:
                    break

                elif key == keys.UP: # previous command in the history
                    try:
                        # if historycur = -1, that's the end of the history
                        prevbuffer = buffer
                        if historycur == -2:
                            historycur = len(cmdhistory)
                        if historycur > 0:
                            historycur -= 1
                            buffer = cmdhistory[historycur]
                            print('\b \b' * len(prevbuffer), end='')
                            print(buffer,end='')
                    except:
                        pass
                    
                elif key == keys.DOWN: # next command in the history
                    try:
                        prevbuffer = buffer
                        if historycur == -2:
                            historycur = len(cmdhistory)-1
                        if historycur < len(cmdhistory)-1:
                            historycur += 1
                            buffer = cmdhistory[historycur]
                            print('\b \b' * len(prevbuffer), end='')
                            print(buffer,end='')
                    except:
                        pass

                elif key == keys.BACKSPACE: # handle backspace
                    try:
                        if len(buffer) > 0:
                            buffer = buffer[:len(buffer)-1]
                            print('\b \b', end='')
                    except:
                        pass
                else:
                    buffer += str(key)
                    print(key, end='')

            print() # newline
            tcmd = buffer
            tcmdargs = tcmd.split(' ')
            cmdargs = [x for x in tcmdargs if x != '']
            cmd = ' '.join(cmdargs)

            try: # make sure that empty and duplicate commands don't get added to the command history
                if not cmd.replace(' ','') == '' and not cmd == cmdhistory[len(cmdhistory)-1]:
                    cmdhistory.append(' '.join(cmdargs))
            except:
                if not cmd.replace(' ','') == '':
                    cmdhistory.append(cmd)

            if cmdargs == []:
                cmdargs.append('')

            historycur = -2
        
        print(c.r + c.e,end='') # attempt to stop command output from using the set text color

        # for special commands
            
        # change directory (cd)
        if cmdargs[0] == ('cd'):
            try:
                os.chdir(cmd.split(' ')[1])
            except:
                throwerror('Invalid directory, or a directory was not specified')

        # breadhelp (bhelp)
        elif cmdargs[0] == ('bhelp'):
            print(f'''
    breadshell version {c.cyan}{version}{c.r}

    --- CUSTOM COMMANDS ---

    {c.yellow}bhelp{c.r} - open this page
    {c.yellow}butils{c.r} - start utility launcher (broken in bshv2)
    {c.yellow}version{c.r} - displays version information
    {c.yellow}settings{c.r} - change your breadshell settings
    {c.yellow}scedit{c.r} - edit, view, and create breadshell shortcuts
    {c.red}exit{c.r} - exits breadshell
    ''')

        # exit... self explanatory
        elif cmdargs[0] == ('exit'):
            exit()

        # "developer commands"
            
        # throw a generic error
        elif cmdargs[0] == ('dev-generic-error'):
            throwerror()
            
        # throw a FATAL generic error, which is red...
        elif cmdargs[0] == ('dev-generic-fatalerror'):
            fatalerror()

        # set background color to a random color
        elif cmdargs[0] == ('dev-randombg'):
            quickColors = [bc.red,bc.yellow,bc.green,bc.blue,bc.magenta]
            print(quickColors[random.randint(0,len(quickColors)-1)])
            os.system('clear')
        
        # reset the background color
        elif cmdargs[0] == ('dev-resetbg'):
            print(bc.r)
            os.system('clear')
        
        # colortest 1024 times... for some reason
        elif cmdargs[0] == ('dev-explosionofcolors'):
            for i in range(1024):
                startu_colortester()

        # actually useful, directly execute code from breadshell.py
        # able to execute multiple commands at a time without semicolon seperators
        elif cmdargs[0] == ('dev-exec'):
            try:
                exec(' '.join(cmdargs[1:]))
            except Exception as e:
                throwerror('(Python) '+str(e))

        elif cmdargs[0] == ('dev-text-effects-demo'):
            print(f'''
{c.b}this text should be bold{c.e} and this text is normal
{c.i}this should be italic{c.e}
{c.u}this should be underlined{c.e}
''')

        elif cmdargs[0] == ('dev-clear-history'):
            try:
                cmdhistory = []
            except Exception as e:
                throwerror(f'Failed to clear command history ({e})')

        # launch utilities
        elif cmdargs[0] == ('butils'):
            utillauncher()

        # display version info
        elif cmdargs[0] == ('version'):
            print(f'breadshell version {c.cyan}{version}{c.r}{vt}')                

            # display version type
            if versiontype == 1:
                print(f'this is a {c.green}release{c.r} of breadshell')
            elif versiontype == 2:
                print(f'this is a {c.yellow}prerelease{c.r} of breadshell. \nsome bugs may occur')
            elif versiontype == 3:
                print(f'this is a {c.magenta}development{c.r} version of breadshell. \nsome bugs or unfinished features may occur')
            elif versiontype == 4:
                print(f'this is an {c.cyan}early development{c.r} version of breadshell. \nmany bugs or unfinished features may occur')
            else:
                print(f'this is an {c.red}unknown {c.r}or {c.red}unofficial{c.r} version of breadshell')

            # display installation status
            if installed == True:
                if DEFAULT_SETTINGS == False:
                    print(f'breadshell is {c.green}installed{c.r} (version {c.cyan}{settings["h_version"]}{c.r})')
                else:
                    print(f'breadshell is {c.green}installed{c.r} (version {c.red}unknown{c.r})')
            else:
                print(f'breadshell is {c.red}not installed{c.r}')

            # running from file or not
            if runfrominstall == True:
                print(f'running from {c.green}install{c.r}')
            else:
                print(f'running from {c.red}file{c.r}')

            print(f'source code on {c.blue}github.com/wheatbread2056/breadshell{c.r}')

            if not devnote == """""" and not devnote == '' and not devnote == None:
                print('Note from the developer:')
                print(devnote)

        # edit settings --editsettings
        elif cmdargs[0] == ('settings'):
            if settings == {}:
                throwerror(f'No settings were found, or there was an error reading settings.ini ({settingspath})')
                main()
            else:
                tm0 = 0
                reflist = []
                for key, value in settings.items():
                    if not key.startswith('h_') and not key.startswith('s_'):
                        if key in friendlySettings:
                            if settings[key] == 'False':
                                print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.red}{value}{c.r}")
                            elif settings[key] == 'True':
                                print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.green}{value}{c.r}")
                            else:
                                print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.cyan}{value}{c.r}")

                        else:
                            print(f"({c.yellow}{tm0}{c.r}) {c.yellow}{key}{c.r} - {c.cyan}{value}{c.r}") # if there is no friendly name for the setting
                        reflist.append(key)
                        tm0 += 1

            print('Type the number of the setting you would like to change, or list to list settings, or exit to leave')

            while True:
                setting = input(f'{c.cyan}settings{c.r} {settings["pointerChar"]} ')
                completed = False

                # new (1.0+) settings, number-based selection
                # legacy settings removed because i am NOT updating the code twice whenever i need to change this
                try:
                    if int(setting) < len(reflist) and int(setting) > -1:
                        print('Enter a new value:')
                        newValue = input(f'{c.green}{friendlySettings[reflist[int(setting)]]}{c.r} {settings["pointerChar"]} ')
                        if settingtypes[reflist[int(setting)]] == 'bool':
                            if newValue.lower() in boolTranslation:
                                try:
                                    add_settings(reflist[int(setting)],boolTranslation[newValue.lower()])
                                    print(f'Successfully updated the setting {c.green}{friendlySettings[reflist[int(setting)]]}{c.r}.')
                                except:
                                    throwerror(f'Failed to update the setting {c.green}{friendlySettings[reflist[int(setting)]]}{c.r}')
                            else:
                                throwerror(f'Invalid value, type \'{settingtypes[reflist[int(setting)]]}\' only allows values {types["bool"]}')

                        elif newValue.lower() == 'exit':
                            pass

                        else:
                            if not types[settingtypes[reflist[int(setting)]]] == 'any' and not types[settingtypes[reflist[int(setting)]]] == None:
                                if newValue.lower() in types[settingtypes[reflist[int(setting)]]]:
                                    try:
                                        if settingtypes[reflist[int(setting)]] == 'color':
                                            if newValue.lower() == 'default':
                                                add_settings(reflist[int(setting)],'r')
                                            else:
                                                add_settings(reflist[int(setting)], newValue.lower())

                                        elif settingtypes[reflist[int(setting)]] == 'texteffect':
                                            if newValue.lower() == 'none':
                                                add_settings(reflist[int(setting)],'e')
                                            elif newValue.lower() == 'bold':
                                                add_settings(reflist[int(setting)],'b')
                                            elif newValue.lower() == 'italic':
                                                add_settings(reflist[int(setting)],'i')
                                            elif newValue.lower() == 'underline':
                                                add_settings(reflist[int(setting)],'u')
                                                
                                        else:
                                            add_settings(reflist[int(setting)], newValue)

                                        print(f'Successfully updated the setting {c.green}{friendlySettings[reflist[int(setting)]]}{c.r}.')
                                    except:
                                        throwerror(f'Failed to update the setting {c.green}{friendlySettings[reflist[int(setting)]]}{c.r}')
                                else:
                                    throwerror(f'Invalid value, type \'{settingtypes[reflist[int(setting)]]}\' only allows values {types[settingtypes[reflist[int(setting)]]]}')
                            else:
                                try:
                                    add_settings(reflist[int(setting)], newValue)
                                    print(f'Successfully updated the setting {c.green}{friendlySettings[reflist[int(setting)]]}{c.r}.')
                                except:
                                    throwerror(f'Failed to update the setting {c.green}{friendlySettings[reflist[int(setting)]]}{c.r}')


                        completed = True
                except:
                    pass

                if setting.lower() == 'list':
                    tm0 = 0
                    reflist = []
                    for key, value in settings.items():
                        if not key.startswith('h_') and not key.startswith('s_'):
                            if key in friendlySettings:
                                if settings[key] == 'False':
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.red}{value}{c.r}")
                                elif settings[key] == 'True':
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.green}{value}{c.r}")
                                else:
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.cyan}{value}{c.r}")

                            else:
                                print(f"({c.yellow}{tm0}{c.r}) {c.yellow}{key}{c.r} - {c.cyan}{value}{c.r}") # if there is no friendly name for the setting
                            reflist.append(key)
                            tm0 += 1

                elif setting.lower() == 'dev-list':
                    tm0 = 0
                    reflist = []
                    for key, value in settings.items():
                        if not key.startswith('h_') and not key.startswith('s_'):
                            if key in friendlySettings:
                                if key in settingtypes:
                                    if settings[key] == 'False' and settingtypes[key] == 'bool':
                                        print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} [{key}] - {c.red}{value}{c.r} [{c.yellow}bool{c.r}]")
                                    elif settings[key] == 'True' and settingtypes[key] == 'bool':
                                        print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} [{key}] - {c.green}{value}{c.r} [{c.yellow}bool{c.r}]")
                                    else:
                                        print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} [{key}] - {c.cyan}{value}{c.r} [{c.yellow}{settingtypes[key]}{c.r}]")
                                else:
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} [{key}] - {c.cyan}{value}{c.r}")
                            else:
                                if key in settingtypes:
                                    print(f"({c.yellow}{tm0}{c.r}) {key} - {c.cyan}{value}{c.r} [{c.yellow}{settingtypes[key]}{c.r}]")
                                else:
                                    print(f"({c.yellow}{tm0}{c.r}) {key} - {c.cyan}{value}{c.r}")
                            reflist.append(key)
                            tm0 += 1
                        else:
                            if key in friendlySettings:
                                if key in settingtypes:
                                    if settings[key] == 'False' and settingtypes[key] == 'bool':
                                        print(f"({c.red}X{c.r}) {friendlySettings[key]} [{c.red}{key}{c.r}] - {c.red}{value}{c.r} [{c.yellow}bool{c.r}]")
                                    elif settings[key] == 'True' and settingtypes[key] == 'bool':
                                        print(f"({c.red}X{c.r}) {friendlySettings[key]} [{c.red}{key}{c.r}] - {c.green}{value}{c.r} [{c.yellow}bool{c.r}]")
                                    else:
                                        print(f"({c.red}X{c.r}) {friendlySettings[key]} [{c.red}{key}{c.r}] - {c.cyan}{value}{c.r} [{c.yellow}{settingtypes[key]}{c.r}]")
                                else:
                                    print(f"({c.red}X{c.r}) {friendlySettings[key]} [{c.red}{key}{c.r}] - {c.cyan}{value}{c.r}")
                            else:
                                if key in settingtypes:
                                    print(f"({c.red}X{c.r}) {c.red}{key}{c.r} - {c.cyan}{value}{c.r} [{c.yellow}{settingtypes[key]}{c.r}]")
                                else:
                                    print(f"({c.red}X{c.r}) {c.red}{key}{c.r} - {c.cyan}{value}{c.r}")

                elif setting.lower() == 'exit':
                    break

                elif completed == True: # variable added to stop throwing errors when nothing went wrong
                    pass

                else:
                    throwerror('Invalid setting')

        # edit shortcuts (totally not just modified settings)
        elif cmdargs[0] == ('scedit'):
            if settings == {}:
                throwerror(f'No shortcuts were found, or there was an error reading settings.ini ({settingspath})')
                main()
            else:
                for key, value in settings.items():
                    if key.startswith('s_'):
                        print(f"{key[2:]} - {c.cyan}{value}{c.r}")

            print('which shortcut would you like to change? alternatively, you can type exit, list, remove, or add.')
            
            while True:
                setting = input(f'{c.cyan}scedit{c.r} {settings["pointerChar"]} ')
                
                if 's_'+setting in settings:
                    print('Enter a new command for this shortcut:')
                    newValue = input(f'{c.cyan}{setting}{c.r} {settings["pointerChar"]} ')
                    add_settings('s_'+setting,newValue)

                elif setting == 'exit':
                    break

                elif setting == 'add':
                    print('what would you like to type to activate the shortcut?')
                    newshortcutname = input(f'{c.cyan}new shortcut{c.r} {settings["pointerChar"]} ')
                    print('what command would you like to run for this shortcut?')
                    newshortcutcmd = input(f'{c.cyan}{newshortcutname}{c.r} {settings["pointerChar"]} ')
                    add_settings('s_'+newshortcutname,newshortcutcmd)

                elif setting == 'remove':
                    print('which shortcut would you like to remove?')
                    delshortcut = input(f'{c.cyan}scedit{c.r} {settings["pointerChar"]} ')
                    if 's_'+delshortcut in settings:
                        remove_settings('s_'+delshortcut)
                    else:
                        throwerror('Invalid shortcut.')

                elif setting == 'list':
                    for key, value in settings.items():
                        if key.startswith('s_'):
                            print(f"{key[2:]} - {c.cyan}{value}{c.r}")

                else:
                    throwerror('Invalid shortcut.')

        elif cmdargs[0] == ('kill yourself'):
            print('Ok, closing in 5 seconds...')
            time.sleep(5)
            exit()

        # shortcuts (added in 0.5-pre4h)
        elif 's_'+cmd in settings:
            subprocess.run(['bash','-c',settings['s_'+cmd]]) 

        # if none of the above commands were selected, it will run this (run any command inside the input)
            
        else:
            try:
                subprocess.run(['bash','-c',cmd])
            except Exception as e:
                fatalerror('An error has occured: '+e)
            
# run main function (moved from while loop to function in 0.3 so the user can be returned back to the shell in case anything goes wrong)
main()