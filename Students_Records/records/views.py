from django.http import HttpResponse
from django.template import loader
from .models import Records
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required 
def records(request):
  myrecords = Records.objects.all().values()
  template = loader.get_template('index.html')
  context ={
    "myrecords" : myrecords
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
    messages.success(request,'Task Edited Successfully')
  return render(request, 'edit_task.html', {
      "records": records
    })

def delete_task(request,id):
  records = Records.objects.get(id=id)
  records.delete()
  return redirect('records')
