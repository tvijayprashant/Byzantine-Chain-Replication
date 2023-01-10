# -*- generated by 1.0.11 -*-
import da
PatternExpr_480 = da.pat.TuplePattern([da.pat.ConstantPattern('done'), da.pat.BoundPattern('_BoundPattern483_'), da.pat.FreePattern(None), da.pat.FreePattern(None)])
PatternExpr_520 = da.pat.TuplePattern([da.pat.ConstantPattern('doneolympus')])
PatternExpr_525 = da.pat.FreePattern('olympus')
_config_object = {'channel': {'fifo', 'reliable'}, 'clock': 'lamport'}
import sys
from enum import Enum
import time
import nacl.encoding
import nacl.signing
from OrderProof import OrderProof
from OrderStatement import OrderStatement
from Crypto import Crypto
from State import State
from Validations import Validations
from ResultProof import ResultProof
from ResultStatement import ResultStatement
from Shuttle import Shuttle
from ReplicaHistory import ReplicaHistory
import pickle
from configread import configread
from TestCases import TestCases
from Operation import Operation
str_exp = ','
log_level = 20
cl = da.import_da('client')
ol = da.import_da('olympus')
rl = da.import_da('replica')

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._Node_ReceivedEvent_0 = []
        self._Node_ReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_Node_ReceivedEvent_0', PatternExpr_480, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_Node_ReceivedEvent_1', PatternExpr_520, sources=[PatternExpr_525], destinations=None, timestamps=None, record_history=True, handlers=[])])

    def run(self):
        test_files = list(range(1, 22))
        test_files.extend(['stresstest_1', 'stresstest_2'])
        for test in test_files:
            start_time = time.time()
            self.output('Test Case : ', test)
            config = configread((('config/test_' + str(test)) + '.txt'))
            self.output('configuration parameters are read from file')
            nclients = config.num_client
            nReplicas = ((2 * config.failure_num) + 1)
            crypto = Crypto()
            (olympusPrivate, olympusPublic) = crypto.getSignedKey()
            clientPrivate = []
            clientPublic = []
            for i in range(nclients):
                (private, public) = crypto.getSignedKey()
                clientPrivate.append(private)
                clientPublic.append(public)
            clients = self.new(cl.Client, num=nclients, at='ClientNode')
            clients = list(clients)
            masterDict = dict()
            testCases = TestCases(config.test_case_name, masterDict)
            olympus = self.new(ol.Olympus, num=1, at='OlympusNode')
            for i in range(nclients):
                masterDict = dict()
                if (config.test_case_name == 'stresstest'):
                    work = config.workload[i]
                    for load in work:
                        operation = Operation(load.action, load.key, load.value)
                        operation.performOperation(masterDict)
                    testCases = TestCases(config.test_case_name, masterDict)
                self._setup(clients[i], (olympus, i, clientPrivate[i], olympusPublic, config.workload[i], config.failure_num, testCases, config.client_timeout))
            self._setup(olympus, (nReplicas, clients, olympusPrivate, olympusPublic, clientPublic, config.failure, config.nonhead_timeout, config))
            self._start(olympus)
            self._start(clients)
            super()._label('_st_label_471', block=False)
            client = None

            def UniversalOpExpr_472():
                nonlocal client
                for client in clients:

                    def ExistentialOpExpr_478(client):
                        for (_, _, (_ConstantPattern496_, _BoundPattern498_, _, _)) in self._Node_ReceivedEvent_0:
                            if (_ConstantPattern496_ == 'done'):
                                if (_BoundPattern498_ == client):
                                    if True:
                                        return True
                        return False
                    if (not ExistentialOpExpr_478(client=client)):
                        return False
                return True
            _st_label_471 = 0
            while (_st_label_471 == 0):
                _st_label_471 += 1
                if UniversalOpExpr_472():
                    _st_label_471 += 1
                else:
                    super()._label('_st_label_471', block=True)
                    _st_label_471 -= 1
            else:
                if (_st_label_471 != 2):
                    continue
            if (_st_label_471 != 2):
                break
            self.output('master received done from all clients', level=log_level, sep=str_exp)
            self.send(('done',), to=clients)
            self.output('master acknowledge done to clients')
            self.output('master waiting  done from  olympus')
            super()._label('_st_label_517', block=False)
            olympus = None

            def ExistentialOpExpr_518():
                nonlocal olympus
                for (_, (_, _, olympus), (_ConstantPattern535_,)) in self._Node_ReceivedEvent_1:
                    if (_ConstantPattern535_ == 'doneolympus'):
                        if True:
                            return True
                return False
            _st_label_517 = 0
            while (_st_label_517 == 0):
                _st_label_517 += 1
                if ExistentialOpExpr_518():
                    _st_label_517 += 1
                else:
                    super()._label('_st_label_517', block=True)
                    _st_label_517 -= 1
            else:
                if (_st_label_517 != 2):
                    continue
            if (_st_label_517 != 2):
                break
            self.output('master received done from olympus. Terminating')
            end_time = time.time()
            self.output(('elapsed time (seconds):%lf' % ((end_time - start_time),)), level=log_level, sep=str_exp)
            self.output('Test Case ', test, ' Passed')
            self.output('----------------------------------------------------------------------------------------------------\n\n')
