import os
import inspect

# .NET framework versions supported by AAComm nuget package
NET48                   = 'net48'
NET60                   = 'net6.0'
NET80                   = 'net8.0'

NET_FRAMEWORK_CHOICES   = [NET48, NET60, NET80]
TARGET_FRAMEWORKS       = ["4.8", "6.0", "8.0"]
DEFAULT_NET_FRAMEWORK   = NET48

TARGET_FOLDER           = os.path.join(os.path.dirname(__file__), 'aacommpyDownloader-main')
NUGET_EXE               = 'nuget.exe'
NUGET_EXE_PATH          = os.path.join(TARGET_FOLDER, NUGET_EXE)

# nuget dependencies
YAML_DOT_NET            = 'YamlDotNet'
YAML_DOT_NET_48_SRC_VER = 'net47'
SYSTEM_IO_PORTS         = 'System.IO.Ports'

AGITO_AACOMM            = 'Agito.AAComm'
AACOMM_DLL              = 'AAComm.dll'
AACOMMSERVER            = 'AACommServer'

# 'aacommpy install/update' scripts will modify 'settings.py' to provide the full path to AAComm.dll and AACommServer.exe
AACOMM_DLL_PATH         = os.path.join(os.path.dirname(__file__), AACOMM_DLL)
AACOMM_SERVER_EXE_PATH  = os.path.join(os.path.dirname(__file__), f'{AACOMMSERVER}.exe')

# this function returns the name of a variable. 
# usage: nameof(AACOMM_DLL_PATH)[0]) # Output: AACOMM_DLL_PATH
# must be called within the local scope of the variable
def nameof(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [name for name, val in callers_local_vars if val is var]

AACOMM_DEF_NAME         = nameof(AACOMM_DLL_PATH)[0]
AACOMMSERVER_DEF_NAME   = nameof(AACOMM_SERVER_EXE_PATH)[0]