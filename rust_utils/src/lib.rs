use pyo3::prelude::*;
use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader};

#[pyclass]
struct FastModerator {
    bad_words: HashSet<String>,
}

#[pymethods]
impl FastModerator {
    #[new]
    fn new(file_path: String) -> PyResult<Self> {
        let file = File::open(file_path)?;
        let reader = BufReader::new(file);
        let mut bad_words = HashSet::new();

        for line in reader.lines() {
            if let Ok(word) = line {
                bad_words.insert(word.trim().to_lowercase());
            }
        }
        Ok(FastModerator { bad_words })
    }

    fn check_message(&self, text: &str) -> bool {
        // High-speed native string processing
        let clean_text = text.to_lowercase();
        clean_text.split_whitespace().any(|word| {
            let stripped = word.trim_matches(|c: char| !c.is_alphanumeric());
            self.bad_words.contains(stripped)
        })
    }
}

#[pymodule]
fn rust_utils(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<FastModerator>()?;
    Ok(())
}