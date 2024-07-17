from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.template_folder = 'app/templates'
app.config['UPLOAD_FOLDER'] = 'app/uploads'


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/person')
def person():
    return render_template('personal_info.html')


# @app.route('/event')
# def event():
#     return render_template('event.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/personal_info', methods=['POST'])
def get_personal_info():
    surname = request.form.get('surname')
    name = request.form.get('name')
    second_name = request.form.get('second_name', '')

    address = request.form.get('address')

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    photo = request.files.get('photo')
    photo_name = None
    initials = f'{surname} {name} {second_name}'
    if photo and photo.filename != '':
        photo_name = initials + os.path.splitext(photo.filename)[1]
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_name)

        try:
            photo.save(photo_path)
        except Exception as e:
            print(f"Ошибка при сохранении фотографии {photo.filename} у пользователя по имени {initials}: {e}")

    return render_template('student.html')


@app.route('/student_status', methods=['POST'])
def student():
    if request.form.get('student_status') == 'Да':
        return render_template('bachelor.html')
    elif request.form.get('student_status') == 'Нет':
        return render_template('employee.html')


@app.route('/bachelor_status', methods=['POST'])
def bachelor():
    if request.form.get('bachelor_status') == 'Да':
        return render_template('bachelor_data.html')
    elif request.form.get('bachelor_status') == 'Нет':
        return render_template('master.html')


@app.route('/master_status', methods=['POST'])
def master():
    if request.form.get('master_status') == 'Да':
        return render_template('master_data.html')
    elif request.form.get('master_status') == 'Нет':
        return render_template('phd.html')


@app.route('/phd_status', methods=['POST'])
def phd():
    if request.form.get('phd_status') == 'Да':
        return render_template('phd_data.html')
    elif request.form.get('phd_status') == 'Нет':
        return render_template('employee.html')


@app.route('/bachelor_data', methods=['POST'])
def bachelor_data():
    bachelor_data = {}
    section_count = 1

    while True:
        bach_program = request.form.get(f'bach_program_{section_count}')
        bach_start_year = request.form.get(f'bach_start_year_{section_count}')
        bach_end_year = request.form.get(f'bach_end_year_{section_count}')
        bach_curator = request.form.get(f'bach_curator_{section_count}')

        if not bach_program and not bach_start_year and not bach_end_year and not bach_curator:
            break

        bachelor_data[f'bachelor_degree_{section_count}'] = {
            'bach_program': bach_program,
            'bach_start_year': bach_start_year,
            'bach_end_year': bach_end_year,
            'bach_curator': bach_curator
        }

        section_count += 1

    return render_template('master.html')


@app.route('/master_data', methods=['POST'])
def master_data():
    master_data = {}
    section_count = 1

    while True:
        master_program = request.form.get(f'master_program_{section_count}')
        master_start_year = request.form.get(f'master_start_year_{section_count}')
        master_end_year = request.form.get(f'master_end_year_{section_count}')
        master_curator = request.form.get(f'master_curator_{section_count}')

        if not master_program and not master_start_year and not master_end_year and not master_curator:
            break

        master_data[f'master_degree_{section_count}'] = {
            'master_program': master_program,
            'master_start_year': master_start_year,
            'master_end_year': master_end_year,
            'master_curator': master_curator
        }

        section_count += 1

    return render_template('phd.html')


@app.route('/phd_data', methods=['POST'])
def phd_data():
    phd_data = {}
    section_count = 1

    while True:
        phd_program = request.form.get(f'phd_program_{section_count}')
        phd_start_year = request.form.get(f'phd_start_year_{section_count}')
        phd_end_year = request.form.get(f'phd_end_year_{section_count}')
        phd_curator = request.form.get(f'phd_curator_{section_count}')

        if not phd_program and not phd_start_year and not phd_end_year and not phd_curator:
            break

        phd_data[f'phd_degree_{section_count}'] = {
            'phd_program': phd_program,
            'post_start_year': phd_start_year,
            'post_end_year': phd_end_year,
            'phd_curator': phd_curator
        }

        section_count += 1

    return render_template('employee.html')


@app.route('/employee_status', methods=['POST'])
def employee():
    if request.form.get('employee_status') == 'Да':
        return render_template('teaching.html')
    elif request.form.get('employee_status') == 'Нет':
        return render_template('internships.html')


@app.route('/teaching_status', methods=['POST'])
def teaching():
    if request.form.get('teaching_status') == 'Да':
        return render_template('teaching_data.html')
    elif request.form.get('teaching_status') == 'Нет':
        return render_template('management.html')


@app.route('/management_status', methods=['POST'])
def management():
    if request.form.get('management_status') == 'Да':
        return render_template('management_data.html')
    elif request.form.get('management_status') == 'Нет':
        return render_template('research.html')


@app.route('/research_status', methods=['POST'])
def research():
    if request.form.get('research_status') == 'Да':
        return render_template('research_data.html')
    elif request.form.get('research_status') == 'Нет':
        return render_template('internships.html')


@app.route('/teaching_data', methods=['POST'])
def teaching_data():
    teaching_data = {}
    section_count = 1

    while True:
        teaching_position = request.form.get(f'teaching_position_{section_count}')
        subject = request.form.get(f'subject_{section_count}')
        teaching_start_year = request.form.get(f'teaching_start_year_{section_count}')
        teaching_end_year = request.form.get(f'teaching_end_year_{section_count}')

        if not teaching_position and not subject and not teaching_start_year and not teaching_end_year:
            break

        teaching_data[f'section_{section_count}'] = {
            'teaching_position': teaching_position,
            'subject': subject,
            'teaching_start_year': teaching_start_year,
            'teaching_end_year': teaching_end_year
        }

        section_count += 1

    return render_template('management.html')


@app.route('/management_data', methods=['POST'])
def management_data():
    management_data = {}
    section_count = 1

    while True:
        management_position = request.form.get(f'management_position_{section_count}')
        management_start_year = request.form.get(f'management_start_year_{section_count}')
        management_end_year = request.form.get(f'management_end_year_{section_count}')

        if not management_position and not management_start_year and not management_end_year:
            break

        management_data[f'section_{section_count}'] = {
            'management_position': management_position,
            'management_start_year': management_start_year,
            'management_end_year': management_end_year
        }

        section_count += 1
    return render_template('research.html')


@app.route('/research_data', methods=['POST'])
def research_data():
    research_data = {}
    section_count = 1

    while True:
        laboratory_name = request.form.get(f'laboratory_name_{section_count}')
        research_position = request.form.get(f'research_position_{section_count}')
        research_start_year = request.form.get(f'research_start_year_{section_count}')
        research_end_year = request.form.get(f'research_end_year_{section_count}')

        if not laboratory_name and not research_position and not research_start_year and not research_end_year:
            break

        research_data[f'section_{section_count}'] = {
            'laboratory_name': laboratory_name,
            'research_position': research_position,
            'research_start_year': research_start_year,
            'research_end_year': research_end_year
        }

        section_count += 1

    return render_template('internships.html')


@app.route('/internships', methods=['POST'])
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


@app.route('/now', methods=['POST'])
def now():
    current_city = request.form.get('current_city')
    current_workplace = request.form.get('current_workplace')
    return render_template('expedition.html')


@app.route('/expedition_status', methods=['POST'])
def expedition():
    if request.form.get('expedition_status') == 'Да':
        return render_template('expedition_data.html')
    elif request.form.get('expedition_status') == 'Нет':
        return render_template('important.html')


@app.route('/expedition_data', methods=['POST'])
def expedition_data():
    return render_template('important.html')


@app.route('/important_data', methods=['POST'])
def important():
    important_projects = {}
    section_count = 1
    while True:
        project = request.form.get(f'project_{section_count}')

        if not project:
            break

    important_projects[f'important_project_{section_count}'] = project

    return render_template('memories.html')


@app.route('/memories_status', methods=['POST'])
def memories():
    if request.form.get('memories_status') == 'Да':
        return render_template('memories_data.html')
    elif request.form.get('memories_status') == 'Нет':
        return render_template('stories.html')


@app.route('/memories_data', methods=['POST'])
def memories_data():
    return render_template('stories.html')


@app.route('/stories_status', methods=['POST'])
def stories():
    if request.form.get('stories_status') == 'Да':
        return render_template('stories_data.html')
    elif request.form.get('stories_status') == 'Нет':
        return render_template('what_shl_is.html')


@app.route('/stories_data', methods=['POST'])
def stories_data():
    return render_template('what_shl_is.html')


@app.route('/what_shl_is', methods=['POST'])
def what_shl_is():
    answer = request.form.get('answer')
    return render_template('thanks.html')

# @app.route('/event_data', methods=['POST'])
# def event_data():
#     # собираем какую-нибудь информацию
#     return render_template('thanks.html')


if __name__ == '__main__':
    app.run(debug=False, port=5001)
