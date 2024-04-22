from rest_framework.decorators import api_view
from machine_efficiency.serializers import *
from rest_framework.response import Response
from rest_framework.status  import *
from datetime import datetime

def validate_duration_get_sec(machine_sum,mc_data,each_mc_data,field_name):
    if isinstance(each_mc_data[field_name],str):
        if each_mc_data[field_name] == "00:00:00":
                pass
        else:
            duration_parts = each_mc_data[field_name].split(':')
            duration_hours = int(duration_parts[0])
            duration_minutes = int(duration_parts[1])
            duration_seconds = int(duration_parts[2])
            duration_td = timedelta(hours=duration_hours, minutes=duration_minutes, seconds=duration_seconds)
            machine_sum[mc_data][field_name] = int(duration_td.total_seconds())
    else:
        if field_name not in machine_sum[mc_data]:
            machine_sum[mc_data][field_name] = int(each_mc_data[field_name].total_seconds())
        else:
            machine_sum[mc_data][field_name] += int(each_mc_data[field_name].total_seconds())

def sum_qty(machine_sum,mc_data,each_mc_data,field_name):
    if each_mc_data[field_name]:
        if field_name not in machine_sum[mc_data]:
            machine_sum[mc_data][field_name] = int(each_mc_data[field_name])
        else:
            machine_sum[mc_data][field_name] += int(each_mc_data[field_name])


@api_view(["GET"])
def get_machine_efficiency(request):
    data = None
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    machine_name = request.GET.get("machine_name")
    machine_wise_data = {}
    response = {}
    machine_sum = {}
    
    # Apply filters using AND condition
    query_set = ProductionLog.objects.all()
    if machine_name:
        query_set = query_set.filter(machine__machine_name=machine_name)
    if from_date and to_date:
        from_date = datetime.strptime(request.GET.get("from_date"), "%Y-%m-%d")
        to_date = datetime.strptime(request.GET.get("to_date"), "%Y-%m-%d")
        query_set = query_set.filter(start_time__gte=from_date, end_time__lte=to_date)
    elif from_date:
        from_date = datetime.strptime(request.GET.get("from_date"), "%Y-%m-%d")
        query_set = query_set.filter(start_time__gte=from_date)
    elif to_date:
        to_date = datetime.strptime(request.GET.get("to_date"), "%Y-%m-%d")
        query_set = query_set.filter(end_time__lte=to_date)

    # Serialize the queryset
    if query_set:
        serializers_resp = ProductionLogModelSerializer(query_set, many=True)
        data = serializers_resp.data
        for each_data in data:
            each_data["available_time_seconds"] = timedelta(hours=8)
            if each_data.get("machine").get("machine_name") not in machine_wise_data:
                machine_wise_data[each_data.get("machine").get("machine_name")] = [each_data]
            else:
                machine_wise_data[each_data.get("machine").get("machine_name")].append(each_data)
        for mc_data in machine_wise_data:
            machine_sum[mc_data] = {}
            for each_mc_data in machine_wise_data[mc_data]:
                if each_mc_data["available_time_seconds"]:
                    validate_duration_get_sec(machine_sum,mc_data,each_mc_data,"available_time_seconds")
                if each_mc_data["unplanned_downtime"]:
                    validate_duration_get_sec(machine_sum,mc_data,each_mc_data,"unplanned_downtime")
                if each_mc_data["ideal_cycle_time"]:
                    validate_duration_get_sec(machine_sum,mc_data,each_mc_data,"ideal_cycle_time")
                if each_mc_data["actual_output"]:
                    sum_qty(machine_sum,mc_data,each_mc_data,"actual_output")
                if each_mc_data["available_operating_time"]:
                    validate_duration_get_sec(machine_sum,mc_data,each_mc_data,"available_operating_time")
                if each_mc_data["good_product"]:
                    sum_qty(machine_sum,mc_data,each_mc_data,"good_product")
                if each_mc_data["total_product"]:
                    sum_qty(machine_sum,mc_data,each_mc_data,"total_product")
        for machine in machine_sum:
            machine_sum[machine]["availability"] = (machine_sum[machine].get("available_time_seconds",1) - machine_sum[machine].get("unplanned_downtime",0) / machine_sum[machine].get("available_time_seconds",1)) * 100
            machine_sum[machine]["performance"] = (machine_sum[machine].get("ideal_cycle_time",1) * machine_sum[machine].get("actual_output",0) / machine_sum[machine].get("available_operating_time",1)) * 100
            machine_sum[machine]["quality"] = (machine_sum[machine].get("good_product",1) / machine_sum[machine].get("total_product",0)) * 100
            response[machine] = {}
            response[machine]["OEM"] = machine_sum[machine]["availability"] * machine_sum[machine]["performance"] * machine_sum[machine]["quality"]
    return Response({"status": "success", "data": response}, status=HTTP_200_OK)