from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,RadioField,IntegerField
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

bcrypt = Bcrypt()


db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/MURAT/OneDrive/Masaüstü/KombinFlask/dolap.db"

db = SQLAlchemy(app)

app.secret_key="kombin"



class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    email = db.Column(db.String)
class dolap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sahip=db.Column(db.String)
    isim = db.Column(db.String)
    marka = db.Column(db.String)
    renk = db.Column(db.String)
    kategori=db.Column(db.String)

class LoginForm(Form):
    username=StringField("Kullanıcı Adı:")
    password=PasswordField("Parola:")

class verifyForm(Form):
    code=StringField("Gönderilen Kod:")

class dereceform(Form):
    derece=IntegerField("Bölgendeki tahmini hava sıcaklığı nedir ?")

class elbiseform(Form):
    isim=StringField("İsim :")
    renk=StringField("Renk :")
    marka=StringField("Marka :")
    kategori=option = RadioField('Kategori: ', choices=[('yazust', 'Yaz Üst'), ('yazelbise', 'Yaz Elbise'), ('yazayakkabi', 'Yaz Ayakkabi'), ('mont', 'Mont'), ('kisbirincilust', 'Kış Birincil Üst'), ('kisikincilust', 'Kış İkincil Üst'), ('kisayakkabi', 'Kış Ayakkabi'), ('altgiyim', 'Alt Giyim'), ('aksesuar', 'Aksesuar')])

class registerform(Form):
    username= StringField("Kullanıcı Adı:",validators=[validators.Length(min=5,max=14)])
    email= StringField("Mail Adresi:",validators=[validators.Email(message="Gecerli bir mail adresi giriniz:")])
    password= PasswordField("Parola",validators=[
        validators.DataRequired("Lutfen bir parola giriniz:")])

class passchange(Form):
    newpass=PasswordField("Yeni Parola:")
    newpassconfirm=PasswordField("Parola Tekrar:")

class yazust(Form):
    isim=StringField("Elbise Adı:",validators=[validators.length(min=5,max=100)])
    marka=TextAreaField("İcerik:",validators=[validators.length(min=20)])
    renk=TextAreaField("İcerik:",validators=[validators.length(min=20)])

class yazelbise(Form):
    isim=StringField("Elbise Adı:",validators=[validators.length(min=5,max=100)])
    marka=TextAreaField("İcerik:",validators=[validators.length(min=20)])
    renk=TextAreaField("İcerik:",validators=[validators.length(min=20)])

class yazayakkabi(Form):
    isim=StringField("Elbise Adı:",validators=[validators.length(min=5,max=100)])
    marka=TextAreaField("İcerik:",validators=[validators.length(min=20)])
    renk=TextAreaField("İcerik:",validators=[validators.length(min=20)])

class mont(Form):
    isim=StringField("Elbise Adı:",validators=[validators.length(min=5,max=100)])
    marka=TextAreaField("İcerik:",validators=[validators.length(min=20)])
    renk=TextAreaField("İcerik:",validators=[validators.length(min=20)])

class kisikincilust(Form):
    isim=StringField("Elbise Adı:",validators=[validators.length(min=5,max=100)])
    marka=TextAreaField("İcerik:",validators=[validators.length(min=20)])
    renk=TextAreaField("İcerik:",validators=[validators.length(min=20)])

class kisbirincilust(Form):
    isim=StringField("Elbise Adı:",validators=[validators.length(min=5,max=100)])
    marka=TextAreaField("İcerik:",validators=[validators.length(min=20)])
    renk=TextAreaField("İcerik:",validators=[validators.length(min=20)])

class kisayakkabi(Form):
    isim=StringField("Elbise Adı:",validators=[validators.length(min=5,max=100)])
    marka=TextAreaField("İcerik:",validators=[validators.length(min=20)])
    renk=TextAreaField("İcerik:",validators=[validators.length(min=20)])

class altgiyim(Form):
    isim=StringField("Elbise Adı:",validators=[validators.length(min=5,max=100)])
    marka=TextAreaField("İcerik:",validators=[validators.length(min=20)])
    renk=TextAreaField("İcerik:",validators=[validators.length(min=20)])
    
class aksesuar(Form):
    isim=StringField("Elbise Adı:",validators=[validators.length(min=5,max=100)])
    marka=TextAreaField("İcerik:",validators=[validators.length(min=20)])
    renk=TextAreaField("İcerik:",validators=[validators.length(min=20)])

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giris yapınız.","danger")
            return redirect(url_for("login"))
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/addclothes",methods=["GET","POST"])
@login_required
def addclothes():
    form=elbiseform(request.form)

    if request.method=="POST":
        isim=form.isim.data
        renk=form.renk.data
        marka=form.marka.data
        kategori=form.kategori.data
        newclothe=dolap(sahip=session["username"],isim=isim,renk=renk,marka=marka,kategori=kategori)
        db.session.add(newclothe)
        db.session.commit()
        flash("Elbise Kaydı Basariyla Gerceklesti !","success")
        return redirect(url_for("dolapp"))
    else:
        return render_template("addclothes.html",form=form)
    
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    elbise = dolap.query.filter_by(id = id).first()


    if elbise:
        db.session.delete(elbise)
        db.session.commit()
        flash("Makale silme basarili.","success")
        return redirect(url_for("dolapp"))
    else:
        flash("Böyle bir elbise yok.","danger")
        return redirect(url_for("index"))

@app.route("/dolap")
@login_required
def dolapp():
    return render_template("dolap.html")

@app.route("/yaz_ust")
@login_required
def yaz_ust():
    data=dolap.query.filter_by(sahip=session["username"],kategori="yazust").all()
    return render_template("kategori.html",data=data)
@app.route("/yaz_elbise")
@login_required
def yaz_elbise():
    data=dolap.query.filter_by(sahip=session["username"],kategori="yazelbise").all()
    return render_template("kategori.html",data=data)
@app.route("/yaz_ayakkabi")
@login_required
def yaz_ayakkabi():
    data=dolap.query.filter_by(sahip=session["username"],kategori="yazayakkabi").all()
    return render_template("kategori.html",data=data)
@app.route("/montt")
@login_required
def montt():
    data=dolap.query.filter_by(sahip=session["username"],kategori="mont").all()
    return render_template("kategori.html",data=data)
@app.route("/kis_birincil_ust")
@login_required
def kis_birincil_ust():
    data=dolap.query.filter_by(sahip=session["username"],kategori="kisbirincilust").all()
    return render_template("kategori.html",data=data)
@app.route("/kis_ikincil_ust")
@login_required
def kis_ikincil_ust():
    data=dolap.query.filter_by(sahip=session["username"],kategori="kisikincilust").all()
    return render_template("kategori.html",data=data)
@app.route("/kis_ayakkabi")
@login_required
def kis_ayakkabi():
    data=dolap.query.filter_by(sahip=session["username"],kategori="kisayakkabi").all()
    return render_template("kategori.html",data=data)
@app.route("/alt_giyim")
@login_required
def alt_giyim():
    data=dolap.query.filter_by(sahip=session["username"],kategori="altgiyim").all()
    return render_template("kategori.html",data=data)
@app.route("/aksesuarr")
@login_required
def aksesuarr():
    data=dolap.query.filter_by(sahip=session["username"],kategori="aksesuar").all()
    return render_template("kategori.html",data=data)

@app.route("/changepassword",methods=["POST","GET"])
@login_required
def changePass():
    form=passchange(request.form)
    if request.method=="POST":
        newpass=form.newpass.data
        newpassconfirm=form.newpassconfirm.data
        user=users.query.filter_by(username=session["username"]).first()
        if newpass==newpassconfirm:
            user.password=bcrypt.generate_password_hash(newpass)
            db.session.commit()
            flash("Sifre Degistirme Basarili.","success")
            return redirect(url_for("index"))
        else:
            flash("Girilen sifreler uyusmuyor.","warning")
            return redirect(url_for("changePass"))
    else:
        return render_template("changepassword.html",form=form)

@app.route("/register",methods=["GET","POST"])
def register():
    form=registerform(request.form)
    if request.method=="POST" and form.validate():
        newusername=form.username.data
        newemail=form.email.data
        newpassword=bcrypt.generate_password_hash(form.password.data)
        user=users(username=newusername,password=newpassword,email=newemail)
        db.session.add(user)
        db.session.commit()
        flash("Basariyla kayit oldunuz.","success")
        return redirect(url_for("index"))
    else:
        return render_template("register.html",form =form)


@app.route("/login",methods=["GET","POST"])
def login():
    loginform=LoginForm(request.form)
    if request.method=="POST":
        username=loginform.username.data
        password=loginform.password.data
        data=users.query.filter_by(username=username).first()
        if data:
            realPassword=data.password
            if bcrypt.check_password_hash(realPassword,password):
                session["twostep"]=True
                session["username"]=username
                """flash("Basariyla giris yaptiniz.","success")
                session["logged_in"]=True
                session["username"]=username"""
                return redirect(url_for("twostep"))
            else:
                flash("Sifre hatali.","danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kullanıcı bulunamadı.","danger")
            return redirect(url_for("login"))
    else:
        return render_template("login.html",loginform=loginform)

@app.route("/twostep", methods=["GET", "POST"])
def twostep():
    current_time = datetime.datetime.now().minute
    #cd=datetime.datetime.now()
    #day=cd.day
    random.seed(current_time)
    form = verifyForm(request.form)
    kod = random.randint(1000,9999)
    if "twostep" in session:
        if request.method == "POST":
            code=int(form.code.data)
            if kod == code:
                session["logged_in"] = True
                flash("Basariyla giris yaptiniz.","success")
                return redirect(url_for("index"))
            else:
                session.clear()
                flash("Hatalı kod !","danger")
                return redirect(url_for("login"))
        else:
            mesaj = MIMEMultipart()
            mesaj["From"] = "mrtkvk2135@gmail.com"
            mesaj["To"] = "kavakmuratt@gmail.com"
            mesaj["Subject"] = "Onay Kodu"
            yazi = str(kod)
            mesajgovde = MIMEText(yazi, "plain")
            mesaj.attach(mesajgovde)
            mail = smtplib.SMTP("smtp.gmail.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login("mrtkvk2135@gmail.com","yypducysrkupuhip")
            mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
            mail.close()
            return render_template("twostep.html", form=form)
    else:
        flash("Giris yapınız.","danger")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    flash("Basariyla cikis yapildi.","success")
    return redirect(url_for("index"))

@app.route("/kombinolustur",methods=["GET","POST"])
@login_required
def kombinolustur():
    form=dereceform()
    if request.method == "POST":
        
        derece = int(request.form.get("derece"))
        if derece<15:
                try:
                    datakisbirincilust=dolap.query.filter_by(sahip=session["username"],kategori="kisbirincilust").all()
                    kisbirincilust=random.choice(datakisbirincilust)
                    datamont=dolap.query.filter_by(sahip=session["username"],kategori="mont").all()
                    mont=random.choice(datamont)
                    datakisikincilust=dolap.query.filter_by(sahip=session["username"],kategori="kisikincilust").all()
                    kisikincilust=random.choice(datakisikincilust)
                    dataaltgiyim=dolap.query.filter_by(sahip=session["username"],kategori="altgiyim").all()
                    altgiyim=random.choice(dataaltgiyim)
                    datakisayakkabi=dolap.query.filter_by(sahip=session["username"],kategori="kisayakkabi").all()
                    ayakkabi=random.choice(datakisayakkabi)
                    dataaksesuar=dolap.query.filter_by(sahip=session["username"],kategori="aksesuar").all()
                    aksesuar=random.choice(dataaksesuar)
                    data=[kisbirincilust,kisikincilust,altgiyim,ayakkabi,aksesuar,mont]
                except IndexError:
                    flash("Anlasılan dolabınızda bosluk var. Kombin önerisi yapabilmemiz icin lütfen doldurun.","danger")
                    return redirect(url_for("index"))
        elif derece<25:
                try:
                    datakisbirincilust=dolap.query.filter_by(sahip=session["username"],kategori="kisbirincilust").all()
                    kisbirincilust=random.choice(datakisbirincilust)
                    dataaltgiyim=dolap.query.filter_by(sahip=session["username"],kategori="altgiyim").all()
                    altgiyim=random.choice(dataaltgiyim)
                    datakisayakkabi=dolap.query.filter_by(sahip=session["username"],kategori="kisayakkabi").all()
                    ayakkabi=random.choice(datakisayakkabi)
                    dataaksesuar=dolap.query.filter_by(sahip=session["username"],kategori="aksesuar").all()
                    aksesuar=random.choice(dataaksesuar)
                    data=[kisbirincilust,altgiyim,ayakkabi,aksesuar]
                except IndexError:
                    flash("Anlasılan dolabınızda bosluk var. Kombin önerisi yapabilmemiz icin lütfen doldurun.","danger")
                    return redirect(url_for("index"))
        else:
            a=random.randint(1,2)
            if a==1:
                #elbise giyme durumu
                try:
                    dataelbise=dolap.query.filter_by(sahip=session["username"],kategori="yazelbise").all()
                    elbise=random.choice(dataelbise)
                    datayazayakkabi=dolap.query.filter_by(sahip=session["username"],kategori="yazayakkabi").all()
                    ayakkabi=random.choice(datayazayakkabi)
                    dataaksesuar=dolap.query.filter_by(sahip=session["username"],kategori="aksesuar").all()
                    aksesuar=random.choice(dataaksesuar)
                    data=[elbise,ayakkabi,aksesuar]
                except IndexError:
                    flash("Anlasılan dolabınızda bosluk var. Kombin önerisi yapabilmemiz icin lütfen doldurun.","danger")
                    return redirect(url_for("index"))
            else:
                try:
                    datayazust=dolap.query.filter_by(sahip=session["username"],kategori="yazust").all()
                    yazust=random.choice(datayazust)
                    dataaltgiyim=dolap.query.filter_by(sahip=session["username"],kategori="altgiyim").all()
                    altgiyim=random.choice(dataaltgiyim)
                    datayazayakkabi=dolap.query.filter_by(sahip=session["username"],kategori="yazayakkabi").all()
                    ayakkabi=random.choice(datayazayakkabi)
                    dataaksesuar=dolap.query.filter_by(sahip=session["username"],kategori="aksesuar").all()
                    aksesuar=random.choice(dataaksesuar)
                    data=[yazust,altgiyim,ayakkabi,aksesuar]
                except IndexError:
                    flash("Anlasılan dolabınızda bosluk var. Kombin önerisi yapabilmemiz icin lütfen doldurun.","danger")
                    return redirect(url_for("index"))
        return render_template("kombinolustur.html",data=data)
    else:
        return render_template("dereceal.html")


if __name__=="__main__":
    app.run(debug=True)
