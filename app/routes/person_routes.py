import os

from flask import Blueprint, render_template, request, current_app
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
    new_person = Person(surname=surname,
                        name=name,
                        second_name=second_name,
                        contact=contact,
                        photo_filename=photo_name)
    db.session.add(new_person)
    db.session.commit()
    global respondent_id
    respondent_id = new_person.id

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
    program = request.form.get('bach_program_1')
    year_start = request.form.get('bach_start_year_1')
    year_fin = request.form.get('bach_end_year_1')
    curator = request.form.get('bach_curator_1')
    new_bach = StatusPerson(pers_id=respondent_id,
                            program=program,
                            stat_id=1,
                            year_start=year_start,
                            year_fin=year_fin,
                            curator=curator)
    db.session.add(new_bach)
    db.session.commit()
    return render_template('master.html')


@person_routes.route('/master_data', methods=['POST'])
def master_data():
    program = request.form.get('master_program_1')
    year_start = request.form.get('master_start_year_1')
    year_fin = request.form.get('master_end_year_1')
    curator = request.form.get('master_curator_1')
    new_master = StatusPerson(pers_id=respondent_id,
                              program=program,
                              stat_id=2,
                              year_start=year_start,
                              year_fin=year_fin,
                              curator=curator)
    db.session.add(new_master)
    db.session.commit()

    return render_template('phd.html')


@person_routes.route('/phd_data', methods=['POST'])
def phd_data():
    program = request.form.get('phd_program_1')
    year_start = request.form.get('phd_start_year_1')
    year_fin = request.form.get('phd_end_year_1')
    curator = request.form.get('phd_curator_1')
    new_phd = StatusPerson(pers_id=respondent_id,
                           program=program,
                           stat_id=3,
                           year_start=year_start,
                           year_fin=year_fin,
                           curator=curator)
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
    intern_data = {}
    section_count = 1
    while True:
        intern_place = request.form.get(f'intern_place_{section_count}')
        intern_year = request.form.get(f'intern_year_{section_count}')

        if not intern_place and not intern_year:
            break

    intern_data[f'internship_{section_count}'] = {
        'intern_place': intern_place,
        'intern_year': intern_year
    }

    return render_template('now.html')


@person_routes.route('/now', methods=['POST'])
def now():
    current_city = request.form.get('current_city')
    current_workplace = request.form.get('current_workplace')
    return render_template('expedition.html')


@person_routes.route('/expedition_status', methods=['POST'])
def expedition():
    if request.form.get('expedition_status') == 'Да':
        return render_template('expedition_data.html')
    elif request.form.get('expedition_status') == 'Нет':
        return render_template('important.html')


@person_routes.route('/expedition_data', methods=['POST'])
def expedition_data():
    return render_template('important.html')


@person_routes.route('/important_data', methods=['POST'])
def important():
    important_projects = {}
    section_count = 1
    while True:
        project = request.form.get(f'project_{section_count}')
        if not project:
            break

    important_projects[f'important_project_{section_count}'] = project

    return render_template('memories.html')


@person_routes.route('/memories_status', methods=['POST'])
def memories():
    if request.form.get('memories_status') == 'Да':
        return render_template('memories_data.html')
    elif request.form.get('memories_status') == 'Нет':
        return render_template('stories.html')


@person_routes.route('/memories_data', methods=['POST'])
def memories_data():
    response = request.form.get('response')
    if response == 'Поделюсь сейчас':
        link = request.form.get('link')
        description = request.form.get('description')
    elif response == 'Свяжитесь со мной позже':
        contact_method = request.form.get('contact-method')
        if contact_method == 'По тому адресу, который был указан мною ранее':
            # в бд должен остаться старый адрес
            pass
        elif contact_method == 'Указать новый адрес':
            # в бд новый адрес
            new_address = request.form.get('new_address')
    return render_template('stories.html')


@person_routes.route('/stories_status', methods=['POST'])
def stories():
    if request.form.get('stories_status') == 'Да':
        return render_template('stories_data.html')
    elif request.form.get('stories_status') == 'Нет':
        return render_template('what_shl_is.html')


@person_routes.route('/stories_data', methods=['POST'])
def stories_data():
    response = request.form.get('response')
    if response == 'Поделюсь сейчас':
        story = request.form.get('story')
    elif response == 'Свяжитесь со мной позже':
        contact_method = request.form.get('contact-method')
        if contact_method == 'По тому адресу, который был указан мною ранее':
            # в бд должен остаться старый адрес
            pass
        elif contact_method == 'Указать новый адрес':
            # в бд новый адрес
            new_address = request.form.get('new_address')
    return render_template('what_shl_is.html')


@person_routes.route('/what_shl_is', methods=['POST'])
def what_shl_is():
    answer = request.form.get('answer')
    return render_template('thanks.html')
