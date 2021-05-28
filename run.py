from flask import Flask, render_template, request,session,send_from_directory,Response
import os
import random
app=Flask(__name__)
app.secret_key = 'jsbcdsjkvbdjkbvdjcbkjf'
bufferSize = 64 * 1024
from pymsgbox import *
import pymysql
from Mail import send_email
import cryptography
from cryptography.fernet import Fernet
import socket
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import datetime
from Rest import post
adminMail = "recoverhospital1@gmail.com"
conn=pymysql.connect(host="localhost",user="root",password="root",db="skyline")
cursor=conn.cursor()
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cloudServer')
def cloudServer():
    return render_template('cloudServer.html')

@app.route('/owner')
def owner():
    return render_template('owner.html')

@app.route('/client')
def client():
    return render_template('client.html')


@app.route('/cloudServer1')
def cloudServer1():
    username = request.args.get('username')
    password = request.args.get('password')
    if username == 'admin' and password == 'admin':
        return render_template('serverhome.html')
    else:
        return render_template('cloudServer.html')



@app.route('/ownerRegister')
def ownerRegister():
    return render_template('ownerRegister.html')


@app.route('/ownerregister1',methods=['POST'])
def ownerregister1():
    target = os.path.join(APP_ROOT, 'images/')
    for upload in request.files.getlist("file"):

        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        filename = upload.filename
        print(filename)
        destination = "/".join([target, filename])
        upload.save(destination)
        resultvalue = cursor.execute("select * from ownerreg where username='"+username+"' and email='"+email+"'")
        conn.commit()

        userDetails = cursor.fetchall()
        if resultvalue > 0:
             alert(text='UserAlready Exist', title='REGISTRATION STATUS', button='OK')
             return render_template('ownerRegister.html')


        else:

                result = cursor.execute(
                    " insert into ownerreg(name,username,email,password,phone,pic)values('" + name + "','" + username + "','" + email + "','" + password + "','" + phone + "','"+upload.filename+"')");
                conn.commit()
                alert(text='Registration Success', title='REGISTRATION STATUS', button='OK')
                return render_template('owner.html')


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)



@app.route('/clientRegister')
def clientRegister():
    return render_template('clientRegister.html')



@app.route('/clientregister1',methods=['POST'])
def clientregister1():
    target = os.path.join(APP_ROOT, 'images/')
    for upload in request.files.getlist("file"):

        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        filename = upload.filename
        print(filename)
        destination = "/".join([target, filename])
        upload.save(destination)
        resultvalue = cursor.execute("select * from userreg where username='"+username+"' and email='"+email+"'")
        conn.commit()

        userDetails = cursor.fetchall()
        if resultvalue > 0:
             alert(text='UserAlready Exist', title='REGISTRATION STATUS', button='OK')
             return render_template('clientRegister.html')


        else:

                result = cursor.execute(
                    " insert into userreg(name,username,email,password,phone,pic)values('" + name + "','" + username + "','" + email + "','" + password + "','" + phone + "','"+upload.filename+"')");
                conn.commit()
                alert(text='Registration Success', title='REGISTRATION STATUS', button='OK')
                return render_template('client.html')


@app.route('/verifyowners')
def verifyowners():
    image_names = os.listdir('./images')

    resultvalue = cursor.execute("select * from ownerreg")
    conn.commit()

    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('allowners.html', userDetails=userDetails)
    else:
        alert(text='Owner Details are not Available', title='REGISTRATION STATUS', button='OK')
        return render_template('serverhome.html')



@app.route('/verifyowner')
def verifyowner():
        req_id=request.args.get('Id')
        query=cursor.execute("select * from ownerreg where o_id='"+req_id+"'")
        conn.commit()
        querydetails=cursor.fetchall()

        for user in querydetails:
            email=user[3]
            resultvalue = cursor.execute("update ownerreg set status='authoried' where  o_id='"+req_id+"' ")
            conn.commit()
            #Mail.EmailSending.send_email("","Activation Response","Your Registration Request Activated from the cloud server",email)
            send_email("Activation Response", "Your Registration Request Activated from the cloud server", email)


            return verifyowners()




@app.route('/unauthorizeowner')
def unauthorizeowner():
        req_id=request.args.get('Id')
        query=cursor.execute("select * from ownerreg where o_id='"+req_id+"'")
        conn.commit()
        querydetails=cursor.fetchall()

        for user in querydetails:
            email=user[3]
            resultvalue = cursor.execute("update ownerreg set status='unauthorized' where  o_id='"+req_id+"' ")
            conn.commit()
            #Mail.EmailSending.send_email("","Activation Response","Your Registration Request Unautorized from the cloud server",email)
            send_email("Activation Response", "Your Registration Request Unauthorized from the cloud server", email)

            if resultvalue > 0:
                return verifyowners()
            else:
                alert(text='Activation Fails', title='ACTIVATION STATUS', button='OK')
                return verifyowners()





@app.route('/verifyusers')
def verifyusers():
    image_names = os.listdir('./images')

    resultvalue = cursor.execute("select * from userreg")
    conn.commit()

    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('allusers.html', userDetails=userDetails)
    else:
        alert(text='Users Details are not Available', title='Details STATUS', button='OK')
        return render_template('serverhome.html')



@app.route('/verifyuser')
def verifyuser():
        req_id=request.args.get('Id')
        query=cursor.execute("select * from userreg where o_id='"+req_id+"'")
        conn.commit()
        querydetails=cursor.fetchall()

        for user in querydetails:
            email=user[3]
            #Mail.EmailSending.send_email("","Activation Response","Your Registration Request Activated from the cloud server",email)
            send_email("Activation Response", "Your Registration Request Activated from the cloud server", email)
            resultvalue = cursor.execute("update userreg set status='authoried' where  o_id='"+req_id+"' ")
            conn.commit()


            if resultvalue > 0:
                return verifyowners()
            else:
                alert(text='Activation Fails', title='ACTIVATION STATUS', button='OK')
                return verifyusers()



@app.route('/unauthorizeuser')
def unauthorizeuser():
        req_id=request.args.get('Id')
        query=cursor.execute("select * from userreg where o_id='"+req_id+"'")
        conn.commit()
        querydetails=cursor.fetchall()

        for user in querydetails:
            email=user[3]
            resultvalue = cursor.execute("update userreg set status='unauthorized' where  o_id='"+req_id+"' ")
            conn.commit()
            #Mail.EmailSending.send_email("","Activation Response","Your Registration Request Unautorized from the cloud server",email)
            send_email("Activation Response", "Your Registration Request Unauthorized from the cloud server", email)
            if resultvalue > 0:
                return verifyowners()
            else:
                alert(text='Activation Fails', title='ACTIVATION STATUS', button='OK')
                return verifyusers()




@app.route('/owner1')
def owner1():
    username = request.args.get('username')
    password = request.args.get('password')

    result = cursor.execute(" select * from ownerreg where username='" + username + "' and password='" + password + "'  and status='authoried'")
    details=cursor.fetchall()
    conn.commit()
    if result > 0:
        for user in details:


                 session['username'] = user[2]
                 session['user_id']=user[0]
                 session['email']=user[3]
                 session['role']=user[6]
        return render_template('ownerHome.html')




    else:
            return render_template('owner.html')



@app.route('/ownerProfile')
def ownerProfile():
    username = session['username']
    id = session['user_id']
    query=cursor.execute("select * from ownerreg where username='"+username+"' ")
    querydetails=cursor.fetchall()
    if query > 0 :
        return render_template('ownerProfile.html',details=querydetails)



@app.route('/ownerHome')
def ownerHome():
    return render_template('ownerHome.html')

@app.route('/uploadPatient')
def uploadPatient():
    return render_template('uploadPatient.html')



@app.route('/uploadpatient1',methods=['POST'])
def uploadpatient1():
    target = os.path.join(APP_ROOT, 'images/')
    target1 = os.path.join(APP_ROOT, 'reports/')

    for upload in request.files.getlist("file"):
      for upload1 in request.files.getlist("myfile"):
        pname = request.form.get('pname')
        address = request.form.get('address')
        dob = request.form.get('dob')
        email = request.form.get('email')
        phone = request.form.get('phone')
        hname = request.form.get('hname')
        bloodgroup = request.form.get('bloodgroup')
        dname = request.form.get('dname')
        dsym = request.form.get('dsym')
        age = request.form.get('age')
        file = request.files['myfile']
        c = random.randint(500, 455000)
        newfiledate = file.read()
        data = str(newfiledate)
        x = data.replace("'", " ")

        filename = upload.filename
        rename = upload1.filename

        print(filename)
        destination = "/".join([target, filename])
        destination1 = "/".join([target1, rename])

        upload.save(destination)
        upload1.save(destination1)
        key = Fernet.generate_key()
        enemail = email.encode()
        enphone = phone.encode()
        enaddress = address.encode()
        endob = dob.encode()
        enhname = hname.encode()
        enbloodgroup = bloodgroup.encode()
        endname = dname.encode()
        endsym = dsym.encode()
        enage = age.encode()
        endata = data.encode()
        f = Fernet(key)
        encryptedemail = f.encrypt(enemail)
        encryptedphone = f.encrypt(enphone)
        encryptedaddress = f.encrypt(enaddress)
        encrypteddob = f.encrypt(endob)
        encryptedhname = f.encrypt(enhname)
        encryptedbloodgroup = f.encrypt(enbloodgroup)
        encrypteddname = f.encrypt(endname)
        encrypteddsysm = f.encrypt(endsym)
        encryptedage = f.encrypt(enage)
        encrypteddata = f.encrypt(endata)
        email1=str(encryptedemail).replace("'","")
        phone1=str(encryptedphone).replace("'","")
        address1=str(encryptedaddress).replace("'","")
        dob1=str(encrypteddob).replace("'","")
        hname1=str(encryptedhname).replace("'","")
        bloodgroup1=str(encryptedbloodgroup).replace("'","")
        dname1=str(encrypteddname).replace("'","")
        dsym1=str(encrypteddsysm).replace("'","")
        age1=str(encryptedage).replace("'","")
        data1=str(encrypteddata).replace("'","")
        url = 'Skyline/files/' + session['username'] + '/' + pname;
        firebasedata = '{"pname":"' + pname + '", "email":"' + email1 + '", "phone":"' + phone1 + '","address":"' + address1 + '","dob":"' + dob1 + '","hname":"' + hname1 + '","bgroup":"' + bloodgroup1 + '","disease":"' + dname1 + '","symptom":"' + dsym1 + '","age":"' + age1 + '","pic":"' + upload.filename + '","rdata":"' + data1 + '","uploadby":"' + session['username'] + '","datee":"' + str(datetime.datetime.now()) + '"}'
        print(firebasedata)
        result = post(url=url, data=firebasedata)
        print(result)
        print(encrypteddata)
        print(" insert into patient(pname,email,phone,address,dob,hname,bgroup,disease,symptom,age,pic,rdata,uploadby,datee)"
                                "values('" + pname + "','" + email + "','" + phone + "','" + address + "','" + dob + "','"+hname+"','"+bloodgroup+"','"+dname+"','"+dsym+"','"+age+"','"+upload.filename+"','"+x+"','"+session['username']+"',now())")


        result = cursor.execute(" insert into patient(pname,email,phone,address,dob,hname,bgroup,disease,symptom,age,pic,rdata,uploadby,datee,keyy)"
                                "values('" + pname + "','" + email + "','" + phone + "','" + address + "','" + dob + "','"+hname+"','"+bloodgroup+"','"+dname+"','"+dsym+"','"+age+"','"+upload.filename+"','"+x+"','"+session['username']+"',now(),'"+str(c)+"')");
        conn.commit()
        rowid = cursor.lastrowid
        print(rowid)
        print(" insert into epatient(epname,eemail,ephone,eaddress,edob,ehname,ebgroup,edisease,esymptom,eage,epic,erdata,euploadby,edatee,patientid)"
            "values('" + pname + "','" + email1 + "','" + phone1 + "','" + address1 + "','" +dob1 + "','" + hname1 + "','" + bloodgroup1 + "','" + dname1 + "','" + dsym1 + "','" + age1 + "','" + upload.filename + "','" + data1 + "','" +
            session['username'] + "',now(),'1')")
        result = cursor.execute(
            " insert into epatient(epname,eemail,ephone,eaddress,edob,ehname,ebgroup,edisease,esymptom,eage,epic,erdata,euploadby,edatee,patientid)"
            "values('" + pname + "','" + email1 + "','" + phone1 + "','" + address1 + "','" +dob1 + "','" + hname1 + "','" + bloodgroup1 + "','" + dname1 + "','" + dsym1 + "','" + age1 + "','" + upload.filename + "','" + data1 + "','" +
            session['username'] + "',now(),'1')");
        conn.commit()
        alert(text='Patient Added Success', title='REGISTRATION STATUS', button='OK')
        return render_template('uploadPatient.html')


@app.route('/viewmyPatientdel')
def viewmyPatientdel():
    username = session['username']
    a=cursor.execute("select * from patient where uploadby='"+username+"'")
    data=cursor.fetchall()
    if a > 0:
        return render_template('viewpatientdel.html',pdel=data)
    else:
        alert(text='Patient Details are not availale', title='Details STATUS', button='OK')
        return render_template('ownerHome.html')

@app.route('/viewdata')
def viewdata():
    idd = request.args.get('id')
    a=cursor.execute("select * from patient where id='"+idd+"'")
    data=cursor.fetchall()
    if a > 0:
        return render_template('viewdata.html',pdel=data)
    else:
        alert(text='Patient Details are not availale', title='Details STATUS', button='OK')
        return render_template('ownerHome.html')

@app.route('/userlogout')
def userlogout():
    session.pop('username', None)
    session.pop('email', None)
    session.pop('user_id', None)

    return render_template('index.html')


@app.route('/ownerlogout')
def ownerlogout():
    session.pop('username', None)
    session.pop('email', None)
    session.pop('user_id', None)

    return render_template('index.html')



@app.route('/client1')
def client1():
    username = request.args.get('username')
    password = request.args.get('password')

    result = cursor.execute(" select * from userreg where username='" + username + "' and password='" + password + "'  and status='authoried'")
    details=cursor.fetchall()
    conn.commit()
    if result > 0:
        for user in details:


                 session['username'] = user[2]
                 session['user_id']=user[0]
                 session['email']=user[3]
        return render_template('userHome.html')




    else:
            return render_template('login.html')


@app.route('/userHome')
def userHome():
    return render_template('userHome.html')

@app.route('/search')
def search():

            return render_template('search.html')

@app.route('/search1')
def search1():
    filename = request.args.get('pname')
    username = session['username']

    print(filename)
    resultvalue1 = cursor.execute(
        "insert into userTransaction(transactiontype,filename,datee,username) values('search','" + filename + "',now(),'"+username+"') ")

    resultvalue = cursor.execute("select * from patient where pname='"+filename+"' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('userviewpatient.html', userDetails=userDetails)
    else:
        alert(text='Patient Details are not availale', title='Details STATUS', button='OK')
        return render_template('search.html')


@app.route('/request')
def request1():
        req_id=request.args.get('id')
        filename=request.args.get('pname')
        username = session['username']
        ownername =request.args.get('ownername')
        resultvalue1 = cursor.execute("insert into userTransaction(transactiontype,filename,datee,username) values('request','"+filename+"',now(),'"+username+"') ")

        resultvalue = cursor.execute("insert into request(p_id,pname,reqby,ownername,datee) values('"+req_id+"','"+filename+"','"+username+"','"+ownername+"',now()) ")

        conn.commit()
        if resultvalue > 0:
            alert(text='Request sent successfully to the cloud server', title='Request STATUS', button='OK')
            return render_template('search.html')

        else:
            alert(text='Request sent Fails to the cloud server', title='Request STATUS', button='OK')
            return render_template('search.html')

@app.route('/searchbyage')
def searchbyage():

            return render_template('searchbyage.html')


@app.route('/searchbyage1')
def searchbyage1():
    filename = request.args.get('page')
    username = session['username']

    print(filename)
    resultvalue1 = cursor.execute(
        "insert into userTransaction(transactiontype,filename,datee,username) values('search','" + filename + "',now(),'"+username+"') ")

    resultvalue = cursor.execute("select * from patient where age='"+filename+"' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('userviewpatient.html', userDetails=userDetails)
    else:
        alert(text='Patient Details are not availale', title='Details STATUS', button='OK')
        return render_template('search.html')


@app.route('/aviewpatient')
def aviewpatient():
    a = cursor.execute("select * from epatient")
    data = cursor.fetchall()
    if a > 0:
        return render_template('aviewpatientdel.html', pdel=data)
    else:
        alert(text='Patient Details are not availale', title='Details STATUS', button='OK')
        return render_template('serverhome.html')

@app.route('/viewdata1')
def viewdata1():
    idd = request.args.get('id')
    a=cursor.execute("select * from epatient where id='"+idd+"'")
    data=cursor.fetchall()
    if a > 0:
        return render_template('aviewdata.html',pdel=data)
    else:
        alert(text='Patient Details are not availale', title='Details STATUS', button='OK')
        return render_template('serverhome.html')

@app.route('/viewtransaction')
def viewtransaction():

    resultvalue = cursor.execute("select * from usertransaction")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('viewuserTransactiondel.html', userDetails=userDetails)
    else:
        alert(text='Transaction Details are not availale', title='Details STATUS', button='OK')
        return render_template('serverhome.html')

@app.route('/aviewreq')
def aviewreq():
    resultvalue = cursor.execute("select * from request")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('reqfiles.html', userDetails=userDetails)
    else:
        alert(text='Request Details are not availale', title='Details STATUS', button='OK')
        return render_template('serverhome.html')

@app.route('/requestedFiles')
def requestedFiles():
    username = session['username']

    resultvalue = cursor.execute("select * from request where reqby='"+username+"' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('myreqfiles.html', userDetails=userDetails)
    else:
        alert(text='Request Details are not availale', title='Details STATUS', button='OK')
        return render_template('userHome.html')

@app.route('/acceptrequest')
def acceptrequest():
    id=request.args.get('id')
    reqby=request.args.get('reqby')
    pid=request.args.get('pid')

    cursor.execute("select * from patient where id='"+pid+"'")
    pdata=cursor.fetchall()
    keyy=""
    for p in pdata:
        keyy=p[13]
    cursor.execute("select * from userreg where username='"+reqby+"'")
    udata=cursor.fetchall()
    email=""
    for u in udata:
        email=u[3]
    cursor.execute("update request set status='accept' where r_id='"+id+"'")
    conn.commit()
    #Mail.EmailSending.send_email('',"Requestd Key","Use This Key for download the patient report"+keyy,email)
    send_email("Requested Keys", "Use This Key for download the patient report "+str(keyy), email)
    alert(text='Request Accepted Success ', title='Details STATUS', button='OK')
    return aviewreq()

@app.route('/uviewpatientdel')
def uviewpatientdel():
    id=request.args.get('pid')
    a=cursor.execute("select * from patient where id='"+id+"'")
    data=cursor.fetchall()
    if a > 0:
        return render_template('uviewpatientdel.html',pdel=data)
    else:
        alert(text='Patient Details are not availale', title='Details STATUS', button='OK')
        return render_template('userHome.html')


@app.route('/download')
def download():
    id=request.args.get('id')
    return render_template('download.html',fileid=id)





@app.route('/uviewdata')
def uviewdata():
    idd = request.args.get('fileid')
    keyy = request.args.get('key')
    a=cursor.execute("select * from patient where id='"+idd+"' and keyy='"+keyy+"'")
    data=cursor.fetchall()
    if a > 0:
        return render_template('uviewdata.html',pdel=data)
    else:
        alert(text='Please Enter Correct key', title='Details STATUS', button='OK')
        return render_template('userHome.html')



@app.route('/download1')
def download1():
    id=request.args.get('id')
    username=session['username']
    a=cursor.execute("select * from patient where id='"+id+"'")
    resultvalue = cursor.fetchall()
    conn.commit()
    if a > 0 :
        for roww in resultvalue:
            cursor.execute(
                "insert into download(user,pname,datee,ownername)values('" + username + "','" + roww[1] + "',now(),'" + roww[2] + "')")
            conn.commit()
            resultvalue1 = cursor.execute(
                "insert into userTransaction(transactiontype,filename,datee,username) values('download','" + roww[1] + "',now(),'" + username + "') ")
            conn.commit()
            c = random.randint(500, 455000)


            a = cursor.execute("update patient set keyy='" + str(
                c) + "' where id='" + str(roww[0]) + "' ")
            conn.commit()


            csv = roww[12]
            return Response(
                csv,
                mimetype="text/csv",
                headers={"Content-disposition":
                             "attachment; filename="+roww[1]+".txt"})
    else:

        alert(text='Wrong Id', title='Details STATUS', button='OK')
        return render_template('userHome.html')

@app.route('/viewDownloaddetails')
def viewDownloaddetails():
    username=session['username']
    a=cursor.execute("select * from download where user='"+username+"'")
    details=cursor.fetchall()
    if a > 0:
        return  render_template('viewmydownloads.html',mydetails=details)
    else:
        alert(text='Details are not available', title='DETAILS STATUS', button='OK')
        return render_template('userHome.html')

@app.route('/attacker')
def attacker():
    return  render_template('attacker.html')

@app.route('/attacker1')
def attacker1():
    filename = request.args.get('filename')

    print(filename)

    resultvalue = cursor.execute("select * from epatient where epname='"+filename+"' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('attackerviewfiles.html', userDetails=userDetails)
    else:
        return render_template("mainmsg.html", msg='File Details not Available')


@app.route('/attackerviewfiles1')
def attackerviewfiles1():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    filename=request.args.get('fname')
    a=cursor.execute("insert into attacker(hostaddress,ipaddress,datee,filename) values('"+hostname+"','"+IPAddr+"',now(),'"+filename+"')")
    conn.commit()
    if a > 0:
        #Mail.EmailSending.send_email("","Attacker","Attacker hack the file..the file name is"+filename,"dhaatrisolutions4@gmail.com")
        send_email("Attacker", "Attacker hack the file..the file name is"+filename , adminMail)
        alert(text='YOU CAN NOT HACK THE FILE', title='DETAILS STATUS', button='OK')
        return render_template('index.html')
    else:
        alert(text='YOU CAN NOT HACK THE FILE', title='DETAILS STATUS', button='OK')
        return render_template('index.html')


@app.route('/viewAttackedFiles')
def viewAttackedFiles():
    a=cursor.execute("select * from attacker")
    details=cursor.fetchall()
    if a > 0:
        return  render_template('viewattackersfiles.html',fdetails=details)
    else:
        alert(text='All patient details are in safe', title='DETAILS STATUS', button='OK')
        return render_template('serverhome.html')


@app.route('/samedesease')
def samedesease():
    a=cursor.execute("select count(*),disease from patient group by disease")
    sdel=cursor.fetchall()
    if a > 0:
        objects1=()
        performance1=[]
        print(sdel)
        for s in sdel:
            objects1=objects1+(s[1],)
            performance1.append(s[0])
        print(objects1)
        print(performance1)
        objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
        y_pos = np.arange(len(objects1))
        performance = [10, 8, 6, 4, 2, 1]

        plt.bar(y_pos, performance1, align='center', alpha=0.5)
        plt.xticks(y_pos, objects1)
        plt.ylabel('Usage')
        plt.title('Same Disease Rank Chart')
        plt.show()
        return render_template('serverhome.html')

    else:
        alert(text='details are not available', title='DETAILS STATUS', button='OK')
        return render_template('serverhome.html')


@app.route('/accesschart')
def accesschart():
    a=cursor.execute("select count(*),pname from download group by pname")
    sdel=cursor.fetchall()
    if a > 0:
        objects1=()
        performance1=[]
        print(sdel)
        for s in sdel:
            objects1=objects1+(s[1],)
            performance1.append(s[0])
        print(objects1)
        print(performance1)
        objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
        y_pos = np.arange(len(objects1))
        performance = [10, 8, 6, 4, 2, 1]

        plt.bar(y_pos, performance1, align='center', alpha=0.5)
        plt.xticks(y_pos, objects1)
        plt.ylabel('Usage')
        plt.title('Same Disease Rank Chart')
        plt.show()
        return render_template('serverhome.html')

    else:
        alert(text='details are not available', title='DETAILS STATUS', button='OK')
        return render_template('serverhome.html')



if __name__ == '__main__':
    app.run(debug=True)