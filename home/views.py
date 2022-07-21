from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.conf import settings


from courses.models import Course

from .forms import TeacherSignUpForm, SignUpForm
from .tokens import account_activation_token


def home_page_view(req: HttpRequest):
    """
    Homepage view
    """
    all_courses = Course.objects.all()
    context = {'courses': all_courses}
    return render(req, 'home/home.html', context)


def account_register_view(req: HttpRequest, account_type):
    """
    Register page
    """
    if not settings.EMAIL_HOST_USER:
        print('Warning: EMAIL_HOST_USER is empty!!')
        
    context = {}
    if account_type == 'teacher':
        form = TeacherSignUpForm()
        context['role'] = 'giảng viên'
    else:
        form = SignUpForm()
        context['role'] = 'học viên'

    if req.method == 'POST':
        if account_type == 'teacher':
            form = TeacherSignUpForm(req.POST)
        else:
            form = SignUpForm(req.POST)

        if form.is_valid():
            user: User = form.save()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.userprofile.profession = form.cleaned_data.get('profession')
            user.userprofile.department = form.cleaned_data.get('department')
            user.userprofile.birthday = form.cleaned_data.get('birthday')
            user.userprofile.gender = form.cleaned_data.get('gender')
            
            if settings.EMAIL_HOST_USER:
                user.is_active = False
            
            # Send confirmation email
            current_site = get_current_site(req)
            mail_subject = 'Kích hoạt tài khoản Netaholi của bạn'
            to_email = form.cleaned_data.get('email')

            print(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            # If account is teacher => extra information
            if account_type == 'teacher':
                user.userprofile.bio = form.cleaned_data.get('bio')
                user.userprofile.is_teacher = True
                user.is_active = False
                message = render_to_string('home/acc_active_email_teacher.html', {
                    'user': user
                })
                messages.warning(req, 'Tài khoản của bạn đã được tạo, vui lòng đợi xác nhận từ phía hệ thống.')
            else:
                messages.info(req, 'Tài khoản của bạn đã được tạo!')
                message = render_to_string('home/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
            user.save()

            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            if settings.EMAIL_HOST_USER:
                email.send()
                print('Email sent')

            return redirect('login')
        
    context['form'] = form
    return render(req, 'home/register.html', context)


def login_page_view(req: HttpRequest):
    """
    Login page of the website
    """
    if req.method == 'GET':
        return render(req, 'home/login.html')
    elif req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        # Check user is locked
        try:
            user: User = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(req, 'Tên đăng nhập không tồn tại trên hệ thống')
            return redirect('login')
        
        if not user.is_active:
            if user.userprofile.is_teacher:
                messages.error(req, 'Tài khoản của bạn đang chờ QTV xác nhận.')
            else:
                messages.error(req, 'Tài khoản của bạn chưa được kích hoạt. Vui lòng kiểm tra email xác nhận.')
            return redirect('login')

        user = authenticate(username=username, password=password)
        if user is not None:
            print('User authenticated:', username)
            login(req, user)
            return redirect('home')
        else:
            print('Login error')
            messages.error(req, 'Sai mật khẩu')
            return redirect('login')


def logout_page_view(req: HttpRequest):
    logout(req)
    return redirect('login')


def choose_acc_register_view(req: HttpRequest):
    return render(req, 'home/register_choose.html')

@login_required
def change_password_view(req: HttpRequest):
    form = PasswordChangeForm(user=req.user)
    context = {'form': form}

    if req.method == 'POST':
        form = PasswordChangeForm(user=req.user, data=req.POST or None)
        if form.is_valid():
            form.save()
            update_session_auth_hash(req, form.user)
            messages.success(req, 'Mật khẩu của bạn đã được cập nhật thành công!')
            return redirect('home')
        else:
            print(form.errors)
            messages.error(req, 'Đã có lỗi xảy ra, vui lòng kiểm tra lại!!')
    
    return render(req, 'home/change_pwd.html', context)

def activate_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')