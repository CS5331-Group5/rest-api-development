# Extended models for user auth, this is to comply with API specifications.
# Added by Arvee on 2018-02-24
from django.db import models
from django.contrib.auth.models import User

age = models.PositiveIntegerField(default=1)
age.contribute_to_class(User, 'age')
fullname = models.CharField(max_length=100,default='empty')
fullname.contribute_to_class(User, 'fullname')

