use std::fs::File;
use std::io;
use std::io::prelude::*;

use std::env;

use std::collections::HashMap;

fn main() -> io::Result<()> {
    // Set up CLI args
    let args: Vec<String> = env::args().collect();

    // Read the input file
    let mut f = File::open(&args[2])?;
    let mut buffer = String::new();
    f.read_to_string(&mut buffer)?;

    // Do processing
    if &args[1] == "a" {
        part_a(buffer)
    } else {
        part_b(buffer)
    }

    Ok(())
}

fn part_a(input: String) {
    let mut twos = 0;
    let mut threes = 0;

    let mut got_two = false;
    let mut got_three = false;

    for line in input.split_whitespace() {
        let count = count_letters(line);
        println!("id: {} count: {:?}", line, count);
        for v in count.values() {
            if (*v == 2) && !got_two {
                twos += 1;
                got_two = true;
            } else if (*v == 3) && !got_three {
                threes += 1;
                got_three = true;
            }
        }

        got_two = false;
        got_three = false;
    }
    println!("twos: {} threes: {}", twos, threes);
    println!("checksum: {}", twos * threes);
}

fn part_b(input: String) {
    let ids = input.split_whitespace().collect::<Vec<&str>>();
    'outer: for (i, a) in ids.iter().enumerate() {
        for b in &ids[i..ids.len()] {
            let distance = hamming_distance(a, b);
            if distance == 1 {
                println!("a: {} b: {}", a, b);
                //find letters in common
                for (x, y) in a.chars().zip(b.chars()) {
                    if x == y {
                        print!("{}", x);
                    }
                }
                println!();
                break 'outer;
            }
        }
    }
}

fn count_letters(word: &str) -> HashMap<char, u32> {
    let mut count = HashMap::new();

    for c in word.chars() {
        let counter = count.entry(c).or_insert(0);
        *counter += 1;
    }

    count
}

fn hamming_distance(w1: &str, w2: &str) -> u32 {
    let mut distance = 0;
    for (a, b) in w1.chars().zip(w2.chars()) {
        if a != b {
            distance += 1;
        }
    }
    distance
}
