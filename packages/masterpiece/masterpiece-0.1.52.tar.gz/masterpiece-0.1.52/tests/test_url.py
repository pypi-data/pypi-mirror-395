import unittest
from masterpiece.url import URL


class TestURL(unittest.TestCase):
    def test_initialization(self) -> None:
        url = URL("/foo/bar")
        self.assertEqual(url.get(), "/foo/bar")
        self.assertTrue(url.is_absolute())

        url = URL("foo/bar")
        self.assertEqual(url.get(), "foo/bar")
        self.assertFalse(url.is_absolute())

        url = URL("")
        self.assertEqual(url.get(), "")
        self.assertTrue(url.is_empty())

    def test_push_tail(self) -> None:
        url = URL("/foo")
        url.push_tail("bar")
        self.assertEqual(url.get(), "/foo/bar")

    def test_push_head(self) -> None:
        url = URL("/bar")
        url.push_head("foo")
        self.assertEqual(url.get(), "/foo/bar")

    def test_pop_tail(self) -> None:
        url = URL("/foo/bar")
        tail = url.pop_tail()
        self.assertEqual(tail, "bar")
        self.assertEqual(url.get(), "/foo")

    def test_pop_head(self) -> None:
        url = URL("/foo/bar")
        head = url.pop_head()
        self.assertEqual(head, "foo")
        self.assertEqual(url.get(), "/bar")

    def test_normalize(self) -> None:
        url = URL("/foo/./bar/../baz")
        url.normalize()
        self.assertEqual(url.get(), "/foo/baz")

        url = URL("../foo/./bar/../baz")
        url.normalize()
        self.assertEqual(url.get(), "../foo/baz")

    def test_is_absolute(self) -> None:
        url = URL("/foo/bar")
        self.assertTrue(url.is_absolute())

        url = URL("foo/bar")
        self.assertFalse(url.is_absolute())

    def test_make_absolute(self) -> None:
        base = URL("/root")
        relative = URL("child/grandchild")
        absolute = relative.make_absolute(base)
        self.assertEqual(absolute.get(), "/root/child/grandchild")

    def test_prepend_base(self) -> None:
        url = URL("foo/bar")
        url.prepend_base("/root")
        self.assertEqual(url.get(), "/root/foo/bar")

        url = URL("../foo")
        url.prepend_base("/root")
        self.assertEqual(url.get(), "/root/../foo")

    def test_starts_with(self) -> None:
        url = URL("/foo/bar")
        self.assertTrue(url.starts_with("foo"))
        self.assertFalse(url.starts_with("bar"))

    def test_copy(self) -> None:
        url = URL("/foo/bar")
        copy = url.copy()
        self.assertEqual(copy.get(), "/foo/bar")
        self.assertIsNot(copy, url)  # Ensure the copy is a different object

    def test_is_empty(self) -> None:
        url = URL("")
        self.assertTrue(url.is_empty())

        url = URL("foo")
        self.assertFalse(url.is_empty())

    def test_string_representation(self) -> None:
        url = URL("/foo/bar")
        self.assertEqual(str(url), "/foo/bar")
        self.assertEqual(repr(url), "URL('/foo/bar')")


if __name__ == "__main__":
    unittest.main()
