# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 19:56:57 2017

@author: a.chiplunkar
"""

import rlp
from ethereum.blocks import BlockHeader
from ethereum.transactions import Transaction
from ethereum import utils
import csv
 
def openCSVWriter(file_name):
    pointer_csv = open(file_name, 'wb')
    csv_writer = csv.writer(pointer_csv, dialect='excel')
    return [pointer_csv, csv_writer]

blknum, pos = 0, 0
# gethDumpFileName = 'geth-914358.dump'
# gethDumpFileName = 'geth-1055375.dump'
gethDumpFileName = 'geth-3604935.dump'
f = open(gethDumpFileName)
blockData = []
transactionData = []
 
startBlock = 0
endBlocks =  [100000*l for l in range(1, 37)]


for endBlock in endBlocks:
    txStarted = 0
    uncStarted = 0
    pointer_csv_file_blockData, blockWriter = openCSVWriter("blockData_%s.csv" % (endBlock,))
    pointer_csv_file_transactionData, transactionWriter = openCSVWriter("transactionData_%s.csv" % (endBlock,))
    pointer_csv_file_uncleData, uncleWriter =  openCSVWriter("uncleData_%s.csv" % (endBlock,))
    
    while (blknum < endBlock):
        f.seek(pos)
        prefix = f.read(10)
        _typ, _len, _pos = rlp.codec.consume_length_prefix(prefix, 0)
        blkdata = prefix + f.read(_pos + _len - 10)
        header = rlp.decode(rlp.descend(blkdata, 0), BlockHeader)
        headerDictionary = header.to_dict()
        del headerDictionary['bloom']

        if blknum%100000==0:
            list_columnNames = headerDictionary.keys()
            list_columnNames.append('pos')
            list_columnNames.append('txcount')
            list_columnNames.append('unclecount')
            blockWriter.writerow(list_columnNames)
            print 'reached here'
            
        list_blockvalues = [ v for v in headerDictionary.values()]
        list_blockvalues.append(pos)
        txCount = len(rlp.decode(rlp.descend(blkdata, 1)))
        uncleCount = len(rlp.decode(rlp.descend(blkdata, 2)))  
        list_blockvalues.append(txCount)   
        list_blockvalues.append(uncleCount)
        blockWriter.writerow(list_blockvalues)

        for i in range(0, txCount):
            tempTx = rlp.decode(rlp.descend(blkdata, 1, i), Transaction)
            tempTxDictionary = tempTx.to_dict()        
            listTransactionValues = [v for v in tempTxDictionary.values()]
            listTransactionValues.insert(0, header.number)
            listTransactionValues[3] = utils.decode_addr(listTransactionValues[3])
            listTransactionValues[6] = utils.decode_addr(listTransactionValues[6])
            # print list_transactionValues    
            if txStarted==0:
                listTransactionColumnNames = tempTxDictionary.keys()
                listTransactionColumnNames.insert(0, 'blocknumber')
                transactionWriter.writerow(listTransactionColumnNames)
                txStarted = 1            
                
            transactionWriter.writerow(listTransactionValues)

        for i in range(0, uncleCount):
            tempUncle = rlp.decode(rlp.descend(blkdata, 2, i), BlockHeader)
            tempUncleDictionary = tempUncle.to_dict()
            del tempUncleDictionary['bloom']
            listUncleValues = [v for v in tempUncleDictionary.values()]
            listUncleValues.insert(0, header.number)
            if uncStarted==0:
                listUncleColumnNames = tempUncleDictionary.keys()
                listUncleColumnNames.insert(0, 'blocknumber')
                uncleWriter.writerow(listUncleColumnNames)
                uncStarted=1
                
            uncleWriter.writerow(listUncleValues)
        pos += _pos + _len
        blknum = blknum+1
        
        if blknum%10000==0:
            print blknum
        

    pointer_csv_file_blockData.close()
    pointer_csv_file_transactionData.close()
    pointer_csv_file_uncleData.close()


    
