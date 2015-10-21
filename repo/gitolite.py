import os
import threading

import git

class GitoliteAdminRepo:
    def __init__(self, path):
        self.path = path
        self.repo = git.Repo(path)
        self.lock = threading.Lock()

    def addUser(self, name, key):
        with self.lock:
            with open(os.path.join(self.path, 'keydir', 'user.' + name + '.pub'), 'w+') as f:
                f.write(key)

            self.commit('Add user "' + name + '"')

    def removeUser(self, name):
        with self.lock:
            os.remove(os.path.join(self.path, 'keydir', name + '.pub'))

            self.commit('Remove user "' + name + '"')

    def addEntityToGroup(self, name, group):
        with self.lock:
            with open(os.path.join(self.path, 'conf', 'groups', group + '_' + name + '.conf'), 'w+') as f:
                f.write('@')
                f.write(group)
                f.write(' = ')
                f.write(name)

            self.commit('Added entity "' + name + '" to group"' + group + '"')

    def removeEntityFromGroup(self, name, group):
        with self.lock:
            os.remove(os.path.join(self.path, 'conf', 'groups', group + '_' + name + '.conf'))

            self.commit('Removed entity "' + name + '" from group"' + group + '"')

    def addUserToGroup(self, name, group):
        self.addEntityToGroup('user.' + name, group)

    def removeUserFromGroup(self, name, group):
        self.removeEntityFromGroup('user.' + name, group)

    def addRepoToGroup(self, name, group):
        self.addEntityToGroup(name, group)

    def removeRepoFromGroup(self, name, group):
        self.removeEntityFromGroup(name, group)

    def commit(self, message):
        index = self.repo.index

        index.add('.')

        author = git.Actor('ILab', 'GitoliteAdminRepo@server')
        index.commit(message, author=author)

        remote = self.repo.remotes['origin']

        remote.push()

from app import app

instance = GitoliteAdminRepo(app.config['GITOLITE_ADMIN_DIR'])
