use crate::closest_string::closest_string;

lazy_static::lazy_static! {
    static ref YALE_DEPARTMENTS_LIST: Box<[&'static str]> = {
        let mut unsorted = include_str!("./yale_departments.txt").lines().collect::<Vec<_>>();
        unsorted.sort();
        unsorted.into_boxed_slice()
    };
}

pub fn is_department(department: &str) -> bool {
    YALE_DEPARTMENTS_LIST.binary_search(&department).is_ok()
}

pub fn closest_department(misspelled_department: &str) -> &'static str {
    closest_string(misspelled_department, YALE_DEPARTMENTS_LIST.as_ref())
        .expect("YALE_DEPARTMENTS_LIST is never empty")
}
