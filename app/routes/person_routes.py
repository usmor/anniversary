import os

from flask import Blueprint, render_template, request, current_app, session
from app import db
from app.models.models import *


person_routes = Blueprint('person_routes', __name__)


@person_routes.route('/person')
def person():
    return render_template('personal_info.html')


@person_routes.route('/personal_info', methods=['POST'])
def get_personal_info():
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
        photo_filename=photo_name)
    db.session.add(new_person)
    db.session.commit()
    session['respondent_id'] = new_person.id

    return render_template('student.html')


@person_routes.route('/student_status', methods=['POST'])
def student():
    if request.form.get('student_status') == 'Да':
        return render_template('bachelor.html')
    elif request.form.get('student_status') == 'Нет':
        return render_template('employee.html')


@person_routes.route('/bachelor_status', methods=['POST'])
def bachelor():
    if request.form.get('bachelor_status') == 'Да':
        return render_template('bachelor_data.html')
    elif request.form.get('bachelor_status') == 'Нет':
        return render_template('master.html')


@person_routes.route('/master_status', methods=['POST'])
def master():
    if request.form.get('master_status') == 'Да':
        return render_template('master_data.html')
    elif request.form.get('master_status') == 'Нет':
        return render_template('phd.html')


@person_routes.route('/phd_status', methods=['POST'])
def phd():
    if request.form.get('phd_status') == 'Да':
        return render_template('phd_data.html')
    elif request.form.get('phd_status') == 'Нет':
        return render_template('employee.html')


@person_routes.route('/bachelor_data', methods=['POST'])
def bachelor_data():
    respondent_id = session.get('respondent_id')
    sections = [key.split('_')[2] for key in request.form.keys()
                if key.startswith('bach_program_')]
    for section in sections:
        program = request.form.get(f'bach_program_{section}')
        year_start = request.form.get(f'bach_start_year_{section}')
        year_fin = request.form.get(f'bach_end_year_{section}')
        curator = request.form.get(f'bach_curator_{section}')

        new_bach = StatusPerson(pers_id=respondent_id,
                                program=program,
                                stat_id=1,
                                year_start=year_start or None,
                                year_fin=year_fin or None,
                                curator=curator or None)
        db.session.add(new_bach)

    db.session.commit()
    return render_template('master.html')


@person_routes.route('/master_data', methods=['POST'])
def master_data():
    respondent_id = session.get('respondent_id')
    sections = [key.split('_')[2] for key in request.form.keys()
                if key.startswith('master_program_')]
    for section in sections:
        program = request.form.get(f'master_program_{section}')
        year_start = request.form.get(f'master_start_year_{section}')
        year_fin = request.form.get(f'master_end_year_{section}')
        curator = request.form.get(f'master_curator_{section}')

        new_master = StatusPerson(pers_id=respondent_id,
                                  program=program,
                                  stat_id=2,
                                  year_start=year_start or None,
                                  year_fin=year_fin or None,
                                  curator=curator or None)
        db.session.add(new_master)

    db.session.commit()
    return render_template('phd.html')


@person_routes.route('/phd_data', methods=['POST'])
def phd_data():
    respondent_id = session.get('respondent_id')
    sections = [key.split('_')[2] for key in request.form.keys()
                if key.startswith('phd_program_')]
    for section in sections:
        program = request.form.get(f'phd_program_{section}')
        year_start = request.form.get(f'phd_start_year_{section}')
        year_fin = request.form.get(f'phd_end_year_{section}')
        curator = request.form.get(f'phd_curator_{section}')

        new_phd = StatusPerson(pers_id=respondent_id,
                               program=program,
                               stat_id=3,
                               year_start=year_start or None,
                               year_fin=year_fin or None,
                               curator=curator or None)
        db.session.add(new_phd)

    db.session.commit()
    return render_template('employee.html')


@person_routes.route('/employee_status', methods=['POST'])
def employee():
    if request.form.get('employee_status') == 'Да':
        return render_template('teaching.html')
    elif request.form.get('employee_status') == 'Нет':
        return render_template('connection.html')


@person_routes.route('/connection', methods=['POST'])
def connection():
    connect = request.form.get('connection')
    return render_template('now.html')


@person_routes.route('/teaching_status', methods=['POST'])
def teaching():
    if request.form.get('teaching_status') == 'Да':
        return render_template('teaching_data.html')
    elif request.form.get('teaching_status') == 'Нет':
        return render_template('management.html')


@person_routes.route('/management_status', methods=['POST'])
def management():
    if request.form.get('management_status') == 'Да':
        return render_template('management_data.html')
    elif request.form.get('management_status') == 'Нет':
        return render_template('research.html')


@person_routes.route('/research_status', methods=['POST'])
def research():
    if request.form.get('research_status') == 'Да':
        return render_template('research_data.html')
    elif request.form.get('research_status') == 'Нет':
        return render_template('internships.html')


@person_routes.route('/teaching_data', methods=['POST'])
def teaching_data():
    respondent_id = session.get('respondent_id')
    programs_list = request.form.getlist('courses')
    year_start = request.form.get('teaching_start_year')
    year_fin = request.form.get('teaching_end_year')
    new_teacher = StatusPerson(pers_id=respondent_id,
                               program=' '.join(programs_list),
                               stat_id=4,
                               year_start=year_start,
                               year_fin=year_fin)
    db.session.add(new_teacher)
    db.session.commit()
    return render_template('management.html')


@person_routes.route('/management_data', methods=['POST'])
def management_data():
    respondent_id = session.get('respondent_id')
    institutions = request.form.getlist('institution')
    other_institution = request.form.get('other_institution', '')
    if 'Другое' in institutions:
        institutions.remove('Другое')
        institutions.append(other_institution)

    year_start = request.form.get('management_start_year')
    year_fin = request.form.get('management_end_year')
    new_manager = StatusPerson(pers_id=respondent_id,
                               program=' '.join(institutions),
                               stat_id=5,
                               year_start=year_start,
                               year_fin=year_fin)
    db.session.add(new_manager)
    db.session.commit()

    return render_template('research.html')


@person_routes.route('/research_data', methods=['POST'])
def research_data():
    respondent_id = session.get('respondent_id')
    research_groups = request.form.getlist('research_groups')
    year_start = request.form.get('research_start_year')
    year_fin = request.form.get('research_end_year')
    new_laborant = StatusPerson(pers_id=respondent_id,
                                program=' '.join(research_groups),
                                stat_id=6,
                                year_start=year_start,
                                year_fin=year_fin)
    db.session.add(new_laborant)
    db.session.commit()
    return render_template('internships.html')


@person_routes.route('/internships', methods=['POST'])
def internships_data():
    respondent_id = session.get('respondent_id')
    sections = [key.split('_')[2] for key in request.form.keys()
                if key.startswith('intern_place_')]
    for section in sections:
        stage_name = request.form.get(f'intern_place_{section}')
        stage_year = request.form.get(f'intern_year_{section}')

        new_stage = Stages(pers_id=respondent_id,
                           year=stage_year,
                           stage=stage_name)
        db.session.add(new_stage)

    db.session.commit()
    return render_template('now.html')


@person_routes.route('/now', methods=['POST'])
def now():
    respondent_id = session.get('respondent_id')
    current_city = request.form.get('current_city')
    current_workplace = request.form.get('current_workplace')
    new_current = CurrentAddresses(pers_id=respondent_id,
                                   address=current_city,
                                   position=current_workplace)
    db.session.add(new_current)
    db.session.commit()
    return render_template('expedition.html')


@person_routes.route('/expedition_status', methods=['POST'])
def expedition():
    if request.form.get('expedition_status') == 'Да':
        return render_template('expedition_data.html')
    elif request.form.get('expedition_status') == 'Нет':
        return render_template('important.html')


@person_routes.route('/expedition_data', methods=['POST'])
def expedition_data():
    respondent_id = session.get('respondent_id')
    for exp in request.form.getlist('expeditions[]'):
        new_exp = ExpeditionsParticipation(pers_id=respondent_id,
                                           expeditions=exp)
        db.session.add(new_exp)
    db.session.commit()
    return render_template('important.html')


@person_routes.route('/important_data', methods=['POST'])
def important():
    respondent_id = session.get('respondent_id')
    sections = [key.split('_')[1] for key in request.form.keys()
                if key.startswith('project_')]
    for section in sections:
        project_desc = request.form.get(f'project_{section}')
        new_project = UserProjects(pers_id=respondent_id,
                                   project_info=project_desc)
        db.session.add(new_project)
        db.session.commit()
    return render_template('memories.html')


@person_routes.route('/memories_status', methods=['POST'])
def memories():
    if request.form.get('memories_status') == 'Да':
        return render_template('memories_data.html')
    elif request.form.get('memories_status') == 'Нет':
        return render_template('stories.html')


@person_routes.route('/memories_data', methods=['POST'])
def memories_data():
    respondent_id = session.get('respondent_id')
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
                                    contact=address,
                                    link=link,
                                    description=description)
        db.session.add(new_link)
        db.session.commit()

    elif response == 'Свяжитесь со мной позже':
        contact_method = request.form.get('contact-method')
        link = 'to be added'
        description = 'to be added'

        if contact_method == 'Указать новый адрес':
            address = request.form.get('new_address')

        new_link = CrowdSourceLinks(pers_id=respondent_id,
                                    contact=address,
                                    link=link,
                                    description=description)
        db.session.add(new_link)
        db.session.commit()

    return render_template('stories.html')


@person_routes.route('/stories_status', methods=['POST'])
def stories():
    if request.form.get('stories_status') == 'Да':
        return render_template('stories_data.html')
    elif request.form.get('stories_status') == 'Нет':
        return render_template('what_shl_is.html')


@person_routes.route('/stories_data', methods=['POST'])
def stories_data():
    respondent_id = session.get('respondent_id')
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
                                       contact=address,
                                       story=story)
        db.session.add(new_story)
        db.session.commit()
    elif response == 'Свяжитесь со мной позже':
        contact_method = request.form.get('contact-method')
        story = 'to be added'

        if contact_method == 'Указать новый адрес':
            address = request.form.get('new_address')

        new_story = CrowdSourceStories(pers_id=respondent_id,
                                       contact=address,
                                       story=story)
        db.session.add(new_story)
        db.session.commit()

    return render_template('what_shl_is.html')


@person_routes.route('/what_shl_is', methods=['POST'])
def what_shl_is():
    respondent_id = session.get('respondent_id')
    answer = request.form.get('answer')
    new_emotion = EmotionalSchl(pers_id=respondent_id,
                                content=answer)
    db.session.add(new_emotion)
    db.session.commit()
    return render_template('thanks.html')
