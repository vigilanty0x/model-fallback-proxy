import unittest
from model_fallback_proxy import route,probe
M={"name":"m","order":1,"status":"healthy","remaining_requests":1,"context_limit":10,"capabilities":["text"]}
class T(unittest.TestCase):
 def test_route(self):self.assertEqual(route({"request":{"context_tokens":1,"capabilities":["text"]},"models":[M]})["selected"],"m")
 def test_unhealthy(self):self.assertFalse(route({"request":{"context_tokens":1},"models":[{**M,"status":"down"}]})["ok"])
 def test_context(self):self.assertFalse(route({"request":{"context_tokens":11},"models":[M]})["ok"])
 def test_probe(self):self.assertTrue(probe()["ok"])
if __name__=="__main__":unittest.main()
