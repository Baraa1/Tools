# Generated by Django 4.2.6 on 2023-12-23 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='المبلغ')),
                ('i_date', models.DateField(verbose_name='تاريخ الحوالة')),
                ('ref', models.CharField(max_length=150, verbose_name='الرقم المرجعي')),
                ('installments', models.IntegerField(verbose_name='عدد الدفعات')),
                ('installment_amount', models.IntegerField(verbose_name='مبلغ الدفعة')),
                ('status', models.BooleanField(default=False, verbose_name='حالة الاستثمار (مستمر أو منتهي)')),
                ('profits_or_losses', models.FloatField(verbose_name='الأرباح أو الخسائر')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='ملاحظات')),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='المبلغ')),
                ('l_date', models.DateField(verbose_name='تاريخ الحوالة')),
                ('ref', models.CharField(max_length=150, verbose_name='الرقم المرجعي')),
                ('installments', models.IntegerField(verbose_name='عدد الدفعات')),
                ('installment_amount', models.IntegerField(verbose_name='مبلغ الدفعة')),
                ('paid', models.BooleanField(default=False, verbose_name='تم تسديده')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='ملاحظات')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ar_name', models.CharField(max_length=150, verbose_name='الإسم بالعربي')),
                ('position', models.CharField(max_length=50, verbose_name='المنصب')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='العضو')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=150, verbose_name='السنة')),
                ('amount', models.FloatField(verbose_name='المبلغ')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='المبلغ')),
                ('t_date', models.DateField(verbose_name='تاريخ الحوالة')),
                ('ref', models.CharField(max_length=150, verbose_name='الرقم المرجعي')),
                ('bank', models.CharField(max_length=50, verbose_name='البنك')),
                ('t_type', models.CharField(max_length=50, verbose_name='نوع الحوالة')),
                ('positive', models.BooleanField(default=True, verbose_name='موجب')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='ملاحظات')),
                ('investment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='familyTrust.investment', verbose_name='الاستثمار')),
                ('loan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='familyTrust.loan', verbose_name='القرض')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_transactions', to='familyTrust.member', verbose_name='المرسل')),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='familyTrust.subscription', verbose_name='الاشتراك')),
                ('t_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_transactions', to='familyTrust.member', verbose_name='المستقبل')),
            ],
        ),
    ]
