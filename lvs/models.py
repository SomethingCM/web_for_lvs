# encoding: utf-8
from django.db import models

class Realserver(models.Model):
	ip = models.IPAddressField(u'ip地址',blank=True,null=True)
	port = models.SmallIntegerField(u'端口号',null=True, blank=True)
	weight = models.SmallIntegerField(u'权重',null=True, blank=True)
	class Meta:
		unique_together = ("ip","port")
		verbose_name = 'Realserver'
		verbose_name_plural = "Realserver"
	def __unicode__(self):
		return "%s:%s" % (self.ip,self.port)
class VIP(models.Model):
	ip = models.IPAddressField(u'ip地址',blank=True,null=True)
	port = models.SmallIntegerField(u'端口号',null=True, blank=True)
	lb_algo_choice = (('rr', 'rr'),('wrr', 'wrr'),('sh', 'sh'),('dh', 'dh'),('lblc', 'lblc'),('lc', 'lc'),('lblcr', 'lblcr'))
	lb_algo =  models.CharField(max_length=10,choices=lb_algo_choice,default='rr')
	lb_kind_choice = (('NAT', 'NAT'),('DR', 'DR'),('RUN', 'RUN'),)
	lb_kind =  models.CharField(max_length=4,choices=lb_kind_choice,default='NAT')
	realserver = models.ManyToManyField('Realserver', verbose_name=u'Realserver',null=True,blank=True)
	class Meta:
		unique_together = ("ip","port")
		verbose_name = 'VIP'
		verbose_name_plural = "VIP"
	def __unicode__(self):
		return "%s:%s" % (self.ip,self.port)