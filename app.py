from flask import Flask, request, Response
from functions import render, db, Users
import os
from dotenv import load_dotenv

load_dotenv(verbose = True)
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/', methods = ['GET'])
def index_route():
	return "Index"

@app.route('/twilio', methods = ['POST'])
def twilio_route():
	phone_number = request.form['From']
	message = request.form['Body']

	user = Users.query.filter_by(contact = phone_number).filter_by(platform = 'twilio').first()
	if user == None:
		new_user = Users('twilio', phone_number)
		db.session.add(new_user)
		db.session.commit()
		user = Users.query.filter_by(contact = phone_number).filter_by(platform = 'twilio').first()

	response_message = render(user, message)

	xml = '<Response><Message>{}</Message></Response>'.format(response_message)
	return Response(xml, mimetype = 'text/xml')


if __name__ == "__main__":
	app.run(debug = True, use_reloader = True)