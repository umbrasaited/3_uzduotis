import hashlib

from bitcoin.rpc import RawProxy

p = RawProxy()

#counting transaction payment

txid = "4410c8d14ff9f87ceeed1d65cb58e7c7b2422b2d7529afc675208ce2ce09ed7d"
raw_tx = p.getrawtransaction(txid)
decoded_tx = p.decoderawtransaction(raw_tx)
in_tx_id = []
in_id = []

for output in decoded_tx['vin']:
        in_tx_id.append(output['txid'])
        in_id.append(output['vout'])

sent = []
k = 0

for out in in_tx_id:
        raw_tx = p.getrawtransaction(out)
        decoded_tx = p.decoderawtransaction(raw_tx)
        sent.append(decoded_tx['vout'][in_id[k]]['value'])
        k += 1

got = []
raw_tx = p.getrawtransaction(txid)
decoded_tx = p.decoderawtransaction(raw_tx)

for output in decoded_tx['vout']:
        got.append(output['value'])

print("Sent:")
for a in sent:
        print(a)

print("Received: ")
for a in got:
        print(a)

print("Payment: ")
a = 0
for b in sent:
        a += b

for b in got:
        a -= b

print(a)

#check if hash is correct

def swapOrder(data):
        x = ""
        k = len(data)/2
        for i in range(0, k):
                byte = data[2*i] + data[2*i+1]
                x = byte + x
        return x

block_hash = p.getblockhash(605730)
block = p.getblock(block_hash)
header = (swapOrder(block["versionHex"]) + swapOrder(block["previousblockhash"]) +
          swapOrder(block["merkleroot"]) + swapOrder('{:08x}'.format(block["time"])) +
          swapOrder(block["bits"]) + swapOrder('{:08x}'.format(block["time"])))
                                               
header_bin = header.decode('hex')
check = hashlib.sha256(hashlib.sha256(header_bin).digest()).digest()

print("Checked hash: ")
print check[::-1].encode('hex_codec')
print("Hash: ")
print block['hash']                                                          

