import paramiko
import re
import time
import sys

class connection:
    def __init__(self, method, host, port, user, pw):
        self.method = method
        self.host = host
        self.port = port
        self.user = user
        self.pw = pw
        print("hello")
    def connect(self, **kwargs):
          try:	 
            if self.method == "ssh":
              ssh=paramiko.SSHClient()
              ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
              print("Performing ssh connection to the cluster ......")
              ssh.connect(self.host,self.port,self.user,self.pw)
              print("SSH Connected")
              return ssh
          except:
              print("Could not ssh to the cluster...Please check the reachability and the inputs provided above")
              sys.exit(0)
    def execute(self, **kwargs):
           try:
            if self.method == "ssh" and kwargs['ob'] and kwargs['comm']:
             stdin,stdout,stderr=kwargs['ob'].exec_command(kwargs['comm'])
             outlines=stdout.readlines()
             resp=''.join(outlines)
             print("##############################################################################")
             print(resp)
             print("##############################################################################") 
             return resp
           except:
             print("Command could not be excuted...Please check the command and try again")
    def user_prompt(self, item, user_reponse):
           if user_response == "y":
                 #package_D = package_D + " {}".format(item)
                 return item
           elif user_response == "n":
                print("{} package not selected for upgrade".format(item))
                return "noupg"
           else:
                 print("Make sure you enter y/n")
                 return "negative"
    def user_prompts(self, service_resp):
           if service_resp == "y":
                 #package_D = package_D + " {}".format(item)
                 return "allow"
           elif service_resp == "n":
                #print("{} package not selected for upgrade".format(item))
                return "disallow"
           else:
                 print("Make sure you enter y/n")
                 return "negative"

if __name__ == '__main__':
      cluster_ip = input("Enter the cluster ip:")
      cluster_port = int(input("Enter the cluster port:"))
      cluster_un = input("Enter the cluster username:")
      cluster_pw = input("Enter the cluster password:")
      ssh_conn = connection("ssh",cluster_ip,cluster_port,cluster_un,cluster_pw)
      obj = ssh_conn.connect()
      ssh_conn.execute(ob=obj,comm="magctl appstack status")
      #out = ssh_conn.execute(ob=obj,comm="magctl appstack status | grep -v Running")
      out = ssh_conn.execute(ob=obj,comm="magctl appstack status | grep network")
      service_resp = input("Do you want to enter into the service restart section y/n?")
      ser_resp_out = ssh_conn.user_prompts(service_resp)
      while ser_resp_out == "negative":
        service_resp = input("Do you want to enter into the service restart section y/n?")
        ser_resp_out = ssh_conn.user_prompts(service_resp)
      if ser_resp_out == "allow":
       i = 0
       try:
        for line in out.split("\n"):
          if re.search(r'(\w+)\s+(.*)(\s+\d\/\d).*',line):
             i = i+1
             match = re.search(r'(\w+)\s+(.*)(\s+\d\/\d).*',line)
             print("Restarting services for {}" .format(match.group(2)))
             out = ssh_conn.execute(connexec=1,ob=obj,comm="magctl service restart -d {}" .format(match.group(2)))
          #else:
          #   print("The service you are looking for is not found")
        if i > 1:
         print("Waiting for 2 mins for the services to restart..............")
         time.sleep(5)
        else:
         print("No services available to restart .... All are un running state")
       except:
        print("An Error ocured during the service restart")
      else:
        print("Skipping the service restart section")
      print("**************** Entering the package deploy section ********************")
      out = ssh_conn.execute(ob=obj,comm="maglev package status")
      #package_list= ['NCP-Base','NCP-Services','Network Controller Platform','Automation - Base','Automation - Device Onboarding','Automation - Image Management','Assurance - Path Trace','Automation - Sensor','Automation - SD Access','Command Runner','Automation - Application Policy','Network Data Platform - Core','Network Data Platform - Base Analytics','Network Data Platform - Manager','Assurance - Base']
      package_list = ['ncp-system','automation-core','network-visibility','base-provision-core','device-onboarding','image-management','path-trace','sensor-automation','sd-access','command-runner','application-policy','ndp-platform','ndp-base-analytics','ndp-ui','assurance']
      #package_list = ['base-provision-core','sensor-automation','sd-access']
      package_ND = []
      package_D = ""
      final_list = ""
      for line in out.split("\n"):
          if re.search(r'(\w+\-\w+\-\w+|\w+|\w+\-\w+)\s+(\w+|\w+\s\-\s\w+|\w+\s\w+|\w+\s\w+\s\w+\s\-\s\w+|\w+\s\w+\s\w+\s\-\s\w+\s\w+|\w+\s\-\s\w+\s\w+)\s+(\-|\d\.\d\.\d\.\d+)\s+(\-|\d\.\d\.\d\.\d+)\s+(\w+)',line):
             match = re.search(r'(\w+\-\w+\-\w+|\w+|\w+\-\w+)\s+(\w+|\w+\s\-\s\w+|\w+\s\w+|\w+\s\w+\s\w+\s\-\s\w+|\w+\s\w+\s\w+\s\-\s\w+\s\w+|\w+\s\-\s\w+\s\w+)\s+(\-|\d\.\d\.\d\.\d+)\s+(\-|\d\.\d\.\d\.\d+)\s+(\w+)',line)
             if match.group(5) != "DEPLOYED":
                #print('package:{} Deployed:{} Available:{} Status:{}' .format(match.group(1),match.group(3),match.group(4),match.group(5)))
                package_ND.append(match.group(1))
      print("**************** List of undeployed packages *******************")
      print(package_ND)
      for item in package_list:
          if item in package_ND:
             print("*********************************************************************")
             user_response = input("Do you want to deploy {} package y/n?".format(item))
             print("*********************************************************************")
             output = ssh_conn.user_prompt(item, user_response)
             while output == "negative":
                user_response = input("Do you want to deploy {} package y/n?".format(item))
                output = ssh_conn.user_prompt(item, user_response)
             package_D = package_D + " {}".format(output)
      #print(type(package_D))
      new_list = package_D.replace("noupg","")
      print(new_list)
      ssh_conn.execute(ob = obj, comm = "maglev package deploy {} --force".format(new_list))
      #ssh_conn.execute(obj = obj, comm = "maglev package status")
       
      
