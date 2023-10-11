from phillies import splitHTML,getAverageSalary, getQOHist
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/current-team")
def current_team():
    averageSalary,playersWithData, playersNoData = getAverageSalary()
    return render_template('curTeam.html',averageSalary = averageSalary, players= playersWithData, playersNoData=playersNoData)
@app.route("/future-team")
def future_team():
    averageSalary,playersWithData, playersNoData = getAverageSalary()
    return render_template('futureTeam.html',averageSalary = averageSalary, players= playersWithData, playersNoData=playersNoData)

@app.route("/compare", methods=["POST"])
def compare():
    formData = request.form
    if request.form["posPlayerName1"] and request.form["posPlayerName2"]:
        return render_template('comparePos.html', formData = formData)
    if request.form["pitName1"] and request.form["pitName2"]:
        return render_template('comparePit.html', formData = formData)
    return render_template('cannotCompare.html')
@app.route("/")
def home():
    return render_template('home.html', QOHist = getQOHist())
