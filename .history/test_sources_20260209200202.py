from duckduckgo_search import DDGS
import wikipedia

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

def test_wikipedia(query="Domain name"):
    print("\n--- Wikipedia Test ---")
    try:
        summary = wikipedia.summary(query, sentences=2)
        print("Wikipedia connected ✅")
        print(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        print("Wikipedia disambiguation ❌")
        print("Options:", e.options[:5])  # show first 5 options
    except Exception as e:
        print("Wikipedia error:", e)

if __name__ == "__main__":
    test_duckduckgo("network domain definition")
    test_wikipedia("Domain name")