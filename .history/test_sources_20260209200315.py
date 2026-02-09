from duckduckgo_search import DDGS
import wikipedia

def test_duckduckgo(queries):
    print("\n=== DuckDuckGo Tests ===")
    try:
        with DDGS() as ddgs:
            for q in queries:
                print(f"\nQuery: {q}")
                results = list(ddgs.text(q, max_results=2))
                if results:
                    for r in results:
                        print("DuckDuckGo ✅", r["title"], "-", r["body"])
                else:
                    print("DuckDuckGo ❌ No results")
    except Exception as e:
        print("DuckDuckGo error:", e)

def test_wikipedia(queries):
    print("\n=== Wikipedia Tests ===")
    for q in queries:
        print(f"\nQuery: {q}")
        try:
            summary = wikipedia.summary(q, sentences=2)
            print("Wikipedia ✅", summary)
        except wikipedia.exceptions.DisambiguationError as e:
            print("Wikipedia ❌ Disambiguation, options:", e.options[:5])
        except Exception as e:
            print("Wikipedia error:", e)

if __name__ == "__main__":
    duck_queries = ["network domain definition", "artificial intelligence", "Python programming"]
    wiki_queries = ["Domain name", "Artificial intelligence", "Python (programming language)"]

    test_duckduckgo(duck_queries)
    test_wikipedia(wiki_queries)