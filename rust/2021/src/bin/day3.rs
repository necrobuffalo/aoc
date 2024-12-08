use std::fs;
use std::collections::HashMap;
use std::cmp::Ordering;

fn main() {
    // ingest file
    let input = fs::read_to_string("input/day3.txt")
        .expect("Failed to read file");
    let input: Vec<&str> = input.lines().collect();

    part_a(&input);
    part_b(&input);
}

fn part_a(input: &[&str]) {
    let gamma = gamma_rate(input);
    let epsilon = epsilon_rate(input);

    let gamma = usize::from_str_radix(&gamma, 2).unwrap();
    let epsilon = usize::from_str_radix(&epsilon, 2).unwrap();

    println!("gamma: {}", gamma);
    println!("epsilon: {}", epsilon);
    println!("multiplied: {}", gamma * epsilon);
}

fn part_b(input: &[&str]) {
    let oxygen = o2_rating(input);
    let co2 = co2_rating(input);

    let oxygen = usize::from_str_radix(&oxygen, 2).unwrap();
    let co2 = usize::from_str_radix(&co2, 2).unwrap();

    println!("o2: {}", oxygen);
    println!("co2: {}", co2);
    println!("multiplied: {}", oxygen * co2);
}

// TODO rewrite to use count_digts_etc
fn gamma_rate(input: &[&str]) -> String {
    // Count ones in each position. If greater than half the # of entries, put it in the gamma rate.
    let digits = input[0].len();
    let entries = input.len();
    let mut counts = vec![0; digits];

    for i in input {
        for (pos, c) in i.char_indices() {
            if c == '1' {
                counts[pos] += 1;
            }
        }
    }

    let mut binary_rate = String::from("");
    for c in &counts {
        if c > &(entries / 2) {
            binary_rate.push('1');
        } else {
            binary_rate.push('0');
        }
    }

    binary_rate
}

// epsilon rate is inverted gamma rate
fn epsilon_rate(input: &[&str]) -> String {
    let g_rate = gamma_rate(input);
    let mut e_rate = String::from("");
    for c in g_rate.chars() {
        match c {
            '0' => e_rate.push('1'),
            '1' => e_rate.push('0'),
            _ => panic!("Couldn't parse gamma rate"),
        }
    }

    e_rate
}

fn o2_rating(input: &[&str]) -> String {
    let mut bit_position = 0;
    let mut entries = input.to_vec();

    while entries.len() > 1 {
        let counts = count_digits_at_position(&entries, bit_position);
        match counts.get(&'0').unwrap().cmp(counts.get(&'1').unwrap()) {
            Ordering::Less => {
                // keep 1s
                entries.retain(|n| char::from(n.as_bytes()[bit_position]) == '1');
            }
            Ordering::Equal => {
                // keep 1s
                entries.retain(|n| char::from(n.as_bytes()[bit_position]) == '1');
            }
            Ordering::Greater => {
                // keep 0s
                entries.retain(|n| char::from(n.as_bytes()[bit_position]) == '0');
            },
        }
        bit_position += 1;
    }

    String::from(entries[0])
}

fn co2_rating(input: &[&str]) -> String {
    let mut bit_position = 0;
    let mut entries = input.to_vec();

    while entries.len() > 1 {
        let counts = count_digits_at_position(&entries, bit_position);
        match counts.get(&'0').unwrap().cmp(counts.get(&'1').unwrap()) {
            Ordering::Less => {
                // keep 0s
                entries.retain(|n| char::from(n.as_bytes()[bit_position]) == '0');
            }
            Ordering::Equal => {
                // keep 0s
                entries.retain(|n| char::from(n.as_bytes()[bit_position]) == '0');
            }
            Ordering::Greater => {
                // keep 1s
                entries.retain(|n| char::from(n.as_bytes()[bit_position]) == '1');
            },
        }
        bit_position += 1;
    }

    String::from(entries[0])
}

fn count_digits_at_position(binary_numbers: &[&str], index: usize) -> HashMap<char, usize> {
    let mut counts = HashMap::new();

    for n in binary_numbers {
        let character = char::from(n.as_bytes()[index]);
        let entry = counts.entry(character).or_insert(0);
        *entry += 1;
    }

    counts
}