from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
  return render(request, 'index.html')

def sign_up(request):
    return render(request, 'register.html') 

def register(request):
  if request.method == "POST":
    errors = User.objects.registration_val(request.POST)
    if len(errors) > 0:
      for key, val in errors.items():
        messages.error(request, val)
      return redirect("/signup")
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash_pw)
  return HttpResponse("<h1>Success! You can now <a href = '/login'>Log In</a></h1>")

def login(request):
  if request.method == "POST":
    email = request.POST['email']
    password = request.POST['password']
    if not User.objects.authenticate(email, password):
      messages.error(request, 'Email and Password do not match')
      return redirect("/")
    user = User.objects.get(email=email)
    request.session['user_id'] = user.id
    return redirect("/recipes")
  return redirect('/')

def logout(request):
  del request.session['user_id']
  return redirect('/')

def recipes(request):
  if 'user_id' not in request.session:
    return HttpResponse("<h1>You must be <a href = '/login'>logged in</a> to get to your account</h1>")
  user = User.objects.get(id=request.session['user_id'])
  recipes = Recipe.objects.all()
  context = {
    "user": user,
    "recipes": recipes,
  }
  return render(request, 'list.html', context)

def add_recipe(request):
  if request.method == "POST":
    errors = Recipe.objects.basic_validation(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/recipes')
    recipe_name = request.POST['recipe_name']
    ingredients = request.POST['ingredients']
    duration = request.POST['duration']
    desc = request.POST['desc']
    instruction = request.POST['steps']
    user = User.objects.get(id=request.session['user_id'])
    Recipe.objects.create(recipe_name = recipe_name, ingredients = ingredients, cooking_instruction = instruction, desc = desc, duration = duration, user = user)
    return redirect('/recipes')

def recipe_info(request, recipe_id):
    recipe_info = Recipe.objects.get(id=recipe_id)
    context = {
        "recipe": recipe_info,
    }
    return render(request, 'recipe_info.html', context)

def edit_recipe(request, recipe_id):
    if request.method == "GET":
        recipe_to_update = Recipe.objects.get(id=recipe_id)
        context = {
            "recipe": recipe_to_update,
        }
        
    return redirect(f"/recipes/{recipe_to_update.id}")

# def edit_post(request, post_id):
#   post_to_edit = Post.objects.get(id=tweet_id)
#   context = {
#     "post": post_to_edit
#   }
#   return render(request, 'edit-post.html', context)

# def modify_post(request):
#   if request.method == "POST":
#     post_id = request.POST['post_id']
#     new_text = request.POST['post_text']
#     errors = Post.objects.validate_post(new_text)
#     if len(errors) > 0:
#       for key, val in errors.items():
#         messages.error(request, val)
#       return redirect('/post')
#     post_to_edit = Post.objects.get(id=post_id) 
#     post_to_edit.text = new_text
#     post_to_edit.save()
#     return redirect('/wall')

# def add_comment(request):
#   comment_text = request.POST['comment_text']
#   post_id = request.POST['post_id']
#   user = User.objects.get(id=request.session['user_id'])
#   post = Post.objects.get(id=post_id)
#   Comment.objects.create(text=comment_text, user=user, post=post)
#   return redirect('/wall')

# def add_like(request, post_id):
#   # query tweet to add likes to
#   post = Post.objects.get(id=post_id)
#   # query the user
#   user = User.objects.get(id=request.session['user_id'])
#   # add likes
#   post.likes.add(user)
#   return redirect('/wall')