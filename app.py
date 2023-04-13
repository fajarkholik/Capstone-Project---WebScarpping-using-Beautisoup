from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody')
row_length = len(table.find_all('a', attrs={'class':'n'}))

#row_length = len(___)

#temp = [] #initiating a list 
temp = [(table.find_all('a', attrs={'class':'n'})[i].text, 
         table.find_all('span', attrs={'class':'w'})[i].text.strip())
        for i in range(row_length)]
temp
#for i in range(1, row_length):
#insert the scrapping process here
    
#    temp.append((____,____,____)) 

#temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('Date', 'Kurs'))

#insert data wrangling here
df['Kurs'] = df['Kurs'].str.replace(r'\$|1 =|Rp|,', '', regex=True)
df = df.astype({'Date': 'datetime64[ns]', 'Kurs': 'float'})
df = df.set_index('Date')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["Kurs"].mean().round(2)}' #be careful with the " and '

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)