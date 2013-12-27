from flask import Flask, redirect

app = Flask(__name__)

# We only need one normal route the index
def api_index():
    return redirect("https://github.com/stevenleeg/campusdish_api#readme")
