from typing import Literal, assert_type
from unittest import TestCase

from thelabtyping.guards import is_literal_factory


class IsLiteralTest(TestCase):
    def test_normal_literal(self) -> None:
        MyLiteral = Literal["foo", "bar"]
        is_literal = is_literal_factory(MyLiteral)

        scenarios: list[tuple[str, bool]] = [
            ("a", False),
            ("foo", True),
            ("bar", True),
            ("baz", False),
        ]
        for arg, should_match in scenarios:
            with self.subTest(
                f"{arg} {'is literal' if should_match else 'is not literal'}"
            ):
                # Outside the type guard, some_str is just a string
                assert_type(arg, str)
                if is_literal(arg):
                    # Assert that mypy correctly narrowed the str type into the
                    # literal type
                    assert_type(arg, MyLiteral)
                    did_match = True
                else:
                    did_match = False
                # Check if matching/not-matching was expected.
                self.assertEqual(did_match, should_match)

    def test_alias_literal(self) -> None:
        type MyLiteral = Literal["foo", "bar"]
        is_literal = is_literal_factory(MyLiteral)

        scenarios: list[tuple[str, bool]] = [
            ("a", False),
            ("foo", True),
            ("bar", True),
            ("baz", False),
        ]
        for arg, should_match in scenarios:
            with self.subTest(
                f"{arg} {'is literal' if should_match else 'is not literal'}"
            ):
                # Outside the type guard, some_str is just a string
                assert_type(arg, str)
                if is_literal(arg):
                    # Assert that mypy correctly narrowed the str type into the
                    # literal type
                    assert_type(arg, MyLiteral)
                    did_match = True
                else:
                    did_match = False
                # Check if matching/not-matching was expected.
                self.assertEqual(did_match, should_match)
