import math
import traceback

from celery import shared_task
from django.utils import timezone

from .apps import JOB_STATUS_PK_MAP
from .constants import JOB_NAME_FUNCTION_REGISTRY, JobStatusEnum
from .models import JobRunMetaDataV2


@shared_task
def _execute_setup_or_context_function(job_metadata:dict, partner_id:int=None):

    records_count = additional_details = error_info = None

    task_metadata = {
        'job_name': job_metadata['job_name'],
        'job_id': job_metadata['job_id'],
        'job_run_log_id': job_metadata['job_run_log_id'],
        'config': job_metadata['config'],
        'parameters': job_metadata['parameters'],
        'partner_id': partner_id,
        'records_to_fetch_count': job_metadata['records_to_fetch_count']
    }

    # Scheduled Run
    if not job_metadata['trigger_source']:

        if setup_func := JOB_NAME_FUNCTION_REGISTRY[job_metadata['job_name']].get('setup_func'):

            setup_func_arguments = {**job_metadata['parameters']}

            # Partner level processing enabled
            if partner_id:
                setup_func_arguments['partner_id'] = partner_id

            # f(records_to_fetch_count=1000, config={}, **{})
            valid_data_list, additional_details, error_info = setup_func(
                config=job_metadata['config'],
                records_to_fetch_count = job_metadata['records_to_fetch_count'],
                **setup_func_arguments
            )

            if error_info:
                # Error encountered in setup_func, e.g. DB connection error or timeout
                if partner_id:
                    # Create an entry in JRMD
                    JobRunMetaDataV2.objects.create(
                        created_dtm=timezone.now(),
                        updated_dtm=timezone.now(),
                        job_id=job_metadata['job_id'],
                        job_run_log_id=job_metadata['job_run_log_id'],
                        metadata={'partner_id': partner_id},
                        error_info=error_info,
                        status=JOB_STATUS_PK_MAP[JobStatusEnum.FAILED.value]
                    )
                return None, None, error_info

            if valid_data_list:
                records_count = len(valid_data_list)
                if partner_id:
                    JobRunMetaDataV2.objects.create(
                        created_dtm=timezone.now(),
                        updated_dtm=timezone.now(),
                        job_id=job_metadata['job_id'],
                        job_run_log_id=job_metadata['job_run_log_id'],
                        metadata={
                            'partner_id': partner_id,
                            'eligible_records_count': records_count,
                            'additional_details': additional_details
                        },
                        status=JOB_STATUS_PK_MAP[JobStatusEnum.SUCCESS.value]
                    )

                batch_size = job_metadata['batch_size']
                if batch_size == 1:
                    for data_to_process in valid_data_list:
                        task_metadata['data'] = data_to_process
                        if isinstance(data_to_process, dict):
                            unique_id = data_to_process[job_metadata['config']['unique_key_name']]
                        else:
                             # str | int
                             unique_id = data_to_process

                        if job_metadata['run_async']:
                            try:
                                _execute_business_logic.apply_async(
                                    kwargs={
                                        'task_metadata': task_metadata
                                    },
                                    queue=job_metadata['task_queue_name']
                                )
                            except:
                                # this will happen only when Redis is down, resulting in connection error
                                JobRunMetaDataV2.objects.create(
                                    created_dtm=timezone.now(),
                                    updated_dtm=timezone.now(),
                                    job_id=job_metadata['job_id'],
                                    job_run_log_id=job_metadata['job_run_log_id'],
                                    metadata={
                                        'partner_id': partner_id,
                                        'data': unique_id
                                    },
                                    error_info=traceback.format_exc(),
                                    status=JOB_STATUS_PK_MAP[JobStatusEnum.FAILED.value]
                                )

                        else:
                            _execute_business_logic(task_metadata)

                else:
                    for idx in range(math.ceil(records_count / batch_size)):
                        start_idx = idx * batch_size
                        end_idx = start_idx + batch_size
                        batch_data_list = valid_data_list[start_idx:end_idx]
                        task_metadata['data'] = batch_data_list

                        if isinstance(batch_data_list[0], dict):
                            unique_id_list = [
                                data[job_metadata['config']['unique_key_name']]
                                for data in batch_data_list
                            ]
                        else:
                            unique_id_list = batch_data_list

                        if job_metadata['run_async']:
                            try:
                                _execute_business_logic.apply_async(
                                    kwargs={'task_metadata': task_metadata},
                                    queue=job_metadata['task_queue_name']
                                )
                            except:
                                # this will happen only when Redis is down, resulting in connection error
                                JobRunMetaDataV2.objects.create(
                                    created_dtm=timezone.now(),
                                    updated_dtm=timezone.now(),
                                    job_id=job_metadata['job_id'],
                                    job_run_log_id=job_metadata['job_run_log_id'],
                                    metadata={
                                        'partner_id': partner_id,
                                        'unique_id_list': unique_id_list
                                    },
                                    error_info=traceback.format_exc(),
                                    status=JOB_STATUS_PK_MAP[JobStatusEnum.FAILED.value]
                                )

                        else:
                            _execute_business_logic(task_metadata)

        else:
            # setup_func is not defined for the job e.g. File upload
            _execute_business_logic(task_metadata)

    # API Invocation
    else:
        _execute_business_logic(task_metadata)

    return records_count, additional_details, error_info


@shared_task
def _execute_business_logic(task_metadata:dict):

    # task_metadata format ::
    #   job_name
    #   job_id
    #   job_run_log_id
    #   config
    #   parameters
    #   partner_id
    #   data : int | str | dict

    job_run_meta_data_obj = JobRunMetaDataV2(
        created_dtm=timezone.now(),
        job_id=task_metadata['job_id'],
        job_run_log_id=task_metadata['job_run_log_id'],
        status=JOB_STATUS_PK_MAP[JobStatusEnum.SUCCESS.value]
    )

    metadata = {}
    context_func_arguments = {
        'config': task_metadata['config']
    }

    # Partner level processing or passed as a parameter in case of an API
    partner_id = task_metadata.get('partner_id') or task_metadata['parameters'].get('partner_id')
    if partner_id:
        context_func_arguments['partner_id'] = partner_id
        metadata['partner_id'] = partner_id

    context_func = JOB_NAME_FUNCTION_REGISTRY[task_metadata['job_name']]['context_func']

    data_to_process = task_metadata.get('data')

    # setup_function is defined
    if data_to_process:
        # str | int
        unique_id_or_id_list = data_to_process
        if isinstance(data_to_process, dict):
            unique_id_or_id_list = data_to_process[task_metadata['config']['unique_key_name']]
        elif isinstance(data_to_process, list) and isinstance(data_to_process[0], dict):
            unique_id_or_id_list = [
                data[task_metadata['config']['unique_key_name']]
                for data in data_to_process
            ]
        metadata['unique_id_or_id_list'] = unique_id_or_id_list
        error_info = context_func(data_to_process, **context_func_arguments)
    else:
        # when setup_function is not defined
        metadata['parameters'] = task_metadata['parameters']
        error_info = context_func(**task_metadata['parameters'], **context_func_arguments)

    if error_info:
        job_run_meta_data_obj.status = JOB_STATUS_PK_MAP[JobStatusEnum.FAILED.value]

    job_run_meta_data_obj.metadata = metadata
    job_run_meta_data_obj.error_info = error_info
    job_run_meta_data_obj.updated_dtm = timezone.now()
    job_run_meta_data_obj.save()
