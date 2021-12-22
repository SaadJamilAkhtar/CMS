from django.db import models


class Client(models.Model):
    Display_name = models.CharField(max_length=500, blank=True, null=True)
    Prefix = models.CharField(max_length=500, blank=True, null=True)
    First = models.CharField(max_length=500, blank=True, null=True)
    Middle = models.CharField(max_length=500, blank=True, null=True)
    Last = models.CharField(max_length=500, blank=True, null=True)
    Suffix = models.CharField(max_length=500, blank=True, null=True)
    Nickname = models.CharField(max_length=500, blank=True, null=True)
    Job = models.CharField(max_length=500, blank=True, null=True)
    Title = models.CharField(max_length=500, blank=True, null=True)
    Company = models.CharField(max_length=500, blank=True, null=True)
    Department = models.CharField(max_length=500, blank=True, null=True)
    Business_Phone = models.CharField(max_length=500, blank=True, null=True)
    Car_Exchange_Phone = models.CharField(max_length=500, blank=True, null=True)
    Cell_Phone = models.CharField(max_length=500, blank=True, null=True)
    Direct_Phone = models.CharField(max_length=500, blank=True, null=True)
    Direct_Phone2 = models.CharField(max_length=500, blank=True, null=True)
    Fax_Phone = models.CharField(max_length=500, blank=True, null=True)
    Home_Phone = models.CharField(max_length=500, blank=True, null=True)
    Home_Phone2 = models.CharField(max_length=500, blank=True, null=True)
    Home_Fax_Phone = models.CharField(max_length=500, blank=True, null=True)
    IPhone_Phone = models.CharField(max_length=500, blank=True, null=True)
    Main_Phone = models.CharField(max_length=500, blank=True, null=True)
    Mobile_Phone = models.CharField(max_length=500, blank=True, null=True)
    Mobile_Phone2 = models.CharField(max_length=500, blank=True, null=True)
    Mobile_Phone3 = models.CharField(max_length=500, blank=True, null=True)
    None_Phone = models.CharField(max_length=500, blank=True, null=True)
    Office_Phone = models.CharField(max_length=500, blank=True, null=True)
    Other_Phone = models.CharField(max_length=500, blank=True, null=True)
    Other_Phone2 = models.CharField(max_length=500, blank=True, null=True)
    Other_Phone3 = models.CharField(max_length=500, blank=True, null=True)
    Other_Fax_Phone = models.CharField(max_length=500, blank=True, null=True)
    Tel_Phone = models.CharField(max_length=500, blank=True, null=True)
    Trading_Phone = models.CharField(max_length=500, blank=True, null=True)
    Work_Phone = models.CharField(max_length=500, blank=True, null=True)
    Work_Phone2 = models.CharField(max_length=500, blank=True, null=True)
    Work_Fax_Phone = models.CharField(max_length=500, blank=True, null=True)
    Direct_Email = models.EmailField(blank=True, null=True)
    Email_Email = models.EmailField(blank=True, null=True)
    Home_Email = models.EmailField(blank=True, null=True)
    None_Email = models.EmailField(blank=True, null=True)
    None_Email2 = models.EmailField(blank=True, null=True)
    Other_Email = models.EmailField(blank=True, null=True)
    Other_Email2 = models.EmailField(blank=True, null=True)
    Personal_Email = models.EmailField(blank=True, null=True)
    Work_Email = models.EmailField(blank=True, null=True)
    Work_Email2 = models.EmailField(blank=True, null=True)
    Work_Email3 = models.EmailField(blank=True, null=True)
    Home_address = models.CharField(max_length=500, null=True, blank=True)
    Home_Street = models.CharField(max_length=500, null=True, blank=True)
    Home_City = models.CharField(max_length=500, null=True, blank=True)
    Home_ZIP = models.CharField(max_length=500, null=True, blank=True)
    Home_State = models.CharField(max_length=500, null=True, blank=True)
    Home_Country = models.CharField(max_length=500, null=True, blank=True)
    Other_Address = models.CharField(max_length=500, null=True, blank=True)
    Other_Street = models.CharField(max_length=500, null=True, blank=True)
    Other_City = models.CharField(max_length=500, null=True, blank=True)
    Other_ZIP = models.CharField(max_length=500, null=True, blank=True)
    Other_State = models.CharField(max_length=500, null=True, blank=True)
    Work_Address = models.CharField(max_length=500, null=True, blank=True)
    Work_Street = models.CharField(max_length=500, null=True, blank=True)
    Work_City = models.CharField(max_length=500, null=True, blank=True)
    Work_ZIP = models.CharField(max_length=500, null=True, blank=True)
    Work_State = models.CharField(max_length=500, null=True, blank=True)
    Work_Country = models.CharField(max_length=500, null=True, blank=True)
    Work_Address2 = models.CharField(max_length=500, null=True, blank=True)
    Work_Street2 = models.CharField(max_length=500, null=True, blank=True)
    Work_City2 = models.CharField(max_length=500, null=True, blank=True)
    Work_ZIP2 = models.CharField(max_length=500, null=True, blank=True)
    Work_State2 = models.CharField(max_length=500, null=True, blank=True)
    Work_Country2 = models.CharField(max_length=500, null=True, blank=True)
    Birthday = models.DateField(null=True, blank=True)
    Note = models.TextField(null=True, blank=True)
    Group = models.ManyToManyField("Group", null=True, blank=True)
    Creation = models.CharField(max_length=500, null=True, blank=True)
    Modification = models.CharField(max_length=500, null=True, blank=True)
    UID = models.CharField(max_length=500, null=True, blank=True)
    Contact_Type = models.CharField(max_length=500, null=True, blank=True)
    In_the_Class = models.CharField(max_length=500, null=True, blank=True)
    NO = models.CharField(max_length=500, null=True, blank=True)
    FINAL_REC = models.CharField(max_length=500, null=True, blank=True)
    Candidate_Ranking = models.CharField(max_length=500, null=True, blank=True)
    Interview_TARS = models.CharField(max_length=500, null=True, blank=True)
    Super_Vote = models.CharField(max_length=500, null=True, blank=True)
    Yes_Total = models.CharField(max_length=500, null=True, blank=True)
    Reader_TARS = models.CharField(max_length=500, null=True, blank=True)
    Total_Avg_TARS = models.CharField(max_length=500, null=True, blank=True)
    Gender = models.CharField(max_length=500, null=True, blank=True)
    Ethnicity = models.CharField(max_length=500, null=True, blank=True)
    Industry = models.CharField(max_length=500, null=True, blank=True)
    CUP_Corp_Partner = models.CharField(max_length=500, null=True, blank=True)
    Recommendation_By = models.CharField(max_length=500, null=True, blank=True)
    Introduced_to_CUP_via = models.CharField(max_length=500, null=True, blank=True)

    def getGroup(self):
        return ','.join([grp.name for grp in self.Group.all()])

    def __str__(self):
        return self.Display_name if self.Display_name else " No Display Name "


class APIKEY(models.Model):
    key = models.CharField(max_length=500, blank=False, null=False)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name_plural = "My API Keys"


class Group(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class ExtraFields(models.Model):
    field_name = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.field_name

    class Meta:
        verbose_name_plural = 'Extra Fields'


class ConnectedData(models.Model):
    field = models.ManyToManyField(ExtraFields, null=True, blank=True)
    client = models.ManyToManyField(Client)
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        try:
            return str(self.client.all()[0]) + " | " + self.field.all()[0].field_name + " | " + self.value
        except:
            return super().__str__()

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "Connected Data Entries"


class ImportDataFiles(models.Model):
    file = models.FileField(blank=False, null=False, upload_to='assets/uploads/')

    def __str__(self):
        return self.file.path
