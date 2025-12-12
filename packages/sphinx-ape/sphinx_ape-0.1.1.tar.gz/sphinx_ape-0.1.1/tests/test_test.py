from pathlib import Path

from sphinx_ape.testing import DocumentationTester


class TestDocumentationTester:
    def test_test(self, temp_path):
        tester = DocumentationTester(base_path=Path(__file__).parent.parent)
        tester.test()
        assert tester.doctest_output_file.is_file()
