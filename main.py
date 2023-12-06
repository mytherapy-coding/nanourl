import url_shortener

if __name__ == "__main__":
    url_shortener.app.run(host="0.0.0.0", port=5000, debug=True)
    print("Main is called")
