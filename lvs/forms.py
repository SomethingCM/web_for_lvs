#!/usr/bin/env python
#-*- coding: utf-8 -*-


from django import forms
from auto_lvs.models import Realserver,VIP

# class IPForm(forms.ModelForm):
    # class Meta:
        # model = IP
        # fields = ('ipaddr','ip_type')
        # widgets = {
            # 'ipaddr' : forms.TextInput(attrs={'class':'form-control'}),
            # 'ip_type' : forms.Select(choices=(('VIP', u'VIP'),('Realserver', u'Realserver')),attrs={'class':'form-control'}),
        # }

    # def __init__(self,*args,**kwargs):
        # super(IPForm,self).__init__(*args,**kwargs)
        # self.fields['ipaddr'].label=u'IP'
        # self.fields['ipaddr'].error_messages={'required':u'请输入ip'}
        # self.fields['ip_type'].label=u'IP类型'


class RealserverForm(forms.ModelForm):
    # ip = forms.ModelChoiceField(queryset=IP.objects.filter(ip_type='Realserver'),widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Realserver
        fields = ('ip','port','weight')
        widgets = {
            'ip' :  forms.TextInput(attrs={'class':'form-control'}),
            'port' : forms.TextInput(attrs={'class':'form-control'}),
            'weight' : forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self,*args,**kwargs):
        super(RealserverForm,self).__init__(*args,**kwargs)
        self.fields['ip'].label=u'realserver ip'
        self.fields['port'].label=u'端口号'
        self.fields['port'].error_messages={'required':u'请输入端口号'}
        self.fields['weight'].label=u'权重'
        self.fields['weight'].error_messages={'required':u'请输入权重'}

class VIPForm(forms.ModelForm):
    class Meta:
        model = VIP
        fields = ('ip','port','lb_algo','lb_kind','realserver')
        widgets = {
            'ip' :  forms.TextInput(attrs={'class':'form-control'}),
            'port' : forms.TextInput(attrs={'class':'form-control'}),
            'lb_algo' : forms.Select(choices=(('NAT', 'NAT'),('DR', 'DR'),('RUN', 'RUN')),attrs={'class':'form-control'}),
            'lb_kind' : forms.Select(choices=(('rr', 'rr'),('wrr', 'wrr'),('sh', 'sh'),('dh', 'dh'),('lblc', 'lblc'),('lc', 'lc'),('lblcr', 'lblcr')),attrs={'class':'form-control'}),
            'realserver' : forms.SelectMultiple(attrs={'class':'form-control','size':'10','multiple':'multiple'}),
        }

    def __init__(self,*args,**kwargs):
        super(VIPForm,self).__init__(*args,**kwargs)
        self.fields['ip'].label=u'VIP'
        self.fields['port'].label=u'端口号'
        self.fields['port'].error_messages={'required':u'请输入端口号'}
        self.fields['lb_algo'].label=u'转发规则'
        self.fields['lb_kind'].label=u'转发算法'
        self.fields['realserver'].label=u'realserver'
        self.fields['realserver'].required=False