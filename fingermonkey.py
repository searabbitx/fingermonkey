import sys
import subprocess


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


if __name__ == '__main__':
    args = Args(sys.argv)
    print('''
          Repository:            {}
          Path to file in repo:  {}
          File to test:          {} 


          Please make sure that the repository is at the current revision!
          '''.format(args.repo(), args.repo_file(), args.file()))

    test_file = File(args.file())
    repo_file = File(args.repo() + '/' + args.repo_file())

    print('''
          File to test hash:     {} 
          Repo file hash:        {}
        '''.format(test_file.hash(), repo_file.hash()))
