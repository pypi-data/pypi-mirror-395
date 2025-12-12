import os
import shutil
import subprocess
import threading
import time
import requests
import zipfile
import xml.etree.ElementTree as ET

from aacommpy.settings import NET40, NET48, NET60, NET80, SYSTEM_IO_PORTS, YAML_DOT_NET, YAML_DOT_NET_40_SRC_VER, YAML_DOT_NET_40_VER, YAML_DOT_NET_48_SRC_VER
from aacommpy.settings import AGITO_AACOMM, DEFAULT_NET_FRAMEWORK, NET_FRAMEWORK_CHOICES, NUGET_EXE, NUGET_EXE_PATH, TARGET_FOLDER
from aacommpy.settings import AACOMM_DLL, AACOMMSERVER, AACOMM_DEF_NAME, AACOMMSERVER_DEF_NAME

def dotnetfw(version: str = DEFAULT_NET_FRAMEWORK) -> None:
    if version not in NET_FRAMEWORK_CHOICES:
        raise ValueError(f".NET framework version {version} is not supported.")
    
    latest_version  = aacomm_nuget_version()
    source_dir      = os.path.join(TARGET_FOLDER, f"{AGITO_AACOMM}.{latest_version}")
    dest_dir        = os.path.dirname(__file__)    
    source_dir      = os.path.join(source_dir, 'lib', version)  
    dll_path        = os.path.join(source_dir, AACOMM_DLL)
    if not os.path.isfile(dll_path):
        raise FileNotFoundError(f"Could not find {AACOMM_DLL} in {source_dir}.")
    
    shutil.copy2(dll_path, dest_dir)
    print(f"The AAComm .NET target framework is {version}")

    #copy dependencies to the working directory according to the target version
    copy_nuget_dependencies(version, dest_dir)

    return None

def download_nuget_exe() -> None:
    os.makedirs(TARGET_FOLDER, exist_ok=True)  # Create the directory if it doesn't exist

    nuget_path = os.path.join(TARGET_FOLDER, NUGET_EXE)
    if os.path.exists(nuget_path):
        return None
    
    # Start the progress indicator in a separate thread
    progress_thread = threading.Thread(target=show_progress_indicator, args=(nuget_path,))
    progress_thread.start()

    # Perform the download
    print(f'downloading {NUGET_EXE}...')
    url = f'https://dist.nuget.org/win-x86-commandline/latest/{NUGET_EXE}'
    r = requests.get(url)
    with open(nuget_path, 'wb') as f:
        f.write(r.content)

    # Wait for the progress thread to complete
    progress_thread.join()

    print(f'{NUGET_EXE} downloaded successfully.')
    return None

def show_progress_indicator(nuget_path):
    while not os.path.exists(nuget_path):
        print('.', end='', flush=True)
        time.sleep(0.5)
    print('')

def download_aacomm_nuget(version: str = "", update: bool = False) -> None:
    # check if old version is installed and remove it if update is True
    installed = False
    for dirname in os.listdir(TARGET_FOLDER):
        if dirname.startswith(f'{AGITO_AACOMM}.') and os.path.isdir(os.path.join(TARGET_FOLDER, dirname)):
            installed = True
            old_version = dirname.split('.')[2:]
            old_version = '.'.join(old_version)
            break

    if update and installed:
        shutil.rmtree(os.path.join(TARGET_FOLDER, f'{AGITO_AACOMM}.{old_version}'))

    # Download the main package
    install_nuget_package(AGITO_AACOMM, version)

    # Extract the .nuspec file from the downloaded package
    aacomm_folder = f'{AGITO_AACOMM}.{aacomm_nuget_version()}'
    package_path = os.path.join(TARGET_FOLDER, aacomm_folder, f"{aacomm_folder}.nupkg")
    nuspec_path = extract_nuspec(package_path, TARGET_FOLDER)

    # Parse the .nuspec file to get the dependencies
    dependencies = parse_nuspec(nuspec_path)

    # Install each dependency with the exact version
    for id, version in dependencies:
        print(f'Installing {id} version {version}...')
        install_nuget_package(id, version)

    print('All dependencies installed.')

    # Copy the AACommServer.exe and AACommServerAPI.dll to the working directory
    aacs_dir = os.path.join(TARGET_FOLDER, aacomm_folder, 'build', AACOMMSERVER)
    dest_dir = os.path.dirname(__file__)
    shutil.copy2(os.path.join(aacs_dir, f'{AACOMMSERVER}.exe'), dest_dir)
    shutil.copy2(os.path.join(aacs_dir, f'{AACOMMSERVER}API.dll'), dest_dir)

    # copy AAComm.dll + dependencies to the working directory        
    dotnetfw()

    # modify settings.py to include the full path to AAComm.dll and AACommServer.exe
    aacomm_dll_path         = os.path.join(dest_dir, AACOMM_DLL).replace('\\', '/')
    aacomm_server_exe_path  = os.path.join(dest_dir, f'{AACOMMSERVER}.exe').replace('\\', '/')
    settings_path           = os.path.join(os.path.dirname(__file__), 'settings.py')
    aacomm_def_name         = AACOMM_DEF_NAME
    aacommserver_def_name   = AACOMMSERVER_DEF_NAME

    with open(settings_path, 'r+') as settings_file:
        lines = settings_file.readlines()
        settings_file.seek(0)

        for line in lines:
            if line.startswith(aacomm_def_name):
                settings_file.write(f"{aacomm_def_name}\t\t\t= '{aacomm_dll_path}'\n")
            elif line.startswith(aacommserver_def_name):
                settings_file.write(f"{aacommserver_def_name}\t= '{aacomm_server_exe_path}'\n")
            else:
                settings_file.write(line)
                
        settings_file.truncate()

    return None

def install_nuget_package(id, version):
    nuget_cmd = [
        NUGET_EXE_PATH,
        'install',
        id,
        '-OutputDirectory', TARGET_FOLDER,
        '-Source', 'https://api.nuget.org/v3/index.json',
    ]

    if version != "":
        nuget_cmd.extend(['-Version', version])

    subprocess.run(nuget_cmd, check=True)

def extract_nuspec(package_path, output_dir):
    with zipfile.ZipFile(package_path, 'r') as zip_ref:
        nuspec_file = [f for f in zip_ref.namelist() if f.endswith('.nuspec')][0]
        zip_ref.extract(nuspec_file, output_dir)
    return os.path.join(output_dir, nuspec_file)

def parse_nuspec(nuspec_path):
    tree = ET.parse(nuspec_path)
    root = tree.getroot()
    namespace = {'default': 'http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd'}
    dependencies = set()

    for group in root.findall('.//default:dependencies/default:group', namespace):
        for dependency in group.findall('default:dependency', namespace):
            id = dependency.get('id')
            version = dependency.get('version').strip('[]')
            dependencies.add((id, version))
    
    return list(dependencies)

def aacomm_nuget_version() -> str:
    if not os.path.exists(NUGET_EXE_PATH):
        raise RuntimeError("Nuget executable not found. Please run the 'install' command.")
    
    installed = False
    latest_version = None
    for dirname in os.listdir(TARGET_FOLDER):
        if dirname.startswith(f'{AGITO_AACOMM}.') and os.path.isdir(os.path.join(TARGET_FOLDER, dirname)):
            installed = True
            version = dirname.split('.')[2:]
            latest_version = '.'.join(version)
            print(f"The installed version of {AGITO_AACOMM} is {latest_version}.")
            break

    if not installed:
        raise RuntimeError(f'{AGITO_AACOMM} nuget package is not installed.')
    
    return latest_version


def copy_nuget_dependencies(version, dest_dir):
    for dir in os.listdir(TARGET_FOLDER):
        if dir.startswith(YAML_DOT_NET) and YAML_DOT_NET_40_VER not in dir:
            YAML_DOT_NET_VER = dir.split('.')[1:]
            YAML_DOT_NET_VER = '.'.join(YAML_DOT_NET_VER)
        elif dir.startswith(SYSTEM_IO_PORTS):
            SYSTEM_IO_PORTS_VERSION = dir.split('.')[3:]
            SYSTEM_IO_PORTS_VERSION = '.'.join(SYSTEM_IO_PORTS_VERSION)

    if version == NET40:
        copy_dll(YAML_DOT_NET   , YAML_DOT_NET_40_VER       , YAML_DOT_NET_40_SRC_VER, dest_dir)
    elif version == NET48:
        copy_dll(YAML_DOT_NET   , YAML_DOT_NET_VER          , YAML_DOT_NET_48_SRC_VER, dest_dir)
    elif version == NET60 or version == NET80:
        copy_dll(YAML_DOT_NET   , YAML_DOT_NET_VER          , version, dest_dir)
        copy_dll(SYSTEM_IO_PORTS, SYSTEM_IO_PORTS_VERSION   , version, dest_dir)
    else:
        raise ValueError(f"Unsupported .NET target framework version: {version}")

def copy_dll(package_name, package_version, framework_version, dest_dir):
    dll_source_dir = os.path.join(TARGET_FOLDER, f"{package_name}.{package_version}", "lib", framework_version)
    dll_path = os.path.join(dll_source_dir, f"{package_name}.dll")

    if not os.path.isfile(dll_path):
        raise FileNotFoundError(f"Could not find {package_name}.dll in {dll_source_dir}.")

    shutil.copy2(dll_path, dest_dir)
    print(f"The {package_name} .NET target framework is {framework_version}")