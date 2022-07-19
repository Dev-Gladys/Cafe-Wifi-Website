from flask import Flask, render_template, redirect,url_for,jsonify,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,BooleanField,IntegerField
from wtforms.validators import DataRequired,URL
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)

#Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean)
    has_wifi = db.Column(db.Boolean)
    has_sockets = db.Column(db.Boolean)
    can_take_calls = db.Column(db.Boolean)
    coffee_price = db.Column(db.String(250), nullable=True)
#db.create_all()




class CafeForm(FlaskForm):
    id=IntegerField('ID', validators=[DataRequired()])
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[DataRequired(), URL(require_tld=True)])
    image_url = StringField('Image URL', validators=[DataRequired(), URL(require_tld=True)])
    location = StringField('Location', validators=[DataRequired()])
    has_toilet = BooleanField('Has Toilets', validators=[DataRequired()])
    has_socket = BooleanField('Has Sockets', validators=[DataRequired()])
    has_wifi= BooleanField('Has Wifi', validators=[DataRequired()])
    can_take_calls = BooleanField('Can Take Calls?', validators=[DataRequired()])
    seats =StringField('Number of Seats e.g 20-30', validators=[DataRequired()])
    coffee_price =StringField('Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index_cafe.html")

@app.route("/cafes")
def cafes():
    cafes = Cafe.query.all()
    return render_template("cafes.html", cafes=cafes)

@app.route('/add' , methods=["GET","POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
                id=form.id.data,
                name=form.name.data,
                map_url=form.map_url.data,
                img_url=form.image_url.data,
                location=form.location.data,
                has_toilet=form.has_toilet.data,
                has_sockets = form.has_socket.data,
                has_wifi=form.has_wifi.data,
                can_take_calls = form.can_take_calls.data,
                seats=form.seats.data,
                coffee_price=form.coffee_price.data,
            )
        db.session.add(new_cafe)
        db.session.commit()

    return render_template('add_cafe.html', form=form)


@app.route("/delete/<int:id>")
def delete(id):
    to_delete = Cafe.query.filter_by(id=id).first()
    db.session.delete(to_delete)
    db.session.commit()
    return redirect(url_for("cafes"))


if __name__=="__main__":
    app.run(debug=True)