from app import db


class Person(db.Model):
    __tablename__ = "Person"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    surname = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    second_name = db.Column(db.String, nullable=True)
    contact = db.Column(db.String, nullable=True)
    photo_filename = db.Column(db.String, nullable=True)
    status = db.relationship('StatusPerson', backref='Person', lazy=True)
    stage = db.relationship('Stages', backref='Person', lazy=True)
    current = db.relationship('CurrentAddresses', backref='Person', lazy=True)
    expeditions = db.relationship(
        'ExpeditionsParticipation',
        backref='Person',
        lazy=True)
    userprojects = db.relationship('UserProjects', backref='Person', lazy=True)
    links = db.relationship('CrowdSourceLinks', backref='Person', lazy=True)
    stories = db.relationship(
        'CrowdSourceStories',
        backref='Person',
        lazy=True)
    emotional = db.relationship('EmotionalSchl', backref='Person', lazy=True)
    # institution = db.relationship(
    #     'PersonInstitution',
    #     backref='Person',
    #     lazy=True)
#    event_role = db.relationship('PersonEvent', backref='Person', lazy=True)


class StatusList(db.Model):
    __tablename__ = "StatusList"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String, nullable=False)
    sp = db.relationship('StatusPerson', backref='StatusList', lazy=True)


class StatusPerson(db.Model):
    __tablename__ = "StatusPerson"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stat_id = db.Column(
        db.Integer,
        db.ForeignKey("StatusList.id"),
        nullable=False)
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"), nullable=False)
    year_start = db.Column(db.Integer, nullable=True)
    year_fin = db.Column(db.Integer, nullable=True)
    program = db.Column(db.String, nullable=True)
    curator = db.Column(db.String, nullable=True)


class Stages(db.Model):
    __tablename__ = "Stages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    stage = db.Column(db.String, nullable=True)


class CurrentAddresses(db.Model):
    __tablename__ = "CurrentAddresses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"), nullable=False)
    address = db.Column(db.String, nullable=True)
    position = db.Column(db.String, nullable=True)


class ExpeditionsParticipation(db.Model):
    __tablename__ = "ExpeditionsParticipation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    expeditions = db.Column(db.String, nullable=True)


class UserProjects(db.Model):
    __tablename__ = "UserProjects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"), nullable=False)
    project_info = db.Column(db.String, nullable=True)


class CrowdSourceLinks(db.Model):
    __tablename__ = "CrowdSourceLinks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"), nullable=False)
    contact = db.Column(db.String, nullable=True)
    link = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)


class CrowdSourceStories(db.Model):
    __tablename__ = "CrowdSourceStories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"), nullable=False)
    contact = db.Column(db.String, nullable=True)
    story = db.Column(db.String, nullable=True)


class EmotionalSchl(db.Model):
    __tablename__ = "EmotionalSchl"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"), nullable=False)
    content = db.Column(db.String, nullable=True)


# class InstitutionType(db.Model):  # презабить
#     __tablename__ = "InstitutionType"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     institutions = db.relationship(
#         'Institutions', backref='StatusList', lazy=True)


# class Institutions(db.Model):
#     __tablename__ = "Institutions"
#     id = db.Column(db.Integer, primary_key=True)
#     type_id = db.Column(db.Integer, db.ForeignKey("InstitutionType.id"))
#     name = db.Column(db.String)
#     description = db.Column(db.String)
#     year_start = db.Column(db.Integer)
#     year_fin = db.Column(db.Integer)
#     # person_link = db.relationship(
#     #     'PersonInstitution',
#     #     backref='Institutions',
#     #     lazy=True)
#     event_role = db.relationship(
#         'InstitutionEvent',
#         backref='Institutions',
#         lazy=True)


# class PersonInstitution(db.Model):
#     __tablename__ = "PersonInstitution"
#     id = db.Column(db.Integer, primary_key=True)
#     pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
#     inst_id = db.Column(db.Integer, db.ForeignKey("Institutions.id"))
#     year_start = db.Column(db.Integer)
#     year_fin = db.Column(db.Integer)
#     position = db.Column(db.String)


# class EventType(db.Model):  # презабить
#     __tablename__ = "EventType"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     description = db.Column(db.String)
#     event = db.relationship('Event', backref='EventType', lazy=True)


# class Event(db.Model):
#     __tablename__ = "Event"
#     id = db.Column(db.Integer, primary_key=True)
#     type_id = db.Column(db.Integer, db.ForeignKey("EventType.id"))
#     name = db.Column(db.String)
#     description = db.Column(db.String)
#     year_start = db.Column(db.Integer)
#     year_fin = db.Column(db.Integer)
#     event_person_role = db.relationship(
#         'PersonEvent', backref='Event', lazy=True)
#     event_inst_role = db.relationship(
#         'InstitutionEvent', backref='Event', lazy=True)


# class PersonInEvent(db.Model):
#     __tablename__ = "PersonInEvent"
#     id = db.Column(db.Integer, primary_key=True)
#     role = db.Column(db.String)
#     person_in_event = db.relationship(
#         'PersonEvent', backref='PersonInEvent', lazy=True)


# class InstitutionInEvent(db.Model):
#     __tablename__ = "InstitutionInEvent"
#     id = db.Column(db.Integer, primary_key=True)
#     role = db.Column(db.String)
#     inst_in_event = db.relationship(
#         'InstitutionEvent',
#         backref='InstitutionInEvent',
#         lazy=True)


# class PersonEvent(db.Model):
#     __tablename__ = "PersonEvent"
#     id = db.Column(db.Integer, primary_key=True)
#     pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
#     ev_id = db.Column(db.Integer, db.ForeignKey("Event.id"))
#     role_id = db.Column(db.Integer, db.ForeignKey("PersonInEvent.id"))


# class InstitutionEvent(db.Model):
#     __tablename__ = "InstitutionEvent"
#     id = db.Column(db.Integer, primary_key=True)
#     inst_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
#     ev_id = db.Column(db.Integer, db.ForeignKey("Event.id"))
#     role_id = db.Column(db.Integer, db.ForeignKey("InstitutionInEvent.id"))


# class DocumentFormat(db.Model):
#     __tablename__ = "DocumentFormat"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     documents = db.relationship(
#         'Document',
#         backref='DocumentFormat',
#         lazy=True)


# class DocumentType(db.Model):
#     __tablename__ = "DocumentType"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     description = db.Column(db.String)
#     documents = db.relationship('Document', backref='DocumentType', lazy=True)


# class Document(db.Model):
#     __tablename__ = "Document"
#     id = db.Column(db.Integer, primary_key=True)
#     format_id = db.Column(db.Integer, db.ForeignKey("DocumentFormat.id"))
#     type_id = db.Column(db.Integer, db.ForeignKey("DocumentType.id"))
#     name = db.Column(db.String)
#     description = db.Column(db.String)
#     link = db.Column(db.String)


# class PersonDocument(db.Model):
#     __tablename__ = "PersonDocument"
#     id = db.Column(db.Integer, primary_key=True)
#     pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
#     doc_id = db.Column(db.Integer, db.ForeignKey("Document.id"))
#     role = db.Column(db.String)


# class InstitutionDocument(db.Model):
#     __tablename__ = "InstitutionDocument"
#     id = db.Column(db.Integer, primary_key=True)
#     pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
#     doc_id = db.Column(db.Integer, db.ForeignKey("Document.id"))
#     role = db.Column(db.String)


# class EventDocument(db.Model):
#     __tablename__ = "EventDocument"
#     id = db.Column(db.Integer, primary_key=True)
#     ev_id = db.Column(db.Integer, db.ForeignKey("Event.id"))
#     doc_id = db.Column(db.Integer, db.ForeignKey("Document.id"))
#     role = db.Column(db.String)


# class Place(db.Model):
#     __tablename__ = "Place"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     description = db.Column(db.String)
#     geolocation = db.Column(db.Integer)
#     id_parent = db.Column(db.Integer, db.ForeignKey("Place.id"))
#     date = db.Column(db.Integer)


# class PlaceDocument(db.Model):
#     __tablename__ = "PlaceDocument"
#     id = db.Column(db.Integer, primary_key=True)
#     place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
#     doc_id = db.Column(db.Integer, db.ForeignKey("Document.id"))
#     name = db.Column(db.String)
#     description = db.Column(db.String)
#     date = db.Column(db.Integer)


# class PlaceInstitution(db.Model):
#     __tablename__ = "PlaceInstitution"
#     id = db.Column(db.Integer, primary_key=True)
#     place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
#     inst_id = db.Column(db.Integer, db.ForeignKey("Institutions.id"))
#     name = db.Column(db.String)
#     description = db.Column(db.String)
#     date = db.Column(db.Integer)


# class PlacePerson(db.Model):
#     __tablename__ = "PlacePerson"
#     id = db.Column(db.Integer, primary_key=True)
#     place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
#     pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
#     name = db.Column(db.String)
#     description = db.Column(db.String)
#     date = db.Column(db.Integer)


# class PlaceEvent(db.Model):
#     __tablename__ = "PlaceEvent"
#     id = db.Column(db.Integer, primary_key=True)
#     place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
#     ev_id = db.Column(db.Integer, db.ForeignKey("Event.id"))
#     name = db.Column(db.String)
#     description = db.Column(db.String)
#     date = db.Column(db.Integer)


# class PlaceArtifact(db.Model):
#     __tablename__ = "PlaceArtifact"
#     id = db.Column(db.Integer, primary_key=True)
#     place_id = db.Column(db.Integer, db.ForeignKey("Place.id"))
#     art_id = db.Column(db.Integer, db.ForeignKey("Artifact.id"))
#     name = db.Column(db.String)
#     description = db.Column(db.String)
#     date = db.Column(db.Integer)


# class Artifact(db.Model):
#     __tablename__ = "Artifact"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     description = db.Column(db.String)
#     date = db.Column(db.Integer)


# class ArtifactInstitution(db.Model):
#     __tablename__ = "ArtifactInstitution"
#     id = db.Column(db.Integer, primary_key=True)
#     art_id = db.Column(db.Integer, db.ForeignKey("Artifact.id"))
#     inst_id = db.Column(db.Integer, db.ForeignKey("Institutions.id"))
#     name = db.Column(db.String)
#     description = db.Column(db.String)


# class ArtifactPerson(db.Model):
#     __tablename__ = "ArtifactPerson"
#     id = db.Column(db.Integer, primary_key=True)
#     art_id = db.Column(db.Integer, db.ForeignKey("Artifact.id"))
#     pers_id = db.Column(db.Integer, db.ForeignKey("Person.id"))
#     name = db.Column(db.String)
#     description = db.Column(db.String)


# class ArtifactEvent(db.Model):
#     __tablename__ = "ArtifactEvent"
#     id = db.Column(db.Integer, primary_key=True)
#     art_id = db.Column(db.Integer, db.ForeignKey("Artifact.id"))
#     ev_id = db.Column(db.Integer, db.ForeignKey("Event.id"))
#     name = db.Column(db.String)
#     description = db.Column(db.String)


# class ArtifactDocument(db.Model):
#     __tablename__ = "ArtifactDocument"
#     id = db.Column(db.Integer, primary_key=True)
#     art_id = db.Column(db.Integer, db.ForeignKey("Artifact.id"))
#     doc_id = db.Column(db.Integer, db.ForeignKey("Document.id"))
#     name = db.Column(db.String)
#     description = db.Column(db.String)
