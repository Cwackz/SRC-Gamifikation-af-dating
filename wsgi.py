from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import requests

app = Flask(__name__, static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

user_profile = {
    'username': 'Dummy',
    'location': 'Copenhagen, Denmark',
    'looking_for': '?',
    'age': 18,
    'bio': 'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Voluptatibus similique voluptatem, praesentium vitae ex dolorem tenetur cum reiciendis iusto ratione laboriosam eligendi dolorum? Facere odio quos officia exercitationem quasi impedit.',
    'interests': ['Running', 'Travelling', 'Biking'],
    'profile_picture': 'default.png',
    'rating': 0
}
@app.before_request
async def before_request():
    await random_person()

@app.route('/admin', methods=['GET', 'POST'])
async def edit_profile():
    if request.method == 'POST':
        user_profile['username'] = request.form['username']
        user_profile['location'] = request.form['location']
        user_profile['age'] = int(request.form['age'])
        user_profile['bio'] = request.form['bio']
        user_profile['interests'] = request.form.getlist('interests')
        user_profile['rating'] = int(request.form['rating'])
        user_profile['looking_for'] = request.form['looking_for']

        if 'profile_picture' in request.files:
            file = request.files['profile_picture']

            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                user_profile['profile_picture'] = filename

        return redirect(url_for('profile'))

    return render_template('edit.html', profile=user_profile)

@app.route('/')
async def profile():
    return render_template('profile.html', profile=user_profile)

@app.route('/generate-person')
async def random_person():
    request_url = 'https://thispersondoesnotexist.com/'
    response = requests.get(request_url)
    if response.status_code == 200:
        image_data = response.content
        image_filename = "default.png"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        with open(image_path, 'wb') as image_file:
            image_file.write(image_data)
        return image_filename
    else:
        raise Exception('Failed to fetch image')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
