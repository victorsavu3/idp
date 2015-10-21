import os

def analyse(repository, branch, diff, repo, repodir):
    with open(os.path.join(repodir, 'likes', 'state')) as f:
        for line in f:
            print(line)
