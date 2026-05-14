from django.http import HttpResponse
from django.template import loader

def records(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

def dashboard(request):
  template = loader.get_template('dashboard.html')
  return HttpResponse(template.render())

def add_task(request):
  template = loader.get_template('add_task.html')
  return HttpResponse(template.render())

def edit_task(request):
  template = loader.get_template('add_task.html')
  return HttpResponse(template.render())

def delete_task(request):
  template = loader.get_template('delete_task.html')
  return HttpResponse(template.render())
