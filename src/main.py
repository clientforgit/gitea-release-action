import github_action_utils as gha_utils
from github_action_utils import get_user_input, set_output, get_env
import httpx
import sys
import re

defaults = {}

with gha_utils.group("My Group"):
  tag_name = get_user_input("tag_name")
  tag_name = re.sub(r'[^\t]', '', tag_name.strip()) if tag_name else None
  gha_utils.notice("tag_name: " + tag_name)
  owner = get_user_input("owner").strip()
  owner = owner.strip() if owner else None
  gha_utils.notice("owner: " + owner)
  repo = get_user_input("repo").strip()
  repo = repo.strip() if repo else None
  gha_utils.notice("repo: " + repo)
  if not tag_name or not owner or not repo:
    gha_utils.error(
        f"Cannot find one of required user inputs: tag_name, owner or repo", title="Missing requirements", file="src/main.py"
    )
    sys.exit()
  release_name = get_user_input("release_name")
  release_name = re.sub(r'[^\w]', ' ', release_name.strip()) if release_name else None
  gha_utils.notice("release_name: " + release_name)
  draft = get_user_input("draft") == 'true'
  prerelease = get_user_input("prerelease") == 'true'
  commitsh = get_user_input("commitsh")
  commitsh = commitsh.strip() if commitsh else None

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
  gha_utils.notice(url)
  headers = {'Authorization': 'token ' + access_token}

  response = httpx.post(url, headers=headers, json=body, verify=False) 
  response_json = response.json()
  if response.status_code in [200, 201]:
    set_output("id", response.json["id"])
    set_output("html_url", response.json["html_url"])
    set_output("upload_url", response.json["upload_url"])
  else:
    gha_utils.error(
        f"ERROR: {response.status_code} status code of server response", title="Request failure", file="src/main.py"
    )
    sys.exit()
