from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_name():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Please provide "name" in the JSON body'}), 400

    full_name = data['name']
    names = full_name.split()
    
    results = []
    for i, name in enumerate(names):
        results.append({
            'name': name,
            'length': len(name),
            'position': f"{i + 1}º nome",
            'reversed': name[::-1]
        })
        
    return jsonify({
        'original_name': full_name,
        'analysis': results
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
