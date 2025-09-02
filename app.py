import sqlite3
import os
from flask import Flask, render_template, request, flash, redirect, url_for, session, make_response
from models import *
from database import db, init_db
import logging
from datetime import datetime
from models.crypto_utils import encrypt_field, decrypt_field


app = Flask(__name__)
app.secret_key = 'your-secret-key'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            is_success = User.authenticate(username, password)
            if is_success[0]:
                user = is_success[1]
                session['user'] = user.id
                session['role'] = user.role
                return redirect(url_for('dashboard'))
            else:
               
                flash('Invalid username or password', 'danger')
                return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        name = request.form['name']
        nid = request.form['nid']
        date_of_birth = request.form['dob']
        print(date_of_birth)
        address = request.form['address']
        password = request.form['password']
        contact = request.form['phone']
        blood_type = request.form['bloodgroup']
        is_success = User.registerUser(username, email, name, nid, date_of_birth, address, password, contact, blood_type)
        if is_success[0]:
            flash(is_success[1], 'success')
            return redirect(url_for('login'))
        else:
            flash(is_success[1],'danger')
            return redirect(url_for('signup'))


@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        if session['role'] == 'volunteer':
            return redirect(url_for('volunteer'))
        user = User.getUser(session['user'])
        info = user.getInfo()
        return render_template('dash.html', user = user, info=info)
    return redirect(url_for('login'))


@app.route('/makedonation', methods=['GET', 'POST'])
def makeDonation():
    if session.get('user') is not None:
        if request.method == 'POST':
            donorid = session['user']
            method = request.form['method']
            amount = request.form['amount']
            date = datetime.now().strftime('%m-%d-%Y')
            tid = request.form['tid']
            Donation.add_donation(method, donorid, amount, date, tid)
            return redirect(url_for('dashboard'))
        return render_template('makedonation.html')
    return redirect(url_for('login'))


@app.route('/donateblood', methods = ["GET", "POST"])
def donateblood():
    if session.get('user') is None:
        return redirect(url_for('login'))
    id = session['user']
    result = User.donate_blood(id)
    return redirect(url_for('dashboard'))


@app.route('/bloodavailability', methods=['GET', 'POST'])
def bloodavailability():
    if request.method == 'GET':
        user = User.getAlluser()
        return render_template('bloodavailability.html', user=user)
    elif request.method == 'POST':
        bloodgroup = request.form['bloodgroup']
        location = request.form['location']
        is_success = User.filter_bloodbank(bloodgroup, location)
        return render_template('bloodavailability.html', user=is_success)


@app.route('/missingperson', methods=['GET', 'POST'])
def missingperson():
    if request.method == 'GET':
        return render_template('registermissing.html')
    elif request.method == 'POST':
        name = request.form['personName']
        last_seen = request.form['lastSeen']
        contact_number = request.form['contactNumber']
        photo = request.files['uploadPhoto'].read()

        mperson = MissingPerson(name, last_seen, contact_number, photo)
        is_success = mperson.registerMissing()

        if is_success:
            flash('Missing person report submitted successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Failed to submit the missing person report.', 'danger')
            return render_template('registermissing.html')


@app.route('/viewmissing', methods=['GET', 'POST'])
def viewmissing():
    missingpersons = MissingPerson.getMissingPersons()
    return render_template('showmissingpersons.html', missingpersons=missingpersons)

@app.route('/photo/<int:person_id>')
def serve_photo(person_id):
    person = MissingPerson.getMissingPersonByParam(id=person_id)
    photo_data = person.photo
    
    response = make_response(photo_data)
    response.headers.set('Content-Type', 'image/jpeg')
    return response




@app.route('/volunteer')
def volunteer():
    voln = Volunteer.getVolunteer(session['user'])
    user = User.getUser(session['user'])
    info = voln.getInfo()
    return render_template('vdash.html', voln=voln, info=info, user=user, decrypt_field=decrypt_field)


@app.route('/allocatedonation', methods=['GET', 'POST'])
def allocatedonation():
    if request.method == 'GET':
        return render_template('allocatedonation.html', available=Allocation.available_fund())
    elif request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']
        if Allocation.add_allocation(description, amount, date):
            flash('Allocation successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Not enough balance!', 'danger')
            return redirect(url_for('allocatedonation'))


@app.route('/update_disaster/<volunteer_id>', methods=['GET', 'POST'])
def update_disaster(volunteer_id):
    if request.method == 'POST':
        disaster_type = request.form['disaster_type']
        location = request.form['location']
        OngoingDisaster.addOrUpdateDisaster(volunteer_id, disaster_type, location)
        flash("Disaster updated successfully", 'success')
        return redirect(url_for('volunteer'))

    ongoing_disaster = OngoingDisaster.query.filter_by(volunteer_id=volunteer_id).first()
    return render_template('update_add_dis.html', volunteer_id=volunteer_id, ongoing_disaster=ongoing_disaster)

@app.route('/rcamp', methods=['GET', 'POST'])
def r_camp_info():
    if "role" in session:
        if session['role'] != 'volunteer':
            return redirect(url_for('login'))
    v_id = session['user']
    if Volunteer.getVolunteer(v_id) is None:
        return redirect(url_for('login'))
    if request.method == 'GET':
        rid = WorkAssigned.getCampID(v_id)
        if rid is None:
            return "You are not assigned to any Relief Camp"
        result = Rcamp.get_camp(rid)
        occupied = WorkAssigned.count_volunteers(result.id)
        return render_template('rcamp.html', rcamp=result, occupied=occupied)
    elif request.method == 'POST':
        v_cap = request.form['v_capacity']
        v_occ = request.form['v_occupied']
        id = request.form['id']
        result = Rcamp.query.filter_by(id = id).first()
        result.update_camp(v_cap, v_occ)
        return redirect(url_for('r_camp_info'))

@app.route('/emergency_directory', methods=['GET', 'POST'])
def emergency_directory():
    if 'role' in session:
        if session['role'] == 'volunteer':
            if request.method == 'POST':
                id = request.form['id']
                name = request.form['name']
                designation = request.form['designation']
                contact = request.form['contact']
                location = request.form['location']
                econtact = EmergencyDirectory.getContact(id)
                econtact.updateContact(name, designation, contact, location)
                return redirect(url_for('emergency_directory'))
            directory = EmergencyDirectory.query.all()
            return render_template('emergency_directory_voln.html', directory=directory)
    directory = EmergencyDirectory.query.all()
    return render_template('emergency_directory.html', directory=directory)


@app.route('/add_emergency_directory', methods=['POST'])
def add_emergency_directory():
    if 'role' in session:
        if session['role'] == 'volunteer':
            if request.method == 'POST':
                name = request.form['name']
                designation = request.form['designation']
                contact = request.form['contact']
                location = request.form['location']
                EmergencyDirectory.addEmergencyDirectory(name, designation, contact, location)
                return redirect(url_for('emergency_directory'))
    return redirect(url_for('login'))


@app.route('/add_volunteer', methods=['GET','POST'])
def add_volunteer():
    if 'role' in session:
        if session['role'] == 'volunteer':
            voln = Volunteer.getVolunteer(session['user'])
            if voln.role != 'coordinator':
                return "You do not have access to it!"
            if request.method == 'POST':
                id = request.form['id']
                stat = ApplyVolunteer.accept_application(id)
                flash(stat[0], stat[1])
                return redirect(url_for('volunteer'))
            requests = ApplyVolunteer.get_all_applicant()
            return render_template('add_volunteer.html', applicants=requests, user = User)
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

    
@app.route('/resources')
def resources_dashboard():
    resources = Resource.query.all()
    return render_template('resources.html', resources=resources)

@app.route('/add-resource', methods=['GET', 'POST'])
def add_resource():
    if request.method == 'POST':
        campID = request.form['campID']
        type = request.form['type']
        quantity = request.form['quantity']
        location = request.form['location']
        
        Resource.addResource(campID, type, quantity, location)
        flash("Resource added successfully!", "success")
        return redirect(url_for('resources_dashboard'))
    return render_template('add_resource.html')

@app.route('/update-resource/<int:resID>', methods=['POST'])
def update_resource(resID):
    if request.method == 'POST':
        quantity = request.form['quantity']
        Resource.updateResource(resID, quantity)
        flash("Resource updated successfully!", "success")
        return redirect(url_for('resources_dashboard'))

@app.route('/apply_volunteer', methods=['POST'])
def apply_volunteer():
    if request.method == 'POST':
        email = request.form['email']
        application = ApplyVolunteer(email)
        db.session.add(application)
        db.session.commit()
        flash("Application submitted successfully!", "success")
        return redirect(url_for('dashboard'))


@app.route('/updatevolunteer', methods=['GET', 'POST'])
def updatevolunteer():
    if 'role' in session:
        if session['role'] == 'volunteer':
            voln = Volunteer.getVolunteer(session['user'])
            if voln.role != 'coordinator':
                return "You do not have access to it!"
            if request.method == 'POST': 
                v_id = request.form['volunteer_id']
                r_id = request.form['camp_id']
                assigned = WorkAssigned.query.filter_by(volnID = v_id).first()
                if assigned:
                    assigned.rcamp_id = r_id
                    flash("Volunteer already assigned", "danger")
                elif v_id and r_id:
                    new_assignment = WorkAssigned(volnID=v_id, rcamp_id=r_id)
                    db.session.add(new_assignment)
                    db.session.commit()
                    flash("Volunteer assigned successfully", "success")
                else:
                    flash("Some Error", "danger")
                return redirect(url_for('updatevolunteer'))
            return render_template('volnlist.html', user = User, volunteers= Volunteer.getAllVolunteers(), camps = Rcamp.get_all_camps())
        
    return redirect(url_for('dashboard'))           

@app.route('/logout' , methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
