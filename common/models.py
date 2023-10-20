from typing import Any
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


# base model for every model
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# extedning the default user model to add phone and user type fields
class KinBechUser(AbstractUser):
    USER_TYPE = (
                 ('buyer','Buyer'),
                 ('seller','Seller')
                 )
    
    phone = models.BigIntegerField(null=False,blank=False)
    user_type = models.CharField(max_length=10,choices=USER_TYPE,null=False,blank=False)
    
    # swapping the default user model with this model
    class Meta(AbstractUser.Meta):
        # flag to denote that KinBechUser will now Swap the default User class of django
        swappable = "AUTH_USER_MODEL"


        




