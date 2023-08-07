from urllib.request import urlopen
from bs4 import BeautifulSoup as bs 
import os 
from flask import Flask,request,render_template
import requests
import logging
import pymongo

logging.basicConfig(filename='image_scrapper_logger.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')
app=Flask(__name__)

@app.route('/',methods=['GET'])
def homepage():
    return render_template('index.html')
logging.info(msg='Home page rendered')
   
@app.route('/review',methods=['POST'])
def main_function():
    if request.method=='POST':
        query=request.form['content']
        final_query=query.replace('',' ')
        logging.info('search querry recieved')
        image_url=f'https://www.google.com/search?q={final_query}&tbm=isch&ved=2ahUKEwj5oOaokMaAAxW66DgGHQyVAkgQ2-cCegQIABAA&oq=elonmusk&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BwgAEIoFEEM6BAgjECc6BggAEAcQHjoICAAQBRAHEB46BwgAEBgQgAQ6CQgAEBgQgAQQClDgmWBY5rlgYK69YGgCcAB4AIABzAGIAfAKkgEFMC45LjGYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=HpLOZPmZHbrR4-EPjKqKwAQ&bih=754&biw=1482'
        image_page_html=bs(requests.get(image_url).text,'html.parser')
        images=image_page_html.find_all('img')
        del images[0]
        image_sources=[]
        for image in images:
            image_sources.append(image['src'])
        os.makedirs(f'{query}_images')
        logging.info('Directory for saving the images have been created')
        client=pymongo.MongoClient('mongodb+srv://yugpratapsingh:313ycd014916@cluster0.25gtiu5.mongodb.net/?retryWrites=true&w=majority')
        db=client['image_scrapping_database']
        collec=db[f'Images of {query}']
        for n,i in enumerate(image_sources): # This will store all the images in local directory
            with open(f'{query}_images/image_{n}.jpg','wb') as f:
                f.write(urlopen(i).read())
                f.close()
            data={'image name':f'{query} image_{n}',
                 'image_data_binary':urlopen(i).read()}
            collec.insert_one(data)
        
        logging.info('Images have been saved to the local directory')
    return 'All Images have been saved in your local directory'

if __name__=='__main__':
    app.run(host='0.0.0.0',port=7000)