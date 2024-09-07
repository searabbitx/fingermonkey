import argparse
import os
import subprocess
import sys


def log_info(msg, indent=0, before=0):
    print('{}{}[+] {}'.format(before * '\n', indent * '  ', msg))


def log_section(msg):
    print('\n----====    {}    ====----\n'.format(msg))


def log_warn(msg, indent=0):
    print('{}[!] Warning: {}'.format(indent * '  ', msg))


class Args:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="python fingermonkey.py", description="A tool to detect versions of open source apps based on the world-readable assets such as images, js, css or static html")
        parser.add_argument('REPOSITORY', help='Path to the git repository')
        parser.add_argument(
            'FILE', nargs='+', help='Path(s) to the file(s) to use for fingerprinting. If a directory is passed, the tool will find all files under this directory and its subdirectories recursively.')
        parser.add_argument('-v', '--verbose', action='store_true')
        self.__args = parser.parse_args()

    def repo(self):
        return self.__args.REPOSITORY

    def files(self):
        return self.__args.FILE

    def longest_filename(self):
        return max([len(n) for n in self.files()])

    def verbose(self):
        return self.__args.verbose


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
        [_, self.type, self.hash, *name] = output.split()
        self.name = ' '.join(name)


class Mapping:
    def __init__(self, test_file, repo_file):
        self.test_file = test_file
        self.repo_file = repo_file


class Result:
    def __init__(self, tag, mappings):
        self.tag = tag
        self.mappings = mappings
        self.matches = len(mappings)


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

    def object_exists(self, obj):
        # git cat-file -t <obj>
        exit_code = subprocess.Popen(
            ['git', 'cat-file', '-t', obj], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,  cwd=self.__path).wait()
        return exit_code == 0


class Progress:
    def __init__(self, total):
        self.__total = total
        self.__current = 0
        self.__last_len = 0

    def advance(self, additional_msg=None):
        self.__current += 1
        suffix = ' | {}'.format(additional_msg) if additional_msg else ''
        msg = '\r... [{}/{}] ...{}'.format(self.__current,
                                           self.__total, suffix).ljust(self.__last_len)
        print(msg, end='\n\n')
        sys.stdout.write("\033[F\033[F")
        self.__last_len = len(msg)

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

    most_mappings = 0
    current_winner_msg = None
    for tag in all_tags:
        progress.advance(current_winner_msg)
        mappings = find_mappings(tag, files)
        if len(mappings) > 0:
            if len(mappings) > most_mappings:
                most_mappings = len(mappings)
                current_winner_msg = 'Current winner: {} ({} files matched)'.format(
                    tag, len(mappings))
            found_tags.append(Result(tag, mappings))

    progress.finish()

    return found_tags


def print_banner(args: Args, files, print_files=False):
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
    print(pad + 'Number of files that exist in some revision: {}'.format(len(files)))
    if print_files:
        print(pad + 'Files that exist in some revision:')
        for file in files:
            print(
                pad + '  - {} (git hash: {})'.format(file.path.ljust(args.longest_filename()), file.hash()))


def print_results(results, longest_filename, print_mappings=False):
    log_section('Results')
    log_info(
        'Done! found {} tags with at least one matching file'.format(len(results)))

    print('Top 10 tags:')
    top_results = sorted(results, key=lambda x: x.matches, reverse=True)[:10]
    longest_tag_name = max([len(r.tag) for r in top_results])
    for result in top_results:
        print('  - {} ({} files matched)'.format(result.tag.ljust(longest_tag_name), result.matches))
        if print_mappings:  # todo: print_mappings=True when -v
            for mapping in result.mappings:
                print(
                    '    {} -> {}'.format(mapping.test_file.ljust(longest_filename + 1), mapping.repo_file))


def find_files_recursively(paths):
    result = []
    for path in paths:
        if os.path.isfile(path):
            result.append(File(path))
        else:
            for dir, _, files in os.walk(path):
                for file in files:
                    result.append(File(os.path.join(dir, file)))
    return result


def filter_files_with_existing_objects(repository, files):
    return [f for f in files if repository.object_exists(f.hash())]


if __name__ == '__main__':
    args = Args()
    all_files = find_files_recursively(args.files())
    repository = Repository(args.repo())
    files = filter_files_with_existing_objects(repository, all_files)

    print_banner(args, files, args.verbose())

    if not len(files):
        log_warn(
            "None of the supplied files exist in any revision of the repository provided")
        exit(1)

    log_section('Looking for matching tags')

    results = find_tags(repository, files)
    print_results(results, args.longest_filename(), args.verbose())
