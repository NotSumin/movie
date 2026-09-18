from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "flask team project!!"

    @app.route('/hsh')
    def hsh():
        return render_template('hsh.html')

    @app.route('/jsm')
    def jsm():
        return render_template('jsm.html')
    return app