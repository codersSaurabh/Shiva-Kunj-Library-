import random
import smtplib
from django.utils import timezone

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login 
from django.http import HttpResponse
from .models import Booking
import requests
from datetime import timedelta
from django.contrib import messages


otp_store = {}
#calling index page
def index(request):
    
    return render(request, 'main/index.html')
#calling booking
def book(request):
    shift = request.GET.get('shift')
    sheet_no = request.GET.get('sheet_no')
    return render(request, 'main/booking.html',{'sheet_no': sheet_no,'shift': shift,'error':False})
def send_msg_to_mobile(email,msg):
    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('njneha.1590@gmail.com' , 'pzoz ulqp fujw lsop')
        server.sendmail("njneha.1590@gmail.com",email,msg)
    except Exception as e:
        return HttpResponse("Email is not valid")

    
#send otp
def send_otp(request):
    if request.method == 'POST':
        sheet_number=request.POST.get('sheet_no')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email=request.POST.get('email')
        aadhar = request.POST.get('aadhar')
        shift = request.POST.get('shift')
        found = Booking.objects.filter(aadhar=aadhar)
        if found:
            return render(request,'main/booking.html',{'sheet_no': sheet_number,'shift': shift,'error':True})
        request.session['verified_email'] = email

        otp = str(random.randint(100000, 999999))
        msg="Dear candidate your one time password for email verification is "+otp+".\n\nShiva Kunj Library"
        send_msg_to_mobile(email,msg)
        otp_store[email] = {
            'otp': otp,
            'name': name,
            'mobile': mobile,
            'aadhar': aadhar,
            'shift': shift,
            'email':email,
            'sheet_number':sheet_number,
        }
        
        return render(request, 'main/verify_otp.html', {'email': email})
#verif otp
def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        entered_otp = request.POST.get('otp')

        data = otp_store.get(email)
        if data and data['otp'] == entered_otp:
            request.session['verified_email'] =email
            request.session['name'] = data['name']
            request.session['aadhar'] = data['aadhar']
            request.session['shift'] = data['shift']

            Booking.objects.create(
                name=data['name'],
                mobile=data['mobile'],
                aadhar=data['aadhar'],
                shift=data['shift'],
                email=data['email'],
                sheet_number=data['sheet_number']
                
            )
            msg=data['name']+' Your Sheet '+data['sheet_number']+' at Shiva Kunj Library has been confirmed!!\n\nShiva Kunj Library'
            send_msg_to_mobile(data['email'],msg)

            # Clear session
            # del request.session['otp']
            
            return render(request, "main/sucess.html", {'name': data['name'],'sheet_no':data['sheet_number']})
        else:
            return render(request, 'main/verify_otp.html', {'error': 'Invalid OTP', 'email':email})
    return render(request, "main/verify_otp.html")
#admin portal
def admin(request):
    if 'user' in request.session:
        students = Booking.objects.all()
        return render(request, 'main/admin.html', {'students': students})
        
        #admin portal
    
    if(request.method=='POST'):
        username = request.POST.get("username","")  
        password = request.POST.get("password","")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("user found")
            login(request, user)
            request.session['user'] = username
            students = Booking.objects.all()
            return render(request, 'main/admin.html', {'students': students})
        
            #same admin portal
        else:
            return render(request,'main/admin-login.html',{'msg':'username or password is not valid'})
    return render(request,'main/admin-login.html')
#logout admin
def logout(request):
    try:
        del request.session['user']
    except:
        return redirect("/")
    return redirect("/")

# admin_fee
def admin_fee(request):
    query = request.GET.get('q', '')
    try:
        if query:
            if query.isalpha():
                students = Booking.objects.filter(name=query)
            else:
                students = Booking.objects.filter(sheet_number=query)
            
        else:
            students = Booking.objects.all()
    except Exception as e:
                    students = Booking.objects.all()
        
   
    return render(request, 'main/fees.html', {'students': students})
#fee status update
def mark_paid(request, id):
    student = get_object_or_404(Booking, id=id)
    student.fee_status = 'Paid'
    student.save()
    return redirect('admin_fee')
#sheet matrix
def admin_sheets(request):
    total_sheets = 108
    matrix = []

    for sheet_no in range(1, total_sheets + 1):
        # Get all bookings for this sheet
        bookings = Booking.objects.filter(sheet_number=sheet_no)

        # Initialize shift status
        morning = evening = 'vacant'

        for booking in bookings:
            shift = booking.shift.lower()
            if shift == 'full_day':
                morning = evening = 'full'
                break  # no need to check further
            elif shift == 'morning':
                morning = 'full'
            elif shift == 'evening':
                evening = 'full'

        matrix.append({
            'sheet_no': sheet_no,
            'morning': morning,
            'evening': evening,
        })

    return render(request, 'main/sheet_status.html', {'matrix': matrix})



#remove_Student
def remove_student(request, id):
    student = get_object_or_404(Booking, id=id)
    student.delete()
    return redirect('admin-login')
#send reminder
def send_reminder(request):
    today = timezone.now().date()

    # Fetch bookings where one month has passed and fee is still marked as paid
    due_bookings = Booking.objects.filter(fee_status='Paid')
    count = 0
    print(len(due_bookings))
    for booking in due_bookings:
        booking_date = booking.booking_date.date()
        if booking_date + timedelta(days=30) == today:
            
            # Update status
            booking.fee_status = 'Unpaid'
            booking.save()

            # Send SMS
           
            msg = f"Dear {booking.name}, your monthly fee is now due. Please pay to continue using Shiva Kunj Library.\
If You had already pay ignore this reminder.\n \nShiva Kunj Lybrary"
            send_msg_to_mobile({booking.email},msg)  
            count += 1
        

    messages.success(request, f"✅ Sent {count} reminder(s).")
    return redirect('admin-login')  # replace with your actual admin dashboard url name
def admin_search(request):
    query = request.GET.get('q')
    students = []
    try:
        if query:
            if query.isalpha():
                students = Booking.objects.filter(name=query)
            else:
                students = Booking.objects.filter(sheet_number=query)
            
        else:
            students = Booking.objects.all()
    except Exception as e:
                    students = Booking.objects.all()




    return render(request, 'main/admin.html', {'students': students})

