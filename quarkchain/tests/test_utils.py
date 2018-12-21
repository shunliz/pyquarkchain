import pytest
import random

from quarkchain.core import (
    Address,
    Transaction,
    TransactionInput,
    TransactionOutput,
    Code,
    random_bytes,
)

from quarkchain.utils import token_id_encode, token_id_decode


def create_test_transaction(
    from_id,
    from_tx_id,
    to_address,
    amount=100,
    remaining=100,
    shard_id=0,
    output_index=0,
    code=Code.get_transfer_code(),
):
    acc1 = Address.create_from_identity(from_id, shard_id)
    tx = Transaction(
        in_list=[TransactionInput(from_tx_id, output_index)],
        code=code,
        out_list=[
            TransactionOutput(acc1, remaining),
            TransactionOutput(to_address, amount),
        ],
    )
    tx.sign([from_id.get_key()])
    return tx


def create_random_test_transaction(from_id, to_address, amount=100, remaining=100):
    return create_test_transaction(
        from_id,
        random_bytes(32),
        to_address,
        random.randint(0, 100),
        random.randint(0, 100),
    )


ENCODED_VALUES = [
    ("0", 0),
    ("Z", 35),
    ("00", 36),
    ("0Z", 71),
    ("1Z", 107),
    ("20", 108),
    ("ZZ", 1331),
    ("QKC", 35760),
    ("ZZZZZZZZZZZZ", 4873763662273663091),
    # ("2V4D00153RFRF", 2**64-1),
]


@pytest.mark.parametrize("name, id", ENCODED_VALUES)
def test_token_id_encode(name, id):
    assert token_id_encode(name) == id
    assert name == token_id_decode(id)
