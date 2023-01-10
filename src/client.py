# -*- generated by 1.0.11 -*-
import da
PatternExpr_740 = da.pat.TuplePattern([da.pat.ConstantPattern('done')])
PatternExpr_745 = da.pat.BoundPattern('_BoundPattern747_')
PatternExpr_815 = da.pat.TuplePattern([da.pat.ConstantPattern('getconfiguration_response'), da.pat.FreePattern('isValid')])
PatternExpr_822 = da.pat.BoundPattern('_BoundPattern823_')
PatternExpr_837 = da.pat.TuplePattern([da.pat.ConstantPattern('client_operation_response'), da.pat.FreePattern('receivedOperationName'), da.pat.FreePattern('receivedOperationId'), da.pat.FreePattern('result'), da.pat.FreePattern('resultProof'), da.pat.FreePattern('c'), da.pat.FreePattern('sender')])
PatternExpr_854 = da.pat.BoundPattern('_BoundPattern855_')
PatternExpr_1100 = da.pat.TuplePattern([da.pat.ConstantPattern('configuration_response'), da.pat.FreePattern('replicas'), da.pat.FreePattern('head'), da.pat.FreePattern('tail'), da.pat.FreePattern('c'), da.pat.FreePattern('replicaPublicList'), da.pat.FreePattern('isConfigurationValidOl')])
PatternExpr_1113 = da.pat.BoundPattern('_BoundPattern1114_')
PatternExpr_748 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.BoundPattern('_BoundPattern754_')]), da.pat.TuplePattern([da.pat.ConstantPattern('done')])])
_config_object = {'channel': {'fifo', 'reliable'}, 'clock': 'lamport'}
import sys
from enum import Enum
import nacl.encoding
import nacl.signing
from OrderProof import OrderProof
from OrderStatement import OrderStatement
from Crypto import Crypto
from State import State
from Validations import Validations
from ResultProof import ResultProof
from ResultStatement import ResultStatement
from ReplicaHistory import ReplicaHistory
from Operation import Operation
from TestCases import TestCases
from ClientRequest import ClientRequest
from ReconfigurationRequestObject import ReconfigurationRequestObject
import pickle
str_exp = ','
log_level = 20
ol = da.import_da('olympus')

class Client(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._ClientReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_0', PatternExpr_740, sources=[PatternExpr_745], destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_1', PatternExpr_815, sources=[PatternExpr_822], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_814]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_2', PatternExpr_837, sources=[PatternExpr_854], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_836]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_3', PatternExpr_1100, sources=[PatternExpr_1113], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_1099])])

    def setup(self, olympus, clientNumber, signedKey, olympusPublic, workload, numberOfFailures, testCases, client_timeout, **rest_1151):
        super().setup(olympus=olympus, clientNumber=clientNumber, signedKey=signedKey, olympusPublic=olympusPublic, workload=workload, numberOfFailures=numberOfFailures, testCases=testCases, client_timeout=client_timeout, **rest_1151)
        self._state.olympus = olympus
        self._state.clientNumber = clientNumber
        self._state.signedKey = signedKey
        self._state.olympusPublic = olympusPublic
        self._state.workload = workload
        self._state.numberOfFailures = numberOfFailures
        self._state.testCases = testCases
        self._state.client_timeout = client_timeout
        self._state.olympus = self._state.olympus
        self._state.q = []
        self._state.head = None
        self._state.tail = None
        self._state.replicas = None
        self._state.upTime = self.logical_clock()
        self._state.operationId = 0
        self._state.signedKey = self._state.signedKey
        self._state.olympusPublic = self._state.olympusPublic
        self._state.replicaPublicList = []
        self._state.workload = self._state.workload
        self._state.validations = Validations()
        self._state.isValidResponse = False
        self._state.operationName = None
        self._state.isConfigurationValid = False
        self._state.t = self._state.numberOfFailures
        self._state.quoramSize = (self._state.numberOfFailures + 1)
        self._state.numberOfResponses = 0
        self._state.successfulResponseResultCountDict = None
        self._state.maxResponsesPerResult = None
        self._state.clientWorkLoadResultDict = dict()
        self._state.resultWithMaxResponses = None
        self._state.crypto = Crypto()
        self._state.receivedResponse = dict()

    def run(self):
        c = self.logical_clock()
        loadCounter = 0
        while (loadCounter < len(self._state.workload)):
            load = self._state.workload[loadCounter]
            key = load.key
            value = load.value
            self._state.operationName = load.action
            self._state.operationId = (self._state.operationId + 1)
            self._state.receivedResponse[self._state.operationId] = False
            c = self.logical_clock()
            resultReceivedForthisRequest = False
            super()._label('_st_label_455', block=False)
            _st_label_455 = 0
            while (_st_label_455 == 0):
                _st_label_455 += 1
                if self._state.isConfigurationValid:
                    self._state.isValidResponse = False
                    self._state.numberOfResponses = 0
                    self._state.successfulResponseResultCountDict = dict()
                    self._state.maxResponsesPerResult = 0
                    clientOperationReq = ClientRequest(self._state.operationName, key, value, self._id, self._state.operationId, c, self._state.clientNumber)
                    signedClientReq = self._state.crypto.sign(self._state.signedKey, clientOperationReq)
                    self.send(('client_operation_request', signedClientReq, self._state.clientNumber), to=self._state.head)
                    self.output(('Client %i sent (operationName,operationId,key,value):(%s,%s,%s,%s) to head' % (self._state.clientNumber, self._state.operationName, self._state.operationId, key, value)), level=log_level, sep=str_exp)
                    super()._label('_st_label_509', block=False)
                    _st_label_509 = 0
                    self._timer_start()
                    while (_st_label_509 == 0):
                        _st_label_509 += 1
                        if self._state.isValidResponse:
                            self.output(('Client:%i received VALID result' % (self._state.clientNumber,)), level=log_level, sep=str_exp)
                            resultReceivedForthisRequest = True
                            self.modifyDictionary(self._state.resultWithMaxResponses, self._state.clientWorkLoadResultDict, self._state.operationName, key, value)
                            _st_label_509 += 1
                        elif self._timer_expired:
                            self.output(('Client :%i Failed to receive the response in time, sending request to all replicas' % (self._state.clientNumber,)), level=log_level, sep=str_exp)
                            self._state.numberOfResponses = 0
                            self._state.successfulResponseResultCountDict = dict()
                            self._state.maxResponsesPerResult = 0
                            super()._label('_st_label_548', block=False)
                            _st_label_548 = 0
                            self._timer_start()
                            while (_st_label_548 == 0):
                                _st_label_548 += 1
                                if self._state.isConfigurationValid:
                                    clientRetrasmitReq = ClientRequest(self._state.operationName, key, value, self._id, self._state.operationId, c, self._state.clientNumber)
                                    signedClientRetransmitReq = self._state.crypto.sign(self._state.signedKey, clientRetrasmitReq)
                                    self.send(('client_retransmission_request', signedClientRetransmitReq, self._state.clientNumber), to=self._state.replicas)
                                    super()._label('_st_label_578', block=False)
                                    _st_label_578 = 0
                                    self._timer_start()
                                    while (_st_label_578 == 0):
                                        _st_label_578 += 1
                                        if (self._state.numberOfResponses == ((2 * self._state.t) + 1)):
                                            self.output(('Client :%i received :%i responses from replicas' % (self._state.clientNumber, self._state.numberOfResponses)), level=log_level, sep=str_exp)
                                            if (self._state.maxResponsesPerResult >= (self._state.t + 1)):
                                                self.output(('Client :%i received :%i correct quorum of correct result:%s from replicas' % (self._state.clientNumber, self._state.maxResponsesPerResult, self._state.resultWithMaxResponses)), level=log_level, sep=str_exp)
                                                resultReceivedForthisRequest = True
                                                self.modifyDictionary(self._state.resultWithMaxResponses, self._state.clientWorkLoadResultDict, self._state.operationName, key, value)
                                            else:
                                                self.output(("Client :%i hasn't received :%i correct quorum of correct results from replicas.Initiating reconfiguration" % (self._state.clientNumber, self._state.maxResponsesPerResult)), level=log_level, sep=str_exp)
                                                self.initiateReconfigurationRequest(self._state.signedKey, self._state.clientNumber, 'client')
                                            _st_label_578 += 1
                                        elif self._timer_expired:
                                            self.output(('Client :%i Failed to receive the response from all the replicas.Initiating reconfiguration' % self._state.clientNumber), level=log_level, sep=str_exp)
                                            self.initiateReconfigurationRequest(self._state.signedKey, self._state.clientNumber, 'client')
                                            if (self._state.maxResponsesPerResult >= (self._state.t + 1)):
                                                self.output(('But, Client :%i received :%i correct quorum of correct result:%s from replicas' % (self._state.clientNumber, self._state.maxResponsesPerResult, self._state.resultWithMaxResponses)), level=log_level, sep=str_exp)
                                                resultReceivedForthisRequest = True
                                                self.modifyDictionary(self._state.resultWithMaxResponses, self._state.clientWorkLoadResultDict, self._state.operationName, key, value)
                                            _st_label_578 += 1
                                        else:
                                            super()._label('_st_label_578', block=True, timeout=self._state.client_timeout)
                                            _st_label_578 -= 1
                                    else:
                                        if (_st_label_578 != 2):
                                            continue
                                    if (_st_label_578 != 2):
                                        break
                                    _st_label_548 += 1
                                elif self._timer_expired:
                                    self.output(('Client :%i has not received valid configuration from olympus' % self._state.clientNumber), level=log_level, sep=str_exp)
                                    _st_label_548 += 1
                                else:
                                    super()._label('_st_label_548', block=True, timeout=self._state.client_timeout)
                                    _st_label_548 -= 1
                            else:
                                if (_st_label_548 != 2):
                                    continue
                            if (_st_label_548 != 2):
                                break
                            _st_label_509 += 1
                        else:
                            super()._label('_st_label_509', block=True, timeout=self._state.client_timeout)
                            _st_label_509 -= 1
                    else:
                        if (_st_label_509 != 2):
                            continue
                    if (_st_label_509 != 2):
                        break
                    _st_label_455 += 1
                else:
                    super()._label('_st_label_455', block=True)
                    _st_label_455 -= 1
            else:
                if (_st_label_455 != 2):
                    continue
            if (_st_label_455 != 2):
                break
            if (resultReceivedForthisRequest == True):
                self._state.receivedResponse[self._state.operationId] = True
                loadCounter = (loadCounter + 1)
                self.output(('client %i workload after request %i is %s' % (self._state.clientNumber, loadCounter, self._state.clientWorkLoadResultDict)), level=log_level, sep=str_exp)
        resdict = self._state.clientWorkLoadResultDict
        self.output(('client %i workload output:%s' % (self._state.clientNumber, self._state.clientWorkLoadResultDict)), level=log_level, sep=str_exp)
        if self._state.testCases.verify(self._state.clientNumber, self._state.clientWorkLoadResultDict, resdict):
            self.output('Test Case PASSED')
        else:
            self.output('Test Case FAILED')
        self.send(('done', self._id, self._state.clientNumber, self._state.clientWorkLoadResultDict), to=self.parent())
        super()._label('_st_label_737', block=False)
        _st_label_737 = 0
        while (_st_label_737 == 0):
            _st_label_737 += 1
            if PatternExpr_748.match_iter(self._ClientReceivedEvent_0, _BoundPattern754_=self.parent(), SELF_ID=self._id):
                _st_label_737 += 1
            else:
                super()._label('_st_label_737', block=True)
                _st_label_737 -= 1
        self.output(('client:%i received done from master' % self._state.clientNumber), level=log_level, sep=str_exp)
        self.output(('client:%i sending done to olympus' % self._state.clientNumber), level=log_level, sep=str_exp)
        self.send(('done', self._id, self._state.clientNumber), to=self._state.olympus)
        self.output(('Client %i terminating' % self._state.clientNumber), level=log_level, sep=str_exp)

    def modifyDictionary(self, resultWithMaxResponses, clientWorkLoadResultDict, operationName, key, value):
        if (resultWithMaxResponses == 'OK'):
            operation = Operation(operationName, key, value)
            result = operation.performOperation(clientWorkLoadResultDict)

    def initiateReconfigurationRequest(self, privateKey, index, type):
        self._state.isConfigurationValid = False
        req = ReconfigurationRequestObject(self._id)
        signedReq = self._state.crypto.sign(privateKey, req)
        self.send(('reconfiguration_request', signedReq, index, type), to=self._state.olympus)

    def _Client_handler_814(self, isValid):
        self.output(('Client %i setting isConfigurationValid to :%s' % (self._state.clientNumber, isValid)), level=log_level, sep=str_exp)
        self._state.isConfigurationValid = isValid
    _Client_handler_814._labels = None
    _Client_handler_814._notlabels = None

    def _Client_handler_836(self, receivedOperationName, receivedOperationId, result, resultProof, c, sender):
        self.output(('Client:%i received result:%s from %s' % (self._state.clientNumber, result, sender)), level=log_level, sep=str_exp)
        if (sender == 'olympus'):
            self.output('Sending Result Shuttle response to Olympus')
            self.send(('result_shuttle_response', self._state.clientNumber), to=self._state.olympus)
            if (self._state.receivedResponse[receivedOperationId] == True):
                self.output('Client has already received result Shuttle')
            else:
                self.output('Processing started for Olympus result Shuttle')
                self._state.isValidResponse = self._state.validations.responseReceivedWithCorrectOperation(self._state.operationName, self._state.operationId, receivedOperationName, receivedOperationId)
                self.output(('Client:%i is operation valid: %s' % (self._state.clientNumber, str(self._state.isValidResponse))), level=log_level, sep=str_exp)
                (isResultValid, reason) = self._state.validations.clientValidationOfResultProofOlympus(result, resultProof, self._state.replicaPublicList, self._id, self._state.t)
                self.output(('Client:%i %s' % (self._state.clientNumber, str(reason))), level=log_level, sep=str_exp)
                self._state.isValidResponse = (self._state.isValidResponse and isResultValid)
                (self._state.numberOfResponses == ((2 * self._state.t) + 1))
                if self._state.isValidResponse:
                    if (result in self._state.successfulResponseResultCountDict):
                        self._state.successfulResponseResultCountDict[result] = (self._state.successfulResponseResultCountDict[result] + 1)
                    else:
                        self._state.successfulResponseResultCountDict[result] = (self._state.t + 1)
                    if (self._state.maxResponsesPerResult < self._state.successfulResponseResultCountDict[result]):
                        self._state.maxResponsesPerResult = self._state.successfulResponseResultCountDict[result]
                        self._state.resultWithMaxResponses = result
        else:
            self._state.isValidResponse = self._state.validations.responseReceivedWithCorrectOperation(self._state.operationName, self._state.operationId, receivedOperationName, receivedOperationId)
            self.output(('Client:%i is operation valid: %s' % (self._state.clientNumber, str(self._state.isValidResponse))), level=log_level, sep=str_exp)
            (isResultValid, reason) = self._state.validations.clientValidationOfResultProof(result, resultProof, self._state.replicaPublicList, self._id, self._state.t)
            self.output(('Client:%i %s' % (self._state.clientNumber, str(reason))), level=log_level, sep=str_exp)
            self._state.isValidResponse = (self._state.isValidResponse and isResultValid)
            self._state.numberOfResponses = (self._state.numberOfResponses + 1)
            if self._state.isValidResponse:
                if (result in self._state.successfulResponseResultCountDict):
                    self._state.successfulResponseResultCountDict[result] = (self._state.successfulResponseResultCountDict[result] + 1)
                else:
                    self._state.successfulResponseResultCountDict[result] = 1
                if (self._state.maxResponsesPerResult < self._state.successfulResponseResultCountDict[result]):
                    self._state.maxResponsesPerResult = self._state.successfulResponseResultCountDict[result]
                    self._state.resultWithMaxResponses = result
    _Client_handler_836._labels = None
    _Client_handler_836._notlabels = None

    def _Client_handler_1099(self, replicas, head, tail, c, replicaPublicList, isConfigurationValidOl):
        self.output(('Client %i received :%s: configuration_response from olympus' % (self._state.clientNumber, isConfigurationValidOl)), level=log_level, sep=str_exp)
        self._state.head = head
        self._state.tail = tail
        self._state.replicas = replicas
        self._state.replicaPublicList = replicaPublicList
        self._state.isConfigurationValid = isConfigurationValidOl
    _Client_handler_1099._labels = None
    _Client_handler_1099._notlabels = None
