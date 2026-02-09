from duckduckgo_search import DDGS

def test_duckduckgo(query="network domain definition"):
    print("\n--- DuckDuckGo Test ---")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                print("DuckDuckGo connected ✅")
                for r in results:
                    print(r["title"], "-", r["body"])
            else:
                print("DuckDuckGo connected but no results ❌")
    except Exception as e:
        print("DuckDuckGo error:", e)

test_duckduckgo()