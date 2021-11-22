from recordclass import recordclass
import yaml

path_to_settings = 'settings.yaml'

with open(path_to_settings) as fp:
    y = yaml.safe_load(fp)
    Settings = recordclass('Settings', y)
    settings = Settings(**y)


def save_to_file(settings):
    with open(path_to_settings, 'w') as fp:
        fp.write(yaml.dump(settings))
