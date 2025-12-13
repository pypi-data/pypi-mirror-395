from django.conf import settings
from django.db import models


class DefaultTimeStamp(models.Model):
    created_dtm = models.DateTimeField(auto_now_add=True)
    updated_dtm = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class JobTypeEnum(models.TextChoices):
    PARTNER = 'P', 'PARTNER'
    SYSTEM = 'SY', 'SYSTEM'


class JobConfiguration(DefaultTimeStamp):
    job_name = models.CharField(max_length=100)
    is_scheduled_run_enabled = models.BooleanField(default=True)
    is_realtime_run_enabled = models.BooleanField(default=False)
    batch_size = models.PositiveSmallIntegerField()
    records_to_fetch_count = models.PositiveIntegerField()
    # this is to handle cases when we run jobs locally and want to execute batches sequentially or w/o celery
    run_async = models.BooleanField(default=False)
    task_queue_name = models.CharField(max_length=30, default=settings.CELERY_TASK_DEFAULT_QUEUE)
    process_at_partner_level = models.BooleanField(default=False)
    config = models.JSONField(null=True)
    type = models.CharField(max_length=2, choices=JobTypeEnum.choices, default=JobTypeEnum.PARTNER)

    class Meta:
        db_table = 'job_configuration'
        verbose_name = 'Job Configuration'
        verbose_name_plural = 'Job Configurations'


class JobPartnerMapping(DefaultTimeStamp):
    job = models.ForeignKey(JobConfiguration, related_name='partner_configs', on_delete=models.DO_NOTHING)
    partner_id = models.PositiveSmallIntegerField()
    is_enabled = models.BooleanField(default=False)
    config = models.JSONField(null=True)

    class Meta:
        db_table = 'job_partner_mapping'
        unique_together = ('job', 'partner_id')
        verbose_name = 'Job Partner Mapping'
        verbose_name_plural = 'Job Partner Mappings'


class PeriodicJobRunLog(models.Model):
    created_dtm = models.DateTimeField()
    updated_dtm = models.DateTimeField()
    job_id = models.PositiveSmallIntegerField()
    # 32-character lowercase hexadecimal string
    job_run_log_id = models.CharField(max_length=35)
    status = models.PositiveSmallIntegerField()
    parameters = models.JSONField(null=True)
    # this will be populated only if setup_func fails or push to redis fails
    error_info = models.TextField(null=True)

    class Meta:
        db_table = 'periodic_job_run_log'
        verbose_name = 'Periodic Job Run Log'
        verbose_name_plural = 'Periodic Job Run Logs'


class JobRunMetaDataV2(models.Model):
    created_dtm = models.DateTimeField()
    updated_dtm = models.DateTimeField()
    job_id = models.PositiveSmallIntegerField()
    job_run_log_id = models.CharField(max_length=35, null=True)
    metadata = models.JSONField(null=True)
    error_info = models.TextField(null=True)
    status = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'job_run_meta_data_v2'
        verbose_name = 'Job Run Meta Data V2'
        verbose_name_plural = 'Job Run Meta Data V2'


class JobStatusConstant(DefaultTimeStamp):
    status = models.CharField(max_length=10)
    code = models.CharField(max_length=2)

    class Meta:
        db_table = 'job_status_constant'
        verbose_name = 'Job Status Constant'
        verbose_name_plural = 'Job Status Constants'
