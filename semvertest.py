#!/usr/bin/env python
# vim: shiftwidth=4 tabstop=4 softtabstop wrapmargin=79 textwidth=72
#
# Test-bed for verifying behaviour with full Semantic Version strings
#
# Ref: https://semver.org/#semantic-versioning-specification-semver

import argparse

appname = 'SemVerTest'
applongname = 'Semantic Version Test'
appversion = '1.0.0-beta1'
copyright = '© Athanasius 2020'

def main() -> None:
    print('Version: {}'.format(appversion))

###########################################################################
# Command-Line Arguments
###########################################################################
__parser = argparse.ArgumentParser()
__parser.add_argument("--setversion", help="set the version for this invocation")
__parser.add_argument("py2exe", help="specify py2exe building", nargs="*")
__args = __parser.parse_args()
if __args.setversion:
	appversion = __args.setversion
###########################################################################

if __name__ == "__main__":
    main()
