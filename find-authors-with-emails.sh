#!/bin/bash
# Get unique list of authors with emails
authors=$(git log --pretty="%an <%ae>" -- src/app-ng2 | sort | uniq)

# Loop through each author and get the date of their latest commit
echo "$authors" | while read author; do
    last_commit_date=$(git log --author="$author" --pretty="%cd" --date=short -1 -- src/app-ng2)
    echo "$author, last commit date: $last_commit_date"
done
