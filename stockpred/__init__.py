from flask import Flask, render_template


app=Flask(__name__)
app.config['SECRET_KEY'] = '2b8c674fd1815cb4c61fb207'
app.add_url_rule('/source/<filename>', endpoint='source', view_func=app.send_static_file)


from stockpred import route