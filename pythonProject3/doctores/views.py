from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from doctores.functions import handle_uploaded_file
from doctores.form import DoctorForm
from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages






def index(request):

    if request.method == 'POST':
        doctor = DoctorForm(request.POST, request.FILES)


        if doctor.is_valid():

            doctor.save()

            with connection.cursor() as cursor:
                email=request.POST['email']
                cursor.execute(f"select * from doctor where email=\'{email}\'")
                doctorobj=cursor.fetchall()
                cursor.execute(f"select docid from doctor where email=\'{email}\'")
                doc_ID=cursor.fetchone()
                request.session['Doctor_ID']=doc_ID[0]



            return render(request,'Doctor_home.html',{'form':doctorobj})



    doctor = DoctorForm()
    messages.info(request,"Email is taken or faulty data entry occured")
    return render(request,"doctorform.html",{'form':doctor})



def Update_doctor_info(request):
    return HttpResponse("This is DoctorHome")



def show_patients(request):
    Doctor_ID=request.session['Doctor_ID']
    print(Doctor_ID)
    with connection.cursor() as cursor:

        output_cursor=connection.cursor()
        sql_query=f"""SELECT *
                        FROM patient
                        WHERE id IN (SELECT Patient_ID_ID FROM appointment WHERE doctor_ID_ID = {Doctor_ID});"""
        #cursor.callproc('GetPatientsofDoctor',[1,output_cursor])
        #cursor.execute('GetPatientsofDoctor')
        #patient=cursor.callfunc('GetPatientsByDoctor',1)
        cursor.execute(sql_query)
        patient= cursor.fetchall()
        print(patient)

    return render(request,"Show_patients.html",{'patient':patient})


def test(request,id):

    with connection.cursor() as cursor:
        Doctor_ID=request.session['Doctor_ID']
        sql_query=f'select * from patient where ID={id}'
        print(sql_query)
        cursor.execute(sql_query)
        patient_info=cursor.fetchall()
        print(sql_query)
        sql_query2=f'select * from doctor_patient_test where Patient_ID={id}'

        cursor.execute(sql_query2)
        patient_test=cursor.fetchall()
        print(sql_query2)
        doctor={
            'patient_info':patient_info,
            'patient_test':patient_test,
        }



    return render(request,"tests.html",doctor)

def loginpage(request):
    return render (request,"doctor_loginpage.html")

def login_verify(request):
    if request.method=="GET":
        request.sesion['login_status']=False

        render(request,'doctor_loginpage.html')

    else :
        email=request.POST['email']

        password=request.POST['password']



        with connection.cursor() as cursor:
            sql_query=f'select docid from doctor where password=\'{password}\' and email=\'{email}\';'
            print(sql_query)
            cursor.execute(sql_query)
            ID=cursor.fetchone()

            id=int(0 if ID is None else ID[0])
            if(id >=1):
                request.session['login_status']=True
                sql_query=f"select * from doctor where email=\'{email}\' and password=\'{password}\';"
                print(sql_query)
                cursor.execute(sql_query)
                doctor_info=cursor.fetchall()
                request.session['Doctor_ID']=id
               # print(patient_info)
                return render(request,'Doctor_home.html',{'form':doctor_info})

            else :
                messages.info(request,"faulty email or password")
                return render (request,'doctor_loginpage.html')


def test_list(request,id):
    Doctor_ID=request.session['Doctor_ID']
    request.session['Patient_ID']=id




    with connection.cursor() as cursor:
        sql_query=f"""(SELECT test_name, test_type, id FROM Test) 
        minus 
        (SELECT TEST_NAME, test_type, id FROM Test t JOIN 
        Doctor_patient_test D ON t.id = D.test_id WHERE patient_ID = {id} AND Doctor_id = {Doctor_ID})
         minus 
         (select Test_name,test_type,id
         from test
         join 
         Sample_Collector_Nurse_Patient_TEST
         ON
         patient_ID={id}
         )
          """

        cursor.execute(sql_query)
        tests=cursor.fetchall()

        sql_query2=f'SELECT TEST_NAME,test_type,id FROM Test t JOIN Doctor_patient_test D ON  t.id =D.test_id where patient_ID={id} and Doctor_id={Doctor_ID}'
        cursor.execute(sql_query2)
        test_to_remove=cursor.fetchall()


        test_list={
            'test':tests,
            'patient_id':id,
            'test_to_remove':test_to_remove
  }

    return  render(request,'test_list.html',test_list)

def remove_test(request,id):

    Doctor_ID=request.session['Doctor_ID']
    Patient_ID=request.session['Patient_ID']

    with connection.cursor() as cursor:
        sql_query=f'DELETE FROM Doctor_patient_test WHERE Doctor_ID = {Doctor_ID} AND Patient_ID = {Patient_ID} AND test_id = {id}'
        cursor.execute(sql_query)


    return redirect(test_list,id=Patient_ID)




def add_test(request,id):

    Doctor_ID=request.session['Doctor_ID']
    Patient_ID=request.session['Patient_ID']

    with connection.cursor() as cursor:
        sql_query=f'Insert into Doctor_patient_test values({Doctor_ID},{Patient_ID},{id})'
        cursor.execute(sql_query)


    return redirect(test_list,id=Patient_ID)

def see_report(request,id):
    with connection.cursor() as cursor:
        sql_query=f"""select (select name from patient
         where id=r.patient_ID),(select name from sample where id=r.sample_ID),Hand_report 
         from report  r where 
        patient_ID={id}
        """
        cursor.execute(sql_query)
        report=cursor.fetchall()
        return render(request,'report.html',{'report':report})

