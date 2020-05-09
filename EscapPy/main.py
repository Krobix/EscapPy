import xml.etree.ElementTree as xml
import bottle
import secrets
from base64 import b64encode, b64decode

base64encode = b64encode
base64decode = b64decode

devmode = False

pagekeys = {}
loaded_pages = {}
dev_secret = secrets.token_urlsafe(50)

def process_page(page):
	html = "<link rel='stylesheet' href='/styles.css'>"
	if devmode:
		html += f"debug:correct={page.attrib['correct-answer']}<br/> debug:pgnum={page.attrib['id']}"
	html += xml.tostring(page, encoding="unicode")
	html += f"<form action='/process/{page.attrib['id']}' method='POST'><input type='hidden' value='{page.attrib['correct-answer']}' name='correct'>ENTER ANSWER HERE:<input type='text'name='given'><input type='submit' value='submit'></form>"
	return html

@bottle.route("/")
def main_page():
	return bottle.static_file("static/mainmenu.html", root="./")
	
@bottle.route("/styles.css")
def stylesheet():
	return bottle.static_file("static/styles.css", root="./")
	
@bottle.route("/start/<action>")
def start(action):
	return bottle.static_file(f"static/start/{action}.html", root="./")
	
@bottle.route("/process/<pageid:int>", method="POST")
def process(pageid):
	pageid = int(pageid)
	correct = bottle.request.forms.get("correct")
	given = bottle.request.forms.get("given")
	if given == correct:
		for key, page in pagekeys["default"].items():
			if int(page) == pageid + 1:
				bottle.redirect(f"/escaperoom/default/{key}")
		return "<h1>u escaled,,, congration!</h1>"
	else:
		return process_page(loaded_pages["default"][pageid]) + "<script>alert('Incorrect! Please try again')</script>"
	
@bottle.route("/escaperoom/<filename>/<pagekey>")
def escaperoom_pg(filename, pagekey):
	global devmode
	if (not (filename in pagekeys)) or (pagekey=="0") or (pagekey=="-1"):
		if pagekey == "-1":
			devmode = True
		pagekeys[filename] = {}
		loaded_pages[filename] = xml.parse(f"./EscapeRooms/{filename}.xml").getroot()
		pgnum = 0
		for child in loaded_pages[filename]:
			pagekeys[filename][secrets.token_urlsafe(16)] = pgnum
			pgnum += 1
		current_page = loaded_pages[filename][0]
	else:
		current_page = loaded_pages[filename][int(pagekeys[filename][pagekey])]
	return process_page(current_page)
		
	
bottle.run(host="localhost", port="80", debug=True)