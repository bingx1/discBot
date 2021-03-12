from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return ('Hello World')

@app.route('/api/items/all', methods=['GET'])
def fetch_all_items():
    return

if __name__ == "__main__":
    app.run()