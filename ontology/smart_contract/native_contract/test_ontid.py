from unittest import TestCase

from ontology.account.account import Account
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.rpc.rpc import RpcClient
from binascii import a2b_hex

from ontology.smart_contract.native_contract import ontid

rpc_address = "http://polaris3.ont.io:20336"
rpc_address = "http://127.0.0.1:20336"
private_key = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key2 = "c19f16785b8f3543bbaf5e1dbb5d398dfa6c85aaad54fc9d71203ce83e505c07"
acc = Account(a2b_hex(private_key.encode()), SignatureScheme.SHA256withECDSA)
acc2 = Account(a2b_hex(private_key2.encode()), SignatureScheme.SHA256withECDSA)
cli = RpcClient(0, rpc_address)
did = "did:ont:" + acc.get_address_base58()


class test_ontid(TestCase):

    def test_new_registry_ontid_transaction(self):
        tx = ontid.new_registry_ontid_transaction(did, acc.get_public_key(), 20000, 500)
        tx = cli.sign_transaction(tx, acc)
        print(tx.hash256().hex())
        print(tx.serialize().hex())
        cli.send_raw_transaction(tx)

    def test_new_get_ddo_transaction(self):
        tx = ontid.new_get_ddo_transaction(did)
        ddo = cli.send_raw_transaction_preexec(tx)
        print(ddo)
        print(ontid.parse_ddo(did, ddo))

    def test_new_add_attribute_transaction(self):
        attris = []
        attri = {}
        attri["key"] = "key1"
        attri["type"] = "string"
        attri["value"] = "value100"
        attris.append(attri)
        tx = ontid.new_add_attribute_transaction(did, acc.get_public_key(), attris, acc.get_address_base58(), 20000,
                                                 500)
        tx = cli.sign_transaction(tx, acc)
        cli.send_raw_transaction(tx)

    def test_new_remove_attribute_transaction(self):
        tx = ontid.new_remove_attribute_transaction(did,acc.get_public_key(),"key1",acc.get_address_base58(),20000,500)
        tx = cli.sign_transaction(tx, acc)
        cli.send_raw_transaction(tx)

    def test_new_add_pubkey_transaction(self):
        tx = ontid.new_add_pubkey_transaction(did, acc.get_public_key(), acc2.get_public_key(), acc.get_address_base58(), 20000,
                                                    500)
        tx = cli.sign_transaction(tx, acc)
        cli.send_raw_transaction(tx)

    def test_new_remove_pubkey_transaction(self):
        tx = ontid.new_remove_pubkey_transaction(did, acc.get_public_key(), acc2.get_public_key(), acc.get_address_base58(), 20000,
                                                    500)
        tx = cli.sign_transaction(tx, acc)
        cli.send_raw_transaction(tx)

    def test_new_add_recovery_transaction(self):
        tx = ontid.new_add_rcovery_transaction(did, acc.get_public_key(), acc2.get_address_base58(), acc.get_address_base58(), 20000,
                                                    500)
        tx = cli.sign_transaction(tx, acc)
        cli.send_raw_transaction(tx)
