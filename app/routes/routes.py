from flask import Blueprint, render_template, request
from app import db
from app.models.models import Person, StatusPerson

routes = Blueprint('routes', __name__)

current_person_id = None


@routes.route('/')
def main():
    return render_template('main.html')


@routes.route('/form')
def form():
    return render_template('personal_info.html')


@routes.route('/personal_info', methods=['POST'])
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


@routes.route('/student_status', methods=['POST'])
def student():
    if request.form.get('student_status') == 'Да':
        new_sp = StatusPerson(
            stat_id=1,
            pers_id=current_person_id,
            year_start=2020,
            year_fin=2024)
        db.session.add(new_sp)
        db.session.commit()
        return render_template('student_data.html')
    elif request.form.get('student_status') == 'Нет':
        new_sp = StatusPerson(
            stat_id=0,
            pers_id=current_person_id,
            year_start=2020,
            year_fin=2024)
        db.session.add(new_sp)
        db.session.commit()
        return render_template('employee.html')


@routes.route('/student_data', methods=['POST'])
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


@routes.route('/employee_status', methods=['POST'])
def employee():
    if request.form.get('employee_status') == 'Да':
        return render_template('employee_data.html')
    elif request.form.get('employee_status') == 'Нет':
        return render_template('non_official_status.html')


@routes.route('/employee_data', methods=['POST'])
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


@routes.route('/non_official_status', methods=['POST'])
def non_offical_status():
    # собираем какую-нибудь информацию
    return render_template('research_papers.html')


@routes.route('/research_papers', methods=['POST'])
def research_papers():
    research_papers = []
    # сил понять, как собирать данные, нет
    return render_template('thanks.html')


@routes.route('/contacts')
def contacts():
    return render_template('contacts.html')
