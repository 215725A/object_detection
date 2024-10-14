import yaml

def read(config_path):
    with open(config_path, 'r') as yml:
        config = yaml.safe_load(yml)
    
    return config
