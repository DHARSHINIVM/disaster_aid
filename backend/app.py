from flask import Flask, request, jsonify
from verification import verify_ngo_darpan
from supabase_client import save_verified_ngo
from config import INFURA_URL, CONTRACT_ADDRESS, OWNER_PRIVATE_KEY
from web3 import Web3
import json

app = Flask(__name__)

# Web3 & Contract setup
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
with open("NGOFundTrackerABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)
owner = w3.eth.account.from_key(OWNER_PRIVATE_KEY)

@app.route("/verify_ngo", methods=["POST"])
def verify_ngo():
    data = request.get_json()
    reg_id = data.get("registration_id")
    wallet_address = data.get("wallet_address")

    if not reg_id or not wallet_address:
        return jsonify({"error": "Missing parameters"}), 400

    result = verify_ngo_darpan(reg_id)

    if result["valid"]:
        # Save in Supabase
        save_verified_ngo(result["name"], reg_id, wallet_address)

        # Register in smart contract
        nonce = w3.eth.get_transaction_count(owner.address)
        tx = contract.functions.registerNGO(wallet_address, result["name"]).build_transaction({
            "from": owner.address,
            "gas": 300000,
            "nonce": nonce,
        })

        signed_tx = w3.eth.account.sign_transaction(tx, OWNER_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        return jsonify({
            "message": "NGO verified and registered on blockchain.",
            "tx_hash": tx_hash.hex()
        })

    else:
        return jsonify({"error": "NGO not valid"}), 403

if __name__ == "__main__":
    app.run(debug=True)
