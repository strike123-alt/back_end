from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from ecdsa import SigningKey, VerifyingKey, NIST384p, BadSignatureError
from flask_session import Session
from passlib.hash import sha256_crypt
from uuid import uuid4
# from wtforms import FileField, TextAreaField
# from wtforms.validators import InputRequired


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/user_detail"
mongo = PyMongo(app)
app.secret_key = 'Blue@System26'
sess = Session()
sess.init_app(app)
CORS(app)


@app.route("/signup", methods=['POST'])
# @cross_origin()
def sign_up():

    print(request.form['firstName'])
    _name = request.form['firstName']
    print(request.form['lastName'])
    _lastname = request.form['lastName']
    print(request.form['mobile'])
    _mobile = request.form['mobile']
    print(request.form['email'])
    _email = request.form['email']
    print(request.form['password'])
    _password = request.form['password']

    _sk = SigningKey.generate(curve=NIST384p)
    _vk = _sk.verifying_key
    _sk = _sk.to_string().hex()
    _vk = _vk.to_string().hex()
    print(_sk)
    print(_vk)

    id = mongo.db.user_info.insert_one({'name': _name, 'last_name': _lastname, 'mobile': _mobile,
                                       'email': _email, 'password': sha256_crypt.hash(_password), 'private_key': _sk, 'verify_key': _vk})
    return 'Success'
    # return {"success": True}


@app.route("/signin", methods=['POST'])
# @cross_origin()
def sign_in():

    email = request.form['email']
    password = request.form['password']

    user = mongo.db.user_info.find_one({'email': email})
    r_pass = sha256_crypt.verify(password, user['password'])
    if user is None or not (r_pass):
        return 'Failed'
    else:
        return 'Success'


@ app.route("/fileUpload", methods=['POST'])
# @cross_origin()
def file_upload():
    # form = UploadFileForm()

    # user_info = mongo.db.session.find_one({'email': email})
    file_name = request.form.get('fileName').split('.')[0]
    file = request.files.get('file').read()
    email = request.form.get('email')
    print(type(file))
    # print(email)
    print(file_name, '\n',  email)
    user = mongo.db.user_info.find_one({'email': email})
    private_key = user['private_key']
    sign = SigningKey.from_string(bytes.fromhex(
        private_key), curve=NIST384p)
    m_d = sign.sign(file)
    is_file = mongo.db.file_name.find_one({'file_sign': m_d})
    u_id = uuid4().hex
    if is_file is None:
        id = mongo.db.file_name.insert_one(
            {'email': email, 'file_id': u_id, 'file_name': file_name, 'file_sign': m_d.hex()})
        return 'Success'
    else:
        return 'Failed'


@ app.route("/fileVerify", methods=['POST'])
# @cross_origin()
def file_verify():
    file_id = request.form.get('fileName')
    doc = request.files.get('file').read()
    is_file = mongo.db.file_name.find_one({'file_id': file_id})
    if is_file is None:
        return 'Failed'
    else:
        m_d = is_file['file_sign']
        email = is_file['email']
        user = mongo.db.user_info.find_one({'email': email})
        vk = VerifyingKey.from_string(
            bytes.fromhex(user['verify_key']), curve=NIST384p)
        try:
            is_sign = vk.verify(bytes.fromhex(m_d), doc)
            return 'Verify'
        except BadSignatureError:
            is_sign = False
            print(is_sign)
            return 'Bad-Sign'


@ app.route("/fileDisplay", methods=['POST'])
def file_display():
    email = request.form.get('email')
    file_detail = mongo.db.file_name.find(
        {'email': email}, {'_id': False, 'email': False})
    file_detail = jsonify(list(file_detail))
    return file_detail


if __name__ == "__main__":

    app.run(port=5000, debug=True)
