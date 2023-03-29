from flask import Flask, render_template, request, redirect, session, url_for
import pymongo, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from datetime import datetime

app = Flask(__name__)
app.secret_key = "kcadmin123"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///comment.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CLOUDINARY_URL'] = 'CLOUDINARY_URL=cloudinary://345185736596456:maKIpUw92_h0SVWFGBHtO57bbqo@doyci5m01'

db = SQLAlchemy(app)

Private_Repl_URL = "https://714ba195-313b-4fba-b8cf-84ddb002db0f.id.repl.co/" # Found this Private URL in "Toggle Developers Tool" in "Webview" section inside "Resources" tab. Scroll a bit to find it with "https://*.id.repl.co/".

MONGO_URI = "mongodb+srv://devTeam:FamLearn123@cluster0.uxghxpb.mongodb.net/"

# Connect to the MongoDB cluster
client = pymongo.MongoClient(MONGO_URI, connect=False)

MONGO_DATABASE = "prod"
MONGO_COLLECTION = "collegeinfos"
COUNSELINGS_MONGO_COLLECTION = "councellings"
NEWS_MONGO_COLLECTION = "news"
EXAMS_MONGO_COLLECTION = "exams"
BLOGS_MONGO_COLLECTION = "blogs"

# Get the database
dbs = client[MONGO_DATABASE]

# Get the collection: College
collection = dbs[MONGO_COLLECTION]
counselings_collection = dbs[COUNSELINGS_MONGO_COLLECTION]
news_collection = dbs[NEWS_MONGO_COLLECTION]
exams_collection = dbs[EXAMS_MONGO_COLLECTION]
blogs_collection = dbs[BLOGS_MONGO_COLLECTION]


# 404 Error Handler
@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404


# Define the custom error handler for 503 errors
@app.errorhandler(503)
def handle_503_error(e):
	return render_template('503.html'), 503


# Define the custom error handler for 500 errors
@app.errorhandler(500)
def handle_500_error(e):
	return render_template('500.html'), 500


# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

	return render_template("./Dashboard/dashboard.html")


# Login Route
@app.route('/', methods=['GET', 'POST'])
def hello_world():
	if request.method == 'POST':
		username = request.form['login_id']
		password = request.form['login_password']
		session['username'] = username
		session['password'] = password
		if (username == 'admin' and password == 'kcadmin123'):
			return redirect(url_for("abcd"))
		elif (username == 'user1' and password == 'kc1234'):
			return redirect("/dashboard")
	return render_template('login.html')


"""
COLLEGE FUNCTIONS
"""


# College Data Collection Route [Index]: CREATE
@app.route('/index', methods=['GET', 'POST'])
def a():
	if request.method == "POST":
		college_name = request.form['college_name']
		college_uuid = request.form['college_uuid']
		college_location = request.form['college_location']
		college_state = request.form['college_state']
		college_campus_area = request.form['college_campus_area']
		header_photo_link = request.form['header_photo_link']
		college_logo_link = request.form['college_logo_link']
		overview = request.form['overview']
		nirf = request.form['nirf']
		mode_of_admission = json.loads(
		 request.form['mode_of_admission']
		) if request.form['mode_of_admission'] else None
		exams = json.loads(request.form['exams']) if request.form['exams'] else None
		railway = request.form['railway'] if request.form['railway'] else None,
		airport = request.form['airport'] if request.form['airport'] else None,
		bus = request.form['bus'] if request.form['bus'] else None,
		fees = json.loads(request.form['fees']) if request.form['fees'] else None,
		scholarships = json.loads(
		 request.form['scholarships']) if request.form['scholarships'] else None
		positives = request.form['positives']
		negatives = request.form['negatives']
		highest_package = request.form['highest_package']
		average_package = request.form['average_package']
		median_package = request.form['median_package']
		top_recruiters = request.form['top_recruiters']
		review_video = request.form['review_video']

		print(
		 f"{request.form['college_uuid']} is being added!\n({request.form['college_name']})"
		)

		nextSno = list(collection.find({}))[-1]["sno"] + 1
		college = College(
		 college_name=college_name,
		 college_uuid=college_uuid,
		 college_location=college_location,
		 college_state=college_state,
		 college_campus_area=college_campus_area,
		 header_photo_link=header_photo_link,
		 college_logo_link=college_logo_link,
		 overview=overview,
		 nirf=nirf,
		 mode_of_admission=mode_of_admission,
		 exams=exams,
		 connectivity=combineConn(railway, airport, bus),
		 fees=fees[0],
		 scholarships=scholarships,
		 # positives=positives.split(","),
		 # negatives=negatives.split(","),
		 positives=positives.split("\n"),
		 negatives=negatives.split("\n"),
		 highest_package=highest_package,
		 average_package=average_package,
		 median_package=median_package,
		 top_recruiters=top_recruiters.split(","),
		 review_video=review_video,
		 sno=nextSno,
		 approvedStatus=0)
		collegeDocument = college.generate_document_JSON()

		# Insert New Data In College DB
		inserted_id = collection.insert_one(collegeDocument).inserted_id

		print(f'\nCollege with id: {inserted_id} is now inserted in DB.\n')
		print(f'\nFull College Data:\n>>>{collegeDocument}\n')

	allComments = Comment.query.all()

	print("here in index")
	return render_template("index.html",
	                       allColleges=list(collection.find()),
	                       allComments=allComments)


# College Data Collection Route [Delete_User]: DELETE
@app.route('/delete_user/<int:sno>')
def delete_user(sno):
	deleteMongoDocument(sno, collection)
	return redirect('/index')


# College Data Collection Route [Update]: UPDATE
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
	if request.method == 'POST':
		college_name = request.form['college_name']
		college_uuid = request.form['college_uuid']
		college_location = request.form['college_location']
		college_state = request.form['college_state']
		college_campus_area = request.form['college_campus_area']
		header_photo_link = request.form['header_photo_link']
		college_logo_link = request.form['college_logo_link']
		overview = request.form['overview']
		nirf = request.form['nirf']
		mode_of_admission = json.loads(
		 request.form['mode_of_admission']
		) if request.form['mode_of_admission'] else None
		exams = json.loads(request.form['exams']) if request.form['exams'] else None
		# connectivity = request.form['connectivity']
		railway = request.form['railway'] if request.form['railway'] else None,
		airport = request.form['airport'] if request.form['airport'] else None,
		bus = request.form['bus'] if request.form['bus'] else None,
		fees = json.loads(request.form['fees']) if request.form['fees'] else None,
		scholarships = json.loads(
		 request.form['scholarships']) if request.form['scholarships'] else None
		positives = json.loads(
		 request.form['positives']) if request.form['positives'] else None
		negatives = json.loads(
		 request.form['negatives']) if request.form['negatives'] else None
		highest_package = request.form['highest_package']
		average_package = request.form['average_package']
		median_package = request.form['median_package']
		top_recruiters = json.loads(
		 request.form['top_recruiters']) if request.form['top_recruiters'] else None
		review_video = request.form['review_video']

		college = College(college_name=college_name,
		                  college_uuid=college_uuid,
		                  college_location=college_location,
		                  college_state=college_state,
		                  college_campus_area=college_campus_area,
		                  header_photo_link=header_photo_link,
		                  college_logo_link=college_logo_link,
		                  overview=overview,
		                  nirf=nirf,
		                  mode_of_admission=mode_of_admission,
		                  exams=exams,
		                  connectivity=combineConn(railway, airport, bus),
		                  fees=fees[0],
		                  scholarships=scholarships,
		                  positives=positives,
		                  negatives=negatives,
		                  highest_package=highest_package,
		                  average_package=average_package,
		                  median_package=median_package,
		                  top_recruiters=top_recruiters,
		                  review_video=review_video,
		                  sno=sno,
		                  approvedStatus=0)
		q = college.generate_document_JSON()

		print(q)

		updateMongoDocument(sno, q, collection)

		return redirect('/index')

	# Find document based on sno & pass as q
	q = list(collection.find({"sno": sno}))[0]

	q["railway"] = seperateConn(q["connectivity"])[0]
	q["bus"] = seperateConn(q["connectivity"])[1]
	q["airport"] = seperateConn(q["connectivity"])[2]
	return render_template('update.html', college=q)


"""
COUNSELINGS FUNCTIONS
"""


# Counseling Collection Route [Index]: CREATE, READ
@app.route('/counselings', methods=['GET', 'POST'])
def counselings_collection_function():

	if request.method == "POST":
		counselings_exam_name = request.form['counselings_exam_name']
		counselings_img = request.form['counselings_img']
		counselings_apply_link = request.form['counselings_apply_link']
		counselings_top_colleges = request.form[
		 'counselings_top_colleges'] if request.form[
		  'counselings_top_colleges'] != None else None
		counselings_sub_heading = request.form['counselings_sub_heading']
		counselings_date = request.form['counselings_date']

		nextSno = list(counselings_collection.find({}))[-1]["sno"] + 1
		counselingsDocument = {
		 "img": counselings_img,
		 "exam_name": counselings_exam_name,
		 "apply_link": counselings_apply_link,
		 "top_colleges": counselings_top_colleges,
		 "sub_heading": counselings_sub_heading,
		 "date": counselings_date,
		 "sno": nextSno,
		 "approvedStatus": 0
		}
		print(counselingsDocument)

		# Insert New Data In College DB
		counselings_inserted_id = counselings_collection.insert_one(
		 counselingsDocument).inserted_id

		print(counselings_inserted_id)

	print("here in counselings")
	return render_template("./Counselings/counselings.html",
	                       all_counselings=list(counselings_collection.find({})))


# Counseling Data Collection Route [Update]: UPDATE
@app.route('/update_counselings/<int:sno>', methods=['GET', 'POST'])
def update_counselings_function(sno):
	if request.method == 'POST':
		counselings_exam_name = request.form['counselings_exam_name']
		counselings_img = request.form['counselings_img']
		counselings_apply_link = request.form['counselings_apply_link']
		counselings_top_colleges = json.loads(
		 request.form['counselings_top_colleges']
		) if request.form['counselings_top_colleges'] != None else None
		counselings_sub_heading = request.form['counselings_sub_heading']
		counselings_date = request.form['counselings_date']

		# nextSno = list(counselings_collection.find({}))[-1]["sno"] + 1
		q = {
		 "img": counselings_img,
		 "exam_name": counselings_exam_name,
		 "apply_link": counselings_apply_link,
		 "top_colleges": counselings_top_colleges,
		 "sub_heading": counselings_sub_heading,
		 "date": counselings_date,
		 "sno": sno,
		 "approvedStatus": 0
		}
		print(q)

		updateMongoDocument(sno, q, counselings_collection)

		return redirect('/counselings')

	# Find document based on sno & pass as q
	q = list(counselings_collection.find({"sno": sno}))[0]

	return render_template('./Counselings/counselings_update.html', counselings=q)


# Counseling Collection Route [Delete_User]: DELETE
@app.route('/delete_user_counselings/<int:sno>')
def delete_user_counselings_function(sno):
	deleteMongoDocument(sno, counselings_collection)
	return redirect('/counselings')


"""
NEWS FUNCTIONS
"""


# News Collection Route [Index]: CREATE, READ
@app.route('/news', methods=['GET', 'POST'])
def news_collection_function():

	if request.method == "POST":
		heading_text = request.form['heading_text']
		sub_heading_text = request.form['sub_heading_text']
		icon = request.form['icon']
		header_image = request.form['header_image']
		link_to_article = request.form['link_to_article']
		date = request.form['date']

		latest = False

		nextSno = list(news_collection.find({}))[-1]["sno"] + 1
		newsDocument = {
		 "heading_text": heading_text,
		 "sub_heading_text": sub_heading_text,
		 "icon": icon,
		 "header_image": header_image,
		 "link_to_article": link_to_article,
		 "date": date,
		 "latest": latest,
		 "sno": nextSno
		}
		print(newsDocument)

		# Insert New Data In College DB
		news_inserted_id = news_collection.insert_one(newsDocument).inserted_id

		print(news_inserted_id)

	print("here in news")
	return render_template("./News/news.html",
	                       all_news=list(news_collection.find({})))


# News Data Collection Route [Update]: UPDATE
@app.route('/update_news/<int:sno>', methods=['GET', 'POST'])
def update_news_function(sno):
	if request.method == 'POST':
		heading_text = request.form['heading_text']
		sub_heading_text = request.form['sub_heading_text']
		icon = request.form['icon']
		header_image = request.form['header_image']
		link_to_article = request.form['link_to_article']
		date = request.form['date']

		latest = False

		q = {
		 "heading_text": heading_text,
		 "sub_heading_text": sub_heading_text,
		 "icon": icon,
		 "header_image": header_image,
		 "link_to_article": link_to_article,
		 "date": date,
		 "latest": latest,
		 "sno": sno
		}
		print(q)

		updateMongoDocument(sno, q, news_collection)

		return redirect('/news')

	# Find document based on sno & pass as q
	q = list(news_collection.find({"sno": sno}))[0]

	return render_template('./News/news_update.html', news=q)


# News Collection Route [Delete_User]: DELETE
@app.route('/delete_user_news/<int:sno>')
def delete_user_news_function(sno):
	deleteMongoDocument(sno, news_collection)
	return redirect('/news')


"""
EXAMS FUNCTIONS
"""


# Exam Collection Route [Index]: CREATE, READ
@app.route('/exams', methods=['GET', 'POST'])
def exams_collection_function():

	if request.method == "POST":
		exams_exam_name = request.form['exams_exam_name']
		exams_img = request.form['exams_img']
		exams_apply_link = request.form['exams_apply_link']
		exams_sub_heading = request.form['exams_sub_heading']
		exams_date = request.form['exams_date']

		nextSno = list(exams_collection.find({}))[-1]["sno"] + 1
		examsDocument = {
		 "img": exams_img,
		 "exam_name": exams_exam_name,
		 "apply_link": exams_apply_link,
		 "sub_heading": exams_sub_heading,
		 "date": exams_date,
		 "sno": nextSno
		}
		print(examsDocument)

		# Insert New Data In College DB
		exams_inserted_id = exams_collection.insert_one(examsDocument).inserted_id

		print(exams_inserted_id)

	print("here in exams")
	return render_template("./Exams/exams.html",
	                       all_exams=list(exams_collection.find({})))


# Exam Data Collection Route [Update]: UPDATE
@app.route('/update_exams/<int:sno>', methods=['GET', 'POST'])
def update_exams_function(sno):
	if request.method == 'POST':
		exams_exam_name = request.form['exams_exam_name']
		exams_img = request.form['exams_img']
		exams_apply_link = request.form['exams_apply_link']
		exams_sub_heading = request.form['exams_sub_heading']
		exams_date = request.form['exams_date']

		q = {
		 "img": exams_img,
		 "exam_name": exams_exam_name,
		 "apply_link": exams_apply_link,
		 "sub_heading": exams_sub_heading,
		 "date": exams_date,
		 "sno": sno
		}
		print(q)

		updateMongoDocument(sno, q, exams_collection)

		return redirect('/exams')

	# Find document based on sno & pass as q
	q = list(exams_collection.find({"sno": sno}))[0]

	return render_template('./Exams/exams_update.html', exams=q)


# Exam Collection Route [Delete_User]: DELETE
@app.route('/delete_user_exams/<int:sno>')
def delete_user_exams_function(sno):
	deleteMongoDocument(sno, exams_collection)
	return redirect('/exams')


"""
BLOG FUNCTIONS
"""


# Blogs Collection Route [Index]: CREATE, READ
@app.route('/blogs', methods=['GET', 'POST'])
def blogs_collection_function():

	if request.method == "POST":
		title = request.form['title']
		subheading = request.form['subheading']
		header_image = request.form['header_image']
		author = request.form['author']
		print(request.form['content'])
		content = json.loads(request.form['content']) if request.form['content'] else None
		category_id = int(request.form['category_id'])

		created_at = datetime.now()

		nextSno = list(blogs_collection.find({}))[-1]["sno"] + 1
		# nextSno = 0 + 1
		blogsDocument = {
		 "title": title,
		 "subheading": subheading,
		 "header_image": header_image,
		 "author": author,
		 "content": content,
		 "created_at": created_at,
		 "category_id": category_id,
		 "sno": nextSno,
		 "approvedStatus": False
		}
		print(blogsDocument)

		# Insert New Data In College DB
		blogs_inserted_id = blogs_collection.insert_one(blogsDocument).inserted_id

		print(blogs_inserted_id)

	print("here in blogs")
	return render_template("./Blogs/blogs.html",
	                       all_blogs=list(blogs_collection.find({})))


# Blogs Data Collection Route [Update]: UPDATE
@app.route('/update_blog/<int:sno>', methods=['GET', 'POST'])
def update_blog_function(sno):

	if request.method == 'POST':
		title = request.form['title']
		subheading = request.form['subheading']
		header_image = request.form['header_image']
		author = request.form['author']
		content = json.loads(request.form['content']) if request.form['content'] else None
		category_id = int(request.form['category_id'])

		created_at = datetime.now()

		q = {
		 "title": title,
		 "subheading": subheading,
		 "header_image": header_image,
		 "author": author,
		 "content": content,
		 "created_at": created_at,
		 "category_id": category_id,
		 "sno": sno,
		 "approvedStatus": False
		}
		print(q)

		updateMongoDocument(sno, q, blogs_collection)

		return redirect('/blogs')

	# Find document based on sno & pass as q
	q = list(blogs_collection.find({"sno": sno}))[0]

	return render_template('./Blogs/blogs_update.html', blogs=q, content=q['content'])


# Blog [Approve]: UPDATE
@app.route('/approve_blog/<int:sno>', methods=['GET', 'POST'])
def approve_blog(sno):

	updateMongoDocument(sno, {"approvedStatus": 1}, blogs_collection)
	return redirect('/adminPage')


# Blog [UnApprove]: UPDATE
@app.route('/unapprove_blog/<int:sno>', methods=['GET', 'POST'])
def unApprove_blog(sno):

	updateMongoDocument(sno, {"approvedStatus": 0}, blogs_collection)
	return redirect('/adminPage')


# Blog Data Collection Route [Delete_Admin]: DELETE
@app.route('/delete_blog_admin/<int:sno>')
def delete_blog_admin(sno):
	deleteMongoDocument(sno, blogs_collection)
	return redirect('/adminPage')


# Blogs Collection Route [Delete_User]: DELETE
@app.route('/delete_user_blog/<int:sno>')
def delete_user_blog_function(sno):
	deleteMongoDocument(sno, blogs_collection)
	return redirect('/blogs')


# Admin Functions
@app.route('/adminPage', methods=['GET', 'POST'])
def abcd():

	if request.method == "POST":
		user_name = request.form['commenter']
		sno = request.form['sno']
		message = request.form['message']

		date_created = datetime.now()

		last_comment = Comment.query.order_by(Comment.n.desc()).first()
		next = (last_comment.n + 1) if last_comment else 0

		print(f'{next}. {user_name} wrote {message} at {date_created}')
		comment = Comment(user_name=user_name,
		                  sno=sno,
		                  n=next,
		                  message=message,
		                  date_created=date_created,
		                  commentApprovedStatus=0)
		db.session.add(comment)
		db.session.commit()

	allComments = Comment.query.all()

	print(f'Total Comments: {len(allComments)}')

	nonApprovedColleges = list(collection.find({"approvedStatus": 0}))
	approvedColleges = list(collection.find({"approvedStatus": 1}))

	return render_template("approve.html",
	                       nonApprovedColleges=nonApprovedColleges,
	                       approvedColleges=approvedColleges,
	                       username=session['username'],
	                       password=session['password'],
	                       allComments=allComments)


@app.route('/delete_comment/<int:n>')
def delete_comment(n):

	comment = Comment.query.filter_by(n=n).first()
	db.session.delete(comment)
	db.session.commit()
	return redirect('/adminPage')


@app.route('/approve_comment/<int:n>', methods=['GET', 'POST'])
def approve_comment(n):

	comment = Comment.query.filter_by(n=n).first()
	print(f'S. No. {comment.n}: {comment.message} was approved.')
	comment.commentApprovedStatus = 1
	db.session.add(comment)
	db.session.commit()
	return redirect('/adminPage')


# Admin Route [Approve]: UPDATE
@app.route('/approve/<int:sno>', methods=['GET', 'POST'])
def approve(sno):

	updateMongoDocument(sno, {"approvedStatus": 1}, collection)
	return redirect('/adminPage')


# Admin Route [UnApprove]: UPDATE
@app.route('/unapprove/<int:sno>', methods=['GET', 'POST'])
def unApprove(sno):

	updateMongoDocument(sno, {"approvedStatus": 0}, collection)
	return redirect('/adminPage')


# College Data Collection Route [Delete_Admin]: DELETE
@app.route('/delete_admin/<int:sno>')
def delete_admin(sno):
	deleteMongoDocument(sno, collection)
	return redirect('/adminPage')


# Helper Route: Check for UUID Page
@app.route('/uuid', methods=['GET', 'POST'])
def checkUUID():

	isUnique = None
	collegeUUID = None
	if request.method == "POST":
		college_uuid = request.form['college_uuid']
		collegeUUID = college_uuid
		if (collection.find_one({"college_uuid": college_uuid}, {"_id": 0})):
			isUnique = True
		else:
			isUnique = False

	return render_template("uuid.html", uuidStatus=isUnique, prevUUID=collegeUUID)


# Helper Route: Show HTML College Page
# @app.route('/show/<int:sno>')
# def products(sno):
# 	allColleges = list(collection.find())
# 	allColleges = College.query.all()
# 	print(allColleges)
# 	q = list(collection.find({"sno": sno}))[0]
# 	return render_template('show.html', college=q)

# Helper Functions


def updateMongoDocument(sno, query, collection):

	update = {"$set": query}
	collection.update_one({"sno": sno}, update)
	return update, list(collection.find({"sno": sno}))


def deleteMongoDocument(sno, collection):

	collection.delete_one({"sno": sno})
	return "Deleted for" + str(sno)


def combineConn(railway, airport, bus):

	print(f'railway: {railway},\n airport: {airport},\n bus: {bus}')
	final = []

	if railway[0]:
		print('>>> Railways added!', railway[0], type(railway[0]))
		json_val = json.loads(f'[{railway[0]}]')
		if (len(json_val) > 0):
			for r in json_val:
				r[
				 'icon'] = 'https://konsa-college-website-icons.s3.ap-northeast-1.amazonaws.com/assets/icons/train.png'
				final.append(r)

	if bus[0]:
		print('>>> Buses added!', bus[0], type(bus[0]))
		json_val = json.loads(f'[{bus[0]}]')
		if (len(json_val) > 0):
			for b in json_val:
				b[
				 'icon'] = 'https://konsa-college-website-icons.s3.ap-northeast-1.amazonaws.com/assets/icons/bus.png'
				final.append(b)

	if airport[0]:
		print('>>> Airports added!', airport, type(airport))
		json_val = json.loads(f'[{airport[0]}]')
		if (len(json_val) > 0):
			for a in json_val:
				a[
				 'icon'] = 'https://konsa-college-website-icons.s3.ap-northeast-1.amazonaws.com/assets/icons/plane.png'
				final.append(a)

	return final


def seperateConn(json):

	rList = []
	bList = []
	aList = []
	for t in json:
		if t != None:
			if str(t['icon']).__contains__("train"):
				rList.append([t['trans'], t['dist']])
			if str(t['icon']).__contains__("bus"):
				bList.append([t['trans'], t['dist']])
			if str(t['icon']).__contains__("plane"):
				aList.append([t['trans'], t['dist']])
	return [rList, bList, aList]


def last_row(Table: type, *, session):  # -> Table
	primary_key = inspect(Table).primary_key.name  # must be an arithmetic type
	primary_key_row = getattr(
	 Table, primary_key)  # get first, sorted by negative ID (primary key)
	return session.query(Table).order_by(-primary_key_row).first()


class Comment(db.Model):
	n = db.Column(db.Integer, primary_key=True)
	sno = db.Column(db.Integer, primary_key=False)
	user_name = db.Column(db.String(200), nullable=False)
	message = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	commentApprovedStatus = db.Column(db.Integer, primary_key=False)


class College:

	def __init__(
	 self,
	 college_name,
	 college_uuid,
	 college_location,
	 college_state,
	 college_campus_area,
	 header_photo_link,
	 college_logo_link,
	 overview,
	 nirf,
	 mode_of_admission,
	 exams,
	 connectivity,
	 fees,
	 scholarships,
	 positives,
	 negatives,
	 highest_package,
	 average_package,
	 median_package,
	 top_recruiters,
	 review_video,
	 sno,
	 approvedStatus=0,
	):
		self.college_name = college_name
		self.college_uuid = college_uuid
		self.college_location = college_location
		self.college_state = college_state
		self.college_campus_area = college_campus_area
		self.header_photo_link = header_photo_link
		self.college_logo_link = college_logo_link
		self.overview = overview
		self.nirf = nirf
		self.mode_of_admission = mode_of_admission
		self.exams = exams
		self.connectivity = connectivity
		self.fees = fees
		self.scholarships = scholarships
		self.positives = positives
		self.negatives = negatives
		self.highest_package = highest_package
		self.average_package = average_package
		self.median_package = median_package
		self.top_recruiters = top_recruiters
		self.review_video = review_video
		self.sno = sno
		self.approvedStatus = approvedStatus

	def generate_document_JSON(self):
		return {
		 "college_name": self.college_name,
		 "college_uuid": self.college_uuid,
		 "college_location": self.college_location,
		 "college_state": self.college_state,
		 "college_campus_area": self.college_campus_area,
		 "header_photo_link": self.header_photo_link,
		 "college_logo_link": self.college_logo_link,
		 "overview": self.overview,
		 "nirf": self.nirf,
		 "mode_of_admission": self.mode_of_admission,
		 "exams": self.exams,
		 "connectivity": self.connectivity,
		 "fees": self.fees,
		 "scholarships": self.scholarships,
		 "positives": self.positives,
		 "negatives": self.negatives,
		 "highest_package": self.highest_package,
		 "average_package": self.average_package,
		 "median_package": self.median_package,
		 "top_recruiters": self.top_recruiters,
		 "review_video": self.review_video,
		 "sno": self.sno,
		 "approvedStatus": self.approvedStatus,
		}


# Support Function: Creates new thread for Flask to run endlessly
"""
def new_thread():
	while True:
		try:
			for url in db.keys():
				new_req = requests.get(url)
				if new_req.status_code == 200:
					print("successfully pinged %s" % url)
				else:
					print(new_req.status_code)
		except:
			pass
"""
import json

def fix_json(json_str):
    try:
        json.loads(json_str)
        return json_str
    except ValueError:
        fixed_str = ""
        for c in json_str:
            if c in ['{', '[', ']', '}']:
                fixed_str += c
            elif c == ',':
                fixed_str += c + ' '
            elif c == ':' and fixed_str[-1] != ' ':
                fixed_str += ' ' + c + ' '
            else:
                fixed_str += c
        try:
            json.loads(fixed_str)
            return fixed_str
        except ValueError:
            return None

# Example usage:
invalid_json = '{"foo": "bar", "baz": "qux",}'
fixed_json = fix_json(invalid_json)
if fixed_json is not None:
    print("Fixed JSON: ", fixed_json)
else:
    print("Invalid JSON")


@app.route('/comments', methods=['GET', 'POST'])
def comments():
	return render_template('./Comments/comments.html')


if __name__ == "__main__":
	# app.run(debug=True)
	# Thread(target=new_thread, daemon=True).start()
	app.run(host='0.0.0.0', port=81)
