from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from machine_efficiency.models import ProductionLog, Machine
from datetime import datetime,timedelta


class MachineEfficiencyTestCase(APITestCase):
    def setUp(self):
        # Create some sample data for testing
        self.machine1 = Machine.objects.create(machine_name="Machine1")
        self.machine2 = Machine.objects.create(machine_name="Machine2")
        self.production_log1 = ProductionLog.objects.create(
            machine=self.machine1,
            start_time=datetime.now(),
            end_time=datetime.now(),
            unplanned_downtime=timedelta(minutes=30),
            duration = timedelta(seconds=30),
            ideal_cycle_time=timedelta(seconds=60),
            actual_output=10,
            available_operating_time=timedelta(hours=7),
            good_product=9,
            bad_product=1,
            total_product=10,
        )
        self.production_log2 = ProductionLog.objects.create(
            machine=self.machine2,
            start_time=datetime.now(),
            end_time=datetime.now(),
            unplanned_downtime=timedelta(minutes=15),
            duration = timedelta(seconds=30),
            ideal_cycle_time=timedelta(seconds=90),
            actual_output=8,
            available_operating_time=timedelta(hours=7),
            good_product=7,
            bad_product=1,
            total_product=8,
        )

    def test_get_machine_efficiency(self):
        # Test the view with query parameters
        url = reverse("get_machine_efficiency")
        params = {
            "from_date": "2023-04-20",
            "to_date": "2023-04-22",
            "machine_name": "Machine1",
        }
        response = self.client.get(url, params)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        data = response.json()
        self.assertIn("status", data)
        self.assertEqual(data["status"], "success")
        self.assertIn("data", data)
       

    def test_get_machine_efficiency_no_data(self):
        # Test the view with no data
        url = reverse("get_machine_efficiency")
        params = {
            "from_date": "2023-04-01",
            "to_date": "2023-04-30",
            "machine_name": "Machine1",
        }
        response = self.client.get(url, params)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        data = response.json()