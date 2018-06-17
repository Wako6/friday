from flask import Flask, render_template, request, make_response, redirect, url_for
import requests



app = Flask(__name__)

#server_endpoint = "http://127.0.0.1:5001"
server_endpoint = "http://spacink.xyz:5000"

@app.before_request
def before_request():
    if request.endpoint == 'login' and request.method == 'GET':
        r = requests.get(server_endpoint + '/session', headers={'x-access-token': request.cookies.get('token','')})
        print(r.text)
        if r.status_code == 200 and r.text == 'True':
            return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/standing')
def standing():
    return render_template('standing.html')

@app.route('/user/<name>')
def user_one(name):
    # TODO
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        r = requests.post(server_endpoint + '/login', json={'username': request.form['username'],
                                                        'password': request.form['password']})
        if r.status_code == 200:
            json = r.json()
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('token', json['token'])
            return resp

    return render_template('login.html')


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        r = requests.post(server_endpoint+'/signin', json={'name': request.form['name'], 'email': request.form['email'],
                                                                  'password': request.form['password']})
        if r.status_code == 200:
            json = r.json()
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('token', json['token'])
            return resp

    return render_template('login.html')


@app.route('/logout')
def logout():
    # flash('You were logged out')
    r = requests.post(server_endpoint + '/logout', headers={'x-access-token': request.cookies.get('token')})
    if r.status_code == 200 or r.status_code == 401:
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('token', '', expires=0)
        return resp
    return redirect(url_for('index'))


@app.route('/new_topic', methods=['GET', 'POST'])
def new_topic():
    return render_template('new_topic.html')


@app.route('/topics', methods=['GET', 'POST'])
def topic_handler():
    if request.method == 'GET':
        # r = requests.get('server_endpoint/topic', headers={'x-access-token': request.cookies.get('token')})
        r = requests.get(server_endpoint + '/topic', headers={'x-access-token': request.cookies.get('token')})
        if r.status_code == 200:
            json = r.json()
            topics = json.get('topics')

    if request.method == 'POST':
        print(request.form['name'])
        r = requests.post(server_endpoint + '/topic', headers={'x-access-token': request.cookies.get('token')},
                          json={'name': request.form['name']})
        if r.status_code == 200:
            json = r.json()
            token_img = json['token_image']
            print(request.files['file'])
            f = request.files['file']
            # c = checksumMD5(f.stream)
            f.seek(0)
            sendFile = {"file": (f.filename, f.stream, f.mimetype)}
            r = requests.post(server_endpoint+'/', files=sendFile,
                             headers={'token_image': token_img})
            if r.status_code != 200:
                print("fail")
                return redirect(request.url, code=302)
            r = requests.put(server_endpoint+'/topic/' + request.form['name'],
                             headers={'x-access-token': request.cookies.get('token'),
                                      'token_image': token_img})
            if r.status_code != 200:
                return "fail"
            return url_for('topic_handler')
    return render_template('topics.html', topic_list=topics)


@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    r = requests.get(server_endpoint+'/topic', headers={'x-access-token': request.cookies.get('token')})
    if r.status_code == 200:
        json = r.json()
        topics = json.get('topics')
    return render_template('new_post.html', topic_list=topics)


@app.route('/posts', methods=['GET', 'POST'])
def get_post():
    #print()
    #print(request.form.getlist('topic'))
    if request.method == 'POST':
        r = requests.post(server_endpoint+ '/post', headers={'x-access-token': request.cookies.get('token')},
                          json={'title': request.form['title'], 'body': request.form['body'],
                                'topics': request.form.getlist('topics')})
        if r.status_code == 200:
            json = r.json()
            token_img = json.get('token_image')
            id = json.get('id')
            if 'file' not in request.files:
                return redirect(request.url, code=302)
            f = request.files['file']
            # c = checksumMD5(f.stream)
            f.seek(0)
            sendFile = {"file": (f.filename, f.stream, f.mimetype)}
            r = requests.post(server_endpoint+'/', files=sendFile,
                              headers={'token_image': token_img})
            if r.status_code != 200:
                return redirect(request.url, code=302)
            r = requests.put(server_endpoint + '/post/' + id,
                             headers={'x-access-token': request.cookies.get('token'),
                                      'token_image': token_img})
        #    topics = json.get('topic')
        # return render_template('new_post.html')

    # r = requests.get('server_endpoint/topic', headers={'x-access-token': request.cookies.get('token')})
    r = requests.get(server_endpoint + '/post', headers={'x-access-token': request.cookies.get('token')})
    #TODO change URI
    posts = None
    username = None
    if r.status_code == 200:
        json = r.json()
        posts = json.get('posts')
        r = requests.get(server_endpoint + '/session', headers={'x-access-token': request.cookies.get('token', '')})
        if r.status_code == 200:
            json = r.json()
            username = json.get('username')
    return render_template('posts.html', post_list=posts, username=username)


@app.route('/rate_post/<p_id>', methods=['GET', 'POST'])
def set_rate(p_id):
    r = requests.post(server_endpoint + '/rate_post/' + p_id, headers={'x-access-token': request.cookies.get('token')},
                      json={'rate': request.form.get('body')})
    json = r.json()
    return json.get('new_rate')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)