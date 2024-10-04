from flask import Flask,redirect,url_for,request,render_template
app=Flask(__name__)
data={
    '343434':{'pinno':111,'balance':2020}
}
@app.route('/')
def welcome():
    return render_template('welcome.html')
@app.route('/get_accounts')
def get_accounts(): 
    data_list=[{'account_no':accno,'balance':details['balance'],'pinno':details['pinno']} for accno,details in data.items()]
    return data_list
@app.route('/create',methods=['GET','POST'])
def create():
    if request.method=='POST':
        print(request.form)
        account_no=request.form['accno']
        pin_no=int(request.form['pinno'])
        #balance=float(request.form.get('balance),0)
        balance=0
        if account_no in data:
            return 'Account already existed'
        data[account_no]={'pinno':pin_no,'balance':balance}
            #return redirect(url_for('welcome'))
        return data
    return render_template('create.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        accno=request.form['acn']
        pin=int(request.form['pin'])
        if accno in data:
            if data[accno]['pinno']==pin:
                return redirect(url_for('panel',account_no=accno,pin_no=pin))
            else:
                return 'pin wrong'
        else:
            return 'No account exist'
    return render_template('logindetails.html')
@app.route('/panel/<account_no>/<pin_no>')
def panel(account_no,pin_no):
    return render_template('panel.html',account_no=account_no,pin_no=pin_no)
@app.route('/balance/<an>/<pn>')
def balance(an,pn):
    details=data[an] #{'pin':pin,'balance':balance}
    data_list=[{'account_no':an,'balance':details['balance']}]
    balance=data_list[0]['balance']
    return render_template('balance.html',balance=balance,an=an,pn=pn)
@app.route('/credit/<an>/<pn>',methods=['GET','POST'])
def credit(an,pn):
    if request.method=='POST':
        amount=int(request.form['amount'])
        details=data[an]    #if accountno is 343434 then details {'pin':pin,'balance':balance}
        data_list=[{'account_no':an,'balance':details['balance']}]  #creating a list with accno,balance from above details.
        if data_list[0]['account_no']==an:  #validating accno
            original_amount=data_list[0]['balance']     #fetching original amount
            data[an]['balance']=original_amount+amount  #incrementing amount
            print(data_list)
            return redirect(url_for('balance',an=an,pn=pn))
    return render_template('credit.html',an=an,pn=pn)
@app.route('/debit/<an>/<pn>',methods=['GET','POST'])
def debit(an,pn):
    if request.method=='POST':
        amn=int(request.form['amn'])
        details=data[an]
        data_list=[{'account_no':an,'balance':details['balance']}]
        if data_list[0]['account_no']==an:
            original=data_list[0]['balance']
            if original>=amn:
                data[an]['balance']=original-amn
                return redirect(url_for('balance',an=an,pn=pn))
            else:
                return 'Insufficient Balance'
    return render_template('debit.html',an=an,pn=pn)
@app.route('/delete/<accno>')
def delete(accno):
    data.pop(accno)
    return 'Account deleted successfully'
app.run(debug=True)