import git

from .api import Search
from dotenv import load_dotenv
from arglite import parser as cliarg
from rich.progress import Progress, track

def clone(org, pattern):
    for item in track(Search().query(org, pattern), description = "Downloading repos..."):
        git.Repo.clone_from(item.url, item.name)

def main():
    org = cliarg.required.org
    pattern = cliarg.required.pattern
    clone(org, pattern)

if __name__ == "__main__":
    main()
