from django.contrib import admin

# Register your models here.


from profiles_api import models


#Esto nos permite administrar los perfiles de usuario desde la pagina de adminitracion de django en el navegador
admin.site.register(models.UserProfiles)
admin.site.register(models.ProfileFeedItem)