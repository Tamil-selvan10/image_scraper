import os
from flask import Flask, request, render_template,url_for
import requests
from bs4 import BeautifulSoup
import logging
import pymongo
import os
logging.basicConfig(level=logging.INFO,
                    filename='scrapper.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%B-%Y %H:%M:%S')


application = Flask(__name__)

app=application

@app.route('/',methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/review',methods=['POST'])
def review():

    if request.method == 'POST':

        try:
            # query to search for images
            query = request.form['content'].replace(" ", "")
            
            # directory to store downloaded images
            save_dir = 'images/'

            # create the directory if it doesn't exist
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # fetch the search results page
            response = requests.get(f'https://www.google.com/search?rlz=1C1VDKB_enIN1053IN1053&sxsrf=AB5stBi7e7A2QOPCMR08P9HaH2CDUWvUXQ:1691025478172&q={query}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwjczbrnqL-AAxX-xjgGHW1JDAIQ0pQJegQIDBAB&biw=1366&bih=619')

            # parse the html using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # find all image tags
            image_tags = soup.find_all('img')

            del image_tags[0]
            
            img_data=list()

            for index, image_tag in enumerate(image_tags):
                 # get image url from the src tag
                image_url = image_tag.get('src')
                image_data = requests.get(image_url).content
                filename = f'{query}_{index}.jpg'
                filepath = os.path.join(save_dir, filename)

                my_dict={'Index':index,'Image':image_data}
                img_data.append(my_dict)

                with open(filepath, 'wb') as f:
                   f.write(image_data)

            client=pymongo.MongoClient('mongodb+srv://etamilselvan2710111996:Valliammal11@cluster0.sgeazoo.mongodb.net/?retryWrites=true&w=majority')
            db=client['img_scrap_db']
            review_col=db['img_scrap_collection']
            review_col.insert_many(img_data)

            return 'image loaded'

        except Exception as e:
            logging.info(e)
            return 'something is wrong'


    else:
      return render_template('index.html')
    

if __name__=='__main__':
    #app.run(host='0.0.0.0',port=8000)
    print('72')
    app.run(debug=True)
