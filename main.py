from flask import Flask, render_template, request, jsonify
from newspaper import Article
from textblob import TextBlob
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Fetch and parse the article
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    # Perform sentiment analysis
    analysis = TextBlob(article.text)
    sentiment = "positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"

    # Format publication date
    publish_time = article.publish_date
    if publish_time:
        publish_time = publish_time.strftime('%B %d, %Y')
    else:
        publish_time = "Unknown"

    # Return article data as JSON
    return jsonify({
        'title': article.title,
        'authors': article.authors,
        'summary': article.summary,
        'publish_time': publish_time,
        'sentiment': sentiment
    })

if __name__ == '__main__':
    app.run(debug=True)
