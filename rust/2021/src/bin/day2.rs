use std::fs;
use std::str::FromStr;

enum Direction {
    Forward(usize),
    Up(usize),
    Down(usize),
}

impl FromStr for Direction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let split = s.split_once(" ").unwrap();
        let amount = split.1.parse().unwrap();
        match split.0 {
            "forward" => Ok(Direction::Forward(amount)),
            "up" => Ok(Direction::Up(amount)),
            "down" => Ok(Direction::Down(amount)),
            _ => Err("Invalid submarine instruction".to_string()),
        }
    }
}

fn main() {
    // ingest file
    let input = fs::read_to_string("input/day2.txt")
        .expect("Failed to read file");
    let input: Vec<&str> = input.lines().collect();

    let mut directions = Vec::new();
    for i in input {
        directions.push(i.parse().unwrap())
    }

    part_a(&directions);
    part_b(&directions);
}

fn part_a(input: &[Direction]) {
    let mut horizontal = 0;
    let mut depth = 0;

    for instruction in input {
        match instruction {
            Direction::Forward(n) => horizontal += n,
            Direction::Up(n) => depth -= n,
            Direction::Down(n) => depth += n,
        }
    }

    println!("Final position: {}", horizontal);
    println!("Final depth: {}", depth);

    println!("Multiplied: {}", horizontal * depth);
}

fn part_b(input: &[Direction]) {
    let mut horizontal = 0;
    let mut depth = 0;
    let mut aim = 0;

    for instruction in input {
        match instruction {
            Direction::Forward(n) => {
                horizontal += n;
                depth += aim * n;
            },
            Direction::Up(n) => aim -= n,
            Direction::Down(n) => aim += n,
        }
    }

    println!("p2 Final position: {}", horizontal);
    println!("p2 Final depth: {}", depth);

    println!("Multiplied: {}", horizontal * depth);
}