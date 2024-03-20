import grpc
from concurrent import futures
import node_pb2 as node
import node_pb2_grpc
import random

class RaftNodeImplementation(node_pb2_grpc.RaftServiceServicer):
    def __init__(self,node_id):
        self.node_id = node_id
        self.currTerm=0
        self.timer=random.randint(150,300)
        self.votedFor=None
        self.currRole="Follower"
        self.votesRecv=0
        self.commitLength=0
        self.currLeader=None
        self.logFile = open(f"log_{node_id}.txt", "w")
        self.metaFile = open(f"meta_{node_id}.txt", "w")
    
    def RequestVotes(self, request, context):
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


    def AppendEntries(self, request, context):
        if request.term > self.currTerm:
            self.currTerm = request.term
            self.votedFor = None
            self.currRole = "Follower"
            self.currLeader = request.leaderId
        if request.term < self.currTerm:
            return node.AppendEntryResponse(term=self.currTerm, success=False)
        if request.prevLogIndex > len(self.log) or request.prevLogTerm != self.log[request.prevLogIndex]:
            return node.AppendEntryResponse(term=self.currTerm, success=False)
        if request.leaderCommit > self.commitLength:
            self.commitLength = min(request.leaderCommit, len(self.log))
        self.log[request.prevLogIndex+1:] = request.entries
        return node.AppendEntryResponse(term=self.currTerm, success=True)

    def Recovery(self, request, context):
        return node.RecoveryResponse(term=self.currTerm, success=True, log=self.log, commitLength=self.commitLength, votedFor=self.votedFor, currRole=self.currRole, currLeader=self.currLeader)

    def handleRequestVote(self, request):
        response = self.RequestVotes(request)
        return response

    def handleAppendEntries(self, request):
        response = self.AppendEntries(request)
        return response

    def handleRecovery(self, request):
        response = self.Recovery(request)
        return response

    

def main():
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # node_service=RaftNodeImplementation()
    # node_pb2_grpc.add_RaftNodeServicer_to_server(node_service, server)
    # server.add_insecure_port('[::]:50051')
    # server.start()
    # print("Raft Node Server started on port 50051")
    # server.wait_for_termination()
    
    node=RaftNodeImplementation(1)
    node.recover()


