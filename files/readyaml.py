#! /usr/bin/env python

import yaml


def get_yamlconfig():
    with open("configration/myappConfig.yaml", 'r') as stream:
        try:
            yaml_data = yaml.load(stream)
            return yaml_data
        except yaml.YAMLError as exc:
            print(exc)


def readyamlcompilationcheck():
    return True


if __name__ == "__main__":
    get_yamlconfig()
