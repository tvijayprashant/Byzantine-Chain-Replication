# Installation of Environment

Use the command to create a new environment in conda
```
conda create --name bcr python=3.5
source activate bcr
pip install pyDistAlgo==1.0.11
pip install --upgrade pynacl
cd src
```

# Testing file for Byzantine Chain Replication

<!-- Added configuration for test: failure action: change_privatekey()  -- Replica signs the OrderStatement & Result Statement in next forward Shuttle/ Backward Shuttle with a different privatekey 

Added configuration for test: failure action: remove_operationhistory()  -- Replica doesn't store (slot,operation) pair in history




CLIENT:

	1. ask Olympus whether configuration changed (periodically or as needed)  :  test_2

	2. check that dictionary contains expected content at end of test case :  All test cases manually



OLYMPUS:
	1. upon reconfiguration-request, send wedge requests : test_2
	2. validate wedged messages : 
	3. compute initial running state (incl. replica catch-up) : test_2
	4. create keys and create and setup processes for new replicas : test_2

REPLICA:
	1. head: send reconfiguration-request if timeout waiting for result shuttle :  test_11
	2. non-head: send reconfiguration-request if timeout waiting for result shuttle after forwarding request to head :  test_12
	3. detect provable misbehavior and send reconfiguration-request : test_2 and greater
	4. head: periodically initiate checkpoint, send checkpoint shuttle : test_1
	5. non-head: add signed checkpoint proof, send updated checkpoint shuttle : test_1
	6. handle completed checkpoint shuttle : test_1
	7. validate completed checkpoint proof : test_5
	8. delete history prefix, forward completed checkpoint proof : test_1
	9. handle catch-up message, execute operations, send caught-up message : test_3
	10. fault-injection: additional triggers for phase 3 
		wedge_request(m): test_8
		new_configuration(m): test_10
		checkpoint(m): test_5
		completed_checkpoint(m): test_7
		get_running_state(m): test_6
		catch_up(m):	test_9
	11. fault-injection: additional failures for phase 3 
		crash(): test_2
		truncate_history(): test_8
		sleep(time): test_3
		drop(): test_3, test_7
		increment_slot(): test_4
		extra_op(): test_4
		invalid_order_sig(): test_3
		invalid_result_sig(): test_4
		drop_checkpt_stmts(): test_5 -->



To run Multi Host on MacOS:

	./run.sh

For Windows User (Open Each line in a new Terminal)
```bash
python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/replica0.log --logfilelevel info -n ReplicaNode0  -D replica.da
python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/replica1.log --logfilelevel info -n ReplicaNode1  -D replica.da
python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/replica2.log --logfilelevel info -n ReplicaNode2  -D replica.da
python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/replica3.log --logfilelevel info -n ReplicaNode3  -D replica.da
python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/replica4.log --logfilelevel info -n ReplicaNode4  -D replica.da
python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/replica5.log --logfilelevel info -n ReplicaNode5  -D replica.da

python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/client.log --logfilelevel info  -n ClientNode   -D client.da
python -m da -r  --message-buffer-size=1280000 --logfile --logfilename logdirect/olympus.log --logfilelevel info  -n OlympusNode  -D olympus.da
python -m da -r --message-buffer-size=1280000 --logfile --logfilename logdirect/master.log --logfilelevel 'info' -n MasterNode bcr.da
```

<!-- python3 -m da --logfile --logfilename test_1_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da config/test_1.txt
python -m da --logfile --logfilename test_2_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_2.txt
python -m da --logfile --logfilename test_3_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_3.txt
python -m da --logfile --logfilename test_4_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_4.txt
python -m da --logfile --logfilename test_5_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_5.txt
python -m da --logfile --logfilename test_6_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_6.txt
python -m da --logfile --logfilename test_7_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_7.txt
python -m da --logfile --logfilename test_8_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_8.txt
python -m da --logfile --logfilename test_9_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_9.txt
python -m da --logfile --logfilename test_10_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_10.txt
python -m da --logfile --logfilename test_11_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_11.txt
python -m da --logfile --logfilename test_12_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_12.txt
python -m da --logfile --logfilename test_13_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_13.txt -->

TEST_CASES:

### 1. Checkpointing: No Failure Case:

```
test_case_name = test_1
t = 1
num_client = 3
client_timeout = 3000
head_timeout = 3000
nonhead_timeout = 3000
checkpt_interval = 2
workload[0] = put('movie','star'); get('movie')
workload[1] = put('movie','star plus'); append('movie',' wars'); get('movie')
workload[2] = put('jedi,'luke skywalker'); slice('jedi','0:4'); get('jedi')

Description: 1 client, 3 replicas. Client sends operation. Head receives operation and modifies dict, sends forward shuttle. 
	All other replicas modify their dict and forward Shuttle. Tail sends result shuttle to client and other replicas. 
	Client verifies result shuttle. Head initiates Checkpoint Shuttle after result shuttle of 2nd slot reaches it. Chcekpointing is done.

test_1: python3 -m da --logfile --logfilename test_1_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_1.txt
```

	
### 2. Fault Injection:

```
test_case_name = test_2
t = 1
num_client = 3
client_timeout = 3000
head_timeout = 3000
nonhead_timeout = 3000
checkpt_interval = 2
workload[0] = put('movie','star'); get('movie')
workload[1] = put('movie','star'); append('movie',' wars'); get('movie')
workload[2] = put('jedi,'luke skywalker'); get('jedi')
failures[0,0] = client_request(0,1), crash()

Description: 1 client, 3 replicas. Client sends operation. Head receives operation and modifies dict, sends forward shuttle. 
All other replicas modify their dict and forward Shuttle. Tail sends result shuttle to client and other replicas. 
Client verifies result shuttle. Result is empty string because key doesn't exist.

test_2: python3 -m da --logfile --logfilename test_2_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_2.txt
```
	
### 3. Fault Injection: 

```
test_case_name = test_3
t = 1
num_client = 3
client_timeout = 3000
head_timeout = 3000
nonhead_timeout = 3000
checkpt_interval = 2
workload[0] = put('movie','star'); get('movie')
workload[1] = put('movie','stars'); append('movie',' wars'); get('movie')
workload[2] = put('jedi,'luke skywalker'); get('jedi')
failures[0,1] = shuttle(0,0), drop()
failures[1,1] = shuttle(0,0), sleep(4)



Description: 1 client, 3 replicas. Client sends operation. Head receives operation and modifies dict, sends forward shuttle. All other replicas modify their dict and forward Shuttle. Tail sends result shuttle to client and other replicas. Client verifies result shuttle. Result is fail because key doesn't exist.

test_3: python3 -m da --logfile --logfilename test_3_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_3.txt 
```
	
### 4.
```
test_case_name = test_4
t = 1
num_client = 3
client_timeout = 3000
head_timeout = 3000
nonhead_timeout = 3000
checkpt_interval = 2
workload[0] = put('movie','star'); get('movie')
workload[1] = put('movie','star'); append('movie',' wars'); get('movie')
workload[2] = put('jedi,'luke skywalker'); slice('jedi','0:4'); get('jedi')
failures[0,0] = client_request(0,0), extra_op(); client_request(0,1), increment_slot()
failures[1,1] = shuttle(1,0), invalid_result_sig()

Description: 1 client, 3 replicas. Client sends operation. Head receives operation and modifies dict, sends forward shuttle. All other replicas modify their dict and forward Shuttle. Tail sends result shuttle to client and other replicas. Client verifies result shuttle. Result is fail because key doesn't exist.

test_4: python3 -m da --logfile --logfilename test_4_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_4.txt 
```

### 5. 

```
test_case_name = test_5
t = 1
num_client = 3
client_timeout = 3000
head_timeout = 3000
nonhead_timeout = 3000
checkpt_interval = 2
workload[0] = put('movie','star'); get('movie')
workload[1] = put('movie','star'); append('movie',' wars'); get('movie')
workload[2] = put('jedi,'luke skywalker'); slice('jedi','0:4'); get('jedi')
failures[0,1] = checkpoint(0), drop_checkpt_stmts()
failures[1,1] = shuttle(0,1), invalid_order_sig()

Description: 1 client, 3 replicas. Client sends operation. Head receives operation and modifies dict, sends forward shuttle. All other replicas modify their dict and forward Shuttle. Tail sends result shuttle to client and other replicas. Client verifies result shuttle.

test_5 : python3 -m da --logfile --logfilename test_5_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_5.txt
```
	
### 6. 
```
test_case_name = test_6
t = 1
num_client = 3
client_timeout = 3000
head_timeout = 3000
nonhead_timeout = 3000
checkpt_interval = 2
workload[0] = put('movie','star'); get('movie')
workload[1] = put('movie','star'); append('movie',' wars'); get('movie')
workload[2] = put('jedi,'luke skywalker'); slice('jedi','0:4'); get('jedi')
failures[0,0] = get_running_state(0), drop()
failures[0,1] = shuttle(0,0), drop() ; get_running_state(0), drop()

Description: 1 client, 3 replicas. Client sends operation. Head receives operation and modifies dict, sends forward shuttle. All other replicas modify their dict and forward Shuttle. Tail sends result shuttle to client and other replicas. Client verifies result shuttle. 3rd Result is fail because index out of range


test_6: python3 -m da --logfile --logfilename test_6_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_6.txt
```

### 7. 
```
test_case_name = test_7
t = 1
num_client = 3
client_timeout = 3000
head_timeout = 3000
nonhead_timeout = 3000
checkpt_interval = 2
workload[0] = put('movie','star'); get('movie')
workload[1] = put('movie','star'); append('movie',' wars'); get('movie')
workload[2] = put('jedi,'luke skywalker'); slice('jedi','0:4'); get('jedi')
failures[0,1] = completed_checkpoint(0), drop()

Description: 1 client, 3 replicas. Client sends operation. Head receives operation and modifies dict, sends forward shuttle. All other replicas modify their dict and forward Shuttle. Tail sends result shuttle to client and other replicas. Client verifies result shuttle. Both results fail because key doesnt exist


test_7: python3 -m da --logfile --logfilename test_7_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_7.txt
```

### 8. 
```
test_case_name = test_8
t = 2
num_client = 3
client_timeout = 3000
head_timeout = 3000
nonhead_timeout = 3000
checkpt_interval = 2
workload[0] = put('movie','star'); get('movie')
workload[1] = put('movie','star'); append('movie',' wars'); get('movie')
workload[2] = put('jedi,'luke skywalker'); slice('jedi','0:4'); get('jedi')
failures[0,1] =  shuttle(0,1), drop() ; wedge_request(0), truncate_history()

Description: 1 client, 5 replicas. Client sends put. Head receives put and modifies dict, sends forward shuttle. All other replicas modify their dict and forward Shuttle. Tail sends result shuttle to client and sends Result Shuttle to other replicas. Client verifies result shuttle. 

test_8: python3 -m da --logfile --logfilename test_8_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_8.txt
```
### 9. 

```
test_case_name = test_9
t = 1
num_client = 2
client_timeout = 3000
head_timeout = 3000
nonhead_timeout = 3000
checkpt_interval = 2
workload[0] = put('movie','star'); get('movie')
workload[1] = put('movie','star'); append('movie',' wars'); get('movie')
workload[2] = put('jedi,'luke skywalker'); slice('jedi','0:4'); get('jedi')
failures[0,1] = shuttle(1,1), drop(); catch_up(0), extra_op()

Description: 2 client, 3 replicas. Clients sends operation. Head receives operation and modifies dict, sends forward shuttle. All other replicas modify their dict and forward Shuttle. Tail sends result shuttle to client and other replicas. Client verifies result shuttle. Result is fail because key doesn't exist.


test_9: python3 -m da --logfile --logfilename test_9_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_9.txt
```
### 10. 
```
test_case_name = test_10
t = 1
num_client = 1
client_timeout = 5000
head_timeout = 3000
nonhead_timeout = 4000
checkpt_interval = 2
workload[0] = put('movie','star'); get('movie')
failures[0,1] = new_configuration(0,0), drop()

Description:  Failure case to verify signatures at client and replicas. Here when replica:2 receives forward_shuttle for message:0 of client:0, it changes its private key and signs Order Statement and Result Statement with this key. It then transmits this result proof to client and as Backward_shuttle. Previous replica validates sign and sends reconfiguration request.Client retransmits 

test_10: python3 -m da --logfile --logfilename test_10_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_10.txt
```
### 11. 
```
test_case_name = test_11
t = 1
num_client = 1
client_timeout = 5000
head_timeout = 3000
nonhead_timeout = 4000
checkpt_interval = 2
workload[0] = put('movie','star'); get('movie')
failures[0,1] = shuttle(0,0), drop()

Description: 1 client, 3 replicas. Clients send operations. When Head receives operation client_request(0,0) it modifies forward shuttle and sends it. 
Replica:1 detects fault and sends reconfiguration request. If client 1 sends before client 0, then its shuttle passes through all replicas and gets result shuttle. 
If client 0 sends before client 1, then replica:1 doesn't accept any more requests from any client because slots would not be continuous. 
Both clients would retransmit request and time-out and then send reconfiguration request to olympus

test_11: python3 -m da --logfile --logfilename test_11_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_11.txt
```
### 12.

```
test_case_name = test_12
t = 1
num_client = 1
client_timeout = 5000
head_timeout = 4000
nonhead_timeout = 3000
checkpt_interval = 2
workload[0] = put('movie','star'); get('movie')
failures[0,2] = shuttle(0,0), drop()

Description: 2 client, 3 replicas. Client sends operation. When Replica 1 receives Forward Shuttle:0 for Client:0, it modifies forward shuttle and sends it. 
Replica:2 detects fault and sends reconfiguration request. If client 1 sends before client 0, then its shuttle passes through all replicas and gets result shuttle. 
If client 0 sends before client 1, then replica:2 doesn't accept any more requests from any client because slots would not be continuous. 
Both clients would retransmit request and time-out and then send reconfiguration request to olympus

test_12: python3 -m da --logfile --logfilename test_12_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_12.txt
```
###13. 
```
test_case_name = test_13
t = 2
num_client = 2
client_timeout = 4000
head_timeout = 4000
nonhead_timeout = 4000
workload[0] = put('movie','star'); slice('movie','1:4')
workload[1] = get('movie'); put('movie','stars')
failures[0,1] = shuttle(0,0), change_result()
failures[0,2] = result_shuttle(0,0), change_result()

Description: 2 client, 5 replicas. Client sends operation. When Replica 1 receives Forward Shuttle:0 for Client:0, it modifies forward shuttle and sends it. 
Replica:2 detects fault and sends reconfiguration request. If client 1 sends before client 0, then its shuttle passes through all replicas and gets result shuttle. 
If client 0 sends before client 1, then replica:2 doesn't accept any more requests from any client because slots would not be continuous. 
Both clients would retransmit request and time-out and then send reconfiguration request to olympus

test_13: python3 -m da --logfile --logfilename test_13_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da test_13.txt

```
### 22. 
```
stresstest_1: python -m da --logfile --logfilename stresstest_1_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da config/stresstest_1.txt

test_case_name = stresstest_1
t = 1
pseudorandom_workload[0] = put('movie','star');append('movie','wars');get('movie');slice('movie','1:3');put('movie','star1');append('movie','wars1');get('movie');slice('movie','1:2');append('movie','redemption')
pseudorandom_workload[1] = put('movie1','star');append('movie1','wars');get('movie1');slice('movie1','1:3');put('movie11','star1');append('movie11','wars1');get('movie1');slice('movie1','1:2');append('movie11','star1')
pseudorandom_workload[2] = put('movie2','star');append('movie2','wars');get('movie2');slice('movie2','1:3');put('movie21','star1');append('movie21','wars1');get('movie2');slice('movie2','1:2');append('movie21','star1')
pseudorandom_workload[3] = put('movie3','star');append('movie3','wars');get('movie3');slice('movie3','1:3');put('movie31','star1');append('movie31','wars1');get('movie3');slice('movie3','1:2');append('movie31','star1')
pseudorandom_workload[4] = put('movie4','star');append('movie4','wars');get('movie4');slice('movie4','1:3');put('movie41','star1');append('movie41','wars1');get('movie4');slice('movie4','1:2');append('movie41','star1')
pseudorandom_workload[5] = put('movie5','star');append('movie5','wars');get('movie5');slice('movie5','1:3');put('movie51','star1');append('movie51','wars1');get('movie5');slice('movie5','1:2');append('movie51','star1')
pseudorandom_workload[6] = put('movie6','star');append('movie6','wars');get('movie6');slice('movie6','1:3');put('movie61','star1');append('movie61','wars1');get('movie6');slice('movie6','1:2');append('movie61','star1')
pseudorandom_workload[7] = put('movie7','star');append('movie7','wars');get('movie7');slice('movie7','1:3');put('movie71','star1');append('movie71','wars1');get('movie7');slice('movie7','1:2');append('movie71','star1')
pseudorandom_workload[8] = put('movie8','star');append('movie8','wars');get('movie8');slice('movie8','1:3');put('movie81','star1');append('movie81','wars1');get('movie8');slice('movie8','1:2');append('movie81','star1')
pseudorandom_workload[9] = put('movie9','star');append('movie9','wars');get('movie9');slice('movie9','1:3');put('movie91','star1');append('movie91','wars1');get('movie9');slice('movie9','1:2');append('movie91','star1')
num_client = 10
client_timeout = 3000
head_timeout = 3000
nonhead_timeout = 3000

workload[0] = pseudorandom(233,100)
workload[1] = pseudorandom(234,100)
workload[2] = pseudorandom(235,100)
workload[3] = pseudorandom(236,100)
workload[4] = pseudorandom(237,100)
workload[5] = pseudorandom(238,100)
workload[6] = pseudorandom(239,100)
workload[7] = pseudorandom(240,100)
workload[8] = pseudorandom(241,100)
workload[9] = pseudorandom(242,100)

Description: stress case without failures
```

### 23. 
```
stresstest_2: python3 -m da --logfile --logfilename stresstest_2_log.txt  --logfilelevel 'info' --message-buffer-size 90000 bcr.da stresstest_2.txt

test_case_name = stresstest_2
t = 1
pseudorandom_workload[0] = put('movie','star');append('movie','wars');get('movie');slice('movie','1:3');put('movie','star1');append('movie','wars1');get('movie');slice('movie','1:2');append('movie','redemption')
pseudorandom_workload[1] = put('movie1','star');append('movie1','wars');get('movie1');slice('movie1','1:3');put('movie11','star1');append('movie11','wars1');get('movie1');slice('movie1','1:2');append('movie11','star1')
pseudorandom_workload[2] = put('movie2','star');append('movie2','wars');get('movie2');slice('movie2','1:3');put('movie21','star1');append('movie21','wars1');get('movie2');slice('movie2','1:2');append('movie21','star1')
pseudorandom_workload[3] = put('movie3','star');append('movie3','wars');get('movie3');slice('movie3','1:3');put('movie31','star1');append('movie31','wars1');get('movie3');slice('movie3','1:2');append('movie31','star1')
pseudorandom_workload[4] = put('movie4','star');append('movie4','wars');get('movie4');slice('movie4','1:3');put('movie41','star1');append('movie41','wars1');get('movie4');slice('movie4','1:2');append('movie41','star1')
pseudorandom_workload[5] = put('movie5','star');append('movie5','wars');get('movie5');slice('movie5','1:3');put('movie51','star1');append('movie51','wars1');get('movie5');slice('movie5','1:2');append('movie51','star1')
pseudorandom_workload[6] = put('movie6','star');append('movie6','wars');get('movie6');slice('movie6','1:3');put('movie61','star1');append('movie61','wars1');get('movie6');slice('movie6','1:2');append('movie61','star1')
pseudorandom_workload[7] = put('movie7','star');append('movie7','wars');get('movie7');slice('movie7','1:3');put('movie71','star1');append('movie71','wars1');get('movie7');slice('movie7','1:2');append('movie71','star1')
pseudorandom_workload[8] = put('movie8','star');append('movie8','wars');get('movie8');slice('movie8','1:3');put('movie81','star1');append('movie81','wars1');get('movie8');slice('movie8','1:2');append('movie81','star1')
pseudorandom_workload[9] = put('movie9','star');append('movie9','wars');get('movie9');slice('movie9','1:3');put('movie91','star1');append('movie91','wars1');get('movie9');slice('movie9','1:2');append('movie91','star1')
num_client = 10
client_timeout = 3000
head_timeout = 3000
nonhead_timeout = 3000

workload[0] = pseudorandom(233,100)
workload[1] = pseudorandom(234,100)
workload[2] = pseudorandom(235,100)
workload[3] = pseudorandom(236,100)
workload[4] = pseudorandom(237,100)
workload[5] = pseudorandom(238,100)
workload[6] = pseudorandom(239,100)
workload[7] = pseudorandom(240,100)
workload[8] = pseudorandom(241,100)
workload[9] = pseudorandom(242,100)
failures[0,0] = client_request(0,0), change_operation()

Description: stress case with failures
```