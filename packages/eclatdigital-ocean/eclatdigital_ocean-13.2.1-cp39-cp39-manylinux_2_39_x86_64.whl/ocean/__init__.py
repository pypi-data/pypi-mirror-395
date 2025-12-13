import  os
from pathlib import Path

# EXPORT EXAMPLES
__SCRIPT_DIR=os.path.dirname(os.path.abspath( __file__))
__example_dir=os.path.join(__SCRIPT_DIR, '_examples')

if os.path.exists(__example_dir):
    cwd=os.getcwd()
    os.chdir(__example_dir)
    __xmlsPath = [ os.path.join(__example_dir, name) for name in os.listdir(__example_dir) if name.endswith(".ocxml")]
    __key = [Path(name).stem for name in __xmlsPath]
    examples=dict(zip(__key, __xmlsPath))
    os.chdir(cwd)
else:
    print("Can't find %s folder", __example_dir)
    examples={}
    
# EXPORT OCLIB_PATH
OCLIB_PATH=os.path.join(__SCRIPT_DIR, 'data', 'libraries')

# EXPORT ABYSS
is_embeded_lib=True

abyss_lib_path=[]

if is_embeded_lib:
    embedded_lib=os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
    abyss_lib_path.append(embedded_lib)
else:
    if os.name == 'nt':#TODO: what if user choose a custom install dir ... ?
        abyss_lib_path.append(os.path.join(os.environ["ProgramFiles"],"Eclat-Digital Research","OCEAN 2025"))
    else:
        abyss_lib_path.append("/opt/ocean/2025/lib")

if os.name == 'nt':
    for p in abyss_lib_path:
        try:
            os.add_dll_directory(p)
        except Exception as e:
            print('Failed os.add_dll_directory(): '+ str(e))
            pass
    os.environ['PATH'] = ';'.join(abyss_lib_path) + ';' + os.environ.get('PATH', '')
    # print('Ocean loader: PATH={}'.format(str(os.environ['PATH'])))
else:
    os.environ['LD_LIBRARY_PATH'] = ':'.join(abyss_lib_path) + ':' + os.environ.get('LD_LIBRARY_PATH', '')

__all__=["examples", "OCLIB_PATH", "abyss", "utils"]
from . import abyss
from . import utils
