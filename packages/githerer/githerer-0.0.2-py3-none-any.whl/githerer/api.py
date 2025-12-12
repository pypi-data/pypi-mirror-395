import os
import re
import json
import requests

from collections import namedtuple
Repo = namedtuple('Repo', ['name', 'url'])

class Search:

    GITHUB_URL = "https://api.github.com"

    def __request_headers(self) -> dict:
        return {
            "Accept": "application/json",
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
        }

    def __request_params(self, page: int = 1) -> dict:
        return {
            "user": os.getenv("GITHUB_USER"),
            "page": page
        }

    def query(self, org: str = "", pattern: str = "", page: int = 1):
        while True:
            request = requests.get(
                f"{self.GITHUB_URL}/orgs/{org}/repos",
                headers = self.__request_headers(),
                params = self.__request_params(page)
            )
            repos = json.loads(request.text)
            if not repos: break
            pattern = re.compile(pattern)
            for repo in repos:
                if pattern.match(repo["name"]):
                    yield(Repo(repo["name"], repo["ssh_url"]))
            page += 1

