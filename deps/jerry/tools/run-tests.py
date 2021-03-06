#!/usr/bin/env python

# Copyright JS Foundation and other contributors, http://js.foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import argparse
import collections
import os
import subprocess
import sys
import settings

OUTPUT_DIR = os.path.join(settings.PROJECT_DIR, 'build', 'tests')

Options = collections.namedtuple('Options', ['name', 'build_args', 'test_args'])
Options.__new__.__defaults__ = ([], [])

def get_binary_path(bin_dir_path):
    return os.path.join(bin_dir_path, 'jerry')

# Test options for unittests
JERRY_UNITTESTS_OPTIONS = [
    Options('unittests',
            ['--unittests', '--jerry-cmdline=off', '--error-messages=on', '--snapshot-save=on',
             '--snapshot-exec=on', '--vm-exec-stop=on', '--profile=es2015-subset', '--mem-stats=on']),
    Options('unittests-debug',
            ['--unittests', '--jerry-cmdline=off', '--debug', '--error-messages=on', '--snapshot-save=on',
             '--snapshot-exec=on', '--vm-exec-stop=on', '--profile=es2015-subset', '--mem-stats=on']),
    Options('doctests',
            ['--doctests', '--jerry-cmdline=off', '--error-messages=on', '--snapshot-save=on',
             '--snapshot-exec=on', '--vm-exec-stop=on', '--profile=es2015-subset']),
    Options('doctests-debug',
            ['--doctests', '--jerry-cmdline=off', '--debug', '--error-messages=on',
             '--snapshot-save=on', '--snapshot-exec=on', '--vm-exec-stop=on', '--profile=es2015-subset'])
]

# Test options for jerry-tests
JERRY_TESTS_OPTIONS = [
    Options('jerry_tests'),
    Options('jerry_tests-debug',
            ['--debug']),
    Options('jerry_tests-debug-cpointer_32bit',
            ['--debug', '--cpointer-32bit=on', '--mem-heap=1024']),
    Options('jerry_tests-snapshot',
            ['--snapshot-save=on', '--snapshot-exec=on', '--jerry-cmdline-snapshot=on'],
            ['--snapshot']),
    Options('jerry_tests-debug-snapshot',
            ['--debug', '--snapshot-save=on', '--snapshot-exec=on', '--jerry-cmdline-snapshot=on'],
            ['--snapshot']),
    Options('jerry_tests-es2015_subset-debug',
            ['--debug', '--profile=es2015-subset']),
    Options('jerry_tests-debug-external_context',
            ['--debug', '--jerry-libc=off', '--external-context=on'])
]

# Test options for jerry-test-suite
JERRY_TEST_SUITE_OPTIONS = JERRY_TESTS_OPTIONS[:]
JERRY_TEST_SUITE_OPTIONS.extend([
    Options('jerry_test_suite-minimal',
            ['--profile=minimal']),
    Options('jerry_test_suite-minimal-snapshot',
            ['--profile=minimal', '--snapshot-save=on', '--snapshot-exec=on', '--jerry-cmdline-snapshot=on'],
            ['--snapshot']),
    Options('jerry_test_suite-minimal-debug',
            ['--debug', '--profile=minimal']),
    Options('jerry_test_suite-minimal-debug-snapshot',
            ['--debug', '--profile=minimal', '--snapshot-save=on', '--snapshot-exec=on', '--jerry-cmdline-snapshot=on'],
            ['--snapshot']),
    Options('jerry_test_suite-es2015_subset',
            ['--profile=es2015-subset']),
    Options('jerry_test_suite-es2015_subset-snapshot',
            ['--profile=es2015-subset', '--snapshot-save=on', '--snapshot-exec=on', '--jerry-cmdline-snapshot=on'],
            ['--snapshot']),
    Options('jerry_test_suite-es2015_subset-debug-snapshot',
            ['--debug', '--profile=es2015-subset', '--snapshot-save=on', '--snapshot-exec=on',
             '--jerry-cmdline-snapshot=on'],
            ['--snapshot'])
])

# Test options for test262
TEST262_TEST_SUITE_OPTIONS = [
    Options('test262_tests')
]

# Test options for jerry-debugger
DEBUGGER_TEST_OPTIONS = [
    Options('jerry_debugger_tests',
            ['--debug', '--jerry-debugger=on', '--jerry-libc=off'])
]

# Test options for buildoption-test
JERRY_BUILDOPTIONS = [
    Options('buildoption_test-lto',
            ['--lto=on']),
    Options('buildoption_test-error_messages',
            ['--error-messages=on']),
    Options('buildoption_test-all_in_one',
            ['--all-in-one=on']),
    Options('buildoption_test-valgrind',
            ['--valgrind=on']),
    Options('buildoption_test-valgrind_freya',
            ['--valgrind-freya=on']),
    Options('buildoption_test-mem_stats',
            ['--mem-stats=on']),
    Options('buildoption_test-show_opcodes',
            ['--show-opcodes=on']),
    Options('buildoption_test-show_regexp_opcodes',
            ['--show-regexp-opcodes=on']),
    Options('buildoption_test-compiler_default_libc',
            ['--jerry-libc=off']),
    Options('buildoption_test-cpointer_32bit',
            ['--jerry-libc=off', '--compile-flag=-m32', '--cpointer-32bit=on', '--system-allocator=on']),
    Options('buildoption_test-external_context',
            ['--jerry-libc=off', '--external-context=on']),
    Options('buildoption_test-cmdline_test',
            ['--jerry-cmdline-test=on']),
    Options('buildoption_test-cmdline_snapshot',
            ['--jerry-cmdline-snapshot=on']),
]

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--toolchain', metavar='FILE',
                        help='Add toolchain file')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Only print out failing tests')
    parser.add_argument('--buildoptions', metavar='LIST',
                        help='Add a comma separated list of extra build options to each test')
    parser.add_argument('--skip-list', metavar='LIST',
                        help='Add a comma separated list of patterns of the excluded JS-tests')
    parser.add_argument('--outdir', metavar='DIR', default=OUTPUT_DIR,
                        help='Specify output directory (default: %(default)s)')
    parser.add_argument('--check-signed-off', metavar='TYPE', nargs='?',
                        choices=['strict', 'tolerant', 'travis'], const='strict',
                        help='Run signed-off check (%(choices)s; default type if not given: %(const)s)')
    parser.add_argument('--check-cppcheck', action='store_true',
                        help='Run cppcheck')
    parser.add_argument('--check-doxygen', action='store_true',
                        help='Run doxygen')
    parser.add_argument('--check-pylint', action='store_true',
                        help='Run pylint')
    parser.add_argument('--check-vera', action='store_true',
                        help='Run vera check')
    parser.add_argument('--check-license', action='store_true',
                        help='Run license check')
    parser.add_argument('--check-magic-strings', action='store_true',
                        help='Run "magic string source code generator should be executed" check')
    parser.add_argument('--jerry-debugger', action='store_true',
                        help='Run jerry-debugger tests')
    parser.add_argument('--jerry-tests', action='store_true',
                        help='Run jerry-tests')
    parser.add_argument('--jerry-test-suite', action='store_true',
                        help='Run jerry-test-suite')
    parser.add_argument('--test262', action='store_true',
                        help='Run test262')
    parser.add_argument('--unittests', action='store_true',
                        help='Run unittests (including doctests)')
    parser.add_argument('--buildoption-test', action='store_true',
                        help='Run buildoption-test')
    parser.add_argument('--all', '--precommit', action='store_true',
                        help='Run all tests')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    script_args = parser.parse_args()

    return script_args

BINARY_CACHE = {}

def create_binary(job, options):
    build_cmd = [settings.BUILD_SCRIPT]
    build_cmd.extend(job.build_args)

    build_dir_path = os.path.join(options.outdir, job.name)
    build_cmd.append('--builddir=%s' % build_dir_path)

    if options.toolchain:
        build_cmd.append('--toolchain=%s' % options.toolchain)

    if options.buildoptions:
        build_cmd.extend(options.buildoptions.split(','))

    sys.stderr.write('Build command: %s\n' % ' '.join(build_cmd))

    binary_key = tuple(job.build_args)
    if binary_key in BINARY_CACHE:
        ret, build_dir_path = BINARY_CACHE[binary_key]
        sys.stderr.write('(skipping: already built at %s with returncode %d)\n' % (build_dir_path, ret))
        return ret, os.path.join(build_dir_path, 'bin')

    try:
        subprocess.check_output(build_cmd)
        ret = 0
    except subprocess.CalledProcessError as err:
        ret = err.returncode

    BINARY_CACHE[binary_key] = (ret, build_dir_path)
    return ret, os.path.join(build_dir_path, 'bin')

def run_check(runnable):
    sys.stderr.write('Test command: %s\n' % ' '.join(runnable))

    try:
        ret = subprocess.check_call(runnable)
    except subprocess.CalledProcessError as err:
        return err.returncode

    return ret

def run_jerry_debugger_tests(options):
    ret_build = ret_test = 0
    for job in DEBUGGER_TEST_OPTIONS:
        ret_build, bin_dir_path = create_binary(job, options)
        if ret_build:
            break

        for test_file in os.listdir(settings.DEBUGGER_TESTS_DIR):
            if test_file.endswith(".cmd"):
                test_case, _ = os.path.splitext(test_file)
                test_case_path = os.path.join(settings.DEBUGGER_TESTS_DIR, test_case)
                test_cmd = [
                    settings.DEBUGGER_TEST_RUNNER_SCRIPT,
                    get_binary_path(bin_dir_path),
                    settings.DEBUGGER_CLIENT_SCRIPT,
                    os.path.relpath(test_case_path, settings.PROJECT_DIR)
                ]

                if job.test_args:
                    test_cmd.extend(job.test_args)

                ret_test |= run_check(test_cmd)

    return ret_build | ret_test

def run_jerry_tests(options):
    ret_build = ret_test = 0
    for job in JERRY_TESTS_OPTIONS:
        ret_build, bin_dir_path = create_binary(job, options)
        if ret_build:
            break

        test_cmd = [
            settings.TEST_RUNNER_SCRIPT,
            get_binary_path(bin_dir_path),
            settings.JERRY_TESTS_DIR
        ]
        skip_list = []

        if '--profile=es2015-subset' not in job.build_args:
            skip_list.append(r"es2015\/")
        else:
            skip_list.append(r"es5.1\/")

        if options.skip_list:
            skip_list.append(options.skip_list)

        if options.quiet:
            test_cmd.append("-q")

        if skip_list:
            test_cmd.append("--skip-list=" + ",".join(skip_list))

        if job.test_args:
            test_cmd.extend(job.test_args)

        ret_test |= run_check(test_cmd)

    return ret_build | ret_test

def run_jerry_test_suite(options):
    ret_build = ret_test = 0
    for job in JERRY_TEST_SUITE_OPTIONS:
        ret_build, bin_dir_path = create_binary(job, options)
        if ret_build:
            break

        test_cmd = [settings.TEST_RUNNER_SCRIPT, get_binary_path(bin_dir_path)]

        if '--profile=minimal' in job.build_args:
            test_cmd.append(settings.JERRY_TEST_SUITE_MINIMAL_LIST)
        elif '--profile=es2015-subset' in job.build_args:
            test_cmd.append(settings.JERRY_TEST_SUITE_DIR)
        else:
            test_cmd.append(settings.JERRY_TEST_SUITE_ES51_LIST)

        if options.quiet:
            test_cmd.append("-q")

        if options.skip_list:
            test_cmd.append("--skip-list=" + options.skip_list)

        if job.test_args:
            test_cmd.extend(job.test_args)

        ret_test |= run_check(test_cmd)

    return ret_build | ret_test

def run_test262_test_suite(options):
    ret_build = ret_test = 0
    for job in TEST262_TEST_SUITE_OPTIONS:
        ret_build, bin_dir_path = create_binary(job, options)
        if ret_build:
            break

        test_cmd = [
            settings.TEST262_RUNNER_SCRIPT,
            get_binary_path(bin_dir_path),
            settings.TEST262_TEST_SUITE_DIR
        ]

        if job.test_args:
            test_cmd.extend(job.test_args)

        ret_test |= run_check(test_cmd)

    return ret_build | ret_test

def run_unittests(options):
    ret_build = ret_test = 0
    for job in JERRY_UNITTESTS_OPTIONS:
        ret_build, bin_dir_path = create_binary(job, options)
        if ret_build:
            break

        ret_test |= run_check([
            settings.UNITTEST_RUNNER_SCRIPT,
            bin_dir_path,
            "-q" if options.quiet else "",
        ])

    return ret_build | ret_test

def run_buildoption_test(options):
    for job in JERRY_BUILDOPTIONS:
        ret, _ = create_binary(job, options)
        if ret:
            break

    return ret

Check = collections.namedtuple('Check', ['enabled', 'runner', 'arg'])

def main(options):
    checks = [
        Check(options.check_signed_off, run_check, [settings.SIGNED_OFF_SCRIPT]
              + {'tolerant': ['--tolerant'], 'travis': ['--travis']}.get(options.check_signed_off, [])),
        Check(options.check_cppcheck, run_check, [settings.CPPCHECK_SCRIPT]),
        Check(options.check_doxygen, run_check, [settings.DOXYGEN_SCRIPT]),
        Check(options.check_pylint, run_check, [settings.PYLINT_SCRIPT]),
        Check(options.check_vera, run_check, [settings.VERA_SCRIPT]),
        Check(options.check_license, run_check, [settings.LICENSE_SCRIPT]),
        Check(options.check_magic_strings, run_check, [settings.MAGIC_STRINGS_SCRIPT]),
        Check(options.jerry_debugger, run_jerry_debugger_tests, options),
        Check(options.jerry_tests, run_jerry_tests, options),
        Check(options.jerry_test_suite, run_jerry_test_suite, options),
        Check(options.test262, run_test262_test_suite, options),
        Check(options.unittests, run_unittests, options),
        Check(options.buildoption_test, run_buildoption_test, options),
    ]

    for check in checks:
        if check.enabled or options.all:
            ret = check.runner(check.arg)
            if ret:
                sys.exit(ret)

if __name__ == "__main__":
    main(get_arguments())
