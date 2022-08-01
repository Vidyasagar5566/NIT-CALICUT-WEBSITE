from django.shortcuts import render
from . models import UserTable,UserPostTable
from django.contrib import messages
from datetime import date

# Create your views here.
def check_email(a):
    c,d = ['cs','ec','ee','me','ce'],a[-13:-11]
    if len(a) <= 21 or a[-21] != '_' or a[-20] not in 'bm' or a[-11:] != "@nitc.ac.in" or d not in c:
        return 0
    return 1

def fun_for_likes(dests,username):
    for i in dests:
        a = i.likes
        a = a.split('$')
        if username in a:
            i.likes = True
        else:
            i.likes = False
    return dests

def fun_for_all(username):
    dests = UserPostTable.objects.raw('SELECT * FROM travello3_UserPostTable WHERE Admin = %s ORDER BY posted_date DESC', [False])
    return fun_for_likes(dests,username)

def revial_comments(comments):
    comments = comments[:10000]
    comments = comments.split('$')
    for i in range(len(comments)):
        a = comments[i].split('^')
        class b:
            username,comment,date = a[0],a[1],a[2]
            profile_pic = UserTable.objects.get(username = a[0]).profile_pic
        comments[i] = b
    return comments

def count_post(username):
    try:
        a = UserPostTable.objects.raw('SELECT * FROM travello3_UserPostTable WHERE username = %s', [username])
    except:
        return 1
    ans = 0
    for i in a:
        ans = max(ans,i.post_count)
    return ans + 1


def home_page(request):
    return render(request, 'bla bla.html')
def create_account(request):
    return render(request, 'bla bla.html')


def register(request):
    if request.method == 'POST':
        username = request.POST["input1"]
        first_name = request.POST["input2"]
        last_name = request.POST["input3"]
        password1 = request.POST["input4"]
        password2 = request.POST["input5"]
        e_mail = request.POST["input6"]

        if username and first_name and last_name and password1 and password2 and e_mail:
            if password1 != password2:
                messages.info(request, "When will u grown up!!, password1 and password2 aren't matching")
                return render(request, 'register.html')
            elif UserTable.objects.filter(username=username).exists():
                messages.info(request, "UserName was already taken, please register with another user name")
                return render(request, 'register.html')
            elif UserTable.objects.filter(e_mail = e_mail).exists():
                messages.info(request, "e_mail was already taken, please register with another user name")
                return render(request, 'register.html')
            elif password1 == password2:
                if not check_email(e_mail):
                    messages.info(request, "please provide nitc mail id")
                    return render(request, 'register.html')
                user = UserTable.objects.create_user(username=username, password=password1, e_mail=e_mail, first_name=first_name,last_name=last_name)
                user.save()
                user = UserTable.objects.get(e_mail = e_mail)
                main_page,tag = "student","all"
                return render(request, 'bla bla.html', {'posts':fun_for_all(username),'user':user,'mai_page':main_page,'tag':tag})
        else:
            messages.info(request, "Fill All The Details While Registering")
            return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        e_mail = request.POST["input1"]
        password = request.POST["input2"]
        try:
            user = UserTable.objects.get(e_mail = e_mail, password = password)
            main_page,tag = "student","all"
            return render(request, 'bla bla.html', {'posts':fun_for_all(user.username),'user':user,'mai_page':main_page,'tag':tag})
        except:
            messages.info(request, 'invalid credentials, if u dont have an account goto create an account HOWLE:')
            return render(request, 'login,register.html')
    else:
        return render(request, 'login,register.html')

def official_page(request):
    if request.method == 'POST':
        username = request.POST["input1"]
        user = UserTable.objects.get(username=username)
        posts = UserPostTable.objects.raw('''SELECT * FROM travello3_UserPostTable 
                                              WHERE Admin = %s
                                              ORDER BY posted_date DESC''', [True])
        posts = fun_for_likes(posts,username)
        main_page, tag = "official", "all"
        return render(request, 'bla bla.html',{'posts': posts, 'user': user,'main_page':main_page,'tag':tag})

def personal_page(request):
    if request.method == 'POST':
        username = request.POST["input1"]
        user = UserTable.objects.get(username = username)
        posts = UserPostTable.objects.raw('''SELECT * FROM travello3_UserPostTable
                                              WHERE username = %S
                                              ORDER BY posted_date DESC''', [username])
        posts = fun_for_likes(posts, username)
        main_page = "personal"
        return render(request, 'bla bla.html',{'posts': posts, 'user': user,'main_page':main_page})

def trending_official1(request):
    if request.method == 'POST':
        username = request.POST["input1"]
        user = UserTable.objects.get(username=username)
        posts = UserPostTable.objects.raw('''SELECT * FROM travello3_UserPostTable 
                                                      WHERE Admin = %s
                                                      ORDER BY comments_count DESC''', [True])
        posts = fun_for_likes(posts, username)
        main_page, tag = "official", "trending"
        return render(request, 'bla bla.html', {'posts': posts, 'user': user, 'main_page': main_page, 'tag': tag})

def trending1(request):
    if request.method == 'POST':
        username = request.POST["input1"]
        user = UserTable.objects.get(username=username)
        posts = UserPostTable.objects.raw('''SELECT * FROM travello3_UserPostTable 
                                                      WHERE Admin = %s
                                                      ORDER BY comments_count DESC''', [False])
        posts = fun_for_likes(posts, username)
        main_page, tag = "main_page", "trending"
        return render(request, 'bla bla.html', {'posts': posts, 'user': user, 'main_page': main_page, 'tag': tag})

def trending_official2(request):
    if request.method == 'POST':
        username = request.POST["input1"]
        user = UserTable.objects.get(username=username)
        posts = UserPostTable.objects.raw('''SELECT * FROM travello3_UserPostTable 
                                                      WHERE Admin = %s
                                                      ORDER BY likes_count DESC''', [True])
        posts = fun_for_likes(posts, username)
        main_page, tag = "official", "trending"
        return render(request, 'bla bla.html', {'posts': posts, 'user': user, 'main_page': main_page, 'tag': tag})

def trending2(request):
    if request.method == 'POST':
        username = request.POST["input1"]
        user = UserTable.objects.get(username=username)
        posts = UserPostTable.objects.raw('''SELECT * FROM travello3_UserPostTable 
                                                      WHERE Admin = %s
                                                      ORDER BY likes_count DESC''', [False])
        posts = fun_for_likes(posts, username)
        main_page, tag = "main_page", "trending"
        return render(request, 'bla bla.html', {'posts': posts, 'user': user, 'main_page': main_page, 'tag': tag})

def filter(request):
    if request.method == 'POST':
        username = request.POST["input1"]
        tag = request.POST["input2"]
        user = UserTable.objects.get(username=username)
        posts = UserPostTable.objects.raw('''SELECT * FROM travello3_UserPostTable 
                                                      WHERE Admin = %s AND tag = %s
                                                      ORDER BY posted_date DESC''', [False,tag])
        posts = fun_for_likes(posts, username)
        main_page, tag = "main_page", "trending"
        return render(request, 'bla bla.html', {'posts': posts, 'user': user, 'main_page': main_page, 'tag': tag})

def view_comments(request):
    if request.method == 'POST':
        username = request.POST["input1"]
        post_id = request.POST["input2"]
        user = UserTable.objects.get(username = username)
        post = UserPostTable.objects.get(post_id = post_id)
        post.comments = revial_comments(user_post.comments)
        return render(request, 'bla bla.html', {'post':post.comments,'user':user})

def username_to_profile(request):
    if request.method == 'POST':
        username = request.POST["input1"]
        username_m = request.POST["input2"]
        user_m = UserTable.objects.get(username = username_m)
        posts = UserPostTable.objects.raw('''SELECT * FROM travello3_UserPostTable 
                                                              WHERE username = %s
                                                              ORDER BY posted_date DESC''', [username])
        posts = fun_for_likes(posts, username)
        user = UserTable.objects.get(username = username)
        return render(request, 'bla bla.html', {'user_m':user_m,'user':user,'posts':posts})

def user_updates(request):
    if request.method == 'POST':
        e_mail = request.FILES['input1']
        user = UserTable.objects.get(e_mail=e_mail)
        user.profile_pic = request.FILES['input2']
        user.bio = request.FILES['input3']
        user.first_name = request.FILES['input4']
        user.last_name = request.FILES['input5']
        user.save()
        user = UserTable.objects.get(e_mail=e_mail)
        posts = UserPostTable.objects.raw('''SELECT * FROM travello3_UserPostTable
                                                      WHERE username = %S
                                                      ORDER BY posted_date DESC''', [user.username])
        for post in posts:
            post.profile_pic = user.profile_pic
            post.save()
        posts = fun_for_likes(posts, user.username)
        main_page = "personal"
        return render(request, 'bla bla.html', {'posts': posts, 'user': user, 'main_page': main_page})

def user_post(request):
    if request.method == 'POST':
        username = request.POST["input1"]
        table = UserPostTable()
        post_count = count_post(username)
        try:
            table.username = username
            table.post = request.FILES["input2"]
            table.tag = request.POST["input3"]
            table.caption = request.POST["input4"]
            table.post_file = request.POST["input5"]
        except:
            s = 0
        user = UserTable.objects.get(username=username)
        table.post_id = str(post_count) + username
        table.post_count = post_count
        table.profile_pic = user.profile_pic
        table.user_post_count = post_count
        table.Admin = user.Admin
        table.save()
        main_page, tag = "student", "all"
        return render(request, 'bla bla.html',
                      {'posts': fun_for_all(username), 'user': user, 'mai_page': main_page, 'tag': tag})


def post_comment(request):
    if request.method == 'POST':
        username = request.FILES['input1']
        post_id = request.FILES['input2']
        comment = request.FILES['input3']
        post = UserPostTable.objects.get(post_id = post_id)
        today = date.today()
        datetime = today.strftime("%b-%d-%Y")
        post.comments += '$' + username + '^' + comment + '^' + datetime
        post.comments_count += 1
        post.save()

        user = UserTable.objects.get(username = username)
        user_post = UserPostTable.objects.get(post_id = post_id)
        user_post.comments = revial_comments(user_post.comments)
        return render(request, 'bla bla.html', {'comments':user_post.comments,'user':user})

def delete_post(request):
    if request.method == 'POST':
        username = request.FILES['input1']
        post_id = request.FILES['input2']
        user_post = UserPostTable.objects.get(post_id = post_id)
        user_post.delete()
        user = UserTable.objects.get(username=username)
        posts = UserPostTable.objects.raw('''SELECT * FROM travello3_UserPostTable
                                                      WHERE username = %S
                                                      ORDER BY posted_date DESC''', [username])
        posts = fun_for_likes(posts, username)
        main_page = "personal"
        return render(request, 'bla bla.html', {'posts': posts, 'user': user, 'main_page': main_page})

def likes(request):
    if request.method == 'POST':
        username = request.FILES['input1']
        post_id = request.FILES['input2']
        post = UserPostTable.objects.get(post_id = post_id)
        post.likes += username + '$'
        post.likes_count += 1
        post.save()
        return





