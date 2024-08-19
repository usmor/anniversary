from flask import Blueprint, render_template, redirect, url_for, request, session
from app.models.models import *
from sqlalchemy import inspect


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
    respondent_id = session.get('emotion_respondent_id')
    surname = request.form.get('surname') or None
    name = request.form.get('name') or None
    second_name = request.form.get('second_name')
    second_name = None if second_name in ['-', ''] else second_name

    existing_entry = Emotions_main.query.get(
        respondent_id) if respondent_id else None

    if existing_entry:
        existing_entry.surname = surname
        existing_entry.name = name
        existing_entry.sec_name = second_name
        db.session.commit()
    else:
        person_entry = Emotions_main(surname=surname,
                                     name=name,
                                     sec_name=second_name)
        db.session.add(person_entry)
        db.session.commit()
        session['emotion_respondent_id'] = person_entry.id

    return redirect(url_for('emotion_routes.questionnaire',
                            page_id='emotion_data_1'))


@emotion_routes.route('/emotion_data_1', methods=['POST'])
def emotion_data_1():
    respondent_id = session.get('emotion_respondent_id')
    memories_education = request.form.get('memories-education') or None
    memories_life = request.form.get('memories-life') or None
    memories_people = request.form.get('memories-people') or None
    significant_spaces = request.form.get('significant-spaces') or None

    add_user = Emotions_main.query.get(respondent_id)

    if add_user:
        add_user.studies = memories_education
        add_user.not_studies = memories_life
        add_user.people = memories_people
        add_user.spaces = significant_spaces
    else:
        add_user = Emotions_main(id=respondent_id,
                                 studies=memories_education,
                                 not_studies=memories_life,
                                 people=memories_people,
                                 spaces=significant_spaces)
        db.session.add(add_user)

    db.session.commit()
    return redirect(
        url_for(
            'emotion_routes.questionnaire',
            page_id='emotion_data_2'))


@emotion_routes.route('/emotion_data_2', methods=['POST'])
def emotion_data_2():
    respondent_id = session.get('emotion_respondent_id')
    unusual_experience = request.form.get('unusual-experience') or None

    add_user = Emotions_main.query.get(respondent_id)

    if add_user:
        add_user.exp = unusual_experience
    else:
        add_user = Emotions_main(id=respondent_id, exp=unusual_experience)
        db.session.add(add_user)

    db.session.commit()
    return redirect(
        url_for(
            'emotion_routes.questionnaire',
            page_id='emotion_data_3'))


@emotion_routes.route('/emotion_data_3', methods=['POST'])
def emotion_data_3():
    respondent_id = session.get('emotion_respondent_id')
    noun = request.form.get('noun') or None
    verb = request.form.get('verb') or None
    pronoun = request.form.get('pronoun') or None
    school_definition = request.form.get('school-definition') or None

    add_user = Emotions_main.query.get(respondent_id)

    if add_user:
        add_user.words_noun = noun
        add_user.words_verb = verb
        add_user.words_pron = pronoun
        add_user.this = school_definition
    else:
        add_user = Emotions_main(id=respondent_id,
                                 words_noun=noun,
                                 words_verb=verb,
                                 words_pron=pronoun,
                                 this=school_definition)
        db.session.add(add_user)

    db.session.commit()
    return redirect(
        url_for(
            'emotion_routes.questionnaire',
            page_id='emotion_data_4'))


@emotion_routes.route('/emotion_data_4', methods=['POST'])
def emotion_data_4():
    respondent_id = session.get('emotion_respondent_id')
    greetings = request.form.get('greetings') or None

    add_user = Emotions_main.query.get(respondent_id)

    if add_user:
        add_user.hello = greetings
    else:
        add_user = Emotions_main(id=respondent_id, hello=greetings)
        db.session.add(add_user)

    db.session.commit()

    # Check if all fields are empty and delete the record if so
    add_user = Emotions_main.query.get(respondent_id)
    if add_user:
        mapper = inspect(Emotions_main)
        if all(getattr(add_user, column.key) is None
           for column in mapper.columns
           if column.key != 'id'):
            db.session.delete(add_user)
            db.session.commit()

    return redirect(url_for('emotion_routes.questionnaire', page_id='thanks'))
