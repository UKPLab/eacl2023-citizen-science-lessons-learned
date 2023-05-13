import hashlib
import logging
import os
import sys

import sqlalchemy as db
from flask import Flask, request, redirect, render_template, flash
from flask import session as fsession
from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(stream=sys.stderr)

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'webapp.db'),
    USERNAME='webadmin',
    PASSWORD='admin',
    SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
))

engine = create_engine("sqlite:///citizen.db")
metadata_obj = db.MetaData()


CHANNELS = [
    "twitter",
    "facebook",
    "linkedin",
    "mailing",
    "stellenwerk",
    "other"
]

##################################################################
#		DATABASE TABLES
##################################################################

Users = db.Table(
    'user',
    metadata_obj,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column('username', db.String),
    db.Column('password', db.String),
    db.Column('email', db.String),
    db.Column('name', db.String),
    db.Column('address', db.String)
)

Studies = db.Table(
    'study',
    metadata_obj,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column('name', db.String),
    db.Column('url', db.String),
    db.Column('purpose', db.String),
    db.Column('data_usage', db.String),
    db.Column('data_publication', db.String),
    db.Column('data_deletion', db.String),
    db.Column('questionnaire', db.String),
)

Consents = db.Table(
    'consent',
    metadata_obj,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column('name', db.String),
    db.Column('personal', db.String),
)

UserStudyMaps = db.Table(
    'user_study_map',
    metadata_obj,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column('user_id', db.Integer),
    db.Column('study_id', db.Integer),
)

ConsentStudyMaps = db.Table(
    'consent_study_map',
    metadata_obj,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column('consent_id', db.Integer),
    db.Column('study_id', db.Integer),
)

Channels = db.Table(
    'channel',
    metadata_obj,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column('study_id', db.Integer),
    db.Column('name', db.String),
    db.Column('url', db.String),
    db.Column('count', db.Integer),
)

metadata_obj.create_all(engine)
Base = automap_base(metadata=metadata_obj)
Base.prepare()

User = Base.classes.user
Study = Base.classes.study
Consent = Base.classes.consent
ConsentStudyMap = Base.classes.consent_study_map
UserStudyMap = Base.classes.user_study_map
Channel = Base.classes.channel

##################################################################
#		DATABASE FUNCTIONS
##################################################################

# Create session with all tables
def create_session():
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def check_user_credentials(username, password):
    session = create_session()
    try:
        user_id = session.query(Users).filter_by(name=username).first().id
        phash = session.query(Users).filter_by(name=username).first().password
        phash_tmp = hashlib.sha512(bytes(password, 'utf-8')).hexdigest()
        if phash == phash_tmp:
            session.commit()
            session.close()
            return True
        else:
            return False

    except AttributeError:
        session.commit()
        session.close()
        return False


def add_user(username, password, email, name, address):
    session = create_session()
    try:
        user_id = session.query(Users).filter_by(username=username).first().id
        session.commit()
        session.close()
        return False

    except AttributeError:
        # Set user credentials 
        passwordhash = hashlib.sha512(bytes(password, 'utf-8')).hexdigest()

        session.add(
            User(username=username, password=passwordhash, email=email, name=name, address=address)

        )
        session.commit()

    session.commit()
    session.close()
    return True


def get_public_data():
    session = create_session()
    data = session.query(Consent).filter_by(personal=0).all()
    result = [{'id': d.id, 'name': d.name} for d in data]
    session.commit()
    session.close()
    return result


def get_personal_data():
    session = create_session()
    data = session.query(Consent).filter_by(personal=1).all()
    result = [{'id': d.id, 'name': d.name} for d in data]
    session.commit()
    session.close()
    return result


def get_consent_data(study_id):
    session = create_session()
    personal = []
    public = []
    data = session.query(ConsentStudyMap).filter_by(study_id=study_id).all()
    for dat in data:
        datatype = session.query(Consent).filter_by(id=dat.consent_id).first()
        if datatype.personal == 1:
            personal.append(datatype.name)
        else:
            public.append(datatype.name)
    session.commit()
    session.close()
    return {"personal": personal, "public": public}


# NOTE: Only use, when logged in!
def get_user_id(username):
    session = create_session()
    user_id = session.query(Users).filter_by(username=username).first().id
    session.close()
    return user_id


def get_studies():
    session = create_session()
    studies = session.query(Studies).all()
    study_data = [{'id': s.id, 'name': s.name} for s in studies]
    session.close()
    return study_data


def get_study_id(sname):
    session = create_session()
    try:
        sid = session.query(Studies).filter_by(name=sname).first().id
        session.commit()
        session.close()
        return sid

    except AttributeError:

        session.commit()
        session.close()

    return False


def get_study_data(sid):
    session = create_session()
    study_data = session.query(Studies).filter_by(id=sid).first()
    name = study_data.name
    url = study_data.url
    purpose = study_data.purpose
    usage = study_data.data_usage
    publication = study_data.data_publication
    deletion = study_data.data_deletion
    questionnaire = study_data.questionnaire
    session.commit()
    session.close()
    return {"name": name,
            "url": url,
            "purpose": purpose,
            "usage": usage,
            "publication": publication,
            "deletion": deletion,
            "questionnaire": questionnaire}


def get_link_data(sid, channel):
    session = create_session()
    study_stats = session.query(Channels).filter_by(study_id=sid, name=channel).first()
    session.query(Channels).filter_by(study_id=sid, name=channel).update({"count": study_stats.count + 1})

    study = session.query(Studies).filter_by(id=sid).first()

    session.commit()
    session.close()
    return study.url


def add_study(name, url, purpose, data_usage, data_publication, data_deletion, questionnaire):
    session = create_session()
    session.add( Study(name=name, url=url, purpose=purpose, data_usage=data_usage, data_publication=data_publication,
          data_deletion=data_deletion, questionnaire=questionnaire))
    study = session.query(Studies).filter_by(name=name).first()

    for channel in CHANNELS:
        session.add(
            Channel(study_id=study.id, name=channel, url=study.url + "?channel=" + channel, count=0)
        )

    session.commit()
    session.close()

    return True


def add_data_type(name, personal):
    session = create_session()
    try:
        data_id = session.query(Consent).filter_by(name=name).first().id
        session.commit()
        session.close()
        return False

    except AttributeError:
        # Set user credentials 
        session.add(Consent(name=name, personal=personal))
        session.commit()
        session.close()

    return True


def link_user_study(user_id, study_id):
    session = create_session()
    session.add(UserStudyMap(user_id=user_id, study_id=study_id))
    session.commit()
    session.close()


def add_consent(study_id, data_list):
    session = create_session()
    for data_id in data_list:
        session.add(ConsentStudyMap(consent_id=data_id, study_id=study_id))
    session.commit()
    session.close()


def get_conductor_data(study_id):
    session = create_session()
    user_id = session.query(UserStudyMap).filter_by(study_id=study_id).first().user_id
    user_data = session.query(Users).filter_by(id=user_id).first()
    uname = user_data.name
    umail = user_data.email
    uaddress = user_data.address
    session.commit()
    session.close()
    return {"name": uname, "email": umail, "address": uaddress}


##################################################################
#		WEBEND
##################################################################

# Starting page for the exercise generator
@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index(name=None):
    return render_template('study_index.html', name=name, data={})


@app.route('/study')
def study(name=None):
    user_studies = get_studies()
    return render_template('study_task.html', name=name, data={'tasks': user_studies})


@app.route('/help')
def help(name=None):
    return render_template('study_help.html', name=name, data={})


@app.route('/informed_consent', methods=['POST', 'GET'])
def informed_consent(name=None):
    sid = int(request.form['study'])
    fsession['study_id'] = sid
    userdata = get_conductor_data(sid)
    sdata = get_study_data(sid)
    return render_template('study_conductor.html', name=name, data={'userdata': userdata, 'purpose': sdata['purpose']})


@app.route('/consent_data')
def consent_data(name=None):
    sdata = get_study_data(fsession['study_id'])
    data = get_consent_data(fsession['study_id'])
    if len(data["personal"]) < 1:
        data["personal"] = ["No personal data will be collected in this study."]
    if len(data["public"]) < 1:
        data["public"] = ["No non-personal data will be collected in this study."]

    data["questionnaire"] = {"usage": False, "description": ""}
    if sdata['questionnaire'].strip() != "":
        data["questionnaire"]["usage"] = True
        data["questionnaire"]["description"] = sdata['questionnaire'].strip()
    return render_template('study_consent_data.html', name=name, data=data)


@app.route('/consent_usage')
def consent_usage(name=None):
    sdata = get_study_data(fsession['study_id'])
    return render_template('study_consent_usage.html', name=name, data=sdata)


@app.route('/agree')
def give_consent(name=None):
    try:
        channel = request.args['channel']
    except KeyError:
        channel = "other"  # in case no answer is provided
    link = get_link_data(fsession['study_id'], channel)
    return redirect(link)


@app.route('/disagree')
def reject_consent(name=None):
    flash('Thank you for considering participating in the study.')
    return index()


@app.route('/consent_all', methods=['POST', 'GET'])
def consent_all(name=None):
    sid = int(request.form['study'])
    fsession['study_id'] = sid
    userdata = get_conductor_data(sid)
    sdata = get_study_data(sid)
    data = get_consent_data(fsession['study_id'])
    if len(data["personal"]) < 1:
        data["personal"] = ["No personal data will be collected in this study."]
    if len(data["public"]) < 1:
        data["public"] = ["No non-personal data will be collected in this study."]

    data["questionnaire"] = {"usage": False, "description": ""}
    if sdata['questionnaire'].strip() != "":
        data["questionnaire"]["usage"] = True
        data["questionnaire"]["description"] = sdata['questionnaire'].strip()
    for k, v in sdata.items():
        data[k] = v
    data['userdata'] = userdata
    data['purpose'] = sdata['purpose']
    data['url'] = sdata['url']
    return render_template('study_consent_all.html', name=name, data=data)


@app.route('/register')
def registrate(name=None):
    return render_template('study_registrate.html', name=name, data={})


# Add a new user
@app.route('/create_user', methods=['POST'])
def create_user(name=None):
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    address = request.form['address']
    email = request.form['email']
    if not add_user(username, password, email, name, address):
        flash('Username {} is already taken. Please select a different one!'.format(username))
        return registrate()
    else:
        flash('Registrated user {}. Thank you for registering!'.format(username))
        fsession['logged_in'] = True
        fsession['user_id'] = get_user_id(username)
        return index()


@app.route('/create_task')
def create_study(name=None):
    # fetch personal information
    personal_data = get_personal_data()
    # fetch public information
    public_data = get_public_data()
    return render_template('study_create.html', name=name, data={'personal': personal_data, 'public': public_data})


# Add new data fields
@app.route('/add_data', methods=['POST'])
def add_data(name=None):
    dname = request.form['data_name']
    personal = int(request.form['personal'])
    if not add_data_type(dname, personal):
        flash('{} already exists'.format(dname))
        return create_study()
    else:
        flash('Added {}.'.format(dname))
        return create_study()


# Add a new task
@app.route('/create_task', methods=['POST'])
def create_task(name=None):
    personal = request.form.getlist('personal')
    public = request.form.getlist('public')
    sname = request.form['study_name']
    surl = request.form['study_url']
    spurpose = request.form['study_purpose']
    susage = request.form['usage']
    spublication = request.form['publication']
    sdeletion = request.form['deletion']
    squestionnaire = request.form['questionnaire']
    if not get_study_id(sname):
        add_study(sname, surl, spurpose, susage, spublication, sdeletion, squestionnaire)
        sid = get_study_id(sname)
        link_user_study(fsession['user_id'], sid)
        consent_links = [int(x) for x in personal] + [int(x) for x in public]
        add_consent(sid, consent_links)
        flash('Created task {}.'.format(sname))
        return index()
    else:
        flash('Taskname {} is already taken. Please select a different one!'.format(sname))
        return create_study()


# Login 
@app.route('/login', methods=['POST', 'GET'])
def login(name=None):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user_credentials(username, password):
            fsession['logged_in'] = True
            fsession['user_id'] = get_user_id(username)
            return render_template('study_index.html', name=name, data={})
        else:
            flash('Non existing user or wrong password.')

        return index()

    else:
        return render_template('study_login.html')


# Logout
@app.route('/logout', methods=['POST', 'GET'])
def logout(name=None):
    fsession['logged_in'] = False
    return index()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
