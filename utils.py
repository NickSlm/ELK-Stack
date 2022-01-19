from copy import copy
from msilib import sequence
import sys
import json
import csv
from shutil import copyfile
from turtle import dot
from typing import Sequence
from venv import create
from ruamel.yaml import YAML
import dotenv

class Configuration():
    def __init__(self):
        self.hosts = {"kibana":[],"elasticsearch":[]}
        self.hosts_data = {"instances": []}
        self.docker_compose = {"Version":"2.2","services":{}}

    def add_host(self,host):
        self.hosts_data['instances'].append(host)

    def add_host_file(self,file_name):
        with open(f"{file_name}", "r") as file:
            for line in file:
                currentline = line.split(',')
                if currentline[3].rstrip('\n') == 'kb':
                    self.hosts['kibana'].append(currentline[0])
                if currentline[3].rstrip('\n') == 'es':
                    self.hosts['elasticsearch'].append(currentline[0])
                self.hosts_data['instances'].append({"name":currentline[0],"dns":[currentline[1]],"ip":[currentline[2]]})

    def create_instances_file(self,directory_path):
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent(sequence=4,offset=2)
        with open(rf'{directory_path}\instances.yml', 'w') as file:
            yaml.dump(self.hosts_data, file)

    def create_conf_files(self,directory_path):
        dotenv.set_key(f'{directory_path}\.env',"VERSION","7.16.2")
        dotenv.set_key(f'{directory_path}\.env',"COMPOSE_PROJECT_NAME","es")
        dotenv.set_key(f'{directory_path}\.env',"CERTS_DIR","/usr/share/elasticsearch/config/certificates" )

    def create_certs(self,directory_path):
        copyfile(r'D:\ELK docker-compose script\create_certs.yml',directory_path)

    def create_docker_compose(self):
        for host in self.hosts_data['instances']:
            # elasticsearch
            self.docker_compose['services'].update({host['name']:{"container_name":host['name'],"image": "docker.elastic.co/elasticsearch/elasticsearch:$VERSION",
            "environment":[f"node.nodename={host['name']}"]}})

            # kibana
        
        # yaml = YAML()
        # yaml.explicit_start = True
        # yaml.indent(sequence=4, offset=2)
        # with open(r'D:\ELK docker-compose script\docker-compose.yml', 'w') as file:
        #     yaml.dump(self.docker_compose, file)


