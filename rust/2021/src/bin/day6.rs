use std::fs;
use std::collections::HashMap;

extern crate util;

fn main() {
    // ingest file
    let input = fs::read_to_string("input/day6.txt")
        .expect("Failed to read file");
    let input = input.trim().split(',').collect();
    let input = util::convert_vec(input);

    part_a(&input);
    part_b(&input);
}

fn step(population: &mut HashMap<usize, usize>) {
    // count how many new fish we need to add, before we do anything else.
    let new_fish = *population.get(&0).unwrap_or(&0);
    // shift everything else down
    for index in 1..=8 {
        population.insert(index - 1, *population.get(&index).unwrap_or(&0));
    }
    // add the new fish
    population.insert(8, new_fish);
    // reset internal timers for fish who made new fish
    population.insert(6, *population.get(&6).unwrap_or(&0) + new_fish);
}

fn part_a(input: &[usize]) {
    let mut population: HashMap<usize,usize> = HashMap::new();
    for i in input {
        let entry = population.entry(*i).or_insert(0);
        *entry += 1;
    }

    for _i in 0..80 {
        step(&mut population);
    }

    // count total fish
    let sum = population.iter().fold(0, |acc, (_key,  val)| acc + val);
    println!("a: total population: {}", sum);
}

fn part_b(input: &[usize]) {
    let mut population: HashMap<usize,usize> = HashMap::new();
    for i in input {
        let entry = population.entry(*i).or_insert(0);
        *entry += 1;
    }

    for _i in 0..256 {
        step(&mut population);
    }

    // count total fish
    let sum = population.iter().fold(0, |acc, (_key,  val)| acc + val);
    println!("total population: {}", sum);
}