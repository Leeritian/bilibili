from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import danmu

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY']='xxx'

class BiliForm(Form):
    av = StringField('',validators=[Required()])
   
    submit = SubmitField()


@app.route('/')
def index(username=None):
    username=username
    strr = '<h1>New Life</h1>'
    return render_template('index.html', username=username)



@app.route('/bilibili', methods=['GET','POST'])
def b_crawl():
    if request.method == 'POST':
        av = request.form['av']
        try:
            int(av)
        except ValueError:
            return render_template('bilibili.html',content='fuck you it`s not a number')    
        bilidanmu=danmu.danmu_spider(str(av))
        if bilidanmu.exist:
            image = bilidanmu.coverImg()
            content = bilidanmu.show_top()
            title=bilidanmu.title
            return render_template('bilibili.html',image=image,av=av,content=content,title=title)
        else:
            return render_template('bilibili.html',av=av,error='fuck you it`s not exist')
    return render_template('bilibili.html')

@app.route('/rank',methods=['GET','POST'])
def rank():
    if request.method == 'POST':
        av = request.form['av']
        bd=danmu.danmu_spider(str(av))
        if bd.exist:
            ranks = bd.getData()
        return render_template('rank.html',rank=ranks)
    else:
        return render_template('rank.html')

if __name__ == '__main__':
    app.run()
