from flask import Blueprint, render_template, redirect, url_for, request, session
from app.models.models import *

emotion_routes = Blueprint('emotion_routes', __name__)


@emotion_routes.route('/emotion/page_<string:page_id>')
def questionnaire(page_id):
    page_templates = {
        'personal_data': 'personal_data.html',
        'emotion_data_1': 'emotion_data_1.html',
        'emotion_data_2': 'emotion_data_2.html',
        'emotion_data_3': 'emotion_data_3.html',
        'emotion_data_4': 'emotion_data_4.html',
        'thanks': 'thanks.html'
    }
    template = page_templates.get(page_id)

    if template:
        return render_template(template)


@emotion_routes.route('/emotion')
def emotion():
    return redirect(url_for('emotion_routes.questionnaire',
                            page_id='personal_data'))


@emotion_routes.route('/emotion_personal_data', methods=['POST'])
def emotion_personal_data():
    respondent_id = session.get('respondent_id')
    surname = request.form.get('surname')
    name = request.form.get('name')
    second_name = request.form.get('second_name')
    if respondent_id:
        # Delete existing person if going back
        existing_entry = Emotions_main.query.get(respondent_id)
        if existing_entry:
            if surname != '':
                existing_entry.surname = surname
            if name != '':
                existing_entry.name = name
            if second_name != '':
                existing_entry.sec_name = second_name
            db.session.commit()

    else:
        person_entry = Emotions_main(surname=surname,
                                     name=name,
                                     sec_name=second_name)
        db.session.add(person_entry)
        db.session.commit()
        session['respondent_id'] = person_entry.id
    return redirect(url_for('emotion_routes.questionnaire',
                            page_id='emotion_data_1'))


@emotion_routes.route('/emotion_data_1', methods=['POST'])
def emotion_data_1():
    respondent_id = session.get('respondent_id')
    memories_education = request.form.get('memories-education')
    memories_life = request.form.get('memories-life')
    memories_people = request.form.get('memories-people')
    significant_spaces = request.form.get('significant-spaces')
    if respondent_id:
        add_user = Emotions_main.query.filter_by(id=respondent_id).first()
        if memories_education != '':
            add_user.studies = memories_education
        if memories_life != '':
            add_user.not_studies = memories_life
        if memories_people != '':
            add_user.people = memories_people
        if significant_spaces != '':
            add_user.spaces = significant_spaces
        db.session.commit()
    else:
        info_entry = Emotions_main(studies=memories_education,
                                   not_studies=memories_life,
                                   people=memories_people,
                                   spaces=significant_spaces)
        db.session.add(info_entry)
        db.session.commit()
        session['respondent_id'] = info_entry.id
    return redirect(url_for('emotion_routes.questionnaire', page_id='emotion_data_2'))


@emotion_routes.route('/emotion_data_2', methods=['POST'])
def emotion_data_2():
    respondent_id = session.get('respondent_id')
    unusual_experience = request.form.get('unusual-experience')
    if respondent_id:
        add_user = Emotions_main.query.filter_by(id=respondent_id).first()
        if unusual_experience != '':
            add_user.exp = unusual_experience
        db.session.commit()
    else:
        info_entry = Emotions_main(exp=unusual_experience)
        db.session.add(info_entry)
        db.session.commit()
        session['respondent_id'] = info_entry.id
    return redirect(url_for('emotion_routes.questionnaire', page_id='emotion_data_3'))


@emotion_routes.route('/emotion_data_3', methods=['POST'])
def emotion_data_3():
    respondent_id = session.get('respondent_id')
    noun = request.form.get('noun')
    verb = request.form.get('verb')
    pronoun = request.form.get('pronoun')
    school_definition = request.form.get('school-definition')
    if respondent_id:
        add_user = Emotions_main.query.filter_by(id=respondent_id).first()
        if noun != '':
            add_user.words_noun = noun
        if verb != '':
            add_user.words_verb = verb
        if pronoun != '':
            add_user.words_pron = pronoun
        if school_definition != '':
            add_user.this = school_definition
        db.session.commit()
    else:
        info_entry = Emotions_main(words_noun = noun,
                                   words_verb = verb,
                                   words_pron = pronoun,
                                   this = school_definition)
        db.session.add(info_entry)
        db.session.commit()
        session['respondent_id'] = info_entry.id
    return redirect(url_for('emotion_routes.questionnaire', page_id='emotion_data_4'))


@emotion_routes.route('/emotion_data_4', methods=['POST'])
def emotion_data_4():
    respondent_id = session.get('respondent_id')
    greetings = request.form.get('greetings')
    if respondent_id:
        add_user = Emotions_main.query.filter_by(id=respondent_id).first()
        if greetings != '':
            add_user.hello = greetings
        db.session.commit()
    else:
        info_entry = Emotions_main(hello=greetings)
        db.session.add(info_entry)
        db.session.commit()
        session['respondent_id'] = info_entry.id
    return redirect(url_for('emotion_routes.questionnaire', page_id='thanks'))
