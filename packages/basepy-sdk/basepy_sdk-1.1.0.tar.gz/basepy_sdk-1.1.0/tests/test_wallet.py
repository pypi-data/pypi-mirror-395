import unittest
from basepy.wallet import Wallet

class TestWallet(unittest.TestCase):
    def test_create_wallet(self):
        wallet = Wallet.create()
        self.assertIsNotNone(wallet.address)
        self.assertIsNotNone(wallet.private_key)

    def test_import_wallet(self):
        wallet1 = Wallet.create()
        wallet2 = Wallet.from_private_key(wallet1.private_key)
        self.assertEqual(wallet1.address, wallet2.address)

if __name__ == '__main__':
    unittest.main()
