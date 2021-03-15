from flask import Flask, jsonify, request, render_template
from util.db_handler import DbHandler
app = Flask(__name__)
DbHandler = DbHandler()

@app.route('/index')
@app.route('/')
def index():
    items = [{'name': 'Rogue Ohio Deadlift Bar - Black Zinc', 'manufacturer':'Rogue', 'price': 550, 'stock': False, 'url': 'https://www.rogueaustralia.com.au/rogue-ohio-deadlift-bar-black-zinc-au', 'img_url': 'https://assets.roguefitness.com/f_auto,q_auto,h_400,b_rgb:f8f8f8/catalog/Weightlifting%20Bars%20and%20Plates/Barbells/Mens%2020KG%20Barbells/AU-RA0963-BLBR/AU-RA0963-BLBR-h_t4opya.png'},
             {'name': 'Rogue 20KG Ohio Power Bar - Stainless Steel', 'manufacturer':'Rogue','price': 680, 'stock': True, 'url': 'https://www.rogueaustralia.com.au/rogue-20-kg-ohio-power-bar-stainless-steel-au', 'img_url':'https://assets.roguefitness.com/f_auto,q_auto,h_400,b_rgb:f8f8f8/catalog/Weightlifting%20Bars%20and%20Plates/Barbells/Mens%2020KG%20Barbells/RA0692-SSDC/20kg-ohio-power-bar-header-1_1_IPF_qbhfyb.jpg'}]

    return render_template('index.html', title='Home', items=items)


@app.route('/api/items/all', methods=['GET'])
def fetch_all_items():
    return

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        req = request.form
        print(req)
        return render_template('search.html')
    return render_template('search.html')

if __name__ == "__main__":
    app.run(debug=True)
