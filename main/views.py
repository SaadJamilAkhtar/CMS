from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import *
from rest_framework_api_key.models import APIKey

from .models import *
from pandas import *


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
        form = ClientForm(instance=client, initial={
            'Group': [grp.id for grp in client.Group.all()]
        })
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


@login_required()
def deleteExtraField(request, id):
    field = ExtraFields.objects.get(id=id)
    data = ConnectedData.objects.filter(field=field)
    for data_ in data:
        data_.delete()
    field.delete()
    return redirect(f"{reverse('fields')}?del=True")


@login_required()
def uploadFile(request):
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            # try:
            xls = ExcelFile(file.file.path)
            df = xls.parse(xls.sheet_names[0])
            records = df.to_dict('list')
            all_models = []
            print(f"{len(df.index)} total loop iterations")
            for i in range(len(df.index)):
                print("Here")
                all_models.append(Client(
                    Display_name=records.get('Display Name')[i] if records.get('Display Name') else None,
                    Prefix=records.get('Prefix')[i] if records.get('Prefix') else None,
                    First=records.get('First')[i] if records.get('First') else None,
                    Middle=records.get('Middle')[i] if records.get('Middle') else None,
                    Last=records.get('Last')[i] if records.get('Last') else None,
                    Suffix=records.get('Suffix')[i] if records.get('Suffix') else None,
                    Nickname=records.get('Nickname')[i] if records.get('Nickname') else None,
                    Job=records.get('Job')[i] if records.get('Job') else None,
                    Title=records.get('Title')[i] if records.get('Title') else None,
                    Company=records.get('Company')[i] if records.get('Company') else None,
                    Department=records.get('Department')[i] if records.get('Department') else None,
                    Business_Phone=records.get('Business Phone')[i] if records.get('Business Phone') else None,
                    Car_Exchange_Phone=records.get('car (Exchange) Phone')[i] if records.get(
                        'car (Exchange) Phone') else None,
                    Cell_Phone=records.get('Cell Phone')[i] if records.get('Cell Phone') else None,
                    Direct_Phone=records.get('direct Phone')[i] if records.get('direct Phone') else None,
                    Direct_Phone2=records.get('Direct Phone')[i] if records.get('Direct Phone') else None,
                    Fax_Phone=records.get('Fax Phone')[i] if records.get('Fax Phone') else None,
                    Home_Phone=records.get('home Phone')[i] if records.get('home Phone') else None,
                    Home_Phone2=records.get('home (2) Phone')[i] if records.get('home (2) Phone') else None,
                    Home_Fax_Phone=records.get('home fax Phone')[i] if records.get('home fax Phone') else None,
                    IPhone_Phone=records.get('iPhone Phone')[i] if records.get('iPhone Phone') else None,
                    Main_Phone=records.get('main Phone')[i] if records.get('main Phone') else None,
                    Mobile_Phone=records.get('mobile Phone')[i] if records.get('mobile Phone') else None,
                    Mobile_Phone2=records.get('mobile (2) Phone')[i] if records.get('mobile (2) Phone') else None,
                    Mobile_Phone3=records.get('mobile (3) Phone')[i] if records.get('mobile (3) Phone') else None,
                    None_Phone=records.get('None Phone')[i] if records.get('None Phone') else None,
                    Office_Phone=records.get('Office Phone')[i] if records.get('Office Phone') else None,
                    Other_Phone=records.get('other Phone')[i] if records.get('other Phone') else None,
                    Other_Phone2=records.get('other (2) Phone')[i] if records.get('other (2) Phone') else None,
                    Other_Phone3=records.get('other (3) Phone')[i] if records.get('other (3) Phone') else None,
                    Other_Fax_Phone=records.get('other fax Phone')[i] if records.get('other fax Phone') else None,
                    Tel_Phone=records.get('Tel Phone')[i] if records.get('Tel Phone') else None,
                    Trading_Phone=records.get('Trading Phone')[i] if records.get('Trading Phone') else None,
                    Work_Phone=records.get('work Phone')[i] if records.get('work Phone') else None,
                    Work_Phone2=records.get('work (2) Phone')[i] if records.get('work (2) Phone') else None,
                    Work_Fax_Phone=records.get('work fax Phone')[i] if records.get('work fax Phone') else None,
                    Direct_Email=records.get('Direct Email')[i] if records.get('Direct Email') else None,
                    Email_Email=records.get('Email Email')[i] if records.get('Email Email') else None,
                    Home_Email=records.get('home Email')[i] if records.get('home Email') else None,
                    None_Email=records.get('None Email')[i] if records.get('None Email') else None,
                    None_Email2=records.get('None (2) Email')[i] if records.get('None (2) Email') else None,
                    Other_Email=records.get('other Email')[i] if records.get('other Email') else None,
                    Other_Email2=records.get('other (2) Email')[i] if records.get('other (2) Email') else None,
                    Personal_Email=records.get('Personal Email')[i] if records.get('Personal Email') else None,
                    Work_Email=records.get('work Email')[i] if records.get('work Email') else None,
                    Work_Email2=records.get('work Email2')[i] if records.get('work Email2') else None,
                    Work_Email3=records.get('Work Email3')[i] if records.get('Work Email3') else None,
                    Home_address=records.get('home Address')[i] if records.get('home Address') else None,
                    Home_Street=records.get('home Street')[i] if records.get('home Street') else None,
                    Home_City=records.get('home City')[i] if records.get('home City') else None,
                    Home_ZIP=records.get('home ZIP')[i] if records.get('home ZIP') else None,
                    Home_State=records.get('home State')[i] if records.get('home State') else None,
                    Home_Country=records.get('home Country')[i] if records.get('home Country') else None,
                    Other_Address=records.get('other Address')[i] if records.get('other Address') else None,
                    Other_Street=records.get('other Street')[i] if records.get('other Street') else None,
                    Other_City=records.get('other City')[i] if records.get('other City') else None,
                    Other_ZIP=records.get('other ZIP')[i] if records.get('other ZIP') else None,
                    Other_State=records.get('other State')[i] if records.get('other State') else None,
                    Work_Address=records.get('work Address')[i] if records.get('work Address') else None,
                    Work_Street=records.get('work Street')[i] if records.get('work Street') else None,
                    Work_City=records.get('work City')[i] if records.get('work City') else None,
                    Work_ZIP=records.get('work ZIP')[i] if records.get('work ZIP') else None,
                    Work_State=records.get('work State')[i] if records.get('work State') else None,
                    Work_Country=records.get('work Country')[i] if records.get('work Country') else None,
                    Work_Address2=records.get('work (2) Address')[i] if records.get('work (2) Address') else None,
                    Work_Street2=records.get('work (2) Street')[i] if records.get('work (2) Street') else None,
                    Work_City2=records.get('work (2) City')[i] if records.get('work (2) City') else None,
                    Work_ZIP2=records.get('work (2) ZIP')[i] if records.get('work (2) ZIP') else None,
                    Work_State2=records.get('work (2) State')[i] if records.get('work (2) State') else None,
                    Work_Country2=records.get('work (2) Country')[i] if records.get('work (2) Country') else None,
                    Birthday=records.get('Birthday')[i] if records.get('Birthday') else None,
                    Note=records.get('Note')[i] if records.get('Note') else None,
                    Creation=records.get('Creation')[i] if records.get('Creation') else None,
                    Modification=records.get('Modification')[i] if records.get('Modification') else None,
                    UID=records.get('UID')[i] if records.get('UID') else None,
                    Contact_Type=records.get('Contact Type')[i] if records.get('Contact Type') else None,
                    In_the_Class=records.get('In the Class?')[i] if records.get('In the Class?') else None,
                    NO=records.get('#')[i] if records.get('#') else None,
                    FINAL_REC=records.get('FINAL REC:')[i] if records.get('FINAL REC:') else None,
                    Candidate_Ranking=records.get('Candidate Ranking')[i] if records.get('Candidate Ranking') else None,
                    Interview_TARS=records.get('Interview TARS')[i] if records.get('Interview TARS') else None,
                    Super_Vote=records.get('Super Vote')[i] if records.get('Super Vote') else None,
                    Yes_Total=records.get('Yes Total')[i] if records.get('Yes Total') else None,
                    Reader_TARS=records.get('Reader TARS')[i] if records.get('Reader TARS') else None,
                    Total_Avg_TARS=records.get('Total Avg TARS')[i] if records.get('Total Avg TARS') else None,
                    Gender=records.get('Gender')[i] if records.get('Gender') else None,
                    Ethnicity=records.get('Ethnicity')[i] if records.get('Ethnicity') else None,
                    Industry=records.get('Industry')[i] if records.get('Industry') else None,
                    CUP_Corp_Partner=records.get('CUP Corp. Partner')[i] if records.get('CUP Corp. Partner') else None,
                    Recommendation_By=records.get('Recommendation By')[i] if records.get('Recommendation By') else None,
                    Introduced_to_CUP_via=records.get('Introduced to CUP via?')[i] if records.get(
                        'Introduced to CUP via?') else None
                ))
            Client.objects.bulk_create(all_models)
        # except:
        #     pass
        return redirect(reverse('dashboard'))

    form = UploadForm()
    data = {
        'title': 'Upload',
        'description': 'Upload Excel File',
        'form': form
    }
    return render(request, 'add.html', data)
