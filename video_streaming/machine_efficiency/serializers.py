from rest_framework import serializers
from machine_efficiency.models import *


class MachineModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ["machine_name"]

class ProductionLogModelSerializer(serializers.ModelSerializer):
    machine = MachineModelSerializer(read_only = True)
    class Meta:
        model = ProductionLog
        fields = "__all__"
    