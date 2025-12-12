import unittest
from aiodatacube.datacubeclient import DataCubeClient
from aiodatacube.stub.datacube_p2p import *
import random
from datetime import timedelta
from dateutil.parser import parse as parse_datetime

class TestDataCubeClient(unittest.TestCase):

    def setUp(self):
        self.host_port = "localhost:6565"
        self.collect_name = "unittest"
        self.ts1 = parse_datetime("2025-01-03 12:34:45.56")
        self.ts2 = parse_datetime("2025-12-23 14:13:33.23")

    def test_ping(self):
        with DataCubeClient(self.host_port) as client:
            res = client.ping()
            self.assertEqual("OK", res["message"])


    def test_collection_create_delete(self):
        with DataCubeClient(self.host_port) as client:
            res = client.list_collection()
            if self.collect_name in res:
                client.delete_collection(self.collect_name)

            res = client.create_collection(self.collect_name)
            self.assertTrue(res["ack"])
            res = client.list_collection()
            self.assertTrue(isinstance(res, list))
            self.assertTrue(self.collect_name in res)
            res = client.delete_collection(self.collect_name)
            self.assertTrue(res["ack"])
            res = client.list_collection()
            self.assertFalse(self.collect_name in res)



    def test_save_delete_records(self):
        with DataCubeClient(self.host_port) as client:
            res = client.list_collection()
            if self.collect_name in res:
                client.delete_collection(self.collect_name)
            client.create_collection(self.collect_name)
            ts1 = parse_datetime("2025-12-03 12:34:45.56")
            ts2 = parse_datetime("2025-12-03 14:13:33.23")
            records = [MeasureByKey(key="c1", ts=int(ts1.timestamp()), value=10.0),
                       MeasureByKey(key="c2", ts=int(ts1.timestamp()), value=20.0),
                       MeasureByKey(key="c3", ts=int(ts1.timestamp()), value=30.0),
                       MeasureByKey(key="c1", ts=int(ts1.timestamp()), value=15.0),
                       MeasureByKey(key="c1", ts=int(ts2.timestamp()), value=45.0)
            ]
            req = SaveRequest(cf=self.collect_name, records=records)
            client.save(req)
            req = QueryKeysRequest(cf=self.collect_name, prefix="c")
            res = client.query_keys(req)
            self.assertEqual(4, len(res.keys))
            self.assertEqual(4, len(set(res.keys)))
            self.assertTrue(res.keys[0].startswith("c1/"))
            self.assertTrue(res.keys[1].startswith("c1/"))
            self.assertTrue(res.keys[2].startswith("c2/"))
            self.assertTrue(res.keys[3].startswith("c3/"))

            req = QueryRequest(cf=self.collect_name, keys=["c1", "c10"])
            res = client.query(req)
            self.assertEqual(1, len(res.stats))
            stat = res.stats[0]
            assert isinstance(stat, MeasureStats)
            self.assertEqual("c1", stat.key)
            self.assertEqual(3, stat.count)
            self.assertEqual(70, stat.sum)

            req = QueryRequest(cf=self.collect_name, keys=["c1", "c10"], end_ts=int(ts2.timestamp())-1)
            res = client.query(req)
            self.assertEqual(1, len(res.stats))
            stat = res.stats[0]
            assert isinstance(stat, MeasureStats)
            self.assertEqual("c1", stat.key)
            self.assertEqual(2, stat.count)
            self.assertEqual(25, stat.sum)

            req = QueryRequest(cf=self.collect_name, keys=["c1", "c10"], start_ts=int(ts1.timestamp()),
                               end_ts=int(ts2.timestamp()) - 1)
            res = client.query(req)
            self.assertEqual(1, len(res.stats))
            stat = res.stats[0]
            assert isinstance(stat, MeasureStats)
            self.assertEqual("c1", stat.key)
            self.assertEqual(2, stat.count)
            self.assertEqual(25, stat.sum)

            req = QueryRequest(cf=self.collect_name, keys=["c1", "c10"], start_ts=int(ts1.timestamp())+1,
                               end_ts=int(ts2.timestamp()) - 1)
            res = client.query(req)
            self.assertEqual(0, len(res.stats))

            # test freq
            req = QueryRequest(cf=self.collect_name, keys=["c1", "c10"], as_freq="1H")
            res = client.query(req)
            self.assertEqual(2, len(res.stats))
            stat = res.stats[0]
            assert isinstance(stat, MeasureStats)
            self.assertEqual("c1", stat.key)
            self.assertEqual(2, stat.count)
            self.assertEqual(25, stat.sum)

            stat = res.stats[1]
            assert isinstance(stat, MeasureStats)
            self.assertEqual("c1", stat.key)
            self.assertEqual(1, stat.count)
            self.assertEqual(45, stat.sum)


    def test_scan(self):
        input_records = self.build_transaction_network()
        with DataCubeClient(self.host_port) as client:
            req = ScanRequest(cf=self.collect_name, prefix="c", size=2)
            total_count = 0
            for res in client.scan(req):
                self.assertIsNotNone(res)
                total_count += len(res.batch)
            self.assertEqual(len(input_records), total_count)

    def random_ts(self):
        ts1 = self.ts1
        ts2 = self.ts2
        time_diff = ts2 - ts1
        total_seconds = int(time_diff.total_seconds())
        random_seconds = random.randrange(total_seconds)
        return int((ts1 + timedelta(seconds=random_seconds)).timestamp())

    def build_transaction_network(self):
        with DataCubeClient(self.host_port) as client:
            res = client.list_collection()
            if self.collect_name in res:
                client.delete_collection(self.collect_name)
            client.create_collection(self.collect_name)
            random_ts = self.random_ts

            records = [MeasureByKey(key="c1:c2", ts=random_ts(), value=10.0),
                       MeasureByKey(key="c1:c3", ts=random_ts(), value=20.0),
                       MeasureByKey(key="c1:c4", ts=random_ts(), value=30.0),
                       MeasureByKey(key="c2:c5", ts=random_ts(), value=15.0),
                       MeasureByKey(key="c5:c1", ts=random_ts(), value=15.0),
                       MeasureByKey(key="c5:c6", ts=random_ts(), value=15.0),

                       MeasureByKey(key="c1:c9", ts=random_ts(), value=15.0),
                       MeasureByKey(key="c9:c12", ts=random_ts(), value=15.0),
                       MeasureByKey(key="c12:c1", ts=random_ts(), value=15.0),

                       MeasureByKey(key="c1:c6", ts=random_ts(), value=15.0),

            ]
            req = SaveRequest(cf=self.collect_name, records=records)
            client.save(req)
            return records


    def test_triangle(self):
        input_records = self.build_transaction_network()
        with DataCubeClient(self.host_port) as client:
            req = FindTrianglesRequest(cf=self.collect_name, src="c1", max_depth=10, separator=":")
            res = client.find_triangles(req)
            self.assertIsNotNone(res)
            self.assertEqual(2, len(res.triangles))
            path1 = res.triangles[0].ids
            path2 = res.triangles[1].ids
            self.assertListEqual(["c1", "c9", "c12"], path1)
            self.assertListEqual(["c1", "c2", "c5"], path2)

    def test_paths_finding(self):
        input_records = self.build_transaction_network()
        with DataCubeClient(self.host_port) as client:
            req = FindPathsRequest(cf=self.collect_name, src="c1", dst="c6", max_depth=10, separator=":")
            res = client.find_paths(req)
            self.assertIsNotNone(res)
            self.assertEqual(2, len(res.paths))
            path1 = res.paths[0].ids
            path2 = res.paths[1].ids
            self.assertListEqual(["c1", "c6"], path1)
            self.assertListEqual(["c1", "c6", "c2", "c5", "c6"], path2)

    @staticmethod
    def min_max_ts(records):
        min_ts = min([r.ts for r in records])
        max_ts = max([r.ts for r in records])
        return min_ts, max_ts

    def test_networks(self):
        input_records = self.build_transaction_network()
        min_ts, max_ts = self.min_max_ts(input_records)
        start_ts = int(self.ts1.timestamp())
        end_ts = int(self.ts2.timestamp())
        with DataCubeClient(self.host_port) as client:
            req = NetworkRequest(cf=self.collect_name, src_ids = ["c1"], max_depth=3, separator=":", start_ts=start_ts, end_ts=end_ts)
            res = client.find_networks(req)
            self.assertIsNotNone(res)
            items = res.items
            self.assertTrue(len(items)>0)
