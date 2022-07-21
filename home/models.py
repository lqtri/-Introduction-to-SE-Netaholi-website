from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


MAX_LENGTH_LONG = 100
MAX_LENGTH_MED = 50

User._meta.get_field('email')._unique = True

class UserProfile(models.Model):
    GENDER_CHOICES = (
        (True, 'Nam'),
        (False, 'Nữ')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(verbose_name='Ngày sinh', null=True)
    gender = models.BooleanField(verbose_name='Giới tính', choices=GENDER_CHOICES, null=True)
    is_teacher = models.BooleanField(default=False)
    profession = models.CharField(verbose_name='Nghề nghiệp', max_length=MAX_LENGTH_MED, null=True)
    department = models.CharField(verbose_name='Nơi công tác', max_length=MAX_LENGTH_LONG, null=True)
    bio = models.TextField(verbose_name='Giới thiệu bản thân', null=True)

    def __str__(self):
        return self.user.last_name + ' ' + self.user.first_name

    @staticmethod
    def get_all_waiting_teachers():
        return User.objects.filter(userprofile__is_teacher=True, is_active=False)
    
    def is_teacher_admin(self):
        return self.is_teacher or self.user.is_staff
    
    def get_role_repr(self):
        if self.user.is_staff:
            return 'Quản trị viên'
        elif self.is_teacher:
            return 'Giáo viên'
        else:
            return 'Học viên'


# Database trigger
@receiver(post_save, sender=User)
def create_profile_signal(sender, instance, created, **kwargs):
    # If a NEWLY CREATED User object emitted this signal -> create a profile for it
    if created:
        print('Created a new profile for this user:', instance.username)
        UserProfile.objects.create(user=instance)
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
