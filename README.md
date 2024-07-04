# gitea-release-action
action for gitea releases

# Inputs
- `tag_name`: The name of the tag for this release
- `release_name`: The name of the release
- `body`: Text describing the contents of the release. Optional, and not needed if using `body_path`.
- `body_path`: A file with contents describing the release. Optional, and not needed if using `body`.
- `draft`: `true` to create a draft (unpublished) release, `false` to create a published one. Default: `false`
- `prerelease`: `true` to identify the release as a prerelease. `false` to identify the release as a full release. Default: `false`
- `commitish` : Any branch or commit SHA the Git tag is created from, unused if the Git tag already exists. Default: SHA of current commit

# Outputs
- `id`: The release ID
- `html_url`: The URL users can navigate to in order to view the release. i.e. 
- `upload_url`: The URL for uploading assets to the release, which could be used by GitHub Actions for additional uses

# Example
```yaml
on: [push]

name: Create Release

jobs:
  build:
    name: Create Release
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Create Release
        id: create_release
        uses: clientforgit/gitea-release-action@latest
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # This token is provided by Actions, you do not need to create your own token
          ACCESS_TOKEN: ${{ secrets.ACCESS_TOKEN }} # Create your own access token, by following this section - https://docs.gitea.com/development/api-usage#generating-and-listing-api-tokens
        with:
          tag_name: latest
          release_name: TEST
          draft: false
          prerelease: false
```
