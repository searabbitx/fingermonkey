# fingermonkey

A tool to detect versions of open source apps based on the world-readable files such as unminified javascript, css or static html.

## Usage

```bash
python fingermonkey.py REPOSITORY FILES/DIRECTORIES...
```
If you use a directory then fingermonkey will find all of the files in this directory recursively.

**NOTE**: The tool first checks if a file exists in any revision of the supplied

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

### Example 2. Downloading as much stuff as possible :)

### Preparation

Download all assets from couple of pages recursively:

```bash
wget -r -erobots=off https://superopensourceapp.example.com/some_page -P /tmp/some_page/
wget -r -erobots=off https://superopensourceapp.example.com/other_page -P /tmp/other_page/
# sometimes 404 pages are static, so try
wget -r -erobots=off https://superopensourceapp.example.com/idontexist123123 -P /tmp/404_page/
```

Then run:

```bash
python fingermonkey.py ~/repos/SomeOpenSourceApp /tmp/some_page /tmp/other_page/ /tmp/404_page/
```

fingermonkey will pick up all files in specified directories recursively and ignore those, that don't exist in any revision of the repository.

## How does it work

First, fingermonkey calculates a git hash of a file:

```bash
git hash-object <your-file>
```

Then it iterates through all the tags in the repository and outputs those that have a blob with the same hash in their tree, meaning that in this revision there is a file of identical content.

```bash
# for each tag:
git ls-tree -r <tag>
```