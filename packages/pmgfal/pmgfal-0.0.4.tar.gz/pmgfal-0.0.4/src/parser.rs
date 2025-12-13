//! lexicon file parsing

use std::fs;
use std::io;
use std::path::Path;

use atrium_lex::LexiconDoc;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ParseError {
    #[error("not a directory: {0}")]
    NotADirectory(String),

    #[error("io error: {0}")]
    Io(#[from] io::Error),

}

/// parse all lexicon files from a directory recursively
pub fn parse_lexicons(dir: &Path) -> Result<Vec<LexiconDoc>, ParseError> {
    if !dir.is_dir() {
        return Err(ParseError::NotADirectory(dir.display().to_string()));
    }

    let mut docs = Vec::new();
    visit_dir(dir, &mut docs)?;
    docs.sort_by(|a, b| a.id.cmp(&b.id));
    Ok(docs)
}

fn visit_dir(dir: &Path, docs: &mut Vec<LexiconDoc>) -> Result<(), ParseError> {
    for entry in fs::read_dir(dir)? {
        let path = entry?.path();

        if path.is_dir() {
            visit_dir(&path, docs)?;
        } else if path.extension().is_some_and(|e| e == "json") {
            let content = fs::read_to_string(&path)?;

            // skip non-lexicon json files silently
            if let Ok(doc) = serde_json::from_str::<LexiconDoc>(&content) {
                docs.push(doc);
            }
        }
    }
    Ok(())
}
