from json.decoder import JSONDecodeError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .job_utils import CSVController, JobController


class JobTaskSave(APIView):
    def post(self, request):
        # job 생성
        data = request.data

        # job 생성에서 직접 id를 입력하려 한 경우
        if data.get('job_id'):
            return Response({"message" : "job_id는 직접 입력 할 수 없습니다."},
                status=status.HTTP_400_BAD_REQUEST
                )

        # 필수값이 안들어온 경우
        if list(data.keys()) != ['job_name', 'task_list', 'property']:
            return Response({"message" : "필수값을 확인하세요. ['job_name', 'task_list', 'property']"},
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            job = JobController().get_job_data()
            # pk auto increment
            keys = job.keys()
            pk = int(list(keys)[-1]) + 1

            # 필수값이 안들어온 경우
            if list(data.keys()) != ['job_name', 'task_list', 'property']:
                raise KeyError

        except (FileNotFoundError, JSONDecodeError, IndexError):
            # job.json 파일이 존재하지 않거나, job.json 파일이 비어있을 경우
            pk = "1"
            job = {}

        job[f"{pk}"] = JobController().get_json_from(pk, data)
        result = JobController().set_job_data(job)
        return Response(result, status=status.HTTP_201_CREATED)


class JobTaskEdit(APIView):
    def delete(self, request, pk):
        job = JobController().get_job_data()

        if pk not in list(job.keys()):
            return Response({"message" : "존재하지 않는 job_id입니다."}, status=status.HTTP_400_BAD_REQUEST)

        del job[pk]
        result = JobController().set_job_data(job)
        return Response(result, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        data = request.data
        job = JobController().get_job_data()

        if pk not in list(job.keys()):
            return Response({"message" : "존재하지 않는 job_id입니다."}, status=status.HTTP_400_BAD_REQUEST)

        job[pk] = JobController().get_json_from(pk, data)
        result = JobController().set_job_data(job)
        return Response(result, status=status.HTTP_200_OK)

class JobTaskRun(APIView):
    def get(self, request, pk):
        job = JobController().get_job_data()

        if pk not in list(job.keys()):
            return Response({"message" : "존재하지 않는 job_id입니다."}, status=status.HTTP_400_BAD_REQUEST)

        job = job[pk]
        task_list = JobController().topology_sort(job['task_list'])

        for task in task_list:
            if task == "read":
                data = CSVController().read(job['property']['read']['filename'], job['property']['read']['sep'])
            if task == "drop":
                data = CSVController().drop(job['property']['drop']['column_name'], data)
            if task == "write":
                data = CSVController().write(job['property']['read']['filename'], data)

        return Response(status=status.HTTP_200_OK)
