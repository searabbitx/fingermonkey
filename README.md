# fingermonkey

A tool to detect versions of open source apps based on the world-readable files such as unminified javascript, css, static html or images.

## How does it work

To use the tool, you need to download some files from your target (preferably a lot of them :), `wget -r` is your friend) and the git repository of the app. Fingermonkey then:

1. Iterates through all supplied files calculates their git hashes:

```bash
git hash-object <your-file>
```

2. Checks if those files exist in any revision of the supplied repository. The files that don't have corresponding `blob` objects in the repository are ignored.

3. Iterates through all the tags in the repository and gathers those that have at least one of the blob objects from step 2. in their tree.

```bash
# for each tag:
git ls-tree -r <tag>
```

4. Finally, fingermonkey will show display 10 tags with the highest number of matching blobs

## Usage

```bash
python fingermonkey.py REPOSITORY FILES/DIRECTORIES...
```
If you use a directory then fingermonkey will find all of the files in this directory recursively.

### Example 1. Downloading as much stuff as possible :)

#### Preparation

Say that `SomeOpenSourceApp` is running on http://superopensourceapp.example.com. Download all assets from couple of pages recursively:

```bash
wget -r -erobots=off https://superopensourceapp.example.com/some_page -P /tmp/some_page/
wget -r -erobots=off https://superopensourceapp.example.com/other_page -P /tmp/other_page/
# sometimes 404 pages are static, so try:
wget -r -erobots=off https://superopensourceapp.example.com/idontexist123123 -P /tmp/404_page/
```

Then clone the `SomeOpenSourceApp`'s repo to some location (say `~/repos/SomeOpenSourceApp`)

```bash
git clone https://imaginary.git.hosting.example.com/superopensourceapp ~/repos/SomeOpenSourceApp
```

#### Running the tool
To find possible versions of `SomeOpenSourceApp` based on versions of gathered files, run:
```bash
python fingermonkey.py ~/repos/SomeOpenSourceApp /tmp/some_page /tmp/other_page/ /tmp/404_page/
```

### Example 1. Testing specific files

#### Preparation
Rarely some apps won't minify their javascript/css files, so you can use them for fingerprinting.

Say that `SomeOpenSourceApp` is running on http://superopensourceapp.example.com and there's:
- an unminified javascript file at http://superopensourceapp.example.com/js/app.js
- an unminified css file at http://superopensourceapp.example.com/styles/main.css

Download those files to some location:
```bash
wget http://superopensourceapp.example.com/js/app.js -O /tmp/app.js
wget http://superopensourceapp.example.com/styles/main.css -O /tmp/main.css
```

#### Running the tool
To find possible versions of `SomeOpenSourceApp` based on versions of gathered files, run:
```bash
python fingermonkey.py ~/repos/SomeOpenSourceApp /tmp/app.js /tmp/main.css
```