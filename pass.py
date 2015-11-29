"""
A simple script that allows for GPG-encrypted passwords to be retrieved.
The password is stored in the clipboard (with no expiration!).

The password directory structure and encryption is understood to be equivalent
to the one defined/used by the [pass](http://www.passwordstore.org/) utility.

In the future it might be expanded to provide support for generating, storing,
and editing passwords, equivalent to the full `pass` utility. The need for this
script arose due to the Windows client advertised by `pass` being broken.
"""
import subprocess
import os


def get_homedir():
    return os.path.expanduser('~')


class Manager(object):
    def __init__(self, passwds_dir=None):
        if passwds_dir is None:
	    passwds_dir = os.path.join(get_homedir(), '.passwds')
	self.passwds_dir = passwds_dir

    def get_pass(self, pass_name):
        path = os.path.join(self.passwds_dir, pass_name)
        path = path + '.gpg'

        return subprocess.check_output(['gpg', '--decrypt', path])

    def copy_pass_to_clipboard(self, pass_name):
        passwd = self.get_pass(pass_name)
        clip = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
        return clip.communicate(input=passwd)[0]


def main():
    import sys
    if len(sys.argv) != 2:
        print 'Expected only a single argument (name of password)'
        return

    name = sys.argv[1]
    mgr = Manager()
    mgr.copy_pass_to_clipboard(name)


if __name__ == '__main__':
    main()
