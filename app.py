from flask import Flask, render_template, request, redirect, url_for
from models import db, Order

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html', success=request.args.get("success"))

@app.route('/submit_order', methods=['POST'])
def submit_order():
    main_dish = request.form['main_dish']
    side_dishes = request.form.getlist('side_dishes')  # 多選會是 list
    
    # 確保選擇的配菜不超過三樣
    if len(side_dishes) > 3:
        return redirect(url_for('index', success=0))

    order = Order(
        main_dish=main_dish,
        side_dishes=", ".join(side_dishes)  # 存成一個字串，例如 "滷蛋, 花椰菜"
    )
    db.session.add(order)
    db.session.commit()
    
    return redirect(url_for('index', success=1))

@app.route('/orders')
def orders():
    # 查詢所有訂單
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
