from flask import Flask, render_template, request
import main
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/result', methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]
    return render_template('index.html', name=name)


@app.route('/alg1', methods=['POST', 'GET'])
def alg1():
    result = main.PLACE_Long_Put_Options()
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)