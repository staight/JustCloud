from django.shortcuts import render, HttpResponse, redirect
from SqlMaster.models import *
from django.db.models import F, Q
import datetime
import json


def waringDevice(user_obj):
    devices = []
    system = []
    waring_devices = []
    for system_obj in user_obj.system.all():
        for device_obj in system_obj.device.all():
            devices.append(device_obj)
    for device_obj in devices:
        if device_obj.data.filter(waring=1).all():
            system.append(device_obj.system)
            waring_devices.append(device_obj)
    return system, waring_devices


# Create your views here.

# 模板函数
def systemType(request, username, sid):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        if request.session.get('USERNAME') == username:
            # 判断是否为此用户

            # 拿到用户ORM对象
            user_obj = Users.objects.filter(username=username, domain_id=request.session.get('DOMAIN_ID'))[0]
            # 有无异常设备
            waring_system_list, waring_device_list = waringDevice(user_obj)
            user_name = user_obj.name
            first_name = user_name[0]
            # 确定header选中
            plat_admin_chose = 'active'
            # 确定menu选中
            analy_admin = 'active'
            # 主体栏显示的部分
            exhibition_name = '系统分析'

            # 系统对象
            system_obj = System.objects.filter(id=sid).all()
            if system_obj:
                system_obj = system_obj[0]
            else:
                return redirect('/admin/' + request.session.get('USERNAME'))

            # 判断是否有管理权限
            if user_obj in system_obj.admin.all() and system_obj.platform == 'Jinger':
                # 设备queryset
                devices = system_obj.device.all()
                device_count = len(devices)

                # 该系统的异常设备
                system_waring_devices = []
                for device in system_obj.device.all():
                    for data in device.data.all():
                        if data.waring == 1:
                            system_waring_devices.append(device)

                # 利用集合的特性去重
                system_waring_devices = list(set(system_waring_devices))
                system_waring_device_count = len(system_waring_devices)

                return render(request, 'Jinger/jingerAnaly.html', locals())
            else:
                return redirect('/admin/' + request.session.get('USERNAME'))
        else:
            return redirect('/admin/' + request.session.get('USERNAME'))
    else:
        return redirect('/')


def systemMain(request, username, sid):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        if request.session.get('USERNAME') == username:
            # 判断是否为此用户

            # 拿到用户ORM对象
            user_obj = Users.objects.filter(username=username, domain_id=request.session.get('DOMAIN_ID'))[0]
            # 有无异常设备
            waring_system_list, waring_device_list = waringDevice(user_obj)
            user_name = user_obj.name
            first_name = user_name[0]
            # 确定header选中
            plat_admin_chose = 'active'
            # 确定menu选中
            main_admin = 'active'
            # 主体栏显示的部分
            exhibition_name = '系统概况'

            # 系统对象
            system_obj = System.objects.filter(id=sid).all()
            if system_obj:
                system_obj = system_obj[0]
            else:
                return redirect('/admin/' + request.session.get('USERNAME'))

            # 判断是否有管理权限
            if user_obj in system_obj.admin.all() and system_obj.platform == 'Jinger':

                # 设备queryset
                devices = system_obj.device.all()
                device_count = len(devices)

                # 在线设备/不在线设备
                device_active_list = []
                device_inactive_list = []
                # 数据信息
                data_count = 0
                push_count = 0
                pull_count = 0
                new_data_count = 0
                # 今日时间
                now_time = datetime.datetime.now().date()
                now_date = str(now_time)
                # 运行天数
                running_days = (now_time - system_obj.date.date()).days
                # 最近五天
                time_list = [now_date, ]
                tmp_time = now_time
                yes_time = datetime.timedelta(days=-1)
                for i in range(0, 4):
                    time_list.append(str(tmp_time + yes_time))
                    tmp_time = tmp_time + yes_time
                time_list.reverse()

                data_push_list = [0, 0, 0, 0, 0]
                data_pull_list = [0, 0, 0, 0, 0]
                data_waring_list = [0, 0, 0, 0, 0]

                new_devices = []
                # 该系统的异常设备
                system_waring_devices = []
                for device in devices:
                    if device.data.all():
                        device_active_list.append(device)
                    else:
                        device_inactive_list.append(device)
                    if str(device.date).split()[0] == now_date:
                        new_devices.append(device)
                    data_count = data_count + len(device.data.all())
                    for data in device.data.all():
                        if data.waring == 1:
                            system_waring_devices.append(device)
                        if data.model:
                            push_count = push_count + 1
                        else:
                            pull_count = pull_count + 1
                        if str(data.date).split()[0] == now_date:
                            new_data_count = new_data_count + 1
                        for i in range(0, 5):
                            if str(data.date).split()[0] == time_list[i]:
                                if data.model:
                                    data_push_list[i] = data_push_list[i] + 1
                                else:
                                    # 订阅数据中的异常数据
                                    if data.waring == 0 or data.waring == 1:
                                        data_waring_list[i] = data_waring_list[i] + 1
                                    # 正常数据
                                    else:
                                        data_pull_list[i] = data_pull_list[i] + 1

                # 利用集合的特性去重
                system_waring_devices = list(set(system_waring_devices))
                system_waring_device_count = len(system_waring_devices)

                data_waring_count = len(data_waring_list)
                device_active_count = len(device_active_list)
                device_inactive_count = len(device_inactive_list)
                new_devices_count = len(new_devices)
                new_device_active = 0
                new_device_inactive = 0
                for device in new_devices:
                    if device in device_active_list:
                        if not (device in system_waring_devices):
                            new_device_active = new_device_active + 1
                    else:
                        new_device_inactive = new_device_inactive + 1

                return render(request, 'Jinger/jingerMain.html', locals())
            else:
                return redirect('/admin/' + request.session.get('USERNAME'))
        else:
            return redirect('/admin/' + request.session.get('USERNAME'))
    else:
        return redirect('/')


def systemAnaly(request, username, sid):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        if request.session.get('USERNAME') == username:
            # 判断是否为此用户

            # 拿到用户ORM对象
            user_obj = Users.objects.filter(username=username, domain_id=request.session.get('DOMAIN_ID'))[0]
            # 有无异常设备
            waring_system_list, waring_device_list = waringDevice(user_obj)
            user_name = user_obj.name
            first_name = user_name[0]
            # 确定header选中
            plat_admin_chose = 'active'
            # 确定menu选中
            analy_admin = 'active'
            # 主体栏显示的部分
            exhibition_name = '系统分析'
            # 系统对象
            system_obj = System.objects.filter(id=sid).all()
            if system_obj:
                system_obj = system_obj[0]
            else:
                return redirect('/admin/' + request.session.get('USERNAME'))

            # 判断是否有管理权限

            if user_obj in system_obj.admin.all() and system_obj.platform == 'Jinger':

                # 设备queryset
                devices = system_obj.device.all()
                device_count = len(devices)

                # 该系统的异常设备
                system_waring_devices = []
                system_waring_datas = []
                for device in system_obj.device.all():
                    for data in device.data.all():
                        if data.waring == 1:
                            system_waring_devices.append(device)
                        if data.waring == 1 or data.waring == 0:
                            system_waring_datas.append(data)

                # 利用集合的特性去重
                system_waring_devices = list(set(system_waring_devices))
                system_waring_device_count = len(system_waring_devices)
                system_waring_data_count = len(system_waring_datas)

                data_type = tuple(eval(system_obj.type))
                device_map = {}
                waring_device_map = {}
                # 地图数据
                for device in devices:
                    if device.data.filter(model=0).all() and device not in system_waring_devices:
                        data = eval(str(device.data.all().last()))
                        device_map[device.name] = {}
                        for key_data, value_data in data.items():
                            if key_data in data_type:
                                device_map[device.name][key_data] = value_data
                # 异常设备地图数据
                for device in system_waring_devices:
                    data = eval(str(device.data.all().last()))
                    waring_device_map[device.name] = {}
                    for key_data, value_data in data.items():
                        if key_data in data_type:
                            waring_device_map[device.name][key_data] = value_data

                return render(request, 'Jinger/jingerAnaly.html', locals())
            else:
                return redirect('/admin/' + request.session.get('USERNAME'))
        else:
            return redirect('/admin/' + request.session.get('USERNAME'))
    else:
        return redirect('/')


def systemDevice(request, username, sid):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        if request.session.get('USERNAME') == username:
            # 判断是否为此用户

            # 拿到用户ORM对象
            user_obj = Users.objects.filter(username=username, domain_id=request.session.get('DOMAIN_ID'))[0]
            # 有无异常设备
            waring_system_list, waring_device_list = waringDevice(user_obj)
            user_name = user_obj.name
            first_name = user_name[0]
            # 确定header选中
            plat_admin_chose = 'active'
            # 确定menu选中
            device_admin = 'active'
            # 主体栏显示的部分
            exhibition_name = '设备列表'

            # 系统对象
            system_obj = System.objects.filter(id=sid).all()
            if system_obj:
                system_obj = system_obj[0]
            else:
                return redirect('/admin/' + request.session.get('USERNAME'))

            # 判断是否有管理权限
            if user_obj in system_obj.admin.all() and system_obj.platform == 'Jinger':
                # 设备queryset
                devices = system_obj.device.all()
                device_count = len(devices)

                # 在线设备/不在线设备
                device_active_list = []
                device_inactive_list = []

                # 今日时间
                now_time = datetime.datetime.now().date()
                now_date = str(now_time)

                # 最近五天
                time_list = [now_time, ]
                tmp_time = now_time
                yes_time = datetime.timedelta(days=-1)
                for i in range(0, 4):
                    time_list.append(tmp_time + yes_time)
                    tmp_time = tmp_time + yes_time
                time_list.reverse()

                device_new_change_list = [0, 0, 0, 0, 0]
                device_waring_change_list = [0, 0, 0, 0, 0]

                new_devices = []
                # 该系统的异常设备
                system_waring_devices = []
                for device in devices:
                    if device.data.all():
                        device_active_list.append(device)
                    else:
                        device_inactive_list.append(device)
                    if str(device.date).split()[0] == now_date:
                        new_devices.append(device)
                    for data in device.data.all():
                        if data.waring == 1:
                            system_waring_devices.append(device)
                    for i in range(0, 5):
                        if device.date.date() == time_list[i]:
                            device_new_change_list[i] = device_new_change_list[i] + 1
                        if device.data.all():
                            for data in device.data.all():
                                if device.data.filter(Q(waring=1) | Q(waring=0)).all():
                                    if device.data.filter(Q(waring=1) | Q(waring=0))[0].date.date() == time_list[i]:
                                        device_waring_change_list[i] = device_waring_change_list[i] + 1
                                        break

                # 利用集合的特性去重
                system_waring_devices = list(set(system_waring_devices))
                system_waring_device_count = len(system_waring_devices)

                device_active_count = len(device_active_list)
                device_inactive_count = len(device_inactive_list)
                new_devices_count = len(new_devices)

                return render(request, 'Jinger/jingerDevice.html', locals())
            else:
                return redirect('/admin/' + request.session.get('USERNAME'))
        else:
            return redirect('/admin/' + request.session.get('USERNAME'))
    else:
        return redirect('/')


def waringRemove(request, username, sid):
    if request.method == 'POST':
        is_login = request.session.get('IS_LOGIN', False)
        if is_login:
            if request.session.get('USERNAME') == username:
                # 判断是否为此用户
                # 系统对象
                system_obj = System.objects.filter(id=sid).all()
                if system_obj:
                    system_obj = system_obj[0]
                else:
                    return redirect('/admin/' + request.session.get('USERNAME'))
                user_obj = Users.objects.filter(username=username, domain_id=request.session.get('DOMAIN_ID'))[0]

                # 判断是否有管理权限
                if user_obj in system_obj.admin.all() and system_obj.platform == 'Jinger':

                    # 获得post数据
                    device_id = request.POST.get('did')
                    data_id = request.POST.get('dataid')

                    data_obj = Data.objects.filter(id=data_id, device_id=device_id, waring=1).all()
                    if data_obj:
                        data_obj = data_obj[0]
                        data_obj.waring = 0
                        data_obj.save()
                        # 操作记录
                        Operation.objects.create(code=401, user=user_obj)
                        return HttpResponse('666')
                    else:
                        return HttpResponse('444')
                else:
                    return redirect('/admin/' + request.session.get('USERNAME'))
            else:
                return redirect('/admin/' + request.session.get('USERNAME'))
        else:
            return redirect('/')
    else:
        return redirect('/')


def deviceRemove(request, username, sid):
    if request.method == 'POST':
        is_login = request.session.get('IS_LOGIN', False)
        if is_login:
            if request.session.get('USERNAME') == username:
                # 判断是否为此用户
                # 系统对象
                system_obj = System.objects.filter(id=sid).all()
                if system_obj:
                    system_obj = system_obj[0]
                else:
                    return redirect('/admin/' + request.session.get('USERNAME'))
                user_obj = Users.objects.filter(username=username, domain_id=request.session.get('DOMAIN_ID'))[0]

                # 判断是否有管理权限
                if user_obj in system_obj.admin.all() and system_obj.platform == 'Jinger':

                    # 获得post数据
                    device_id = request.POST.get('did')

                    device_obj = Device.objects.filter(id=device_id, system_id=sid)
                    if device_obj:
                        data_obj = device_obj[0]
                        data_obj.delete()
                        # 操作记录
                        Operation.objects.create(code=303, user=user_obj)
                        return HttpResponse('666')
                    else:
                        return HttpResponse('444')
                else:
                    return redirect('/admin/' + request.session.get('USERNAME'))
            else:
                return redirect('/admin/' + request.session.get('USERNAME'))
        else:
            return redirect('/')
    else:
        return redirect('/')


def deviceAdd(request, username, sid):
    if request.method == 'POST':
        is_login = request.session.get('IS_LOGIN', False)
        if is_login:
            if request.session.get('USERNAME') == username:
                # 判断是否为此用户
                # 系统对象
                system_obj = System.objects.filter(id=sid).all()
                if system_obj:
                    system_obj = system_obj[0]
                else:
                    return redirect('/admin/' + request.session.get('USERNAME'))
                user_obj = Users.objects.filter(username=username, domain_id=request.session.get('DOMAIN_ID'))[0]
                # 获得post数据
                name = request.POST.get('name')
                IMEI = request.POST.get('IMEI')
                if Device.objects.filter(system_id=sid, name=name):
                    return HttpResponse('444')
                else:
                    Device.objects.create(name=name, IMEI=IMEI, system=system_obj)
                    # 操作记录
                    Operation.objects.create(code=302, user=user_obj)
                return HttpResponse('666')
            else:
                return redirect('/admin/' + request.session.get('USERNAME'))
        else:
            return redirect('/')
    else:
        return redirect('/')
