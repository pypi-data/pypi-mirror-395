import json
import traceback

from django.db.models import Prefetch

from .models import JobConfiguration, JobPartnerMapping, JobTypeEnum
from .tasks import _execute_setup_or_context_function


def check_job_status_and_fetch_config(job_name, trigger_source, job_type):
    filters = {
        'job_name': job_name,
        'type': job_type
    }

    if trigger_source:
        filters['is_realtime_run_enabled'] = True
    else:
        filters['is_scheduled_run_enabled'] = True

    job_config_qs = JobConfiguration.objects.filter(
        **filters
    ).only(
        'id', 'batch_size', 'records_to_fetch_count', 'task_queue_name', 'process_at_partner_level', 'config',
        'run_async'
    )

    if job_type == JobTypeEnum.PARTNER:
        job_config_qs = job_config_qs.prefetch_related(
            Prefetch(
                'partner_configs',
                queryset=JobPartnerMapping.objects.filter(is_enabled=True).only('partner_id', 'config'),
                to_attr='active_partner_configs'
            )
        )

    job_config_data = job_config_qs[:1]

    if job_config_data:
        job_config_obj = job_config_data[0]
        job_config = {
            'job_name': job_name,
            'trigger_source': trigger_source,
            'job_id':  job_config_obj.id,
            'batch_size': job_config_obj.batch_size,
            'records_to_fetch_count': job_config_obj.records_to_fetch_count,
            'run_async': job_config_obj.run_async,
            'task_queue_name': job_config_obj.task_queue_name,
            'process_at_partner_level': job_config_obj.process_at_partner_level,
            'config': job_config_obj.config or {},
            'job_type': job_type
        }

        if job_type == JobTypeEnum.PARTNER:
            if not job_config_obj.active_partner_configs:
                return None
            else:
                job_config['partner_config_map'] = {
                    partner_config_obj.partner_id: partner_config_obj.config or {}
                    for partner_config_obj in job_config_obj.active_partner_configs
                }

        return job_config

    # Even if Job is enabled, there can be no partners mapped to it
    return None


def _process_task(job_metadata: dict, config:dict) -> tuple[int | None, dict | None, str | None]:

    records_count = additional_details = error_info = None
    error_info_map = {}

    if job_metadata['process_at_partner_level']:

        partner_config_map = config.pop('partner_config_map')
        allowed_partner_id_set = partner_config_map.keys()

        # if partner_id is passed, then we need to run only for given partners else all partners from the config
        if partner_id_list := job_metadata['partner_id_list']:
            partner_id_set = set(partner_id_list)
            diff = partner_id_set - allowed_partner_id_set
            if diff:
                # in this case, neither PJRL nor JRMD will be created if it's not a scheduled run
                return None, None, f'Either partner is disabled or Config missing for partner_id(s) : {diff}'
        else:
            partner_id_set = allowed_partner_id_set

        run_async = job_metadata['run_async']
        for partner_id in partner_id_set:
            job_metadata['config'] = {
                **config,
                **partner_config_map[partner_id]
            }
            if run_async:
                try:
                    _execute_setup_or_context_function.apply_async(
                        kwargs={
                            'job_metadata': job_metadata,
                            'partner_id': partner_id
                        },
                        queue=job_metadata['task_queue_name']
                    )
                except:
                    # Redis connection error
                    error_info_map[partner_id] = traceback.format_exc()
            else:
                _execute_setup_or_context_function(job_metadata, partner_id)

    else:
        job_metadata['config'] = config
        records_count, additional_details, error_info = _execute_setup_or_context_function(job_metadata)

    if error_info_map:
        error_info = json.dumps(error_info_map)

    return records_count, additional_details, error_info
