import yaml

from types import SimpleNamespace

def yaml2dict(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    

config = yaml2dict("config.yaml")
config = SimpleNamespace(**config)