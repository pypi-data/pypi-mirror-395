import unittest

from zenodo_client import *


class Test_ZenodoClient(unittest.TestCase):
    def setUp(self) -> None:
        with open('sandbox-token', 'r') as fp:
            access_token = fp.read().strip()
        self.client = ZenodoClient(
            host='sandbox.zenodo.org',
            access_token=access_token)

    def tearDown(self) -> None:
        pass

    def skip_test_list_depositions(self) -> None:
        deposition_list = self.client.list_depositions()
        self.assertIsInstance(deposition_list, list)
        self.assertIsInstance(deposition_list[0], dict)
        for kee in ['doi', 'doi_url', 'state']:
            self.assertIn(kee, deposition_list[0].keys())
        for kee in deposition_list[0].keys():
            self.assertIn(deposition_list[0][kee].__class__, [bool, int, str, list, dict])

    def test_metadata(self) -> None:
        nd = self.client.new_deposition()
        
        metadata = MetaData(title='ttl1', description='desc2',
            notes='did you ever think about\nmoving to Basel?',
            contributors=[Contributor(name='con1', affiliation='aff2')],
            creators=[Creator(name='crtr1', affiliation='aff3')],
            license='CC-BY-4.0', subjects=[Subject(term='xxx', identifier='https://xx.ch/yy')],
            related_identifiers=[Identifier(identifier='https://xx.ch/zz', relation=Relation.isDerivedFrom)]
        )
        r = self.client.set_metadata(deposition_id=nd['id'], metadata=metadata)['metadata']

        metadata.related_identifiers[0].scheme = 'url'  # derived by zenodo
        self.assertEqual(metadata.related_identifiers[0].relation,
                         Relation[Identifier(**r['related_identifiers'][0]).relation])

        metadata.subjects[0].scheme = 'url'  # derived by zenodo
        self.assertEqual(metadata.subjects[0], Subject(**r['subjects'][0]))

        self.client.delete(nd['id'])


if __name__ == '__main__':
    unittest.main()
