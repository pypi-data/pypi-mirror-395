import unittest

from zenodo_client import *

class Test_ZenodoClient(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_metadata(self) -> None:
        metadata = MetaData(title='t1', description='d2',
            notes='did you ever think about\nmoving to Basel?',
            contributors=[Contributor(name='con1', affiliation='aff2')],
            creators=[Creator(name='cr1', affiliation='aff3')],
            license='CC-BY-4.0',
            subjects=[Subject(term='xxx', identifier='https://xx.ch/yy', )],
            related_identifiers=[
                Identifier(
                    identifier='https://xx.ch/zz',
                    resource_type=ResourceType.publication_thesis,
                    relation=Relation.isReferencedBy)],
            version='v3'
        )
        self.assertIsInstance(metadata.contributors[0], Contributor)
        js = metadata.to_json()
        self.assertEqual(js,
            '{"metadata": {"title": "t1", "description": "d2", "upload_type": "dataset",'
            ' "contributors": [{"name": "con1", "affiliation": "aff2", "type": "DataCollector"}],'
            ' "creators": [{"name": "cr1", "affiliation": "aff3"}], "license": "CC-BY-4.0",'
            ' "notes": "did you ever think about\\nmoving to Basel?",'
            ' "related_identifiers": [{"identifier": "https://xx.ch/zz", "relation": "isReferencedBy", "resource_type": "publication-thesis"}],'
            ' "subjects": [{"term": "xxx", "identifier": "https://xx.ch/yy"}], "version": "v3"}'
            '}')


if __name__ == '__main__':
    unittest.main()
