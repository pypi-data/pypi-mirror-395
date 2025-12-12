# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

import logging

from ..elogger import get_correlation_id, set_correlation_id


def create_celery_custom_task_class(logger: logging.Logger):
    from celery import Task

    class CeleryCustomTask(Task):
        def apply_async(
            self,
            args=None,
            kwargs=None,
            task_id=None,
            producer=None,
            link=None,
            link_error=None,
            shadow=None,
            **options,
        ):
            cid = get_correlation_id()
            # add log event id to header
            if cid:
                headers = options.get("headers", {})
                if "cid" not in headers:
                    headers["cid"] = cid
                    options["headers"] = headers

            # add task to queue
            task_result = super().apply_async(
                args, kwargs, task_id, producer, link, link_error, shadow, **options
            )
            logger.info(
                f"called task {self.name} with correlation_id: {cid}",
                extra={
                    "loc": "core0006",
                    "celery_task_id": task_result.id,
                    "celery_task_name": self.name,
                    "celery_task_args": str(args),
                    "celery_task_kwargs": str(kwargs),
                },
            )
            return task_result

        def before_start(self, task_id, args, kwargs):
            headers = self.request.headers
            if isinstance(headers, dict) and "cid" in headers:
                # get log event id from headers
                cid = headers.get("cid")
            else:
                cid = get_correlation_id()

            set_correlation_id(cid)
            # run other overide before_start
            return super().before_start(task_id, args, kwargs)

        def after_return(self, status, retval, task_id, args, kwargs, einfo):
            logger.debug(
                "task done",
                extra={"celery_task_id": task_id, "celery_task_retval": str(retval)},
            )
            return super().after_return(status, retval, task_id, args, kwargs, einfo)

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            logger.critical(
                "task failed",
                extra={"celery_task_id": task_id, "celery_task_exc_info": str(einfo)},
            )
            return super().on_failure(exc, task_id, args, kwargs, einfo)

        def on_success(self, retval, task_id, args, kwargs):
            logger.debug(
                "task success",
                extra={"celery_task_id": task_id, "celery_task_retval": str(retval)},
            )
            return super().on_success(retval, task_id, args, kwargs)

    return CeleryCustomTask
