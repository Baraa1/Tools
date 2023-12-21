from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    member   = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='العضو')
    position = models.CharField(max_length=50, verbose_name='المنصب')

    def __str__(self) -> str:
        return super().__str__(self.member.username)
    
class TransactionType(models.Model):
    name     = models.CharField(max_length=100, verbose_name='الإسم')
    positive = models.BooleanField(default=True, verbose_name='موجب')

    def __str__(self) -> str:
        return super().__str__(self.name)
    
class Transaction(models.Model):
    sender     = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sent_transfers', verbose_name='المرسل')
    # The dash to avoid possible naming conflicts 
    t_receiver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='received_transfers', verbose_name='المستقبل')
    amount     = models.FloatField(verbose_name='المبلغ')
    t_date     = models.DateField(verbose_name='تاريخ الحوالة')
    ref        = models.CharField(max_length=150, verbose_name='الرقم المرجعي')
    bank       = models.CharField(max_length=50, verbose_name='البنك')
    t_type     = models.ForeignKey(TransactionType, on_delete=models.CASCADE, verbose_name='نوع الحوالة')
    remarks    = models.TextField(verbose_name='ملاحظات')