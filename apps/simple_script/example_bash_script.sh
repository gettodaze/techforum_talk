#!/bin/bash
while true; do
    git status
    read -p "Do you wish to create $1? [y/n] " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit 1;;
        * ) echo "Please answer yes or no.";;
    esac
done
# echo "created $1"
git branch $1
git checkout $1
git push --set-upstream origin $1
