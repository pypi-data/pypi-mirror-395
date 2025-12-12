use std::collections::BTreeMap;

use strsim::jaro_winkler;

pub(crate) fn closest_string<'a>(
    test: impl AsRef<str>,
    options: impl AsRef<[&'a str]>,
) -> Option<&'a str> {
    let test = test.as_ref();
    let options = options.as_ref();

    let test_normalized = test.to_ascii_lowercase();

    let mut map = BTreeMap::new();

    for option in options {
        let option_normalized = option.to_ascii_lowercase();
        let score = (jaro_winkler(&test_normalized, &option_normalized) * 1000f64) as i32;
        map.insert(score, *option);
    }

    map.last_key_value().map(|(_, best_match)| *best_match)
}
