import contextlib
import difflib
import pathlib
import sys

import pytest


class TestCommon:
    # adapted from https://stackoverflow.com/a/42327075
    @contextlib.contextmanager
    def does_not_raise(
        self,
        exception,
    ):
        try:
            yield
        except exception:
            # ruff: noqa: B904
            raise pytest.fail(f'raised unwanted exception {exception}')

    def assert_herkules_absolute(
        self,
        root_path,
        expected_files,
        actual_paths,
        ignore_order=False,
    ):
        actual_paths_relative = []
        for actual_path in actual_paths:
            actual_path_relative = actual_path.relative_to(root_path)
            actual_paths_relative.append(
                pathlib.Path(actual_path_relative),
            )

        return self.assert_herkules_relative(
            expected_files,
            actual_paths_relative,
            ignore_order,
        )

    def assert_herkules_relative(
        self,
        expected_files,
        actual_paths,
        ignore_order=False,
    ):
        actual_files = []
        for actual_path in actual_paths:
            assert isinstance(
                actual_path,
                pathlib.Path,
            )

            actual_files.append(
                str(actual_path),
            )

        if ignore_order:
            expected_files = sorted(expected_files)
            actual_files = sorted(actual_files)

        if actual_files != expected_files:
            # force well-formatted diff output
            expected_files = '\n'.join(expected_files) + '\n'
            actual_files = '\n'.join(actual_files) + '\n'

            diff_result = difflib.unified_diff(
                expected_files.splitlines(keepends=True),
                actual_files.splitlines(keepends=True),
                fromfile='EXPECTED',
                tofile='ACTUAL',
            )

            print('------------------------------------------------------')
            print()
            print('Difference between expected and actual output:')
            print()
            sys.stdout.writelines(diff_result)
            print()

            pytest.fail('Found differing files.')
