from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Variable to keep track of the current position for new buttons
button_count = 0
selected_button = None

@app.route('/')
def index():
    return render_template('index.html', button_count=button_count)

@app.route('/create_button', methods=['POST'])
def create_button():
    global button_count
    button_name = request.form.get('name')
    button_id = f"button_{button_count}"
    button_count += 1
    return jsonify({'id': button_id, 'name': button_name, 'count': button_count})

@app.route('/select_button', methods=['POST'])
def select_button():
    global selected_button
    button_id = request.form.get('id')
    selected_button = button_id
    return jsonify({'selected': selected_button})

if __name__ == '__main__':
    app.run(debug=True)
