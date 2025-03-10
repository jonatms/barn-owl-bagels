from flask import Flask, render_template, request, make_response, session
import uuid
import base64
import os
  
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Lx1jEPHy2wXtmdUko2KywbiIMCKfttu8'

bind_port = 8000
  
@app.before_request
def before_request():
    if not 'username' in session:
        response = make_response() 
        session['username'] = "user"
        session['idor'] = "Incomplete"
        session['path'] = "Incomplete"
        if 'user_id' not in request.cookies:
            user_id = str(uuid.uuid4())
            response.set_cookie('user_id', user_id)
        if 'MSYHM' not in request.cookies:
            MSYHM = str(uuid.uuid4())
            response.set_cookie('MSYHM', MSYHM)
        if 'ai_central' not in request.cookies:
            ai_central = base64.b64encode(str(uuid.uuid4()).encode("ascii")).decode("ascii")
            response.set_cookie('user_id', ai_central)
        if 'vSecureCookie' not in request.cookies:
            sc = base64.b64encode("cookieFlagBypass=False".encode("ascii")).decode("ascii")
            response.set_cookie('vSecureCookie', sc)
        if 'ySoXT7' not in request.cookies:
            y = str(uuid.uuid4())
            response.set_cookie('ySoXT7', y)
        return response

@app.route('/idor', methods=['GET'])  
def idor():  
    return render_template('idor.html')

@app.route('/path', methods=['GET'])  
def path():  
    return render_template('path.html')

@app.route('/imageContent', methods=['GET'])  
def imageContent():  
    file_input = request.args.get('file')
    # remove path traversal payloads from path, twice
    if '../' in file_input:
        file_input = file_input.replace('../', '')
    if '../' in file_input:
        file_input = file_input.replace('../', '')
    if '..\\' in file_input:
        file_input = file_input.replace('..\\', '')
    if '..\\' in file_input:
        file_input = file_input.replace('..\\', '')

    path = 'static/content/images/' + file_input
    print(path)
    path = os.path.commonpath([os.path.abspath(path)])
    print(path)
    if 'Barn Owl Bagels\\static' not in path:
        return "Invalid path", 400
    if os.path.isdir(path):
        try:
            files = os.listdir(path)
            print(files)
            return render_template('directory.html', files=files, directory=path)
        except Exception as e:
            return str(e), 500
    elif path:
        try:
            with open(path, 'rb') as file:
                content = file.read()
            response = make_response(content)
            response.headers['Content-Type'] = 'image/jpeg'
            return response
        except FileNotFoundError:
            return "File not found", 404
        except Exception as e:
            return str(e), 500
    return "No file specified", 400

@app.route('/orderdetails/<int:order_id>', methods=['GET'])  
def order(order_id):  
    if order_id == 639:
        order_details = {
            "order_id": order_id,
            "item": "Flag",
            "quantity": "1",
            "price": "Free",
            "special_instructions": "1NS3CUr3_D1r3CT_BAG3L_r3F3r3C3"
        }
    elif order_id > 999 or order_id < 100:
        order_details = {
            "order_id": order_id,
            "item": "Invalid Order ID",
            "quantity": "Invalid Order ID",
            "price": "Invalid Order ID",
            "special_instructions": "Invalid Order ID"
        }
    else:  
        q = order_id % 8
        p = round(q * 4.33, 2)
        order_details = {
            "order_id": order_id,
            "item": "Bagel",
            "quantity": q,
            "price": p,
            "special_instructions": "Everything bagels please!"
        }
    return order_details

@app.route('/flags', methods=['GET'])  
def flags():  
    vSecureCookie = request.cookies.get('vSecureCookie')
    decoded_sc = base64.b64decode(vSecureCookie.encode("ascii")).decode("ascii")
    cFlag = "Incomplete"
    if decoded_sc == 'cookieFlagBypass=True':
        cFlag = "Complete"
    return render_template('flags.html', session=session, cookieFlag=cFlag)

@app.route('/submitflag', methods=['POST'])
def submit_flag():
    flag = request.form.get('flag')
    if flag == "1NS3CUr3_D1r3CT_BAG3L_r3F3r3C3":
        session['idor'] = "Complete"
        return "Flag is correct!"
    elif flag == 'the_path_less_traveled_leads_to_bagels':
        session['path'] = "Complete"
        return "Flag is correct!"
    else:
        return "Flag is incorrect."

if __name__ == '__main__':  
    app.run(debug=False, host='0.0.0.0', port=bind_port)