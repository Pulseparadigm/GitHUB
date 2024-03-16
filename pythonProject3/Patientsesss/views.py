from django.shortcuts import render


from datetime import datetime
from django.shortcuts import HttpResponse
from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages


# Create your views here.



def registration(request):
     if request.method == 'GET':
        return redirect(patient_form)

     name=request.POST['name']
     #dob=datetime.strptime((request.POST['dob']),'%d-%m-%y').date()
     adress=request.POST['adress']
     dob=(request.POST['dob'])
     print(dob)

     phone=int(request.POST['phone'])
     medical_history=request.POST['medical_history']
     password=request.POST['password']
     password2=request.POST['password2']
     email=request.POST['email']
     if(password!=password2 and password2 is not None) :
         messages.error(request,"Password don't match or empty")
         return redirect(patient_form)





     with connection.cursor() as cursor:

         sql_query=f"""select email from patient where email='{email}'"""
         cursor.execute(sql_query)
         emailrepeat=cursor.fetchone()
         if emailrepeat[0] is not None:
            messages.error(request,"Email is taken")
            return redirect(patient_form)



         sql_query=f"""insert into patient(name,date_of_birth,adress,phone,medical_History,password,email) 
         values('{name}',to_date('{dob}'),'{adress}','{phone}','{medical_history}','{password}','{email}')"""
         print(sql_query)
         cursor.execute(sql_query)

         sql_query=f"select * from patient where email='{email}';"
         print(sql_query)


         cursor.execute(sql_query)
         patient=cursor.fetchall()
         sql_query2=f"select id from patient where email='{email}';"

         cursor.execute(sql_query2)
         registration_number=cursor.fetchall()
         print(sql_query)



     #Patient1=Patient(name=name,date_of_birth=dob,adress=adress,phone=phone,medical_history=medical_history)
     #Patient1.save();

     request.session['Registration_Number']=registration_number
     request.session['login_status']=True

     return render(request,'patient_home.html',{'patient_data':patient})



def login(request):
    return render(request,'loginpage.html')

def patient_form(request):
     return render(request,'form.html')

def patient_home_showDoc(request):

     if request.session['login_status']== False :
         return redirect(login)
     with connection.cursor() as cursor:
                cursor.execute("Select * From doctor")
                members=cursor.fetchall()





     return render(request,'Patient_Home_ShowDoc.html',{'member':members})


def filter(request):
        name=request.POST['name']

        if (name ==''):
             with connection.cursor() as cursor:
                #sql_query="select * from patient where name=\'%s\';"
                #cursor.execute(sql_query,name)
                cursor.execute("select * from doctor")
                print("THIS IS WRONG1")

                members=cursor.fetchall()

             return render(request,'Patient_Home_ShowDoc.html',{'member':members})




        else:
            with connection.cursor() as cursor:
                print("THIS IS WRONG2")
                sql_query=f"select * from doctor where firstname Like '%{name}%' Or lastname Like '%{name}%' " \
                          f"or Concat(firstname, lastname) like '%{name}%';"
                print(sql_query)
                cursor.execute(sql_query)
                print(sql_query)

                members=cursor.fetchall()
                print(members)
            return render(request,'Patient_Home_ShowDoc.html',{'member':members})

      #else:

       #     with connection.cursor() as cursor:
        #        cursor.execute("select * from patients")
         #       members=cursor.fetchall()
          #  return render(request,'filter.html',{'member':members})


def patient_Home(request):

    if( request.method=="GET"):
        return redirect(login)

    if request.session['login_status']==True :

        id=request.session['Registration_Number']

        with connection.cursor() as cursor:
            sql_query=f'select * from patient where id={id};'
            cursor.execute(sql_query)
            patient=cursor.fetchall()

        render(request,'patient_home.html',{'patient_data':patient})

    else :
        return redirect(login)


def login_verify(request):
    if request.method=="GET":
        request.sesion['login_status']=False

        return  render(request,'loginpage.html')

    else :
        email=request.POST['email']

        password=request.POST['password']

        with connection.cursor() as cursor:
            sql_query=f'select id from patient where password=\'{password}\' and email=\'{email}\';'
            print(sql_query)
            cursor.execute(sql_query)
            ID=cursor.fetchone()

            id=int(0 if ID is None else ID[0])
            if(id >=1):
                request.session['login_status']=True
                sql_query=f"select * from patient where email=\'{email}\' and password=\'{password}\';"
                print(sql_query)
                cursor.execute(sql_query)
                patient_info=cursor.fetchall()
                request.session['Registration_Number']=id
               # print(patient_info)
                return render(request,'patient_home.html',{'patient_data':patient_info})

            else :
                messages.error(request,"Password or Email is wrong input")

                return render (request,'loginpage.html')



def Update_Patient_info(request):
    if(request.method=='POST'):
        name=request.POST['name']
       # dob=request.POST['dob']
        adress=request.POST['adress']
        phone=int(request.POST['phone'])
        medical_history=request.POST['medical_history']
        password=request.POST['password']
        id=int(request.session['Registration_Number'])

        with connection.cursor() as cursor:
            sql_query=f"""UPDATE patient SET name = '{name}',
            adress = '{adress}', phone = {phone}, medical_history = '{medical_history}',
            password = '{password}' where id = {id} """
            print(sql_query)
            cursor.execute(sql_query)
            sql_query=f"select * from patient where id={id} ;"
            print(sql_query)
            cursor.execute(sql_query)
            patient_info=cursor.fetchall()





        return render(request,'patient_Home.html',{'patient_data':patient_info})


def Upadte_PatientForm(request):
     if(request.session['login_status']==True):
        print("This line printed")
        registration=request.session['Registration_Number']
        print(registration)
        with connection.cursor() as cursor:
            sql_query=f"select * from patient where id={registration}"
            cursor.execute(sql_query)
            patient_info=cursor.fetchall()

        print(patient_info)
        return render(request,'Update_Patientinfo.html',{'data':patient_info})


def view_appointment(request,id):

    with connection.cursor() as cursor:
        sql_query=f"""select a.date_and_time,
        (select (firstname ||' '||lastname) from doctor where docid=a.doctor_ID_ID),
        (select email from doctor where docid=a.doctor_ID_ID) 
        from appointment a where a.patient_ID_id={id}"""
        cursor.execute(sql_query)
        appointment=cursor.fetchall()

        return render(request,'viewappointments.html',{'appointment':appointment})


def booking_appointment(request,docID):

    if request.session['login_status']==False:

        return redirect(login)
    #book an appointment
    else :
        #return HttpResponse("docID")

        patientID=request.session['Registration_Number']


        sql_query1=f'select name from patient where id={patientID}'
        sql_query2=f'select lastname from doctor where docid={docID}'
        print("HELLO")
        date='2024-December-24'








        with connection.cursor() as cursor:

            cursor.execute(sql_query1)
            print("HELLO1")



            patient_name=cursor.fetchall()
            cursor.execute(sql_query2)
            print("HELLO2")
            doc_name=cursor.fetchall()
            print("HELLO3")
            print(f'{docID}')
            print(f'{patientID}')
            sql_query3=f'select ID from appointment where patient_ID_ID={patientID} and doctor_ID_ID={docID}'
            cursor.execute(sql_query3)
            appointment=cursor.fetchone()

            if appointment is  None:
                sql_query=f"""Insert into Appointment 
                (date_and_time,Doctor_ID_ID,patient_ID_ID,visit)
                 values('{date}','{docID}','{patientID}','hello')"""
                cursor.execute(sql_query)


            sql_query3=f"""select  Date_and_Time ,
            (select (d1.firstname|| ' '||d1.lastname)   from doctor d1 where d1.docID=a.Doctor_ID_ID) 
             from Appointment a where a.Patient_ID_ID='{patientID}'"""
            cursor.execute(sql_query3)
            appointments=cursor.fetchall()

            return render(request,'Appointments.html',{'appointments':appointments})



def view_test(request):
    patient_ID=request.session['Registration_Number']
    print(patient_ID)

    with connection.cursor() as cursor:
        sql_query=f"""select test_name,test_type,id  from Test t
         where  t.ID in 
         (select test_id from Doctor_patient_test t1 where t1.patient_ID={patient_ID} and t.id=t1.test_id) 
         minus 
         (select test_name,test_type,id from test t where 
          EXISTS
           (select test_id from Nurse_patient_Test where t.id=test_id))"""
        cursor.execute(sql_query)
        test=cursor.fetchall()
        sql_query2=f"""select test_name,test_type,id  from Test t 
        where  t.ID in
         (select test_id from Doctor_patient_test t1 where t1.patient_ID={patient_ID} and t.id=t1.test_id)
          minus
           (select test_name,test_type,id from test t where 
           NOT EXISTS
            (select test_id from Nurse_patient_Test where t.id=test_id))"""
        cursor.execute(sql_query2)
        test_ordered=cursor.fetchall()


        return render(request,'view_test.html',{'tests':test,'test_ordered':test_ordered})

def order_test(request,id):

    test_id=id
    patient_ID=request.session['Registration_Number']


    with connection.cursor() as cursor:
        nurse_ID=cursor.callfunc("find_nurse_id",int,[patient_ID])


        if nurse_ID == 0 :
            nurse_ID=cursor.callfunc("get_available_nurse_id",int,[patient_ID])



        cursor.callproc("InsertIntoNursePatientTest",[nurse_ID,patient_ID,test_id])
        #make a procedure which calls the nurse having orders of that patient else having least orders
        #return id of the nure from that procedure
        #use the id to insert the tests in the table


        return redirect(view_test)

