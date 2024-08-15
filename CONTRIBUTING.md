# How to Contribute

We'd love to accept your patches and contributions to this project. There are
just a few small guidelines you need to follow.

## Contributor License Agreement

Contributions to this project must be accompanied by a Contributor License
Agreement. You (or your employer) retain the copyright to your contribution;
this simply gives us permission to use and redistribute your contributions as
part of the project. Head over to <https://cla.developers.google.com/> to see
your current agreements on file or to sign a new one.

You generally only need to submit a CLA once, so if you've already submitted one
(even if it was for a different project), you probably don't need to do it
again.

## Notebook Template

If you're creating a Jupyter Notebook, use `/gemini/getting-started/intro_gemini_python.ipynb` as a template.

## Code Quality Checks

All notebooks in this project are checked for formatting and style, to ensure a
consistent experience. To test notebooks prior to submitting a pull request,
you can follow these steps.

From a command-line terminal (e.g. from Vertex Workbench or locally), install
the code analysis tools:

```shell
pip3 install --user -U nbqa black flake8 isort pyupgrade git+https://github.com/tensorflow/docs
```

You'll likely need to add the directory where these were installed to your PATH:

```shell
export PATH="$HOME/.local/bin:$PATH"
```

Then, set an environment variable for your notebook (or directory):

```shell
export notebook="your-notebook.ipynb"
```

Finally, run this code block to check for errors. Each step will attempt to
automatically fix any issues. If the fixes can't be performed automatically,
then you will need to manually address them before submitting your PR.

Note: For official, only submit one notebook per PR.

```shell
python3 -m pip install -U -r .github/workflows/notebook_linter/requirements.txt
.github/workflows/notebook_linter/run_linter.sh
```

```shell
python3 -m pip install --upgrade nox
nox -s format
```

## Code Reviews

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.

## Community Guidelines

This project follows [Google's Open Source Community
Guidelines](https://opensource.google/conduct/).

## Contributor Guide

If you are new to contributing to open source, you can find helpful information in this contributor guide.

You may follow these steps to contribute:

1. **Fork the official repository.** This will create a copy of the official repository in your own account.
2. **Sync the branches.** This will ensure that your copy of the repository is up-to-date with the latest changes from the official repository.
3. **Work on your forked repository's feature branch.** This is where you will make your changes to the code.
4. **Commit your updates on your forked repository's feature branch.** This will save your changes to your copy of the repository.
5. **Submit a pull request to the official repository's main branch.** This will request that your changes be merged into the official repository.
6. **Resolve any linting errors.** This will ensure that your changes are formatted correctly.

Here are some additional things to keep in mind during the process:

- **Read the [Google's Open Source Community Guidelines](https://opensource.google/conduct/).** The contribution guidelines will provide you with more information about the project and how to contribute.
- **Test your changes.** Before you submit a pull request, make sure that your changes work as expected.
- **Be patient.** It may take some time for your pull request to be reviewed and merged.

---

## For Google Employees

Complete the following steps to register your GitHub account and be added as a contributor to this repository.

1. Register your GitHub account at [go/github](https://goto.google.com/github)

1. Once you have registered, go to [go/github-googlecloudplatform](https://goto.google.com/github-googlecloudplatform)and request to join the GoogleCloudPlatform organization. Check the box "I need write access on a public repository".

1. You'll receive an email to your GitHub registered email to approve the request to join. Approve it.

1. Request to join this team [GoogleCloudPlatform/teams/generative-ai-samples-contributors](https://github.com/orgs/GoogleCloudPlatform/teams/generative-ai-samples-contributors/members)
