import sys
import subprocess
import re
import getopt
from pathlib import Path

def get_flags(pattern, input):
    patpat = r'\{([^\}]+)\}'

    print('[DEBUG]: pattern: %s' % pattern)
    print('[DEBUG]: input: %s' % input)

    pats = re.findall(patpat, pattern)

    matcher = re.sub(patpat, r'(.*?)', pattern)

    match = re.search(matcher, input)

    print('[DEBUG]: matcher: %s' % matcher)

    if match:
        print('[DEBUG]: match groups: %r' % (match.groups(),))
        return [pats[i].replace('%', result) for i, result in enumerate(match.groups())]

    return None

def main(argv):
    additional_flags = file_flag_pattern = directory_flag_pattern = directory = None

    opts, args = getopt.getopt(argv, '', [
        'directory=',
        'directory-flag-pattern=',
        'file-flag-pattern=',
        'additional-flags=',
    ])

    print('[DEBUG]: opts: %r' % (opts,))
    print('[DEBUG]: argv: %r' % (argv,))

    for opt, arg in opts:
        if opt == '--directory':
            directory = arg
        elif opt == '--directory-flag-pattern':
            directory_flag_pattern = arg
        elif opt == '--file-flag-pattern':
            print('[DEBUG]: opt: %r || arg: %r' % (opt,arg))
            file_flag_pattern = arg
        elif opt == '--additional-flags':
            additional_flags = arg

        extra_flags = additional_flags.split(',') if additional_flags else []

        flags = {}

        directory = Path(directory) if directory else Path.cwd()

        for f in directory.rglob('*'):
            if f.is_file():
                iflags = set()
                if directory_flag_pattern:
                    print('[DEBUG]: %r' % (f.parent.parts,))
                    for part in f.parent.parts:
                        dflags = get_flags(directory_flag_pattern, part)
                        if dflags:
                            iflags.update(dflags)

                print('[DEBUG]: file_flag_pattern: %r' % (file_flag_pattern,))
                fflags = get_flags(file_flag_pattern, str(f.name))
                if fflags:
                    iflags.update(fflags)

                for flag in iflags:
                    flags.setdefault(flag, []).append(str(f.resolve()))

        logextra = ' (+%r)' % extra_flags if extra_flags else ''

        for flag, files in flags.items():
            cmd = ['codecov', '-F', flag]
            [cmd.extend(['-F', extra] for extra in extra_flags)]
            [cmd.extend(['-f', file]) for file in files]

            print('::group::Flag: %s%s' % (flag, logextra))

            print('Executing: %r' % cmd)
            subprocess.run(cmd, stderr=subprocess.STDOUT, check=True)

            print('::endgroup::')

if __name__ == '__main__':
    main(sys.argv[1:])
