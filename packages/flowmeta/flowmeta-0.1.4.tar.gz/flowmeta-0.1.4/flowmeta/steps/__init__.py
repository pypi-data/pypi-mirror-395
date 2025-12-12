"""Step modules for flowmeta pipeline"""

from .step1_qc import run_fastp_qc, check_fastp_results
from .step2_remove_host import run_remove_host, check_host_remove_results
from .step3_extract_host import run_extract_host
from .step4_kraken_bracken import run_kraken_bracken, check_kraken_results
from .step5_remove_host_counts import run_remove_host_counts

try:
    from .step6_merge_results import run_merge_step
except ModuleNotFoundError as exc:  # typically missing pandas
    run_merge_step = None
    STEP6_IMPORT_ERROR = exc
else:
    STEP6_IMPORT_ERROR = None

__all__ = [
    'run_fastp_qc',
    'check_fastp_results',
    'run_remove_host',
    'check_host_remove_results',
    'run_extract_host',
    'run_kraken_bracken',
    'check_kraken_results',
    'run_remove_host_counts',
    'run_merge_step'
]

if run_merge_step is None:
    __all__.remove('run_merge_step')

__all__.append('STEP6_IMPORT_ERROR')
