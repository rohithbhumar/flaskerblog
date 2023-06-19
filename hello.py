from flask import Flask, render_template

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route("/")
def hello():
    return render_template('hello.html')

@app.route("/user/<name>")
def user(name):
    return render_template('jinja.html', name=name)

#custom error page

# invalid url
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#internal server error
@app.errorhandler(500)
def internal_server_e(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)