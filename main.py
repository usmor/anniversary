from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smoltest_3.db'
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = "Person"
    id = db.Column(db.Integer, primary_key=True)
    FIO = db.Column(db.String)
    status = db.relationship('StatusPerson', backref='Person', lazy=True)
    institution = db.relationship('PersonInstitution', backref='Person', lazy=True)
    event_role = db.relationship('PersonEvent', backref='Person', lazy=True)


class StatusList(db.Model):
    __tablename__ = "StatusList"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    sp = db.relationship('StatusPerson', backref='StatusList', lazy=True)


class StatusPerson(db.Model):
    __tablename__ = "StatusPerson"
    id = db.Column(db.Integer, primary_key=True)
    stat_id = db.Column(db.Integer, db.ForeignKey("StatusList.id"))
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
    year_start = db.Column(db.Integer)
    year_fin = db.Column(db.Integer)


class InstitutionType(db.Model): #презабить
    __tablename__ = "InstitutionType"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    institutions = db.relationship('Institutions', backref='StatusList', lazy=True)


class Institutions(db.Model):
    __tablename__ = "Institutions"
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey("InstitutionType.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    year_start = db.Column(db.Integer)
    year_fin = db.Column(db.Integer)
    person_link = db.relationship('PersonInstitution', backref='Institutions', lazy=True)
    event_role = db.relationship('InstitutionEvent', backref='Institutions', lazy=True)


class PersonInstitution(db.Model):
    __tablename__ = "PersonInstitution"
    id = db.Column(db.Integer, primary_key=True)
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
    inst_id = db.Column(db.Integer, db.ForeignKey("Institutions.id"))
    year_start = db.Column(db.Integer)
    year_fin = db.Column(db.Integer)
    position = db.Column(db.String)


class EventType(db.Model): #презабить
    __tablename__ = "EventType"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    event = db.relationship('Event', backref='EventType', lazy=True)


class Event(db.Model):
    __tablename__ = "Event"
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey("EventType.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    year_start = db.Column(db.Integer)
    year_fin = db.Column(db.Integer)
    event_person_role = db.relationship('PersonEvent', backref='Event', lazy=True)
    event_inst_role = db.relationship('InstitutionEvent', backref='Event', lazy=True)


class PersonInEvent(db.Model):
    __tablename__ = "PersonInEvent"
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)
    person_in_event = db.relationship('PersonEvent', backref='PersonInEvent', lazy=True)


class InstitutionInEvent(db.Model):
    __tablename__ = "InstitutionInEvent"
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)
    inst_in_event = db.relationship('InstitutionEvent', backref='InstitutionInEvent', lazy=True)


class PersonEvent(db.Model):
    __tablename__ = "PersonEvent"
    id = db.Column(db.Integer, primary_key=True)
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
    ev_id = db.Column(db.Integer, db.ForeignKey("Event.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("PersonInEvent.id"))


class InstitutionEvent(db.Model):
    __tablename__ = "InstitutionEvent"
    id = db.Column(db.Integer, primary_key=True)
    inst_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
    ev_id = db.Column(db.Integer, db.ForeignKey("Event.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("InstitutionInEvent.id"))


class DocumentFormat(db.Model):
    __tablename__ = "DocumentFormat"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    documents = db.relationship('Document', backref='DocumentFormat', lazy=True)


class DocumentType(db.Model):
    __tablename__ = "DocumentType"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    documents = db.relationship('Document', backref='DocumentType', lazy=True)


class Document(db.Model):
    __tablename__ = "Document"
    id = db.Column(db.Integer, primary_key=True)
    format_id = db.Column(db.Integer, db.ForeignKey("DocumentFormat.id"))
    type_id = db.Column(db.Integer, db.ForeignKey("DocumentType.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    link = db.Column(db.String)


class PersonDocument(db.Model): ##
    __tablename__ = "PersonDocument"
    id = db.Column(db.Integer, primary_key=True)
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
    doc_id = db.Column(db.Integer, db.ForeignKey("Document.id"))
    role = db.Column(db.String)


class InstitutionDocument(db.Model): ##
    __tablename__ = "InstitutionDocument"
    id = db.Column(db.Integer, primary_key=True)
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
    doc_id = db.Column(db.Integer, db.ForeignKey("Document.id"))
    role = db.Column(db.String)


class EventDocument(db.Model): ##
    __tablename__ = "EventDocument"
    id = db.Column(db.Integer, primary_key=True)
    ev_id = db.Column(db.Integer, db.ForeignKey("Event.id"))
    doc_id = db.Column(db.Integer, db.ForeignKey("Document.id"))
    role = db.Column(db.String)


class Place(db.Model):
    __tablename__ = "Place"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    geolocation = db.Column(db.Integer)
    id_parent = db.Column(db.Integer, db.ForeignKey("Place.id"))
    date = db.Column(db.Integer)


class PlaceDocument(db.Model):
    __tablename__ = "PlaceDocument"
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
    doc_id = db.Column(db.Integer, db.ForeignKey("Document.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.Integer)


class PlaceInstitution(db.Model):
    __tablename__ = "PlaceInstitution"
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
    inst_id = db.Column(db.Integer, db.ForeignKey("Institutions.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.Integer)


class PlacePerson(db.Model):
    __tablename__ = "PlacePerson"
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.Integer)


class PlaceEvent(db.Model):
    __tablename__ = "PlaceEvent"
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
    ev_id = db.Column(db.Integer, db.ForeignKey("Event.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.Integer)


class PlaceArtifact(db.Model):
    __tablename__ = "PlaceArtifact"
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
    art_id = db.Column(db.Integer, db.ForeignKey("Artifact.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.Integer)


class Artifact(db.Model):
    __tablename__ = "Artifact"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.Integer)


class ArtifactInstitution(db.Model):
    __tablename__ = "ArtifactInstitution"
    id = db.Column(db.Integer, primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey("Artifact.id"))
    inst_id = db.Column(db.Integer, db.ForeignKey("Institutions.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)


class ArtifactPerson(db.Model):
    __tablename__ = "ArtifactPerson"
    id = db.Column(db.Integer, primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey("Artifact.id"))
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)


class ArtifactEvent(db.Model):
    __tablename__ = "ArtifactEvent"
    id = db.Column(db.Integer, primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey("Artifact.id"))
    ev_id = db.Column(db.Integer, db.ForeignKey("Event.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)


class ArtifactDocument(db.Model):
    __tablename__ = "ArtifactDocument"
    id = db.Column(db.Integer, primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey("Artifact.id"))
    doc_id = db.Column(db.Integer, db.ForeignKey("Document.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)


with app.app_context():
    db.create_all()


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/form')
def form():
    return render_template('personal_info.html')


@app.route('/personal_info', methods=['POST'])
def get_personal_info():
    surname = request.form.get('surname')
    name = request.form.get('name')
    second_name = request.form.get('second_name')
    full_name = surname + ' ' + name + ' ' + second_name
    new_person = Person(FIO=full_name)
    db.session.add(new_person)
    db.session.commit()
    global current_person_id
    current_person_id = new_person.id
    return render_template('student.html')


@app.route('/student_status', methods=['POST'])
def student():
    if request.form.get('student_status') == 'Да':
        new_sp = StatusPerson(stat_id = 1, pers_id = current_person_id, year_start=2020, year_fin=2024)
        db.session.add(new_sp)
        db.session.commit()
        return render_template('student_data.html')
    elif request.form.get('student_status') == 'Нет':
        new_sp = StatusPerson(stat_id=0, pers_id=current_person_id, year_start=2020, year_fin=2024)
        db.session.add(new_sp)
        db.session.commit()
        return render_template('employee.html')


@app.route('/student_data', methods=['POST'])
def student_data():
    if request.form.get('bach_course') != '–':
        bach_course = request.form.get('bach_course')
        bach_start = request.form.get('bach_start')
        bach_end = request.form.get('bach_end')

    if request.form.get('mag_status') != '–':
        mag_course = request.form.get('mag_course')
        mag_start = request.form.get('mag_start')
        mag_end = request.form.get('mag_end')

    if request.form.get('asp_status') != '–':
        asp_course = request.form.get('asp_course')
        asp_start = request.form.get('asp_start')
        asp_end = request.form.get('asp_end')

    return render_template('employee.html')


@app.route('/employee_status', methods=['POST'])
def employee():
    if request.form.get('employee_status') == 'Да':
        return render_template('employee_data.html')
    elif request.form.get('employee_status') == 'Нет':
        return render_template('non_official_status.html')


@app.route('/employee_data', methods=['POST'])
def employee_data():
    teacher_status = request.form.get('teacher_status')
    teacher_start = request.form.get('teacher_start')
    teacher_end = request.form.get('teacher_end')

    authority_status = request.form.get('authority_status')
    authority_start = request.form.get('authority_start')
    authority_end = request.form.get('authority_end')

    laboratories = ['НУЛ по формальным моделям в лингвистике',
                    'НУЛ социогуманитарных исследований Севера и Арктики']
    labotaries_data = []
    for l in range(len(laboratories)):
        if request.form.get(f'position_in_{l + 1}') is not None:
            labotaries_data.append([laboratories[l],
                                    request.form.get(f'position_in_{l + 1}'),
                                    request.form.get(f'start_{l+1}'),
                                    request.form.get(f'end_{l+1}')])

    return render_template('non_official_status.html')

@app.route('/non_official_status', methods=['POST'])
def non_offical_status():
    # собираем какую-нибудь информацию
    return render_template('research_papers.html')

@app.route('/research_papers', methods=['POST'])
def research_papers():
    research_papers = []
    # сил понять, как собирать данные, нет
    return render_template('thanks.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.run(debug=False, port=5001)
