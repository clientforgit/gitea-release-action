const core = require('@actions/core');
const { GitHub, context } = require('@actions/github');
const fs = require('fs');

async function run() {
  try {
    // Get authenticated GitHub client (Ocktokit): https://github.com/actions/toolkit/tree/master/packages/github#usage
    const github = new GitHub(process.env.GITHUB_TOKEN);
    const auth_token = process.env.ACCESS_TOKEN;
    const gitea_domain = process.env.gitea_domain;

    // Get owner and repo from context of payload that triggered the action
    const { owner: currentOwner, repo: currentRepo } = context.repo;

    // Get the inputs from the workflow file: https://github.com/actions/toolkit/tree/master/packages/core#inputsoutputs
    const tagName = core.getInput('tag_name', { required: true });

    // This removes the 'refs/tags' portion of the string, i.e. from 'refs/tags/v1.10.15' to 'v1.10.15'
    const tag = tagName.replace('refs/tags/', '');
    const releaseName = core.getInput('release_name', { required: false }).replace('refs/tags/', '');
    const body = core.getInput('body', { required: false });
    const draft = core.getInput('draft', { required: false }) === 'true';
    const prerelease = core.getInput('prerelease', { required: false }) === 'true';
    const commitish = core.getInput('commitish', { required: false }) || context.sha;

    const bodyPath = core.getInput('body_path', { required: false });
    const owner = core.getInput('owner', { required: false }) || currentOwner;
    const repo = core.getInput('repo', { required: false }) || currentRepo;
    let bodyFileContent = null;
    if (bodyPath !== '' && !!bodyPath) {
      try {
        bodyFileContent = fs.readFileSync(bodyPath, { encoding: 'utf8' });
      } catch (error) {
        core.setFailed(error.message);
      }
    }

    // Create a release
    // API Documentation: https://developer.github.com/v3/repos/releases/#create-a-release
    // Octokit Documentation: https://octokit.github.io/rest.js/#octokit-routes-repos-create-release
    let xhr = new XMLHttpRequest();
    var url = 'https://${gitea_domain}/api/v1/repos/${owner}/${repo}/releases';
    xhr.open('POST', url, false);
    xhr.setRequestHeader("Authorization", auth_token);
    xhr.send(JSON.stringify({"tag_name": tag, "name": releaseName, "draft": draft, "prerelease": prerelease, "target_commitish": commitish}));
    try {
        xhr.send();
        if (xhr.status !== 200) {
            core.setFailed(`Error ${xhr.status}: ${xhr.statusText}`);
        } else {
            var response = JSON.parse(xhr.responseText);
            core.setOutput('id', response['id']);
            core.setOutput('html_url', response['html_url']);
            core.setOutput('upload_url', response['url']);
        }
    } catch(err) {
        core.setFailed(err.message);;
    }
} catch (error) {
    core.setFailed(error.message);
}}

module.exports = run;
