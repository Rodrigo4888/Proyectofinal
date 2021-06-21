from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Producto
from django.views.generic import FormView, TemplateView, View, UpdateView
from django.urls import reverse_lazy 
from django.contrib.auth import login
from django.shortcuts import redirect
from django.db.models import F
from random import randint
from django.contrib import messages

# Importamos forms.py
from .forms import *
#Importamos las clases recien creadas
from .models import *

class HomePageView(TemplateView):

    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Producto.objects.all()[:5]

        return context


class ProductListView(ListView):
    model = Producto

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is not None:
            object_list = Producto.objects.filter(nombre__icontains=query)
            return object_list
        else:
            return Producto.objects.all()


class ProductDetailView(DetailView):
    model = Producto


class RegistrationView(FormView):
    template_name = 'registration/register.html'
    form_class = UserForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # This methos is called when valid from data has been POSTed
        # It should return an HttpResponse

        # Create User
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()

        # Create Profile
        documento_identidad = form.cleaned_data['documento_identidad']
        fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
        telefono = form.cleaned_data['telefono']
        genero = form.cleaned_data['genero']

        user_profile = Profile.objects.create( user=user, documento_identidad=documento_identidad, fecha_nacimiento=fecha_nacimiento, telefono=telefono, genero=genero)
        user_profile.save()
        cliente = Cliente.objects.create(user_profile=user_profile)
        cliente.save()
        # Create Cliente if needed
        '''
        is_cliente = form.cleaned_data['is_cliente']
        if is_cliente:
            cliente = Cliente.objects.create(user_profile=user_profile)

            # Handle special attribute
            preferencias = form.cleaned_data['preferencias']
            preferencias_set = Categoria.objects.filter(pk=preferencias.pk)
            cliente.preferencias.set(preferencias_set)

            cliente.save()
        ''' 
        # Create Colaborador if needed
        '''
        is_colaborador = form.cleaned_data['is_colaborador']
        if is_colaborador:
            reputacion = form.cleaned_data['reputacion']
            colaborador = Colaborador.objects.create(user_profile=user_profile, reputacion=reputacion)

            # Handle special attribute
            cobertura_entrega = form.cleaned_data['cobertura_entrega']
            cobertura_entrega_set = Localizacion.objects.filter(pk=cobertura_entrega.pk)
            colaborador.cobertura_entrega.set(cobertura_entrega_set)

            colaborador.save()
        '''
        # Login the user
        messages.info(self.request, 'Registro completado, se envio tu informacion a tu email ' + email)
        login(self.request, user)
        return super().form_valid(form)
           


class AddToCartView(View):
    def get(self, request, product_pk):
        # Obten el cliente
        try:
            user_profile = Profile.objects.get(user=request.user)
        except:
            messages.info(request, 'Tienes que estar logueado para añadir a carrito')
            return redirect('home')

        cliente = Cliente.objects.get(user_profile=user_profile)
        # Obtén el producto que queremos añadir al carrito
        producto = Producto.objects.get(pk=product_pk)
        # Obtén/Crea un/el pedido en proceso (EP) del usuario
        pedido, _  = Pedido.objects.get_or_create(cliente=cliente, estado='EP')
        # Obtén/Crea un/el detalle de pedido
        detalle_pedido, created = DetallePedido.objects.get_or_create(
            producto=producto,
            pedido=pedido,
        )

        # Si el detalle de pedido es creado la cantidad es 1
        # Si no sumamos 1 a la cantidad actual
        if created:
            detalle_pedido.cantidad = 1
        else:
            detalle_pedido.cantidad = F('cantidad') + 1
        # Guardamos los cambios
        detalle_pedido.save()
        # Recarga la página
        return redirect(request.META['HTTP_REFERER'])

class RemoveFromCartView(View):
    def get(self, request, product_pk):
        # Obten el cliente
        try:
            user_profile = Profile.objects.get(user=request.user)
        except:
            messages.info(request, 'Tienes que estar logueado para remover de carrito')
            return redirect('home')
        cliente = Cliente.objects.get(user_profile=user_profile)
        # Obtén el producto que queremos añadir al carrito
        producto = Producto.objects.get(pk=product_pk)
        # Obtén/Crea un/el pedido en proceso (EP) del usuario
        pedido, _  = Pedido.objects.get_or_create(cliente=cliente, estado='EP')
        # Obtén/Crea un/el detalle de pedido
        detalle_pedido = DetallePedido.objects.get(
            producto=producto,
            pedido=pedido,
        )
        # Si la cantidad actual menos 1 es 0 elmina el producto del carrito
        # Si no restamos 1 a la cantidad actual
        if detalle_pedido.cantidad - 1 == 0:
            detalle_pedido.delete()
        else:
            detalle_pedido.cantidad = F('cantidad') - 1
            # Guardamos los cambios
            detalle_pedido.save()
        # Recarga la página
        return redirect(request.META['HTTP_REFERER'])


class RemoveFromCartView(View):
    def get(self, request, product_pk):
        # Obten el cliente
        try:
            user_profile = Profile.objects.get(user=request.user)
        except:
            messages.info(request, 'Tienes que estar logueado para remover de carrito')
            return redirect('home')
        cliente = Cliente.objects.get(user_profile=user_profile)
        # Obtén el producto que queremos añadir al carrito
        producto = Producto.objects.get(pk=product_pk)
        # Obtén/Crea un/el pedido en proceso (EP) del usuario
        pedido, _  = Pedido.objects.get_or_create(cliente=cliente, estado='EP')
        # Obtén/Crea un/el detalle de pedido
        detalle_pedido = DetallePedido.objects.get(
            producto=producto,
            pedido=pedido,
        )
        # Si la cantidad actual menos 1 es 0 elmina el producto del carrito
        # Si no restamos 1 a la cantidad actual
        if detalle_pedido.cantidad - 1 == 0:
            detalle_pedido.delete()
        else:
            detalle_pedido.cantidad = F('cantidad') - 1
            # Guardamos los cambios
            detalle_pedido.save()
        # Recarga la página
        return redirect(request.META['HTTP_REFERER'])


class PedidoDetailView(DetailView):
    model = Pedido

    def get(self, request, *args, **kwargs):
        try:
            user_profile = Profile.objects.get(user=request.user)
        except:
            # redirect here
            messages.info(request, 'Tienes que estar logueado para ver el carrito')
            return redirect('home')
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


    def get_object(self):
        # Obten el cliente
        #user_profile = Profile.objects.get(user=self.request.user)
        user_profile = Profile.objects.get(user=self.request.user)
        cliente = Cliente.objects.get(user_profile=user_profile)
        # Obtén/Crea un/el pedido en proceso (EP) del usuario
        try: 
            pedido = Pedido.objects.get(cliente=cliente, estado='EP')
        except:
            pedido,_ = Pedido.objects.get_or_create(cliente=cliente, estado='EP')
        return pedido

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if type(context['object']) != bool:
            context['detalles'] = context['object'].detallepedido_set.all()
            context['latest_products'] = Producto.objects.all()[:5]
            context['total_detalles'] = len(context['detalles'])
            context['subtotal'] = context['object'].get_subtotal()
        else:
            context['detalles']=[]
        return context

    def get_queryset(self):
        return Producto.objects.all()


class PedidoUpdateView(UpdateView):
    model = Pedido
    fields = ['ubicacion', 'direccion_entrega']
    success_url = reverse_lazy('payment')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.object = form.save(commit=False)
        # Calculo de tarifa
        self.object.tarifa = randint(5, 20)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        localizaciones = Localizacion.objects.all()
        elementos = []
        for localizacion in localizaciones:
            elementos.append({ "id":localizacion.id, "name":localizacion.get_full_name() })
        if type(context['object']) != bool:
            context['localizaciones'] = elementos
        else:
            context['localizaciones']=[]
        return context

class PaymentView(TemplateView): 
    template_name = "main/payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obten el cliente
        user_profile = Profile.objects.get(user=self.request.user)
        cliente = Cliente.objects.get(user_profile=user_profile)
        context['pedido'] = Pedido.objects.get(cliente=cliente, estado='EP')

        return context


class CompletePaymentView(View):
    def get(self, request):
        # Obten el cliente
        try:
            user_profile = Profile.objects.get(user=request.user)
        except:
            messages.info(self.request, 'Tienes que estar logueado para acceder al pago')
            return redirect('home')
        cliente = Cliente.objects.get(user_profile=user_profile)
        # Obtén/Crea un/el pedido en proceso (EP) del usuario
        pedido = Pedido.objects.get(cliente=cliente, estado='EP')
        # Cambia el estado del pedido
        pedido.estado = 'PAG'
        # Asignacion de repartidor
        pedido.repartidor = Colaborador.objects.order_by('?').first()
        # Guardamos los cambios
        pedido.save()
        messages.success(request, 'Gracias por tu compra! Un repartidor ha sido asignado a tu pedido.')
        return redirect('home')

