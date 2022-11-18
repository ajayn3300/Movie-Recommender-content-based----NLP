from flask import Flask,render_template,url_for,request
import pickle
import pandas as pd


#movies dataset
data=pd.read_csv('movies.csv',lineterminator="\n")

# movies similarity dataset
corr=pd.read_csv('corr.csv',lineterminator='\n')

#we have got one extra column in our dataset which is nothing but indices let's remove that:
corr.drop(columns=['Unnamed: 0'],inplace=True)
corr.columns=corr.index


#same with data
data.set_index(data['Unnamed: 0'],inplace=True,drop=True)


app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend',methods=['GET','POST'])
def recommend():
    movie_name=str(request.form['movies']).strip()

      # get index first
    indexed=data[data['Title']==movie_name].index[0]

  # get top 10 movies
    top_10=list(corr.loc[:,indexed].sort_values(ascending=False)[1:11].index)
    posters=dict()
    # saving posters name as key and poster's link as value 
    for i in top_10:
        posters[data.iloc[i,:].Title]=data.iloc[i,:]['Poster_Url\r']
    
    return render_template('index.html',op=posters.items())

if __name__=="__main__":
    app.run(debug=True)