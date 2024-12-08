use std::fs;

extern crate util;

fn main() {
    // ingest file
    let input = fs::read_to_string("input/day1.txt")
        .expect("Failed to read file");
    let input: Vec<&str> = input.lines().collect();
    let input = util::convert_vec(input);

    part_a(&input);
    part_b(&input);
}

// single measurement
fn part_a(input: &[isize]) {
    let mut last = input[0];
    let mut index = 1;
    let mut larger_count = 0;

    while index < input.len() {
        if input[index] > last {
            larger_count += 1;
        }

        last = input[index];
        index += 1;
    }

    println!("{} larger measurements", larger_count);
}

// 3 measurement sliding window
fn part_b(input: &[isize]) {
    let mut last_sum: isize = input[0..3].iter().sum();
    let mut index = 1;
    let mut larger_count = 0;

    while index < input.len() - 2 {
        let sum = input[index..index+3].iter().sum();
        if sum > last_sum {
            larger_count += 1
        }

        last_sum = sum;
        index += 1;
    }

    println!("p2 {} larger measurements", larger_count);
}