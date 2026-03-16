from pathlib import Path
import sys,platform,os,ctypes


traits_path = Path.home() / ".ethos" / "traits"
if not traits_path.exists():
    traits_path.mkdir(parents=True, exist_ok=True)

def create_enviroment():
    env={}
    list_traits=os.listdir(traits_path)
    hard_traits=[]
    hard_traits_ext=""
    if platform.system()=="Darwin":
        hard_traits_ext=(".so",".dylib")
    elif platform.system()=="Linux":
        hard_traits_ext=".so"
    elif platform.system()=="Windows":
        hard_traits_ext=".dll"
    for i in list_traits:
        if i.endswith(hard_traits_ext):
            hard_traits.append(i)
            library = ctypes.CDLL(str(traits_path / i))
            env[Path(i).stem] = library
    
    return env

def run(python_code,memory_box=None):
    sys.path.append(str(traits_path))
    if not python_code or python_code=="":
        return
    if not memory_box:
        memory_box=create_enviroment()
    try:
        exec(python_code,memory_box)
    except Exception as e:
        print("Ethos Runtime Error:",e)
