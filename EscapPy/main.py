import xml.etree.ElementTree as xml
import bottle
import sqlite3 as sql

db = sql.connect("data.db")

@bottle.route("/")
def main_page():
	return bottle.static_file("static/mainmenu.html", root="./")
	
@bottle.route("/styles.css")
def stylesheet():
	return bottle.static_file("static/styles.css", root="./")
	
@bottle.route("/start/<action>")
def start(action):
	return bottle.static_file(f"static/start/{action}.html", root="./")
	
bottle.run(host="localhost", port="8000", debug=True)