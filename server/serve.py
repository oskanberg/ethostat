
from twitter import twitter_stat
from flask import Flask
ts = twitter_stat()
app = Flask('ethostat')

@app.route('/query/<username>')
def twitter_term_temperature(username):
    temperature = ts.get_temperature(username)
    return 'Temperature:\t%d' % temperature

if __name__ == "__main__":
    app.run(debug=True)