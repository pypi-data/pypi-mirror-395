"""Command-line interface for flowmeta pipeline."""

import argparse
import json
import sys
from pathlib import Path
from .flowmeta_base import flowmeta_base, DEFAULT_SUFFIX1, DEFAULT_SUFFIX2


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def build_parser():
	parser = argparse.ArgumentParser(
		prog="flowmeta_base",
		description="Run the integrated flowmeta metagenomic pipeline"
	)
	parser.add_argument("--input_dir", required=True, help="Directory containing raw FASTQ files")
	parser.add_argument("--output_dir", required=True, help="Directory to write pipeline outputs")
	parser.add_argument("--db_bowtie2", required=True, help="Path prefix to Bowtie2 host index")
	parser.add_argument("--db_kraken", required=True, help="Path to Kraken2 database")
	parser.add_argument("--threads", type=int, default=32, help="Threads per process (default: 32)")
	parser.add_argument("--batch", type=int, default=2, help="Samples processed in parallel (default: 2)")
	parser.add_argument("--se", action="store_true", help="Treat input as single-end data")
	parser.add_argument("--fastp_retries", type=int, default=3, help="Retries for fastp step")
	parser.add_argument("--host_retries", type=int, default=3, help="Retries for Bowtie2 step")
	parser.add_argument("--kraken_retries", type=int, default=3, help="Retries for Kraken step")
	parser.add_argument("--fastp_length_required", type=int, default=50, help="fastp --length_required value")
	parser.add_argument("--min_count", type=int, default=4, help="Bracken minimum read count cut-off")
	parser.add_argument("--suffix1", default=DEFAULT_SUFFIX1, help="Suffix for read 1 FASTQ files")
	parser.add_argument("--suffix2", default=DEFAULT_SUFFIX2, help="Suffix for read 2 FASTQ files")
	parser.add_argument("--skip_host_extract", action="store_true", help="Skip samtools host-read extraction")
	parser.add_argument("--force", action="store_true", help="Force re-run even when .task.complete exists")
	parser.add_argument("--project_prefix", default="", help="Prefix to add to merged outputs (Step 6)")
	parser.add_argument("--no_shm", action="store_true", help="Disable copying Kraken DB to shared memory")
	parser.add_argument("--shm_path", default="/dev/shm/k2ppf", help="Shared-memory path for Kraken DB copy")
	parser.add_argument("--check_result", action="store_true", help="Enable integrity checks (steps 2 and 4)")
	parser.add_argument("--dry_run", action="store_true", help="Print settings and exit without running")
	parser.add_argument("--print_config", action="store_true", help="Print the parsed configuration as JSON")
	parser.add_argument(
		"--step",
		type=int,
		help="Resume from a logical pipeline step (1-10). Leave unset to run the entire workflow.",
	)
	return parser


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def main(argv=None):
	parser = build_parser()
	args = parser.parse_args(argv)

	config = {
		"input_dir": args.input_dir,
		"output_dir": args.output_dir,
		"db_bowtie2": args.db_bowtie2,
		"db_kraken": args.db_kraken,
		"threads": args.threads,
		"batch_size": args.batch,
		"se": args.se,
		"fastp_length_required": args.fastp_length_required,
		"fastp_retries": args.fastp_retries,
		"host_retries": args.host_retries,
		"kraken_retries": args.kraken_retries,
		"copy_db_to_shm": not args.no_shm,
		"shm_path": args.shm_path,
		"min_count": args.min_count,
		"suffix1": args.suffix1,
		"suffix2": args.suffix2,
		"skip_host_extract": args.skip_host_extract,
		"force": args.force,
		"project_prefix": args.project_prefix,
		"step": args.step,
		"check_result": args.check_result,
	}

	if args.print_config:
		json.dump(config, sys.stdout, indent=2)
		sys.stdout.write("\n")

	if args.dry_run:
		return 0

	# expand and validate paths early for friendlier errors
	for key in ("input_dir", "output_dir", "db_bowtie2", "db_kraken"):
		config[key] = str(Path(config[key]).expanduser())

	flowmeta_base(**config)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
