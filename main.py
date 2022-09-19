import requests
from requests.auth import HTTPBasicAuth
import json

class jubs_automation:

    email_address = None
    account_id = None

    # Метод для парсинга полей в запросе.
    def task_fields_parse(self):
        url = "https://jaxel-inc.atlassian.net/rest/api/3/issue/TES-102"
        auth = HTTPBasicAuth("YOUR-EMAIL", "YOUR-TOKEN")

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth
        )

        if (response.json()['fields']['customfield_10198']['value'] == "Jaxel Russia" and
            response.json()['fields']['customfield_10199']['value'] == "Consulting"): 
            return response.json()['fields']['customfield_10130']
        else:
            return False

    # Метод для создания нового аккаунта в системе Atlassian Jira/Confluence.
    def create_new_account(self):
        self.email_address = self.task_fields_parse()
        print("email_address", self.email_address)
        url = "https://jaxel-inc.atlassian.net/rest/api/3/user"
        auth = HTTPBasicAuth("YOUR-EMAIL", "YOUR-TOKEN")

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if self.email_address != False and '@' in self.email_address:
            payload = json.dumps( {
                "emailAddress": self.email_address,
            })

            response = requests.request(
                "POST",
                url,
                data=payload,
                headers=headers,
                auth=auth
            )
            return response.json().get('accountId')
        else:
            return False

    # Метод для добавления аккаунта в группу системы Atlassian Jira/Confluence.
    def invite_account_to_group(self):
        self.account_id = self.create_new_account()
        print("account_id: ", self.account_id)
        url = "https://jaxel-inc.atlassian.net/rest/api/3/group/user"
        auth = HTTPBasicAuth("YOUR-EMAIL", "YOUR-TOKEN")

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if self.account_id != False and self.account_id != None:
            query = {
                'groupId': '9060a7ee-73f9-412c-b769-a68577e312a7'
            }

            payload = json.dumps({
                "accountId": self.account_id
            })

            response = requests.request(
                "POST",
                url,
                data=payload,
                headers=headers,
                params=query,
                auth=auth
            )
            
            return response.json()
        else:
            return False

jubs_automation().invite_account_to_group()

