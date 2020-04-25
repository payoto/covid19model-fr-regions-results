#!/bin/bash

hooklist="prepare-commit-msg
"

for foo in ${hooklist}
do
	chmod +x $foo
	cp -p .githooks/$foo .git/hooks/$foo
done