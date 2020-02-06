import sys
import json
from kapacitor.udf.agent import Agent, Handler, Server
from kapacitor.udf import udf_pb2
import signal

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger()


# Mirrors all points it receives back to Kapacitor
class pythonTest(Handler):


    def __init__(self, agent):
        self._agent = agent



    def info(self):
        response = udf_pb2.Response()
        response.info.wants = udf_pb2.STREAM
        response.info.provides = udf_pb2.STREAM
        return response

    def init(self, init_req):
        response = udf_pb2.Response()
        response.init.success = True
        self._f = open("/home/kapacitor/pythonTestOutput.txt","w+")

        return response

    def snapshot(self):
        response = udf_pb2.Response()
        response.snapshot.snapshot = ''
        return response

    def restore(self, restore_req):
        response = udf_pb2.Response()
        response.restore.success = False
        response.restore.error = 'not implemented'
        return response

    def begin_batch(self, begin_req):
        raise Exception("not supported")

    def point(self, point):
        response = udf_pb2.Response()
        response.point.CopyFrom(point)

        self._f.write("" + str(point) + "\n")
        self._f.flush()

        self._agent.write_response(response, True)

    def end_batch(self, end_req):
        raise Exception("not supported")

if __name__ == '__main__':
    # Create an agent
    agent = Agent()

    # Create a handler and pass it an agent so it can write points
    h = pythonTest(agent)


    # Set the handler on the agent
    agent.handler = h

    # anything printed to STDERR from a UDF process gets captured into the logs
    logger.info("Starting agent for pythonTestHandler")
    agent.start()
    agent.wait()
    logger.info("Agent finished")