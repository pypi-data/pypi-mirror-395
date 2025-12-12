from aiodatacube.stub import datacube_pb2
from aiodatacube.stub.datacube_pb2_grpc import DataCubeServiceStub
import grpc
from aiodatacube.stub.datacube_p2p import *
from google.protobuf.json_format import ParseDict, MessageToDict


class DataCubeClient:

    def __init__(self, host_port:str):
        self.channel = grpc.insecure_channel(host_port)

    @property
    def stub(self):
        return DataCubeServiceStub(self.channel)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.channel.close()

    def ping(self):
        req = datacube_pb2.PingRequest()
        res = self.stub.ping(req)
        return {"message": res.message, "version": res.version}

    def create_collection(self, cf:str):
        req = datacube_pb2.CreateCollectionRequest(cf = cf)
        res = self.stub.create_collection(req)
        return {"ack": res.ack}

    def delete_collection(self, cf:str):
        req = datacube_pb2.DeleteCollectionRequest(cf = cf)
        res = self.stub.delete_collection(req)
        return {"ack": res.ack}

    def list_collection(self):
        req = datacube_pb2.ListCollectionsRequest()
        res = self.stub.list_collections(req)
        return list(res.cfs)

    def save(self, request: SaveRequest):
        req_dict = request.model_dump()
        req_proto  = ParseDict(req_dict, datacube_pb2.SaveRequest())
        res = self.stub.save(req_proto)
        return {"ack": res.ack}

    def query(self, request: QueryRequest):
        req_dict = request.model_dump()
        req_proto  = ParseDict(req_dict, datacube_pb2.QueryRequest())
        res_proto = self.stub.query(req_proto)
        res_dict = MessageToDict(res_proto)
        return QueryResponse(**res_dict)

    def query_keys(self, request: QueryKeysRequest):
        req_dict = request.model_dump()
        req_proto  = ParseDict(req_dict, datacube_pb2.QueryKeysRequest())
        res_proto = self.stub.query_keys(req_proto)
        res_dict = MessageToDict(res_proto)
        return QueryKeysResponse(**res_dict)

    def scan(self, request: ScanRequest):
        if request.size == 0:
            request.size = 100
        req_dict = request.model_dump()
        req_proto  = ParseDict(req_dict, datacube_pb2.ScanRequest())
        try:
            for res_proto in self.stub.scan(req_proto):
                res_dict = MessageToDict(res_proto)
                yield ScanResponse(**res_dict)
        except grpc.RpcError as e:
            raise e

    def find_triangles(self, request: FindTrianglesRequest):
        req_dict = request.model_dump()
        req_proto = ParseDict(req_dict, datacube_pb2.FindTrianglesRequest())
        res_proto = self.stub.find_triangles(req_proto)
        res_dict = MessageToDict(res_proto)
        return FindTrianglesResponse(**res_dict)

    def find_paths(self, request: FindPathsRequest):
        req_dict = request.model_dump()
        req_proto = ParseDict(req_dict, datacube_pb2.FindPathsRequest())
        res_proto = self.stub.find_paths(req_proto)
        res_dict = MessageToDict(res_proto)
        return FindPathsResponse(**res_dict)

    def find_networks(self, request: NetworkRequest):
        req_dict = request.model_dump()
        req_proto = ParseDict(req_dict, datacube_pb2.NetworkRequest())
        res_proto = self.stub.find_networks(req_proto)
        res_dict = MessageToDict(res_proto)
        return NetworkResponse(**res_dict)

    def build_adjacency_list(self, request: BuildAdjacencyListRequest):
        req_dict = request.model_dump()
        req_proto = ParseDict(req_dict, datacube_pb2.BuildAdjacencyListRequest())
        res_proto = self.stub.build_adjacency_list(req_proto)
        res_dict = MessageToDict(res_proto)
        return BuildAdjacencyListResponse(**res_dict)