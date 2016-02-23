#!/usr/bin/env python
#-*- coding: utf-8 -*-
from pexpect import * 
from django.db.models import Q
import traceback,re
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required
from auto_auth.views.permission import PermissionVerify
from auto_lvs.models import Realserver,VIP
from auto_lvs.forms import RealserverForm,VIPForm
from django.contrib.auth.models import User
import ConfigParser
import string, os, sys
cf = ConfigParser.ConfigParser()
cf.read("conf/conf.ini")
master_ip=cf.get("keepalived_master", "host")
master_user=cf.get("keepalived_master", "user")
master_passwd=cf.get("keepalived_master", "password")
slave_ip=cf.get("keepalived_master", "host")
slave_user=cf.get("keepalived_master", "user")
slave_passwd=cf.get("keepalived_master", "password")
'''
@login_required
# @PermissionVerify()
def ListIP(request):
    user = request.user
    mList = IP.objects.all()
    #分页功能
    lst = SelfPaginator(request,mList, 20)
    kwvars = {
        'user':user,
        'lPage':lst,
        'request':request,
    }
    return render_to_response('auto_lvs/IP.list.html',kwvars,RequestContext(request))
@login_required
# @PermissionVerify()
def AddIP(request):
    if request.method == "POST":
        form = IPForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listIPurl'))
    else:
        form = IPForm()
    user = request.user
    kwvars = {
        'user':user,
        'form':form,
        'request':request,
    }

    return render_to_response('auto_lvs/IP.add.html',kwvars,RequestContext(request))
def DeleteIP(request,ID):
    IP.objects.filter(id = ID).delete()
    return HttpResponseRedirect(reverse('listIPurl'))
'''

@login_required
@PermissionVerify()
#列出后端实例机
def ListRealserver(request):
    user = request.user
    mList = Realserver.objects.all()

    #分页功能
    lst = SelfPaginator(request,mList, 20)

    kwvars = {
        'user':user,
        'lPage':lst,
        'request':request,
    }

    return render_to_response('auto_lvs/Realserver.list.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
#添加后端实例机
def AddRealserver(request):

    if request.method == "POST":
        form = RealserverForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listRealserverurl'))
    else:
        # ip = Realserver.objects.filter(ip__ip_type='Realserver')
        form = RealserverForm(initial={'port':80,'weight':10})
    user = request.user
    kwvars = {
        'user':user,
        'form':form,
        'request':request,
    }

    return render_to_response('auto_lvs/Realserver.add.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
#编辑后端实例机信息
def EditRealserver(request,ID):
    user = request.user
    editRealserver = Realserver.objects.get(id=ID)

    if request.method == "POST":
        form = RealserverForm(request.POST,instance=editRealserver)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listRealserverurl'))
    else:
        form = RealserverForm(instance=editRealserver)
    kwvars = {
        'user':user,
        'ID':ID,
        'form':form,
        'request':request,
    }

    return render_to_response('auto_lvs/Realserver.edit.html',kwvars,RequestContext(request))
#删除后端实例机
def DeleteRealserver(request,ID):

    Realserver.objects.filter(id = ID).delete()
    return HttpResponseRedirect(reverse('listRealserverurl'))

@login_required
@PermissionVerify()
#列出vip信息
def ListVIP(request):
    user = request.user
    mList = VIP.objects.all()

    #分页功能
    lst = SelfPaginator(request,mList, 20)

    kwvars = {
        'user':user,
        'lPage':lst,
        'request':request,
    }

    return render_to_response('auto_lvs/VIP.list.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
#添加vip
def AddVIP(request):
    user = request.user
    if request.method == "POST":
        form = VIPForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listVIPurl'))
    else:
        form = VIPForm(initial={'port':80})

    kwvars = {
        'user':user,
        'form':form,
        'request':request,
    }

    return render_to_response('auto_lvs/VIP.add.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
#编辑vip信息
def EditVIP(request,ID):
    user = request.user
    editVIP = VIP.objects.get(id=ID)

    if request.method == "POST":
        form = VIPForm(request.POST,instance=editVIP)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listVIPurl'))
    else:
        form = VIPForm(instance=editVIP)

    kwvars = {
        'user':user,
        'ID':ID,
        'form':form,
        'request':request,
    }

    return render_to_response('auto_lvs/VIP.edit.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
#删除vip
def DeleteVIP(request,ID):
    user = request.user
    VIP.objects.filter(id = ID).delete()

    return HttpResponseRedirect(reverse('listVIPurl'))

@login_required
# @PermissionVerify()
#keepalive配置信息
def keepalive(request):
    user = request.user    
    kwvars = {
        'user':user,
    }
    return render_to_response('auto_lvs/keepalive.html',kwvars,RequestContext(request))
@login_required
@PermissionVerify()
#创建配置
def createtemplate(request):
    user = request.user
    msg = []
    err = []
    master = """
! Configuration File for keepalived
global_defs {
   router_id LVS_MASTER            
}
vrrp_instance VI_1 {
    state MASTER                 
    interface eth1
    virtual_router_id 51
    priority 100                   
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
"""
    master_a = """
     }
}

    vrrp_instance LAN_GATEWAY {
    state MASTER                   
    interface eth0
    virtual_router_id 52
    priority 100                   
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.19.200
    }
}
   """
    slave = """
! Configuration File for keepalived
    global_defs {
      router_id LVS_BACKUP            
     }
    vrrp_instance VI_1 {
    state BACKUP                   
    interface eth1
    virtual_router_id 51
    priority 80                   
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
"""
    slave_a = """
   }
}

vrrp_instance LAN_GATEWAY {
    state BACKUP                   
    interface eth0
    virtual_router_id 52
    priority 80                   
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.19.200
    }
}
   """
    vip=''
    vipconf=''
    vips = VIP.objects.all()
    for i in vips:
        vip=vip+'      '+i.ip+'\n'
    for i in vips:
        vipconf+="virtual_server " + (i.ip).encode("utf-8") + ' ' + str(i.port)+' {\n' + '        delay_loop 6\n'+'        lb_algo '+i.lb_algo+'\n'+'        lb_kind '+i.lb_kind+'\n'+'        protocol TCP\n'
        for t in i.realserver.all():
            vipconf = vipconf + '    real_server '+t.ip+' '+ str(t.port)+' {\n'+'           weight '+' '+ str(t.weight)+"""
            TCP_CHECK {
            connect_timeout 3
            nb_get_retry 3
            delay_before_retry 3
            connect_port  """ +str(t.port) + "\n    } \n    }\n "
        vipconf+='}\n'
    masterconf=master+vip+master_a+vipconf
    slaveconf=slave+vip+slave_a+vipconf
    try:
        BASE_DIR = os.path.dirname(__file__)
        M_DIR = os.path.join(BASE_DIR, 'master/keepalived.conf')
        # M_DIR = os.path.join("/srv/salt/keepalive/", 'master/keepalived.conf')
        S_DIR = os.path.join(BASE_DIR, 'slave/keepalived.conf')
        # S_DIR = os.path.join("/srv/salt/keepalive/", 'slave/keepalived.conf')
        try:
            fm=open(M_DIR,'w')
            # fm=open("/srv/salt/keepalive_m/master/keepalived.conf",'r+')
            fm.write(masterconf)
            fm.close()
            msg.append("Master file create successed!")
        except:
            err.append("Master file create failed!")
        try:
            fs=open(S_DIR,'w')
            # fs=open("/srv/salt/keepalive_s/slave/keepalived.conf",'r+')
            fs.write(slaveconf)
            fs.close()
            msg.append("Slave file create successed!")
        except:
            err.append("Slave file create failed!")
    except:
        pass
    
    kwvars = {
        'user':user,
        'msg':msg,
        'err':err,
        'masterconf':masterconf,
        'slaveconf':slaveconf
    }
    return render_to_response('auto_lvs/keepalive.html',kwvars,RequestContext(request))
@login_required
# @PermissionVerify()
#下发配置
def rsynctemplate(request):
    try:
        msg = []
        err = []
        user = request.user
        BASE_DIR = os.path.dirname(__file__)
        M_DIR = os.path.join(BASE_DIR, 'master/keepalived.conf')
        # M_DIR = os.path.join("/srv/salt/keepalive/", 'master/keepalived.conf')
        # S_DIR = os.path.join(BASE_DIR, 'slave/keepalived.conf')
        S_DIR = os.path.join(BASE_DIR, 'slave/keepalived.conf')
        # tg1 = os.system("salt 'lvs_master' cp.get_file M_DIR /etc/keepalived/")
        # tg1 = os.system("scp "+M_DIR+ " root:118.244.209.155:/etc/keepalived/")
		#远程scp下发配置
        tg1 = os.system("scp -r "+M_DIR+ " root@118.244.209.155:/etc/keepalived/")
        print tg1
        if tg1 == 0:
            msg.append("Master send file successed!\n")
            tg2 = os.system("salt 'lvs_master' cmd.run '/etc/init.d/keepalived  reload'")
            # tg2 = os.system("salt 'lvs_master' cmd.run '/etc/init.d/keepalived  restart'")
            print tg2
            if tg2 == 0:
                msg.append("Master reload successed!\n")
            else:
                err.append("MASTER reload failed!\n")
        else:
            err.append("MASTER send file failed!\n")
        # tag1 = os.system("salt 'lvs_slave' cp.get_file S_DIR /etc/keepalived/")
        tag1 = os.system("scp -r " +S_DIR +" root@118.244.209.156:/etc/keepalived/")
        print tag1
        if tag1 == 0:
            msg.append("Slave send file successed!\n")
            tag2 = os.system("salt 'lvs_slave' cmd.run '/etc/init.d/keepalived  reload'")
            # tag2 = os.system("salt 'lvs_slave' cmd.run '/etc/init.d/keepalived  restart'")
            print tag2
            if tg2 == 0:
                msg.append("Slave reload successed!\n")
            else:
                err.append("Slave reload failed!\n")
        else:
            err.append("Slave send file failed!\n")
    except Exception as e:
        print e
    try:
        BASE_DIR = os.path.dirname(__file__)
        M_DIR = os.path.join(BASE_DIR, 'master/keepalived.conf')
        S_DIR = os.path.join(BASE_DIR, 'slave/keepalived.conf')
        try:
            fm=open(M_DIR,'r')
            masterconf=fm.read()
            fm.close()
        except:
            masterconf=''
        try:
            fs=open(S_DIR,'r')
            slaveconf=fs.read()
            fs.close()
        except:
            slaveconf=''
    except:
        pass    
    kwvars = {
        'user':user,
        'msg':msg,
        'err':err,
        'masterconf':masterconf,
        'slaveconf':slaveconf
    }
    return render_to_response('auto_lvs/keepalive.html',kwvars,RequestContext(request))