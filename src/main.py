import github_action_utils as gha_utils
from github_action_utils import get_user_input, set_output, get_env
import httpx
import sys

defaults = {}

with gha_utils.group("My Group"):
  tag_name = get_user_input("tag_name") 
  if not tag_name:
    gha_utils.error(
        f"Cannot find specified tag name '{tag_name}'", title="Missing tag name", file="src/main.py"
    )
    sys.exit()
  release_name = get_user_input("release_name")
  owner = get_user_input("owner")
  repo = get_user_input("repo")
  draft = get_user_input("draft") == 'true'
  prerelease = get_user_input("prerelease") == 'true'
  commitsh = get_user_input("commitsh")

  gitea_domain = get_env("GITEA_DOMAIN")
  gha_utils.notice("gitea_domain: " + gitea_domain)
  access_token = get_env("ACCESS_TOKEN")
  gha_utils.notice("access_token: " + access_token)
  body = {"tag_name": tag_name, 
          "release_name": release_name,
          "owner": owner,
          "repo": repo,
          "draft": draft,
          "prerelease": prerelease,
          "commitsh": commitsh
         }
  
  url = f'https://{gitea_domain}/api/v1/repos/{owner}/{repo}/releases'
  headers = {'Authorization': 'token ' + access_token}

  response = httpx.post(url, headers=headers, json=body, verify=False) 
  response_json = response.json()
  if response.status_code == 200:
    set_output("id", response.json["id"])
    set_output("html_url", response.json["html_url"])
    set_output("upload_url", response.json["upload_url"])
  else:
    gha_utils.error(
        f"ERROR: {response.status_code} status code of server response", title="Request failure", file="src/main.py"
    )
    sys.exit()
