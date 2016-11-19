from flask import Flask, jsonify, request
import pg
import bcrypt
import uuid

password = 'null' # the entered password
salt = bcrypt.gensalt() # generate a salt
# now generate the encrypted password
encrypted_password = bcrypt.hashpw(password.encode('utf-8'), salt)

app = Flask('e-commerce')

db = pg.DB(dbname='E_commerce')


@app.route('/api/products')
def products():
    results = db.query('select * from product').dictresult()
    return jsonify(results)

@app.route('/api/product/<id>')
def product(id):

    results = db.query('select * from product where product.id = $1', id).dictresult()
    return jsonify(results)


@app.route('/api/user/signup', methods=['POST'])
def userSignUp():

    data = request.get_json()
    userName = data['username']
    password = data['password']
    email = data['email']
    firstName = data['first_name']
    lastName = data['last_name']
     # the entered password
    salt = bcrypt.gensalt() # generate a salt
    # now generate the encrypted password
    encrypted_password = bcrypt.hashpw(password.encode('utf-8'), salt)


    result = db.insert('customer', username=userName, password=encrypted_password, email=email, first_name=firstName, last_name=lastName)
    return jsonify(result)



@app.route('/api/user/login', methods=['POST'])
def login():
    data = request.get_json()
    password = data['password']
    customer = data['username']

    encrypted_password = db.query('select password, username, first_name, last_name, email, id from customer where customer.username=$1', customer).dictresult()[0]
    encrypted_passwordx = encrypted_password['password']
    myid = encrypted_password['id']
    rehash = bcrypt.hashpw(password.encode('utf-8'), encrypted_passwordx)
    if rehash == encrypted_passwordx:
        token = uuid.uuid4()
        tokenUpdate = db.insert('auth_token', customer_id=myid, token=token)

        userInfo = {
        'user': {
        'username': encrypted_password['username'],
        'email': encrypted_password['email'],
        'first name': encrypted_password['first_name'],
        'last name': encrypted_password['last_name']

        },
        'auth_token': tokenUpdate
        }
        print 'Login success!'
    else:
        print 'Login failed!'
    return jsonify(userInfo)


if __name__ == '__main__':
    app.run(debug=True)
