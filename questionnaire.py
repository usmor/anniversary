from flask import Flask, render_template, request

app = Flask(__name__)
app.template_folder = 'app/templates'


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/person')
def person():
    return render_template('personal_info.html')


@app.route('/event')
def event():
    return render_template('event.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/personal_info', methods=['POST'])
def get_personal_info():
    surname = request.form.get('surname')
    name = request.form.get('name')
    second_name = request.form.get('second_name')
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
        return render_template('postgraduate.html')


@app.route('/postgraduate_status', methods=['POST'])
def postgraduate():
    if request.form.get('postgraduate_status') == 'Да':
        return render_template('postgraduate_data.html')
    elif request.form.get('postgraduate_status') == 'Нет':
        return render_template('employee.html')


@app.route('/bachelor_data', methods=['POST'])
def bachelor_data():
    bachelor_data = {}
    section_count = 1

    while True:
        bach_program = request.form.get(f'bach_program_{section_count}')
        bach_start_year = request.form.get(f'bach_start_year_{section_count}')
        bach_end_year = request.form.get(f'bach_end_year_{section_count}')

        if not bach_program and not bach_start_year and not bach_end_year:
            break

        bachelor_data[f'section_{section_count}'] = {
            'bach_program': bach_program,
            'bach_start_year': bach_start_year,
            'bach_end_year': bach_end_year
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

        if not master_program and not master_start_year and not master_end_year:
            break

        master_data[f'section_{section_count}'] = {
            'master_program': master_program,
            'master_start_year': master_start_year,
            'master_end_year': master_end_year
        }

        section_count += 1

    return render_template('postgraduate.html')


@app.route('/postgraduate_data', methods=['POST'])
def postgraduate_data():
    postgraduate_data = {}
    section_count = 1

    while True:
        post_program = request.form.get(f'post_program_{section_count}')
        post_start_year = request.form.get(f'post_start_year_{section_count}')
        post_end_year = request.form.get(f'post_end_year_{section_count}')

        if not post_program and not post_start_year and not post_end_year:
            break

        postgraduate_data[f'section_{section_count}'] = {
            'post_program': post_program,
            'post_start_year': post_start_year,
            'post_end_year': post_end_year
        }

        section_count += 1

    return render_template('employee.html')


@app.route('/employee_status', methods=['POST'])
def employee():
    if request.form.get('employee_status') == 'Да':
        return render_template('teaching.html')
    elif request.form.get('employee_status') == 'Нет':
        return render_template('non_official_status.html')


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
        return render_template('non_official_status.html')


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

    return render_template('non_official_status.html')


@app.route('/non_official_status', methods=['POST'])
def non_offical_status():
    # собираем какую-нибудь информацию
    return render_template('funny.html')


@app.route('/funny', methods=['POST'])
def funny():
    # собираем какую-нибудь информацию
    return render_template('thanks.html')


@app.route('/event_data', methods=['POST'])
def event_data():
    # собираем какую-нибудь информацию
    return render_template('thanks.html')


if __name__ == '__main__':
    app.run(debug=False, port=5001)
