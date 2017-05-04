# analyzeEthereum
Analysing ethereum blockchain

Objective is to download the ethereum blockchain in human readable format
Extension of this script: https://github.com/ethereum/research/blob/master/uncle_regressions/block_datadump_generator.py

To run the script
1. Install geth: https://github.com/ethereum/go-ethereum
2. Sync the geth to ethereum blockchain: 
```
$ geth --fast --cache=512 console
```
3. Export the chain using the command: 
```
$ geth export geth.dump
```
4. Install pyethapp: https://github.com/ethereum/pyethapp

5. Run the script and start downloading human readable chain as csv


