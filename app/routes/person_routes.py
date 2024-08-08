import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from app import db
from app.models.models import *


person_routes = Blueprint('person_routes', __name__)


@person_routes.route('/person/page_<string:page_id>')
def questionnaire(page_id):
    page_templates = {
        'personal_info': 'personal_info.html',
        'student': 'student.html',
        'bachelor': 'bachelor.html',
        'bachelor_data': 'bachelor_data.html',
        'master': 'master.html',
        'master_data': 'master_data.html',
        'phd': 'phd.html',
        'phd_data': 'phd_data.html',
        'employee': 'employee.html',
        'teaching': 'teaching.html',
        'teaching_data': 'teaching_data.html',
        'management': 'management.html',
        'management_data': 'management_data.html',
        'research': 'research.html',
        'research_data': 'research_data.html',
        'connection': 'connection.html',
        'internships_check': 'internships_check.html',
        'internships': 'internships.html',
        'now': 'now.html',
        'expedition': 'expedition.html',
        'expedition_data': 'expedition_data.html',
        'important': 'important.html',
        'memories': 'memories.html',
        'memories_data': 'memories_data.html',
        'stories': 'stories.html',
        'stories_data': 'stories_data.html',
        'what_shl_is': 'what_shl_is.html',
        'thanks': 'thanks.html'
    }

    template = page_templates.get(page_id)

    if template:
        return render_template(template)


@person_routes.route('/person')
def person():
    return redirect(
        url_for(
            'person_routes.questionnaire',
            page_id='personal_info'))


@person_routes.route('/personal_info', methods=['POST'])
def get_personal_info():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing person if going back
        existing_person = Person.query.get(respondent_id)
        if existing_person:
            db.session.delete(existing_person)
            db.session.commit()

    surname = request.form.get('surname')
    name = request.form.get('name')
    second_name = request.form.get('second_name', '')
    contact = request.form.get('address')

    if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
        os.makedirs(current_app.config['UPLOAD_FOLDER'])

    photo = request.files.get('photo')
    photo_name = None
    initials = f'{surname} {name} {second_name}'

    if photo and photo.filename != '':
        photo_name = initials + os.path.splitext(photo.filename)[1]
        photo_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'], photo_name)

        try:
            photo.save(photo_path)
        except Exception as e:
            print(
                f"Ошибка при сохранении фотографии {photo.filename} у пользователя по имени {initials}: {e}")

    new_person = Person(
        surname=surname,
        name=name,
        second_name=second_name if second_name != '-' else None,
        contact=contact or None,
        photo_filename=photo_name or None)

    db.session.add(new_person)
    db.session.commit()
    session['respondent_id'] = new_person.id

    return redirect(url_for('person_routes.questionnaire', page_id='student'))


@person_routes.route('/student_status', methods=['POST'])
def student():
    session['connection_present'] = False
    if request.form.get('student_status') == 'Да':
        session['connection_present'] = True
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='bachelor'))
    elif request.form.get('student_status') == 'Нет':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='employee'))


@person_routes.route('/bachelor_status', methods=['POST'])
def bachelor():
    if request.form.get('bachelor_status') == 'Да':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='bachelor_data'))
    elif request.form.get('bachelor_status') == 'Нет':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='master'))


@person_routes.route('/master_status', methods=['POST'])
def master():
    if request.form.get('master_status') == 'Да':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='master_data'))
    elif request.form.get('master_status') == 'Нет':
        return redirect(url_for('person_routes.questionnaire', page_id='phd'))


@person_routes.route('/phd_status', methods=['POST'])
def phd():
    if request.form.get('phd_status') == 'Да':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='phd_data'))
    elif request.form.get('phd_status') == 'Нет':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='employee'))


@person_routes.route('/internship_status', methods=['POST'])
def internship():
    if request.form.get('internship_status') == 'Да':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='internships'))
    elif request.form.get('internship_status') == 'Нет':
        return redirect(url_for('person_routes.questionnaire', page_id='now'))


@person_routes.route('/bachelor_data', methods=['POST'])
def bachelor_data():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing bachelor data
        StatusPerson.query.filter_by(pers_id=respondent_id, stat_id=1).delete()
        db.session.commit()

    sections = [key.split('_')[3] for key in request.form.keys()
                if key.startswith('bach_start_year_')]

    for section in sections:
        year_start = request.form.get(f'bach_start_year_{section}')
        year_fin = request.form.get(f'bach_end_year_{section}')
        curator = request.form.get(f'bach_curator_{section}')

        new_bach = StatusPerson(
            pers_id=respondent_id,
            program='ФиКЛ',
            stat_id=1,
            year_start=year_start or None,
            year_fin=year_fin if year_fin and year_fin != '-' else None,
            curator=curator or None)
        db.session.add(new_bach)

    db.session.commit()
    return redirect(url_for('person_routes.questionnaire', page_id='master'))


@person_routes.route('/master_data', methods=['POST'])
def master_data():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing master data
        StatusPerson.query.filter_by(pers_id=respondent_id, stat_id=2).delete()
        db.session.commit()

    sections = [key.split('_')[2] for key in request.form.keys()
                if key.startswith('master_program_')]
    for section in sections:
        program = request.form.get(f'master_program_{section}')
        year_start = request.form.get(f'master_start_year_{section}')
        year_fin = request.form.get(f'master_end_year_{section}')
        curator = request.form.get(f'master_curator_{section}')

        new_master = StatusPerson(
            pers_id=respondent_id,
            program=program or None,
            stat_id=2,
            year_start=year_start or None,
            year_fin=year_fin if year_fin and year_fin != '-' else None,
            curator=curator or None)
        db.session.add(new_master)

    db.session.commit()
    return redirect(url_for('person_routes.questionnaire', page_id='phd'))


@person_routes.route('/phd_data', methods=['POST'])
def phd_data():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing phd data
        StatusPerson.query.filter_by(pers_id=respondent_id, stat_id=3).delete()
        db.session.commit()

    sections = [key.split('_')[3] for key in request.form.keys()
                if key.startswith('phd_start_year_')]
    for section in sections:
        # program = request.form.get(f'phd_program_{section}')
        year_start = request.form.get(f'phd_start_year_{section}')
        year_fin = request.form.get(f'phd_end_year_{section}')
        curator = request.form.get(f'phd_curator_{section}')

        new_phd = StatusPerson(
            pers_id=respondent_id,
            program='Аспирантская школа по филологическим наукам',
            stat_id=3,
            year_start=year_start or None,
            year_fin=year_fin if year_fin and year_fin != '-' else None,
            curator=curator or None)
        db.session.add(new_phd)

    db.session.commit()
    return redirect(url_for('person_routes.questionnaire', page_id='employee'))


@person_routes.route('/employee_status', methods=['POST'])
def employee():
    if request.form.get('employee_status') == 'Да':
        session['connection_present'] = True
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='teaching'))
    elif request.form.get('employee_status') == 'Нет' and not session['connection_present']:
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='connection'))
    else:
        return redirect(url_for('person_routes.questionnaire', page_id='now'))


@person_routes.route('/connection', methods=['POST'])
def connection():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing connection data
        Connections.query.filter_by(pers_id=respondent_id).delete()
        db.session.commit()

    connect = request.form.get('answer')
    new_status_person = Connections(pers_id=respondent_id,
                                    connection=connect or None)
    db.session.add(new_status_person)
    db.session.commit()
    return redirect(url_for('person_routes.questionnaire', page_id='now'))


@person_routes.route('/teaching_status', methods=['POST'])
def teaching():
    if request.form.get('teaching_status') == 'Да':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='teaching_data'))
    elif request.form.get('teaching_status') == 'Нет':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='management'))


@person_routes.route('/management_status', methods=['POST'])
def management():
    if request.form.get('management_status') == 'Да':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='management_data'))
    elif request.form.get('management_status') == 'Нет':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='research'))


@person_routes.route('/research_status', methods=['POST'])
def research():
    if request.form.get('research_status') == 'Да':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='research_data'))
    elif request.form.get('research_status') == 'Нет':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='internships_check'))


@person_routes.route('/teaching_data', methods=['POST'])
def teaching_data():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing teaching data
        StatusPerson.query.filter_by(pers_id=respondent_id, stat_id=4).delete()
        db.session.commit()

    programs_list = request.form.getlist('courses')
    year_start = request.form.get('teaching_start_year')
    year_fin = request.form.get('teaching_end_year')
    for program in programs_list:
        new_teacher = StatusPerson(
            pers_id=respondent_id,
            program=program or None,
            stat_id=4,
            year_start=year_start or None,
            year_fin=year_fin if year_fin and year_fin != '-' else None)
        db.session.add(new_teacher)
    db.session.commit()
    return redirect(
        url_for(
            'person_routes.questionnaire',
            page_id='management'))


@person_routes.route('/management_data', methods=['POST'])
def management_data():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing management data
        StatusPerson.query.filter_by(pers_id=respondent_id, stat_id=5).delete()
        db.session.commit()

    institutions_list = request.form.getlist('institution')
    other_institution = request.form.get('other_institution', '')
    if 'Другое' in institutions_list:
        institutions_list.remove('Другое')
        institutions_list.append(other_institution)

    year_start = request.form.get('management_start_year')
    for institution in institutions_list:
        new_manager = StatusPerson(pers_id=respondent_id,
                                   program=institution,
                                   stat_id=5,
                                   year_start=year_start or None,
                                   year_fin=None)
        db.session.add(new_manager)

    db.session.commit()
    return redirect(url_for('person_routes.questionnaire', page_id='research'))


@person_routes.route('/research_data', methods=['POST'])
def research_data():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing research data
        StatusPerson.query.filter_by(pers_id=respondent_id, stat_id=6).delete()
        db.session.commit()

    research_groups = request.form.getlist('research_groups')
    year_start = request.form.get('research_start_year')
    for group in research_groups:
        new_laborant = StatusPerson(pers_id=respondent_id,
                                    program=group,
                                    stat_id=6,
                                    year_start=year_start or None,
                                    year_fin=None)
        db.session.add(new_laborant)
    db.session.commit()
    return redirect(
        url_for(
            'person_routes.questionnaire',
            page_id='internships_check'))


@person_routes.route('/internships', methods=['POST'])
def internships_data():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing internship data
        Stages.query.filter_by(pers_id=respondent_id).delete()
        db.session.commit()

    sections = [key.split('_')[2] for key in request.form.keys()
                if key.startswith('intern_place_')]
    for section in sections:
        stage_name = request.form.get(f'intern_place_{section}')
        stage_year = request.form.get(f'intern_year_{section}')

        new_stage = Stages(pers_id=respondent_id,
                           year=stage_year or None,
                           stage=stage_name or None)
        db.session.add(new_stage)

    db.session.commit()
    return redirect(url_for('person_routes.questionnaire', page_id='now'))


@person_routes.route('/now', methods=['POST'])
def now():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing current address data
        CurrentAddresses.query.filter_by(pers_id=respondent_id).delete()
        db.session.commit()

    current_city = request.form.get('current_city')
    current_workplace = request.form.get('current_workplace')
    new_current = CurrentAddresses(pers_id=respondent_id,
                                   address=current_city or None,
                                   position=current_workplace or None)
    db.session.add(new_current)
    db.session.commit()
    return redirect(
        url_for(
            'person_routes.questionnaire',
            page_id='expedition'))


@person_routes.route('/expedition_status', methods=['POST'])
def expedition():
    if request.form.get('expedition_status') == 'Да':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='expedition_data'))
    elif request.form.get('expedition_status') == 'Нет':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='important'))


@person_routes.route('/expedition_data', methods=['POST'])
def expedition_data():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing expedition data
        ExpeditionsParticipation.query.filter_by(
            pers_id=respondent_id).delete()
        db.session.commit()

    form_data = request.form
    sections = [key.split('_')[1]
                for key in form_data.keys() if key.startswith('year_')]

    for section in sections:
        selected_year = form_data.get(f'year_{section}')
        if selected_year:
            expeditions = form_data.getlist(f'expeditions_{section}[]')
            other_expedition = form_data.get(
                f'other_exp_{section}', '').strip()

            if 'Другое' in expeditions:
                expeditions.remove('Другое')
                if other_expedition:
                    expeditions.append(other_expedition)

            for exp in expeditions:
                new_exp = ExpeditionsParticipation(
                    pers_id=respondent_id,
                    year=int(selected_year),
                    expedition=exp
                )
                db.session.add(new_exp)

    db.session.commit()
    return redirect(
        url_for(
            'person_routes.questionnaire',
            page_id='important'))


@person_routes.route('/important_data', methods=['POST'])
def important():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing important project data
        UserProjects.query.filter_by(pers_id=respondent_id).delete()
        db.session.commit()

    sections = [key.split('_')[1] for key in request.form.keys()
                if key.startswith('project_')]
    for section in sections:
        project_desc = request.form.get(f'project_{section}')
        new_project = UserProjects(pers_id=respondent_id,
                                   project_info=project_desc or None)
        db.session.add(new_project)
        db.session.commit()
    return redirect(url_for('person_routes.questionnaire', page_id='memories'))


@person_routes.route('/memories_status', methods=['POST'])
def memories():
    if request.form.get('memories_status') == 'Да':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='memories_data'))
    elif request.form.get('memories_status') == 'Нет':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='stories'))


@person_routes.route('/memories_data', methods=['POST'])
def memories_data():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing memories data
        CrowdSourceLinks.query.filter_by(pers_id=respondent_id).delete()
        db.session.commit()

    response = request.form.get('response')
    current_address = db.session.query(
        Person.contact).filter_by(
            id=respondent_id).one()[0]

    if current_address:
        address = current_address
    else:
        address = None

    if response == 'Поделюсь сейчас':
        link = request.form.get('link')
        description = request.form.get('description')
        new_link = CrowdSourceLinks(pers_id=respondent_id,
                                    contact=address or None,
                                    link=link or None,
                                    description=description or None)
        db.session.add(new_link)
        db.session.commit()

    elif response == 'Свяжитесь со мной позже':
        contact_method = request.form.get('contact-method')
        link = 'to be added'
        description = 'to be added'

        if contact_method == 'Указать новый адрес':
            address = request.form.get('new_address')

        new_link = CrowdSourceLinks(pers_id=respondent_id,
                                    contact=address or None,
                                    link=link or None,
                                    description=description or None)
        db.session.add(new_link)
        db.session.commit()

    return redirect(url_for('person_routes.questionnaire', page_id='stories'))


@person_routes.route('/stories_status', methods=['POST'])
def stories():
    if request.form.get('stories_status') == 'Да':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='stories_data'))
    elif request.form.get('stories_status') == 'Нет':
        return redirect(
            url_for(
                'person_routes.questionnaire',
                page_id='what_shl_is'))


@person_routes.route('/stories_data', methods=['POST'])
def stories_data():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing stories data
        CrowdSourceStories.query.filter_by(pers_id=respondent_id).delete()
        db.session.commit()

    response = request.form.get('response')
    current_address = db.session.query(
        Person.contact).filter_by(
            id=respondent_id).one()[0]

    if current_address:
        address = current_address
    else:
        address = None

    if response == 'Поделюсь сейчас':
        story = request.form.get('story')
        new_story = CrowdSourceStories(pers_id=respondent_id,
                                       contact=address or None,
                                       story=story or None)
        db.session.add(new_story)
        db.session.commit()
    elif response == 'Свяжитесь со мной позже':
        contact_method = request.form.get('contact-method')
        story = 'to be added'

        if contact_method == 'Указать новый адрес':
            address = request.form.get('new_address')

        new_story = CrowdSourceStories(pers_id=respondent_id,
                                       contact=address or None,
                                       story=story or None)
        db.session.add(new_story)
        db.session.commit()

    return redirect(
        url_for(
            'person_routes.questionnaire',
            page_id='what_shl_is'))


@person_routes.route('/what_shl_is', methods=['POST'])
def what_shl_is():
    respondent_id = session.get('respondent_id')
    if respondent_id:
        # Delete existing emotional data
        EmotionalSchl.query.filter_by(pers_id=respondent_id).delete()
        db.session.commit()

    answer = request.form.get('answer')
    new_emotion = EmotionalSchl(pers_id=respondent_id,
                                content=answer or None)
    db.session.add(new_emotion)
    db.session.commit()
    return redirect(url_for('person_routes.questionnaire', page_id='thanks'))
