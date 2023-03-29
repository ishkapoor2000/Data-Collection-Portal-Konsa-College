from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///college.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class College(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    college_name = db.Column(db.String(200), nullable=False)
    header_photo_link = db.Column(db.String(200), nullable=False)
    college_logo_link = db.Column(db.String(200), nullable=False)
    overview = db.Column(db.String(200), nullable=False)
    nirf = db.Column(db.Integer, primary_key=False)
    mode_of_admission = db.Column(db.String(200), nullable=False)
    exams = db.Column(db.String(200), nullable=False)
    connectivity = db.Column(db.String(200), nullable=False)
    scholarships = db.Column(db.String(1000), nullable=False)
    positives = db.Column(db.String(1000), nullable=False)
    negatives = db.Column(db.String(1000), nullable=False)
    highest_package = db.Column(db.Integer, primary_key=False)
    average_package = db.Column(db.Integer, primary_key=False)
    median_package = db.Column(db.Integer, primary_key=False)
    top_recruiters = db.Column(db.String(200), nullable=False)
    review_video = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    approvedStatus = db.Column(db.Integer, primary_key=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.college_name}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        username = request.form['login_id']
        password = request.form['login_password']
        if (username == 'admin' and password == 'kcadmin123'):
            return redirect("/adminPage")
        elif (username == 'user1' and password == 'kc1234'):
            return redirect("/index")
    return render_template('login.html')


@app.route('/index', methods=['GET', 'POST'])
def a():
    if request.method == "POST":
        college_name = request.form['college_name']
        header_photo_link = request.form['header_photo_link']
        college_logo_link = request.form['college_logo_link']
        overview = request.form['overview']
        nirf = request.form['nirf']
        mode_of_admission = request.form['mode_of_admission']
        exams = request.form['exams']
        connectivity = request.form['connectivity']
        scholarships = request.form['scholarships']
        positives = request.form['positives']
        negatives = request.form['negatives']
        highest_package = request.form['highest_package']
        average_package = request.form['average_package']
        median_package = request.form['median_package']
        top_recruiters = request.form['top_recruiters']
        review_video = request.form['review_video']

        print(request.form['college_name'])
        college = College(college_name=college_name,
                          header_photo_link=header_photo_link,
                          college_logo_link=college_logo_link,
                          overview=overview,
                          nirf=nirf,
                          mode_of_admission=mode_of_admission,
                          exams=exams,
                          connectivity=connectivity,
                          scholarships=scholarships,
                          positives=positives,
                          negatives=negatives,
                          highest_package=highest_package,
                          average_package=average_package,
                          median_package=median_package,
                          top_recruiters=top_recruiters,
                          review_video=review_video,
                          approvedStatus=0)
        db.session.add(college)
        db.session.commit()
    allColleges = College.query.all()
    print("here in index")
    print(len(allColleges))
    # return render_template("login.html")
    return render_template("index.html", allColleges=allColleges)
    # return "Hello World!"


@app.route('/show')
def products():
    allColleges = College.query.all()
    print(allColleges)
    return "We are in the products space."


@app.route('/delete_user/<int:sno>')
def delete_user(sno):
    q = College.query.filter_by(sno=sno).first()
    db.session.delete(q)
    db.session.commit()
    return redirect('/index')


@app.route('/delete_admin/<int:sno>')
def delete_admin(sno):
    q = College.query.filter_by(sno=sno).first()
    db.session.delete(q)
    db.session.commit()
    return redirect('/adminPage')


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        college_name = request.form['college_name']
        header_photo_link = request.form['header_photo_link']
        college_logo_link = request.form['college_logo_link']
        overview = request.form['overview']
        nirf = request.form['nirf']
        mode_of_admission = request.form['mode_of_admission']
        exams = request.form['exams']
        connectivity = request.form['connectivity']
        scholarships = request.form['scholarships']
        positives = request.form['positives']
        negatives = request.form['negatives']
        highest_package = request.form['highest_package']
        average_package = request.form['average_package']
        median_package = request.form['median_package']
        top_recruiters = request.form['top_recruiters']
        review_video = request.form['review_video']
        q = College.query.filter_by(sno=sno).first()
        q.college_name = college_name
        q.header_photo_link = header_photo_link
        q.college_logo_link = college_logo_link
        q.overview = overview
        q.nirf = nirf
        q.mode_of_admissions = mode_of_admission
        q.exams = exams
        q.connectivity = connectivity
        q.scholarships = scholarships
        q.positives = positives
        q.negatives = negatives
        q.highest_package = highest_package
        q.average_package = average_package
        q.median_package = median_package
        q.top_recruiters = top_recruiters
        q.review_video = review_video
        db.session.add(q)
        db.session.commit()
        return redirect('/index')

    q = College.query.filter_by(sno=sno).first()
    return render_template('update.html', college=q)


@app.route('/adminPage', methods=['GET', 'POST'])
def abcd():
    nonApprovedColleges = list(College.query.filter_by(approvedStatus=0))
    approvedColleges = list(College.query.filter_by(approvedStatus=1))
    print(len(nonApprovedColleges))
    print(len(approvedColleges))
    return render_template("approve.html",
                           nonApprovedColleges=nonApprovedColleges)


@app.route('/approve/<int:sno>', methods=['GET', 'POST'])
def approve(sno):
    q = College.query.filter_by(sno=sno).first()
    q.approvedStatus = 1
    db.session.add(q)
    db.session.commit()
    return redirect('/adminPage')


if __name__ == "__main__":
    app.run(debug=True)
