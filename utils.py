from yaml import load, Loader

def load_config(file):
    with open(file, 'rt') as f:
        data = load(f, Loader=Loader)
    return data