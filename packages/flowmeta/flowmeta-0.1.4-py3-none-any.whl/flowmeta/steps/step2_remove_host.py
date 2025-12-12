"""Step 2: Remove host reads using Bowtie2"""

# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15

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
    check_fastq_integrity,
)


_LOG_FILE_PATH = None


def _write_log_line(level, message):
    if not _LOG_FILE_PATH:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(_LOG_FILE_PATH, "a", encoding="utf-8") as fp:
            fp.write(f"[{timestamp}] [{level}] {message}\n")
    except Exception:
        pass


def log_info(message):
    base_log_info(message)
    _write_log_line("INFO", message)


def log_success(message):
    base_log_success(message)
    _write_log_line("SUCCESS", message)


def log_warning(message):
    base_log_warning(message)
    _write_log_line("WARNING", message)


def log_error(message):
    base_log_error(message)
    _write_log_line("ERROR", message)


def _initialize_step_logger(output_dir):
    global _LOG_FILE_PATH
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    _LOG_FILE_PATH = os.path.join(output_dir, f"flowmeta-step2-bowtie2-{date_str}.log")
    header = "=" * 80
    try:
        with open(_LOG_FILE_PATH, "a", encoding="utf-8") as fp:
            fp.write(f"\n{header}\nNew run started at {datetime.now().isoformat()}\n{header}\n")
    except Exception:
        pass


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
    # fallback to first token containing digit
    for piece in line.replace(",", " ").split():
        if any(ch.isdigit() for ch in piece):
            piece = piece.lstrip("vV")
            return f"{friendly_name} v{piece}"
    return f"{friendly_name} ({line})"


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


def _detect_bowtie2_version():
    return _detect_version(["bowtie2", "--version"], "bowtie2")


def _detect_samtools_version():
    return _detect_version(["samtools", "--version"], "samtools")


def _outputs_ready(paths):
    return all(os.path.exists(p) and os.path.getsize(p) > 0 for p in paths)


def _sample_outputs_exist(sample_id, hr_dir, bam_dir):
    expected = [
        os.path.join(hr_dir, f"{sample_id}_host_remove_R1.fastq.gz"),
        os.path.join(hr_dir, f"{sample_id}_host_remove_R2.fastq.gz"),
        os.path.join(hr_dir, f"{sample_id}.task.complete"),
        os.path.join(bam_dir, f"{sample_id}.bam"),
    ]
    return all(os.path.exists(path) and os.path.getsize(path) > 0 for path in expected)


def _cleanup_candidate_paths(sample_id, hr_dir, bam_dir):
    return [
        os.path.join(hr_dir, f"{sample_id}_host_remove_R1.fastq.gz"),
        os.path.join(hr_dir, f"{sample_id}_host_remove_R2.fastq.gz"),
        os.path.join(hr_dir, f"{sample_id}.task.complete"),
        os.path.join(bam_dir, f"{sample_id}.bam"),
        os.path.join(bam_dir, f"{sample_id}.bam.sorted"),
        os.path.join(bam_dir, f"{sample_id}.task.complete"),
        os.path.join(bam_dir, f"{sample_id}.sam"),
    ]


def _has_partial_outputs(sample_id, hr_dir, bam_dir):
    return any(os.path.exists(path) for path in _cleanup_candidate_paths(sample_id, hr_dir, bam_dir))


def _cleanup_incomplete_outputs(sample_id, hr_dir, bam_dir):
    removed = []
    for path in _cleanup_candidate_paths(sample_id, hr_dir, bam_dir):
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


def _log_subprocess_failure(sample_id, tool_name, result):
    stderr_output = result.stderr.decode(errors="replace") if result.stderr else ""
    log_warning(f"[{sample_id}] {tool_name} failed (exit code {result.returncode})")
    if stderr_output:
        log_warning(f"[{sample_id}] {tool_name} stderr: {stderr_output}")
    if "libcrypto" in stderr_output.lower():
        log_warning(
            f"[{sample_id}] Detected missing libcrypto in {tool_name} output; "
            "ensure OpenSSL 1.0 compatibility libraries are installed in the environment."
        )


def process_one_sample_bowtie2(sample_id, fastp_dir, hr_dir, bam_dir, db_bowtie2,
                                threads, suffix1="_1.fastq.gz", suffix2="_2.fastq.gz",
                                force=False):
    """
    Remove host reads from one sample using Bowtie2.
    
    Args:
        sample_id (str): Sample ID
        fastp_dir (str): Directory containing fastp outputs
        hr_dir (str): Directory for host-removed reads
        bam_dir (str): Directory for BAM files
        db_bowtie2 (str): Path to Bowtie2 index
        threads (int): Number of threads
        suffix1 (str): Forward read suffix
        suffix2 (str): Reverse read suffix
    """
    # Input files
    fq1 = os.path.join(fastp_dir, f"{sample_id}{suffix1}")
    fq2 = os.path.join(fastp_dir, f"{sample_id}{suffix2}")
    
    # Output files
    hr_fq1 = os.path.join(hr_dir, f"{sample_id}_host_remove_R1.fastq.gz")
    hr_fq2 = os.path.join(hr_dir, f"{sample_id}_host_remove_R2.fastq.gz")
    bam_file = os.path.join(bam_dir, f"{sample_id}.bam")
    task_complete = os.path.join(hr_dir, f"{sample_id}.task.complete")
    
    # Skip if already processed
    outputs_complete = _sample_outputs_exist(sample_id, hr_dir, bam_dir)
    if (not force) and outputs_complete:
        log_info(f"Skipped (already processed): {sample_id}")
        return

    if not outputs_complete and _has_partial_outputs(sample_id, hr_dir, bam_dir):
        log_info(f"[{sample_id}] Previous run incomplete, cleaning stale outputs before rerun")
        _cleanup_incomplete_outputs(sample_id, hr_dir, bam_dir)
    
    # Check input files exist
    if not os.path.exists(fq1) or not os.path.exists(fq2):
        log_warning(f"Input files not found for {sample_id}")
        return

    for fq_path, label in ((fq1, "forward"), (fq2, "reverse")):
        log_info(f"[{sample_id}] Checking {label} file integrity: {fq_path}")
        if not check_fastq_integrity(fq_path, threads=max(1, threads // 4)):
            log_warning(f"[{sample_id}] {label.capitalize()} file failed integrity check: {fq_path}")
            return
        log_success(f"[{sample_id}] {label.capitalize()} file passed integrity check")
    
    log_info(f"Processing: {sample_id}")
    
    try:
        # Run Bowtie2
        sam_file = os.path.join(bam_dir, f"{sample_id}.sam")
        
        bowtie2_cmd = [
            "bowtie2",
            "-p", str(threads),
            "-x", db_bowtie2,
            "-1", fq1,
            "-2", fq2,
            "-S", sam_file,
            "--un-conc-gz", os.path.join(hr_dir, f"{sample_id}_host_remove_R%.fastq.gz")
        ]
        
        result = subprocess.run(bowtie2_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            _log_subprocess_failure(sample_id, "bowtie2", result)
            return
        
        # Convert SAM to BAM and sort
        view_cmd = ["samtools", "view", "-@", str(threads), "-bS", sam_file, "-o", bam_file]
        result = subprocess.run(view_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            _log_subprocess_failure(sample_id, "samtools view", result)
            return
        
        sort_cmd = ["samtools", "sort", "-@", str(threads), "-o", f"{bam_file}.sorted", bam_file]
        result = subprocess.run(sort_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            _log_subprocess_failure(sample_id, "samtools sort", result)
            return
        
        index_cmd = ["samtools", "index", "-@", str(threads), f"{bam_file}.sorted"]
        result = subprocess.run(index_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            _log_subprocess_failure(sample_id, "samtools index", result)
            return
        
        # Clean up SAM file
        if os.path.exists(sam_file):
            os.remove(sam_file)
        
        # Rename sorted BAM
        if os.path.exists(f"{bam_file}.sorted"):
            os.rename(f"{bam_file}.sorted", bam_file)
        
        outputs = [hr_fq1, hr_fq2, bam_file]
        if _outputs_ready(outputs):
            with open(task_complete, 'w') as f:
                f.write(f"Host removal complete for {sample_id}")
            bam_task = os.path.join(bam_dir, f"{sample_id}.task.complete")
            with open(bam_task, 'w') as f:
                f.write(f"BAM generated for {sample_id}")
            log_success(f"Completed: {sample_id}")
        else:
            missing = [p for p in outputs if not (os.path.exists(p) and os.path.getsize(p) > 0)]
            log_warning(f"Host removal outputs missing for {sample_id}: {missing}; task flag not written")
        
    except subprocess.CalledProcessError as e:
        log_warning(f"Error processing {sample_id}: {e}")
    except Exception as e:
        log_warning(f"Error processing {sample_id}: {str(e)}")


def run_remove_host(fastp_dir, hr_dir, bam_dir, db_bowtie2, threads=48,
                    suffix1="_1.fastq.gz", suffix2="_2.fastq.gz", force=False):
    """
    Remove host reads using Bowtie2 for all samples.
    
    Args:
        fastp_dir (str): Directory containing fastp outputs (02-qc)
        hr_dir (str): Output directory for host-removed reads (03-hr)
        bam_dir (str): Output directory for BAM files (04-bam)
        db_bowtie2 (str): Path to Bowtie2 index
        threads (int): Number of threads
        suffix1 (str): Forward read suffix
        suffix2 (str): Reverse read suffix
        
    Returns:
        int: Number of processed samples
    """
    # Create output directories
    os.makedirs(hr_dir, exist_ok=True)
    os.makedirs(bam_dir, exist_ok=True)
    _initialize_step_logger(hr_dir)

    bowtie2_version = _detect_bowtie2_version()
    samtools_version = _detect_samtools_version()

    log_info("=" * 60)
    print_colorful_message(
        f"STEP 2: Remove Host Reads (bowtie2 {bowtie2_version}, samtools {samtools_version})",
        "cyan",
    )
    log_info("=" * 60)
    if _LOG_FILE_PATH:
        log_info(f"Step log file: {_LOG_FILE_PATH}")
    
    # Check Bowtie2 index
    if not (os.path.exists(f"{db_bowtie2}.1.bt2") or os.path.exists(f"{db_bowtie2}.1.bt2l")):
        log_warning(f"Bowtie2 index not found: {db_bowtie2}")
        return 0
    
    # Find all forward read files
    all_files = glob.glob(os.path.join(fastp_dir, f"*{suffix1}"))
    sample_ids = [os.path.basename(f)[:-len(suffix1)] for f in all_files]
    
    if not sample_ids:
        log_warning(f"No samples found in {fastp_dir}")
        return 0
    
    log_info(f"Found {len(sample_ids)} samples to process")
    log_info(f"Input directory: {fastp_dir}")
    log_info(f"Output HR directory: {hr_dir}")
    log_info(f"Output BAM directory: {bam_dir}")
    log_info(f"Bowtie2 index: {db_bowtie2}")
    log_info(f"Threads: {threads}")
    
    # Process samples sequentially (Bowtie2 is already multi-threaded)
    for sample_id in sample_ids:
        process_one_sample_bowtie2(
            sample_id, fastp_dir, hr_dir, bam_dir, db_bowtie2,
            threads, suffix1, suffix2, force=force
        )
    
    # Count successful outputs
    success_count = sum(1 for sid in sample_ids if os.path.exists(
        os.path.join(hr_dir, f"{sid}.task.complete")))
    
    log_success(f"STEP 2 completed: {success_count}/{len(sample_ids)} samples processed")
    
    return success_count


def check_host_remove_results(hr_dir, suffix1="_host_remove_R1.fastq.gz", 
                               suffix2="_host_remove_R2.fastq.gz", threads=16):
    """
    Check host-removed FASTQ file integrity.
    
    Args:
        hr_dir (str): Directory containing host-removed reads
        suffix1 (str): Forward read suffix
        suffix2 (str): Reverse read suffix
        threads (int): Number of threads for checking
        
    Returns:
        tuple: (valid_count, invalid_count)
    """
    from ..utils import check_paired_files, delete_sample_files
    
    log_info("Checking host-removed file integrity...")
    
    all_files = glob.glob(os.path.join(hr_dir, f"*{suffix1}"))
    sample_ids = [os.path.basename(f)[:-len(suffix1)] for f in all_files]
    
    valid_samples = []
    invalid_samples = []
    
    for sample_id in sample_ids:
        is_valid, _ = check_paired_files(sample_id, hr_dir, suffix1, suffix2, threads)
        
        if is_valid:
            valid_samples.append(sample_id)
        else:
            invalid_samples.append(sample_id)
            # Delete corrupted files
            delete_sample_files(
                sample_id,
                hr_dir,
                [suffix1, suffix2, ".task.complete"]
            )
    
    log_info(f"Valid samples: {len(valid_samples)}")
    log_warning(f"Invalid samples: {len(invalid_samples)}")
    
    return len(valid_samples), len(invalid_samples)
