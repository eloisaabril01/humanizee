from flask import Flask, render_template, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
import random

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

def analyze_text_complexity(text):
    # Placeholder complexity calculation
    return 0.1

def humanize(text):
    text = text.lower()
    text = text.replace("i would", "i think")
    text = text.replace(".", "... ")
    text = text.replace(",", " and")
    
    casual_starters = [
        "basically", "honestly", "i think", "from what i understand",
        "as far as i know", "in my opinion", "you see", "like",
        "the thing is", "i mean", "so basically", "i believe"
    ]
    
    fillers = [
        "kind of", "sort of", "pretty much", "you know",
        "like", "actually", "basically", "probably"
    ]
    
    sentences = text.split(". ")
    humanized = []
    
    for sentence in sentences:
        if not sentence.strip():
            continue
        sentence = sentence.strip()
        
        # Add random starter if sentence doesn't already have one
        if not any(sentence.startswith(starter) for starter in casual_starters):
            sentence = random.choice(casual_starters) + ", " + sentence
        
        # Occasionally add filler words
        if random.random() < 0.3 and len(sentence.split()) > 3:
            words = sentence.split()
            insert_pos = random.randint(2, len(words)-1)
            words.insert(insert_pos, random.choice(fillers))
            sentence = " ".join(words)
            
        humanized.append(sentence)

    return " ".join(humanized)

def detect_ai(text):
    # Simple heuristic-based detection for demonstration
    ai_indicators = ["furthermore", "in conclusion", "overall", "therefore"]
    words = text.lower().split()
    score = sum(1 for w in words if w in ai_indicators) / max(1, len(words))
    if score > 0.02 or len(words) > 150:
        return {"message": "⚠️ Likely AI-generated text detected."}
    return {"message": "✅ This text appears mostly human-like."}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/humanize', methods=['POST'])
def humanize_text():
    data = request.json
    text = data.get('text', '')

    humanized_text = humanize(text)
    score = analyze_text_complexity(text)

    return jsonify({
        'humanized_text': humanized_text,
        'score': score,
        'original_words': len(text.split()),
        'humanized_words': len(humanized_text.split())
    })

@app.route('/detect', methods=['POST'])
def detect_text():
    data = request.json
    text = data.get('text', '')
    result = detect_ai(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=19482, debug=True)
