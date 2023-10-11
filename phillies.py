
#used resource https://scrapeops.io/python-web-scraping-playbook/python-beautifulsoup-findall/
from bs4 import BeautifulSoup
#used resource https://www.w3schools.com/python/module_requests.asp
import requests

# Returns a int version of the salary and if it should be used
def cleanSalary(salary):
    try:
        # check to see if there is a salary and it is correctly formated
        if len(salary)>0 and salary[0]=='$':
            #Get int version of salary
            return [int(salary.replace('$','').replace(',', '')),True]
        else:
            return [0,False]
    except Exception as e:
        print(f"Error processing salary: {e}")
        return [0,False]

# takes in HTML and returns a list of players with salary data and players without salary data
def splitHTML(html):
    soup = BeautifulSoup(html, 'html.parser')

    salaryPlayerList = []
    noSalaryPlayerList = []


    # find the most popular year represented
    years = []
    for row in soup.find_all('tr'):
        year = row.find(class_='player-year').text
        years.append(year)
    majorityYear = max(set(years), key=years.count)

    # Parse HTML for player data
    for row in soup.find_all('tr'):
        name = row.find(class_='player-name').text
        salaryVal,salaryAvailable = cleanSalary(row.find(class_='player-salary').text)
        year = row.find(class_='player-year').text
        level = row.find(class_='player-level').text
        
        # Create player object 
        player = {
            'player-name': name,
            'player-salary': salaryVal,
            'format-player-salary': "$" + '{:,}'.format(salaryVal),
            'player-year': year,
            'player-level': level
        }
        
        # check if salary, level, and year are valid
        if salaryAvailable and level=="MLB" and year==majorityYear:
            salaryPlayerList.append(player)
        else:
            noSalaryPlayerList.append(player)
    return salaryPlayerList,noSalaryPlayerList

def getAverageSalary():
    currentPage  = requests.get("https://questionnaire-148920.appspot.com/swe/data.html")
    players, noDataPlayers = splitHTML(currentPage.content)
    # sort players in ascending order of salaries
    sortedPlayers = sorted(players, key=lambda x: x['player-salary'])
    # create a new list of just the 125 highest salaries
    firstPlayers = sortedPlayers[-125:]
    # create list of just top salaries
    salaries = [player['player-salary'] for player in firstPlayers]
    averageSalary = sum(salaries) / len(salaries)
    # round to 2 decimal points
    averageSalary = round(averageSalary, 2)
    # sdd dollar sign and commas for readability
    averageSalary = "$" + '{:,}'.format(averageSalary)
    firstPlayers.reverse()
    return averageSalary, firstPlayers, noDataPlayers

def getQOHist():
    # make request to MLB website for qualifying data information
    QORaw = requests.get("https://www.mlb.com/news/history-of-mlb-qualifying-offer-decisions-c300602464").content
    soup = BeautifulSoup(QORaw, 'html.parser')
    QOHist = ""
    for row in soup.find_all('div', class_='Styles__StoryPartContainer-sc-1mfrmm0-0 groqnz story-part markdown'):
         # remove class from html
         row['class'] = ""
         nested_div = row.find('div')
         #remove class from html
         nested_div['class']=""
         QOHist += str(row)
    return QOHist