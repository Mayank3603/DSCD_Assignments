import grpc
from concurrent import futures
import node_pb2 as node
import node_pb2_grpc
import time
import threading
import random

class RaftNodeImplementation(node_pb2_grpc.RaftServiceServicer):
    def __init__(self, node_id, port, node_ips, lease_duration=100):
        self.node_id = node_id
        self.currTerm = 0
        self.votedFor = None
        self.log = []
        self.commitLength = 0
        self.currRole = "Follower"
        self.currLeader = None
        self.votesReceived = set()
        self.sentLength = {}
        self.ackedLength = {}
        self.lease_duration = 0
        # self.lease_timer = None
        self.election_timer = random.randint(5,10)
        self.heartbeat_interval = 1
        self.ip = "localhost"
        self.port = port
        self.node_ip = f"localhost:{port}"
        self.node_ips = node_ips
        self.data = {}

        self.election_timer_thread = threading.Thread(target=self.run_election_timer)
        self.election_timer_thread.daemon = True
        self.election_timer_thread.start()
        
        self.lease_timer_thread = threading.Thread(target=self.run_lease_timer)
        self.lease_timer_thread.daemon = True
        self.lease_timer_thread.start()

        self.heartbeat_thread = None
        if self.currRole == "Leader":
            self.start_heartbeat_thread()

    def run_lease_timer(self):
        while True:
            if(self.currLeader is not None):
                self.start_lease_timer()
                time.sleep(1)

    def start_lease_timer(self):
        #if(self.currRole == "Leader"): 
        while self.lease_duration > 0:
            time.sleep(1)
            self.lease_duration -= 1
            print(f"Node {self.node_id} Lease Duration: {self.lease_duration} seconds.")
        if(self.lease_duration == 0):
            self.become_follower()
            # self.start_election()

    def become_follower(self):
        self.currRole = "Follower"
        print(f"Node {self.node_id} became Follower after lease timeout.")

    def updateLogs(self):
        if self.currLeader is not None:
            try:
                leader_ip = self.node_ips[self.currLeader]
                channel = grpc.insecure_channel(leader_ip)
                stub = node_pb2_grpc.RaftServiceStub(channel)
                last_log_index = len(self.log) - 1
                last_log_term = self.log[last_log_index]['term'] if self.log else 0
                request = node.LogReplicationRequest(
                    node_id=self.node_id,
                    last_log_index=last_log_index,
                    last_log_term=last_log_term
                )
                response = stub.ReplicateLogs(request)

                for log_entry in response.log_entries:
                    # print(log_entry.index, len(self.log))
                    if log_entry.index >= len(self.log):
                        self.log.extend([None] * (log_entry.index - len(self.log) + 1))
                    if self.log[log_entry.index] is None or self.log[log_entry.index]['term'] != log_entry.term:
                        self.log[log_entry.index] = {
                            'term': log_entry.term,
                            'key': log_entry.key,
                            'operation': log_entry.operation,
                            'value': log_entry.value,
                            'index': log_entry.index
                        }
                print(f"Node {self.node_id} logs updated successfully.")
            except Exception as e:
                print(f"Failed to update logs from leader: {e}")

    def ReplicateLogs(self, request, context):
        print(f"Node {self.node_id} received LogReplicationRequest from Node {request.node_id}.")
        last_log_index = request.last_log_index
        last_log_term = request.last_log_term
        log_entries = []
        for index, entry in enumerate(self.log[last_log_index + 1:], start=last_log_index + 1):
            log_entry = node.LogEntry(
                index=index,
                term=entry['term'],
                key=entry['key'],
                operation=entry['operation'],
                value=entry['value']
            )
            log_entries.append(log_entry)
        response = node.LogReplicationResponse(log_entries=log_entries)
        return response

    def run_election_timer(self):
        while True:
            if self.currRole in ["Follower", "Candidate"]:
                self.start_election_timer()
            time.sleep(1)

    def start_heartbeat_thread(self):
        self.heartbeat_thread = threading.Thread(target=self.heartbeat_thread_func)
        self.heartbeat_thread.daemon = True
        self.heartbeat_thread.start()

    def heartbeat_thread_func(self):
        while self.currRole == "Leader":
            self.send_heartbeats()
            time.sleep(self.heartbeat_interval)

    def start_election(self):
        print("<--------------- starting election ------------------>")
        self.currTerm += 1
        self.currRole = "Candidate"
        self.votedFor = self.node_id
        with open(f"logs_node_{self.node_id}/metadata.txt", "w") as f:
            f.write(f"Current Term: {self.currTerm}\n Commit Lengt: {self.commitLength}\n VotedFor: {self.votedFor}\n")
        f.close()
        self.votesReceived.add(self.node_id)
        self.lastTerm = self.log[-1].get('term', 0) if self.log else 0
        temp=0
        for i in self.node_ips.values():
            if i != self.node_ip:
                try:
                    channel = grpc.insecure_channel(i)
                    stub = node_pb2_grpc.RaftServiceStub(channel)
                    request = node.RequestVoteRequest(term=self.currTerm, candidate_id=self.node_id,
                                                      last_log_index=len(self.log) - 1, last_log_term=self.lastTerm)
                    response = stub.RequestVote(request)
                    if response.vote_granted:
                        self.votesReceived.add(i)
                    temp=max(temp,response.lease_duration)
                except Exception as e:
                    print(f"Node {self.node_id} failed to send or receive RequestVote RPC to/from Node {i}. Error: {e}")
                    continue

        self.check_votes(temp)
        self.election_timer = random.randint(5,10)
        self.start_election_timer()

    def check_votes(self, oldLeaseWaitTimer):
        if len(self.votesReceived) > (len(self.node_ips) + 1) // 2:
            self.waitForOldLease(oldLeaseWaitTimer)
            print(f"Node {self.node_id} received majority votes. Transitioning to Leader.")
            self.become_leader()
        else:
            print(f"Node {self.node_id} did not receive majority votes yet.")

    def waitForOldLease(self, oldLeaseWaitTimer):
        time.sleep(oldLeaseWaitTimer)

    def start_election_timer(self):
        while self.election_timer > 0:
            time.sleep(1)
            self.election_timer -= 1
        if self.currRole == "Follower":
            self.start_election()
        elif self.currRole == "Candidate":
            self.start_election()

    def send_heartbeats(self):
        for i,follower in self.node_ips.items():
            if follower != self.node_ip:
                print(f"Node {self.node_id} sending heartbeat to Node {follower}.")
                try:
                    channel = grpc.insecure_channel(follower)
                    stub = node_pb2_grpc.RaftServiceStub(channel)
                    prev_log_index = self.sentLength.get(follower, 0) - 1
                    prev_log_term = self.log[prev_log_index].get('term', 0) if prev_log_index >= 0 else 0
                    request = node.AppendEntriesRequest(
                        term=self.currTerm,
                        leader_id=self.node_id,
                        prev_log_index=prev_log_index,
                        prev_log_term=prev_log_term,
                        entries=[],
                        leader_commit=self.commitLength,
                        lease_duration=self.lease_duration
                    )
                    response = stub.AppendEntries(request)
                    print(f"Node {self.node_id} received heartbeat response from Node {follower}.")
                    if response.success == "True":
                        self.ackedLength[follower] = self.sentLength[follower]
                except Exception as e:
                    print(
                        f"Node {self.node_id} failed to send or receive heartbeat to/from Node {follower}. Error: {e}")
                    continue
        self.election_timer = random.randint(5,10)

    def AppendEntries(self, request, context):
            print(f"Node {self.node_id} received AppendEntries RPC from Node {request.leader_id}.")
            self.currLeader = request.leader_id
            response = node.AppendEntriesResponse(currTerm=self.currTerm, success="False")
            if request.term >= self.currTerm:
                self.transition_to_follower(request.term)
                response.currTerm = self.currTerm
                response.success = "True"
                self.ackedLength[request.leader_id] = len(self.log)
                if len(request.entries) > 0:
                    for entry in request.entries:
                        self.apply_entry(entry)
        
            if self.currRole == "Leader":
                self.restart_lease_timer()

            if request.lease_duration > self.lease_duration:
                self.lease_duration = request.lease_duration
            
            if request.leader_commit > self.commitLength:
                self.commitLength = min(request.leader_commit, len(self.log))
                with open (f"logs_node_{self.node_id}/metadata.txt", "w") as f:
                    f.write(f"Current Term: {self.currTerm}\n Commit Length: {self.commitLength}\n VotedFor: {self.votedFor}\n")
                f.close()
                self.commit_log_entries()
            self.election_timer = random.randint(5,10)
            return response

    def RequestVote(self, request, context):
            print(f"Node {self.node_id} received RequestVote RPC from Node {request.candidate_id} for term {request.term}.")
            if request.term > self.currTerm:
                print(f"Node {self.node_id} transitioning to follower for term {request.term}.")
                self.transition_to_follower(request.term)
            lastTerm = self.log[-1].get('term', 0) if self.log else 0
            logOk = (request.last_log_term > lastTerm) or \
                    (request.last_log_term == lastTerm and request.last_log_index >= len(self.log) - 1)
            # print(f"Node {self.node_id} logOk: {logOk}")
            if request.term == self.currTerm and logOk and self.votedFor in {request.candidate_id, None}:
                self.votedFor = request.candidate_id
                # self.meta_file.write(f"Current Term: {self.currTerm}\n Commit Length{self.commitLength}\n VotedFor: {self.votedFor}\n")
                with open(f"logs_node_{self.node_id}/metadata.txt", "w") as f:
                    f.write(f"Current Term: {self.currTerm}\n Commit Length: {self.commitLength}\n VotedFor: {self.votedFor}\n")
                f.close()
                print(f"Node {self.node_id} voted for Node {request.candidate_id} for term {request.term}.")
                return node.RequestVoteResponse(term=self.currTerm, vote_granted=True, lease_duration=self.lease_duration)
            else:
                print(f"Node {self.node_id} did not vote for Node {request.candidate_id} for term {request.term}.")
                return node.RequestVoteResponse(term=self.currTerm, vote_granted=False, lease_duration=self.lease_duration)

    def apply_entry(self, entry):
        if entry.operation == "GET":
            value = self.get(entry.key)
        elif entry.operation == "SET":
            self.log.append({'term': entry.term, 'operation': entry.operation, 'key': entry.key, 'value': entry.value, 'index': len(self.log)})
            # self.log_file.write(f"SET {entry.key} {entry.value} {entry.term}\n")
            with open(f"logs_node_{self.node_id}/logs.txt", "a") as f:
                f.write(f"SET {entry.key} {entry.value} {entry.term}\n")
            f.close()
            print(f"Node {self.node_id} added SET operation to log for key: {entry.key}, value: {entry.value}, index: {len(self.log)}") 
        else :
            self.log.append({'term': entry.term, 'operation': entry.operation, 'key': entry.key, 'value': entry.value, 'index': len(self.log)})
            # self.log_file.write(f"NO-OP {entry.term}\n")
            with open(f"logs_node_{self.node_id}/logs.txt", "a") as f:
                f.write(f"NO-OP {entry.term}\n")
            f.close()
            print(f"Node {self.node_id} added NO-OP operation to log for key: {entry.key}, value: {entry.value}, index: {len(self.log)}")

    def commit_log_entries(self):
        for i in range(self.commitLength):
            entry = self.log[i]
            if entry['operation'] == "SET":
                self.data[entry['key']] = entry['value']
                print(f"Node {self.node_id} committed SET operation for key: {entry['key']}, value: {entry['value']}")

    def get(self, key):
        return self.data[key] if key in self.data else None

    def ServeGet(self, request, context):
        key = request.key
        value = self.get(key)
        return node.GetReply(value=value)

    def ServeSet(self, request, context):
        key = request.key
        value = request.value
        log_entry = {'term': self.currTerm, 'operation': "SET", 'key': key, 'value': value, 'index': len(self.log)} #commit later?
        self.log.append(log_entry)
        # self.log_file.write(f"SET {key} {value} {self.currTerm}\n")
        with open(f"logs_node_{self.node_id}/logs.txt", "a") as f:
            f.write(f"SET {key} {value} {self.currTerm}\n")
        f.close()

        print(f"Node {self.node_id} added SET operation to log for key: {key}, value: {value}")
        
        for follower in self.node_ips.values():
            if follower != self.node_ip:
                print(f"Node {self.node_id} sending LOG to Node {follower}.") 
                self.replicate_log_entry(log_entry, self.node_id, follower)
        return node.SetReply(Success="True")  

    def replicate_log_entry(self, log_entry, leader_id, follower_id):
        print(f"Node {self.node_id} sending AppendEntries RPC to Node {follower_id}.")
        try:
            channel = grpc.insecure_channel(follower_id)
            stub = node_pb2_grpc.RaftServiceStub(channel)
            prev_log_index = self.sentLength.get(follower_id, 0) - 1
            prev_log_term = self.log[prev_log_index]['term'] if prev_log_index >= 0 else 0
            request = node.AppendEntriesRequest(
                term=self.currTerm,
                leader_id=leader_id,
                prev_log_index=prev_log_index,
                prev_log_term=prev_log_term,
                entries=[log_entry],
                leader_commit=self.commitLength,
                lease_duration=self.lease_duration
            )
            response = stub.AppendEntries(request)
            print(f"Node {self.node_id} received AppendEntriesResponse RPC from Node {follower_id}.")
            if response.success == "True":
                self.sentLength[follower_id] += 1
                self.ackedLength[follower_id] = self.sentLength[follower_id]
                self.data[log_entry['key']] = log_entry['value']
                self.commitLength += 1
                # self.meta_file.write(f"Current Term: {self.currTerm}\n Commit Length{self.commitLength}\n VotedFor: {self.votedFor}\n")
                with open(f"logs_node_{self.node_id}/metadata.txt", "w") as f:
                    f.write(f"Current Term: {self.currTerm}\n Commit Length: {self.commitLength}\n VotedFor: {self.votedFor}\n")
                f.close()
        except Exception as e:
            print(
                f"Node {self.node_id} failed to send or receive AppendEntries RPC to/from Node {follower_id}. Error: {e}")
            return

    def become_leader(self):
        self.currRole = "Leader"
        self.currLeader = self.node_id
        self.lease_duration = 10
        print(f"Node {self.node_id} became Leader for term {self.currTerm}.")
        self.start_heartbeat_thread()
        log_entry = {'term': self.currTerm, 'operation': "NO-OP", 'key': "", 'value': "", 'index': len(self.log)}
        # self.log_file.write(f"NO-OP {self.currTerm}\n")
        with open(f"logs_node_{self.node_id}/logs.txt", "a") as f:
            f.write(f"NO-OP {self.currTerm}\n")
        f.close()
        self.log.append(log_entry)
        for follower in self.node_ips.values():
            if follower != self.node_ip:
                self.sentLength[follower] = len(self.log)
                self.ackedLength[follower] = 0
                self.sentLength[follower] = len(self.log)
                self.ackedLength[follower] = 0

                channel = grpc.insecure_channel(follower)
                stub = node_pb2_grpc.RaftServiceStub(channel)
                prev_log_index = self.sentLength.get(follower, 0) - 1
                prev_log_term = self.log[prev_log_index]['term'] if prev_log_index >= 0 else 0
                log_entry = {'term': self.currTerm, 'operation': "NO-OP", 'key': "", 'value': "",'index': len(self.log)}


                request = node.AppendEntriesRequest(
                    term=self.currTerm,
                    leader_id=self.node_id,
                    prev_log_index=prev_log_index,
                    prev_log_term=prev_log_term,
                    entries=[log_entry],
                    leader_commit=self.commitLength,
                    lease_duration=self.lease_duration
                )
                response = stub.AppendEntries(request)
                print(f"Node {self.node_id} received AppendEntriesResponse RPC from Node {follower}.")

    def transition_to_follower(self, term):
        self.currTerm = term
        self.currRole = "Follower"
        self.votedFor = None
        # self.meta_file.write(f"Current Term: {self.currTerm}\n Commit Length{self.commitLength}\n VotedFor: {self.votedFor}\n")
        with open(f"logs_node_{self.node_id}/metadata.txt", "w") as f:
            f.write(f"Current Term: {self.currTerm}\n Commit Length: {self.commitLength}\n VotedFor: {self.votedFor}\n")
        f.close()

    # def __del__(self):
    #     self.log_file.close()
    #     self.meta_file.close()
    #     self.dump_file.close()


if  __name__ == '__main__':
    node_id = int(input("Enter the node id: "))
    port = int(input("Enter the port number: "))
    node_ips = {1:'localhost:50051', 2:'localhost:50052', 3:'localhost:50053'}

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_node = RaftNodeImplementation(node_id, port, node_ips)
    node_pb2_grpc.add_RaftServiceServicer_to_server(raft_node, server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()

    if raft_node.currRole == "Follower" and raft_node.currLeader is not None:
        raft_node.updateLogs()
    while True:
        time.sleep(5)
        print(f"Node {node_id} is {raft_node.currRole} for term {raft_node.currTerm}.")
        print("Logs: ")
        for i in raft_node.log:
            print(i)
        print("Data: ")
        for(i, j) in raft_node.data.items():
            print(f"Key: {i}, Value: {j}")
        print(f"Current Lease Duration: {raft_node.lease_duration} seconds.")

