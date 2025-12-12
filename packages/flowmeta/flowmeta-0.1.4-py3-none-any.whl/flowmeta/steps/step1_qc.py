"""Step 1: FASTQ Quality Control using fastp"""

# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-21

import os
import subprocess
import random
import shutil
from datetime import datetime
from multiprocessing import Pool
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
        # We intentionally keep console logging even if file logging fails
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
    _LOG_FILE_PATH = os.path.join(output_dir, f"flowmeta-step1-fastp-{date_str}.log")
    header = "=" * 80
    try:
        with open(_LOG_FILE_PATH, "a", encoding="utf-8") as fp:
            fp.write(f"\n{header}\nNew run started at {datetime.now().isoformat()}\n{header}\n")
    except Exception:
        pass


def _pool_initializer(log_path):
    global _LOG_FILE_PATH
    _LOG_FILE_PATH = log_path


def _detect_fastp_version():
    """Return fastp version string, e.g. '0.23.4'; fallback to 'unknown'."""
    try:
        result = subprocess.run(
            ["fastp", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        output = result.stdout.decode().strip() or result.stderr.decode().strip()
        if output:
            return output.splitlines()[0].strip()
    except FileNotFoundError:
        return "fastp not found"
    except Exception:
        pass
    return "fastp version unknown"


def _files_ready(paths):
    return all(os.path.exists(p) and os.path.getsize(p) > 0 for p in paths)


def _sample_outputs_exist(sample_id, path_output, suffix1, se):
    """Verify whether all expected result files already exist for a sample."""
    expected = [
        os.path.join(path_output, f"{sample_id}{suffix1}"),
        os.path.join(path_output, f"{sample_id}_fastp.html"),
        os.path.join(path_output, f"{sample_id}_fastp.json"),
        os.path.join(path_output, f"{sample_id}.task.complete"),
    ]
    if not se:
        suffix2 = suffix1.replace("1", "2")
        expected.append(os.path.join(path_output, f"{sample_id}{suffix2}"))
    return all(os.path.exists(path) and os.path.getsize(path) > 0 for path in expected)


def _record_corrupted_sample(path_input, sample_id, files, reason):
    """Log corrupted samples and move their files aside for inspection."""
    report_path = os.path.join(path_input, "0-corrupted-samples.tsv")
    report_exists = os.path.exists(report_path)
    corrupted_dir = os.path.join(path_input, "00-corrupted")
    os.makedirs(corrupted_dir, exist_ok=True)

    basenames = []
    for file_path in files:
        if not file_path:
            continue
        basenames.append(os.path.basename(file_path))
        if os.path.exists(file_path):
            destination = os.path.join(corrupted_dir, os.path.basename(file_path))
            try:
                shutil.move(file_path, destination)
            except Exception as move_error:
                log_warning(f"Failed to move {file_path} to {destination}: {move_error}")

    try:
        with open(report_path, "a", encoding="utf-8") as report:
            if not report_exists:
                report.write("sample_id\treason\tfiles\n")
            report.write(f"{sample_id}\t{reason}\t{','.join(basenames)}\n")
    except Exception as report_error:
        log_warning(f"Failed to write corrupted sample log for {sample_id}: {report_error}")


def process_single_sample(file, path_input, path_output, num_threads, suffix1, se,
                          length_required, force):
    """
    Process a single FASTQ file using fastp.
    
    Args:
        file (str): File name of the FASTQ file
        path_input (str): Path where raw FASTQ files are located
        path_output (str): Path where processed files will be saved
        num_threads (int): Number of threads for fastp
        suffix1 (str): Suffix for the forward reads files
        se (bool): Flag to indicate if the data is single-end
        length_required (int): Minimum length of reads to keep
    """
    suffix2 = suffix1.replace("1", "2")
    
    if file.endswith(suffix1):
        forward_file = os.path.join(path_input, file)
        sample_id = file[:-len(suffix1)]
        output_forward = os.path.join(path_output, file)
        task_file = os.path.join(path_output, f"{sample_id}.task.complete")

        # Skip if already processed
        if not force and _sample_outputs_exist(sample_id, path_output, suffix1, se):
            log_info(f"Skipped (already processed): {sample_id}")
            return

        reverse_file = None if se else forward_file[:-len(suffix1)] + suffix2
        files_to_move = [forward_file] + ([reverse_file] if reverse_file else [])

        # Check input file integrity before processing
        files_to_validate = [(forward_file, "forward")]
        if reverse_file:
            files_to_validate.append((reverse_file, "reverse"))

        for file_path, label in files_to_validate:
            log_info(f"[{sample_id}] Checking {label} file integrity: {file_path}")
            if not check_fastq_integrity(file_path, threads=4):
                log_warning(f"[{sample_id}] Input file corrupted or unreadable ({label}): {file_path}")
                _record_corrupted_sample(
                    path_input,
                    sample_id,
                    files_to_move,
                    f"{label} file failed integrity check",
                )
                return
            log_success(f"[{sample_id}] {label.capitalize()} file passed integrity check")

        log_info(f"Processing: {sample_id}")

        try:
            if se:
                # Single-end processing
                command = [
                    "fastp",
                    "-i", forward_file,
                    "-o", output_forward,
                    "--thread", str(num_threads),
                    "--length_required", str(length_required),
                    "--n_base_limit", "6",
                    "--compression", "6",
                    "--html", os.path.join(path_output, f"{sample_id}_fastp.html"),
                    "--json", os.path.join(path_output, f"{sample_id}_fastp.json")
                ]
            else:
                # Paired-end processing
                output_reverse = output_forward[:-len(suffix1)] + suffix2
                command = [
                    "fastp",
                    "-i", forward_file,
                    "-o", output_forward,
                    "-I", reverse_file,
                    "-O", output_reverse,
                    "--thread", str(num_threads),
                    "--length_required", str(length_required),
                    "--n_base_limit", "6",
                    "--compression", "6",
                    "--html", os.path.join(path_output, f"{sample_id}_fastp.html"),
                    "--json", os.path.join(path_output, f"{sample_id}_fastp.json")
                ]
            
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result.returncode != 0:
                stderr_output = result.stderr.decode() if result.stderr else "No stderr captured"
                log_warning(f"Fastp failed for {sample_id} (exit code {result.returncode}):")
                log_warning(f"  {stderr_output}")
                return

            outputs = [output_forward]
            if not se:
                outputs.append(output_reverse)

            if _files_ready(outputs):
                with open(task_file, 'w') as f:
                    f.write(f"Processing complete for {sample_id}")
                log_success(f"Completed: {sample_id}")
            else:
                log_warning(f"Outputs missing/empty for {sample_id}; task flag not written")
            
        except subprocess.CalledProcessError as e:
            stderr_msg = e.stderr.decode() if e.stderr else "No stderr"
            log_warning(f"Error processing {sample_id}: {stderr_msg}")
        except Exception as e:
            log_warning(f"Error processing {sample_id}: {str(e)}")


def run_fastp_qc(input_dir, output_dir, num_threads=16, suffix1="_1.fastq.gz",
                 batch_size=1, se=False, length_required=50, force=False):
    """
    Run FASTQ quality control using fastp.
    
    Args:
        input_dir (str): Input directory containing raw FASTQ files (01-raw)
        output_dir (str): Output directory for QC'd files (02-qc)
        num_threads (int): Number of threads for fastp
        suffix1 (str): Suffix for forward reads
        batch_size (int): Number of samples to process in parallel
        se (bool): Single-end sequencing flag
        length_required (int): Minimum read length
        
    Returns:
        int: Number of processed samples
    """
    # Create output directory and initialize log file
    os.makedirs(output_dir, exist_ok=True)
    _initialize_step_logger(output_dir)
    fastp_version = _detect_fastp_version()

    log_info("=" * 60)
    print_colorful_message(f"STEP 1: FASTQ Quality Control (fastp {fastp_version})", "cyan")
    log_info("=" * 60)
    if _LOG_FILE_PATH:
        log_info(f"Step log file: {_LOG_FILE_PATH}")
    
    # Find all forward read files
    all_files = [f for f in os.listdir(input_dir) if f.endswith(suffix1)]
    
    if not all_files:
        log_warning(f"No files with suffix '{suffix1}' found in {input_dir}")
        return 0
    
    log_info(f"Found {len(all_files)} samples to process")
    log_info(f"Input directory: {input_dir}")
    log_info(f"Output directory: {output_dir}")
    log_info(f"Batch size: {batch_size}, Threads per sample: {num_threads}")
    
    # Shuffle files for better parallelization
    random.shuffle(all_files)
    
    # Process in parallel
    with Pool(processes=batch_size, initializer=_pool_initializer, initargs=(_LOG_FILE_PATH,)) as pool:
        pool.starmap(
            process_single_sample,
            [(f, input_dir, output_dir, num_threads, suffix1, se, length_required, force)
             for f in all_files]
        )
    
    # Count successful outputs
    success_count = sum(1 for f in all_files if os.path.exists(
        os.path.join(output_dir, f"{f[:-len(suffix1)]}.task.complete")))
    
    log_success(f"STEP 1 completed: {success_count}/{len(all_files)} samples processed")
    
    return success_count


def check_fastp_results(output_dir, suffix1="_1.fastq.gz", threads=16, max_rounds=3):
    """
    Check fastp output integrity and remove corrupted files.
    
    Args:
        output_dir (str): Directory containing fastp outputs
        suffix1 (str): Suffix for forward reads
        threads (int): Number of threads for pigz testing
        max_rounds (int): Maximum number of check rounds
        
    Returns:
        tuple: (valid_count, invalid_count)
    """
    from ..utils import check_paired_files, delete_sample_files
    
    log_info("Checking fastp output file integrity...")
    
    suffix2 = suffix1.replace("1", "2")
    all_files = [f for f in os.listdir(output_dir) if f.endswith(suffix1)]
    
    valid_samples = []
    invalid_samples = []
    
    for file in all_files:
        sample_id = file[:-len(suffix1)]
        is_valid, invalid_files = check_paired_files(sample_id, output_dir, suffix1, suffix2, threads)
        
        if is_valid:
            valid_samples.append(sample_id)
        else:
            invalid_samples.append(sample_id)
            log_warning(f"Sample {sample_id} failed integrity check: {invalid_files}")
            # Delete corrupted files and task completion marker
            delete_sample_files(
                sample_id,
                output_dir,
                [suffix1, suffix2, "_fastp.html", "_fastp.json", ".task.complete"]
            )
    
    log_info(f"Valid samples: {len(valid_samples)}")
    log_warning(f"Invalid samples: {len(invalid_samples)}")
    
    return len(valid_samples), len(invalid_samples)
