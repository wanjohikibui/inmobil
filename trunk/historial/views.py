# Create your views here.
from inmobil.historial.models import Pago
from inmobil.balance.models import *

def pago_detail(request, depto_id, consorcio_id):
    """muestra el detalle del pago por departamento"""
    consorcio = Consorcio.objects.get(id=consorcio_id)
    deptos = Depto.objects.filter(consorcio=consorcio_id)
    monto = Pago.objects.filter(depto=depto_id)
    fecha_de_pago = Pago.objects.get(
    
    
    return render_to_response('historial/pago_detail.html', {'consorcio': consorcio, 
                            'deptos':deptos, 'monto':monto, 'fecha_de_pago' : fecha})