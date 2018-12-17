from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index(ldr=None):
    return render_template("index.html", ldr=ldr)

if __name__ == "__main__":
    app.run(debug=True)