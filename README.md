# fingermonkey

A tool to detect versions of open source apps based on the world-readable files such as unminified javascript, css or static html.

## Usage

#### Preparation
Say that SomeOpenSourceApp is running on http://superopensourceapp.example.com and there's an unminified javascript file at http://superopensourceapp.example.com/js/app.js.

First, download the javascript file to some location:
```bash
wget http://superopensourceapp.example.com/js/app.js -O /tmp/app.js
```

Then clone the SomeOpenSourceApp's repo to some location (say `~/repos/SomeOpenSourceApp`)

```bash
git clone https://imaginary.git.hosting.example.com/superopensourceapp ~/repos/SomeOpenSourceApp
```

#### Running the tool
Finally, to find possible versions of SomeOpenSourceApp, run:
```bash
python fingermonkey.py ~/repos/SomeOpenSourceApp /tmp/app.js
```

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