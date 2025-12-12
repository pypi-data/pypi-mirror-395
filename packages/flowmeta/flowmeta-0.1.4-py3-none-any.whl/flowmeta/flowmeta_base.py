"""Main orchestration function for the flowmeta metagenomic pipeline."""

import os
import shutil
import subprocess
from pathlib import Path
from .utils import log_info, log_success, log_warning, log_error, print_colorful_message
from .steps import (
    run_fastp_qc,
    check_fastp_results,
    run_remove_host,
    check_host_remove_results,
    run_extract_host,
    run_kraken_bracken,
    check_kraken_results,
    run_remove_host_counts,
)
from .steps import run_merge_step, STEP6_IMPORT_ERROR

DEFAULT_SUFFIX1 = "_1.fastq.gz"
DEFAULT_SUFFIX2 = "_2.fastq.gz"


class FlowMetaError(RuntimeError):
    """Raised when an unrecoverable error occurs in the pipeline."""


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Repository: https://github.com/SkinMicrobe/FlowMeta
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Repository: https://github.com/SkinMicrobe/FlowMeta
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def verify_fastq_naming(input_dir, suffix1, suffix2):
    """Ensure FASTQ files follow the expected naming convention."""
    files = list(Path(input_dir).glob("*.fastq.gz"))
    if not files:
        raise FlowMetaError(f"No FASTQ files found in {input_dir}")

    invalid = []
    for fp in files:
        name = fp.name
        if name.endswith(suffix1) or name.endswith(suffix2):
            continue
        invalid.append(name)

    if invalid:
        raise FlowMetaError(
            "Found FASTQ files not matching suffix requirements: " + ", ".join(invalid)
        )

    summarize_step(
        "Filename normalization",
        f"All FASTQ files match suffixes {suffix1}/{suffix2}",
        True,
    )


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Repository: https://github.com/SkinMicrobe/FlowMeta
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def load_kraken_db_to_shm(db_path, shm_path="/dev/shm/k2ppf"):
    """Copy the Kraken2 database into shared memory if not present."""
    required = ["hash.k2d", "opts.k2d", "taxo.k2d"]
    db_files = [os.path.join(db_path, f) for f in required]
    if not all(os.path.exists(f) for f in db_files):
        raise FlowMetaError(f"Kraken2 database incomplete at {db_path}")

    if all(os.path.exists(os.path.join(shm_path, f)) for f in required):
        log_info(f"Kraken2 DB already cached in {shm_path}")
        return shm_path

    log_info(f"Copying Kraken2 DB to {shm_path} for faster access")
    if os.path.exists(shm_path):
        shutil.rmtree(shm_path)
    shutil.copytree(db_path, shm_path)

    vmtouch = shutil.which("vmtouch")
    if vmtouch:
        try:
            subprocess.run([vmtouch, "-t", os.path.join(shm_path, "*.k2d")], check=False)
        except Exception:  # best effort
            log_warning("vmtouch preload failed; continuing without preload")
    else:
        log_warning("vmtouch not found; skipping shared-memory preload")
    return shm_path


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Repository: https://github.com/SkinMicrobe/FlowMeta
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def cleanup_kraken_db(shm_path="/dev/shm/k2ppf"):
    if os.path.exists(shm_path):
        log_info(f"Removing shared-memory DB at {shm_path}")
        shutil.rmtree(shm_path, ignore_errors=True)


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Repository: https://github.com/SkinMicrobe/FlowMeta
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def summarize_step(name, description, result):
    status = "✅" if result else "⚠️"
    log_info(f"{status} {name}: {description}")


def log_path_overview(paths, shm_path):
    """Print a concise overview of all key directories for this run."""
    ordered_keys = [
        ("raw", "01-raw"),
        ("qc", "02-qc"),
        ("hr", "03-hr"),
        ("bam", "04-bam"),
        ("host", "05-host"),
        ("kraken", "06-ku"),
        ("bracken", "07-bracken"),
        ("kraken_filtered", "08-ku2"),
        ("mpa", "09-mpa"),
    ]
    log_info("Path overview for this run:")
    for key, label in ordered_keys:
        log_info(f"  {label:<8} -> {paths[key]}")
    log_info(f"  shm_path -> {shm_path}")


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Repository: https://github.com/SkinMicrobe/FlowMeta
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def flowmeta_base(
    input_dir,
    output_dir,
    db_bowtie2,
    db_kraken,
    threads=32,
    batch_size=2,
    se=False,
    fastp_length_required=50,
    fastp_retries=3,
    host_retries=3,
    kraken_retries=3,
    copy_db_to_shm=True,
    shm_path="/dev/shm/k2ppf",
    min_count=4,
    suffix1=DEFAULT_SUFFIX1,
    suffix2=DEFAULT_SUFFIX2,
    skip_host_extract=False,
    force=False,
    project_prefix="",
    step=None,
    check_result=False,
):
    """Run the full 10-step pipeline end-to-end, or resume from a specific step."""
    print_colorful_message("===============================================", "blue")
    print_colorful_message(" flowmeta: Integrated Metagenomic Workflow ", "cyan")
    print_colorful_message(" Repository: https://github.com/SkinMicrobe/FlowMeta", "cyan")
    print_colorful_message("===============================================", "blue")

    if not os.path.isdir(input_dir):
        raise FlowMetaError(f"Input directory not found: {input_dir}")

    output_dir = ensure_dir(output_dir)
    helper_path = os.path.join(os.path.dirname(__file__), "helper")

    max_step = 10
    if step is None:
        start_step = 1
    else:
        try:
            start_step = int(step)
        except (TypeError, ValueError):
            raise FlowMetaError(f"--step must be an integer between 1 and {max_step}")
        if not 1 <= start_step <= max_step:
            raise FlowMetaError(f"--step must be between 1 and {max_step}")

    def should_run_step(step_number):
        return step_number >= start_step

    def should_run_check(step_number):
        return check_result and should_run_step(step_number)

    def log_step_skip(step_number, title):
        if step is not None and step_number < start_step:
            log_info(f"Skipping step {step_number} ({title}) because --step={start_step}")

    def log_validation_skip(step_number, title):
        log_info(f"Skipping step {step_number} ({title}) because check_result is disabled")

    paths = {
        "raw": input_dir,
        "qc": ensure_dir(os.path.join(output_dir, "02-qc")),
        "hr": ensure_dir(os.path.join(output_dir, "03-hr")),
        "bam": ensure_dir(os.path.join(output_dir, "04-bam")),
        "host": ensure_dir(os.path.join(output_dir, "05-host")),
        "kraken": ensure_dir(os.path.join(output_dir, "06-ku")),
        "bracken": ensure_dir(os.path.join(output_dir, "07-bracken")),
        "kraken_filtered": ensure_dir(os.path.join(output_dir, "08-ku2")),
        "mpa": ensure_dir(os.path.join(output_dir, "09-mpa")),
    }

    log_path_overview(paths, shm_path)

    def count_files(directory, pattern):
        return sum(1 for _ in Path(directory).glob(pattern))

    def count_files_with_patterns(directory, patterns):
        for pattern in patterns:
            count = count_files(directory, pattern)
            if count:
                return count
        return 0

    def count_fastq_inputs():
        return count_files(paths["raw"], f"*{suffix1}")

    def count_qc_tasks():
        return count_files(paths["qc"], "*.task.complete")

    def count_host_removed_reads():
        return count_files(paths["hr"], "*_host_remove_R1.fastq.gz")

    def count_bam_files():
        return count_files(paths["bam"], "*.bam")

    def count_kraken_reports():
        return count_files_with_patterns(
            paths["kraken"],
            ["*.kraken.report.std.txt", "*.kraken.report.txt"],
        )

    def count_filtered_mpa():
        return count_files(paths["kraken_filtered"], "*.nohuman.kraken.mpa.std.txt")

    def count_bracken_tables():
        return count_files(paths["kraken_filtered"], "*.bracken")

    def verify_start_step_requirements():
        if should_run_step(1):
            verify_fastq_naming(input_dir, suffix1, suffix2)
            return
        if start_step == 10:
            filtered_mpa = count_filtered_mpa()
            host_bracken = count_bracken_tables()
            missing = []
            if filtered_mpa == 0:
                missing.append(
                    f"no host-filtered MPA files (*.nohuman.kraken.mpa.std.txt) found in {paths['kraken_filtered']}"
                )
            if host_bracken == 0:
                missing.append(
                    f"no Bracken abundance tables (*.bracken) found in {paths['kraken_filtered']}"
                )
            if missing:
                raise FlowMetaError(
                    "Step 10 requires outputs from the host-filtered Kraken step, but they are missing: "
                    + "; ".join(missing)
                )
            log_info(
                f"Step 10 prerequisites satisfied: {filtered_mpa} host-filtered MPA files / "
                f"{host_bracken} Bracken tables detected"
            )

    def safe_count(counter_fn):
        if counter_fn is None:
            return "N/A"
        try:
            return counter_fn()
        except Exception as exc:  # pragma: no cover - defensive logging
            log_warning(f"Unable to count samples for step: {exc}")
            return "unknown"

    def announce_step(step_number, title, counter_fn=None):
        count_value = safe_count(counter_fn)
        count_text = count_value if count_value in ("N/A", "unknown") else str(count_value)
        log_info(
            f"Step {step_number}: {title} | samples ready: {count_text} | force={'ON' if force else 'OFF'}"
        )

    verify_start_step_requirements()

    # Step 1 & 2: fastp + validation loops
    if should_run_step(1):
        announce_step(1, "fastp quality control", count_fastq_inputs)
        if should_run_check(2):
            announce_step(2, "fastp integrity verification", count_qc_tasks)
        elif should_run_step(2):
            log_validation_skip(2, "fastp integrity verification")
        for attempt in range(1, fastp_retries + 1):
            log_info(f"Running fastp pass {attempt}/{fastp_retries}")
            run_fastp_qc(
                paths["raw"], paths["qc"],
                num_threads=threads,
                suffix1=suffix1,
                batch_size=batch_size,
                se=se,
                length_required=fastp_length_required,
                force=force,
            )
            if should_run_check(2):
                valid, invalid = check_fastp_results(paths["qc"], suffix1=suffix1)
                summarize_step("FASTP QC", "fastp + integrity checks", invalid == 0)
                if invalid == 0:
                    break
                if attempt == fastp_retries:
                    raise FlowMetaError("fastp outputs still invalid after retries")
            else:
                break
    else:
        log_step_skip(1, "fastp quality control")

    if should_run_check(2) and not should_run_step(1):
        announce_step(2, "fastp integrity verification", count_qc_tasks)
        valid, invalid = check_fastp_results(paths["qc"], suffix1=suffix1)
        summarize_step("FASTP QC", "fastp + integrity checks", invalid == 0)
        if invalid != 0:
            raise FlowMetaError("fastp outputs invalid; rerun Step 1 with --force")
    elif should_run_step(2) and not check_result:
        log_validation_skip(2, "fastp integrity verification")
    elif not should_run_step(2):
        log_step_skip(2, "fastp integrity verification")

    # Step 3 & 4: Bowtie2 host removal and validation
    if should_run_step(3):
        announce_step(3, "Bowtie2 host removal", count_qc_tasks)
        if should_run_check(4):
            announce_step(4, "Host removal integrity check", count_host_removed_reads)
        elif should_run_step(4):
            log_validation_skip(4, "Host removal integrity check")
        for attempt in range(1, host_retries + 1):
            log_info(f"Removing host pass {attempt}/{host_retries}")
            run_remove_host(
                paths["qc"], paths["hr"], paths["bam"],
                db_bowtie2, threads=threads,
                suffix1=suffix1, suffix2=suffix2,
                force=force,
            )
            if should_run_check(4):
                valid, invalid = check_host_remove_results(paths["hr"])
                summarize_step("Host removal", "Bowtie2 + HR integrity", invalid == 0)
                if invalid == 0:
                    break
                if attempt == host_retries:
                    raise FlowMetaError("Host removal outputs invalid after retries")
            else:
                break
    else:
        log_step_skip(3, "Bowtie2 host removal")

    if should_run_check(4) and not should_run_step(3):
        announce_step(4, "Host removal integrity check", count_host_removed_reads)
        valid, invalid = check_host_remove_results(paths["hr"])
        summarize_step("Host removal", "Bowtie2 + HR integrity", invalid == 0)
        if invalid != 0:
            raise FlowMetaError("Host removal outputs invalid; rerun Step 3 with --force")
    elif should_run_step(4) and not check_result:
        log_validation_skip(4, "Host removal integrity check")
    elif not should_run_step(4):
        log_step_skip(4, "Host removal integrity check")

    # Step 5: Extract host reads for HLA/mtDNA
    if skip_host_extract:
        log_warning("Skipping host-read extraction step (samtools disabled)")
    elif should_run_step(5):
        announce_step(5, "Host-read extraction (samtools fastq)", count_bam_files)
        run_extract_host(
            paths["bam"], paths["host"],
            mode="mapped_anypair",
            samtools_threads=threads,
            pigz_threads=threads,
            force=force,
        )
        summarize_step("Host reads", "Samtools fastq extraction", True)
    else:
        log_step_skip(5, "Host-read extraction (samtools fastq)")

    # Step 6: Prepare Kraken DB
    kraken_db_path = db_kraken
    kraken_db_cached = False
    if copy_db_to_shm and should_run_step(6):
        announce_step(6, "Prepare Kraken2 DB (shared memory staging)")
        kraken_db_path = load_kraken_db_to_shm(db_kraken, shm_path=shm_path)
        kraken_db_cached = True
    elif copy_db_to_shm and not should_run_step(6):
        log_step_skip(6, "Prepare Kraken2 DB (shared memory staging)")

    # Step 7 & 8: Kraken classification + validation loops
    helper_itm = helper_path
    if should_run_step(7):
        announce_step(7, "Kraken2/Bracken classification", count_host_removed_reads)
        if should_run_step(8):
            announce_step(8, "Kraken report validation", count_kraken_reports)
        for attempt in range(1, kraken_retries + 1):
            log_info(f"Kraken/Bracken pass {attempt}/{kraken_retries}")
            run_kraken_bracken(
                paths["hr"], paths["kraken"], paths["bracken"],
                db_kraken=kraken_db_path,
                helper_path=helper_itm,
                batch_size=batch_size,
                num_threads=threads,
                se=se,
                force=force,
            )
            if should_run_step(8):
                valid, invalid = check_kraken_results(paths["kraken"])
                summarize_step("Kraken", "Classification + report checks", invalid == 0)
                if invalid == 0:
                    break
                if attempt == kraken_retries:
                    raise FlowMetaError("Kraken outputs invalid after retries")
            else:
                break
    else:
        log_step_skip(7, "Kraken2/Bracken classification")

    if should_run_step(8) and not should_run_step(7):
        announce_step(8, "Kraken report validation", count_kraken_reports)
        valid, invalid = check_kraken_results(paths["kraken"])
        summarize_step("Kraken", "Classification + report checks", invalid == 0)
        if invalid != 0:
            raise FlowMetaError("Kraken outputs invalid; rerun Step 7 with --force")
    elif not should_run_step(8):
        log_step_skip(8, "Kraken report validation")

    # Step 9: Remove host taxa from reports (Kraken2 second pass)
    if should_run_step(9):
        announce_step(9, "Kraken host cleanup (remove human taxa)", count_kraken_reports)
        run_remove_host_counts(
            paths["kraken"], paths["kraken_filtered"], kraken_db_path,
            helper_path=helper_itm,
            batch_size=batch_size,
            min_count=min_count,
            force=force,
        )
        summarize_step("Kraken host cleanup", "Filter human taxa + rerun Bracken", True)
    else:
        log_step_skip(9, "Kraken host cleanup (remove human taxa)")

    # Step 10: Merge everything into OTU/MPA matrices
    if should_run_step(10):
        if run_merge_step is None:
            detail = f" ({STEP6_IMPORT_ERROR})" if STEP6_IMPORT_ERROR else ""
            raise FlowMetaError(
                "step6_merge_results requires optional dependencies (pandas, numpy). "
                "Install them to enable the final merge step." + detail
            )
        announce_step(
            10,
            "Merge Kraken/Bracken outputs into OTU/MPA matrices",
            lambda: f"{count_filtered_mpa()} MPA / {count_bracken_tables()} Bracken",
        )
        run_merge_step(
            paths["kraken_filtered"],
            paths["kraken_filtered"],
            paths["mpa"],
            helper_path=helper_itm,
            mpa_suffix=".nohuman.kraken.mpa.std.txt",
            report_suffix=".nohuman.kraken.report.std.txt",
            force=force,
            prefix=project_prefix,
        )
        summarize_step("Merge", "Combine Kraken/Bracken tables", True)
    else:
        log_step_skip(10, "Merge Kraken/Bracken outputs into OTU/MPA matrices")

    # Cleanup DB from RAM if requested
    if copy_db_to_shm and kraken_db_cached:
        cleanup_kraken_db(shm_path)

    log_success("flowmeta pipeline finished successfully")
    return paths
