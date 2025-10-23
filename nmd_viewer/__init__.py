from flask import Flask

from .routes import bp

app = Flask(__name__)
app.register_blueprint(bp)



if __name__ == "__main__":
    # run current_app in debug mode on port 5000
    app.run(debug=True, port=5000, host='0.0.0.0')
