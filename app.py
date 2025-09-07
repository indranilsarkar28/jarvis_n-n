from flask import Flask, request, jsonify, render_template
import requests
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key="AIzaSyABs3D46oI4d7rJBFXrtZC3i6EsQl1C79k")  # replace with your key

def get_news():
    api_key = "b9d20d36e92d4358ab53a44ad7f36997"   # replace with your newsapi key
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url).json()
    articles = response.get("articles", [])
    return [a.get("title", "No title") for a in articles[:5]]

def ask_ai(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text if response and response.text else "Sorry, I have no response."
    except Exception as e:
        return f"Error with AI: {e}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query", "")
    query = query.lower()

    if "open youtube" in query:
        return jsonify({"reply": "Opening YouTube", "url": "https://youtube.com"})
    elif "open google" in query:
        return jsonify({"reply": "Opening Google", "url": "https://google.com"})
    elif "news" in query:
        headlines = get_news()
        return jsonify({"reply": "Here are today’s top news:", "news": headlines})
    else:
        reply = ask_ai(query)
        return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
