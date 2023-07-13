from django.shortcuts import render
import pyrebase
from django.contrib import auth
from django.http import HttpResponse

# Create your views here.
config = {
    'apiKey': "AIzaSyCXCZMH_0L8_E3E5FxrcNlRHfoLO9BLfo4",
    'authDomain': "just-digital-diary-9503d.firebaseapp.com",
    'databaseURL': "https://just-digital-diary-9503d-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "just-digital-diary-9503d",
    'storageBucket': "just-digital-diary-9503d.appspot.com",
    'messagingSenderId': "687041537473",
    'appId': "1:687041537473:web:1fdcbc5afd41a929c77b40"
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()


def sign_in(request):
    try:
        idToken = request.session['uid']
        a = authe.get_account_info(idToken)
        a = a['users']
        a = a[0]
        localid = a['localId']
        email = a["email"]
        print(email)
        docid = email.replace(".", "")
        if email == "superadmin@just.edu.bd":
            return render(request, 'SAdminHomeTemp.html', {"e": email})
        elif email == "admin10@just.edu.bd":
            return render(request, 'AdminHome.html', {"e": email})
        elif email == "admin5@just.edu.bd":
            return render(request, 'AdminHome.html', {"e": email})
        else:
            try:
                print("try")
                role = database.child("Admins").child(docid).child("role").get().val()
                print(role)
                if role == "admin":
                    return render(request, 'AdminHome.html', {"e": email})
                elif database.child("Students").child(docid).child('role').get().val() == "student":
                    return render(request, 'StuHome.html', {"e": email})
                elif database.child("Teachers").child(docid).child('role').get().val() == "teacher":
                    return render(request, 'TeaHome.html', {"e": email})
                else:
                    return render(request, 'HomeTemp.html', {"e": email})
            except:
                return render(request, 'HomeTemp.html', {"e": email})

    except:
        return render(request, 'SignInTemp.html')

def post_sign_in(request):
    email = request.POST.get("iemail")
    passw = request.POST.get('ipasss')
    user = authe.sign_in_with_email_and_password(email, passw)
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    email = a["email"]
    docid = email.replace(".", "")

    if email == "superadmin@just.edu.bd":
        return render(request, 'SAdminHomeTemp.html', {"e": email})
    elif email == "admin10@just.edu.bd":
        return render(request, 'AdminHome.html')
    elif email == "admin5@just.edu.bd":
        return render(request, 'AdminHome.html', {"e": email})
    elif email == "student@just.edu.bd":
        return render(request, 'StuHome.html', {"e": email})
    elif email == "teacher@just.edu.bd":
        return render(request, 'TeaHome.html', {"e": email})

# def post_sign_in(request):
#     email = request.POST.get("iemail")
#     passw = request.POST.get('ipasss')
#     try:
#         if email.endswith("just.edu.bd"):
#             user = authe.sign_in_with_email_and_password(email, passw)
#             session_id = user['idToken']
#             request.session['uid'] = str(session_id)
#             idToken = request.session['uid']
#             a = authe.get_account_info(idToken)
#             a = a['users']
#             a = a[0]
#             email = a["email"]
#             docid = email.replace(".", "")
#             if email == "superadmin@just.edu.bd":
#                 return render(request, 'SAdminHomeTemp.html', {"e": email})
#             elif email == "admin10@just.edu.bd":
#                 return render(request, 'AdminHome.html')
#             elif email == "admin5@just.edu.bd":
#                 return render(request, 'AdminHome.html', {"e": email})
#             else:
#                 try:
#
#                     if database.child("Admins").child(docid).child('role').get().val() == "admin":
#                         return render(request, 'AdminHome.html', {"e": email})
#                     elif database.child("Students").child(docid).child('role').get().val() == "student":
#                         return render(request, 'StuHome.html', {"e": email})
#                     elif database.child("Teachers").child(docid).child('role').get().val() == "teacher":
#                         return render(request, 'TeaHome.html', {"e": email})
#                     else:
#                         return render(request, 'HomeTemp.html', {"e": email})
#                 except:
#                     return render(request, 'HomeTemp.html', {"e": email})
#     except:
#         message = 'invalid credentials'
#         return render(request, 'SignInTemp.html', {'msg': message})


def post_sign_up(request):
    name = request.POST.get('uname')
    email = request.POST.get('uemail')
    passw = request.POST.get('upasss')
    try:
        if email.endswith("just.edu.bd"):
            user = authe.create_user_with_email_and_password(email, passw)
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            docid = email.replace(".", "")
            try:
                role = database.child("users").child(docid).child("details").child('role').get().val()
                if role is None:
                    return render(request, 'HomeTemp.html', {"e": email})
                elif role == "admin":
                    return render(request, 'AdminHomeTemp.html', {"e": email})
                elif role == "student":
                    return render(request, 'StuHomeTemp.html', {"e": email})
                elif role == "teacher":
                    return render(request, 'CheHomeTemp.html', {"e": email})
            except:
                return render(request, 'HomeTemp.html', {"e": email})
    except:
        message = "Unable to create account"
        return render(request, "SignInTemp.html", {"msg": message})


def logout(request):
    auth.logout(request)
    return render(request, 'SignInTemp.html')


def admin_req(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    localid = a['localId']
    email = a["email"]
    return render(request, 'AdminReq.html', {"e": email})


def post_admin_req(request):
    import time
    from datetime import datetime, timezone
    from zoneinfo import ZoneInfo

    tz = ZoneInfo('Asia/Dhaka')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))

    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    localid = a['localId']
    email = a["email"]
    docid = email.replace(".", "")

    name = request.POST.get('fname')
    addr = request.POST.get('faddr')
    phone = request.POST.get('phone')
    pEmail = request.POST.get('fpemail')
    position = request.POST.get('fposition')

    image = request.FILES.get('fimage')

    data = {
        "email": email,
        "name": name,
        "addr": addr,
        "phone": phone,
        "pEmail": pEmail,
        "position": position,
        "lastUpdated": millis,
    }

    database.child("Admins").child(docid).update(data)
    storage.child(docid + "/profile.jpg").put(image)

    data = {
        docid: email
    }
    database.child("Requests").update(data)

    return render(request, "HomeTemp.html", {"e": email})


def admin_req_list(request):
    reqIds = database.child("Requests").shallow().get().val()
    print(reqIds)
    if reqIds is None:
        return render(request, "SAdminHomeTemp.html")
    lis_req = []
    for i in reqIds:
        lis_req.append(i)
    print(lis_req)
    names = []
    emails = []
    for i in lis_req:
        ns = database.child("Admins").child(i).child("name").get().val()
        es = database.child("Admins").child(i).child("email").get().val()
        names.append(ns)
        emails.append(es)
    xs = []
    for i in range(1, len(emails) + 1):
        xs.append(i)
    print(emails)
    comb_lis = zip(xs, emails, names)

    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    email = a['email']

    return render(request, "SAdminAReq.html", {'comb_lis': comb_lis, 'e': email})


def post_admin_req_accept(request):
    email = request.GET.get('z')
    docid = email.replace(".", "")
    data = {
        "role": "admin"
    }
    database.child("Admins").child(docid).update(data)
    database.child("Requests").child(docid).remove()
    return admin_req_list(request)


def post_admin_req_reject(request):
    email = request.GET.get('z')
    docid = email.replace(".", "")
    database.child("Requests").child(docid).remove()
    return admin_req_list(request)


def admin_list(request):
    adminIds = database.child("Admins").shallow().get().val()
    if adminIds is None:
        return render(request, "SAdminHomeTemp.html")
    lis_ad = []
    for i in adminIds:
        lis_ad.append(i)
    names = []
    emails = []
    for i in lis_ad:
        if database.child("Admins").child(i).child("role").get().val() == "admin":
            ns = database.child("Admins").child(i).child("name").get().val()
            es = database.child("Admins").child(i).child("email").get().val()
            names.append(ns)
            emails.append(es)
    xs = []
    for i in range(1, len(emails) + 1):
        xs.append(i)
    print(emails)
    comb_lis = zip(xs, emails, names)

    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    email = a['email']

    return render(request, "SAdminAList.html", {'comb_lis': comb_lis, 'e': email})


def post_admin_remove(request):
    email = request.GET.get('z')
    docid = email.replace(".", "")
    data = {
        "role": None
    }
    database.child("Admins").child(docid).update(data)
    return admin_list(request)


def add_tea(request):
    return render(request, "AddTea.html")


def post_add_tea(request):
    import time
    from datetime import datetime, timezone
    from zoneinfo import ZoneInfo

    tz = ZoneInfo('Asia/Dhaka')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))

    email = request.POST.get('femail')
    docid = email.replace(".", "")

    name = request.POST.get('fname')
    fName = request.POST.get('ffname')
    mName = request.POST.get('fmname')
    addr = request.POST.get('faddr')
    phone = request.POST.get('phone')
    pEmail = request.POST.get('fpemail')
    dob = request.POST.get('bdate')
    gender = request.POST.get('physician')
    cStatus = request.POST.get('physician1')

    roomNo = request.POST.get('froom')
    position = request.POST.get('positions')
    faculty = request.POST.get("faculties")
    dept = request.POST.get('departments')
    eduQ = request.POST.get('eduQ')

    image = request.FILES.get('fimage')

    data = {
        "email": email,
        "name": name,
        "fName": fName,
        "mName": mName,
        "addr": addr,
        "phone": phone,
        "pEmail": pEmail,
        "dob": dob,
        'gender': gender,
        "cStatus": cStatus,
        "roomNo": roomNo,
        "position": position,
        "faculty": faculty,
        "dept": dept,
        "eduQ": eduQ,
        "lastUpdated": millis,
    }

    database.child('Teachers').child(docid).update(data)
    storage.child(docid + "/profile.jpg").put(image)

    return render(request, "TeaList.html")


def add_stu(request):
    return render(request, "AddStu.html")


def post_add_stu(request):
    import time
    from datetime import datetime, timezone
    from zoneinfo import ZoneInfo

    tz = ZoneInfo('Asia/Dhaka')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))

    email = request.POST.get('femail')
    docid = email.replace(".", "")

    name = request.POST.get('fname')
    fName = request.POST.get('ffname')
    mName = request.POST.get('fmname')
    addr = request.POST.get('faddr')
    phone = request.POST.get('phone')
    pEmail = request.POST.get('fpemail')
    dob = request.POST.get('bdate')
    gender = request.POST.get('physician')
    regNo = request.POST.get('fregNo')
    acaYear = request.POST.get('aYears')
    hallS = request.POST.get('physician1')
    r11 = request.POST.get('f11')
    r12 = request.POST.get('f12')
    r21 = request.POST.get('f21')
    r22 = request.POST.get('f22')
    r31 = request.POST.get('f31')
    r32 = request.POST.get('f32')
    r41 = request.POST.get('f41')
    r42 = request.POST.get('f42')

    image = request.FILES.get('fimage')

    data = {
        "email": email,
        "name": name,
        "fName": fName,
        "mName": mName,
        "addr": addr,
        "phone": phone,
        "pEmail": pEmail,
        "dob": dob,
        'gender': gender,
        'regNo': regNo,
        "acaYear": acaYear,
        "hallS": hallS,
        "r11": r11,
        "r12": r12,
        "r21": r21,
        "r22": r22,
        "r31": r31,
        "r32": r32,
        "r41": r41,
        "r42": r42,
        "lastUpdated": millis,
    }

    database.child('Students').child(docid).update(data)
    storage.child(docid + "/profile.jpg").put(image)

    return render(request, "StuList.html")


def admin_req(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    email = a['email']
    uid = a['localId']
    print(email)
    data = {
        uid: email
    }
    database.child("Requests").update(data)
    return render(request, "AdminHome.html")


def stu_list(request):
    if request.method == 'GET' and 'csrfmiddlewaretoken' in request.GET:
        search = request.GET.get('search')
        print(search)
        return HttpResponse("got it")
    else:
        stuIds = database.child("Students").shallow().get().val()
        if stuIds is None:
            return render(request, "AddStu.html")
        lis_stu = []
        for i in stuIds:
            lis_stu.append(i)

        names = []
        rolls = []
        regs = []
        depts = []
        aYears = []
        phones = []
        addrs = []
        for i in lis_stu:
            name = database.child("Students").child(i).child('name').get().val()
            roll = i[0:6]
            reg = database.child("Students").child(i).child('regNo').get().val()
            dept = i[6:9].upper()
            aYear = database.child("Students").child(i).child('acaYear').get().val()
            phone = database.child("Students").child(i).child('phone').get().val()
            addr = database.child("Students").child(i).child('addr').get().val()
            names.append(name)
            rolls.append(roll)
            regs.append(reg)
            depts.append(dept)
            aYears.append(aYear)
            phones.append(phone)
            addrs.append(addr)

        sNos = []
        for i in range(1, len(names) + 1):
            sNos.append(i)

        comb_lis = zip(sNos, names, rolls, regs, depts, aYears, phones, addrs)
        return render(request, "StuList.html", {'comb_lis': comb_lis})


def tea_list(request):
    cheIds = database.child("Teachers").shallow().get().val()
    if cheIds is None:
        return render(request, "AddTea.html")
    lis_che = []
    for i in cheIds:
        lis_che.append(i)

    names = []
    positions = []
    depts = []
    rooms = []
    addrs = []
    phones = []
    cStatuss = []

    for i in lis_che:
        name = database.child("Teachers").child(i).child('name').get().val()
        position = database.child("Teachers").child(i).child('position').get().val()
        dept = database.child("Teachers").child(i).child('dept').get().val()
        room = database.child("Teachers").child(i).child('roomNo').get().val()
        addr = database.child("Teachers").child(i).child('addr').get().val()
        phone = database.child("Teachers").child(i).child('phone').get().val()
        cStatus = database.child("Teachers").child(i).child('cStatus').get().val()
        names.append(name)
        positions.append(position)
        depts.append(dept)
        rooms.append(room)
        phones.append(phone)
        addrs.append(addr)
        cStatuss.append(cStatus)

    sNos = []
    for i in range(1, len(names) + 1):
        sNos.append(i)

    comb_lis = zip(sNos, names, positions, depts, rooms, phones, addrs, cStatuss)
    return render(request, "TeaList.html", {'comb_lis': comb_lis})


def s_admin_stu_list(request):
    if request.method == 'GET' and 'csrfmiddlewaretoken' in request.GET:
        search = request.GET.get('search')
        print(search)
        return HttpResponse("got it")
    else:
        stuIds = database.child("Students").shallow().get().val()
        if stuIds is None:
            return render(request, "AddStu.html")
        lis_stu = []
        for i in stuIds:
            lis_stu.append(i)

        names = []
        rolls = []
        regs = []
        depts = []
        aYears = []
        phones = []
        addrs = []
        for i in lis_stu:
            name = database.child("Students").child(i).child('name').get().val()
            roll = i[0:6]
            reg = database.child("Students").child(i).child('regNo').get().val()
            dept = i[6:9].upper()
            aYear = database.child("Students").child(i).child('acaYear').get().val()
            phone = database.child("Students").child(i).child('phone').get().val()
            addr = database.child("Students").child(i).child('addr').get().val()
            names.append(name)
            rolls.append(roll)
            regs.append(reg)
            depts.append(dept)
            aYears.append(aYear)
            phones.append(phone)
            addrs.append(addr)

        sNos = []
        for i in range(1, len(names) + 1):
            sNos.append(i)

        comb_lis = zip(sNos, names, rolls, regs, depts, aYears, phones, addrs)
        return render(request, "SAdminStuList.html", {'comb_lis': comb_lis})


def s_admin_tea_list(request):
    cheIds = database.child("Teachers").shallow().get().val()
    if cheIds is None:
        return render(request, "AddTea.html")
    lis_che = []
    for i in cheIds:
        lis_che.append(i)

    names = []
    positions = []
    depts = []
    rooms = []
    addrs = []
    phones = []
    cStatuss = []

    for i in lis_che:
        name = database.child("Teachers").child(i).child('name').get().val()
        position = database.child("Teachers").child(i).child('position').get().val()
        dept = database.child("Teachers").child(i).child('dept').get().val()
        room = database.child("Teachers").child(i).child('roomNo').get().val()
        addr = database.child("Teachers").child(i).child('addr').get().val()
        phone = database.child("Teachers").child(i).child('phone').get().val()
        cStatus = database.child("Teachers").child(i).child('cStatus').get().val()
        names.append(name)
        positions.append(position)
        depts.append(dept)
        rooms.append(room)
        phones.append(phone)
        addrs.append(addr)
        cStatuss.append(cStatus)

    sNos = []
    for i in range(1, len(names) + 1):
        sNos.append(i)

    comb_lis = zip(sNos, names, positions, depts, rooms, phones, addrs, cStatuss)
    return render(request, "SAdminTeaList.html", {'comb_lis': comb_lis})