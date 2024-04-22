from django.db import models
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


# Create your models here.

class Machine(models.Model):
    machine_name = models.CharField(max_length=200)
    machine_serial_no = models.CharField(max_length=30)
    creation = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.machine_name

def default_duration():
    now = datetime.now()
    end_of_day = datetime.combine(now.date(), datetime.max.time())
    if now < end_of_day:
        return timedelta(hours=24) - timedelta(seconds=now.second) - timedelta(microseconds=now.microsecond)
    else:
        return timedelta(hours=8)

class ProductionLog(models.Model):
    cycle_no = models.CharField(max_length=200)
    # unique_id = models.CharField(max_length=30,unique=True)
    material_name = models.CharField(max_length=50)
    machine = models.ForeignKey(Machine,on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    available_time = models.CharField(choices = (
                ("shift 1", "shift 1"),
                ("shift 2", "shift 2"),
                ("shift 3", "shift 3"),
                ),max_length = 30)
    ideal_cycle_time = models.DurationField()
    actual_output = models.IntegerField()

    available_operating_time = models.DurationField()
    unplanned_downtime = models.DurationField()
    good_product = models.IntegerField()
    bad_product = models.IntegerField()
    total_product = models.IntegerField()

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude = exclude)
        self.duration = self.getting_duration()
        self.actual_output = self.getting_actual_output()
        if self.actual_output:
            self.available_operating_time = self.getting_ava_operating_time()
            self.unplanned_downtime = self.getting_unplanned_downtime()
            self.total_product = self.getting_total_product()
        else:
            raise ValidationError("Ideal cycle time is missing.")

    def getting_ava_operating_time(self):
        if self.actual_output and self.ideal_cycle_time:
            available_operating_time = int(self.actual_output) * self.ideal_cycle_time
            return available_operating_time
        else:
            self.available_operating_time

    def getting_unplanned_downtime(self):
        if self.available_operating_time:
            if timedelta(seconds=self.available_operating_time.total_seconds()) > timedelta(hours=8):
                raise ValidationError("Available operating time can't be grater than 8hrs.")
            unplanned_downtime = timedelta(hours=8) - timedelta(seconds=self.available_operating_time.total_seconds())
            return unplanned_downtime
        else:
            return self.unplanned_downtime

    def getting_total_product(self):
        if self.good_product and self.bad_product and self.actual_output:
            total_product = self.good_product + self.bad_product
            if total_product > self.actual_output:
                raise ValidationError("Total Good product and Bad product can't be greater than actual output.") 
            return total_product
        else:
            return self.total_product

    def getting_duration(self):
        if self.end_time and self.start_time:
            duration = self.end_time - self.start_time
            return duration
        else:
            return self.duration

    def getting_actual_output(self):
        if self.ideal_cycle_time and not self.actual_output:
            actual_output = (timedelta(hours=8) / timedelta(seconds=self.ideal_cycle_time.total_seconds())) or 0
            return int(actual_output)
        else:
            return self.actual_output