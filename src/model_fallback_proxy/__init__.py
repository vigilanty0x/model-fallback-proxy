import argparse,hashlib,json
def route(data):
 models=data.get("models") if isinstance(data,dict) else None;request=data.get("request",{}) if isinstance(data,dict) else {}
 if not isinstance(models,list) or len(models)>100:return {"ok":False,"decision":"blocked","errors":["invalid_models"]}
 need=set(request.get("capabilities",[]));tokens=request.get("context_tokens",0)
 if not isinstance(tokens,int) or tokens<0:return {"ok":False,"decision":"blocked","errors":["invalid_context"]}
 attempts=[];selected=None
 for m in sorted(models,key=lambda x:(int(x.get("order",999)),str(x.get("name")))):
  reasons=[]
  if m.get("status")!="healthy":reasons.append("unhealthy")
  if int(m.get("remaining_requests",0))<=0:reasons.append("quota")
  if int(m.get("context_limit",0))<tokens:reasons.append("context")
  if not need<=set(m.get("capabilities",[])):reasons.append("capability")
  attempts.append({"model":m.get("name"),"eligible":not reasons,"reasons":reasons})
  if not reasons and selected is None:selected=m.get("name")
 body={"selected":selected,"attempts":attempts};return {"ok":selected is not None,"decision":"ready" if selected else "blocked",**body,"route_sha256":hashlib.sha256(json.dumps(body,sort_keys=True,separators=(",",":")).encode()).hexdigest()}
def probe():
 g=route({"request":{"context_tokens":1,"capabilities":["text"]},"models":[{"name":"m","order":1,"status":"healthy","remaining_requests":1,"context_limit":10,"capabilities":["text"]}]});b=route({"request":{"context_tokens":1},"models":[]});return {"ok":g["ok"] and not b["ok"],"no_route_counter_proof":not b["ok"]}
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("command",choices=("route","probe"));p.add_argument("--input");a=p.parse_args(argv);o=probe() if a.command=="probe" else route(json.load(open(a.input)));print(json.dumps(o,sort_keys=True));return 0 if o["ok"] else 2
