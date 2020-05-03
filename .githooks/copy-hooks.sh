#!/bin/bash

hooklist="prepare-commit-msg
"

for foo in ${hooklist}
do
	chmod +x .githooks/$foo
	cp -p .githooks/$foo .git/hooks/$foo
done
