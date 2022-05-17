import json
import pandas as pd
from collections import deque, OrderedDict


class JobController:
    def get_job_data(self):
        # job json file 조회
        with open('job_task/job_data/job.json', 'r') as f:
            job_data = json.load(f)
        return job_data

    def set_job_data(self, job):
    # job json file 수정
        with open('job_task/job_data/job.json', 'w') as f:
            json.dump(job, f, indent='\t')
        return job

    def get_json_from(self, pk, data):
        # 데이터 저장할때 필요한 json 저장 폼
        job_data = {
                "job_id" : pk,
                "job_name" : data['job_name'],
                "task_list" : data['task_list'],
                "property" : {
                        "read": {
                            "task_name": "read", "filename" : data['property']['read']['filename'], "sep" :","
                            },
                        "drop" : {
                            "task_name": "drop", "column_name": data['property']['drop']['column_name']
                            }, 
                        "write" : {
                            "task_name": "write", "filename" : data['property']['write']['filename'], "sep": ","
                            }
                }
            }
        return job_data

    def topology_sort(self, task_list):
        # task 위상정렬
        indegree = OrderedDict()
        result = []
        q = deque()

        # 노드 리스트
        key_list = list(task_list.keys())

        # 간선 리스트
        value_list = []
        for value in list(task_list.values()):
            value_list += value

        for i in key_list:
            indegree[i] = value_list.count(i)

        for i in key_list:
            if indegree[i] == 0:
                q.append(i)

        while q:
            now = q.popleft()
            result.append(now)

            for i in task_list[now]:
                indegree[i] -= 1

                if indegree[i] == 0:
                    q.append(i)
        return result


class CSVController:
    def read(self, filename, sep):
        # csv file 조회
        data = pd.read_csv(filename, sep=sep, encoding='euc-kr')
        return data

    def drop(self, col_name, data):
        # drop column
        col_drop_data = data.drop(col_name, axis=1)
        return col_drop_data

    def write(self, filename, data):
        # csv file 저장
        col_drop_data = data.to_csv(filename, encoding='euc-kr')
        return col_drop_data
