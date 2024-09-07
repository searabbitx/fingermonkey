# fingermonkey

A tool to detect versions of open source apps based on the world-readable files such as unminified javascript, css, static html or images.

## How does it work

1. First, fingermonkey iterates through all supplied files calculates their git hashes:

```bash
git hash-object <your-file>
```

2. Then it checks if those files exist in any revision of the supplied repository. The files that don't have corresponding `blob` objects in the repository are ignored.

3. Then it iterates through all the tags in the repository and gathers those that have at least one of the blob objects from step 2. in their tree.

```bash
# for each tag:
git ls-tree -r <tag>
```

4. Finally, fingermonkey will show top 10 tags with the highest number of matching blobs

## Usage

```bash
python fingermonkey.py REPOSITORY FILES/DIRECTORIES...
```
If you use a directory then fingermonkey will find all of the files in this directory recursively.

**NOTE**: The tool first checks if a file exists in any revision of the supplied. Files that don't exist in any revision are ignored.

### Example 1. Downloading as much stuff as possible :)

#### Preparation

Download all assets from couple of pages recursively:

```bash
wget -r -erobots=off https://superopensourceapp.example.com/some_page -P /tmp/some_page/
wget -r -erobots=off https://superopensourceapp.example.com/other_page -P /tmp/other_page/
# sometimes 404 pages are static, so try
wget -r -erobots=off https://superopensourceapp.example.com/idontexist123123 -P /tmp/404_page/
```

#### Running

Then run:
```bash
python fingermonkey.py ~/repos/SomeOpenSourceApp /tmp/some_page /tmp/other_page/ /tmp/404_page/
```

fingermonkey will pick up all files in specified directories recursively and ignore those, that don't exist in any revision of the repository.

### Example 1. Testing specific files

#### Preparation
Say that `SomeOpenSourceApp` is running on http://superopensourceapp.example.com and there's:
- an unminified javascript file at http://superopensourceapp.example.com/js/app.js
- an unminified css file at http://superopensourceapp.example.com/styles/main.css

First, download those files to some location
```bash
wget http://superopensourceapp.example.com/js/app.js -O /tmp/app.js
wget http://superopensourceapp.example.com/styles/main.css -O /tmp/main.css
```

Then clone the `SomeOpenSourceApp`'s repo to some location (say `~/repos/SomeOpenSourceApp`)

```bash
git clone https://imaginary.git.hosting.example.com/superopensourceapp ~/repos/SomeOpenSourceApp
```

#### Running the tool
Finally, to find possible versions of `SomeOpenSourceApp` based on versions of gathered files, run:
```bash
python fingermonkey.py ~/repos/SomeOpenSourceApp /tmp/app.js /tmp/main.css
```