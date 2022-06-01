from flask import Flask,render_template

app = Flask(__name__) 

blogPosts=[
    {
        'author':'Me',
        'title':'Post 1',
        'content':'Hi !',
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
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