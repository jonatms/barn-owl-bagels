from flask import Flask, render_template, request, jsonify, make_response, session, send_file
import uuid
import base64
import random
import os
from datetime import datetime

app = Flask(__name__)
# This is the key for the session token, so that the session values can't be changed without this key
app.config['SECRET_KEY'] = 'Lx1jEPHy2wXtmdUko2KywbiIMCKfttu8'

bind_port = 8000

# Generate static gift cards on server load
amounts = [10, 25, 50, 75, 100]
all_gift_cards = [
    {"id": i, "amount": f"${random.choice(amounts)}", "expiry_date": f"2025-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}", "status": random.choice(["Active", "Redeemed"])}
    for i in range(1, 101)
]

@app.before_request
def before_request():
    if not 'username' in session:
        response = make_response() 
        session['username'] = "user"
        session['idor'] = "Incomplete"
        session['path'] = "Incomplete"
        session['mauth'] = "Incomplete"
        session['giftcards'] = "Incomplete"
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

@app.route('/mauth', methods=['GET'])  
def git():  
    return render_template('mauth.html')

@app.route('/gift-cards', methods=['GET'])
def gift_cards():
    return render_template('gift-cards.html')

@app.route('/api/gift-cards', methods=['GET'])
def api_gift_cards():
    is_managed = request.args.get('isManaged', 'false').lower() == 'true'

    # Ensure the first two gift cards have status "Redeemed"
    all_gift_cards[0]['status'] = "Redeemed"
    all_gift_cards[1]['status'] = "Redeemed"

    # Add a special flag for the gift card with id 58
    for card in all_gift_cards:
        if card['id'] == 58:
            card['id'] = "i_<3_bagel_gift_cards!"
            card['amount'] = "$100,000"
            card['expiry_date'] = "Never"
            card['status'] = "Active"
    
    if is_managed:
        gift_cards = [card for card in all_gift_cards if card['id'] in [1, 2]]
    else:
        gift_cards = [card for card in all_gift_cards if card['id'] not in [1, 2]]
    
    return jsonify(gift_cards)

@app.route('/imageContent', methods=['GET'])  
def imageContent():  
    file_input = request.args.get('file')
    # remove path traversal payloads from path, twice
    path_traversal_payloads = ['../','..\\']
    for i in range(2):
        for p in path_traversal_payloads:
            file_input = file_input.replace(p, '')

    path = 'static/content/images/' + file_input
    print(path)
    path = os.path.commonpath([os.path.abspath(path)])
    print(path)
    normalized_path = os.path.normcase(path)
    if 'static' not in normalized_path.replace('\\', '/'):
        return "Invalid path", 400
    if os.path.isdir(path):
        try:
            files = os.listdir(path)
            file_info = []
            for file in files:
                file_path = os.path.join(path, file)
                file_info.append({
                    'name': file,
                    'size': os.path.getsize(file_path),
                    'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d/%m/%Y')
                })
            return render_template('directory.html', files=file_info, directory=path)
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

@app.route('/superSecretSpecialFileContent', methods=['GET'])
def superSecretSpecialFileContent():
    file_name = request.args.get('fetchMeThe')
    file_path = os.path.normpath(os.path.join('static/flags/', file_name))
    try:
        return send_file(file_path)
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        return str(e), 500

@app.route('/specialadminendpoint', methods=['GET'])  
def special():  
    return "bagels_and_websites_are_full_of_holes"

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

@app.route('/', methods=['GET'])  
def home():
    return render_template('index.html')

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
    response = {"message": "Flag is incorrect."}
    if flag == "1NS3CUr3_D1r3CT_BAG3L_r3F3r3C3":
        session['idor'] = "Complete"
        response = {"message": "Flag is correct!", "idor": "Complete"}
    elif flag == 'the_path_less_traveled_leads_to_bagels':
        session['path'] = "Complete"
        response = {"message": "Flag is correct!", "path": "Complete"}
    elif flag == 'bagels_and_websites_are_full_of_holes':
        session['mauth'] = "Complete"
        response = {"message": "Flag is correct!", "git": "Complete"}
    elif flag == 'i_<3_bagel_gift_cards!':
        session['giftcards'] = "Complete"
        response = {"message": "Flag is correct!", "giftcards": "Complete"}
    return jsonify(response)

if __name__ == '__main__':  
    app.run(debug=False, host='0.0.0.0', port=bind_port)