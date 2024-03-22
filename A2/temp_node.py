import grpc
from concurrent import futures
import node_pb2 as node
import node_pb2_grpc
import os
import time
import math
import threading

class RaftNodeImplementation(node_pb2_grpc.RaftServiceServicer):
    def __init__(self, node_id, port, node_ips):
        print("Initializing RaftNodeImplementation object...")
        self.node_id = node_id
        self.currTerm = 0
        self.votedFor = None
        self.log = [{}]  
        self.commitLength = 0
        self.currRole = "Follower"  
        self.currLeader = None
        self.votesReceived = set()
        self.sentLength = {}
        self.ackedLength = {}
        self.election_timer = node_id * 4  
        self.heartbeat_interval = 1 
        self.ip = "localhost"
        self.port = port
        self.node_ip = f"localhost:{port}"
        self.node_ips = node_ips
        print(f"Election timer for node {node_id} is {self.election_timer} seconds.")
        

        self.election_timer_thread = threading.Thread(target=self.run_election_timer)
        self.election_timer_thread.daemon = True
        self.election_timer_thread.start()

        self.heartbeat_thread = None
        if self.node_id == min(self.node_ips.values()): 
            self.start_heartbeat_thread()

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
        # if self.node_id == 2:
        #     return
        self.currTerm += 1
        self.currRole = "Candidate"
        self.votedFor = self.node_id
        self.votesReceived.add(self.node_id)
        self.lastTerm = self.log[-1].get('term', 0) if len(self.log) > 0 else 0

        for i in self.node_ips:
            if i != self.node_ip:
                print(f"Node {self.node_id} sending RequestVote RPC to Node {i}.")
                try:
                    channel = grpc.insecure_channel(i)
                    stub = node_pb2_grpc.RaftServiceStub(channel)
                    request = node.RequestVoteRequest(term=self.currTerm, candidate_id=self.node_id, last_log_index=len(self.log) - 1, last_log_term=self.lastTerm)
                    response = stub.RequestVote(request)
                    print(f"Node {self.node_id} received RequestVoteResponse RPC from Node {i}.")
                    if response.vote_granted:
                        self.votesReceived.add(i)
                except Exception as e:
                    print(f"Node {self.node_id} failed to send or receive RequestVote RPC to/from Node {i}. Error: {e}")
                    continue

        self.check_votes()
        self.election_timer = self.node_id * 4
        self.start_election_timer()

    def check_votes(self):
        if len(self.votesReceived) > (len(self.node_ips) + 1) // 2:
            self.become_leader()
        else:
            print(f"Node {self.node_id} did not receive majority votes yet.")

    def RequestVote(self, request, context):
        print(f"Node {self.node_id} received RequestVote RPC from Node {request.candidate_id} for term {request.term}.")
        if request.term > self.currTerm:
            self.transition_to_follower(request.term)

        lastTerm = self.log[-1].get('term', 0) if len(self.log) > 0 else 0
        logOk = (request.last_log_term > lastTerm) or \
                 (request.last_log_term == lastTerm and request.last_log_index >= len(self.log) - 1)

        if request.term == self.currTerm and logOk and self.votedFor in {request.candidate_id, None}:
            self.votedFor = request.candidate_id
            print(f"Node {self.node_id} voted for Node {request.candidate_id} for term {request.term}.")
            return node.RequestVoteResponse(term=self.currTerm, vote_granted=True)
        else: 
            print(f"Node {self.node_id} did not vote for Node {request.candidate_id} for term {request.term}.")
            return node.RequestVoteResponse(term=self.currTerm, vote_granted=False)

    def start_election_timer(self): 
        print("################")
        while self.election_timer > 0:
            time.sleep(1)
            self.election_timer -= 1
        if self.currRole == "Follower":
            self.start_election()
        elif self.currRole == "Candidate":
            self.start_election()

    def send_heartbeats(self):
        for follower, _ in self.node_ips.items(): 
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
                            leader_commit=self.commitLength
                        )
                    response = stub.AppendEntries(request)
                    print(f"Node {self.node_id} received heartbeat response from Node {follower}.")
                    if response.success == "True":
                        self.ackedLength[follower] = self.sentLength[follower]
                except Exception as e:
                    print(f"Node {self.node_id} failed to send or receive heartbeat to/from Node {follower}. Error: {e}")
                    continue
        self.election_timer = node_id * 4

    def AppendEntries(self, request, context):
        print(f"Node {self.node_id} received AppendEntries RPC from Node {request.leader_id}.")
        response = node.AppendEntriesResponse(currTerm=self.currTerm, success="False")

        if request.term >= self.currTerm:
            self.transition_to_follower(request.term)
            response.currTerm = self.currTerm
            response.success = "True"
            self.ackedLength[request.leader_id] = len(self.log)
            if len(request.entries) > 0:
                self.log = self.log[:request.prev_log_index + 1] + request.entries
            if request.leader_commit > self.commitLength:
                self.commitLength = min(request.leader_commit, len(self.log) - 1)
        self.election_timer = node_id * 4
        return response

    def become_leader(self):
        self.currRole = "Leader"
        self.currLeader = self.node_id
        print(f"Node {self.node_id} became Leader for term {self.currTerm}.")
        self.start_heartbeat_thread() 
        for follower in self.node_ips.keys():
            if follower != self.node_ip:
                self.sentLength[follower] = len(self.log)
                self.ackedLength[follower] = 0
                self.replicate_log(self.node_id, follower)

    def transition_to_follower(self, term):
        self.currTerm = term
        self.currRole = "Follower"
        self.votedFor = None

    def replicate_log(self, leader_id, follower_id):
        print(f"Node {self.node_id} sending AppendEntries RPC to Node {follower_id}.")
        try:
            channel = grpc.insecure_channel(follower_id)
            stub = node_pb2_grpc.RaftServiceStub(channel)
            prev_log_index = self.sentLength.get(follower_id, 0) - 1
            prev_log_term = self.log[prev_log_index]['term'] if prev_log_index >= 0 else 0 
            entries_to_send = self.log[prev_log_index + 1:] 
            request = node.AppendEntriesRequest(
                term=self.currTerm,
                leader_id=leader_id,
                prev_log_index=prev_log_index,
                prev_log_term=prev_log_term,
                entries=entries_to_send,
                leader_commit=self.commitLength
            )
            response = stub.AppendEntries(request)
            print(f"Node {self.node_id} received AppendEntriesResponse RPC from Node {follower_id}.")
            if response.success=="True":
                self.sentLength[follower_id] += len(entries_to_send)
                self.ackedLength[follower_id] = self.sentLength[follower_id]
        except Exception as e:
            print(f"Node {self.node_id} failed to send or receive AppendEntries RPC to/from Node {follower_id}. Error: {e}")
            return

if __name__ == '__main__':
    node_id = int(input("Enter the node id: "))  
    port = int(input("Enter the port number: "))  
    node_ips = {'localhost:50051': 0, 'localhost:50052': 1} 

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

