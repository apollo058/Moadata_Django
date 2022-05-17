from json.decoder import JSONDecodeError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .job_utils import CSVController, JobController


# job이 하나도 없는 상태에서 JSONDecodeError 에러발생 예외처리 해줘야함
class JobTaskSave(APIView):
    def post(self, request):
        data = request.data
        job = JobController().get_job_data()
        keys = job.keys()

        # auto increment
        pk = int(list(keys)[-1]) + 1

        job[f"{pk}"] = JobController().get_json_from(pk, data)
        result = JobController().set_job_data(job)
        return Response(result, status=status.HTTP_201_CREATED)


class JobTaskEdit(APIView):
    def delete(self, request, pk):
        job = JobController().get_job_data()
        del job[f'{pk}']
        result = JobController().set_job_data(job)
        return Response(result, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        data = request.data
        job = JobController().get_job_data()

        job[f'{pk}'] = JobController().get_json_from(pk, data)
        result = JobController().set_job_data(job)
        return Response(result, status=status.HTTP_200_OK)

    def get(self, request, pk):
        job = JobController().get_job_data()
        job = job[f'{pk}']

        task_list = JobController().topology_sort(job['task_list'])

        for task in task_list:
            if task == "read":
                data = CSVController().read(job['property']['read']['filename'], job['property']['read']['sep'])
            if task == "drop":
                data = CSVController().drop(job['property']['drop']['column_name'], data)
            if task == "write":
                data = CSVController().write(job['property']['read']['filename'], data)

        return Response(status=status.HTTP_200_OK)
