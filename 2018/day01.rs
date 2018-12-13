use std::io;
use std::io::prelude::*;
use std::fs::File;

use std::env;

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
    let mut frequency = 0;
    for p in input.split_whitespace() {
        print!("Starting at {}, ", frequency);
        print!("add {}, ", p);

        let s: i32 = p.parse().unwrap();
        frequency += s;

        println!("end on {}", frequency);
    }
}

fn part_b(input: String) {
    let mut frequency = 0;
    let mut visited = vec![0];
    let mut found = false;

    while !found {
        for p in input.split_whitespace() {
            let s: i32 = p.parse().unwrap();
            frequency += s;
            if visited.contains(&frequency) {
                found = true;
                break;
            }
            visited.push(frequency);
        }
    }

    println!("first duplicate frequency: {}", frequency);
}
