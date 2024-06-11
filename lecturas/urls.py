from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index/', views.layout, name='layout'), 
    path('logout/',views.exit,name='exit'),
    path('', views.custom_login, name='login'),
    path('Barrio/indexbarrio',views.indexbarrio,name='indexbarrio'),
    path('Barrio/crearbarrio',views.crearbarrio,name="crearbarrio"),
    path('Barrio/editarbarrio/<int:id>/',views.editarbarrio,name="editarbarrio"),
    path('Barrio/eliminarbarrio/<int:id>/', views.eliminarbarrio, name="eliminarbarrio"),


    path('Micromedidor/indexmicromedidor',views.indexmicromedidor,name='indexmicromedidor'),
    path('Micromedidor/crearmicromedidor',views.crearmicromedidor,name="crearmicromedidor"),
    path('Micromedidor/editarmicromedidor/<int:id>/',views.editarmicromedidor,name="editarmicromedidor"),
    path('Micromedidor/eliminarmicromedidor/<int:id>/',views.eliminarmicromedidor,name="eliminarmicromedidor"),

    
    path('Suscriptor/indexsucriptor',views.indexsuscriptor,name='indexsuscriptor'),
    path('Suscriptor/crearsuscriptor',views.crearsuscriptor,name="crearsuscriptor"),
    path('Suscriptor/editarsuscriptor/<int:id>/',views.editarsuscriptor,name="editarsuscriptor"),
    path('Suscriptor/eliminarsuscriptor/<int:id>/',views.eliminarsuscriptor,name="eliminarsuscriptor"),


    path('SuscriptorMicromedidor/indexsuscriptorMicromedidor',views.indexsuscriptormicromedidor,name='indexsuscriptorMicromedidor') ,
    path('SuscriptorMicromedidor/crearsuscriptormicromedidor',views.crearsuscriptormicromedidor,name="crearsuscriptormicromedidor"),
    path('SuscriptorMicromedidor/editarsuscriptormicromedidor/<int:id>/',views.editarsuscriptormicromedidor,name="editarsuscriptormicromedidor"),
    path('SuscriptorMicromedidor/eliminarsuscriptormicromedidor/<int:id>/',views.eliminarsuscriptormicromedidor,name="eliminarsuscriptormicromedidor"),

    path('Lectura/indexlectura',views.indexlectura,name='indexlectura'),
    path('Lectura/crearlectura',views.crearlectura,name="crearlectura"),
    path('Lectura/editarlectura/<int:id>/',views.editarlectura,name="editarlectura"),
    path('Lectura/eliminarlectura/<int:id>/',views.eliminarlectura,name="eliminarlectura"), 

    path('api/lectura-anterior/<int:suscriptor_id>/', views.obtener_lectura_anterior_api, name='obtener_lectura_anterior_api'),
    
    path('informe/informe', views.verinforme, name='informe'), 
     path('Lectura/descargar/', views.descargar_csv, name='descargar_csv'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
   


