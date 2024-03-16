# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from doctores.functions import handle_uploaded_file

from django.db import connection
from django.shortcuts import redirect
from .models import pathologistForm
from .models import pathologistlogin


def loginpage(request):

    if request.method == 'POST':
        pathologist = pathologistlogin(request.POST)


        if pathologist.is_valid():

           email=request.POST['email']
           password=request.POST['password']


           with connection.cursor() as cursor :

               sql_query=f"""select password from pathologist
               where email='{email}'
               """
               cursor.execute(sql_query)
               password1=cursor.fetchone()
               if password1 == None :
                   messages.info(request,"Email or password is wrong")

                   return redirect(loginpage)

               if password1[0] != password :
                   print(password)
                   print(password)
                   messages.info(request,"email or password is wrong")

                   return redirect(loginpage)



               sql_query=f"""select * from pathologist 
               where email='{email}'
               """
               cursor.execute(sql_query)
               pathologist=cursor.fetchall()
               request.session['pathologist']=pathologist[0][0]
               S=request.session['pathologist']
               print(S)



               return  render(request,'pathologist_home.html',{'pathologist':pathologist})

    pathologist=pathologistlogin()
    return render(request,'pathologist_login.html',{'form':pathologist})



def registration(request):

    if request.method == 'POST':
        pathologist = pathologistForm(request.POST)


        if pathologist.is_valid():
           Name=request.POST['name']
           email=request.POST['email']
           password=request.POST['password']
           field=request.POST['field']

           with connection.cursor() as cursor :
               sql_query=f"""select * from pathologist 
               where email='{email}'
               """
               cursor.execute(sql_query)
               pathologist=cursor.fetchall()
               if pathologist == None :
                cursor.callproc('Insertpathologist',[Name,email,password,field])

                request.session['pathologist']=pathologist[0][0]

                return  render(request,'pathologist_home.html',{'pathologist':pathologist})

    pathologist=pathologistForm()
    messages.info(request,"Wrong data input .maybe email is taken")
    return render(request,'pathologist_form.html',{'form':pathologist})

def sample_list(request):
    id=request.session['pathologist']

    with connection.cursor() as cursor:
        sql_query=f"""select s.name,(select name from patient where ps.patient_ID=patient.ID),
        ps.patient_ID,ps.Sample_ID from
        pathologist_patient_sample ps
        join sample s
        on ps.sample_id=s.id
        where ps.pathologist_id={id}
        """
        cursor.execute(sql_query)
        samples=cursor.fetchall()
        print(samples)

        return render(request,'pathologist_list.html',{'sample':samples})

def generate_report(request):
    print(1)
    id=request.session['pathologist']
    order=request.POST.getlist('order_list')
    print("ENTE")
    report=request.POST.get('report')
    print("ENTERED")
    if report is None:
        report='No Comments'
    print(report)
    print(order)

    with connection.cursor() as cursor:
        sample_ID,patient_ID = zip(*(s.split(" ") for s in order))
        print(sample_ID)
        print(patient_ID)

        for sample ,patient in zip(sample_ID,patient_ID):

            cursor.callproc('insert_into_report',[patient,sample,report])
            cursor.callproc('delete_sample',[id,patient,sample])

    sql_query=f"""sample_ID,select patient_ID,(select name from patient p where p.id=r.patient_ID ),
    (select name from sample s where s.id=r.sample_ID )
    where patient_ID={patient_ID[0]}"""
    cursor.execute(sql_query)
    report_generated=cursor.fetchall()
    print(report_generated)



    return redirect(sample_list)

