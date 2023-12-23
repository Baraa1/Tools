from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    member   = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='العضو')
    ar_name  = models.CharField(max_length=150, verbose_name='الإسم بالعربي')
    position = models.CharField(max_length=50, verbose_name='المنصب')

    def __str__(self):
        return f'{self.member.username}'

class Loan(models.Model):
    amount     = models.FloatField(verbose_name='المبلغ')
    l_date     = models.DateField(verbose_name='تاريخ الحوالة')
    ref        = models.CharField(max_length=150, verbose_name='الرقم المرجعي')
    installments       = models.IntegerField(verbose_name='عدد الدفعات')
    installment_amount = models.IntegerField(verbose_name='مبلغ الدفعة')
    paid               = models.BooleanField(default=False, verbose_name='تم تسديده')
    remarks            = models.TextField(verbose_name='ملاحظات', blank=True, null=True)

    def __str__(self):
        return f'{self.l_receiver} - {self.amount} - {self.remarks}'

class Investment(models.Model):
    amount     = models.FloatField(verbose_name='المبلغ')
    i_date     = models.DateField(verbose_name='تاريخ الحوالة')
    ref        = models.CharField(max_length=150, verbose_name='الرقم المرجعي')
    installments       = models.IntegerField(verbose_name='عدد الدفعات')
    installment_amount = models.IntegerField(verbose_name='مبلغ الدفعة')
    # status = Finished or on-going
    status             = models.BooleanField(default=False, verbose_name='حالة الاستثمار (مستمر أو منتهي)')
    profits_or_losses  = models.FloatField(verbose_name='الأرباح أو الخسائر')
    remarks            = models.TextField(verbose_name='ملاحظات', blank=True, null=True)
    
    def __str__(self):
        return f'{self.i_receiver} - {self.amount} - {self.remarks}'

class Subscription(models.Model):
    year   = models.CharField(max_length=150, verbose_name='السنة')
    amount = models.FloatField(verbose_name='المبلغ')

    def __str__(self):
        return f'{self.year} - {self.amount}'
    
class Transaction(models.Model):
    sender     = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sent_transactions', verbose_name='المرسل')
    # The "t_" is short for transaction to avoid possible naming conflicts 
    t_receiver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='received_transactions', verbose_name='المستقبل')
    amount     = models.FloatField(verbose_name='المبلغ')
    t_date     = models.DateField(verbose_name='تاريخ الحوالة')
    ref        = models.CharField(max_length=150, verbose_name='الرقم المرجعي')
    bank       = models.CharField(max_length=50, verbose_name='البنك')
    t_type     = models.CharField(max_length=50, verbose_name="نوع الحوالة")
    loan         = models.ForeignKey(Loan, on_delete=models.CASCADE, verbose_name='القرض', blank=True, null=True)
    investment   = models.ForeignKey(Investment, on_delete=models.CASCADE, verbose_name='الاستثمار', blank=True, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, verbose_name='الاشتراك', blank=True, null=True)
    positive     = models.BooleanField(default=True, verbose_name='موجب')
    remarks      = models.TextField(verbose_name='ملاحظات', blank=True, null=True)