from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def extract_table_data(table):
    data = {}
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) == 2:
            key = columns[0].get_text(strip=True)
            value = columns[1].get_text(strip=True)
            data[key] = value
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    num = None
    table_data_list = []

    if request.method == 'POST':
        num = request.form.get('num')
        url = 'https://paksiminfo.com/sim/search-result.php'
        api = 'https://paksiminfo.com/sim/search-result.php'
        key = '2b5b:1e49:8d01:c2ac:fffd:833e:dfee:13a4:5be8:dde9:7f0b:d5a7:bd01:b3be:9c69:573b:5be8:dde9:7f0b:d5a7:bd01:b3be:9c69:573b:5be8:dde9:7f0b:d5a7:bd01:b3be:9c69:573b'
        security = 'PA'
        urL = api + '?num=' + num + '&key=' + key + '&security=' + security
        
        data = {'num': num}
        response = requests.post(url, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table', class_='tg')

        for table in tables:
            table_data = extract_table_data(table)
            table_data_list.append(table_data)

    return render_template('index.html', num=num, table_list=table_data_list)

if __name__ == '__main__':
    app.run(debug=True)
