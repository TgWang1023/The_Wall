from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Message, Comment
import bcrypt, datetime

# Create your views here.
def main(request):
    return render(request, 'the_wall/lar.html')

def register(request):
    request.session['register'] = True
    request.session['login'] = False
    if request.method == 'POST':
        errors = User.objects.reg_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], bday = request.POST['bday'], pass_hs = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        user.save()
        request.session['logged_in'] = True
        request.session['name'] = user.first_name
        request.session['id'] = user.id
        return redirect('/wall')
    else:
        return redirect('/')

def login(request):
    request.session['register'] = False
    request.session['login'] = True
    if request.method == 'POST':
        errors = User.objects.login_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        request.session['logged_in'] = True
        request.session['name'] = User.objects.get(email = request.POST['login_email']).first_name
        request.session['id'] = User.objects.get(email = request.POST['login_email']).id
        return redirect('/wall')
    else:
        return redirect('/')

def wall(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
        return redirect('/')
    else:
        if request.session['logged_in'] == False:
            return redirect('/')

    context = { 
        'name': request.session['name'],
        'messages': Message.objects.all(),
        'users': User.objects.all()
    }

    return render(request, 'the_wall/wall.html', context)

def logout(request):
    if request.method == 'POST':
        request.session.clear()
        return redirect('/')
    else:
        return redirect('/')

def reset(request):
    request.session.clear()
    return redirect('/')

def new_message(request):
    if request.method == 'POST':
        message = Message.objects.create(message = request.POST['content'], user_id = User.objects.get(id = request.session['id']))
        message.save()
        return redirect('/wall')
    else:
        return redirect('/')

def new_comment(request):
    if request.method == 'POST':
        comment = Comment.objects.create(comment = request.POST['lil_content'], user_id = User.objects.get(id = request.session['id']), message_id = Message.objects.get(id = request.POST['msg_id']))
        comment.save()
        return redirect('/wall')
    else:
        return redirect('/')

def delete(request):
    if request.method == 'POST':
        message = Message.objects.get(id = request.POST['msg_id'])
        message.delete()
        return redirect('/wall')
    else:
        return redirect('/')
