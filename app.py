from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "감격스러운 나의 첫 백엔드"

if __name__ == "__main__":
    app.run(debug=True)