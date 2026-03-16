#To impliment: handle_get, handle_wheel_get, handle_wheel_local, handle_sdist_get, handle_sdist_local
import urllib.request
import json,zipfile,tarfile,platform,pathlib

def get_os_tags():
    system=platform.system()
    


def handle_get(args):
    module_name=str(args.module_name)
