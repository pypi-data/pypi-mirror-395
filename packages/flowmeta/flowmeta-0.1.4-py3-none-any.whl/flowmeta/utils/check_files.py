"""File checking utilities for flowmeta"""

import os
import subprocess
from .logger import log_info, log_warning, log_error


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def check_fastq_integrity(fastq_file, threads=16):
    """
    Check if a FASTQ file is corrupted using pigz.
    
    Args:
        fastq_file (str): Path to the FASTQ file
        threads (int): Number of threads for pigz
        
    Returns:
        bool: True if file is intact, False otherwise
    """
    if not os.path.exists(fastq_file):
        log_warning(f"File does not exist: {fastq_file}")
        return False
    
    if os.path.getsize(fastq_file) == 0:
        log_warning(f"File is empty: {fastq_file}")
        return False
    
    try:
        result = subprocess.run(
            ["pigz", "-t", "-p", str(threads), fastq_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError as e:
        stderr_msg = e.stderr.decode() if e.stderr else "No stderr"
        log_warning(f"File integrity check failed for {fastq_file}: {stderr_msg}")
        return False
    except FileNotFoundError:
        log_warning(f"pigz not found in PATH; cannot verify {fastq_file}")
        return False


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def check_paired_files(sample_id, directory, suffix1="_1.fastq.gz", suffix2="_2.fastq.gz", threads=16):
    """
    Check if paired-end FASTQ files are valid.
    
    Args:
        sample_id (str): Sample ID
        directory (str): Directory containing files
        suffix1 (str): Suffix for R1 file
        suffix2 (str): Suffix for R2 file
        threads (int): Number of threads for checking
        
    Returns:
        tuple: (bool, list) - (all_valid, list of invalid files)
    """
    r1_file = os.path.join(directory, f"{sample_id}{suffix1}")
    r2_file = os.path.join(directory, f"{sample_id}{suffix2}")
    
    invalid_files = []
    
    if not check_fastq_integrity(r1_file, threads):
        invalid_files.append(r1_file)
    
    if not check_fastq_integrity(r2_file, threads):
        invalid_files.append(r2_file)
    
    return (len(invalid_files) == 0, invalid_files)


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def delete_sample_files(sample_id, directory, patterns):
    """
    Delete all files matching patterns for a sample.
    
    Args:
        sample_id (str): Sample ID
        directory (str): Directory containing files
        patterns (list): List of file patterns to delete
    """
    deleted_files = []
    for pattern in patterns:
        filepath = os.path.join(directory, f"{sample_id}{pattern}")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                deleted_files.append(filepath)
            except Exception as e:
                log_error(f"Failed to delete {filepath}: {e}")
    
    if deleted_files:
        log_warning(f"Deleted {len(deleted_files)} files for sample {sample_id}")
    
    return deleted_files
