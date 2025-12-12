# apsfuncsRepo<!-- omit in toc -->

- [Summary](#summary)
- [Uploading a new version](#uploading-a-new-version)


## Summary
The working repository for the aspfuncs python package, which contains the shared functions to use for astrea's python software (those supported by the APU system)

## Uploading a new version
**To contribute to a new package version, please contact Nathaniel Hughes**

To upload a new version of the package to PyPI:
* Complete all changes and submit a pull request to merge to the main branch, ensure that any new package requirements have been added to the pyproject.toml file
* Once the pull request has been aproved, get the latest version of the main branch into your local environment
* Delete any existing contents of the dist folder
* Run the command **"py -m build"** in the terminal 
* Once the build has completed, run the command **"twine upload dist/*"** to upload to the PyPI repo

**An API token is needed for this, if you do not have one then contact Nathaniel Hughes to carry out the update on your behalf**