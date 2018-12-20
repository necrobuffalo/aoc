extern crate regex;

use std::fs::File;
use std::io;
use std::io::prelude::*;
use std::env;

use std::cmp;

use std::collections::HashMap;
use std::collections::HashSet;

use regex::Regex;

#[derive(Clone,Debug)]
struct Claim {
    left: i32,
    right: i32,
    top: i32,
    bottom: i32,
}
#[derive(PartialEq,Eq,Hash)]
struct Point {
    column: i32,
    row: i32,
}

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
    let claims = parse_claim_list(input);
    let mut conflicts: HashSet<Point> = HashSet::new();

    for (k,a) in claims.iter() {
        for (l,b) in claims.iter() {
            println!("Processing: claim ids {} and {}", k, l);
            if k == l {
                continue
            }
            // check if they overlap, record conflicting points
            match overlap(a,b) {
                Some(c) => {
                    println!("Conflict: {:?}", c);
                    for i in c.left..c.right+1 {
                        for j in c.top..c.bottom+1 {
                            conflicts.insert(Point {
                                column: i,
                                row: j,
                            });
                        }
                    }
                },
                None => continue,
            }
        }
    }

    println!("Collected all conflicts. Total overlap: {}", conflicts.len());
}

fn part_b(input: String) {
    let initial_list = parse_claim_list(input);
    let mut final_list = initial_list.clone();

    for (k, a) in initial_list.iter() {
        for (l, b) in initial_list.iter() {
            if k == l {
                continue;
            }
            match overlap(a,b) {
                Some(_) => {
                    // remove the conflicting entries
                    println!("Conflict between {} and {}", k, l);
                    final_list.remove(k);
                    final_list.remove(l);
                },
                None => continue,
            }
        }
    }
    println!("{:?}", final_list);
}

fn parse_claim_list(input: String) -> HashMap<String,Claim> {
    let re = Regex::new(r"^#(?P<id>\d+) @ (?P<left>\d+),(?P<top>\d+): (?P<width>\d+)x(?P<height>\d+)$").unwrap();
    let mut claims = HashMap::new();
    for line in input.lines() {
        println!("Parsing line: {}", line);
        let caps = re.captures(line).unwrap();
        let mut claim = Claim {
            left: caps.name("left").unwrap().as_str().parse::<i32>().unwrap(),
            top: caps.name("top").unwrap().as_str().parse::<i32>().unwrap(),
            right: 0,
            bottom: 0,
        };
        claim.right = claim.left + caps.name("width").unwrap().as_str().parse::<i32>().unwrap() - 1;
        claim.bottom = claim.top + caps.name("height").unwrap().as_str().parse::<i32>().unwrap() - 1;

        claims.insert(caps.name("id").unwrap().as_str().to_string(), claim);
    };

    claims
}

fn overlap(a: &Claim, b: &Claim) -> Option<Claim> {
    if a.left > b.right || b.left > a.right {
        return None;
    }
    if a.top > b.bottom || b.top > a.bottom {
        return None;
    }
    
    let c = Claim {
        top: cmp::max(a.top, b.top),
        left: cmp::max(a.left, b.left),
        bottom: cmp::min(a.bottom, b.bottom),
        right: cmp::min(a.right, b.right),
    };
    
    Some(c)
}
