## T-JSON (TreeJSON / TUI-JSON)
### Traverse a JSON using a collapsible Tree
#### Will show 2 Trees side by side if 2 inputs are passed.
![Screenshot](screenshot.png)

---

## Download
<a href=https://github.com/mefemefe/tjson/releases><button>RELEASES</button></a> <--

## OR Install from source
`pip install -e .`

## OR Install from pypi
`pip install tuijson` (command can be run as both `tjson` or `tuijson`)

---

## Usage:
`tjson <json_file_or_json_string> OPTIONAL:<json_file_or_json_string2>`

### With file:
`tjson example.json`

### With string:
`tjson '{"test": {"test2": "test3"}}'`

### Two files:
`tjson 1.json 2.json`

---

### Bindings
`q` QUIT

`SPACE` COLLAPSE/EXPAND

`e` EXPANDALL

`d` EXPAND BOTH TREES

`c` COLLAPSEALL

`f` COLLAPSE BOTH TREES

`s` SEARCH (find next node that matches query, if no match, searches from root)
