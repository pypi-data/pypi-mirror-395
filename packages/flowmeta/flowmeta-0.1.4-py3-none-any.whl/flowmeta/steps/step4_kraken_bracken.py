"""Step 4: Kraken2 and Bracken taxonomic classification"""

import os
import re
import subprocess
import glob
import random
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
    _LOG_FILE_PATH = os.path.join(output_dir, f"flowmeta-step4-kraken-{date_str}.log")
    header = "=" * 80
    try:
        with open(_LOG_FILE_PATH, "a", encoding="utf-8") as fp:
            fp.write(f"\n{header}\nNew run started at {datetime.now().isoformat()}\n{header}\n")
    except Exception:
        pass


_SIZE_UNITS = 1024 ** 3


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def _format_version_string(raw_line, friendly_name):
    if not raw_line:
        return f"{friendly_name} version unknown"
    line = raw_line.strip()
    lower_line = line.lower()
    digit_match = re.search(r"(\d+(?:\.\d+)+)", line)
    if digit_match:
        return f"{friendly_name} v{digit_match.group(1)}"
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
    short = line if len(line) <= 40 else f"{line[:37]}..."
    return f"{friendly_name} ({short})"


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
            first_non_empty = next((ln for ln in output.splitlines() if ln.strip()), "")
            return _format_version_string(first_non_empty, friendly_name)
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
def _detect_kraken_version():
    return _detect_version(["kraken2", "--version"], "kraken2")


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def _detect_bracken_version():
    # bracken prints usage unless -v is passed; try both
    version = _detect_version(["bracken", "-v"], "bracken")
    if "version check failed" in version or "not found" in version or "version unknown" in version:
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
def _compute_directory_size_bytes(dir_path):
    total = 0
    for root, _dirs, files in os.walk(dir_path):
        for name in files:
            fp = os.path.join(root, name)
            try:
                total += os.path.getsize(fp)
            except OSError:
                continue
    return total


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def _sample_outputs_exist(sample_id, kraken_dir, bracken_dir):
    required = [
        os.path.join(kraken_dir, f"{sample_id}.task.complete"),
        os.path.join(kraken_dir, f"{sample_id}.kraken.report.txt"),
        os.path.join(kraken_dir, f"{sample_id}.kraken.output.txt"),
        os.path.join(bracken_dir, f"{sample_id}.g.bracken"),
        os.path.join(bracken_dir, f"{sample_id}.s.bracken"),
    ]
    return all(os.path.exists(path) and os.path.getsize(path) > 0 for path in required)


def _cleanup_candidate_paths(sample_id, kraken_dir, bracken_dir):
    paths = [
        os.path.join(kraken_dir, f"{sample_id}.task.complete"),
        os.path.join(kraken_dir, f"{sample_id}.kraken.report.txt"),
        os.path.join(kraken_dir, f"{sample_id}.kraken.output.txt"),
        os.path.join(kraken_dir, f"{sample_id}.kraken.report.std.txt"),
        os.path.join(kraken_dir, f"{sample_id}.kraken.mpa.std.txt"),
        os.path.join(bracken_dir, f"{sample_id}.g.bracken"),
        os.path.join(bracken_dir, f"{sample_id}.s.bracken"),
        os.path.join(bracken_dir, f"{sample_id}.f.bracken"),
        os.path.join(bracken_dir, f"{sample_id}.o.bracken"),
    ]
    paths.extend(
        os.path.join(kraken_dir, f"{sample_id}.diversity.{level}.txt")
        for level in ("g", "s")
    )
    return paths


def _has_partial_outputs(sample_id, kraken_dir, bracken_dir):
    return any(os.path.exists(path) for path in _cleanup_candidate_paths(sample_id, kraken_dir, bracken_dir))


def _cleanup_incomplete_outputs(sample_id, kraken_dir, bracken_dir):
    removed = []
    for path in _cleanup_candidate_paths(sample_id, kraken_dir, bracken_dir):
        if not os.path.exists(path):
            continue
        try:
            os.remove(path)
            removed.append(path)
        except Exception as exc:
            log_warning(f"[{sample_id}] Failed to remove stale file {path}: {exc}")
    if removed:
        log_info(f"[{sample_id}] Removed {len(removed)} stale Kraken/Bracken files before rerun")
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
def process_one_sample_kraken(sample_id, hr_dir, kraken_dir, bracken_dir, db_kraken,
                               helper_path, num_threads=16, se=False, force=False):
    """
    Run Kraken2 and Bracken for one sample.
    
    Args:
        sample_id (str): Sample ID
        hr_dir (str): Directory containing host-removed reads
        kraken_dir (str): Output directory for Kraken2 results
        bracken_dir (str): Output directory for Bracken results
        db_kraken (str): Path to Kraken2 database
        helper_path (str): Path to helper scripts
        num_threads (int): Number of threads
        se (bool): Single-end flag
    """
    task_complete = os.path.join(kraken_dir, f"{sample_id}.task.complete")
    kraken_report = os.path.join(kraken_dir, f"{sample_id}.kraken.report.txt")
    
    # Skip if already processed
    outputs_complete = _sample_outputs_exist(sample_id, kraken_dir, bracken_dir)
    if (not force) and outputs_complete:
        log_info(f"Skipped (already processed): {sample_id}")
        return

    if not outputs_complete and _has_partial_outputs(sample_id, kraken_dir, bracken_dir):
        log_info(f"[{sample_id}] Previous run incomplete, cleaning stale Kraken/Bracken outputs before rerun")
        _cleanup_incomplete_outputs(sample_id, kraken_dir, bracken_dir)
    
    log_info(f"Processing Kraken2/Bracken: {sample_id}")
    
    try:
        # Input files
        if se:
            fq = os.path.join(hr_dir, f"{sample_id}_host_remove.fastq.gz")
            if not os.path.exists(fq):
                log_warning(f"Input file not found: {fq}")
                return
            inputs = [fq]
        else:
            fq1 = os.path.join(hr_dir, f"{sample_id}_host_remove_R1.fastq.gz")
            fq2 = os.path.join(hr_dir, f"{sample_id}_host_remove_R2.fastq.gz")
            if not os.path.exists(fq1) or not os.path.exists(fq2):
                log_warning(f"Input files not found for {sample_id}")
                return
            inputs = [fq1, fq2]

        for fq_path in inputs:
            log_info(f"[{sample_id}] Checking input FASTQ: {fq_path}")
            if not os.path.exists(fq_path) or os.path.getsize(fq_path) == 0:
                log_warning(f"[{sample_id}] Input FASTQ missing or empty: {fq_path}")
                return
        
        # Output files
        kraken_output = os.path.join(kraken_dir, f"{sample_id}.kraken.output.txt")
        
        # Run Kraken2
        kraken_cmd = [
            "kraken2",
            "--db", db_kraken,
            "--threads", str(num_threads),
            "--memory-mapping",
            "--report-minimizer-data",
            "--report", kraken_report,
            "--use-names",
            "--output", kraken_output
        ]
        
        if se:
            kraken_cmd.append(fq)
        else:
            kraken_cmd.extend(["--paired", fq1, fq2])
        
        result = subprocess.run(kraken_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            _log_subprocess_failure(sample_id, "kraken2", result)
            return
        
        # Convert Kraken report to standard format (columns 1-3, 6-8)
        kraken_report_std = os.path.join(kraken_dir, f"{sample_id}.kraken.report.std.txt")
        with open(kraken_report, 'r') as fin, open(kraken_report_std, 'w') as fout:
            for line in fin:
                parts = line.rstrip('\n').split('\t')
                if len(parts) < 6:
                    continue
                # Keep first three columns and the trailing rank/taxid/name trio
                selected = parts[0:3] + parts[-3:]
                fout.write('\t'.join(selected) + '\n')
        
        # Convert to MPA format
        mpa_output = os.path.join(kraken_dir, f"{sample_id}.kraken.mpa.std.txt")
        kreport2mpa_script = os.path.join(helper_path, "kreport2mpa.py")
        
        result = subprocess.run(
            ["python", kreport2mpa_script, "-r", kraken_report_std, "-o", mpa_output],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            _log_subprocess_failure(sample_id, "kreport2mpa.py", result)
            return
        
        # Run Bracken for different taxonomic levels
        for level, level_code in [("G", "g"), ("S", "s"), ("F", "f"), ("O", "o")]:
            bracken_output = os.path.join(bracken_dir, f"{sample_id}.{level_code}.bracken")
            
            bracken_cmd = [
                "bracken",
                "-d", db_kraken,
                "-i", kraken_report,
                "-o", bracken_output,
                "-r", "100",
                "-l", level,
                "-t", "2"
            ]
            
            result = subprocess.run(bracken_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                _log_subprocess_failure(sample_id, f"bracken ({level})", result)
                return
        
        # Calculate alpha diversity
        alpha_script = os.path.join(helper_path, "alpha_diversity.py")
        
        for level_code, level_name in [("g", "genus"), ("s", "species")]:
            bracken_file = os.path.join(bracken_dir, f"{sample_id}.{level_code}.bracken")
            diversity_output = os.path.join(bracken_dir, f"{sample_id}.diversity.{level_code}.txt")
            
            with open(diversity_output, 'w') as fout:
                for metric in ["Sh", "BP", "Si", "ISi", "F"]:
                    result = subprocess.run(
                        ["python", alpha_script, "-f", bracken_file, "-a", metric],
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
        
        required = [kraken_report, kraken_output]
        if _outputs_ready(required):
            with open(task_complete, 'w') as f:
                f.write(f"Kraken2/Bracken processing complete for {sample_id}")
            log_success(f"Completed: {sample_id}")
        else:
            missing = [p for p in required if not (os.path.exists(p) and os.path.getsize(p) > 0)]
            log_warning(f"Kraken outputs missing for {sample_id}: {missing}; task flag not written")
        
    except subprocess.CalledProcessError as e:
        log_warning(f"Error processing {sample_id}: {e}")
    except Exception as e:
        log_warning(f"Error processing {sample_id}: {str(e)}")


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def run_kraken_bracken(hr_dir, kraken_dir, bracken_dir, db_kraken, helper_path,
                       batch_size=1, num_threads=16, se=False, force=False):
    """
    Run Kraken2 and Bracken for all samples.
    
    Args:
        hr_dir (str): Directory containing host-removed reads (03-hr)
        kraken_dir (str): Output directory for Kraken2 results (06-ku)
        bracken_dir (str): Output directory for Bracken results (07-bracken)
        db_kraken (str): Path to Kraken2 database
        helper_path (str): Path to helper scripts directory
        batch_size (int): Number of parallel processes
        num_threads (int): Threads per process
        se (bool): Single-end flag
        
    Returns:
        int: Number of processed samples
    """
    # Create output directories and initialize logging
    os.makedirs(kraken_dir, exist_ok=True)
    os.makedirs(bracken_dir, exist_ok=True)
    _initialize_step_logger(kraken_dir)

    kraken_version = _detect_kraken_version()
    bracken_version = _detect_bracken_version()

    log_info("=" * 60)
    print_colorful_message(
        f"STEP 4: Kraken2 & Bracken (kraken2 {kraken_version}, bracken {bracken_version})",
        "cyan",
    )
    log_info("=" * 60)
    log_info(f"kraken2 version: {kraken_version}")
    log_info(f"bracken version: {bracken_version}")
    if _LOG_FILE_PATH:
        log_info(f"Step log file: {_LOG_FILE_PATH}")
    
    # Check database
    required_files = ["hash.k2d", "opts.k2d", "taxo.k2d"]
    for req_file in required_files:
        if not os.path.exists(os.path.join(db_kraken, req_file)):
            log_warning(f"Kraken2 database file not found: {req_file}")
            return 0

    db_size_bytes = _compute_directory_size_bytes(db_kraken)
    db_size_gb = db_size_bytes / _SIZE_UNITS if db_size_bytes else 0
    log_info(f"Kraken DB size: {db_size_gb:.2f} GB")
    
    # Find all samples
    if se:
        pattern = "*_host_remove.fastq.gz"
        suffix_len = len("_host_remove.fastq.gz")
    else:
        pattern = "*_host_remove_R1.fastq.gz"
        suffix_len = len("_host_remove_R1.fastq.gz")
    
    all_files = glob.glob(os.path.join(hr_dir, pattern))
    sample_ids = [os.path.basename(f)[:-suffix_len] for f in all_files]
    
    if not sample_ids:
        log_warning(f"No samples found in {hr_dir}")
        return 0
    
    log_info(f"Found {len(sample_ids)} samples to process")
    log_info(f"Input directory: {hr_dir}")
    log_info(f"Kraken2 output: {kraken_dir}")
    log_info(f"Bracken output: {bracken_dir}")
    log_info(f"Database: {db_kraken}")
    log_info(f"Batch size: {batch_size}, Threads per sample: {num_threads}")
    
    # Shuffle for better load balancing
    random.shuffle(sample_ids)
    
    # Process in parallel
    if batch_size > 1:
        with Pool(processes=batch_size) as pool:
            pool.starmap(
                process_one_sample_kraken,
                                [(sid, hr_dir, kraken_dir, bracken_dir, db_kraken, helper_path,
                                    num_threads, se, force) for sid in sample_ids]
            )
    else:
        for sample_id in sample_ids:
            process_one_sample_kraken(
                                sample_id, hr_dir, kraken_dir, bracken_dir, db_kraken,
                                helper_path, num_threads, se, force
            )
    
    # Count successful outputs
    success_count = sum(1 for sid in sample_ids if os.path.exists(
        os.path.join(kraken_dir, f"{sid}.task.complete")))
    
    log_success(f"STEP 4 completed: {success_count}/{len(sample_ids)} samples processed")
    
    return success_count


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def check_kraken_results(kraken_dir):
    """
    Check Kraken2 results and remove failed samples.
    
    Args:
        kraken_dir (str): Directory containing Kraken2 results
        
    Returns:
        tuple: (valid_count, invalid_count)
    """
    log_info("Checking Kraken2 output files...")
    
    output_files = glob.glob(os.path.join(kraken_dir, "*.kraken.output.txt"))
    
    valid_count = 0
    invalid_count = 0
    
    for output_file in output_files:
        sample_id = os.path.basename(output_file).replace(".kraken.output.txt", "")
        
        # Check if file is empty
        if os.path.getsize(output_file) == 0:
            log_warning(f"Empty Kraken output for {sample_id}, deleting related files")
            
            # Delete all related files
            patterns = [
                f"{sample_id}*.kraken.*",
                f"{sample_id}*.task.complete"
            ]
            
            for pattern in patterns:
                for file in glob.glob(os.path.join(kraken_dir, pattern)):
                    try:
                        os.remove(file)
                    except Exception as e:
                        log_warning(f"Failed to delete {file}: {e}")
            
            invalid_count += 1
        else:
            valid_count += 1
    
    log_info(f"Valid samples: {valid_count}")
    log_warning(f"Invalid samples: {invalid_count}")
    
    return valid_count, invalid_count
