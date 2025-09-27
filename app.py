import cv2
import os
from flask import Flask,request,render_template
from datetime import date
from datetime import datetime
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib
from flaskwebgui import FlaskUI
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense


#### Defining Flask App
app = Flask(__name__)

#### Saving Date today in 2 different formats
def datetoday():
    return date.today().strftime("%m_%d_%y")

def datetoday2():
    return date.today().strftime("%d-%B-%Y")

def datetoday3():
    return date.today().strftime("%Y-%m-%d")

def date3todate(sdate):
    year = sdate.split("-")[0]
    month = sdate.split("-")[1]
    day = sdate.split("-")[2]
    return date(year=int(year), month=int(month), day=int(day)).strftime("%m_%d_%y")

def date3todate2(sdate):
    year = sdate.split("-")[0]
    month = sdate.split("-")[1]
    day = sdate.split("-")[2]
    return date(year=int(year), month=int(month), day=int(day)).strftime("%d-%B-%Y")



#### Initializing VideoCapture object to access WebCam
face_detector = cv2.CascadeClassifier('static/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)


#### If these directories don't exist, create them
if not os.path.isdir('static/data/Attendance'):
    os.makedirs('static/data/Attendance')
if not os.path.isdir('static/data/faces'):
    os.makedirs('static/data/faces')

def create_attn_sheet(date, ftype):
    if f'Attendance-{date}.csv' not in os.listdir('static/data/Attendance'):
        with open(f'static/data/Attendance/Attendance-{date}-{ftype}.csv','w') as f:
            f.write('Name,Roll,StudentNo,Time,ParentNo')


#### get a number of total registered users
def totalreg():
    return len(os.listdir('static/data/faces'))


#### extract the face from an image
def extract_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    return face_points


#### Identify face using ML model
def identify_face(facearray):
    model = joblib.load('static/data/face_recognition_model.pkl')
    probs = model.predict_proba(facearray)
    pred = model.predict(facearray)
    # print(probs)
    # print(pred)
    return pred[0], np.max(probs)


#### A function which trains the model on all the faces available in faces folder
def train_model():

    faces = []
    labels = []
    userlist = os.listdir('static/data/faces')
    for user in userlist:
        for imgname in os.listdir(f'static/data/faces/{user}'):
            img = cv2.imread(f'static/data/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (100, 100))
            faces.append(resized_face)
            labels.append(user)
    faces = np.array(faces)
    labels = np.array(labels)

    # Normalize the pixel values between 0 and 1
    faces = faces / 255.0

    # Convert labels to categorical one-hot encoding
    num_classes = len(np.unique(labels))
    labels = tf.keras.utils.to_categorical(labels, num_classes)

    # Create the CNN model
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    # Compile and train the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(faces, labels, epochs=10, batch_size=32)

    # Save the trained model
    model.save('static/data/face_recognition_model.pkl')


#### Extract info from today's attendance file in attendance folder
def extract_attendance(date, ftype):
    if not os.path.exists(f'static/data/Attendance/Attendance-{date}-{ftype}.csv'):
        create_attn_sheet(date, ftype)
    df = pd.read_csv(f'static/data/Attendance/Attendance-{date}-{ftype}.csv')
    names = df['Name']
    rolls = df['Roll']
    times = df['Time']
    l = len(df)
    return names,rolls,times,l

def extract_absentees(date, ftype):
    users = []
    smobs = []
    pmobs = []
    l = 0
    if os.path.exists(f'static/data/Attendance/Attendance-{date}-{ftype}.csv'):
        names,rolls,times,lt = extract_attendance(date, ftype)
        userlist = os.listdir('static/data/faces')
        for user in userlist:
            userinfo = f'{user}'
            # if userinfo.split('_')[1] not in rolls.values:
            if userinfo.split('_')[1] not in list(rolls):
                users.append(userinfo.split('_')[0])
                smobs.append(userinfo.split('_')[2])
                pmobs.append(userinfo.split('_')[3])
                l = l+1
    return users,smobs,pmobs,l

#### Add Attendance of a specific user
def add_attendance(name, ftype):
    username = name.split('_')[0]
    userid = name.split('_')[1]
    smob = name.split('_')[2]
    pmob = name.split('_')[3]
    current_time = datetime.now().strftime("%H:%M:%S")

    if not os.path.exists(f'static/data/Attendance/Attendance-{datetoday()}-{ftype}.csv'):
        create_attn_sheet(datetoday(), ftype)

    df = pd.read_csv(f'static/data/Attendance/Attendance-{datetoday()}-{ftype}.csv')
    if userid not in list(df['Roll']):
        with open(f'static/data/Attendance/Attendance-{datetoday()}-{ftype}.csv','a') as f:
            f.write(f'\n{username},{userid},{smob},{current_time},{pmob}')

def read_login_info():
    hostel_name = ""
    pwd = ""
    with open(f'static/data/login.info','r') as f:
        info = f.read().split(';')
        hostel_name = info[0]
        pwd = info[1]
    return (hostel_name, pwd)

def write_login_info(name, pwd):
    with open(f'static/data/login.info','w') as f:
        f.write(name + ";" + pwd)
    with open(f'static/data/ftype','w') as f:
        f.write("breakfast")

def update_ftype(ftype):
    with open(f'static/data/ftype','w') as f:
        f.write(f"{ftype}")

def get_ftype():
    ftype = "breakfast"
    with open(f'static/data/ftype','r') as f:
        ftype = f.read()
    return ftype

def get_all_ftypes(selftype = None):
    fnames = ["Breakfast", "Lunch", "Dinner"]
    ftypes = ["breakfast", "lunch", "dinner"]
    fstates = []
    if not selftype:
        selftype = get_ftype()
    for ftype in ftypes:
        if ftype == selftype:
            fstates.append("Y")
        else:
            fstates.append("N")
    return (fnames, ftypes, fstates)

################## ROUTING FUNCTIONS #########################

#### Our main page
@app.route('/')
def home():
    if 'login.info' not in os.listdir('static/data'):
        return render_template('signup.html')
    else:
        (hostelname , pwd) = read_login_info()
        return render_template('login.html',hostelname=hostelname)

@app.route('/signup',methods=['POST'])
def signup():
    write_login_info(request.form['hostelname'],request.form['password'])
    return render_template('login.html',hostelname=request.form['hostelname'])

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    (hostelname , pwd) = read_login_info()
    names,rolls,times,l = extract_attendance(datetoday(), get_ftype())
    fnames,ftypes,fstates = get_all_ftypes()
    return render_template('dashboard.html', hostelname=hostelname, fnames=fnames, ftypes=ftypes, fstates=fstates, totalreg=totalreg(), totalpresent=l, totalabsent=max(totalreg()-l, 0), datetoday=datetoday2())

@app.route('/login',methods=['POST'])
def login():
    (hostelname , pwd) = read_login_info()
    if pwd == request.form['password']:
        return dashboard()
    else:
        return render_template('login.html',hostelname=hostelname, msg='Incorrect Password! Please Try again..')

@app.route('/absentees',methods=['GET','POST'])
def absentees():
    seldate = None
    selftype = None
    if request.method == "POST":
        seldate = request.form['seldate']
        selftype = request.form['selftype']
    if not seldate:
        seldate = datetoday3()
    if not selftype:
        selftype = get_ftype()
    users,smobs,pmobs,l = extract_absentees(date3todate(seldate), selftype)
    (hostelname , pwd) = read_login_info()
    fnames,ftypes,fstates = get_all_ftypes(selftype)
    selfname = ""
    for idx, fstate in enumerate(fstates):
        if fstate == "Y":
            selfname = fnames[idx]
    return render_template('absents.html', hostelname=hostelname, datetoday3=datetoday3(), seldate3=seldate, seldate=date3todate2(seldate), selftype=selftype, selfname=selfname, fnames=fnames, ftypes=ftypes, fstates=fstates, names=users, smobs=smobs, pmobs=pmobs, l=l, totalreg=totalreg(), msg = None if l else "No entries found!")


#### This function will run when we click on Take Attendance Button
@app.route('/start',methods=['GET'])
def start():
    if 'face_recognition_model.pkl' not in os.listdir('static/data'):
        return startattn("No users found! Please add users 1st..")

    confidence_threshold = 0.75
    ftype = get_ftype()

    cap = cv2.VideoCapture(0)
    ret = True
    while ret:
        ret,frame = cap.read()
        if extract_faces(frame)!=():
            (x,y,w,h) = extract_faces(frame)[0]
            cv2.rectangle(frame,(x, y), (x+w, y+h), (255, 0, 20), 2)
            face = cv2.resize(frame[y:y+h,x:x+w], (50, 50))
            identified_person, prob = identify_face(face.reshape(1,-1))
            identified_person = identified_person
            if prob > confidence_threshold:
                add_attendance(identified_person, ftype)
            else:
                identified_person = "UNKNOWN"
            cv2.putText(frame,f'{identified_person.split("_")[0]}',(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 20),2,cv2.LINE_AA)
        cv2.imshow('Attendance',frame)
        if cv2.waitKey(1)==27:
            break
    cap.release()
    cv2.destroyAllWindows()
    return startattn()

@app.route('/updateftype',methods=['GET'])
def updateftype():
    update_ftype(request.args.get('ftype'))
    if(request.args.get("redirect")=="dashboard"):
        return dashboard()
    else:
        return startattn()

#### This function will run when we click on Take Attendance Button
@app.route('/startattn',methods=['GET'])
def startattn(msg = None):
    (hostelname , pwd) = read_login_info()
    names,rolls,times,l = extract_attendance(datetoday(), get_ftype())
    fnames,ftypes,fstates = get_all_ftypes()
    return render_template('attn.html', hostelname=hostelname,fnames=fnames, ftypes=ftypes, fstates=fstates,names=names,rolls=rolls,times=times,l=l,totalreg=totalreg(),datetoday=datetoday2(), msg = msg if (l or msg) else "No entries found!")

#### This function will run when we add a new user
@app.route('/add',methods=['GET','POST'])
def add():
    newusername = request.form['newusername']
    newuserid = request.form['newuserid']
    smob = request.form['smob']
    pmob = request.form['pmob']
    userimagefolder = 'static/data/faces/'+newusername+'_'+str(newuserid)+'_'+str(smob)+'_'+str(pmob)
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)
    cap = cv2.VideoCapture(0)
    i,j = 0,0
    while 1:
        _,frame = cap.read()
        faces = extract_faces(frame)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x, y), (x+w, y+h), (255, 0, 20), 2)
            cv2.putText(frame,f'Images Captured: {i}/50',(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 20),2,cv2.LINE_AA)
            if j%10==0:
                name = newusername+'_'+str(i)+'.jpg'
                cv2.imwrite(userimagefolder+'/'+name,frame[y:y+h,x:x+w])
                i+=1
            j+=1
        if j==500:
            break
        cv2.imshow('Adding new User',frame)
        if cv2.waitKey(1)==27:
            break
    cap.release()
    cv2.destroyAllWindows()
    print('Training Model')
    train_model()
    return adduser("User Added Successfully!")

@app.route('/adduser',methods=['GET','POST'])
def adduser(msg = None):
    (hostelname , pwd) = read_login_info()
    return render_template('adduser.html',hostelname=hostelname, msg=msg)

#### Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True)
    # FlaskUI(app=app, server="flask").run()