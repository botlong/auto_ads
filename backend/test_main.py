import json
from main import run_stage2_diagnosis
from models.schemas import DiagnosisRequest

try:
    req = DiagnosisRequest(campaign_ids=['c_001', 'c_002'], days=7)
    result = run_stage2_diagnosis(req)
    print('Success!')
    print(json.dumps(result, indent=2, default=str)[:500])
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
