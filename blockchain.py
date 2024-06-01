import hashlib as hl
import datetime as dt
from .models import Chain, Block

# This function creates the genesis block which is the 
# first block of every blockchain.
def create_genesis_block(request, chain_id):
    chain = Chain.objects.get(pk=chain_id)
    gen_block = Block(
        index="1", 
        data="Genesis Block",
        chain=chain,
        prev_hash=0
    )
    return gen_block

# This function is used to generate a new block, given the most recent block
# and the data to be added to the current block.
def generate_next(latest_block, data):
    block = Block(
        data=data,
        index=latest_block.index + 1,
        prev_hash=latest_block.block_hash,
    )
    return block

# This function is used to add a new block with the data of the 
# attendance is added using a 'for' loop.
def add_block(request, chain):
    data = []
    i = 1
    for i in range(int(chain.strength)):
        data.append(request.POST["roll_no{}".format(i+1)])
    prev_block = Block.objects.latest('timestamp')
    block_to_add = generate_next(prev_block, data)
    block_to_add.chain = chain
    return block_to_add

# This is the function used to check whether the integrity
# of the chain has been maintained.
def check_integrity(hashes, prev_hashes, length):
    for i, current_hash in enumerate(hashes):
        if i < length - 1:
            if current_hash != prev_hashes[i+1]:
                return "The integrity has been of the blockchain has been broken. Chain is modified at #" + str(i+1)
    else:
        return "Not modified"

