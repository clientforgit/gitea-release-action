import github_action_utils as gha_utils, get_user_input

with gha_utils.group("My Group"):
  gha_utils.notice(get_user_input("tag_name"))
  gha_utils.notice(get_user_input("release_name"))
  gha_utils.notice("successful")
