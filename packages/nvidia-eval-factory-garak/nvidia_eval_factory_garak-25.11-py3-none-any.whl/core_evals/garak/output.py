import os
import json
from pathlib import Path
from collections import defaultdict
from nemo_evaluator.api.api_dataclasses import EvaluationResult


def _parse_jsonl_report(jsonl_path: str) -> dict:
    """Parse garak JSONL report to extract key information."""
    results = {}
    garak_version = None
    model_name = None
    
    with open(jsonl_path, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get('entry_type') == 'init':
                    garak_version = entry.get('garak_version')
                elif entry.get('entry_type') == 'start_run setup':
                    model_name = entry.get('plugins.model_name')
                elif entry.get('entry_type') == 'eval':
                    probe_name = entry['probe']
                    pass_rate = entry.get('passed', 0) / entry.get('total', 0)
                    total_samples = entry.get('total', 0)
                    results[probe_name] = {'pass_rate': pass_rate, 'total_samples': total_samples}
            except json.JSONDecodeError:
                continue
    
    return {
        'model_name': model_name,
        'version': garak_version,
        'results': results
    }

def parse_output(output_dir: str) -> EvaluationResult:
    jsonl_path = Path(output_dir) / "garak" / "garak_runs" / "results.report.jsonl"
    
    if jsonl_path.exists():
        report_data = _parse_jsonl_report(jsonl_path)
        
        tasks = {}
        for probe_name, probe_data in report_data['results'].items():
            tasks[probe_name] = dict(
                metrics={
                    "pass_rate": dict(
                        scores={
                            'pass_rate': dict(
                                value=probe_data['pass_rate'],
                                stats={'count': probe_data['total_samples']}
                            )
                        }
                    )
                }
            )
        
        return EvaluationResult(tasks=tasks, groups=tasks)
    else:
        raise FileNotFoundError(f"No garak report file found at {jsonl_path}")
