import sys
import json
import csv
from typing import Sequence
from ruamel.yaml import YAML


class Instances():
    def __init__(self):
        self.instances_dict = {"instances":  []}

    def add_host(self,host):
        self.instances_dict['instances'].append(host)

    def add_host_file(self,file_name):
        with open(f"{file_name}", "r") as file:
            for line in file:
                currentline = line.split(',')
                self.instances_dict['instances'].append({"name":currentline[0],"dns":[currentline[1]],"ip":[currentline[2].rstrip('\n')]})

    def create_instances_file(self):
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent(sequence=4,offset=2)
        with open(r'D:\ELK docker-compose script\instances.yml', 'w') as file:
            documents = yaml.dump(self.instances_dict, file)