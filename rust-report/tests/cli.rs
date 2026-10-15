use std::{path::PathBuf, process::Command};

fn fixture_path() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("tests")
        .join("fixtures")
        .join("comparison.csv")
}

#[test]
fn prints_only_the_requested_window() {
    let output = Command::new(env!("CARGO_BIN_EXE_money-report"))
        .arg(fixture_path())
        .arg("6-9 months")
        .output()
        .expect("Could not run money-report");

    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );

    let stdout = String::from_utf8(output.stdout).unwrap();

    assert!(stdout.contains("Withdrawal window: 6-9 months"));
    assert!(!stdout.contains("Other window"));

    let row = stdout
        .lines()
        .find(|line| line.starts_with("Synthetic stock, test"))
        .expect("Requested strategy was missing");

    let values: Vec<&str> = row.split_whitespace().collect();
    assert_eq!(&values[3..], &["12", "5.0%", "25.0%", "30.0%"]);
}

#[test]
fn rejects_an_unknown_window() {
    let output = Command::new(env!("CARGO_BIN_EXE_money-report"))
        .arg(fixture_path())
        .arg("99 months")
        .output()
        .expect("Could not run money-report");

    assert!(!output.status.success());
    assert!(
        String::from_utf8_lossy(&output.stderr)
            .contains("No results found for withdrawal window: 99 months")
    );
}

#[test]
fn rejects_extra_arguments() {
    let output = Command::new(env!("CARGO_BIN_EXE_money-report"))
        .arg(fixture_path())
        .args(["6-9 months", "extra"])
        .output()
        .expect("Could not run money-report");

    assert!(!output.status.success());
    assert!(String::from_utf8_lossy(&output.stderr).contains("Usage:"));
}
