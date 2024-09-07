- [x] 1. verify that all supplied files exist at any revision (there are blob objects for all files) and ignore files that don't exist.
     (for example, if a file has a has fe0a0d3d..., check if `.git/fe/0a0d3d...` exists)
- [ ] 2. try to automate stuff – spider the website and download as many assets as possible -> then run the tool against the list of gathered assets -> assets that are not in the repo will be ignored after 1. anyways!

- [x] 3. allow to pass a folder with files instead of a list of files

- [ ] 4. allow to specify verbosity
