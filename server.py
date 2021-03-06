import json
from flask import Flask, redirect, url_for
from flask import render_template
from flask import Response, request, jsonify
import random
app = Flask(__name__)

# Collection of Databases for Learning
learn_skates_db = [
	{
		"name": "Edges",
		"description": "The inside edges are toward the big toe, and the outside edges are toward the pinky toe. Which edge a skater puts his weight on going into a jump is what distinguishes one jump from another.",
		"img": "https://images.squarespace-cdn.com/content/v1/5a086441914e6b339a5f2b21/1542250387886-Q6SQ1LY3GRCAOE6IKNVE/edge.JPG?format=750w"
	},
	{
		"name": "Toe Pick",
		"description": "The toe pick is a little set of jagged teeth at the front of the blade that helps skaters stab into the ice to push upward and launch themselves into the air.",
		"img": "https://bigthink.com/wp-content/uploads/2018/02/18411162.jpg?fit=1200,675"
	}
]


learn_jump_types_db = [
	{
		"name": "Toe Jump",
		"description": "In toe jumps, the skater plants the toe-pick of their free leg and uses it to help launch them into the air. You'll see a skater kick the front of their blade into the ice before a toe jump.",
		"gif": "https://cdn.theatlantic.com/thumbor/8ws46t__LGCg_jT6sj5sh8-KMvo=/media/img/posts/2014/02/gracielutz/original.gif"
	},
	{
		"name": "Edge Jump",
		"description": "In edge jumps, the skater essentially just uses a knee bend to launch.",
		"gif": "https://cdn.theatlantic.com/thumbor/7b2331oQuSNtccoFpvWhUBRBLPU=/media/img/posts/2014/02/2014_02_04_15_51_39/original.gif"
	}	
]

learn_toe_jumps_db = [
	{
		"name": "Toe Loop",
        "description": "As seen in the above GIF of Spanish skater Javier Fernández, the jump begins with the skater approaching the jump backward on the outside edge of one foot, then landing the jump on the outside edge of the same foot.",
        "img": "https://skatesweden.se/wp-content/uploads/2017/11/Toe-Loop-930x280.jpg",
        "gif": "https://cdn.theatlantic.com/thumbor/9h7A-k5S7N2ob4l8XGnP0sdWJSg=/media/img/posts/2014/02/toe_loop/original.gif",
	},
	{
		"name": "Flip",
        "description": "As seen in the GIF above of Russian skater Alina Zagitova, the flip starts on the inside edge of one foot while the skater approaches the jump backward and uses the toe pick of her other foot to take off, and ends with the skater landing on the outside edge of the opposite foot.",
        "img": "https://skatesweden.se/wp-content/uploads/2017/11/Flip-930x280.jpg",
        "gif": "https://cdn.theatlantic.com/thumbor/E1d4g-zCWjpR294Rr4676MujLno=/media/img/posts/2014/02/kimtripleflip/original.gif",
	},
	{
		"name": "Lutz",
        "description": "The lutz, a toe jump, is a lot like the flip. But instead of approaching the jump on an inside edge, it requires skaters to take off from the outside edge of one foot and then land, as they would with a flip, on the outside edge of their opposite foot. Note, in the GIF above, how American skater Nathan Chen leans into the outside edge of his left foot as he extends his right leg and toe pick behind him to launch himself into the air.",
        "img": "https://skatesweden.se/wp-content/uploads/2017/11/Lutz-930x280.jpg",
        "gif": "https://cdn.theatlantic.com/thumbor/iFO_pvUSlqklv_2vei29El3o7JI=/media/img/posts/2014/02/yuna_lutz/original.gif",
	}
]

learn_edge_jumps_db = [
	{
		"name": "Salchow",
        "description": "If you’re looking to better understand the difference between an edge jump and a toe jump, the salchow is one of the jumps that makes it easiest to spot. The salchow doesn’t use a toe pick, and you can clearly see the skater launch himself from the knee bend. It starts from the inside edge of one foot and ends on the outside edge of the opposite foot.",
        "img": "https://skatesweden.se/wp-content/uploads/2017/11/Salchow-930x280.jpg",
        "gif": "https://cdn.theatlantic.com/thumbor/JmGnjavDtfgqxsk5T3tGa63FhWc=/media/img/posts/2014/02/salchoww/original.gif",
	},
	{
		"name": "Loop",
        "description": "The loop is another edge jump. Though it’s executed differently from the toe loop (which I’ll explain below), it shares the same entry and landing as the toe loop — approaching the jump backward on the outside edge of one foot, then landing the jump on the outside edge of the same foot — minus the toe pick. You can see this in the above GIF, where American skater Nathan Chen performs a triple loop.",
        "img": "https://skatesweden.se/wp-content/uploads/2017/11/Skatesweden_ogel_loop1-1280x417-930x280.jpg",
        "gif": "https://cdn.theatlantic.com/thumbor/bkOBNDHWinZtb3xCrMoF_PHWNj4=/media/img/posts/2014/02/loop/original.gif",
	},
	{
		"name": "Axel",
        "description": "The axel is the easiest jump to spot and arguably the hardest to execute. It is the only jump where the skater takes off while facing forward. “The skater needs an extra half rotation to land gliding backward,” Morgan explained, due to that front-facing takeoff. “The extra half rotation is notable because it’s much more difficult to create rotation when taking off from a forward edge.” You can see that extra half rotation in the GIF above, as Korean skater Yuna Kim leaps off the ice and swings her right leg around to vault herself off the ice and then does two full rotations in the air to complete a double axel.",
        "img": "https://skatesweden.se/wp-content/uploads/2017/11/image24-930x280.jpg",
        "gif": "https://cdn.theatlantic.com/thumbor/1oBHvMp0uHTRYTOI8XKcN55QueQ=/media/img/posts/2014/02/axel/original.gif",
	}
]

welcome_db = [

]

final_db = {
	"score": 0.0
}

quiz_edge_jumps_db = [
{
	"options": ["Axel", "Salchow", "Loop"]
},
{
	"correct_answer": "Axel",
	"gif": "https://cdn.vox-cdn.com/thumbor/K9LwhT7m7po13sFf8xnOFANAc1g=/1400x0/filters:no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/10100141/2018_01_25_21_51_46.gif",
	"numAttempts": 0,
	"correct": 0
},
{
	"correct_answer": "Salchow",
	"gif": "https://cdn.vox-cdn.com/thumbor/17uuaevDvRt6iBUu9_EuyDyhfxc=/1400x0/filters:no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/10100567/2018_01_25_22_35_51.gif",
	"numAttempts": 0,
	"correct": 0
},
{
	"correct_answer": "Loop",
	"gif": "https://cdn.vox-cdn.com/thumbor/jdRRKcOZaKFxJt4EvAMIpQQM_r4=/1400x0/filters:no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/10104007/2018_01_26_13_04_23.gif",
	"numAttempts": 0,
	"correct": 0
}
]

quiz_toe_jumps_db = [
{
	"options": ["Toe Loop", "Flip", "Lutz"]
},
{
	"correct_answer": "Toe Loop",
	"gif": "https://cdn.vox-cdn.com/thumbor/QLlcMAq1TEpn9jc1jZYs6JclP4Q=/1400x0/filters:no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/10100903/2018_01_25_23_11_49.gif",
	"numAttempts": 0,
	"correct": 0
},
{
	"correct_answer": "Flip",
	"gif": "https://cdn.vox-cdn.com/thumbor/JpgaaL69exCU2uC_pL14gMYDG_w=/1400x0/filters:no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/10105599/2018_01_26_14_09_56.gif",
	"numAttempts": 0,
	"correct": 0
},
{
	"correct_answer": "Lutz",
	"gif": "https://cdn.vox-cdn.com/thumbor/QDbxxgTVtOpZzISQwq3l6TI8CB4=/1400x0/filters:no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/10100055/2018_01_25_21_30_48.gif",
	"numAttempts": 0,
	"correct": 0
}

]

quiz_jump_types_db = [
{
	"options": ["Edge Jump", "Toe Jump"]
},
{
	"correct_answer": "Toe Jump",
	"gif": "https://cdn.vox-cdn.com/thumbor/QLlcMAq1TEpn9jc1jZYs6JclP4Q=/1400x0/filters:no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/10100903/2018_01_25_23_11_49.gif",
	"numAttempts": 1,
	"correct": 0
},
{
	"correct_answer": "Edge Jump",
	"gif": "https://cdn.vox-cdn.com/thumbor/17uuaevDvRt6iBUu9_EuyDyhfxc=/1400x0/filters:no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/10100567/2018_01_25_22_35_51.gif",
	"numAttempts": 1,
	"correct": 0
},
{
	"correct_answer": "Toe Jump",
	"gif": "https://cdn.vox-cdn.com/thumbor/JpgaaL69exCU2uC_pL14gMYDG_w=/1400x0/filters:no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/10105599/2018_01_26_14_09_56.gif",
	"numAttempts": 1,
	"correct": 0
},
{
	"correct_answer": "Edge Jump",
	"gif": "https://cdn.vox-cdn.com/thumbor/jdRRKcOZaKFxJt4EvAMIpQQM_r4=/1400x0/filters:no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/10104007/2018_01_26_13_04_23.gif",
	"numAttempts": 0,
	"correct": 0
}
]

score_db = {
	
}

def compute_score():
	global quiz_jump_types_db
	global quiz_toe_jumps_db
	global quiz_edge_jumps_db

	score = 0
	for db in [quiz_jump_types_db, quiz_toe_jumps_db, quiz_edge_jumps_db]:
		for idx in range(1, len(db)):
			if db[idx]["correct"] == 1:
				score += 1
	print("Score: " + str(score))
	return score

def results_table():
	global quiz_jump_types_db
	global quiz_toe_jumps_db
	global quiz_edge_jumps_db

	results = {}

	#Jump Types
	for i in range(1, 3):
		if quiz_jump_types_db[i]["correct"] == 1:	
			results[quiz_jump_types_db[i]["correct_answer"]] = "✓"
		else:
			results[quiz_jump_types_db[i]["correct_answer"]] = "✗"
	for i in range(3, 5):
		if quiz_jump_types_db[i]["correct"] == 1:	
			results[quiz_jump_types_db[i]["correct_answer"]] += "✓"
		else:
			results[quiz_jump_types_db[i]["correct_answer"]] += "✗"
	# Toe Jumps
	for i in range(1, len(quiz_toe_jumps_db)):
		if quiz_toe_jumps_db[i]["correct"] == 1:	
			results[quiz_toe_jumps_db[i]["correct_answer"]] = "✓"
		else:
			results[quiz_toe_jumps_db[i]["correct_answer"]] = "✗"
	# Edge Jumps
	for i in range(1, len(quiz_edge_jumps_db)):
		if quiz_edge_jumps_db[i]["correct"] == 1:	
			results[quiz_edge_jumps_db[i]["correct_answer"]] = "✓"
		else:
			results[quiz_edge_jumps_db[i]["correct_answer"]] = "✗"
	
	return results

# Temporarily deprecated
def identify_areas_of_difficulty():
	global quiz_jump_types_db
	global quiz_toe_jumps_db
	global quiz_edge_jumps_db

	# Jump types
	for i in range(1, len(quiz_jump_types_db)):
		if quiz_jump_types_db[i]["correct"] == 0:
			return "Jump Types."
	# Toe Jumps
	for i in range(1, len(quiz_toe_jumps_db)):
		if quiz_toe_jumps_db[i]["correct"] == 0:
			return "Toe Jumps."
	# Edge Jumps
	for i in range(1, len(quiz_edge_jumps_db)):
		if quiz_edge_jumps_db[i]["correct"] == 0:
			return "Edge Jumps."
	
	return "Nothing (Congragulations on a Perfect Score)!"

def clear_score():
	global quiz_jump_types_db
	global quiz_toe_jumps_db
	global quiz_edge_jumps_db

	for db in [quiz_jump_types_db, quiz_toe_jumps_db, quiz_edge_jumps_db]:
		for idx in range(1, len(db)):
			db[idx]["correct"] = 0

# ROUTES
@app.route('/')
def welcome():
	global welcome_db

	clear_score()

	data = {}
	data['src'] = welcome_db
	data['title'] = "Identifying Figure Skating Jumps"
	data['prev'] = "/"
	data['next'] = "/learn_skates"

	return render_template('welcome.html', data=data)


@app.route('/final')
def final():
	global final_db

	score = compute_score()
	area = identify_areas_of_difficulty()
	results = results_table()

	data = {}
	data['score'] = score
	data['area of difficulty'] = area
	data['results'] = results
	data['src'] = final_db
	data['title'] = "Course Ended"
	data['prev'] = "quiz_edge_jumps"
	data['restart'] = "/"

	return render_template('final.html', data=data)

@app.route('/learn_skates')
def learn_skates():
	global learn_skates_db

	data= {}
	data['src'] = learn_skates_db
	data['title'] = "Skate Basics"
	data['prev'] = "/"
	data['next'] = "/learn_jump_types"

	return render_template('learn_v1.html', data=data)

@app.route('/learn_jump_types')
def learn_jump_types():
	global learn_jump_types_db

	data = {}
	data['src'] = learn_jump_types_db
	data['title'] = "Jump Types"
	data['prev'] = "/learn_skates"
	data['next'] = "/quiz_jump_types"

	return render_template('learn_v1.html', data=data)

@app.route('/learn_toe_jumps')
def learn_toe_jumps():
	global learn_toe_jumps_db

	data = {}
	data['src'] = learn_toe_jumps_db
	data['title'] = "Toe Jumps"
	data['prev'] = "/quiz_jump_types"
	data['next'] = "/quiz_toe_jumps"

	return render_template('learn_v2.html', data=data)

@app.route('/learn_edge_jumps')
def learn_edge_jumps():
	global learn_edge_jumps_db
	
	data = {}
	data['src'] = learn_edge_jumps_db
	data['title'] = "Edge Jumps"
	data['prev'] = "/quiz_toe_jumps"
	data['next'] = "/quiz_edge_jumps"

	return render_template('learn_v2.html', data=data)

@app.route('/quiz_edge_jumps')
def quiz_edge_jumps():
	global quiz_edge_jumps_db
	global final_db
	
	data = {}
	data['src'] = quiz_edge_jumps_db
	data['title'] = "Edge Jumps Quiz"
	data['prev'] = "/learn_edge_jumps"
	data['next'] = "/final"

	return render_template('quiz_v2.html', data=data)

@app.route('/quiz_toe_jumps')
def quiz_toe_jumps():
	global quiz_toe_jumps_db
	
	data = {}
	data['src'] = quiz_toe_jumps_db
	data['title'] = "Toe Jumps Quiz"
	data['prev'] = "/learn_toe_jumps"
	data['next'] = "/learn_edge_jumps"

	return render_template('quiz_v2.html', data=data)

@app.route('/quiz_jump_types')
def quiz_jump_types():
	global quiz_jump_types_db

	data = {}
	data['src'] = quiz_jump_types_db
	data['title'] = "Jump Types Quiz"
	data['prev'] = "/learn_jump_types"
	data['next'] = "/learn_toe_jumps"

	return render_template('quiz_v1.html', data=data)

@app.route('/update_correctness', methods=['GET', 'POST'])
def update_correctness():
	global quiz_jump_types_db
	global quiz_toe_jumps_db
	global quiz_edge_jumps_db

	index = int(str(request.get_json()['index'])[-1]) # TEMP SOLUTION COME BACK TO THIS
	db_name = request.get_json()['db']
	correct = int(request.get_json()['correct'])

	if db_name == "Jump Types Quiz":
		quiz_jump_types_db[index]["correct"] = correct
	elif db_name == "Toe Jumps Quiz":
		quiz_toe_jumps_db[index]["correct"] = correct
	elif db_name == "Edge Jumps Quiz":
		quiz_edge_jumps_db[index]["correct"] = correct
	else:
		print("An error has occurred.")

	return jsonify(data=None) # no need to return anything

## Everything below is for reference only

@app.route('/add')
def add():
	return render_template('add_entry.html')

def getAuthors(s):
	return s
	res =  s.split(',')
	res = [x.strip() for x in res]
	return res

@app.route('/create', methods=['GET','POST'])
def create():
	global data
	global LAST_ID
	
	LAST_ID += 1
	json_data = request.get_json()
	newEntry = { 
		"id": str(LAST_ID),
		"title":  json_data["paperTitle"],
		"authors": getAuthors(json_data["paperAuthors"]),
		"conference": json_data["paperConference"],
		"year": int(json_data["paperYear"]),
		"url": json_data["paperURL"],
		"abstract": json_data["paperAbstract"]
	}
	
	data[str(LAST_ID)] = newEntry
	
	res ={
		"newItem": "/view/%s" %(str(LAST_ID))
	}
	return jsonify(res=res)

@app.route('/search', methods=['GET','POST'])
def search():
	global data
	
	json_data = request.get_json()
	searchParam_ = str(json_data['key'])
	searchParam = str(json_data['key']).lower()

	res = []
	for k in data.keys():
		candidate = data[k]
		if searchParam in data[k]['title'].lower():
			res.append(candidate)
		elif searchParam.strip() in data[k]['authors'].lower():
			res.append(candidate)
		elif searchParam in data[k]['conference'].lower():
			res.append(candidate)
		elif searchParam.isnumeric() and int(searchParam)==data[k]['year']:
			res.append(candidate)

	res = {
		"res": res,
		"searchTerm": searchParam_
	}
	return jsonify(res=res)

@app.route('/view/<id>')
def view(id):
    global data
    return render_template("view.html", data=data[str(id)])

@app.route('/edit/<id>',  methods=['GET','POST'])
def edit(id):
	global data
	if request.method == 'GET':
		t = ', '.join(data[str(id)]['authors']).strip()
		data[str(id)]["authorsString"] = t
		return render_template("edit.html", data=data[str(id)])
		# return redirect()
	elif request.method == 'POST':
		json_data = request.get_json()
		data[json_data['id']] = json_data
		newRe = "view/" +  str(json_data['id'])
		res = {
			"out": json_data['id']
		}
		return jsonify(res=res)
		return render_template('add_entry.html') # render_template("view.html", data=data[str(id)])


if __name__ == '__main__':
    app.run(debug = True, port=5000)



