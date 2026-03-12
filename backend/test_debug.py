from rule_engine.stage2_engine import Stage2RuleEngine
from data_sources.mock_data import MockDataSource

mock_data = MockDataSource()
campaigns = mock_data.get_campaigns()
engine = Stage2RuleEngine()

for c in campaigns[:3]:
    print(f'Checking {c.name}...')
    try:
        results = engine.run_stage2_check(c, mock_data)
        print(f'  Found {len(results)} results')
    except Exception as e:
        print(f'  Error: {e}')
        import traceback
        traceback.print_exc()
print('Done')
