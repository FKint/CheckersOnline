from flask import Flask, jsonify

app = Flask("Checkers Online AI Server")
app.config.from_pyfile('config.cfg')


@app.route('/')
def index():
    return jsonify({"error": None})


def main():
    app.run(host=app.config['HOSTNAME'])


if __name__ == "__main__":
    main()
