import os, time
import logging
import threading

class SupervisordApi:
    def __init__(self, host = None, port = None):
        #self.logger = logging.getLogger(__name__)
        self.server = None
        self.host = host if host else "localhost"
        self.port = port if port else 9001
        try:
            server_url = "http://%s:%d/RPC2"%(self.host, self.port)
            self.server = None
            try:
                import xmlrpclib
                self.server = xmlrpclib.Server(server_url)
            except:
                from xmlrpc.client import ServerProxy
                self.server = ServerProxy(server_url)
        except Exception as e:
            #self.logger.error("Error: %s"%(str(e)))
            raise e

    def get_server_status(self):
        #self.logger.debug("Supervisord: get server status")
        try:
            return self.server.supervisor.getState()
        except Exception as e:
            #self.logger.error("Error: %s"%(str(e)))
            return e
    
    def restart_server(self):
        #self.logger.debug("Supervisord: restart supervisord server")
        try:
            return self.server.supervisor.restart()
        except Exception as e:
            #self.logger.error("Error: %s"%(str(e)))
            return e
    def get_process_info(self, name):
        #self.logger.debug("Supervisord: get project info %s"%(name))
        try:
            return self.server.supervisor.getProcessInfo(name)
        except Exception as e:
            #self.logger.error("Error: %s"%(str(e)))
            return e

    def get_all_process_info(self):
        #self.logger.debug("Supervisord: get all process info")
        try:
            return self.server.supervisor.getAllProcessInfo()
        except Exception as e:
            #self.logger.error("Error: %s"%(str(e)))
            return e

    def start_process(self, name):
        #self.logger.debug("Supervisord: start process %s"%(name))
        try:
            return self.server.supervisor.startProcess(name)
        except Exception as e:
            if "ALREADY_STARTED" in str(e):
                #self.logger.info("Error: %s"%(str(e)))
                return True
            else:
                pass
                #self.logger.error("Error: %s"%(str(e)))
            return e

    def start_all_processes(self):
        #self.logger.debug("Supervisord: start all project")
        try:
            return self.server.supervisor.startAllProcesses()
        except Exception as e:
            #self.logger.error("Error: %s"%(str(e)))
            return e

    def start_process_group(self, name):
        #self.logger.debug("Supervisord: start project group %s"%(name))
        try:
            return self.server.supervisor.startProcessGroup(name)
        except Exception as e:
            if "ALREADY_STARTED" in str(e):
                #self.logger.info("Error: %s"%(str(e)))
                return True
            else:
                pass
                #self.logger.error("Error: %s"%(str(e)))
            return e

    def stop_process(self, name):
        #self.logger.debug("Supervisord: stop process %s"%(name))
        try:
            return self.server.supervisor.stopProcess(name)
        except Exception as e:
            #self.logger.error("Error: %s"%(str(e)))
            return e

    def stop_process_group(self, name):
        #self.logger.debug("Supervisord: stop process group %s"%(name))
        try:
            return self.server.supervisor.stopProcessGroup(name)
        except Exception as e:
            #self.logger.error("Error: %s"%(str(e)))
            return e

    def stop_all_processes(self):
        #self.logger.debug("Supervisord: stop all process")
        try:
            return self.server.supervisor.stopAllProcesses()
        except Exception as e:
            #self.logger.error("Error: %s"%(str(e)))
            return e

    def reload_config(self):
        #self.logger.debug("Supervisord: reload (update) config")
        try:
            return self.server.supervisor.reloadConfig()
        except Exception as e:
            #self.logger.error("Error: %s"%(str(e)))
            return e

    def add_process_group(self, name):
        #self.logger.debug("Supervisord: add process group %s"%(name))
        try:
            return self.server.supervisor.addProcessGroup(name)
        except Exception as e:
            if "ALREADY_ADDED" in str(e):
                #self.logger.info("Error: %s"%(str(e)))
                return True
            else:
                pass
                #self.logger.error("Error: %s"%(str(e)))
            return e

    def remove_process_group(self, name):
        #self.logger.debug("Supervisord: remove process group %s"%(name))
        try:
            return self.server.supervisor.removeProcessGroup(name)
        except Exception as e:
            #self.logger.error("Error: %s"%(str(e)))
            return e

    def start_job(self, name):
        #self.logger.debug("Supervisord: start job %s reload_config --> add_process_group --> start"%(name))
        self.reload_config()
        self.add_process_group(name)
        self.start_process(name)
        return 0

    def delete_job(self, name):
        #self.logger.debug("Supervisord: delete job %s Stop_job --> remove_process_group --> delete_config_file --> reload_config"%(name))
        self.stop_process(name)
        time.sleep(1)
        self.remove_process_group(name)
        return 0

    def remove_exited_job(self):
        time.sleep(2)
        job_list = self.get_all_process_info()
        if not job_list:
            #self.logger.warning("Error: %s"%(str(job_list)))
            return 1
        if not type(job_list).__name__  == "list":
            #self.logger.warning("Error, data type is not list: %s"%(str(job_list)))
            return 1
        for job in job_list:
            if job["state"] == 100:
                t = threading.Thread(target=self.delete_job,
                    args=(job["name"],)
                )
                t.start()
        time.sleep(3)
        return 0

