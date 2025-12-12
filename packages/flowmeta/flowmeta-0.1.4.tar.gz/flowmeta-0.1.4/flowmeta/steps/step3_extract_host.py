"""Step 5: Host-read extraction from BAM files"""

import os
import subprocess
import glob
from datetime import datetime
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
    _LOG_FILE_PATH = os.path.join(output_dir, f"flowmeta-step5-hostextract-{date_str}.log")
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
    return f"{friendly_name} ({line})"


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
        output = result.stdout.decode().strip() or result.stderr.decode().strip()
        if output:
            return _format_version_string(output.splitlines()[0], friendly_name)
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
def _detect_samtools_version():
    return _detect_version(["samtools", "--version"], "samtools")


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def _detect_pigz_version():
    return _detect_version(["pigz", "--version"], "pigz")


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
def _sample_outputs_exist(sample_id, host_dir):
    expected = [
        os.path.join(host_dir, f"{sample_id}_host_1.fastq.gz"),
        os.path.join(host_dir, f"{sample_id}_host_2.fastq.gz"),
        os.path.join(host_dir, f"{sample_id}.task.complete"),
    ]
    return all(os.path.exists(path) and os.path.getsize(path) > 0 for path in expected)


def _cleanup_candidate_paths(sample_id, host_dir):
    return [
        os.path.join(host_dir, f"{sample_id}_host_1.fastq.gz"),
        os.path.join(host_dir, f"{sample_id}_host_2.fastq.gz"),
        os.path.join(host_dir, f"{sample_id}_host_1.fastq"),
        os.path.join(host_dir, f"{sample_id}_host_2.fastq"),
        os.path.join(host_dir, f"{sample_id}.task.complete"),
    ]


def _has_partial_outputs(sample_id, host_dir):
    return any(os.path.exists(path) for path in _cleanup_candidate_paths(sample_id, host_dir))


def _cleanup_incomplete_outputs(sample_id, host_dir):
    removed = []
    for path in _cleanup_candidate_paths(sample_id, host_dir):
        if not os.path.exists(path):
            continue
        try:
            os.remove(path)
            removed.append(path)
        except Exception as exc:
            log_warning(f"[{sample_id}] Failed to remove stale file {path}: {exc}")
    if removed:
        log_info(f"[{sample_id}] Removed {len(removed)} stale intermediate files before rerun")
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
def _bam_is_valid(sample_id, bam_file):
    log_info(f"[{sample_id}] Checking BAM integrity: {bam_file}")
    try:
        result = subprocess.run(
            ["samtools", "quickcheck", "-v", bam_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except FileNotFoundError:
        log_warning("samtools not found; cannot validate BAM file integrity")
        return True

    if result.returncode == 0:
        log_success(f"[{sample_id}] BAM file passed quickcheck")
        return True

    messages = result.stdout.decode(errors="replace") or result.stderr.decode(errors="replace")
    log_warning(f"[{sample_id}] BAM validation failed: {messages}")
    return False


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def extract_host_reads_from_bam(sample_id, bam_dir, host_dir, mode="mapped_anypair",
                                 samtools_threads=48, pigz_threads=48, drop_supp=False,
                                 force=False):
    """
    Extract host reads from BAM file.
    
    Args:
        sample_id (str): Sample ID
        bam_dir (str): Directory containing BAM files
        host_dir (str): Output directory for host reads
        mode (str): Extraction mode (unmapped/mapped/mapped_anypair)
        samtools_threads (int): Threads for samtools
        pigz_threads (int): Threads for pigz compression
        drop_supp (bool): Drop supplementary alignments
    """
    bam_file = os.path.join(bam_dir, f"{sample_id}.bam")
    host_fq1 = os.path.join(host_dir, f"{sample_id}_host_1.fastq.gz")
    host_fq2 = os.path.join(host_dir, f"{sample_id}_host_2.fastq.gz")
    task_complete = os.path.join(host_dir, f"{sample_id}.task.complete")
    
    # Skip if already processed
    outputs_complete = _sample_outputs_exist(sample_id, host_dir)
    if (not force) and outputs_complete:
        log_info(f"Skipped (already processed): {sample_id}")
        return

    if not outputs_complete and _has_partial_outputs(sample_id, host_dir):
        log_info(f"[{sample_id}] Previous run incomplete, cleaning stale host files before rerun")
        _cleanup_incomplete_outputs(sample_id, host_dir)
    
    # Check BAM file exists
    if not os.path.exists(bam_file):
        log_warning(f"BAM file not found: {bam_file}")
        return

    if not _bam_is_valid(sample_id, bam_file):
        return
    
    log_info(f"Extracting host reads: {sample_id}")
    
    try:
        # Build samtools command based on mode
        sam_flags = []
        
        if mode == "unmapped":
            sam_flags = ["-f", "12"]  # Both unmapped
        elif mode == "mapped":
            sam_flags = ["-f", "2", "-F", "12"]  # Properly paired and mapped
        elif mode == "mapped_anypair":
            sam_flags = ["-F", "12"]  # At least one mapped
        
        # Always drop secondary alignments
        sam_flags.extend(["-F", "256"])
        
        # Optionally drop supplementary alignments
        if drop_supp:
            sam_flags.extend(["-F", "2048"])
        
        # Extract reads to FASTQ
        temp_fq1 = os.path.join(host_dir, f"{sample_id}_host_1.fastq")
        temp_fq2 = os.path.join(host_dir, f"{sample_id}_host_2.fastq")
        
        # Use samtools fastq to extract paired reads
        sam_cmd = [
            "samtools", "fastq",
            "-@", str(samtools_threads),
            "-1", temp_fq1,
            "-2", temp_fq2,
            "-0", "/dev/null",
            "-s", "/dev/null"
        ] + sam_flags + [bam_file]
        
        result = subprocess.run(sam_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            _log_subprocess_failure(sample_id, "samtools fastq", result)
            return
        
        # Compress with pigz
        pigz_cmd_1 = ["pigz", "-p", str(pigz_threads), temp_fq1]
        result = subprocess.run(pigz_cmd_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            _log_subprocess_failure(sample_id, "pigz (R1)", result)
            return

        pigz_cmd_2 = ["pigz", "-p", str(pigz_threads), temp_fq2]
        result = subprocess.run(pigz_cmd_2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            _log_subprocess_failure(sample_id, "pigz (R2)", result)
            return
        
        outputs = [host_fq1, host_fq2]
        if _outputs_ready(outputs):
            with open(task_complete, 'w') as f:
                f.write(f"Host extraction complete for {sample_id}")
            log_success(f"Completed: {sample_id}")
        else:
            missing = [p for p in outputs if not (os.path.exists(p) and os.path.getsize(p) > 0)]
            log_warning(f"Host FASTQ outputs missing for {sample_id}: {missing}; task flag not written")
        
    except subprocess.CalledProcessError as e:
        log_warning(f"Error extracting host reads from {sample_id}: {e}")
    except Exception as e:
        log_warning(f"Error extracting host reads from {sample_id}: {str(e)}")


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def run_extract_host(bam_dir, host_dir, mode="mapped_anypair",
                     samtools_threads=48, pigz_threads=48, drop_supp=False,
                     force=False):
    """
    Extract host reads from BAM files for all samples.
    
    Args:
        bam_dir (str): Directory containing BAM files (04-bam)
        host_dir (str): Output directory for host reads (05-host)
        mode (str): Extraction mode
        samtools_threads (int): Threads for samtools
        pigz_threads (int): Threads for pigz
        drop_supp (bool): Drop supplementary alignments
        
    Returns:
        int: Number of processed samples
    """
    # Create output directory and initialize logging
    os.makedirs(host_dir, exist_ok=True)
    _initialize_step_logger(host_dir)

    samtools_version = _detect_samtools_version()
    pigz_version = _detect_pigz_version()

    log_info("=" * 60)
    print_colorful_message(
        f"STEP 5: Host-read extraction (samtools {samtools_version}, pigz {pigz_version})",
        "cyan",
    )
    log_info("=" * 60)
    if _LOG_FILE_PATH:
        log_info(f"Step log file: {_LOG_FILE_PATH}")
    
    # Find all BAM files
    bam_files = glob.glob(os.path.join(bam_dir, "*.bam"))
    sample_ids = [os.path.basename(f)[:-4] for f in bam_files]
    
    if not sample_ids:
        log_warning(f"No BAM files found in {bam_dir}")
        return 0
    
    log_info(f"Found {len(sample_ids)} samples to process")
    log_info(f"Input BAM directory: {bam_dir}")
    log_info(f"Output host directory: {host_dir}")
    log_info(f"Extraction mode: {mode}")
    log_info(f"Threads: {samtools_threads}")
    
    # Process samples
    for sample_id in sample_ids:
        extract_host_reads_from_bam(
            sample_id, bam_dir, host_dir, mode,
            samtools_threads, pigz_threads, drop_supp,
            force=force
        )
    
    # Count successful outputs
    success_count = sum(1 for sid in sample_ids if os.path.exists(
        os.path.join(host_dir, f"{sid}.task.complete")))
    
    log_success(f"STEP 5 completed: {success_count}/{len(sample_ids)} samples processed")
    
    return success_count
