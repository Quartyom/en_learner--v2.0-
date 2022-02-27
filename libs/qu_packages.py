import importlib

def install(package_name):
    try:
        importlib.import_module(package_name)
    except ImportError:
        import pip
        pip.main(['install', package_name])
