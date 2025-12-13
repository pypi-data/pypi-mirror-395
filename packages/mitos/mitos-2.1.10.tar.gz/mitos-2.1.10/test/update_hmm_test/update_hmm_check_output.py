from pathlib import Path

output_dir = Path("test/update_hmm_test/output")

# Check essential outputs
expected_files = [
    output_dir / "all_sequences.fas",
    output_dir / "all_hmms.db",
    output_dir / "all_features_hmmsearch_best.tbl",
    output_dir / "plots" / "best_evalues.dat",
    output_dir / "plots" / "discarded_evalues.dat",
    output_dir / "plots" / "gap_fractions.dat",
    output_dir / "plots" / "dist_evalues.png",
    output_dir / "plots" / "gapfractions_per_feature.png",
    output_dir / "plots" / "gapfractions_sum.png",
    output_dir / "logs" / "cross_hits.fas",
    output_dir / "logs" / "unmatched_sequences.fas",
    output_dir / "logs" / "getfeatures.log",
]
for file in expected_files:
    assert file.exists(), f"Missing expected file: {file}"
