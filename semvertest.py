#!/usr/bin/env python
# vim: shiftwidth=4 tabstop=4 softtabstop wrapmargin=79 textwidth=72
#
# Test-bed for verifying behaviour with full Semantic Version strings
#
# Ref: https://semver.org/#semantic-versioning-specification-semver

import argparse
import ctypes
import time

appname = 'SemVerTest'
applongname = 'Semantic Version Test'
appversion = '1.2.3'
copyright = '© Athanasius 2020'
update_feed = 'https://ed.miggy.org/misc/semvertest-appcast.xml'
sleep_interval = 60


###########################################################################
class Updater(object):

    def __init__(self):
        self.updater = ctypes.cdll.WinSparkle
        try:
            # Set the appcast URL
            self.updater.win_sparkle_set_appcast_url(update_feed.encode())

            # Set up the shutdown callback
            self.callback_t = ctypes.CFUNCTYPE(None)  # keep reference
            self.callback_fn = self.callback_t(self.shutdown_request)
            self.updater.win_sparkle_set_shutdown_request_callback(self.callback_fn)

            # Set the appversion *without* build metadata, as WinSparkle
            # doesn't do proper Semantic Version checks.
            # NB: It 'accidentally' supports pre-release due to how it
            # splits and compares strings:
            # <https://github.com/vslavik/winsparkle/issues/214>
            appversion_nobuildmetadata = appversion.split(sep='+')[0]
            print('Version used for WinSparkle: {}'.format(appversion_nobuildmetadata))
            self.updater.win_sparkle_set_app_build_version(appversion_nobuildmetadata)

            # Get WinSparkle running
            self.updater.win_sparkle_init()

        except Exception:
            self.updater = None
            raise

    def shutdown_request(self) -> None:
        print('WinSparkle requested shutdown')
        exit()

    def check_for_updates(self) -> None:
        if self.updater:
            self.updater.win_sparkle_check_update_with_ui()
        else:
            print('check_for_updates(): No updater')

    def close(self) -> None:
        if self.updater:
            self.updater.win_sparkle_cleanup()
        self.updater = None
###########################################################################


def main() -> None:
    print('Version: {}'.format(appversion))
    updater = Updater()
    print('WinSparkle set up and running')
    while True:
        print('Trying check_for_updates()')
        updater.check_for_updates()
        time.sleep(sleep_interval)


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
