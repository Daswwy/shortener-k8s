import os
import secrets
from flask import Flask, request, redirect, abort

app = Flask(__name__)
links = {}
VERSION = os.getenv("APP_VERSION", "dev")

@app.get("/health")
def health():
	return {"status": "ok", "version": VERSION}

@app.post("/shorten")
def shorten():
	data = request.get_json(silent=True) or {}
	url = data.get("url", "")
	if not url.startswith(("http://", "https://")):
		return {"error": "url must start with http:// or https://"}, 400
	code = secrets.token_urlsafe(4)
	links[code] = url
	return {"code": code, "short": request.host_url + code}, 201

@app.get("/<code>")
def follow(code):
	url = links.get(code)
	if url is None:
		abort(404)
	return redirect(url, 302)
