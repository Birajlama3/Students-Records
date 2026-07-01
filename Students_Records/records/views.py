from django.http import HttpResponse
from django.template import loader
from .models import Records
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import RecordsSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view,permission_classes
from django.core.paginator import Paginator
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.core.cache import cache

@login_required 
def records(request):
  myrecords = cache.get("records")
  if myrecords is None:
    print("Cache Miss")
    myrecords = list(Records.objects.all().values())
    cache.set("records", myrecords, timeout=60)

  else:
      print("Cache Hit")

  search = request.GET.get('search')
  stack = request.GET.get('stack')

  if search:
    myrecords = myrecords.filter(name__icontains = search)
  if stack:

    myrecords = myrecords.filter(stack__icontains = stack)

  paginator = Paginator(myrecords, 4) # shows 4 records per page
  page_number = request.GET.get('page')
  page_obj =  paginator.get_page(page_number)
      
  template = loader.get_template('index.html')
  context ={
    "myrecords" : myrecords,
    "page_obj" :page_obj,
  }
  return HttpResponse(template.render(context,request))


def dashboard(request):
  template = loader.get_template('dashboard.html')
  return HttpResponse(template.render())


def login_view(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    print(username)
    print(password)
    print(user)
    if user is not None:
      login(request, user) # Django auth login
      return redirect('records')  
    else:
      return render(request, 'login.html', {
      'error': 'Invalid credentials'
      })
  return render(request, 'login.html')



def add_task(request):
  if request.method == "POST":
    name = request.POST['name']
    stack = request.POST['stack']
    title = request.POST['title']
    description = request.POST['description']
    date = request.POST['date']
    hours_worked  = request.POST['hours_worked']

    records = Records(
      name = name,
      stack = stack,
      title = title,
      description = description,
      date = date,
      hours_worked = hours_worked
    )
    records.save()
    cache.delete("records")
    messages.success(request,'Task added Successfully')
  return render(request,'add_task.html')


def edit_task(request,id):
  records = Records.objects.get(id=id)
  if request.method == 'POST':
    records.name  = request.POST.get('name')
    records.stack = request.POST.get('stack')
    records.title = request.POST.get('title')
    records.description = request.POST.get('description')
    records.date = request.POST.get('date') or records.date
    records.hours_worked = request.POST.get('hours_worked')
    records.save()
    cache.delete("records")
    messages.success(request,'Task Edited Successfully')
  return render(request, 'edit_task.html', {
      "records": records
    })


def delete_task(request,id):
  records = Records.objects.get(id=id)
  records.delete()
  cache.delete("records")
  return redirect('records')


@api_view(['GET'])
def api_records(request):
  records = Records.objects.all()
  serializer = RecordsSerializer(records, many = True)
  return Response(serializer.data)


@api_view(['POST'])
def create_records(request):
  serializer = RecordsSerializer(data=request.data)
  if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def records_details(request,id):
  try:
        records = Records.objects.get(id=id)
  except Records.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
      
  if request.method == 'GET':
      serializer = RecordsSerializer(records)
      return Response(serializer.data)
     
  elif request.method == 'PUT':
      serializer = RecordsSerializer(records, data = request.data)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
      return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
  elif request.method == 'DELETE':
      records.delete()
      return Response(status= status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list(request):
    if request.method == 'GET':
        return Response({"message":"Public can view this data"})
    elif request.method == 'POST':
        return Response({"message": f"Data created by{request.Records.username}"})
    

def home_view(request):
   return HttpResponse("This is Middleware homeview.")


def set_session(request):
   request.session['username']= 'Biraj'
   request.session['course']='Django full course'
   return HttpResponse("Session data saved successfully.")

def get_session(request):
  username = request.session.get('username', 'Guest')
  course = request.session.get('course', 'Not enrolled')
  return HttpResponse(f"Welcome: {username}, you are learning {course}")

def delete_session(request):
  #  try:
  #     del request.session['username']
  #     del request.session['course']
  #   except KeyError:
  #     pass
  #  return HttpResponse('Session data deleted successfully.')
   request.session.flush()
   return HttpResponse("All session data deleted successfully.")


def set_cookies(request):
   response = HttpResponse("Cookie set successfully.")
   response.set_cookie('username','Biraj',max_age=60*60*24) # cookie valid for 1 day.
   response.set_cookie('course', 'Django Full course', max_age=60*60*24)
   return response

def get_cookies(request):
   username = request.COOKIES.get('username','Guest')
   course = request.COOKIES.get('course', 'Not enrolled')
   if 'username' in request.COOKIES:
      return HttpResponse(f"Username : {username}, course: {course}")
   else:
      return HttpResponse("No cookies found")
   

def delete_cookies(request):
  response = HttpResponse("Cookies Deleted Successfully")
  response.delete_cookie("username")
  response.delete_cookie("course")
  return response


# def send_test_email(request):
#    subject = 'Welcome to the records'
#    message = 'Thank you for visiting here.'
#    from_email = "lamabiraj482@gmail.com"
#    recipient_list = ['biraj33bit22@kcc.edu.np']

#    send_mail(subject, message, from_email, recipient_list)
#    return HttpResponse("Test email sent successfully.")

def send_test_email(request):
  subject = "Simple HTML test mail"
  message = render_to_string('email/welcome_email.html', {
    'username': 'Biraj',
    'course' :'Django Tutorial',
  })
  email = EmailMessage(
    subject,
    message,
    "lamabiraj482@gmail.com",
    ['biraj33bit22@kcc.edu.np  ']
  )
  email.content_subtype = "html" # Main content is now html/text
  email.send()
  return HttpResponse("Test email sent successfully.")


def users_list(request):
  users = cache.get('users_data') # Try to get data from cache

  if not users:
    print("Cache miss: Fetching data from database")
    users = Records.objects.all()
    cache.set('users_data', users, timeout=60) # Cache data for 60 seconds.
  else:
    print("Cache hit: Fetching data from cache")

  return render(request, 'index.html', {'myrecords':users})

