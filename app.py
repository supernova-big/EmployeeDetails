from flask import Flask, render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import date
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Emp_details(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    emp_id=db.Column(db.Integer,nullable=False,unique=True)
    name_prefix=db.Column(db.String(10),nullable=False)
    first_name=db.Column(db.String(100),nullable=False)
    last_name=db.Column(db.String(100),nullable=False)
    gender=db.Column(db.String(2),nullable=False)
    e_mail=db.Column(db.String(200),nullable=False)
    salary=db.Column(db.Integer,nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Task %r>' % self.id    

        


@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        emp_id=request.form['emp_id']
        name_prefix=request.form['name_prefix']
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        gender=request.form['gender']
        e_mail=request.form['e_mail']
        salary=request.form['salary']
        
        new_detail=Emp_details(emp_id=emp_id,name_prefix=name_prefix,first_name=first_name,last_name=last_name,gender=gender,e_mail=e_mail,salary=salary)
        try:
            db.session.add(new_detail)
            db.session.commit()
            return redirect('/')
        except:
             return 'There was an issue adding your task'    


    
    else: 
        #plans=Plans.query.order_by(Plans.date_created).all()
        todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)


        emp_details = Emp_details.query.filter(Emp_details.date_created >= todays_datetime).all()   
        return render_template('index.html',emp_details=emp_details)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Emp_details.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"    

 
   
@app.route('/update/<int:id>',methods=["POST","GET"])
def update(id):
    emp_detail = Emp_details.query.get_or_404(id)

    if request.method == 'POST':
        emp_detail.emp_id = request.form['emp_id']
        emp_detail.name_prefix = request.form['name_prefix']
        emp_detail.first_name = request.form['first_name']
        emp_detail.last_name = request.form['last_name']
        emp_detail.gender=request.form['gender']
        emp_detail.e_mail=request.form['e_mail']
        emp_detail.salary=request.form['salary']
            

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', emp_detail=emp_detail)

if __name__=="__main__":
    app.run(debug=True)