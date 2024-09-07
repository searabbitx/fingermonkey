import sys
import subprocess
import os


def log_info(msg, indent=0, before=0):
    print('{}{}[+] {}'.format(before * '\n', indent * '  ', msg))


def log_section(msg):
    print('\n----====    {}    ====----\n'.format(msg))


def log_warn(msg, indent=0):
    print('{}[!] Warning: {}'.format(indent * '  ', msg))


class Args:
    def __init__(self, argv):
        self.__argv = argv

    def repo(self):
        return self.__argv[1]

    def files(self):
        return self.__argv[2:]

    def longest_filename(self):
        return max([len(n) for n in self.files()])


class File:
    def __init__(self, path):
        self.path = path
        self.__hash = None

    def hash(self):
        if self.__hash:
            return self.__hash

        if not os.path.exists(self.path):
            return None
        # git hash-object <file>
        out = subprocess.check_output(['git', 'hash-object', self.path])
        self.__hash = out.decode('utf-8').strip()
        return self.__hash


class TreeEntry:
    def __init__(self, output):
        [_, self.type, self.hash, self.name] = output.split()


class Mapping:
    def __init__(self, test_file, repo_file):
        self.test_file = test_file
        self.repo_file = repo_file


class Result:
    def __init__(self, tag, mappings):
        self.tag = tag
        self.mappings = mappings


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

    def finish(self):
        print('\n', end='\r')


def find_mappings(tag, files):
    mappings = []
    for entry in repository.get_tree_for_revision(tag):
        for file in files:
            if entry.hash == file.hash():
                mappings.append(Mapping(file.path, entry.name))
    return mappings


def find_tags(repository: Repository, files):
    found_tags = []
    all_tags = repository.get_all_tags()
    progress = Progress(len(all_tags))

    for tag in all_tags:
        progress.advance()
        mappings = find_mappings(tag, files)
        if len(files) == len(mappings):  # if all files are present in this tag
            log_info('Found! {}'.format(tag))
            found_tags.append(Result(tag, mappings))

    progress.finish()

    return found_tags


def print_banner(args: Args, files):
    print('''
     ___ _                     
    |  _|_|___ ___ ___ ___     
    |  _| |   | . | -_|  _|    
    |_| |_|_|_|_  |___|_|      
              |___|_           
     _____ ___ ___| |_ ___ _ _ 
    |     | . |   | '_| -_| | |
    |_|_|_|___|_|_|_,_|___|_  |
                          |___|'''[1:])
    pad = 4 * ' '
    print(pad + 'Repository:     {}'.format(args.repo()))
    print(pad + 'Files to test:')
    for file in files:
        print(
            pad + '  - {} (git hash: {})'.format(file.path.ljust(args.longest_filename()), file.hash()))


def print_results(results, longest_filename):
    log_section('Results')
    log_info('Done! found {} tags:'.format(len(results)))

    for result in results:
        print('  - {}'.format(result.tag))
        for mapping in result.mappings:
            print(
                '    {} -> {}'.format(mapping.test_file.ljust(longest_filename + 1), mapping.repo_file))


if __name__ == '__main__':
    args = Args(sys.argv)
    files = [File(path) for path in args.files()]
    repository = Repository(args.repo())

    print_banner(args, files)

    log_section('Looking for matching tags')

    results = find_tags(repository, files)
    print_results(results, args.longest_filename())
