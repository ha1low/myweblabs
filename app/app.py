import random
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, redirect, url_for
from faker import Faker
import re

fake = Faker('ru_RU')

app = Flask(__name__)
application = app

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']


def generate_comments(replies=True):
    comments = []
    for i in range(random.randint(1, 3)):
        comment = {
            'author': fake.name(),
            'text': fake.text(),
            'date': fake.date_time_between(start_date='-2y', end_date='now'),
            'replies': []
        }
        if replies:
            comment['replies'] = [{
                'author': fake.name(),
                'text': fake.text(),
                'date': fake.date_time_between(start_date='-2y', end_date='now')
            } for _ in range(random.randint(0, 2))]
        comments.append(comment)
    return comments


def generate_post(i):
    return {
        'id': i,
        'title': fake.sentence(),
        'text': fake.paragraph(nb_sentences=10),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }


posts_list = sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list)


@app.route('/posts/<int:index>', methods=['GET', 'POST'])
def post(index):
    if request.method == 'POST':
        new_comment = {
            'author': fake.name(),
            'text': request.form['comment_text'],
            'date': datetime.now(),
            'replies': []
        }
        posts_list[index]['comments'].insert(0, new_comment)

    p = posts_list[index]
    return render_template('post.html',
                           title=p['title'],
                           post=p,
                           current_year=datetime.now().year)


@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')

# ЛАБА 2!!!
# Добавляем новые маршруты
@app.route('/url-params')
def url_params():
    return render_template('url_params.html',
                         url_args=request.args,
                         title='Параметры URL')

@app.route('/headers')
def headers():
    return render_template('headers.html',
                         headers=request.headers,
                         title='Заголовки')

@app.route('/cookies')
def cookies():
    return render_template('cookies.html',
                         cookies=request.cookies,
                         title='Cookie')

@app.route('/form-example')
def form_example():
    return render_template('form_example.html',
                         title='Пример формы')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    form_data = {}
    if request.method == 'POST':
        form_data = {
            'login': request.form.get('login'),
            'password': request.form.get('password')
        }
    return render_template('auth.html', form_data=form_data, title='Авторизация')


@app.route('/phone', methods=['GET', 'POST'])
def phone():
    error = None
    phone_number = None
    formatted_number = None

    if request.method == 'POST':
        phone_number = request.form.get('phone')
        error = validate_phone(phone_number)

        if not error:
            formatted_number = format_phone(phone_number)

    return render_template('phone.html',
                           phone_number=phone_number,
                           formatted_number=formatted_number,
                           error=error,
                           title='Проверка телефона')


def validate_phone(number):
    cleaned = re.sub(r'[+\-()\s.]', '', number)

    if not cleaned.isdigit():
        return 'invalid_chars'

    # Определяем допустимую длину
    if cleaned.startswith(('7', '8')):
        if len(cleaned) != 11:
            return 'invalid_length'
    else:
        if len(cleaned) not in (10, 11):
            return 'invalid_length'

    return None

def format_phone(number):
    cleaned = re.sub(r'\D', '', number)

    # Если номер начинается с 7 или 8 и имеет 11 цифр
    if len(cleaned) == 11 and cleaned.startswith(('7', '8')):
        return f'8-{cleaned[1:4]}-{cleaned[4:7]}-{cleaned[7:9]}-{cleaned[9:]}'

    # Если номер имеет 10 цифр (без префикса)
    elif len(cleaned) == 10:
        return f'8-{cleaned[0:3]}-{cleaned[3:6]}-{cleaned[6:8]}-{cleaned[8:]}'

    # Для номеров с другим форматом
    return cleaned



if __name__ == '__main__':
    app.run(debug=True)

#@app.route('/search')
#def search():
    #   query = request.args.get('q', '')  # Получить параметр 'q' (значение по умолчанию: '')
#  return f"Search query: {query}"


#@app.route('/login', methods=['POST'])
#def login():
    #   username = request.form.get('username')
    #  password = request.form.get('password')
    # Проверка данных...
# return "Login processed"

#@app.route('/json')
#def json_response():
    #   data = {"key": "value"}  # Создаём словарь Python
    #  response = make_response(jsonify(data))  # Создаём объект Response
    # response.headers['Content-Type'] = 'application/json'  # Устанавливаем заголовок
    #return response