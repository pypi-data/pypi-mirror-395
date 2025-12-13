import sys, json

def main():
    req = json.load(sys.stdin)
    text = req.get("inputs", {}).get("text", "")
    res = {"status": "ok", "outputs": {"text": text}}
    json.dump(res, sys.stdout)

if __name__ == "__main__":
    main()

