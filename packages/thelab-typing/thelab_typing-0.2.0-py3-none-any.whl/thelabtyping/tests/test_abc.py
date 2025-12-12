from unittest import TestCase

import pydantic

from thelabtyping.abc import DictOf, ListOf


class Person(pydantic.BaseModel):
    name: str


class PersonList(ListOf[Person]):
    pass


Data = DictOf[str, int]


class ListOfTest(TestCase):
    def setUp(self) -> None:
        self.people = PersonList.model_validate(
            [
                {"name": "Jack"},
                {"name": "Diane"},
            ]
        )

    def test_isinstance(self) -> None:
        self.assertIsInstance(self.people, PersonList)
        self.assertIsInstance(self.people[0], Person)

    def test_index_accessors(self) -> None:
        self.assertEqual(self.people[0].name, "Jack")
        self.assertEqual(self.people[1].name, "Diane")

    def test_iteration(self) -> None:
        names = ["Jack", "Diane"]
        for i, person in enumerate(self.people):
            self.assertEqual(person.name, names[i])


class DictOfTest(TestCase):
    def test_dunders(self) -> None:
        data = Data({})
        self.assertEqual(data.model_dump(), {})

        # __setitem__
        data["test"] = 42
        self.assertEqual(data.model_dump(), {"test": 42})

        # __getitem__
        self.assertEqual(data["test"], 42)

        # __contains__
        self.assertIn("test", data)
        self.assertNotIn("foo", data)

        # __iter__
        self.assertEqual(list(data), ["test"])

        # __len__
        self.assertEqual(len(data), 1)

        # keys
        self.assertEqual(list(data.keys()), ["test"])

        # values
        self.assertEqual(list(data.values()), [42])

        # items
        self.assertEqual(list(data.items()), [("test", 42)])

        # get
        self.assertEqual(data.get("test"), 42)
        self.assertEqual(data.get("foo"), None)

        # setdefault
        self.assertEqual(data.setdefault("foo", 10), 10)
        self.assertEqual(data.setdefault("test", 10), 42)

        # update
        data.update({"foo": 5})
        self.assertEqual(data["foo"], 5)

        # pop
        self.assertEqual(data.pop("foo"), 5)
        self.assertEqual(data.model_dump(), {"test": 42})

        # popitem
        data["foo"] = 10
        self.assertEqual(data.popitem(), ("foo", 10))
        self.assertEqual(data.model_dump(), {"test": 42})

        # __delitem__
        del data["test"]
        self.assertEqual(data.model_dump(), {})

        # clear
        data["test"] = 42
        self.assertEqual(data.model_dump(), {"test": 42})
        data.clear()
        self.assertEqual(data.model_dump(), {})
