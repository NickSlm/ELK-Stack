from copy import copy
from msilib import sequence
from operator import le
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
        self.docker_compose = {"version":"2.2","services":{},"volumes":{"certs":{"driver":"local"}},"networks":{"elastic":{"driver":"bridge"}}}

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

    def create_evn_file(self,directory_path):
        dotenv.set_key(f'{directory_path}\.env',"VERSION","7.16.2")
        dotenv.set_key(f'{directory_path}\.env',"COMPOSE_PROJECT_NAME","es")
        dotenv.set_key(f'{directory_path}\.env',"CERTS_DIR","/usr/share/elasticsearch/config/certificates" )

    def create_certs(self,directory_path):
        copyfile(r"D:\ELK docker-compose script\create-certs.yml",f"{directory_path}\create-certs.yml")

    def create_docker_compose(self,directory_path):
        if self.hosts_data['instances'][0]['name'] in self.hosts['elasticsearch']:
                self.docker_compose['volumes'].update({f"{self.hosts_data['instances'][0]['name']}_data":{'driver':'local'}})
                self.docker_compose['services'].update(
                    {self.hosts_data['instances'][0]['name']:
                    {
                    "image": "docker.elastic.co/elasticsearch/elasticsearch:${VERSION}",
                    "container_name":self.hosts_data['instances'][0]['name'],
                    "environment":{
                        "node.name":f"{self.hosts_data['instances'][0]['name']}",
                        "cluster.name": "es-docker-cluster",
                        "discovery.seed_hosts": f"{','.join(self.hosts['elasticsearch'])}",
                        "cluster.initial_master_nodes": f"{','.join(self.hosts['elasticsearch'])}",
                        "bootstrap.memory_lock":"true",
                        "ES_JAVA_OPTS":"-Xms512m -Xmx512m",
                        "xpack.license.self_generated.type":"trial",
                        "xpack.security.enabled":"true",
                        "xpack.security.http.ssl.enabled":"true",
                        "xpack.security.http.ssl.key":f"$CERTS_DIR/{self.hosts_data['instances'][0]['name']}/{self.hosts_data['instances'][0]['name']}.key",
                        "xpack.security.http.ssl.certificate_authorities":"$CERTS_DIR/ca/ca.crt",
                        "xpack.security.http.ssl.certificate":f"$CERTS_DIR/{self.hosts_data['instances'][0]['name']}/{self.hosts_data['instances'][0]['name']}.crt",
                        "xpack.security.transport.ssl.enabled":"true",
                        "xpack.security.transport.ssl.verification_mode":"certificate",
                        "xpack.security.transport.ssl.certificate_authorities":"$CERTS_DIR/ca/ca.crt",
                        "xpack.security.transport.ssl.certificate":f"$CERTS_DIR/{self.hosts_data['instances'][0]['name']}/{self.hosts_data['instances'][0]['name']}.crt",
                        "xpack.security.transport.ssl.key":f"$CERTS_DIR/{self.hosts_data['instances'][0]['name']}/{self.hosts_data['instances'][0]['name']}.key",
                    },
                    "ulimits":{"memlock":{"soft": -1,"hard": -1}},
                    "volumes": [f"{self.hosts_data['instances'][0]['name']}_data:/usr/share/elasticsearch/data", "certs:$CERTS_DIR"],
                    "ports": ['9200:9200'],
                    "networks":["elastic"],
                    "healthcheck": {"test": "curl --cacert $CERTS_DIR/ca/ca.crt -s https://localhost:9200 >/dev/null; if [[ $$? == 52 ]]; then echo 0; else echo 1; fi",
                        "interval": "30s",
                        "timeout": "10s",
                        "retries": 5}}})

        for host in range(1,len(self.hosts_data['instances'])):
            # Elasticsearch nodes
            if self.hosts_data['instances'][host]['name'] in self.hosts['elasticsearch']:
                self.docker_compose['volumes'].update({f"{self.hosts_data['instances'][host]['name']}_data":{'driver':'local'}})
                self.docker_compose['services'].update(
                    {self.hosts_data['instances'][host]['name']:
                    {
                    "image": "docker.elastic.co/elasticsearch/elasticsearch:${VERSION}",
                    "container_name":self.hosts_data['instances'][host]['name'],
                    "environment":{
                        "node.name":f"{self.hosts_data['instances'][host]['name']}",
                        "cluster.name": "es-docker-cluster",
                        "discovery.seed_hosts": f"{','.join(self.hosts['elasticsearch'])}",
                        "cluster.initial_master_nodes": f"{','.join(self.hosts['elasticsearch'])}",
                        "bootstrap.memory_lock":"true",
                        "ES_JAVA_OPTS":"-Xms512m -Xmx512m",
                        "xpack.license.self_generated.type":"trial",
                        "xpack.security.enabled":"true",
                        "xpack.security.http.ssl.enabled":"true",
                        "xpack.security.http.ssl.key":f"$CERTS_DIR/{self.hosts_data['instances'][host]['name']}/{self.hosts_data['instances'][host]['name']}.key",
                        "xpack.security.http.ssl.certificate_authorities":"$CERTS_DIR/ca/ca.crt",
                        "xpack.security.http.ssl.certificate":f"$CERTS_DIR/{self.hosts_data['instances'][host]['name']}/{self.hosts_data['instances'][host]['name']}.crt",
                        "xpack.security.transport.ssl.enabled":"true",
                        "xpack.security.transport.ssl.verification_mode":"certificate",
                        "xpack.security.transport.ssl.certificate_authorities":"$CERTS_DIR/ca/ca.crt",
                        "xpack.security.transport.ssl.certificate":f"$CERTS_DIR/{self.hosts_data['instances'][host]['name']}/{self.hosts_data['instances'][host]['name']}.crt",
                        "xpack.security.transport.ssl.key":f"$CERTS_DIR/{self.hosts_data['instances'][host]['name']}/{self.hosts_data['instances'][host]['name']}.key",  
                    },
                    "ulimits":{"memlock":{"soft": -1,"hard": -1}},
                    "volumes": [f"{self.hosts_data['instances'][host]['name']}_data:/usr/share/elasticsearch/data", "certs:$CERTS_DIR"],
                    "networks":["elastic"]}})
            # Kibana nodes
            if self.hosts_data['instances'][host]['name'] in self.hosts['kibana']:    
                self.docker_compose['services'].update(
                    {self.hosts_data['instances'][host]['name']:{
                        "image":"docker.elastic.co/kibana/kibana:${VERSION}",
                        "container_name":self.hosts_data['instances'][host]['name'],
                        "depends_on": {self.hosts['elasticsearch'][0]:{"condition": "service_healthy"}},
                        "ports":["5601:5601"],
                        "environment":{
                            "SERVERNAME": "localhost",
                            "ELASTICSEARCH_URL": f"https://{self.hosts['elasticsearch'][0]}:9200",
                            "ELASTICSEARCH_HOSTS": f"https://{self.hosts['elasticsearch'][0]}:9200",
                            "ELASTICSEARCH_USERNAME": "kibana_system",
                            "ELASTICSEARCH_PASSWORD": "CHANGEME",
                            "ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES": "$CERTS_DIR/ca/ca.crt",
                            "SERVER_SSL_ENABLED": "true",
                            "SERVER_SSL_KEY": f"$CERTS_DIR/{self.hosts_data['instances'][host]['name']}/{self.hosts_data['instances'][host]['name']}.key",
                            "SERVER_SSL_CERTIFICATE": f"$CERTS_DIR/{self.hosts_data['instances'][host]['name']}/{self.hosts_data['instances'][host]['name']}.crt"
                        },
                        "volumes":["certs:$CERTS_DIR"],
                        "networks":["elastic"]
                    }
                    }
                )
        # Create docker-compose.yml
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent(sequence=4, offset=2)
        with open(fr'{directory_path}\docker-compose.yml', 'w') as file:
            yaml.dump(self.docker_compose, file)


