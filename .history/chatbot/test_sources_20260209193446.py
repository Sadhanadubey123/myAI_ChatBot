from duckduckgo_search import DDGS
import wikipedia

def test_duckduckgo(query="domain"):
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

def test_wikipedia(query="domain"):
    print("\n--- Wikipedia Test ---")
    try:
        summary = wikipedia.summary(query, sentences=2)
        print("Wikipedia connected ✅")
        print(summary)
    except Exception as e:
        print("Wikipedia error:", e)

if __name__ == "__main__":
    test_duckduckgo("domain")
    test_wikipedia("domain")