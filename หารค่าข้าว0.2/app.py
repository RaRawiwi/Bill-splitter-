from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder='templates')  # ระบุโฟลเดอร์ templates

# โค้ดที่เหลือไม่เปลี่ยนแปลง


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # รับค่าที่ส่งมาจากฟอร์ม
    food_names = request.form.getlist('food[]')
    food_prices = request.form.getlist('price[]')
    participant_names = request.form.getlist('participant[]')
    participant_foods = request.form.getlist('foods[]')

    # แปลงข้อมูลอาหารและราคาเป็น list
    foods = []
    for food_name, food_price in zip(food_names, food_prices):
        if food_name and food_price:
            foods.append({
                'name': food_name,
                'price': float(food_price)
            })

    # แปลงข้อมูลผู้ทานและอาหารที่ทานเป็น list
    participants = []
    for participant_name, food_list in zip(participant_names, participant_foods):
        foods_list = [f.strip() for f in food_list.split(',')]
        participants.append({
            'name': participant_name,
            'foods': foods_list
        })

    # คำนวณค่าใช้จ่ายของแต่ละคน
    result = {}
    for participant in participants:
        total_cost = 0
        for food in participant['foods']:
            food_item = next((f for f in foods if f['name'] == food), None)
            if food_item:
                # หาคนที่ทานอาหารชนิดเดียวกัน
                eaters = [p for p in participants if food in p['foods']]
                total_cost += food_item['price'] / len(eaters)
        result[participant['name']] = total_cost

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
