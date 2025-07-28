
import requests
import openai

# === 🔐 CONFIGURATION ===
APIFY_DATASET_ID = "your_dataset_id_here"
APIFY_API_TOKEN = "your_apify_token_here"
OPENAI_API_KEY = "your_openai_key_here"

# === 📥 FETCH PRODUCT DATA ===
def fetch_apify_data():
    url = f"https://api.apify.com/v2/datasets/{APIFY_DATASET_ID}/items?format=json"
    headers = {"Authorization": f"Bearer {APIFY_API_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch Apify data: {response.status_code}")
    return response.json()

# === 🤖 GPT PRODUCT ANALYSIS ===
def analyze_with_gpt(products):
    openai.api_key = OPENAI_API_KEY

    results = []
    for product in products[:10]:  # Limit to 10 items for quick test
        prompt = f"""Analyze this Jumia Nigeria product and provide:
1. A 2–3 sentence summary
2. A sourcing score from 1–10 for resellers
3. Any risks or notes

Title: {product.get('title')}
Price: {product.get('price')}
Rating: {product.get('rating')}
Reviews: {product.get('reviews')}
Stock: {product.get('stock')}
Category: {product.get('category')}
"""

        try:
            res = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            reply = res['choices'][0]['message']['content']
            results.append({
                "title": product.get("title"),
                "ai_summary": reply
            })
        except Exception as e:
            results.append({
                "title": product.get("title"),
                "ai_summary": f"Error: {str(e)}"
            })

    return results

# === 💾 OUTPUT RESULTS ===
def display_results(results):
    for r in results:
        print(f"\n🔹 {r['title']}")
        print(r['ai_summary'])

# === ✅ RUN SCRIPT ===
if __name__ == "__main__":
    print("📦 Fetching product data from Apify...")
    products = fetch_apify_data()

    print("🧠 Sending to OpenAI for analysis...")
    results = analyze_with_gpt(products)

    print("\n🎯 GPT Product Insights:\n")
    display_results(results)
