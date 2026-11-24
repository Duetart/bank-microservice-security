import json, sys, pathlib
if len(sys.argv)!=3: raise SystemExit('Usage: add_idor.py raw.json enriched.json')
src,dst=map(pathlib.Path,sys.argv[1:])
if src.resolve()==dst.resolve(): raise SystemExit('Keep original Semgrep output unchanged')
report=json.loads(src.read_text(encoding='utf-8'))
if not isinstance(report.get('results'),list) or 'version' not in report: raise SystemExit('Expected native Semgrep JSON')
if report.get('errors'): print('WARNING: inspect scanner errors before submission',file=sys.stderr)
report['results'].append({'check_id':'manual.bank.idor-bola','path':'app/crud.py','start':{'line':43,'col':1},'end':{'line':66,'col':46},'extra':{'message':'IDOR/BOLA: идентификатор владельца для истории и проверки исходного счёта определяется через недоверенный X-User-Id. Связанные места: app/security.py:3–13, app/main.py:13–24, app/crud.py:5–16. Условие: корректное связывание импортов API.','severity':'ERROR','metadata':{'source':'manual_review','cwe':['CWE-639'],'related':['CWE-306'],'status':'conditional_static','runtime_tested':False,'recommendation':'Проверенный subject токена и объектная авторизация; межпользовательские тесты.'}}})
dst.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
