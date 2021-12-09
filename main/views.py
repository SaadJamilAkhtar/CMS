from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import *
from rest_framework_api_key.models import APIKey

from .models import *


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    if request.POST:
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect(reverse('dashboard'))
    return render(request, 'login.html')


@login_required()
def dashboard(request):
    if request.POST:
        filterForm = SearchFilter(request.POST)
        if filterForm.is_valid():
            clients = Client.objects.filter(Group__in=filterForm.cleaned_data['group']).distinct()
            data = {
                'form': filterForm,
                'clients': clients,
                'title_main': "Client Records"
            }
            return render(request, 'database.html', data)

    filterForm = SearchFilter()
    clients = Client.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(clients, 10)
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    data = {
        "clients": clients,
        'form': filterForm,
        'title': 'Clients',
        'del': request.GET.get('del'),
        'success': request.GET.get('success')
    }
    return render(request, 'database.html', data)


@login_required()
def getClient(request, id):
    client = Client.objects.get(id=id)
    extra = ConnectedData.objects.filter(client=client)
    data = {
        'client': client,
        'data': extra
    }
    return render(request, 'details.html', data)


@login_required()
def log_out(request):
    logout(request)
    return redirect('/')


@login_required()
def add(request):
    if request.POST:
        form = ClientForm(request.POST)
        form2 = ExtraFieldForm(request.POST)
        if form.is_valid() and form2.is_valid():
            user = form.save()
            form_data = form2.cleaned_data
            for entry in form_data:
                obj = ConnectedData()
                obj.save()
                obj.field.add(ExtraFields.objects.get(field_name=entry))
                obj.client.add(user)
                obj.value = form_data[entry]
                obj.save()
            return redirect(f"{reverse('dashboard')}?success=True")
    form = ClientForm()
    form2 = ExtraFieldForm()
    data = {
        'form': form,
        'title': 'Add Client',
        'description': "New Client",
        'form2': form2
    }
    return render(request, 'add.html', data)


@login_required()
def edit(request, id):
    client = Client.objects.get(id=id)
    if request.POST:
        form = ClientForm(request.POST, instance=client)
        form2 = ExtraFieldForm(request.POST)
        if form.is_valid() and form2.is_valid():
            user = form.save()
            form_data = form2.cleaned_data
            for entry in form_data:
                obj = ConnectedData.objects.get(client=user, field__field_name=entry)
                obj.value = form_data[entry]
                obj.save()
            return redirect(f"{reverse('dashboard')}?success=True")
    else:
        extra_data = ConnectedData.objects.filter(client=client)
        form = ClientForm(instance=client)
        initial = {}
        for field in extra_data:
            initial[field.field.all()[0].field_name] = field.value
        form2 = ExtraFieldForm(initial=initial)
        data = {
            'form': form,
            'title': 'Edit',
            'description': "Edit",
            'form2': form2
        }
        return render(request, 'add.html', data)


@login_required()
def delete(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return redirect(f"{reverse('dashboard')}?del=True")


@login_required()
def getApiKey(request):
    if request.POST:
        if APIKey.objects.count() == 0:
            api_key, key = APIKey.objects.create_key(name="my-remote-service")
            key_obj = APIKEY(key=key)
            key_obj.save()
            data = {'key': key_obj.key}
        else:
            key = APIKEY.objects.first()
            data = {'key': key.key}
    else:
        if APIKey.objects.count() != 0:
            key = APIKEY.objects.first()
            data = {'key': key.key}
        else:
            data = {}
    return render(request, 'API.html', data)


@login_required()
def deleteApiKey(request):
    if request.POST:
        APIKEY.objects.all().delete()
        APIKey.objects.all().delete()
    return redirect(reverse('apikey'))


@login_required()
def addGroup(request):
    if request.POST:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('groups')}?success=True")
    form = GroupForm()
    data = {
        'form': form,
        'title': 'Add Group',
        'description': "New Group"
    }
    return render(request, 'add.html', data)


@login_required()
def editGroup(request, id):
    group = Group.objects.get(id=id)
    if request.POST:
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('groups')}?success=True")
    else:
        form = GroupForm(instance=group)
        data = {
            'form': form,
            'title': 'Edit',
            'description': "Edit Group"
        }
        return render(request, 'add.html', data)


@login_required()
def groupView(request):
    groups = Group.objects.all()
    data = {
        'groups': groups,
        'del': request.GET.get('del'),
        'success': request.GET.get('success')
    }

    return render(request, 'groupView.html', data)


@login_required()
def deleteGroup(request, id):
    client = Group.objects.get(id=id)
    client.delete()
    return redirect(f"{reverse('groups')}?del=True")


# remove this later
@login_required()
def form_renderer(request):
    form = ExtraFieldForm()
    return render(request, 'test.html', {'form': form})


@login_required()
def addNewField(request):
    if request.POST:
        form = NewFieldForm(request.POST)
        if form.is_valid():
            field = form.save()
            for customer in Client.objects.all():
                temp = ConnectedData()
                temp.save()
                temp.field.add(field)
                temp.client.add(customer)
                temp.save()
            return redirect(f"{reverse('fields')}?success=True")
    form = NewFieldForm()
    data = {
        'form': form,
        'title': 'Add Field',
        'description': "New Field"
    }
    return render(request, 'add.html', data)


@login_required()
def showAllFields(request):
    fields = ExtraFields.objects.all()
    data = {
        'fields': fields,
        'del': request.GET.get('del'),
        'success': request.GET.get('success')
    }
    return render(request, 'fieldView.html', data)


@login_required()
def editExtraField(request, id):
    field = ExtraFields.objects.get(id=id)
    if request.POST:
        form = NewFieldForm(request.POST, instance=field)
        if form.is_valid():
            form.save()
        return redirect(f"{reverse('fields')}?success=True")
    form = NewFieldForm(instance=field)
    data = {
        'form': form,
        'title': 'Edit',
        'description': "Edit Field"
    }
    return render(request, 'add.html', data)


def deleteExtraField(request, id):
    field = ExtraFields.objects.get(id=id)
    data = ConnectedData.objects.filter(field=field)
    for data_ in data:
        data_.delete()
    field.delete()
    return redirect(f"{reverse('fields')}?del=True")
