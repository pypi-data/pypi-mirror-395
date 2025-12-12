"""Step 5: Remove host taxa from Kraken/Bracken results"""

import os
import re
import subprocess
import glob
from datetime import datetime
from multiprocessing import Pool
from ..utils import (
    log_info as base_log_info,
    log_success as base_log_success,
    log_warning as base_log_warning,
    log_error as base_log_error,
    print_colorful_message,
)


_LOG_FILE_PATH = None


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def _write_log_line(level, message):
    if not _LOG_FILE_PATH:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(_LOG_FILE_PATH, "a", encoding="utf-8") as fp:
            fp.write(f"[{timestamp}] [{level}] {message}\n")
    except Exception:
        pass


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def log_info(message):
    base_log_info(message)
    _write_log_line("INFO", message)


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def log_success(message):
    base_log_success(message)
    _write_log_line("SUCCESS", message)


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def log_warning(message):
    base_log_warning(message)
    _write_log_line("WARNING", message)


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def log_error(message):
    base_log_error(message)
    _write_log_line("ERROR", message)


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def _initialize_step_logger(output_dir):
    global _LOG_FILE_PATH
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    _LOG_FILE_PATH = os.path.join(output_dir, f"flowmeta-step5-removehost-{date_str}.log")
    header = "=" * 80
    try:
        with open(_LOG_FILE_PATH, "a", encoding="utf-8") as fp:
            fp.write(f"\n{header}\nNew run started at {datetime.now().isoformat()}\n{header}\n")
    except Exception:
        pass


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def _format_version_string(raw_line, friendly_name):
    if not raw_line:
        return f"{friendly_name} version unknown"
    line = raw_line.strip()
    digit_match = re.search(r"(\d+(?:\.\d+)+)", line)
    if digit_match:
        return f"{friendly_name} v{digit_match.group(1)}"
    lower_line = line.lower()
    if "version" in lower_line:
        after = line.lower().split("version", 1)[1].strip()
        token = after.split()[0] if after else ""
        if token:
            token = token.lstrip("vV")
            return f"{friendly_name} v{token}"
    for piece in line.replace(",", " ").split():
        if any(ch.isdigit() for ch in piece):
            piece = piece.lstrip("vV")
            return f"{friendly_name} v{piece}"
    truncated = line if len(line) <= 40 else f"{line[:37]}..."
    return f"{friendly_name} ({truncated})"


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def _detect_version(command, friendly_name):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        output = result.stdout.decode(errors="ignore").strip() or result.stderr.decode(errors="ignore").strip()
        if output:
            first_line = next((ln for ln in output.splitlines() if ln.strip()), "")
            if first_line:
                return _format_version_string(first_line, friendly_name)
        if result.returncode != 0:
            return f"{friendly_name} version check failed (exit {result.returncode})"
    except FileNotFoundError:
        return f"{friendly_name} not found"
    except Exception:
        pass
    return f"{friendly_name} version unknown"


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def _detect_bracken_version():
    version = _detect_version(["bracken", "-v"], "bracken")
    if any(token in version for token in ("not found", "version check failed", "version unknown")):
        return _detect_version(["bracken", "--version"], "bracken")
    return version


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def _outputs_ready(paths):
    return all(os.path.exists(p) and os.path.getsize(p) > 0 for p in paths)


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def _sample_outputs_exist(sample_id, out_dir):
    required = [
        os.path.join(out_dir, f"{sample_id}.task.complete"),
        os.path.join(out_dir, f"{sample_id}.nohuman.kraken.report.txt"),
        os.path.join(out_dir, f"{sample_id}.nohuman.kraken.mpa.std.txt"),
        os.path.join(out_dir, f"{sample_id}.g.bracken"),
        os.path.join(out_dir, f"{sample_id}.s.bracken"),
    ]
    return all(os.path.exists(path) and os.path.getsize(path) > 0 for path in required)


def _cleanup_candidate_paths(sample_id, out_dir):
    paths = [
        os.path.join(out_dir, f"{sample_id}.task.complete"),
        os.path.join(out_dir, f"{sample_id}.nohuman.kraken.report.txt"),
        os.path.join(out_dir, f"{sample_id}.nohuman.kraken.report.std.txt"),
        os.path.join(out_dir, f"{sample_id}.nohuman.kraken.mpa.std.txt"),
        os.path.join(out_dir, f"{sample_id}.g.bracken"),
        os.path.join(out_dir, f"{sample_id}.s.bracken"),
        os.path.join(out_dir, f"{sample_id}.f.bracken"),
        os.path.join(out_dir, f"{sample_id}.o.bracken"),
    ]
    paths.extend(
        os.path.join(out_dir, f"{sample_id}.diversity.{level}.txt")
        for level in ("g", "s")
    )
    return paths


def _has_partial_outputs(sample_id, out_dir):
    return any(os.path.exists(path) for path in _cleanup_candidate_paths(sample_id, out_dir))


def _cleanup_incomplete_outputs(sample_id, out_dir):
    removed = []
    for path in _cleanup_candidate_paths(sample_id, out_dir):
        if not os.path.exists(path):
            continue
        try:
            os.remove(path)
            removed.append(path)
        except Exception as exc:
            log_warning(f"[{sample_id}] Failed to remove stale file {path}: {exc}")
    if removed:
        log_info(f"[{sample_id}] Removed {len(removed)} stale host-filtered Kraken files before rerun")
    return bool(removed)

# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def _log_subprocess_failure(sample_id, tool_name, result):
    stderr_output = result.stderr.decode(errors="replace") if result.stderr else ""
    log_warning(f"[{sample_id}] {tool_name} failed (exit code {result.returncode})")
    if stderr_output:
        log_warning(f"[{sample_id}] {tool_name} stderr: {stderr_output}")


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def process_one_sample_remove_host(sample_id, in_dir, out_dir, db_kraken, helper_path,
                                   min_count=4, host_taxids=None, force=False):
    """Remove host taxa from one Kraken report and re-run Bracken/diversity."""
    if host_taxids is None:
        host_taxids = {
            '33208',   # Metazoa
            '6072',    # Eumetazoa
            '33213',   # Bilateria
            '33511',   # Deuterostomia
            '7711',    # Chordata
            '89593',   # Euteleostomi
            '7742',    # Vertebrata
            '32523',   # Tetrapoda
            '40674',   # Mammalia
            '9443',    # Primates
            '314295',  # Catarrhini
            '9526',    # Hominidae
            '9604',    # Homo/Pan/Gorilla etc
            '9605',    # Homo-Pan-Gorilla
            '9606'     # Homo sapiens
        }

    rpt = os.path.join(in_dir, f"{sample_id}.kraken.report.txt")
    if not os.path.exists(rpt):
        log_warning(f"Missing Kraken report for {sample_id}")
        return

    os.makedirs(out_dir, exist_ok=True)

    nohum_rpt = os.path.join(out_dir, f"{sample_id}.nohuman.kraken.report.txt")
    nohum_std = os.path.join(out_dir, f"{sample_id}.nohuman.kraken.report.std.txt")
    nohum_mpa = os.path.join(out_dir, f"{sample_id}.nohuman.kraken.mpa.std.txt")
    done_flag = os.path.join(out_dir, f"{sample_id}.task.complete")

    outputs_complete = _sample_outputs_exist(sample_id, out_dir)
    if (not force) and outputs_complete:
        log_info(f"Skipped (already processed): {sample_id}")
        return

    if not outputs_complete and _has_partial_outputs(sample_id, out_dir):
        log_info(f"[{sample_id}] Previous run incomplete, cleaning stale host-filtered outputs before rerun")
        _cleanup_incomplete_outputs(sample_id, out_dir)

    log_info(f"Removing host taxa from {sample_id}")

    try:
        # Filter host taxa
        def _kraken_depth(raw_name):
            spaces = 0
            for ch in raw_name:
                if ch == ' ':
                    spaces += 1
                else:
                    break
            return spaces // 2

        skip_stack = []

        with open(rpt) as fin, open(nohum_rpt, 'w') as fout:
            for line in fin:
                parts = line.rstrip('\n').split('\t')
                if len(parts) < 5:
                    continue
                taxid = parts[-2]
                depth = _kraken_depth(parts[-1])

                while skip_stack and depth <= skip_stack[-1]:
                    skip_stack.pop()

                if skip_stack:
                    continue

                if taxid in host_taxids:
                    skip_stack.append(depth)
                    continue
                fout.write(line)

        # Create std file (columns 1-3,6-8)
        with open(nohum_rpt) as fin, open(nohum_std, 'w') as fout:
            for line in fin:
                parts = line.rstrip('\n').split('\t')
                if len(parts) < 6:
                    continue
                selected = parts[0:3] + parts[-3:]
                fout.write('\t'.join(selected) + '\n')

        # Convert to MPA
        kreport2mpa_script = os.path.join(helper_path, 'kreport2mpa.py')
        result = subprocess.run(
            ['python', kreport2mpa_script, '-r', nohum_std, '-o', nohum_mpa],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            _log_subprocess_failure(sample_id, 'kreport2mpa.py', result)
            return

        # Re-run Bracken using filtered report
        for level, level_code in [('G', 'g'), ('S', 's'), ('F', 'f'), ('O', 'o')]:
            bracken_output = os.path.join(out_dir, f"{sample_id}.{level_code}.bracken")
            bracken_cmd = [
                'bracken', '-d', db_kraken,
                '-i', nohum_rpt,
                '-o', bracken_output,
                '-r', '100',
                '-l', level,
                '-t', str(min_count)
            ]
            result = subprocess.run(bracken_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                _log_subprocess_failure(sample_id, f'bracken ({level})', result)
                return

        # Alpha diversity from filtered results
        alpha_script = os.path.join(helper_path, 'alpha_diversity.py')
        for level_code in ['g', 's']:
            bracken_file = os.path.join(out_dir, f"{sample_id}.{level_code}.bracken")
            diversity_output = os.path.join(out_dir, f"{sample_id}.diversity.{level_code}.txt")
            with open(diversity_output, 'w') as fout:
                for metric in ['Sh', 'BP', 'Si', 'ISi', 'F']:
                    result = subprocess.run(
                        ['python', alpha_script, '-f', bracken_file, '-a', metric],
                        capture_output=True,
                        text=True,
                    )
                    if result.returncode != 0:
                        log_warning(
                            f"[{sample_id}] alpha_diversity metric {metric} failed with code {result.returncode}"
                        )
                        log_warning(f"[{sample_id}] alpha_diversity stderr: {result.stderr}")
                        return
                    fout.write(result.stdout)

        outputs = [nohum_rpt, nohum_mpa]
        if _outputs_ready(outputs):
            with open(done_flag, 'w') as f:
                f.write('Host removal from Kraken results complete')
            log_success(f"Host-removed Kraken data ready: {sample_id}")
        else:
            missing = [p for p in outputs if not (os.path.exists(p) and os.path.getsize(p) > 0)]
            log_warning(f"Filtered Kraken outputs missing for {sample_id}: {missing}; task flag not written")

    except subprocess.CalledProcessError as e:
        log_warning(f"Bracken/MPA error for {sample_id}: {e}")
    except Exception as e:
        log_warning(f"Unexpected error for {sample_id}: {str(e)}")


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def run_remove_host_counts(in_dir, out_dir, db_kraken, helper_path,
                            batch_size=1, min_count=4, force=False):
    """Batch remove host taxa from Kraken reports."""
    os.makedirs(out_dir, exist_ok=True)
    _initialize_step_logger(out_dir)

    bracken_version = _detect_bracken_version()

    log_info("=" * 60)
    print_colorful_message(
        f"STEP 5: Remove host taxa from Kraken results (bracken {bracken_version})",
        'cyan'
    )
    log_info("=" * 60)
    if _LOG_FILE_PATH:
        log_info(f"Step log file: {_LOG_FILE_PATH}")
    reports = glob.glob(os.path.join(in_dir, '*.kraken.report.txt'))
    sample_ids = [os.path.basename(r).replace('.kraken.report.txt', '') for r in reports]

    if not sample_ids:
        log_warning(f"No Kraken reports found in {in_dir}")
        return 0

    log_info(f"Input: {in_dir}")
    log_info(f"Output: {out_dir}")

    original_total = len(sample_ids)
    if not force:
        pending = [sid for sid in sample_ids if not _sample_outputs_exist(sid, out_dir)]
        skipped = original_total - len(pending)
        if skipped and pending:
            log_info(f"Skipping {skipped} samples (already processed)")
        elif skipped and not pending:
            log_success(f"STEP 5 already complete: {original_total}/{original_total} samples present")
            return original_total
        sample_ids = pending

    log_info(f"Samples to process: {len(sample_ids)}")

    if not sample_ids:
        log_warning("No samples require processing (force disabled)")
        return 0

    if batch_size > 1:
        with Pool(processes=batch_size) as pool:
            pool.starmap(
                process_one_sample_remove_host,
                [(sid, in_dir, out_dir, db_kraken, helper_path, min_count, None, force)
                 for sid in sample_ids]
            )
    else:
        for sid in sample_ids:
            process_one_sample_remove_host(
                sid, in_dir, out_dir, db_kraken, helper_path, min_count, None, force
            )

    success = sum(1 for sid in sample_ids if os.path.exists(
        os.path.join(out_dir, f"{sid}.task.complete")))
    log_success(f"STEP 5 completed: {success}/{len(sample_ids)} samples processed")
    return success
