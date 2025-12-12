from typing import assert_type
from unittest import TestCase

from thelabtyping.result import (
    Err,
    Ok,
    Result,
    UnwrapError,
    as_result,
    do,
    partition_results,
)


class OkTest(TestCase):
    def test_ok_result(self) -> None:
        res = Ok("foo")
        self.assertTrue(res.is_ok)
        self.assertFalse(res.is_err)
        self.assertEqual(res.ok(), "foo")
        self.assertEqual(res.err(), None)  # type:ignore[func-returns-value]
        self.assertEqual(res.unwrap(), "foo")
        with self.assertRaises(UnwrapError):
            res.unwrap_err()

    def test_dunders(self) -> None:
        self.assertEqual(Ok(5), Ok(5))
        self.assertNotEqual(Ok(5), Ok(6))
        self.assertNotEqual(Ok(5), Err(5))
        self.assertIsNotNone(hash(Ok(1)))
        self.assertEqual(repr(Ok(1)), "Ok(1)")


class ErrTest(TestCase):
    def test_err_result(self) -> None:
        res = Err("foo")
        self.assertFalse(res.is_ok)
        self.assertTrue(res.is_err)
        self.assertEqual(res.ok(), None)  # type:ignore[func-returns-value]
        self.assertEqual(res.err(), "foo")
        with self.assertRaises(UnwrapError):
            res.unwrap()
        self.assertEqual(res.unwrap_err(), "foo")

    def test_dunders(self) -> None:
        self.assertEqual(Err(5), Err(5))
        self.assertNotEqual(Err(5), Err(6))
        self.assertNotEqual(Err(5), Ok(5))
        self.assertIsNotNone(hash(Err(1)))
        self.assertEqual(repr(Err(1)), "Err(1)")


class ResultTest(TestCase):
    def test_result(self) -> None:
        def foo(x: int) -> Result[int, str]:
            if x > 5:
                return Ok(x)
            return Err("x is too small")

        self.assertIsInstance(foo(1), Err)
        self.assertIsInstance(foo(6), Ok)

    def test_as_result(self) -> None:
        @as_result(ValueError)
        def foo(x: int) -> int:
            if x > 5:
                return x
            raise ValueError("x is too small")

        resA = foo(1)
        assert_type(resA, Result[int, ValueError])
        if resA.is_ok:
            assert_type(resA, Ok[int])
        else:
            assert_type(resA, Err[ValueError])

        self.assertIsInstance(foo(1), Err)
        self.assertIsInstance(foo(6), Ok)

    def test_as_result_multi_catch_types(self) -> None:
        @as_result(ValueError, TypeError)
        def foo(x: int) -> int:
            if x > 5:
                return x
            raise ValueError("x is too small")

        resA = foo(1)
        assert_type(resA, Result[int, Exception])
        if resA.is_ok:
            assert_type(resA, Ok[int])
        else:
            assert_type(resA, Err[Exception])

        self.assertIsInstance(foo(1), Err)
        self.assertIsInstance(foo(6), Ok)

    def test_and_then(self) -> None:
        def foo(x: int) -> Result[int, str]:
            if x > 5:
                return Ok(x)
            return Err("x is too small")

        @as_result(Exception)
        def add_five(x: int) -> int:
            return x + 5

        resA = foo(1).and_then(add_five)
        assert_type(resA, Ok[int] | Err[str] | Err[Exception])
        self.assertTrue(resA.is_err)
        self.assertEqual(resA.err(), "x is too small")

        resB = foo(6).and_then(add_five)
        assert_type(resB, Ok[int] | Err[str] | Err[Exception])
        self.assertTrue(resB.is_ok)
        self.assertEqual(resB.ok(), 11)

    def test_do_notation(self) -> None:
        def foo(x: int) -> Result[int, str]:
            if x > 5:
                return Ok(x)
            return Err("x is too small")

        resA: Result[int, str] = do(Ok(x + 5) for x in foo(1))
        assert_type(resA, Result[int, str])
        self.assertEqual(resA.err(), "x is too small")

        resB: Result[int, str] = do(Ok(x + 5) for x in foo(6))
        assert_type(resB, Result[int, str])
        self.assertEqual(resB.ok(), 11)

        # Two calls to foo, both succeed
        resC: Result[int, str] = do(Ok(x + y) for x in foo(6) for y in foo(6))
        assert_type(resC, Result[int, str])
        self.assertEqual(resC.ok(), 12)

        # Error in y
        resD: Result[int, str] = do(Ok(x + y) for x in foo(6) for y in foo(1))
        assert_type(resD, Result[int, str])
        self.assertEqual(resD.err(), "x is too small")

    def test_partition_results(self) -> None:
        mixed_results: list[Result[int, str]] = [
            Ok(1),
            Ok(2),
            Err("foo"),
            Ok(3),
            Err("bar"),
        ]
        oks, errs = partition_results(mixed_results)
        assert_type(oks, list[int])
        assert_type(errs, list[str])
        self.assertEqual(
            oks,
            [
                1,
                2,
                3,
            ],
        )
        self.assertEqual(
            errs,
            [
                "foo",
                "bar",
            ],
        )
