from flask import redirect, request, Flask, render_template, url_for,send_from_directory
import json, requests
import pandas as pd
import joblib
import os

app=Flask(__name__)
app.config['UPLOAD_FOLDER']='./storage'
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hasil', methods=['POST','GET'])
def post():
    model=joblib.load('modeljoblib')

    poke1=request.form['namapokemon1']
    poke2=request.form['namapokemon2']
    poke1=poke1.lower() #nama
    poke2=poke2.lower() #nama

    datapokemon=pd.read_csv('pokemon.csv')
    idpoke1=datapokemon[datapokemon['Name']==poke1.title()]['#'].values[0]
    idpoke2=datapokemon[datapokemon['Name']==poke2.title()]['#'].values[0]

    url1='https://pokeapi.co/api/v2/pokemon/'+poke1
    url2='https://pokeapi.co/api/v2/pokemon/'+poke2
    data1=requests.get(url1)
    data2=requests.get(url2)

    if str(data1)=='<Response [404]>':
        return redirect(url_for('notfound'))
    if str(data2)=='<Response [404]>':
        return redirect(url_for('notfound'))

    gambar1=data1.json()['sprites']['front_default']
    gambar2=data2.json()['sprites']['front_default']

#-------------------------------------------------------- ambil dari pokemon.csv
    dfpoke=pd.read_csv('pokemon.csv',index_col=0)

    hp1=dfpoke.loc[idpoke1]['HP']
    hp2=dfpoke.loc[idpoke2]['HP']
    attack1=dfpoke.loc[idpoke1]['Attack']
    attack2=dfpoke.loc[idpoke2]['Attack']
    defense1=dfpoke.loc[idpoke1]['Defense']
    defense2=dfpoke.loc[idpoke2]['Defense']
    spatk1=dfpoke.loc[idpoke1]['Sp. Atk']
    spatk2=dfpoke.loc[idpoke2]['Sp. Atk']
    spdef1=dfpoke.loc[idpoke1]['Sp. Def']
    spdef2=dfpoke.loc[idpoke2]['Sp. Def']
    speed1=dfpoke.loc[idpoke1]['Speed']
    speed2=dfpoke.loc[idpoke2]['Speed']

    predict=model.predict([[hp1,hp2,attack1,attack2,defense1,defense2,spatk1,spatk2,spdef1,spdef2,speed1,speed2]])[0]
    if predict==0:
        winner=poke1.title()
    else:
        winner=poke2.title()

    proba=model.predict_proba([[hp1,hp2,attack1,attack2,defense1,defense2,spatk1,spatk2,spdef1,spdef2,speed1,speed2]])
    probamax=round(proba[0,predict]*100)
    

    #plot 

    dfhp=pd.DataFrame(dict(nama=[poke1,poke2],hp=[hp1,hp2]))
    dfattack=pd.DataFrame(dict(nama=[poke1,poke2],attack=[attack1,attack2]))
    dfdefense=pd.DataFrame(dict(nama=[poke1,poke2],defense=[defense1,defense2]))
    dfspatk=pd.DataFrame(dict(nama=[poke1,poke2],spatk=[spatk1,spatk2]))
    dfspdef=pd.DataFrame(dict(nama=[poke1,poke2],spdef=[spdef1,spdef2]))
    dfspeed=pd.DataFrame(dict(nama=[poke1,poke2],speed=[speed1,speed2]))

    import matplotlib.pyplot as plt

    plt.figure(figsize=(20,7))
    plt.subplot(161)
    plt.bar(dfhp['nama'],dfhp['hp'],color=['b','g'],alpha=0.5)
    plt.title('HP',fontsize=15)
    plt.xticks(fontsize=15)
   
    plt.subplot(162)
    plt.bar(dfattack['nama'],dfattack['attack'],color=['b','g'],alpha=0.5)
    plt.title('Attack',fontsize=15)
    plt.xticks(fontsize=15)

    plt.subplot(163)
    plt.bar(dfdefense['nama'],dfdefense['defense'],color=['b','g'],alpha=0.5)
    plt.title('Defense',fontsize=15)
    plt.xticks(fontsize=15)
    plt.subplot(164)
    plt.bar(dfspatk['nama'],dfspatk['spatk'],color=['b','g'],alpha=0.5)
    plt.title('Special Attack',fontsize=15)
    plt.xticks(fontsize=15)
    plt.subplot(165)
    plt.bar(dfspdef['nama'],dfspdef['spdef'],color=['b','g'],alpha=0.5)
    plt.title('Special Defense',fontsize=15)
    plt.xticks(fontsize=15)
    plt.subplot(166)
    plt.bar(dfspeed['nama'],dfspeed['speed'],color=['b','g'],alpha=0.5)
    plt.title('Speed',fontsize=15)
    plt.xticks(fontsize=15)
    plt.tight_layout()

    addressplot='./storage/plot'+poke1+poke2+'.png'
    urlplot='http://localhost:5000/fileupload/plot'+poke1+poke2+'.png'
    plt.savefig(addressplot)
    plot=urlplot
    # namafile='plot.png'
    # plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'],namafile))
    return render_template('pokemon.html',nama1=poke1.title(),nama2=poke2.title(),gambar1=gambar1,gambar2=gambar2,winner=winner,proba=probamax,plot=plot)

@app.route('/fileupload/<path:x>')
def hasilUpload(x):
    return send_from_directory('storage',x)

@app.route('/notfound')
def notfound():
    return render_template('error.html')

@app.errorhandler(404)
def notFound404(error):
    return render_template('error.html')

if __name__=='__main__':
    app.run(debug=True)