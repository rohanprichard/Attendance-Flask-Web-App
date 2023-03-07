from flask import Flask, request, render_template
import attendance as at
import scrape as s

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def form_post():
    text = request.form['regno']
    passw = request.form['passw']
    try:
        df = s.getSheet(text, passw)
    except Exception:
        print("Webscrape error. Go complete your Eduserve rating and try again.")
    results, unmarked = at.calc(df)

    return render_template('results.html', results=results, unmarked=unmarked )

if __name__ == "__main__":
    app.run(debug=True)