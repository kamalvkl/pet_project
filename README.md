# servicerestart.py
The servicerestart.py functionality is to restart the services of the network orchestration containers in the DNAC and deploy the application packages.
The paramiko modules are used for the SSH connectivity to the orchestratror.
The user approval for the service restart and the package deploy is recorded.
Each instance of the network orchestration services are parsed and they are restarted.
The undeployed application packages are identified and picked the services are deployed for the same
