from django.shortcuts import render
from .models import *
from  django.db import connection
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.
global_counter1=0

def nurse_form(request):

    if request.method == 'POST':

        name=request.POST['Name']
        password=request.POST['password']
        email=request.POST['email']
        department=request.POST['Department']
        contactinfo=request.POST['ContactInfo']
        salary=request.POST['Salary']
        schedule=request.POST['Schedule']


        with connection.cursor() as cursor:

                sql_query=f"INSERT INTO NURSE(NAME, PASSWORD, EMAIL, DEPARTMENT, CONTACTINFO, SALARY, JOIN_DATE) VALUES ('{name}', '{password}', '{email}', '{department}', {contactinfo}, {salary},SYSDATE);"
                cursor.execute(sql_query)
                email=request.POST['email']
                cursor.execute(f"select * from nurse where name=\'{email}\'")
                nurse=cursor.fetchall()
                sql_query2=f"select id from nurse where email='{request.POST['email']}'"
                cursor.execute(sql_query2)
                nurse_id=cursor.fetchone()
                request.session['Nurse_ID']=nurse_id[0]




        return render(request,'nurse_home.html',{'nurse':nurse})



    nurse = NurseForm()
    messages.info(request,"Faulty data Entry")
    return render(request,"nurse_form.html",{'nurse':nurse})

def nurse_login(request):

    if request.method=='GET' :

        nurse=nurse_login_form()

        return render(request,'nurse_login_page.html',{'nurse':nurse})

    if request.method=='POST' :


        with connection.cursor() as cursor:


                email=request.POST['email']
                sql_query=f"select password from nurse where email=\'{email}\'"
                cursor.execute(sql_query)
                Password=cursor.fetchone()
                if Password is None :
                    nurse=nurse_login_form()
                    messages.info(request,"Email or password is wrong")
                    return render(request,'nurse_login_page.html',{'nurse':nurse})



                if(Password[0] != (request.POST['password'])) :
                    nurse=nurse_login_form()
                    print(request.POST['password'])
                    messages.info(request,"Email or password is wrong")



                    return render(request,'nurse_login_page.html',{'nurse':nurse})


                cursor.execute(f"select * from nurse where email=\'{email}\'")
                nurse=cursor.fetchall()
                sql_query2=f"select id from nurse where email='{request.POST['email']}'"
                cursor.execute(sql_query2)
                nurse_id=cursor.fetchone()
                request.session['Nurse_ID']=nurse_id[0]

        return render(request,'nurse_home.html',{'nurse':nurse})


global_counter=0
def  show_order(request):

    nurse_id=request.session['Nurse_ID']
    global global_counter
    global_counter=0



    with connection.cursor() as cursor :
        sql_query=f"""
                SELECT t.test_type,t.test_name,p.id,p.name, t.id
                FROM NURSE_PATIENT_TEST npt
                    JOIN PATIENT p ON npt.PATIENT_ID = p.ID
                    Join test t on npt.test_ID=t.id
                WHERE nurse_ID={nurse_id} and NOT EXISTS (
                SELECT 1
                FROM SAMPLE_COLLECTOR_NURSE_PATIENT_TEST scnpt
                WHERE scnpt.NURSE_ID = npt.NURSE_ID
                 AND scnpt.PATIENT_ID = npt.PATIENT_ID
                AND scnpt.TEST_ID = npt.TEST_ID)
    
         """



        cursor.execute(sql_query)
        nurse_test=cursor.fetchall()
        sql_query2=f"""SELECT t.test_type,t.test_name,p.id,p.name, t.id
                        FROM NURSE_PATIENT_TEST npt
                        JOIN PATIENT p ON npt.PATIENT_ID = p.ID
                        Join test t on npt.test_ID=t.id
                        WHERE nurse_ID={nurse_id} and  EXISTS (
                        SELECT 1
                         FROM SAMPLE_COLLECTOR_NURSE_PATIENT_TEST scnpt
                        WHERE scnpt.NURSE_ID = npt.NURSE_ID
                        AND scnpt.PATIENT_ID = npt.PATIENT_ID
                        AND scnpt.TEST_ID = npt.TEST_ID
		                and scnpt.status='ORDERED')
         """
        cursor.execute(sql_query2)
        nurse_test_ordered=cursor.fetchall()
        sql_query3=f"""select * from sample"""
        cursor.execute(sql_query3)
        sample=cursor.fetchall()


        return render(request,'nurse_test_order.html',
                        {'nurse':nurse_test,'nurse_test_ordered':nurse_test_ordered,'sample':sample})



def give_order(request):
    global global_counter
    print(global_counter)
    if request.method =='GET' :
       return  redirect(show_order)
    elif global_counter == 1:

         with connection.cursor() as cursor :
            cursor.callproc('DeleteTemporaryOrders')
            global_counter=0

            return redirect(show_order)

    order_list=request.POST.getlist('order_list')
    print("ENTERED")
    print(order_list)

    if len(order_list) ==0 :
        return redirect(show_order)


    orders_list,patient_ID_list,sample_list = zip(*(s.split(" ") for s in order_list))
    print(orders_list)
    print(patient_ID_list)
    print(sample_list)


    with connection.cursor() as cursor:
        sql_query="select * from sample_collector"
        cursor.execute(sql_query)
        sample_collector=cursor.fetchall()
        for (orders,patient_ID,sample) in zip(orders_list,patient_ID_list,sample_list):
            print(global_counter)

            cursor.callproc('InsertTemporaryOrder',[orders,patient_ID,sample])
            global_counter=1
            print(global_counter)

            #connection.commit()
        return render(request,'sample_collector.html',{'sample_collector':sample_collector})


def sample_collector_took_order(request):

    global global_counter
    if request.method =='GET' :
        return redirect(show_order)
    ordered_ID=request.POST.get('ordered_ID')
    nurse_ID=request.session['Nurse_ID']
    print(ordered_ID)
    with connection.cursor() as cursor :
        if ordered_ID == None :
            global_counter=0
            print(f'HEllo')
            cursor.callproc('DeleteTemporaryOrders')
            redirect(show_order)

    with connection.cursor() as cursor :
        sql_query=f"""
                    select * 
                    from temporary_orders"""
        cursor.execute(sql_query)
        temporary_orders=cursor.fetchall()
        print(ordered_ID)
        cursor.callproc('DeleteTemporaryOrders')
        global_counter=0
        print(temporary_orders)
        print(ordered_ID)
        for orders in temporary_orders :

            cursor.callproc('InsertIntoSample_Collector_Nurse_Patient_Test',[nurse_ID,orders[1],orders[0],ordered_ID,orders[2]])


        return redirect(show_order)



def nurse_test_collected(request):
    nurse_id=request.session['Nurse_ID']




    with connection.cursor() as cursor :

        sql_query4=f"""SELECT t.test_name,s.name,p.id,p.name, t.id,s.id
                        FROM sample_collector_nurse_patient_test npt
                        JOIN PATIENT p ON npt.PATIENT_ID = p.ID
                        Join test t on npt.test_ID=t.ID
                        join sample s on s.id=npt.sample_ID
                        WHERE npt.nurse_ID={nurse_id} and 
                        npt.status='COLLECTED'
         """
        cursor.execute(sql_query4)
        nurse_sample_collected=cursor.fetchall()
        print(nurse_sample_collected)


        sql_query5="""Select id from
        sample_collector_nurse_patient_test"""
        cursor.execute(sql_query4)
        sample=cursor.fetchall()
        print(sample)


        return render(request,'nurse_test_collected.html',
                        {'nurse_sample_collected':nurse_sample_collected,'sample':sample})


def send_sample_to_lab(request):
    global global_counter1
    print(global_counter1)
    if request.method =='GET' :
       return  redirect(nurse_test_collected)
    elif global_counter1 == 1:

         with connection.cursor() as cursor :
            cursor.callproc('Delete_from_Temporary_Sample')
            global_counter1=0

            return redirect(nurse_test_collected)

    order_list=request.POST.getlist('order_list')
    print(order_list)
    if len(order_list) ==0 :
        return redirect(show_order)


    orders_list,patient_ID_list,sample_list = zip(*(s.split(" ") for s in order_list))
    print(orders_list)
    print(patient_ID_list)
    print(sample_list)


    with connection.cursor() as cursor:
        for (orders,patient_ID,sample) in zip(orders_list,patient_ID_list,sample_list):



            global_counter1=1
            print(global_counter1)
            print(sample)
            sql_query=f"""select * 
            from pathologist
            where field IN
            (select name from sample
            where id='{sample}'
            )
            """
            cursor.execute(sql_query)
            pathologist=cursor.fetchall()
            print(pathologist)
            cursor.callproc('Insert_into_Temporary_Sample',[orders,patient_ID,sample])

            #connection.commit()
        return render(request,'pathologist_sample_list.html',{'pathologist':pathologist})

def pathologist_took_order(request):

    global global_counter1
    if request.method =='GET' :
        return redirect(nurse_test_collected)
    ordered_ID=request.POST.get('ordered_ID')
    nurse_ID=request.session['Nurse_ID']
    print(ordered_ID)
    with connection.cursor() as cursor :
        if ordered_ID == None :
            global_counter1=0
            print(f'HEllo')
            cursor.callproc('Delete_from_Temporary_Samples')
            redirect(show_order)

    with connection.cursor() as cursor :
         sql_query=f"""
                    select * 
                    from temporary_sample"""
         cursor.execute(sql_query)
         temporary_orders=cursor.fetchone()

         print(temporary_orders)
         cursor.callproc('Insert_pathologist_patient_sample',[ordered_ID,temporary_orders[1],temporary_orders[2]])
         print(temporary_orders[0],temporary_orders[1],nurse_ID,temporary_orders[2])
         cursor.callproc('update_status_to_sent',[temporary_orders[0],temporary_orders[1],nurse_ID,temporary_orders[2]])
         connection.commit()

         cursor.callproc('Delete_from_Temporary_SAmple')
         global_counter1=0
         print(temporary_orders)
         print(ordered_ID)

         return redirect(nurse_test_collected)




