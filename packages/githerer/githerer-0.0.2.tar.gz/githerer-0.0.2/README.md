# The githerer

[![PyPI version](https://img.shields.io/pypi/v/githerer)](https://pypi.org/project/githerer/)

<img src="https://i.imgflip.com/adk2j6.jpg"/>

A command line tool for cloning all repositories in a given GitHub organization which meet
certain pattern matching formulae (at present, only if a repository name starts with
a given pattern, though `regex` incoming in a future release).

## Installation

Find this tool on `PyPI`: `python -m pip install githerer`

## Usage

Use the tool on the command line:
```
githerer --org <NAME_OF_ORG> --pattern <PATTERN_TO_MATCH>
```

As this queries the GitHub API, you'll need to have at least two environment variables set:
* `GITHUB_USER`: the username to provide to the API
* `GITHUB_TOKEN`: the token to use to access private repositories
  * Of course, for public repos in an org, no reason to provide either, really
