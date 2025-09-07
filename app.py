from flask import Flask, request, render_template, jsonify
import whois

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_domains', methods=['POST'])
def check_domains():
    data = request.get_json()
    domains = [d.strip() for d in data.get("domains", []) if d.strip()]
    results = []

    for domain in domains:
        try:
            w = whois.whois(domain)
            # If 'domain_name' is None, it means domain is available
            available = not bool(w.domain_name)
        except Exception:
            # Any exception, assume available
            available = True

        results.append({
            "domain": domain,
            "available": available
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)