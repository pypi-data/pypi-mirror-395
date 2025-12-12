#!/bin/sh
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.


pwd

cd ../../packages/docprovider-codio
pwd
jlpm run clean:all
jlpm
jlpm run build:prod

cd ../../packages/docprovider-extension-codio
pwd
jlpm run clean:all
jlpm
jlpm run build:prod

cd ../../packages/collaboration-extension
pwd
jlpm run clean:all
jlpm
jlpm run build:prod

cd ../../projects/jupyter-docprovider-codio
pwd
rm -rf dir/
python -m build