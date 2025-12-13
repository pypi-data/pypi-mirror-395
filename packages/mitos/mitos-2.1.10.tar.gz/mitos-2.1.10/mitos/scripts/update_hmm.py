#!/usr/bin/venv python

"""
@author: St. Boelsche

This script processes protein sequences from GenBank files and existing HMM
models to generate updated HMM profiles. It performs the following steps:

1. Extracts protein sequences from GenBank files and logs any missing or empty entries.
2. Concatenates all HMM models into a single database.
3. Runs hmmsearch to identify matches between sequences and HMMs.
4. Filters hits to keep only the best match per sequence.
5. Generates alignment files for filtered sequences using hmmalign.
6. Builds updated HMM profiles from these alignments and prepares them with hmmpress.
7. Produces analysis output such as unmatched sequences, cross-hits and plots for visualization.

Outputs:
    - Combined and per-gene FASTA files
    - HMMER tblout files (all hits and filtered best hits)
    - Unmatched sequences and cross-hits FASTA files
    - Updated HMM profiles
    - Alignment files in Stockholm format
    - E-value and gap fraction plots
    - Logs of warnings and errors during extraction

Dependencies:
    - BioPython, typing_extensions
    - HMMER suite (hmmsearch, hmmalign, hmmbuild, hmmpress)
    - R scripts for plotting: mitos/plot_evalues.R, mitos/plot_gapfractions.R

for help on usage, run:
    update_hmm.py --help
"""

import argparse
import importlib.resources as resources
import subprocess
from collections import defaultdict
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from Bio import AlignIO
from typing_extensions import TypedDict

from mitos import util
from mitos.scripts import getfeatures


class Hit(TypedDict):
    """
    Data structure for a single HMMER-hit.
    Necessary for type checking with mypy.
    """

    target: str
    query: str
    evalue: float
    score: float
    line: str


def extract_protein_sequences(
    gb_files: List[Path], log_dir: Path
) -> Dict[str, List[str]]:
    """
    Extract protein sequences from GenBank files using getfeatures.
    Skips entries with empty translation or missing header.

    Args:
        gb_files: List of GenBank file paths.
        log_dir: Directory to write getfeatures log file.

    Returns:
        Mapping from gene_name (lowercase) to list of FASTA entries.
    """
    gene_sequences: Dict[str, List[str]] = {}
    format_string = "%a|%name|%start|%stop\n%trans\n"
    log_file = log_dir / "getfeatures.log"

    with log_file.open("w") as log_handle:
        for gb_file in gb_files:
            argv = ["-p", "gene", "-f", format_string, str(gb_file)]
            try:
                options, args = getfeatures.parse_args(argv)
                # redirect stdout and stderr to log file
                with redirect_stdout(log_handle), redirect_stderr(log_handle):
                    result = getfeatures.run(options, args)
            except Exception as e:
                print(f"Error running getfeatures on {gb_file}: {e}")
                continue

            # Skip empty output
            if not result.strip():
                print(f"Warning: no protein features found in {gb_file}")
                continue

            output_lines: List[str] = result.strip().split("\n")

            for i in range(0, len(output_lines), 2):
                # alternating header and protein sequence
                header: str = output_lines[i].strip()
                seq: str = (
                    output_lines[i + 1].strip() if i + 1 < len(output_lines) else ""
                )

                # Skip entries with empty header or empty sequence
                if not header:
                    print(f"Warning: empty header in {gb_file}, skipping entry")
                    continue
                if not seq:
                    print(
                        f"Warning: empty translation for header '{header}' in {gb_file}, skipping entry"
                    )
                    continue

                gene_name = header.split("|")[1].lower()
                entry = f">{header}\n{seq}\n"
                gene_sequences.setdefault(gene_name, []).append(entry)

    return gene_sequences


def concatenate_files(input_dir: Path, output_file: Path, extension: str) -> None:
    """
    Concatenate all files with a given extension in a directory into a single file.

    Args:
        input_dir: Path object of the directory containing files to concatenate
        output_file: Path object to write the combined file
        extension: File extension to filter for (e.g., '.gb', '.hmm')
    """
    files_to_concat: List[Path] = [
        file_path
        for file_path in sorted(input_dir.glob(f"*{extension}"))
        if file_path.resolve()
        != output_file.resolve()  # Ignore the output file, if it is in the input directory
    ]
    if not files_to_concat:
        raise RuntimeError(f"No files with extension {extension} found in {input_dir}")

    with output_file.open("w") as out_handle:
        for file_path in files_to_concat:
            with file_path.open("r") as f_handle:
                out_handle.write(f_handle.read())
                out_handle.write("\n")

    print(f"All {extension} files in {input_dir} concatenated into {output_file}")


def run_hmmsearch(
    fasta_file: Path,
    hmm_db: Path,
    tbl_file: Path,
    evalue: Optional[float] = None,
    score: Optional[float] = None,
    cpu: Optional[int] = None,
) -> None:
    """Run hmmsearch for a FASTA file against the HMM database and save tabular output."""
    cmd = [
        "hmmsearch",
        "--tblout",
        str(tbl_file),
    ]
    if evalue is not None:
        cmd.extend(["-E", str(evalue)])
    if score is not None:
        cmd.extend(["-T", str(score)])
    if cpu is not None:
        cmd.extend(["--cpu", str(cpu)])

    cmd.extend([str(hmm_db), str(fasta_file)])

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

    print(f"hmmsearch completed for {fasta_file}")


def parse_tblout(tbl_file: Path) -> Tuple[List[str], List[str], List[Hit]]:
    """
    Parse a HMMER --tblout file.

    Returns:
        header_lines: first 3 comment lines
        footer_lines: remaining comment lines at the end
        hits: list of dicts with keys:
              'target', 'query', 'evalue', 'score', 'line'
    """
    header_lines: List[str] = []
    footer_lines: List[str] = []
    hits: List[Hit] = []
    line_count: int = 0

    with tbl_file.open() as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("#") or not line.strip():
                # First 3 comment lines = header
                if line.startswith("#") and line_count < 3:
                    header_lines.append(line)
                else:
                    footer_lines.append(line)
                line_count += 1
                continue

            parts = line.split()
            hit: Hit = {
                "target": parts[0],
                "query": parts[2],
                "evalue": float(parts[4]),
                "score": float(parts[5]),
                "line": line,
            }
            hits.append(hit)

    if not hits:
        raise RuntimeError(f"No hits found in {tbl_file}")

    return header_lines, footer_lines, hits


def filter_best_per_target(hits: List[Hit]) -> Tuple[List[Hit], List[Hit]]:
    """
    Keep only the best hit (lowest evalue) per target.
    In the case of a tie, keep the hit with the highest score.

    Args:
        hits: list of dicts with keys 'target', 'query', 'evalue', 'score', 'line'

    Returns:
        list of dicts with only the best hit per target, sorted by query and evalue
    """
    best_hits: Dict[str, Hit] = {}
    discarded_hits: List[Hit] = []

    for hit in hits:
        target = hit["target"]
        if target not in best_hits:
            best_hits[target] = hit
        else:
            best = best_hits[target]
            # Compare by evalue first, then by score
            if (hit["evalue"] < best["evalue"]) or (
                hit["evalue"] == best["evalue"] and hit["score"] > best["score"]
            ):
                # old best hit gets discarded
                discarded_hits.append(best)
                # new best hit
                best_hits[target] = hit
            else:
                # hit gets discarded
                discarded_hits.append(hit)

    # Sort by query and evalue
    best_hits_sorted = sorted(
        list(best_hits.values()), key=lambda x: (x["query"], x["evalue"])
    )

    return best_hits_sorted, discarded_hits


def write_tblout(
    output_file: Path,
    header_lines: List[str],
    footer_lines: List[str],
    hits: List[Hit],
) -> None:
    """
    Write a HMMER --tblout file, preserving header, original lines, and footer.
    """
    with output_file.open("w") as out:
        for c in header_lines:
            out.write(c + "\n")
        for hit in hits:
            out.write(hit["line"] + "\n")
        for c in footer_lines:
            out.write(c + "\n")


def analyze_matches(
    hits_best: List[Hit], gene_sequences: Dict[str, List[str]], output_dir: Path
) -> None:
    """
    Compare best_hits with gene_sequences and collect:
      1. All sequences without a match (unmatched_sequences.fas)
      2. All cross-hits where feature != query (cross_hits.fas)
         As this function is run after filtering for best hits,
         the remaining cross-hits are those, where a foreign HMM produced a better match.

    Args:
        hits_best: list of dicts with keys 'target', 'query', 'evalue', 'score', 'line'
        gene_sequences: dict with feature name as key and list of headers + sequences as value
    """

    matched_targets = {hit["target"] for hit in hits_best}

    # --- Unmatched sequences ---
    unmatched = []
    for feature, entries in gene_sequences.items():
        for entry in entries:
            header = entry.split("\n", 1)[0][1:]  # remove '>'
            if header not in matched_targets:
                unmatched.append(entry)

    if unmatched:
        unmatched_file = output_dir / "unmatched_sequences.fas"
        with unmatched_file.open("w") as f:
            for entry in unmatched:
                f.write(entry)
        print(f"{len(unmatched)} unmatched sequences written to {unmatched_file}")

    # --- Cross-hits ---
    cross_hits = []
    for hit in hits_best:
        target = hit["target"]
        query = hit["query"]

        # Feature = gene name (second field in header)
        feature = target.split("|")[1].lower() if "|" in target else "unknown"

        if feature != query:
            # Find sequence belonging to this target
            for entry in gene_sequences.get(feature, []):
                header = entry.split("\n", 1)[0][1:]  # remove '>'
                seq = entry.split("\n", 1)[1]
                if header == target:
                    # Append note to header about the HMM it matched
                    new_header = f">{header}|matched_with={query}"
                    cross_hits.append(f"{new_header}\n{seq}")
                    break

    if cross_hits:
        cross_file = output_dir / "cross_hits.fas"
        with cross_file.open("w") as f:
            for entry in cross_hits:
                f.write(entry)
        print(f"{len(cross_hits)} cross-hit sequences written to {cross_file}")


def load_fasta(fasta_file: Path) -> Dict[str, str]:
    """
    Load a FASTA file into a dict {header: sequence}.
    """
    seqs: Dict[str, str] = {}
    with fasta_file.open() as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                header = line[1:].split()[0]
                seqs[header] = ""
            else:
                seqs[header] += line
    return seqs


def run_hmmalign(
    hits_best: List[Hit],
    all_sequences: Path,
    output_dir: Path,
    hmm_dir: Path,
) -> List[Path]:
    """
    Build per-feature alignments with hmmalign in Stockholm format,
    using only the filtered hits from hits_best.

    Args:
        hits_best: list of dicts with keys 'target', 'query', ...
        all_sequences: path to combined FASTA file containing all sequences
        output_dir: directory for writing filtered FASTA and final alignments
        hmm_dir: directory containing the HMM models

    Returns:
        List of successfully created Stockholm alignment files
    """
    # Load all sequences once
    seqs: Dict[str, str] = load_fasta(all_sequences)

    # Group targets by query
    grouped = defaultdict(list)
    for hit in hits_best:
        grouped[hit["query"]].append(hit["target"])

    # list of created alignment files
    created_alignments: List[Path] = []

    for query, targets in grouped.items():
        # Write filtered FASTA for this feature
        seq_file = output_dir / f"{query}_filtered.fas"
        with seq_file.open("w") as f:
            for t in targets:
                if t not in seqs:
                    print(f"Warning: target {t} not found in {all_sequences}")
                    continue
                f.write(f">{t}\n{seqs[t]}\n")

        hmm_file = hmm_dir / f"{query}.db"
        aln_out = output_dir / f"{query}_alignment.sto"

        if not hmm_file.exists():
            print(f"No HMM model for {query} in {hmm_file}")
            continue

        cmd = [
            "hmmalign",
            "--amino",
            "-o",
            str(aln_out),
            str(hmm_file),
            str(seq_file),
        ]
        subprocess.run(cmd, check=True)
        print(f"Alignment for {query} written to {aln_out}")

        created_alignments.append(aln_out)

    return created_alignments


def build_new_hmms(
    alignment_files: List[Path], new_hmm_dir: Path, cpu: Optional[int] = None
) -> None:
    """
    Build new HMMs from a list of existing Stockholm alignments.

    Args:
        alignment_files: list of Path objects pointing to Stockholm alignment files
    """
    for aln_file in alignment_files:
        if not aln_file.exists():
            print(f"Warning: {aln_file} not found, skipping")
            continue

        feature_name = aln_file.stem.replace("_alignment", "")
        filtered_alignment_file = aln_file.with_name(f"{aln_file.stem}_filtered.sto")
        hmm_out = new_hmm_dir / f"{feature_name}.db"

        cmd = [
            "hmmbuild",
            "--amino",
            "--hand",  # define consensus columns using reference annotation of the alignment
            "-n",
            feature_name,
            "-O",
            str(filtered_alignment_file),
        ]
        if cpu is not None:
            cmd.extend(["--cpu", str(cpu)])

        cmd.extend([str(hmm_out), str(aln_file)])

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        print(f"New HMM for {feature_name} written to {hmm_out}")
        # run hmmpress on the new HMM
        press_hmm(hmm_out)


def press_hmm(hmm: Path) -> None:
    """
    Run hmmpress on a given HMM.
    This creates binary compressed data files needed to run hmmscan.
    (hmmscan is not used in this script, but RefSeq stores HMMs this way.)
    """
    cmd = ["hmmpress", "-f", str(hmm)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def write_evalues(hits: List[Hit], outfile: Path) -> None:
    """Write e-values to a file."""
    with outfile.open("w") as f:
        for hit in hits:
            f.write(f"{hit['evalue']}\n")


def analyze_alignments(output_dir: Path, plot_dir: Path) -> Path:
    """
    Analyze all *_filtered.sto alignments, calculate gap fractions per column,
    and write a tab-separated .dat file for plotting in R.
    """
    out_file = plot_dir / "gap_fractions.dat"
    with out_file.open("w") as f:
        # header
        f.write("feature\tcolumn\trf\tgap_fraction\n")

        for aln_file in sorted(output_dir.glob("*alignment_filtered.sto")):
            feature = aln_file.stem.replace("_alignment_filtered", "")
            aln = AlignIO.read(aln_file, "stockholm")
            nseq = len(aln)

            # Reference line should always exist
            rf_line = aln.column_annotations["reference_annotation"]

            for i in range(aln.get_alignment_length()):
                col = aln[:, i]
                nongaps = sum(1 for c in col if c not in ("-", ".", "~"))
                gaps = nseq - nongaps
                gap_fraction = gaps / nseq
                rf = "x" if rf_line[i] == "x" else "no_x"

                f.write(f"{feature}\t{i+1}\t{rf}\t{gap_fraction:.4f}\n")

    print(f"Wrote gap fraction results to {out_file}")
    return out_file


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Update HMMs from GenBank files",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    exclusive = optional.add_mutually_exclusive_group()

    required.add_argument(
        "-gb",
        required=True,
        type=Path,
        metavar="DIR",
        help="Directory containing GenBank files.\nAll .gb files will be used.",
    )
    required.add_argument(
        "-hm",
        required=True,
        type=Path,
        metavar="DIR",
        help="Directory containing HMM models.\nAll .db files will be used.",
    )
    required.add_argument(
        "-o",
        required=True,
        type=Path,
        metavar="DIR",
        help="Output directory (will be created if missing)",
    )
    optional.add_argument(
        "-c",
        "--cpu",
        type=int,
        metavar="NCPU",
        help="Number of CPUs to use (sets HMMER_NCPU). Default: 2",
    )
    exclusive.add_argument(
        "-E",
        type=float,
        metavar="<x>",
        help="Set reporting threshold for hmmsearch (E-value). Default: 10\nOnly hits with E-values <= <x> are used.",
    )
    exclusive.add_argument(
        "-T",
        type=float,
        metavar="<x>",
        help="Set reporting threshold for hmmsearch (bitscore).\nOnly hits with bitscore >= <x> are used.",
    )
    args = parser.parse_args()

    # get absolute paths from given command line parameters
    gb_dir: Path = args.gb.resolve()
    output_dir: Path = args.o.resolve()
    hmm_dir: Path = args.hm.resolve()

    if not gb_dir.is_dir():
        raise FileNotFoundError(
            f"gb_dir does not exist or is not a directory: {gb_dir}"
        )
    if not hmm_dir.is_dir():
        raise FileNotFoundError(
            f"hmm_dir does not exist or is not a directory: {hmm_dir}"
        )
    # Create output directories if they do not exist
    output_dir.mkdir(parents=True, exist_ok=True)
    new_hmm_dir = output_dir / "new_hmms"
    new_hmm_dir.mkdir(parents=True, exist_ok=True)
    plot_dir = output_dir / "plots"
    plot_dir.mkdir(parents=True, exist_ok=True)
    log_dir = output_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    if args.cpu:
        print(f"Using {args.cpu} CPUs")

    # Find all GenBank files in the directory
    print("Collecting protein sequences from GenBank files...")
    gb_files: List[Path] = sorted(gb_dir.glob("*.gb"))
    if not gb_files:
        raise RuntimeError(f"No .gb files found in {gb_dir}")

    # Extract protein sequences from GenBank files
    gene_sequences: Dict[str, List[str]] = extract_protein_sequences(gb_files, log_dir)

    # Write all sequences to a single file and also to separate files
    combined_fas_file: Path = output_dir / "all_sequences.fas"

    with combined_fas_file.open("w") as all_handle:
        for gene_name, entries in gene_sequences.items():
            output_file: Path = output_dir / f"{gene_name}_sequences.fas"
            with output_file.open("w") as out_handle:
                out_handle.writelines(entries)
            all_handle.writelines(entries)

    print("All protein sequences collected successfully.")

    # combine all HMMs into a single file
    all_hmms_file = output_dir / "all_hmms.db"
    concatenate_files(hmm_dir, all_hmms_file, ".db")

    # Run hmmsearch for all sequences and all HMMs
    tbl_file: Path = output_dir / "all_features_hmmsearch.tbl"
    run_hmmsearch(combined_fas_file, all_hmms_file, tbl_file, args.E, args.T, args.cpu)

    # Parse hmmsearch table
    header, footer, hits_all = parse_tblout(tbl_file)

    # Filter to keep only the best hit per target, this will remove most cross-hits
    hits_discarded: List[Hit] = []
    hits_best, hits_discarded = filter_best_per_target(hits_all)

    # Write filtered table, preserving original format
    output_tbl = output_dir / "all_features_hmmsearch_best.tbl"
    write_tblout(output_tbl, header, footer, hits_best)
    print(f"Filtered table written to {output_tbl}")

    # analyze the filtered hits to find unmatched sequences and remaining cross-hits
    analyze_matches(hits_best, gene_sequences, log_dir)

    # Export e-values to files
    best_evalue_file = plot_dir / "best_evalues.dat"
    write_evalues(hits_best, best_evalue_file)
    discarded_evalue_file = plot_dir / "discarded_evalues.dat"
    write_evalues(hits_discarded, discarded_evalue_file)

    # get path to mitos directory
    with resources.path("mitos", "") as mitos_dir:
        mitos_dir = Path(mitos_dir)

    # Create plot of e-values
    cmd = [
        str(mitos_dir / "plot_evalues.R"),
        str(best_evalue_file),
        str(discarded_evalue_file),
        str(plot_dir),
        "dist_evalues.png",
        "Distribution of HMMER E-values",
    ]
    util.execute(cmd, supress_warning=True)

    print("E-value plot created.")

    # Build Stockholm alignments per feature using only filtered hits
    alignment_files = run_hmmalign(hits_best, combined_fas_file, output_dir, hmm_dir)

    # Build new HMMs from Stockholm alignments
    build_new_hmms(alignment_files, new_hmm_dir, args.cpu)

    # Analyze alignments and create gap fraction data file
    gap_file = analyze_alignments(output_dir, plot_dir)

    # create plots of gap fractions
    cmd = [str(mitos_dir / "plot_gapfractions.R"), str(gap_file), str(plot_dir)]
    util.execute(cmd, supress_warning=True)
    print("Gap-fraction plots created.")


if __name__ == "__main__":
    main()
