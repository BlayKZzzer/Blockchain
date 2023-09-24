from flask import Flask, render_template, request, jsonify
from blckchain import Blckchain

app = Flask(__name__)
blockchain = Blckchain()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mine', methods=['POST'])
def mine():
    last_block=blockchain.chain[-1]
    last_proof=last_block.proof
    proof=blockchain.proof_of_work(last_proof)
    # Replace with your wallet address
    blockchain.add_transaction(
        sender="0", recipient="bc1qjhszc2qv8wtvlqmx6zrur5mscg38qwxyktpfeu", amount=1)
    block=blockchain.create_block(proof)
    response={
        'message': 'Block mined successfully!',
        'block': {
            'index': block.index,
            'previous_hash': block.previous_hash,
            'proof': block.proof,
            'timestamp': block.timestamp,
            'transactions': block.transactions,
        }
    }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    response=[block.to_dict() for block in blockchain.chain]
    return jsonify(response), 200


if __name__=='__main__':
    app.run(host='0.0.0.0', port=3000)
