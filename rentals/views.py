import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bicicleta, Aluguel
from .forms import BicicletaForm
from django.utils import timezone
from django.db.models import Q

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html')


@login_required
def bike_list(request):
    q = request.GET.get('q', '')
    bikes = Bicicleta.objects.filter(
        Q(nome__icontains=q) | Q(modelo__icontains=q)
    )
    return render(request, 'rentals/bike_list.html', {'bikes': bikes, 'q': q})


@login_required
def bike_detail(request, pk):
    bike = get_object_or_404(Bicicleta, pk=pk)
    return render(request, 'rentals/bike_detail.html', {'bike': bike})


@login_required
def bike_create(request):
    if request.method == 'POST':
        form = BicicletaForm(request.POST, request.FILES)
        if form.is_valid():
            bike = form.save(commit=False)
            bike.dono = request.user
            bike.save()
            messages.success(request, 'Bicicleta cadastrada com sucesso.')
            return redirect('rentals:bike_list')
    else:
        form = BicicletaForm()
    return render(request, 'rentals/bike_form.html', {'form': form, 'create': True})


@login_required
def bike_edit(request, pk):
    try:
        bike = get_object_or_404(Bicicleta, pk=pk, dono=request.user)
    except Http404:
        messages.error(request, 'Você não possui permissão para modificar esta bicicleta.')
        return redirect('rentals:bike_list')
    if request.method == 'POST':
        form = BicicletaForm(request.POST, request.FILES, instance=bike)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bicicleta editada com sucesso.')
            return redirect('rentals:bike_detail', pk=pk)
    else:
        form = BicicletaForm(instance=bike)
    return render(request, 'rentals/bike_form.html', {'form': form, 'create': False})


@login_required
def bike_delete(request, pk):
    try:
        bike = get_object_or_404(Bicicleta, pk=pk, dono=request.user)
    except Http404:
        messages.error(request, 'Você não possui permissão para modificar esta bicicleta.')
        return redirect('rentals:bike_list')
    if request.method == 'POST':
        logger.warning('Usuário %s excluiu a bicicleta %s.', request.user, bike.pk)
        bike.delete()
        messages.success(request, 'Bicicleta excluída com sucesso.')
        return redirect('rentals:bike_list')
    return render(request, 'rentals/bike_confirm_delete.html', {'bike': bike})


@login_required
def rent_bike(request, pk):
    bike = get_object_or_404(Bicicleta, pk=pk)
    if not bike.disponivel:
        messages.error(request, 'Bicicleta indisponível.')
        return redirect('rentals:bike_detail', pk=pk)
    Aluguel.objects.create(bicicleta=bike, usuario=request.user)
    bike.disponivel = False
    bike.save()
    messages.success(request, 'Bicicleta alugada com sucesso.')
    return redirect('rentals:my_rentals')


@login_required
def return_bike(request, pk):
    aluguel = get_object_or_404(Aluguel, pk=pk, usuario=request.user)
    if not aluguel.ativo:
        messages.info(request, 'Aluguel já finalizado.')
        return redirect('rentals:my_rentals')
    aluguel.data_fim = timezone.now()
    aluguel.ativo = False
    aluguel.save()
    bike = aluguel.bicicleta
    bike.disponivel = True
    bike.save()
    messages.success(request, 'Bicicleta devolvida. Obrigado!')
    return redirect('rentals:my_rentals')


@login_required
def my_rentals(request):
    alugueis = Aluguel.objects.filter(usuario=request.user).order_by('-data_inicio')
    return render(request, 'rentals/my_rentals.html', {'alugueis': alugueis})
