use std::str::FromStr;
use std::fmt::Debug;

pub fn convert_vec<T: FromStr>(strs: Vec<&str>) -> Vec<T> where <T as FromStr>::Err: Debug {
    let mut output = Vec::new();
    for s in strs {
        output.push(T::from_str(s).expect("Failed to parse item in vector"));
    }

    output
}