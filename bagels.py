from flask import Flask, render_template, request, make_response
import uuid
  
app = Flask(__name__)

bind_port = 8000
  
@app.before_request
def before_request():
    if 'user_id' not in request.cookies:
        user_id = str(uuid.uuid4())
        response = make_response()
        response.set_cookie('user_id', user_id)
        return response

@app.route('/idor', methods=['GET'])  
def idor():  
    return render_template('idor.html')

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

if __name__ == '__main__':  
    app.run(debug=False, port=bind_port)