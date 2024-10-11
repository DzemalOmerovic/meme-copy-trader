import requests
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from pprint import pprint
import time

client = Client("https://api.mainnet-beta.solana.com")

WALLETS_TO_TRACK = [
  "7Chh6t175ceh1LETpvqo297e6m8MpiaYysfLqE4hMUj4"
]

def get_wallet_transactions(wallet_address: str, limit: int = 2):
  """
  Fetch recent transacitons of a wallet using Solana JSON RPC
  """
  public_key = Pubkey.from_string(wallet_address)
  response = client.get_signatures_for_address(public_key, limit=limit)
  transactions = []
  # pprint(response)
  for sig_info in response.value:
    time.sleep(5)
    pprint(sig_info.signature)
    tx = client.get_transaction(sig_info.signature, max_supported_transaction_version=0)
    transactions.append(tx)
  return transactions

def parse_transaction(transaction: list):
  """
  Parse a transaction and return the relevant information
  """
  parsed_data = []
  for tx in transaction:
    time.sleep(5)
    # pprint(dir(tx))
    pprint(tx.transaction.signatures)
    if tx.value:
      txn_signature = tx.value.transaction
      txn_details = client.get_confirmed_transaction(txn_signature)
    else:
      print("Transaction has no value")
      break

    if txn_details['result']:
      parsed_data.append({
        'signature': txn_signature,
        'slot': txn_details['result']['slot'],
        'blockTime': txn_details['result']['blockTime'],
        'amount': txn_details['result']['meta']['preTokenBalances'],
        'fee': txn_details['result']['meta']['fee'],
        'status': txn_details['result']['meta']['status']
      })
  return parsed_data

def track_wallets(wallets: list):
  """
  Track a list of wallets and print the transactions
  """
  all_transactions = []
  for wallet in wallets:
    transactions = get_wallet_transactions(wallet)
    if transactions:
      parsed_transactions = parse_transaction(transactions)
      all_transactions.extend(parsed_transactions)
    else:
      all_transactions[wallet] = "No transactions found"
  return all_transactions

# tracked_data = track_wallets(WALLETS_TO_TRACK)


def main():
  tracked_data = track_wallets(WALLETS_TO_TRACK)

  for wallet, data in tracked_data.items():
    print(f"Wallet: {wallet}")
    print(f"Transactions: {data}")
    print("\n")

if __name__ == "__main__":
  main()
