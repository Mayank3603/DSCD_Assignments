import grpc
from concurrent import futures
import node_pb2 as node
import node_pb2_grpc
import os
import time

class RaftNodeImplementation(node_pb2_grpc.RaftServiceServicer):
    def __init__(self, node_id, port, node_ips):
        print("Initializing RaftNodeImplementation object...")
        self.node_id = node_id
        self.currTerm = 0
        self.currRole = "Follower"  
        self.votedFor = None
        self.commitLength = 0
        self.currLeader = None
        self.votesReceived = set()
        self.election_timer = node_id * 4  
        self.ip = "localhost"
        self.port = port
        self.node_ips = node_ips
        self.log_file = f"log_node_{node_id}.txt"
        self.init_files()
        print(f"Election timer for node {node_id} is {self.election_timer} seconds.")
        self.start_election_timer()

    def init_files(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as log_file:
                pass
        if not os.path.exists(self.meta_file):
            with open(self.meta_file, "w") as meta_file:
                meta_file.write(f"node_id: {self.node_id}\n")
                meta_file.write(f"currTerm: {self.currTerm}\n")
                meta_file.write(f"votedFor: {self.votedFor}\n")
                meta_file.write(f"commitLength: {self.commitLength}\n")

    def log_to_dump(self, text):
        with open(self.dump_file, "a") as dump_file:
            dump_file.write(text + "\n")

    def print_and_log(self, text):
        print(text)
        self.log_to_dump(text)

    def recover(self):
        self.init_files()
        with open(self.meta_file, "r") as meta_file:
            lines = meta_file.readlines()
            self.node_id = int(lines[0].split(":")[1].strip())
            self.currTerm = int(lines[1].split(":")[1].strip())
            self.votedFor = int(lines[2].split(":")[1].strip())
            self.commitLength = int(lines[3].split(":")[1].strip())

    def start_election_timer(self):
        while self.election_timer > 0:
            time.sleep(1)
            self.election_timer -= 1
            if self.election_timer <= 0:
                self.start_election()
                break

    
    def cancel_election_timer(self):
        self.election_timer = 0

    def check_votes(self):

        if len(self.votesReceived) >= (len(self.node_ips) + 1) // 2:
            self.currRole = "Leader"
            self.currLeader = self.node_id
            print(f"Node {self.node_id} became the leader for term {self.currTerm}.")
        else:
            print(f"Node {self.node_id} did not receive majority votes yet.")

    def start_election(self):
        self.currTerm += 1
        self.currRole = "Candidate"
        self.votedFor = self.node_id
        self.votesReceived = {self.node_id}  
        print(f"Node {self.node_id} started an election for term {self.currTerm}.")
        self.check_votes()

    # def start_election(self):
    #     self.currTerm += 1
    #     self.currRole = "Candidate"
    #     self.votedFor = self.node_id
    #     self.votesReceived = {self.node_id}
    #     lastTerm = 0
    #     if len(self.log) > 0:
    #         lastTerm = self.log[-1].term
    #     msg = (VoteRequest, self.node_id, self.currTerm, len(self.log), lastTerm)
    #     for node in nodes:
    #         send_msg(msg, node)
    #     self.start_election_timer()
    #     print(f"Node {self.node_id} started an election for term {self.currTerm}.")
    #     self.log_to_dump(f"Election started for term {self.currTerm}.")


    def handle_vote_response(self, response):
        if self.currRole == "Candidate" and response.term == self.currTerm and response.voteGranted:
            self.votesReceived.add(response.voterId)
            print(f"Received vote from {response.voterId}. Total votes: {len(self.votesReceived)}")
            self.check_votes()
        elif response.term > self.currTerm:
            self.currTerm = response.term
            self.currRole = "Follower"
            self.votedFor = None

        # def handle_vote_response(self, response):
        #     if self.currRole == "Candidate" and response.term == self.currTerm and response.voteGranted:
        #     self.votesReceived.add(response.voterId)
        #     print(f"Node {self.node_id} received vote from {response.voterId}. Total votes: {len(self.votesReceived)}")
        #     self.log_to_dump(f"Received vote from {response.voterId}. Total votes: {len(self.votesReceived)}")
        #     if len(self.votesReceived) >= (len(nodes) + 1) // 2:
        #         self.currRole = "Leader"
        #         self.currLeader = self.nodeId
        #         self.cancel_election_timer()
        #         print(f"Node {self.node_id} became the leader for term {self.currTerm}.")
        #         self.log_to_dump(f"Became leader for term {self.currTerm}.")
        #         for follower in nodes - {self.nodeId}:
        #             self.sentLength[follower] = len(self.log)
        #             self.ackedLength[follower] = 0
        #             replicate_log(self.nodeId, follower)
        # elif response.term > self.currTerm:
        #     self.currTerm = response.term
        #     self.currRole = "Follower"
        #     self.votedFor = None
        #     self.cancel_election_timer()
        #     print(f"Node {self.node_id} stepped down to follower due to higher term: {self.currTerm}.")
        #     self.log_to_dump(f"Stepped down to follower due to higher term: {self.currTerm}.")


    def handle_suspected_leader_failure(self):
        self.start_election()

    def handle_request_vote(self, request):
        if request.term > self.currTerm:
            self.currTerm = request.term
            self.votedFor = None
            self.currRole = "Follower"
            self.currLeader = None
        if request.term < self.currTerm:
            return node.VoteResponse(term=self.currTerm, voteGranted=False)
        if self.votedFor is None or self.votedFor == request.candidateId:
            self.votedFor = request.candidateId
            return node.VoteResponse(term=self.currTerm, voteGranted=True)
        return node.VoteResponse(term=self.currTerm, voteGranted=False)
   
    def handle_append_entries(self, request):
        if request.term > self.currTerm:
            self.start_election_timer()
            self.votedFor = None
            self.currRole = "Follower"
            self.currLeader = request.leaderId
        if request.term < self.currTerm:
            return node.AppendEntryResponse(term=self.currTerm, success=False)
        if request.prevLogIndex > len(self.log) or request.prevLogTerm != self.log[request.prevLogIndex]:
            return node.AppendEntryResponse(term=self.currTerm, success=False)
        if request.leaderCommit > self.commitLength:
            self.commitLength = min(request.leaderCommit, len(self.log))
        self.log[request.prevLogIndex + 1:] = request.entries
        return node.AppendEntryResponse(term=self.currTerm, success=True)

    # def handle_vote_response(self, response):
    #     if self.currRole == "Candidate" and response.term == self.currTerm and response.voteGranted:
    #         self.votesReceived.add(response.voterId)
    #         if len(self.votesReceived) >= (len(nodes) + 1) // 2:
    #             self.currRole = "Leader"
    #             self.currLeader = self.nodeId
    #             cancel_election_timer()
    #             for follower in nodes - {self.nodeId}:
    #                 self.sentLength[follower] = len(self.log)
    #                 self.ackedLength[follower] = 0
    #                 replicate_log(self.nodeId, follower)
    #     elif response.term > self.currTerm:
    #         self.currTerm = response.term
    #         self.currRole = "Follower"
    #         self.votedFor = None
    #         cancel_election_timer()

    def broadcast_msg_request(self, msg):
        if self.currRole == "Leader":
            log_entry = {'msg': msg, 'term': self.currTerm}
            with open(self.log_file, "a") as log_file:
                log_file.write(str(log_entry) + '\n')
            self.ackedLength[self.node_id] = len(self.log)
            for follower in nodes - {self.node_id}:
                replicate_log(self.node_id, follower)
        else:
            forward_request_to_leader(msg, self.currLeader)

    def periodically_replicate_logs(self):
        if self.currRole == "Leader":
            for follower in nodes - {self.nodeId}:
                replicate_log(self.nodeId, follower)

    def handle_log_request(self, request):
        if request.term > self.currTerm:
            self.currTerm = request.term
            self.votedFor = None
            cancel_election_timer()
        if request.term == self.currTerm:
            self.currRole = "Follower"
            self.currLeader = request.leaderId
        logOk = (len(self.log) >= request.prefixLen) and \
                 (request.prefixLen == 0 or self.log[request.prefixLen - 1].term == request.prefixTerm)
        if request.term == self.currTerm and logOk:
            self.append_entries(request.prefixLen, request.leaderCommit, request.suffix)
            ack = request.prefixLen + len(request.suffix)
            send_msg((LogResponse, self.nodeId, self.currTerm, ack, True), request.leaderId)
        else:
            send_msg((LogResponse, self.nodeId, self.currTerm, 0, False), request.leaderId)

    def append_entries(self, prefix_len, leader_commit, suffix):
        if len(suffix) > 0 and len(self.log) > prefix_len:
            index = min(len(self.log), prefix_len + len(suffix)) - 1
            if self.log[index].term != suffix[index - prefix_len].term:
                self.log = self.log[:prefix_len] + self.log[prefix_len:]
        if prefix_len + len(suffix) > len(self.log):
            for i in range(len(self.log) - prefix_len, len(suffix)):
                self.log.append(suffix[i])
        if leader_commit > self.commitLength:
            for i in range(self.commitLength, leader_commit):
                deliver(self.log[i].msg)
            self.commitLength = leader_commit

    def handle_log_response(self, response, follower):
        if response.term == self.currTerm and self.currRole == "Leader":
            if response.success and response.ack >= self.ackedLength[follower]:
                self.sentLength[follower] = response.ack
                self.ackedLength[follower] = response.ack
                self.commit_log_entries()
            elif self.sentLength[follower] > 0:
                self.sentLength[follower] -= 1
                replicate_log(self.nodeId, follower)
        elif response.term > self.currTerm:
            self.currTerm = response.term
            self.currRole = "Follower"
            self.votedFor = None
            cancel_election_timer()

    def commit_log_entries(self):
        min_acks = (len(nodes) + 1) // 2
        ready = [length for length in range(1, len(self.log) + 1) if self.acks(length) >= min_acks]
        if ready and max(ready) > self.commitLength and self.log[max(ready) - 1].term == self.currTerm:
            for i in range(self.commitLength, max(ready)):
                deliver(self.log[i].msg)
            self.commitLength = max(ready)

    def get(self, key):
        if(key in self.data):
            return self.data[key]

    def ServeGet(self, request, context):
        key = request.key
        value = self.get(key)
        return node.GetReply(value=value)

    def ServeSet(self, request, context):
        key = request.key
        value = request.value
        self.set(key, value)
        return node.SetReply(Success="True")

    def set(self, key, value):
        self.data[key] = value


    # def acks(self, length):
    #     pass


if __name__ == '__main__':
    node_id = int(input("Enter the node id: "))  
    port = int(input("Enter the port number: "))  
    node_ips = ['localhost:50051','localhost:50052']  

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_node = RaftNodeImplementation(node_id, port, node_ips)
    print(f"Node {node_id} server created.")
    node_pb2_grpc.add_RaftServiceServicer_to_server(raft_node, server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Raft Node Server started on port {port}")

    while True:
        print(f"Node {node_id} - Role: {raft_node.currRole}, Term: {raft_node.currTerm}")
        time.sleep(5)
