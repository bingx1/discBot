from flask import Flask, jsonify, request, render_template
# from flask_bootstrap import Bootstrap
app = Flask(__name__)
# bootstrap = Bootstrap(app)

@app.route('/index')
@app.route('/')
def index():
    items = [{'name': 'Rogue Ohio Deadlift Bar - Black Zinc', 'price': 550, 'stock': False, 'url': 'https://www.rogueaustralia.com.au/rogue-ohio-deadlift-bar-black-zinc-au', 'img_url': 'https://assets.roguefitness.com/f_auto,q_auto,h_400,b_rgb:f8f8f8/catalog/Weightlifting%20Bars%20and%20Plates/Barbells/Mens%2020KG%20Barbells/AU-RA0963-BLBR/AU-RA0963-BLBR-h_t4opya.png'},
             {'name': 'Rogue 20KG Ohio Power Bar - Stainless Steel', 'price': 680, 'stock': True, 'url': 'https://www.rogueaustralia.com.au/rogue-20-kg-ohio-power-bar-stainless-steel-au', 'img_url':'https://assets.roguefitness.com/f_auto,q_auto,h_400,b_rgb:f8f8f8/catalog/Weightlifting%20Bars%20and%20Plates/Barbells/Mens%2020KG%20Barbells/RA0692-SSDC/20kg-ohio-power-bar-header-1_1_IPF_qbhfyb.jpg'}]

    return render_template('index.html', title='Home', items=items)


@app.route('/api/items/all', methods=['GET'])
def fetch_all_items():
    return


if __name__ == "__main__":
    app.run()
