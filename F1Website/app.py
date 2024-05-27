from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/',methods=['POST'])
def getCircuit():
    circuit = request.form['circuit']
    d = ["Shanmuka","Sadhu","IS"]
    return render_template('circuit.html', c = circuit, d = d)
@app.route('/',methods=['POST'])
def getComp():
    driver1 = request.form['compare']
    
    return render_template('compare.html', d1 = driver1)





if __name__ == '__main__':
    app.run(debug=True)