import math
import datetime
from flask import render_template, request, redirect, session, jsonify, url_for
from saleapp import app, untils


@app.route("/")
def home():
    data_mau = untils.get_data_mau()
    data_nha_hang_mau = untils.get_data_nha_hang_mau()
    # untils.so_luong_nha_hang_theo_quan()

    return render_template('index.html', data_mau=data_mau, data_nha_hang_mau=data_nha_hang_mau)

@app.route("/restaurant", methods=['get', 'post'])
def restaurant():
    name = request.args.get('kw', '')
    page = request.args.get('page', 1)
    count = 0


    if request.method == 'POST':
        name = request.form.get("name")

        if name != '':
            products, count = untils.search_by_name(name, page=int(page))
        else:
            products, count = untils.load_product()

        print(products)

        return render_template('restaurant.html', pages=math.ceil(count / app.config['PAGE_SIZE']), products=products, count=count, name=name, page_now=int(page))

    products, count = untils.search_by_name(name, page=int(page))


    return render_template('restaurant.html', pages=math.ceil(count / app.config['PAGE_SIZE']), products=products, count=count, name=name, page_now=int(page))


@app.route("/products/<int:product_id>")
def product_detail(product_id):

    command = request.args.get("command")

    if command == None:
        command = 1
    else:
        command = -int(command)

    comments = untils.load_comments(product_id)
    res = untils.load_res_by_id(product_id)

    visualize_time = untils.vizualize_restaurant(product_id)

    restaurant_evaluation = untils.restaurant_evaluation(product_id)

    res_avg = restaurant_evaluation['avg']

    untils.get_word_cloud(product_id)

    return render_template('product_detail.html', product_id=product_id, command = command, comments=comments, res=res, restaurant_evaluation=restaurant_evaluation, link="../static/image/Time_plot.png",
                           wordcloud_link='../static/image/Word_cloud_res.png', res_avg=int(res_avg))
@app.route("/sentiment", methods=['get', 'post'])
def sentiment():
    post = ''
    result = ''
    label = ''
    pos = 50
    neg = 50
    confi = {}
    if request.method == 'POST':
        post = request.form.get("feedback")
        if post == '':
            return render_template('sentiment.html', confi=confi, label=label, post=post.replace("_", " "), pos=pos, neg=neg)
        result = untils.predict_emotion(post)

        label = result['label']
        for confidence_data in result['confidences']:
            confi[confidence_data['label']] = confidence_data['confidence']
        pos = round(confi['POSITIVE'] * 100, 2)
        neg = round(confi['NEGATIVE'] * 100, 2)

    print(confi)

    return render_template('sentiment.html', confi=confi, label=label, post=post.replace("_", " "), pos=pos, neg=neg)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
