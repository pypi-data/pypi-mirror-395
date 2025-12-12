mod closest_string;
mod parser;
mod yale_departments;

use anyhow::{Context, Result};
use parser::{MQLParser, Rule};
use pest::Parser;

use crate::parser::MQLQueryFile;

#[derive(Debug, Clone)]
pub struct ParseResult {
    parsed_mql_file: MQLQueryFile,
}

impl ParseResult {
    pub fn to_string_pretty(&self) -> Result<String, serde_json::Error> {
        serde_json::to_string_pretty(&self.parsed_mql_file)
    }

    pub fn to_string(&self) -> Result<String, serde_json::Error> {
        serde_json::to_string(&self.parsed_mql_file)
    }

    pub fn parsed_mql_file(&self) -> &MQLQueryFile {
        &self.parsed_mql_file
    }
}

pub fn parse(text: &dyn AsRef<str>) -> Result<ParseResult> {
    let mut pairs = MQLParser::parse(Rule::file, text.as_ref())
        .map_err(|e| e.renamed_rules(parser::renamed_rules_impl))?;

    let parsed_mql_file =
        MQLParser::parse_file(pairs.next().context("File should have a child rule")?)?;

    Ok(ParseResult { parsed_mql_file })
}
