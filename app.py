from flask import Flask,render_template,url_for

app = Flask(__name__) 

blogPosts=[
    {
        'author':'Me',
        'title':'Post 1',
        'content':'Hi !',
        'date':'June 5,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },

    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
]

@app.route('/') 
@app.route('/home')
def home(): 
    return render_template('home.html',posts=blogPosts)

@app.route('/about') 
def about(): 
    return render_template('about.html',newTitle='About')


if __name__=="__main__": 
    app.run(debug=True)