import yaml

from googleapiclient import discovery

service = discovery.build('compute', 'v1')
print('VM Instance starting')

file_obj = open("config.yaml", "r")
config = yaml.safe_load(file_obj)

# Project ID for this request.
project = config['project']
# The name of the zone for this request.
zone = config['zone']
# Name of the instance resource to start.
instance = config['instance']

command = input('command >>> ').strip()

if command == 'start':
    request = service.instances().start(
        project=project, zone=zone, instance=instance
    )
    response = request.execute()
    print('VM Instance started')
    print(response)
elif command == 'stop':
    request = service.instances().stop(
        project=project, zone=zone, instance=instance
    )
    response = request.execute()
    print('VM Instance stopped')
    print(response)
else:
    print(f'unknown command {command}')
