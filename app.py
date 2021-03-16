from flask import Flask, jsonify, request, render_template
from util.db_handler import DbHandler
app = Flask(__name__)
DbHandler = DbHandler() 

items = [{"name" : "Rogue 45LB Ohio Power Bar - Bare Steel", 'manufacturer':'Rogue', "price" : 450, "Stock" : False, "url" : "https://www.rogueaustralia.com.au/rogue-ohio-power-bar-45-lb-bare-steel-au", "img_url" : "https://assets.roguefitness.com/f_auto,q_auto,h_400,b_rgb:f8f8f8/catalog/Weightlifting%20Bars%20and%20Plates/Barbells/Mens%2020KG%20Barbells/AU-RA0586-RWRW/AU-RA0586-RWRW-h_izz6x3.png" },
         {"name" : "Rogue TB-2 Trap Bar", 'manufacturer':'Rogue', "price" : 618, "Stock" : True, "url" : "https://www.rogueaustralia.com.au/rogue-tb-2-trap-bar-au", "img_url" : "https://assets.roguefitness.com/f_auto,q_auto,h_400,b_rgb:f8f8f8/catalog/Weightlifting%20Bars%20and%20Plates/Barbells/Specialty%20Barbells/AU-RA0711/AU-RA0711-h_zvzjbv.png"},
         {"name" : "Rogue Combo Rack", 'manufacturer':'Rogue', "price" : 4420, "Stock" : False, "url" : "https://www.rogueaustralia.com.au/rogue-combo-rack-au", "img_url" : "https://assets.roguefitness.com/f_auto,q_auto,h_400,b_rgb:f8f8f8/catalog/Rigs%20and%20Racks/Squat%20Stands/Monster%20Lite%20Squat%20Stands/AU-RA1736-BLACK-MG/AU-RA1736-BLACK-MG-h_pyflph.png" }, 
         {"name" : "Thompson Fat Pad™", 'manufacturer':'Rogue', "price" : 288, "Stock" : False, "url" : "https://www.rogueaustralia.com.au/thompson-fatpad-au", "img_url" : "https://assets.roguefitness.com/f_auto,q_auto,h_400,b_rgb:f8f8f8/catalog/Strength%20Equipment/Strength%20Training/Weight%20Benches/AU-PAD027/AU-PAD027-H_u2agme.png" },
         {'name': 'Rogue Ohio Deadlift Bar - Black Zinc', 'manufacturer':'Rogue', 'price': 550, 'stock': False, 'url': 'https://www.rogueaustralia.com.au/rogue-ohio-deadlift-bar-black-zinc-au', 'img_url': 'https://assets.roguefitness.com/f_auto,q_auto,h_400,b_rgb:f8f8f8/catalog/Weightlifting%20Bars%20and%20Plates/Barbells/Mens%2020KG%20Barbells/AU-RA0963-BLBR/AU-RA0963-BLBR-h_t4opya.png'},
         {'name': 'Rogue 20KG Ohio Power Bar - Stainless Steel', 'manufacturer':'Rogue','price': 680, 'stock': True, 'url': 'https://www.rogueaustralia.com.au/rogue-20-kg-ohio-power-bar-stainless-steel-au', 'img_url':'https://assets.roguefitness.com/f_auto,q_auto,h_400,b_rgb:f8f8f8/catalog/Weightlifting%20Bars%20and%20Plates/Barbells/Mens%2020KG%20Barbells/RA0692-SSDC/20kg-ohio-power-bar-header-1_1_IPF_qbhfyb.jpg'},
         {'name': 'ATX Buffalo Olympic Bar', 'manufacturer':'ATX', 'price': 560, 'stock': False, 'url':'https://samsfitness.com.au/barbells/specialty-olympic-bars/buffalo-squat-bar', 'img_url':'https://samsfitness.com.au/image/cache/catalog/ATX-LH-BUFFALO/atx-buffalo-bar-800x800.jpg'}]

changes = [{"item_name" : "Rogue 45LB Ohio Power Bar - Bare Steel", 'restock': True, 'time': '7:15PM', 'date': '13/03/2021'},
           {"item_name" : "Rogue Ohio Deadlift Bar - Black Zinc", 'restock': False, 'time': '8:33AM', 'date': '15/03/2021'},
           {"item_name" : "Rogue 20KG Ohio Power Bar - Stainless Steel", 'restock': True, 'time': '4:45PM', 'date': '12/03/2021'},
           {"item_name" : "ATX Buffalo Olympic Bar", 'restock': True, 'time': '9:14AM', 'date': '11/03/2021'},
           {"item_name" : "Rogue Combo Rack", 'restock': False, 'time': '11:33AM', 'date': '10/03/2021'}]
 
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='Home', items=items[:2])


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
        query = req.get('search')
        query_result = parse_query(query, items)
        return render_template('search_results.html', items=query_result, query=query)
    return render_template('search.html')

def parse_query(query, items):
    queries = query.split()
    result = []
    for item in items:
        for q in queries:
            if q in item['name'].lower().split():
                result.append(item)
    return result

# @app.route('/items')
    # req = request.form


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', number=len(items), changes = changes)

if __name__ == "__main__":
    app.run(debug=True)
