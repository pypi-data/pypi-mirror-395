"""
    * Basic implementation of a task manager for application services and ephemeral buffers*
"""
import requests
import logging
from time import sleep
from requests.exceptions import ConnectionError
from threading import Thread
from ebcommon.models_common   import Message, MessageLogin, MessageException, MessageList
from ebcommon.models_runtime  import RuntimeRequest, Runtime, RuntimeStateEnum
from ebcommon.models_mservice import Microservice
from ebcommon.models_job      import Job, JobRunStatusEnum

class EbsRuntimeRequestException(RuntimeError):
    def __init__(self, exc):
        super().__init__(exc)

class EbsRuntime(Thread):
    def __init__(self, baseurl: str, req: RuntimeRequest, uatoken: MessageLogin, Jobtype: type,
                 pooltime: int = 5, keep_going: bool = True, **context) -> None:
        super().__init__()
        self._stop = False
        self._closed = True

        self.baseurl = baseurl        # The app services URL
        self.uatoken = uatoken        # Credentials
        self.req = req                # The runtime descriptor
        self.pooltime = pooltime      # Time between job fetch
        self.keep_going = keep_going  # Continue even when there are errors in services

        self.Jobtype = Jobtype
        self.context = context
        self.desc = None          # Runtime descriptor as returned by the server
        self.mslist = {}          # List of active microservices

    def cleanExistingRuntimes(self):
        """ Clean existing runtimes binded to the same mime-type. """
        response = requests.get(f"{self.baseurl}/runtime", headers=self.uatoken.getAuthHeader())
        for rt in MessageList.castNextResponse(response, Runtime):
            if self.req.accepted_mime_type == rt.accepted_mime_type:
                logging.debug(f"[runner] delete existing runtime with {self.req.accepted_mime_type}: {rt.accepted_mime_type}")
                requests.delete(f"{self.baseurl}/runtime/{rt.uuid}", headers=self.uatoken.getAuthHeader())

    def _set(self, uid: str) -> None:
        """ Set the runtime uuid """
        self.uid = uid
        self.path = f"{self.baseurl}/runtime/{self.uid}"

    def _fetch(self, rpath: str = r'', method: str = r'GET', rtype: type = Message) -> object:
        """ Perform a get and return a casted type.  """
        response = requests.request(method, f"{self.path}{rpath}", headers=self.uatoken.getAuthHeader())
        return Message.castResponse(response, rtype)

    def publish(self) -> Runtime:
        """   """
        response = requests.post(f"{self.baseurl}/runtime", headers=self.uatoken.getAuthHeader(), json=self.req.model_dump())
        self.desc = Message.castResponse(response, Runtime)
        self._set(self.desc.uuid)
        return self.desc

    def lastState(self) -> Runtime:
        return self.desc

    def refresh(self) -> Runtime:
        self.desc = self._fetch(rtype=Runtime)
        return self.desc

    def addTag(self, tag: str) -> Runtime:
        response = requests.post(f"{self.path}/tags/{str(tag)}", headers=self.uatoken.getAuthHeader())
        Message.castResponse(response, Runtime)
        return self.refresh()

    def jobs(self) -> Job:
        response = requests.get(f"{self.path}/job", headers=self.uatoken.getAuthHeader())
        for job in MessageList.castNextResponse(response, Job):
            yield job

    def microservices(self) -> list[Microservice]:
        response = requests.get(f"{self.path}/app_service", headers=self.uatoken.getAuthHeader())
        for mservice in MessageList.castNextResponse(response, Microservice):
            yield mservice

    def lauchMicroservices(self):
        logging.debug(r'[runner] look for new Microservices.')
        for mservice in self.microservices():
            logging.debug(f'[runner] check microservices: {mservice}')
            if mservice.uuid in self.mslist: continue
            logging.info(f'[runner] create Microservice runner for {mservice.uuid}')
            ebs = EbsRuntimeService(self, mservice, self.pooltime)
            ebs.start()
            self.mslist[mservice.uuid] = ebs

    def run(self):
        logging.debug(r'[runner] microservice loop started.')
        try:
            self._closed = False
            while not self._stop:
                try:
                    desc = self.refresh()
                    if desc.state == RuntimeStateEnum.error:
                        logging.error(f'[runner] runtime in error state: {desc.state_desc}')
                        break
                    elif desc.state != RuntimeStateEnum.ready:
                        logging.warning(f'[runner] runtime not ready: {RuntimeStateEnum(desc.state)} ({desc.state_desc})')
                    else:
                        self.lauchMicroservices()
                except ConnectionError as e:
                    logging.error(f"[runtime] unexpected HTTP/S request exception: {e}")
                    if not self.keep_going: raise EbsRuntimeRequestException(e) from e
                except MessageException as m:
                    logging.error(r'[runtime] Exception while starting microservice manager: %s', str(m))
                    if not self.keep_going: raise EbsRuntimeRequestException(m) from m
                sleep(self.pooltime)
        except EbsRuntimeRequestException as m:
            logging.error(r'[runtime] unrecoverable error: %s', str(m))
        finally:
            self._closed = True

    def delete(self) -> Runtime:
        self._stop = True
        for msapp in self.mslist.values():
            msapp.delete()
        while not self._closed: sleep(self.pooltime/2)
        response = requests.delete(f"{self.path}", headers=self.uatoken.getAuthHeader())
        self.desc = MessageList.castNextResponse(response, Runtime)
        return self.desc

class EbsRuntimeService(Thread):
    def __init__(self, rt: EbsRuntime, msapp: Microservice, pooltime: int = 5) -> None:
        super().__init__()
        self._stop = False
        self._closed = True

        self.pooltime = pooltime
        self.rt = rt
        self.mservice = msapp

    def refresh(self, msuuid: str) -> Microservice:
        self.mservice = self.rt._fetch(f"/app_service/{msuuid}", rtype=Microservice)
        return self.mservice

    def jobs(self) -> Job:
        response, err = None, None
        try:
            response = requests.get(f"{self.rt.path}/app_service/{self.mservice.uuid}/job", headers=self.rt.uatoken.getAuthHeader())
            for job in MessageList.castNextResponse(response, Job):
                yield job

        except ConnectionError as e:  err = e; logging.error(f"[runtime] unexpected HTTP/S request exception: {e}")
        except MessageException as m: err = m; logging.error(r'[runtime] Exception while fetching a microservice job: %s', str(m))
        if not response:
            if not self.rt.keep_going: raise EbsRuntimeRequestException(err) from err
            else: return tuple()

    def pullJobs(self):
        for job in self.jobs():
            if job.run_status[0] != JobRunStatusEnum.pending:
                logging.info(f'[runtime] skip job, not pending: {job.uuid} = {job.run_status}')
                continue
            logging.info(f'[runtime] start task from job: {job.uuid}')
            task = self.rt.Jobtype(self.rt, self.mservice, job, **self.rt.context)
            err = task.runJob()
            if err:
                logging.error(f'[runtime] error running task {job.uuid}: {err}')

    def run(self):
        self._closed = False
        try:
            while not self._stop:
                logging.debug(f'[runtime] pull jobs for {self.rt}')
                self.pullJobs()
                sleep(self.pooltime)
        except (ConnectionError, MessageException) as m:
            logging.error(r'Exception while pulling jobs: %s', str(m))
        finally:
            self._closed = True

    def delete(self) -> None:
        self._stop = True
        while not self._closed: sleep(self.pooltime/2)

class EbsRuntimeServiceJob():
    def __init__(self, rt: EbsRuntime, mservice: Microservice, job: Job, **context) -> None:
        self.rt = rt
        self.mservice = mservice
        self.job = job

    def ebinput(self, index: int, ebin_name: str, ebin: str) -> bool:  return False
    def eboutput(self, index: int, ebin_name: str, ebin: str) -> bool: return False
    def vinput(self, index: int, name: str, value: str) -> bool:       return False
    def voutput(self, index: int, name: str) -> str:                   return False
    def execute(self) -> bool:                                         return False

    def setJobStatus(self, status: str) -> Job:
        try:
            response = requests.post(f"{self.rt.path}/job/{self.job.uuid}/status/{status}", headers=self.rt.uatoken.getAuthHeader())
            job = Message.castResponse(response, Job)
            return job is None
        except ConnectionError as e:  err = e; logging.error(f"[runtime] unexpected HTTP/S request exception: {e}")
        except MessageException as m: err = m; logging.error(r'[runtime] Exception while fetching a job status: %s', str(m))
        if not response: return err

    def setJobStatusRunning(self) -> Job:    return self.setJobStatus(r'RUNNING')
    def setJobStatusStopped(self) -> Job:    return self.setJobStatus(r'STOPPED')
    def setJobStatusCompleted(self) -> Job:  return self.setJobStatus(r'COMPLETED')
    def setJobStatusCancelled(self) -> Job:  return self.setJobStatus(r'CANCELLED')
    def setJobStatusFailed(self) -> Job:     return self.setJobStatus(r'FAILED')

    def fetchJobEbInputs(self) -> int:
        for i in range(len(self.job.ebin)):
            ebin_name = self.mservice.ebin_names[i]
            if (error := self.ebinput(i, ebin_name, self.job.ebin[i])): return error
        return False

    def pushJobEbOuputs(self) -> int:
        for i in range(len(self.job.ebout)):
            ebout_name = self.mservice.ebout_names[i]
            if (error := self.eboutput(i, ebout_name, self.job.ebout[i])): return error
        return False

    def fetchJobInputs(self) -> int:
        for i in range(len(self.job.arguments)):
            arg_name = self.mservice.argument_names[i]
            if (error := self.vinput(i, arg_name, self.job.arguments[i])): return error
        return False

    def pushJobOutputs(self) -> int:
        results = []
        for i in range(len(self.mservice.result_names)):
            arg_name = self.mservice.result_names[i]
            results.append(self.voutput(i, arg_name))
        p_results = {'value': results}
        try:
            response = requests.post(f"{self.rt.path}/job/{self.job.uuid}/results", headers=self.rt.uatoken.getAuthHeader(), params=p_results)
            job = Message.castResponse(response, Job)
            return job is None
        except ConnectionError as e:  err = e; logging.error(f"[runtime] unexpected HTTP/S request exception: {e}")
        except MessageException as m: err = m; logging.error(r'[runtime] Exception while fetching a job outputs: %s', str(m))
        if not response: return err

    def runJob(self) -> bool:
        error = False
        logging.debug(f'[runtime] start to execute a task: {self.job}')
        while True:
            if (error := self.fetchJobEbInputs()):    break
            if (error := self.setJobStatusRunning()): break

            logging.info(f'[runtime] fetch inputs: {self.job.uuid}')
            if (error := self.fetchJobInputs()):    break
            logging.info(f'[runtime] execute: {self.job.uuid}')
            if (error := self.execute()):           break
            logging.info(f'[runtime] push outputs: {self.job.uuid}')
            if (error := self.pushJobOutputs()):    break

            if (error := self.setJobStatusStopped()):    break
            logging.info(f'[runtime] push EB outputs: {self.job.uuid}')
            if (error := self.pushJobEbOuputs()):        break
            if (error := self.setJobStatusCompleted()):  break

            logging.info(f'[runtime] task fully completed: {self.job.uuid}')
            break

        if error:
            self.setJobStatusFailed()

        return error
