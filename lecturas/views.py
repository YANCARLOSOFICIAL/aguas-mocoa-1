from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Barrio, Suscriptor, Micromedidor, SuscriptorMicromedidor, Lectura
from .forms import BarrioForm, SuscriptorForm, MicromedidorForm, SuscriptorMicromedidorForm, LecturaForm
from calendar import month_name
from datetime import datetime  
from django.utils import timezone 
from django.contrib.auth.decorators import login_required
from django.contrib.auth  import logout
#############################################
from .decorators import administrador_required, area_comercial_required, tecnico_operativo_required,administrador_or_area_comercial_required
from django.db.models import Count, Q 
def exit(request):
    logout(request)
    return redirect('login')


def layout(request):
    return render(request, 'layout.html')

@login_required
@administrador_or_area_comercial_required

def indexbarrio(request):  
    barrios=Barrio.objects.all()
    return render(request,'Barrio/indexbarrio.html',{'barrios':barrios} ) 


@login_required
@administrador_or_area_comercial_required
def crearbarrio(request):
    formulario = BarrioForm(request.POST or None,request.FILES or None)
    if formulario.is_valid():      
        formulario.save()    
        return redirect('indexbarrio')
    return render(request,'Barrio/crear.html',{'formulario':formulario})
@login_required
@administrador_or_area_comercial_required
def editarbarrio(request, id):
    barrios = get_object_or_404(Barrio, id=id) 
    formulario = BarrioForm(request.POST or None, instance=barrios)

    if formulario.is_valid():
        formulario.save()
        return redirect('indexbarrio')

    return render(request, 'Barrio/editar.html', {'formulario': formulario, 'barrio': barrios}) 
@login_required
@administrador_or_area_comercial_required
def eliminarbarrio(request, id):
    barrio = get_object_or_404(Barrio, id=id)
    
    if request.method == 'POST':
        barrio.delete()
        return redirect('indexbarrio') 

    return render(request, 'Barrio/eliminar.html', {'barrio': barrio}) 



@login_required
@administrador_or_area_comercial_required
def lista_barrios(request):
    barrios = Barrio.objects.all()
    return render(request, 'Barrio/indexbarrio.html', {'barrio': barrios})  


#####################################################################################





@login_required

def indexmicromedidor(request):  
    micromedidores=Micromedidor.objects.all()
    return render(request,'Micromedidor/indexmicromedidor.html',{'micromedidores':micromedidores} ) 
@login_required
@administrador_or_area_comercial_required
def crearmicromedidor(request):
    if request.method == 'POST':
        formulario = MicromedidorForm(request.POST or None, request.FILES or None)
        if formulario.is_valid():
            # Verificar si el valor del campo 'nuid' ya existe en la base de datos
            nuid = formulario.cleaned_data.get('nuid')
            if Micromedidor.objects.filter(nuid=nuid).exists():
                # Si el 'nuid' ya existe, mostrar un mensaje de error en el formulario
                formulario.add_error('nuid', 'El NUID ya existe. Por favor ingrese un valor diferente.')
            else:
                # Guardar el formulario si es válido y el 'nuid' no existe     
                formulario.save()
                return redirect('indexmicromedidor')
    else:
        formulario = MicromedidorForm()
    return render(request, 'Micromedidor/crear.html', {'formulario': formulario}) 
@login_required

def editarmicromedidor(request, id):
    micromedidor = get_object_or_404(Micromedidor, id=id)
    if request.method == 'POST':
        formulario = MicromedidorForm(request.POST, instance=micromedidor)
        if formulario.is_valid():
            nuid = formulario.cleaned_data.get('nuid')
            # Excluir el micromedidor actual de la verificación de duplicados
            if Micromedidor.objects.filter(nuid=nuid).exclude(id=micromedidor.id).exists():
                formulario.add_error('nuid', 'El NUID ya existe. Por favor ingrese uno diferente.')
            else:
                formulario.save()
                return redirect('indexmicromedidor')
    else:
        formulario = MicromedidorForm(instance=micromedidor)

    return render(request, 'Micromedidor/editar.html', {'formulario': formulario, 'micromedidor': micromedidor})


@login_required
@administrador_or_area_comercial_required
def eliminarmicromedidor(request, id):
    micromedidor = get_object_or_404(Micromedidor, id=id)
    
    if request.method == 'POST':
        micromedidor.delete() 
        return redirect('indexmicromedidor') 

    return render(request, 'Micromedidor/eliminar.html', {'micromedidor': micromedidor})



@login_required

def lista_micromedidores(request):
    micromedidores = Micromedidor.objects.all()
    return render(request, 'Micromedidor/indexmicromedidor.html', {'micromedidores': micromedidores}) 




#######################################################################################################


@login_required

def indexsuscriptor(request):  
    suscriptores=Suscriptor.objects.all()
    return render(request,'Suscriptor/indexsuscriptor.html',{'suscriptores':suscriptores} ) 


@login_required
@administrador_or_area_comercial_required
def crearsuscriptor(request):
    barrios = Barrio.objects.all()  # Define barrios fuera del bloque condicional
    if request.method == 'POST':
        form = SuscriptorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('indexsuscriptor')  # Cambia esto al nombre de tu vista de índice de Suscriptor
    else:
        form = SuscriptorForm() 
    return render(request, 'Suscriptor/crear.html', {'form': form, 'barrios': barrios})
@login_required

def editarsuscriptor(request, id):
    suscriptor = get_object_or_404(Suscriptor, id=id)
    
    if request.method == 'POST':
        formulario = SuscriptorForm(request.POST, instance=suscriptor)
        if formulario.is_valid():
            formulario.save()
            return redirect('indexsuscriptor')
    else:
        formulario = SuscriptorForm(instance=suscriptor)

    # Obtener todos los barrios disponibles
    barrios = Barrio.objects.all()

    return render(request, 'Suscriptor/editar.html', {'formulario': formulario, 'barrios': barrios})

@login_required
@administrador_or_area_comercial_required
def eliminarsuscriptor(request, id):
    suscriptor = get_object_or_404(Suscriptor, id=id) 
    
    if request.method == 'POST':
        suscriptor.delete()
        return redirect('indexsuscriptor')

    return render(request, 'Suscriptor/eliminar.html', {'suscriptor': suscriptor})



@login_required

def lista_suscriptor(request):
    suscriptores = Suscriptor.objects.all()
    return render(request, 'Suscriptor/indexsuscriptor.html', {'suscriptores': suscriptores}) 


#########################################################################################################


@login_required

def indexsuscriptormicromedidor(request): 
    suscriptoresmicromedidores = SuscriptorMicromedidor.objects.all()
    return render(request, 'SuscriptorMicromedidor/indexsuscriptorMicromedidor.html', {'suscriptormicromedidor': suscriptoresmicromedidores})

@login_required
@administrador_or_area_comercial_required
def crearsuscriptormicromedidor(request):
    suscriptores = Suscriptor.objects.all()
    micromedidores = Micromedidor.objects.all()
    
    if request.method == 'POST':
        form = SuscriptorMicromedidorForm(request.POST) 
        if form.is_valid():
            # Procesar el formulario aquí si es válido
            form.save()
            return redirect('indexsuscriptorMicromedidor')# Redirigir a la página de éxito o a donde corresponda
    else:
        form = SuscriptorMicromedidorForm()
    
    return render(request, 'SuscriptorMicromedidor/crear.html', {'form': form, 'suscriptores': suscriptores, 'micromedidores': micromedidores})

@login_required

def editarsuscriptormicromedidor(request, id):
    suscriptor_micromedidor = get_object_or_404(SuscriptorMicromedidor, id=id) 
    suscriptores = Suscriptor.objects.all()
    micromedidores = Micromedidor.objects.all() 
    
    if request.method == 'POST':
        form = SuscriptorMicromedidorForm(request.POST, instance=suscriptor_micromedidor)
        if form.is_valid():
            form.save()
            # Redirigir a la página de éxito o a donde corresponda
            return redirect('indexsuscriptorMicromedidor')
    else:
        form = SuscriptorMicromedidorForm(instance=suscriptor_micromedidor)
    
    return render(request, 'SuscriptorMicromedidor/editar.html', {'form': form, 'suscriptores': suscriptores, 'micromedidores': micromedidores})

@login_required
@administrador_or_area_comercial_required
def eliminarsuscriptormicromedidor(request, id):
    suscriptor_micromedidor = get_object_or_404(SuscriptorMicromedidor, id=id)
    if request.method == 'POST':
        suscriptor_micromedidor.delete()
        return redirect('indexsuscriptorMicromedidor')
    return render(request, 'suscriptorMicromedidor/eliminar.html', {'suscriptor_micromedidor': suscriptor_micromedidor})


#############################################################################################################



@login_required
def indexlectura(request):
    lecturas = Lectura.objects.all()
    return render(request, 'Lectura/indexlectura.html', {'lecturas': lecturas})

@login_required
def crearlectura(request):
    if request.method == 'POST':
        form = LecturaForm(request.POST)
        if form.is_valid():
            lectura_nueva = form.save(commit=False)
            
            # Obtener la lectura anterior si existe
            suscriptor = lectura_nueva.suscriptor_micromedidor
            lectura_anterior = Lectura.objects.filter(
                suscriptor_micromedidor=suscriptor
            ).order_by('-FechaLectura').exclude(id=lectura_nueva.id).first() 

            if lectura_anterior:
                lectura_nueva.lectura_anterior = lectura_anterior.lectura_actual
                lectura_nueva.consumototal = lectura_nueva.lectura_actual - lectura_anterior.lectura_actual
            else:
                # Si no hay lectura anterior, consumototal es igual a la lectura actual
                lectura_nueva.consumototal = lectura_nueva.lectura_actual

            # Guardar la fecha y hora actual como FechaLectura (auto_now_add=True)
            lectura_nueva.mes_actual = datetime.now().strftime('%B')

            lectura_nueva.save()
            return redirect('indexlectura')  
    else:
        # Si es una solicitud GET, inicializa un nuevo formulario
        form = LecturaForm()

    # Obtener suscriptores para el formulario
    suscriptores_micromedidores = SuscriptorMicromedidor.objects.all()

    

    # Renderizar la plantilla con el formulario y otros datos necesarios
    return render(request, 'Lectura/crear.html', {
        'form': form,
        'suscriptores_micromedidores': suscriptores_micromedidores,
        
    })

@login_required
def editarlectura(request, id):
    lectura = get_object_or_404(Lectura, id=id)
    if request.method == 'POST':
        form = LecturaForm(request.POST, instance=lectura)
        if form.is_valid():
            lectura = form.save(commit=False)
            lectura.consumototal = lectura.lectura_actual - lectura.lectura_anterior
            lectura.save()
            return redirect('indexlectura')
    else:
        form = LecturaForm(instance=lectura)
    suscriptores_micromedidores = SuscriptorMicromedidor.objects.all()
    return render(request, 'Lectura/editar.html', {'form': form, 'lectura': lectura, 'suscriptores_micromedidores': suscriptores_micromedidores})

@login_required
def eliminarlectura(request, id):
    lectura = get_object_or_404(Lectura, id=id)
    if request.method == 'POST':
        lectura.delete()
        return redirect('indexlectura')
    return render(request, 'Lectura/eliminar.html', {'lectura': lectura}) 
    
def obtener_lectura_anterior_api(request, suscriptor_id):
    try:
        # Obtener la lectura anterior para el suscriptor especificado
        lectura_anterior = Lectura.objects.filter(
            suscriptor_micromedidor__id=suscriptor_id
        ).order_by('-FechaLectura').exclude(id=request.GET.get('lectura_id', 0)).first()

        if lectura_anterior:
            # Construir el JSON con los datos necesarios
            data = {
                'mes_anterior': lectura_anterior.mes_actual,
                'mes_actual': lectura_anterior.mes_actual,
                # Otros datos necesarios aquí...
            }
            return JsonResponse(data)
        else:
            # Si no se encuentra ninguna lectura anterior
            return JsonResponse({'error': 'No se encontró ninguna lectura anterior para este suscriptor'}, status=404)
    except Exception as e:
        # Manejar cualquier error y devolver una respuesta de error
        return JsonResponse({'error': str(e)}, status=500)   

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                return redirect('indexlectura')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
        
    return render(request, 'registration/login.html', {'form': form})


########################### informe ####################################################



from django.db.models import Count  
from collections import Counter

@login_required
def verinforme(request):
    # Obtener todas las lecturas
    todas_las_lecturas = Lectura.objects.all()
    

    # Contar las lecturas por mes_actual
    meses_con_lecturas = [lectura.mes_actual for lectura in todas_las_lecturas]
    conteo_lecturas_por_mes = Counter(meses_con_lecturas)

    # Obtener el mes actual (suponiendo que ya está almacenado en el campo mes_actual)
    mes_actual = todas_las_lecturas[0].mes_actual if todas_las_lecturas else ""

    # Contar los micromedidores con lectura registrada en el mes actual
    micromedidores_con_lectura = set(
        lectura.suscriptor_micromedidor.id 
        for lectura in todas_las_lecturas 
        if lectura.mes_actual == mes_actual
    )

    # Total de micromedidores
    total_micromedidores = Micromedidor.objects.count()

    # Total de micromedidores con lectura registrada en el mes actual
    total_micromedidores_con_lectura = len(micromedidores_con_lectura)

    # Total de micromedidores sin lectura registrada en el mes actual
    micromedidores_sin_lectura = total_micromedidores - total_micromedidores_con_lectura

    # Contar las lecturas por año
    conteo_lecturas_por_anio = {}
    for lectura in todas_las_lecturas:
        anio = lectura.FechaLectura.year
        if anio in conteo_lecturas_por_anio:
            conteo_lecturas_por_anio[anio] += 1
        else:
            conteo_lecturas_por_anio[anio] = 1

    return render(request, 'informe/informe.html', {
        'total_lecturas_mes_actual': conteo_lecturas_por_mes.get(mes_actual, 0),
        'total_micromedidores': total_micromedidores,
        'micromedidores_con_lectura': total_micromedidores_con_lectura,
        'micromedidores_sin_lectura': micromedidores_sin_lectura,
        #'conteo_lecturas_por_mes': conteo_lecturas_por_mes,
        'conteo_lecturas_por_anio': conteo_lecturas_por_anio,
    })



########################### descargar csv con data de entidad lectura ##################################

import csv
from django.http import HttpResponse 
@login_required
def descargar_csv(request):
    # Crear la respuesta con tipo de contenido 'text/csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lecturas.csv"'

    # Crear el escritor CSV
    writer = csv.writer(response, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Escribir los encabezados del CSV
    writer.writerow([
        'ID', 'Suscriptor Nombre', 'Suscriptor Apellido', 'Micromedidor', 'Lectura Actual', 'Lectura Anterior', 'Consumo Total',
        'Observaciones', 'Tipo de Lectura', 'Estado del Micromedidor', 'Mes Anterior', 'Mes Actual',
        'Fecha de Lectura'
    ])

    # Escribir los datos de las lecturas
    lecturas = Lectura.objects.all()
    for lectura in lecturas:
        suscriptor = lectura.suscriptor_micromedidor.suscriptor
        writer.writerow([
            lectura.id,
            suscriptor.primer_nombre,  # Cambia esto al nombre correcto del campo
            suscriptor.primer_apellido,  # Cambia esto al nombre correcto del campo
            lectura.suscriptor_micromedidor.micromedidor.medidor,
            lectura.lectura_actual,
            lectura.lectura_anterior,
            lectura.consumototal,
            lectura.Observaciones,
            lectura.get_tipo_lectura_display(),  # Usando get_FOO_display para campos de elección
            lectura.get_estado_micromedidor_display(),
            lectura.mes_anterior,
            lectura.mes_actual,
            lectura.FechaLectura
        ])

    return response

