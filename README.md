# fingermonkey

A tool to detect versions of open source apps based on the world-readable files such as javascript, css or static html.

## Usage

#### Preparation
Say that SomeOpenSourceApp is running on http://superopensourceapp.example.com and there's a javascript file at http://superopensourceapp.example.com/js/app.js.

First, download the javascript file to some location:
```bash
wget http://superopensourceapp.example.com/js/app.js -O /tmp/app.js
```

Then clone the SomeOpenSourceApp's repo to some location (say `~/repos/SomeOpenSourceApp`)

```bash
git clone https://imaginary.git.hosting.example.com/superopensourceapp ~/repos/SomeOpenSourceApp
```

Now, go find where the `app.js` file is located in the repository. Let's say it is in `public/js/app.js`.

#### Running the tool
Finally, to find possible versions of SomeOpenSourceApp, run:
```bash
python fingermonkey.py ~/repos/SomeOpenSourceApp public/js/app.js /tmp/app.js
#                        the repo                 path in repo     absolute path 
#                                                                to the downloaded file
```

## Todos
- [ ] Track file renames/moves
- [ ] Support multiple files