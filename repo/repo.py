import os
import tempfile
import shutil
import threading

import git
from repo import GitoliteAdminRepo

class RepoManager:
        def __init__(self, domain):
            self.domain = domain
            self.lock = threading.Lock()

        def initRepos(self, name):
            with self.lock:
                tmp = tempfile.mkdtemp()

                coreurl = 'git@' + self.domain + ':core/' + name
                secreturl = 'git@' + self.domain + ':secret/' + name
                feedbackurl = 'git@' + self.domain + ':feedback/' + name

                core =  git.Repo.clone_from(coreurl, os.path.join(tmp, 'core', name))
                secret =  git.Repo.clone_from(secreturl, os.path.join(tmp, 'secret', name))
                feedback =  git.Repo.clone_from(feedbackurl, os.path.join(tmp, 'feedback', name))

                author = git.Actor('ILab', 'RepoManager@server')

                #Secret repo initialization

                os.makedirs(os.path.join(tmp, 'secret', name, 'meta'))

                with open(os.path.join(tmp, 'secret', name, 'meta', 'id'), 'w+') as f:
                    f.write(name)

                secret.git.add('.')

                secret.index.commit('Repository initialization', author=author)

                secret.create_tag('initial_commit')

                secret.remotes['origin'].push()
                secret.remotes['origin'].push(tags=True)

                #Feedback repo initialization

                os.makedirs(os.path.join(tmp, 'feedback', name, 'meta'))

                with open(os.path.join(tmp, 'feedback', name, 'meta', 'id'), 'w+') as f:
                    f.write(name)

                feedback.git.add('.')

                feedback.index.commit('Repository initialization', author=author)

                feedback.create_tag('initial_commit')

                feedback.remotes['origin'].push()
                feedback.remotes['origin'].push(tags=True)

                #Core repository initialization

                os.makedirs(os.path.join(tmp, 'core', name, 'meta'))

                with open(os.path.join(tmp, 'core', name, 'meta', 'id'), 'w+') as f:
                    f.write(name)

                core.git.add('.')

                core.git.submodule('add', secreturl, 'secret')
                core.git.submodule('add', feedbackurl, 'feedback')

                core.index.commit('Repository initialization', author=author)

                core.create_tag('initial_commit')

                core.remotes['origin'].push()
                core.remotes['origin'].push(tags=True)

                #Cleanup

                shutil.rmtree(tmp)

from app import app

instance = RepoManager(app.config['GITOLITE_DOMAIN'])
