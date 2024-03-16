from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from doctores.functions import handle_uploaded_file
from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect
from .models import SampleCollectorForm
from .models import SampleCollectorlogin


def loginpage(request):

    if request.method == 'POST':
        SampleCollector = SampleCollectorlogin(request.POST)


        if SampleCollector.is_valid():

           email=request.POST['email']
           password=request.POST['password']

           with connection.cursor() as cursor :

               sql_query=f"""select password from sample_Collector 
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
                   messages.info(request,"Email or password is wrong")

                   return redirect(loginpage)



               sql_query=f"""select * from sample_Collector 
               where email='{email}'
               """
               cursor.execute(sql_query)
               SampleCollector=cursor.fetchall()
               request.session['SampleCollector_ID']=SampleCollector[0][0]
               S=request.session['SampleCollector_ID']
               print(S)



               return  render(request,'sample_collector_home.html',{'sample_collector':SampleCollector})

    SampleCollector=SampleCollectorlogin()
    return render(request,'sample_collector_login.html',{'form':SampleCollector})



def registration(request):

    if request.method == 'POST':
        SampleCollector = SampleCollectorForm(request.POST)


        if SampleCollector.is_valid():
           CollectorName=request.POST['CollectorName']
           email=request.POST['email']
           password=request.POST['password']

           with connection.cursor() as cursor :
               sql_query=f"""select * from sample_Collector 
               where email='{email}'
               """
               cursor.execute(sql_query)
               SampleCollector=cursor.fetchall()
               if SampleCollector == None :
                cursor.callproc('InsertSampleCollector',[CollectorName,email,password])

                request.session['SampleCollector_ID']=SampleCollector[0][0]

                return  render(request,'sample_collector_home.html',{'sample_collector':SampleCollector})

    SampleCollector=SampleCollectorForm()
    messages.info(request,"Wrong data input .maybe email is taken")
    return render(request,'sample_collector_form.html',{'form':SampleCollector})


def sample_list(request):
    samplecollector_ID=request.session['SampleCollector_ID']
    with connection.cursor() as cursor:
        sql_query=f"""SELECT p.name,p.adress,s.name,sp.patient_id,sp.sample_id,sp.test_ID,sp.nurse_ID  as sample_name
                      FROM sample_collector_nurse_patient_test sp
                      JOIN patient p ON sp.patient_ID = p.ID
                      JOIN sample s ON sp.sample_ID=s.ID
                      WHERE sp.sample_collector_ID = {samplecollector_ID}
                      and
                      sp.status='ORDERED'
                      """




        cursor.execute(sql_query)
        Sample_Collector=cursor.fetchall()

        sql_query2=f"""SELECT p.name,p.adress,s.name,p.id,s.id  as sample_name,sp.test_ID,sp.nurse_ID
                      FROM sample_collector_nurse_patient_test sp
                      JOIN patient p ON sp.patient_ID = p.ID
                      JOIN sample s ON sp.sample_ID=s.ID
                      WHERE sp.sample_collector_ID = {samplecollector_ID}
                      and
                      sp.status='COLLECTED'
                      """
        cursor.execute(sql_query2)
        Sample_Collected=cursor.fetchall()
        print(Sample_Collector)
        print(Sample_Collected)


        return render(request,'sample_list.html',{'form':Sample_Collector,'Sample_Collected':Sample_Collected})



def collect_sample(request):

    patient_sample_list=request.POST.getlist('sample')
    print(patient_sample_list)

    patient_ID,sample_ID,test_ID,nurse_ID = zip(*(s.split(" ") for s in patient_sample_list))
    print(patient_ID)
    print(sample_ID)
    print(test_ID)
    print(nurse_ID)



    with connection.cursor() as cursor:
        cursor.callproc('update_status_to_collected',[test_ID[0],patient_ID[0],nurse_ID[0],sample_ID[0]])


    return redirect(sample_list)







