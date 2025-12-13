#!/bin/sh

# build the archive
python3 -m build

# upload the archive
python3 -m twine upload dist/*