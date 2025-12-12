# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import time
import typing

import requests
from digitalhub.entities._commons.enums import State
from digitalhub.entities.run._base.entity import Run
from digitalhub.factory.entity import entity_factory
from digitalhub.utils.exceptions import EntityError
from digitalhub.utils.logger import LOGGER

from digitalhub_runtime_modelserve.entities._commons.enums import Actions

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_modelserve.entities.run.modelserve_run.spec import RunSpecModelserveRun
    from digitalhub_runtime_modelserve.entities.run.modelserve_run.status import RunStatusModelserveRun


class RunModelserveRun(Run):
    """
    RunModelserveRun class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecModelserveRun,
        status: RunStatusModelserveRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecModelserveRun
        self.status: RunStatusModelserveRun

    def wait(self, log_info: bool = True) -> Run:
        """
        Wait for run to finish.

        Parameters
        ----------
        log_info : bool
            If True, log information.

        Returns
        -------
        Run
            Run object.
        """
        task_kind = self.spec.task.split("://")[0]
        action = entity_factory.get_action_from_task_kind(self.kind, task_kind)

        if action == Actions.SERVE.value:
            serve_timeout = 300
            start = time.time()

            while time.time() - start < serve_timeout:
                if log_info:
                    LOGGER.info(f"Waiting for run {self.id} to deploy service.")

                self.refresh()
                if self.status.service is not None:
                    if log_info:
                        msg = f"Run {self.id} service deployed."
                        LOGGER.info(msg)
                    return self

                elif self.status.state == State.ERROR.value:
                    if log_info:
                        msg = f"Run {self.id} serving failed."
                        LOGGER.info(msg)
                    return self

                time.sleep(5)

            if log_info:
                msg = f"Waiting for run {self.id} service timed out. Check logs for more information."
                LOGGER.info(msg)

            return self

        return super().wait(log_info=log_info)

    def invoke(
        self,
        model_name: str | None = None,
        method: str = "POST",
        url: str | None = None,
        **kwargs,
    ) -> requests.Response:
        """
        Invoke served model. By default it exposes infer v2 endpoint
        (http://<service_url>/v2/models/{model_name}/infer).
        The method defaults to "POST" if data or json is provided in kwargs,
        otherwise it defaults to "GET". The function returns a requests.Response
        object.

        Parameters
        ----------
        model_name : str
            Name of the model to build the URL for.
        method : str
            Method of the request (e.g., "GET", "POST").
        url : str
            URL to invoke. If specified, it must start with the service URL
            (http:// or https:// prefixes are required and stripped before comparison).
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        requests.Response
            Response from the request.
        """
        try:
            base_url: str = self.status.service.get("url")
        except AttributeError:
            raise EntityError(
                "Url not specified and service not found on run status."
                " If a service is deploying, use run.wait() or try again later."
            )

        if url is not None and not url.removeprefix("http://").removeprefix("https://").startswith(base_url):
            raise EntityError(f"Invalid URL: {url}. It must start with the service URL: {base_url}")

        if url is None:
            model_name = model_name if model_name is not None else "model"
            url = f"http://{base_url}/v2/models/{model_name}/infer"

        if "data" not in kwargs and "json" not in kwargs:
            method = "GET"

        return requests.request(method=method, url=url, **kwargs)
