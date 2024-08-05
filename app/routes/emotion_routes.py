from flask import Blueprint, render_template, redirect, url_for, request


emotion_routes = Blueprint('emotion_routes', __name__)

@emotion_routes.route('/emotion/page_<string:page_id>')
def questionnaire(page_id):
    page_templates = {
        'personal_data': 'personal_data.html',
        'emotion_data': 'emotion_data.html',
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
    surname = request.form.get('surname')
    name = request.form.get('name')
    second_name = request.form.get('second_name')

    return redirect(url_for('emotion_routes.questionnaire',
                            page_id='emotion_data'))


@emotion_routes.route('/emotion_data', methods=['POST'])
def emotion_data():
    memories_education = request.form.get('memories-education')
    memories_life = request.form.get('memories-life')
    memories_people = request.form.get('memories-people')
    significant_spaces = request.form.get('significant-spaces')
    unusual_experience = request.form.get('unusual-experience')
    noun = request.form.get('noun')
    verb = request.form.get('verb')
    pronoun = request.form.get('pronoun')
    school_definition = request.form.get('school-definition')
    greetings = request.form.get('greetings')

    return redirect(url_for('emotion_routes.questionnaire', page_id='thanks'))
