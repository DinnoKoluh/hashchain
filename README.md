# About `hashchain`
This repository contains an implementation of a blockchain using Python called `hashchain`.
The blockchain implementation uses a proof-of-work consensus algorithm.
## Account handling
Hashchain uses an account-based system for handling transactions. Each account has a unique address which is the hash of the user's public key, so it is easy to validate an account with the user's private key (private key $\rightarrow$ public key $\rightarrow$ address).  Upon account creation a file containing the private key is automatically downloaded. The private key is not stored in the blockchain database, so the user has the only available copy. The private key should be kept safe as it is the only way to send transactions and validate one's account.

## Transaction handling
A transaction object contains the `from_address` (who submitted the transaction), `to_address` (to whom the transaction is being sent), `message` (any string of characters of maximum length $512$), the `signature` (used to verify the validity of the transaction) and the `public_key` (used to verify the signature).

The private key is required for transaction signing, so submitting any transaction will also require the private key to be presented. This ensures that the key holder and the account which submits the transaction are the same user. Transactions can only be sent to addresses that are linked to an account, so that a user cannot input a random address and send a transaction to it.

### Currency system
The currency name of hashchain is called `atom` denoted by `A`. The currency is by default an integer value, and the smallest amount (cannot be broken down further) is $1A$.

### Fee system
When sending a transaction of amount $X$, the account holder has to have a balance of at least $X + \delta$ where $\delta$ is the fee associated with the transaction. This ensures that $X$ will be sent to the payee but $X + \delta$ will be deducted from the sender.

All transactions have a flat fee of $1A$. If the transaction exceeds $99A$ a fee of $1$% on the transaction value floored is added to the flat fee.

Example: A transaction of $12A$ has a fee of $1A$, whereas a transaction of $150A$ as a fee of $2A$ ($1A$ flat fee $+$ $\lfloor 0.01 \cdot 150A \rfloor$).

### Balance system
An account has two types of balances, the `balance` and `pending_balance`. If the user doesn't have any pending transactions (transactions to be executed when a block is mined) the balance and pending balance are the same. 

Let us assume that an account has a balance of $X$ and the user submits a transaction of value $Y$. As the transaction has not been executed yet, the account's balance is still $X$ but the pending balance is $X-Y$ which is the new balance that can be actually spent. The pending balance is used to ensure that while one transaction is waiting to be executed users cannot submit multiple transactions which would exceed their balance. If now, while waiting for the first transaction to be executed, the user sends another transaction of value $Z$, and $Z > X - Y$, the pending balance would go below $0$ and the backend mechanism ensures that the transaction will not be submitted.

## Blockchain handling
The creation of the `genesis` block is hardcoded such that the first account that is registered to hashchain is by default the genesis block miner. The accounts balance will be set to a predefined value and this is the case only for the first account created, all accounts created after the first one will have a default balance of $0A$. The genesis block is empty by default. Other blocks are not. A block object contains the `previous_hash` (hash of the previous block), `timestamp`, `transaction data`, `miner_address` and the `hash` (their own hash which is calculated from the just mentioned attributes). A block has to have at least one transaction to be able to be mined i.e. empty blocks cannot be mined except the hard-coded genesis block. 

### Block mining
Any user can mine a block. To mine a block the miner has to solve a hash puzzle (enforce that the hash of the block data has a certain number of leading zeros, that number is regarded as the `difficulty` of the puzzle). When the miner solves the puzzle a block reward and the fees of all transaction are given as the total reward to the miner. The block reward is the only way new coins are minted. 

## To be addressed:
* Reducing reward after certain number of blocks?
* Limit the number if transactions contained inside one block?
* Keeping the difficulty constant or changing it such that the time required to mined a block it kept constant?
* Establishing P2P network for blockchain validation between miners?

# How to run the project
Firstly create a new virtual environment inside the root of the repository.
```bash
python -m venv venv 
```
Activate the virtual environment:
```bash
python venv/Scripts/activate 
```
After activating the environment, install all the required packages from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```
Now, move to the `bc_site` directory:
```bash
cd bc_site
```
The next steps are required to setup `django` and create a database:
```bash
python manage.py makemigrations
python manage.py migrate 
```
And finally, to start the server, execute:
```bash
python manage.py runserver
```