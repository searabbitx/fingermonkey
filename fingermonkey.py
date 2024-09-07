import sys
import subprocess
import os


def log_info(msg, indent=0, before=0):
    print('{}{}[+] {}'.format(before * '\n', indent * '  ', msg))


def log_warn(msg, indent=0):
    print('{}[!] Warning: {}'.format(indent * '  ', msg))


class Args:
    def __init__(self, argv):
        self.__argv = argv

    def repo(self):
        return self.__argv[1]

    def file(self):
        return self.__argv[2]


class File:
    def __init__(self, path):
        self.__path = path
        self.__hash = None

    def hash(self):
        if self.__hash:
            return self.__hash

        if not os.path.exists(self.__path):
            return None
        # git hash-object <file>
        out = subprocess.check_output(['git', 'hash-object', self.__path])
        self.__hash = out.decode('utf-8').strip()
        return self.__hash


class TreeEntry:
    def __init__(self, output):
        [_, self.type, self.hash, self.name] = output.split()


class Result:
    def __init__(self, tag, filepath):
        self.tag = tag
        self.filepath = filepath


class Repository:
    def __init__(self, path):
        self.__path = path

    def get_all_tags(self):
        # git tag --sort=taggerdate
        out = subprocess.check_output(
            ['git', 'tag', '--sort=taggerdate'], cwd=self.__path).decode('utf-8')
        result = [ln.strip() for ln in out.split('\n') if ln]
        result.reverse()
        return result

    def get_tree_for_revision(self, revision):
        # git ls-tree -r <revision>
        out = subprocess.check_output(
            ['git', 'ls-tree', '-r', revision], cwd=self.__path).decode('utf-8')
        return [TreeEntry(l) for l in out.split('\n') if l]


class Progress:
    def __init__(self, total):
        self.__total = total
        self.__current = 0

    def advance(self):
        self.__current += 1
        print('... [{}/{}] ...'.format(self.__current, self.__total), end='\r')


def find_tags(repository: Repository, test_file):
    found_tags = []
    all_tags = repository.get_all_tags()
    progress = Progress(len(all_tags))

    for tag in all_tags:
        progress.advance()
        for entry in repository.get_tree_for_revision(tag):
            if entry.hash == test_file.hash():
                log_info('Found! {}'.format(tag), indent=1)
                found_tags.append(Result(tag, entry.name))
    return found_tags


if __name__ == '__main__':
    args = Args(sys.argv)
    test_file = File(args.file())
    repository = Repository(args.repo())

    print('''
          Repository:     {}
          File to test:   {} (git hash: {})
          '''.format(args.repo(), args.file(), test_file.hash()))

    log_info('Looking for all tags with a blob: {}'.format(test_file.hash()))

    found_tags = find_tags(repository, test_file)
    log_info('Done! found tags:', before=2)
    for result in found_tags:
        print('  - {} ({})'.format(result.tag, result.filepath))
