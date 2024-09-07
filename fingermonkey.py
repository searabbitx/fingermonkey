import sys
import subprocess


def log_info(msg, indent=0):
    print('{}[+] {}'.format(indent * '  ', msg))


class Args:
    def __init__(self, argv):
        self.__argv = argv

    def repo(self):
        return sys.argv[1]

    def repo_file(self):
        return sys.argv[2]

    def file(self):
        return sys.argv[3]


class File:
    def __init__(self, path):
        self.__path = path

    def hash(self):
        # todo: use python here to create a checksum
        out = subprocess.check_output(['md5sum', self.__path])
        return out.decode('utf-8').split()[0]


class Repository:
    def __init__(self, path):
        self.__path = path

    def get_all_commits_for(self, file_path):
        # git log --oneline --follow -- <file_path>
        out = subprocess.check_output(
            ['git', 'log', '--oneline', '--follow', '--', file_path], cwd=self.__path).decode('utf-8')
        return [ln.split(' ')[0] for ln in out.split('\n') if ln]

    def get_all_tags(self):
        # git tag --sort=taggerdate
        out = subprocess.check_output(
            ['git', 'tag', '--sort=taggerdate'], cwd=self.__path).decode('utf-8')
        result = [ln.strip() for ln in out.split('\n') if ln]
        result.reverse()
        return result

    def checkout(self, revision):
        # git log --oneline --follow -- <file_path>
        code = subprocess.Popen(
            ['git', 'checkout', revision], cwd=self.__path, stderr=subprocess.DEVNULL).wait()
        if code != 0:
            log_info('Stashing!')
            subprocess.Popen(['git', 'stash'], cwd=self.__path).wait()
            subprocess.Popen(['git', 'stash', 'clear'], cwd=self.__path).wait()
            self.checkout(revision)

    def checkout_initial_revision(self):
        # todo: find an initial revision for a cleanup
        self.checkout('master')


def find_tags(repository, repo_file, test_file):
    found_tags = []
    for tag in repository.get_all_tags():
        log_info('Checking {}'.format(tag), indent=1)
        repository.checkout(tag)
        log_info('Current hash: {}'.format(repo_file.hash()), indent=1)
        if test_file.hash() == repo_file.hash():
            log_info('Found!', indent=2)
            found_tags.append(tag)
    return found_tags


if __name__ == '__main__':
    args = Args(sys.argv)
    test_file = File(args.file())
    repo_file = File(args.repo() + '/' + args.repo_file())
    repository = Repository(args.repo())

    print('''
          Repository:            {}
          Path to file in repo:  {} ({})
          File to test:          {} ({})

          Please make sure that the repository is at the current revision!
          '''.format(args.repo(), args.repo_file(), repo_file.hash(), args.file(), test_file.hash()))

    log_info('Looking for all tags with {} in specified version ({})'.format(
        args.repo_file(), test_file.hash()))

    found_tags = find_tags(repository, repo_file, test_file)

    log_info('Done! found tags:')
    for tag in found_tags:
        print('  - {}'.format(tag))

    repository.checkout_initial_revision()
