# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_GET
from .models import Member
#
@require_GET
def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

@require_GET
def details(request, id):
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))
def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render({},request))
@require_GET
def testing(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('template.html')
  context = {
     'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))