from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Course
from .forms import CourseForm
import pprint
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
import os
from reportlab.pdfgen import canvas
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from io import BytesIO
from reportlab.lib.colors import PCMYKColor
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart




class CourseList(ListView):
    model = Course
class CourseDetail(DetailView):
    model = Course
class CourseCreation(CreateView):
    model = Course
    success_url = reverse_lazy('courses:list')
    fields = ['Nombre', 'Fecha_inicio', 'Fecha_fin','Imagen']
class CourseUpdate(UpdateView):
    model = Course
    success_url = reverse_lazy('courses:list')
    fields = ['Nombre', 'Fecha_inicio', 'Fecha_fin','Imagen']
class CourseDelete(DeleteView):
    model = Course
    success_url = reverse_lazy('courses:list')

def principal(request):
    playera = Course.objects.order_by('id')
    template = loader.get_template('home.html')
    context = {
        'playera': playera  
    }
    return HttpResponse(template.render(context, request))

def playera(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            playera = form.save()
            playera.save()
            return HttpResponseRedirect('/')
    else:
        form = CourseForm()
    template = loader.get_template('nueva.html')
    context = {
        'form': form
    }
    if request.user.is_authenticated():
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/')



def grafica(request):
    print "Genero el PDF[grafica]"
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Grafica.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    courses = []
    styles = getSampleStyleSheet()
    header = Paragraph("Total de Cursos", styles['Heading2'])
    courses.append(header)
    styles = getSampleStyleSheet()
    d = Drawing(600, 300)
    conteo = Course.objects.count()
    # for i in Course.objects.all():
    # print conteo
    data = [(conteo,)]
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 200
    bc.width = 300
    bc.data = data
    bc.strokeColor = colors.blue
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 10
    bc.valueAxis.valueStep = 1  #paso de distancia entre punto y punto
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 30
    bc.categoryAxis.categoryNames = ['Cursos']
    bc.groupSpacing = 10
    bc.barSpacing = 2
    d.add(bc)
    pprint.pprint(bc.getProperties())
    courses.append(d)
    doc.build(courses)
    response.write(buff.getvalue())
    buff.close()
    return response

def pdf(request):
    print "Genero el PDF"
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Lista de Cursos.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    courses = []
    styles = getSampleStyleSheet()
    header = Paragraph("Lista de Cursos", styles['Heading2'])
    courses.append(header)
    headings = ('Nombre', 'Fecha de Inicio', 'Fecha de fin', 'Imagen')
    allcourses = [(p.Nombre, p.Fecha_inicio, p.Fecha_fin,  p.Imagen) for p in Course.objects.all()]
    print allcourses
    t = Table([headings] + allcourses)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))

    courses.append(t)
    doc.build(courses)
    response.write(buff.getvalue())
    buff.close()
    return response
    