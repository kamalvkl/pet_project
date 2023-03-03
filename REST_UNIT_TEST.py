import requests
import sys
import json

def TC_BRINGUP():
        global headers, cookie, resp
        url = "https://x.x.x.x/api/system/v1/identitymgmt/login"
        headers = {
          'Content-Type':"application/json"
          }
        resp = REST_API(head=headers)
        cookie = resp.call_api("GET", url, auth=1)
        print(cookie)

def UNIT_TEST():
        print(resp)
        url = input("Enter the URL:")
        method = input("Enter the method:")
        auth = input("Enter the auth flag(1/0):")
        head = input("Enter the header:")
        payload = input("Enter the payload:")
        headers['Cookie'] = cookie
        disc_count = resp.call_api(method, url, payload, auth=0)
        response_input = input("DO you want to GET the TASK output ? Y/N:")
        if response_input == "Y":
           url = input("Enter the URL:")
           task_status = resp.call_api("GET", url, auth = 0)
        else:
           print("TASK  output skipped as per the user request")

def TASK_TEST():
        url = input("Enter the URL:")
        task_status = resp.call_api("GET", url, auth = 0)

class REST_API:
 def __init__(self, **kwargs):
     self.headers = kwargs['head']
 def call_api(self, method, url, data="", auth=0, verify=False, task = "null"):
    if method == "GET":
           print("ENTERED GET METHOD")
           print(self.headers)
           if auth:
              response = requests.request(method, url, auth=("xxxx","xxxx"), headers=self.headers, verify=False)
              print(response.text)
              cookie = response.headers['set-Cookie']
              return cookie
           if not auth:
               print(self.headers)
               self.headers = input("Enter the header:")
               response = requests.request(method, url, headers=self.headers, verify=False)
               response = response.json()
               response = response['response']
               print(response)
               return response
    elif method == "POST":
       print(self.headers)
       print(data)
       response = requests.request(method, url, data = data, headers=self.headers, verify=False)
       print(response.text)
       return response
    elif method == "PUT":
       print(self.headers)
       print(data)
       self.headers = input("Enter the header:")
       response = requests.request(method, url, data = data, headers=self.headers, verify=False)
       print(response.text)
       return response
    elif method == "DELETE":
       print(self.headers)
       response = requests.request(method, url, headers = self.headers, verify = False)
       print(response.text)
       return response
    if task:
       print(self.headers)
       response = requests.request(method, url, headers=self.headers, verify = False)
       print(response.text)
       return reponse

if __name__ == '__main__':
      TC_BRINGUP()
      UNIT_TEST()
