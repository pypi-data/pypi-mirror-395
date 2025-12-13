import concurrent.futures
import logging
import os
import random
import tempfile
import threading
import time
import traceback
from enum import Enum
import requests
from kombu import Connection, Queue, Exchange
from kombu.pools import producers
from kombu.messaging import Consumer
from kombu.mixins import ConsumerProducerMixin

from .file_management import FileManagement
from .file_client import get_file_client
from .utils import get_job_type, retry_on_connect_error
from .exception import CancelException

jobExchange = Exchange('microservice', type='topic')
metadataExchange = Exchange('metadata', type='topic')
queue_arguments = {
    'x-queue-type': 'quorum',
    'x-delivery-limit': 6,
    'x-dead-letter-exchange': 'dead-letter',
}


class JobStatus(str, Enum):
    QUEUED = 'Queued',
    RUNNING = 'Running',
    SUCCEEDED = 'Succeeded',
    FAILED = 'Failed',
    WAITING_FOR_DEPENDENCIES = 'WaitingForDependencies',
    CANCELED = 'Canceled',


class JobMetricTag(str, Enum):
    Log = 'Log',
    Progress = 'Progress',
    Exception = 'Exception',
    Verbose = 'Verbose',


class JobDefinition:
    name: str
    concurrency: int
    priority: int

    def __init__(self, name, concurrency=1, priority=2):
        self.name = name
        self.concurrency = concurrency
        self.priority = priority


class BaseClientHandler(ConsumerProducerMixin):
    def __init__(self, address: str, jobs: list[JobDefinition]):
        connection = Connection(address)
        connection.connect()
        self.connection = connection
        self.jobs = jobs
        self.queues = [Queue(job.name, routing_key=f'{job.name}.#', exchange=jobExchange,
                             queue_arguments=queue_arguments, consumer_arguments={"x-priority": job.priority}) for job in jobs]
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.semaphore_dict = {
            job.name: threading.Semaphore(job.concurrency) for job in jobs
        }

    def get_consumers(self, consumer, channel):
        return [
            Consumer(channel=channel.connection.channel(), queues=queue, callbacks=[self.handle_message_thread], prefetch_count=job.concurrency)
            for job, queue in zip(self.jobs, self.queues)
        ]

    @retry_on_connect_error(max_retries=8, delay=1)
    def set_status(self, job_id: str, status: JobStatus):
        with producers[self.connection].acquire(block=True) as producer:
            producer.publish(
                {
                    'job_id': job_id,
                    'status': status,
                },
                exchange=metadataExchange, routing_key="status.update",
                serializer='json',
            )
        return status

    @retry_on_connect_error(max_retries=6, delay=2)
    def send_metric(self, job_id: str, tag: JobMetricTag, payload: dict, routing_key='metric'):
        with producers[self.connection].acquire(block=True) as producer:
            producer.publish(
                {
                    'job_id': job_id,
                    'tag': tag,
                    'payload': payload,
                },
                exchange=metadataExchange, routing_key=routing_key,
                serializer='json',
            )

    def send_progress(self, job_id: str, status: str, message='', percentage=0, error=None):
        return self.send_metric(job_id, JobMetricTag.Progress, {
            "status": status,
            "error": str(error),
            "message": message,
            "percentage": percentage
        })

    def log(self, job_id: str, message: str, level='info'):
        getattr(logging, level)(message)
        self.send_metric(job_id, JobMetricTag.Log, {'message': message, 'level': level}, routing_key='log')

    def debug(self, job_id: str, message: str, **kwargs):
        self.log(job_id, message, 'debug')

    def info(self, job_id: str, message: str, **kwargs):
        self.log(job_id, message, 'info')

    def warning(self, job_id: str, message: str, **kwargs):
        self.log(job_id, message, 'warning')

    def error(self, job_id: str, message: str, **kwargs):
        self.log(job_id, message, 'error')

    def handle_message_thread(self, body, message):
        routing_key = message.delivery_info.get('routing_key')
        job_type = get_job_type(routing_key)
        self.log(body['uuid'], f"Acquiring semaphore for job type {job_type}, current available: {self.semaphore_dict[job_type]._value}, running on {os.getenv('HOSTNAME')}")
        logging.info(f'''
===========================
Acquiring semaphore for job type {job_type}, current available: {self.semaphore_dict[job_type]._value}
===========================
        ''')
        self.semaphore_dict[job_type].acquire()
        logging.info(f'''
===========================
Acquired semaphore for job type {job_type}...
===========================
        ''')
        self.executor.submit(self.handle_message, body, message)

    def handle_message(self, body, message):
        status = None
        job_uuid = body['uuid']
        task_info = body['payload']
        routing_key = message.delivery_info.get('routing_key')
        job_type = get_job_type(routing_key)
        try:
            logging.info(f"""
============================
Client get task with task uuid {task_info['task_uuid']}. routing_key={routing_key}
============================
            """)
            if task_info.get('backend_address', None) is not None or 'BACKEND_ADDRESS' in os.environ:
                backend_address = task_info.get('backend_address', os.environ.get('BACKEND_ADDRESS', None))
                response = requests.get(f'{backend_address}/api/scheduler', params={'uuid': job_uuid}).json()
                if response['status'] == JobStatus.CANCELED or response['status'] == JobStatus.SUCCEEDED:
                    message.ack()
                    logging.info('Client report task as canceled with task uuid %s.' % task_info['task_uuid'])
                    return
                elif "s3_auth" in response:
                    task_info["s3_auth"] = response["s3_auth"]

            status = self.set_status(job_uuid, JobStatus.RUNNING)
            self.send_progress(job_uuid, 'Generating', message='Start to generate.', percentage=0)
            file_management = get_file_client(task_info["s3_auth"], task_info['task_uuid'])

            with tempfile.TemporaryDirectory() as tmpdir:
                ret = self.generate_progress(job_uuid, task_info, tmpdir, file_management)

            if ret != -1:
                self.send_progress(job_uuid, 'Done', message='Process Done', percentage=100)
                logging.info(f"""
============================
Client finish task with task uuid {task_info['task_uuid']}.
============================
                """)
                status = self.set_status(job_uuid, JobStatus.SUCCEEDED)
                message.ack()
            else:
                status = self.set_status(job_uuid, JobStatus.CANCELED)
                message.ack()
                logging.info(f"""
============================
Client report task as canceled with task uuid {task_info['task_uuid']}.
============================
                """)
        except CancelException as e:
            logging.info(f"""
============================
Client report task as canceled with task uuid {task_info['task_uuid']}.
============================
            """)
            self.info(job_uuid, str(e))
            tb = traceback.format_exc()
            logging.error(tb)
            self.send_progress(job_uuid, 'Canceled', error=str(e))
            self.send_metric(job_uuid, JobMetricTag.Exception, {
                'message': str(e),
                'traceback': tb,
            })
            status = self.set_status(job_uuid, JobStatus.CANCELED)
            message.ack()
        except Exception as e:
            logging.info(f'''
===========================
Exception occurred while processing task {task_info['task_uuid']}, this task will be retried.
===========================
            ''')
            self.info(job_uuid, str(e))
            tb = traceback.format_exc()
            logging.error(tb)
            self.send_progress(job_uuid, 'Failed', error=str(e))
            self.send_metric(job_uuid, JobMetricTag.Exception, {
                'message': str(e),
                'traceback': tb,
            })
            status = self.set_status(job_uuid, JobStatus.FAILED)
            if status is JobStatus.CANCELED:
                message.ack()
            elif status is JobStatus.FAILED:
                time.sleep(random.randint(1, 5))
                message.requeue()
        finally:
            self.semaphore_dict[job_type].release()

    def generate_progress(self, uuid, resources, tmpdir, file: FileManagement):
        raise NotImplementedError("generate_progress is not implemented.")

    def loop(self):
        self.run()
