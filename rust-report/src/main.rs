use serde::Deserialize;
use std::{env, error::Error};

#[derive(Debug, Deserialize)]
struct ReportRow {
    strategy: String,
    window: String,
    observations: usize,
    median_end_return: f64,
    window_loss_probability: f64,
    probability_below_bil: f64,
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = env::args().skip(1);

    let csv_path = args
        .next()
        .unwrap_or_else(|| "outputs/historical_etf_comparison.csv".to_string());

    let window = args.next().unwrap_or_else(|| "6-9 months".to_string());

    if args.next().is_some() {
        return Err("Usage: money-report [CSV_PATH] [WINDOW]".into());
    }

    let mut reader = csv::Reader::from_path(&csv_path)?;
    let rows: Vec<ReportRow> = reader.deserialize().collect::<Result<_, _>>()?;

    let selected: Vec<&ReportRow> = rows.iter().filter(|row| row.window == window).collect();

    if selected.is_empty() {
        return Err(format!("No results found for withdrawal window: {window}").into());
    }

    println!("Withdrawal window: {window}");
    println!("Historical frequencies; before taxes and inflation.\n");

    println!(
        "{:<34} {:>6} {:>11} {:>13} {:>12}",
        "Strategy", "Obs.", "Median", "Window loss", "Below BIL"
    );

    for row in selected {
        println!(
            "{:<34} {:>6} {:>10.1}% {:>12.1}% {:>11.1}%",
            row.strategy,
            row.observations,
            row.median_end_return * 100.0,
            row.window_loss_probability * 100.0,
            row.probability_below_bil * 100.0,
        );
    }

    Ok(())
}
