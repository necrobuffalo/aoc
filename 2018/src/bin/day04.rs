use std::fs::File;
use std::io;
use std::io::prelude::*;
use std::env;

use std::cmp::Ordering;
use std::collections::BTreeSet;
use std::collections::HashMap;

extern crate regex;
use regex::Regex;

///////////
// TYPES //
///////////
#[derive(Debug)]
enum GuardAction {
    StartedShift(i32),
    FellAsleep,
    WokeUp,
}

#[derive(Debug)]
struct LogEntry {
    month: i32,
    day: i32,
    hour: i32,
    minute: i32,
    action: GuardAction,
}
impl Ord for LogEntry {
    fn cmp(&self, other: &LogEntry) -> Ordering {
        //self.timestamp.cmp(&other.timestamp)
        if self.month < other.month {
            return Ordering::Less;
        } else if self.month > other.month {
            return Ordering::Greater;
        }
        if self.day < other.day {
            return Ordering::Less;
        } else if self.day > other.day {
            return Ordering::Greater;
        }
        if self.hour < other.hour {
            return Ordering::Less;
        } else if self.hour > other.hour {
            return Ordering::Greater;
        }
        if self.minute < other.minute {
            return Ordering::Less;
        } else if self.minute > other.minute {
            return Ordering::Greater;
        }

        Ordering::Equal
    }
}
impl PartialOrd for LogEntry {
    fn partial_cmp(&self, other: &LogEntry) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}
impl PartialEq for LogEntry {
    fn eq(&self, other: &LogEntry) -> bool {
        (self.month == other.month) && (self.day == other.day) && (self.hour == other.hour) && (self.minute == other.minute)
    }
}
impl Eq for LogEntry {}

//////////
// MAIN //
//////////
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

////////////
// PART A //
////////////
fn part_a(input: String) {
    let log = read_guard_log(input);

    let guard = most_sleep(&log);

    let minute = sleepiest_minute(&log, guard);
    println!("Guard {} at minute {}", guard, minute);
    println!("Result: {}", guard * minute);
}

////////////
// PART B //
////////////
fn part_b(input: String) {
    let log = read_guard_log(input);
}

/////////////
// HELPERS //
/////////////
fn read_guard_log(input: String) -> BTreeSet<LogEntry> {
    let re = Regex::new(r"^\[1518-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+)\] (?P<action>.*)$").unwrap();
    let guard_re = Regex::new(r"^Guard #(?P<guard>\d+) begins shift$").unwrap();
    let mut log = BTreeSet::new();

    for line in input.lines() {
        let caps = re.captures(line).unwrap();
        let mut action: GuardAction;

        if caps.name("action").unwrap().as_str() == "wakes up" {
            action = GuardAction::WokeUp;
        } else if caps.name("action").unwrap().as_str() == "falls asleep" {
            action = GuardAction::FellAsleep;
        } else {
            let guard_caps = guard_re.captures(caps.name("action").unwrap().as_str()).unwrap();
            action = GuardAction::StartedShift(guard_caps.name("guard").unwrap().as_str().parse::<i32>().unwrap());
        }

        let entry = LogEntry {
            month: caps.name("month").unwrap().as_str().parse::<i32>().unwrap(),
            day: caps.name("day").unwrap().as_str().parse::<i32>().unwrap(),
            hour: caps.name("hour").unwrap().as_str().parse::<i32>().unwrap(),
            minute: caps.name("minute").unwrap().as_str().parse::<i32>().unwrap(),
            action: action
        };

        log.insert(entry);
    }

    log
}

fn most_sleep(log: &BTreeSet<LogEntry>) -> i32 {
    let mut sleep_counts = HashMap::new();
    let mut current_guard = -1;
    let mut last_slept_minute = 0;

    for entry in log {
        match entry.action {
            GuardAction::FellAsleep => {
                last_slept_minute = entry.minute;
            }
            GuardAction::WokeUp => {
                *sleep_counts.entry(current_guard.clone()).or_insert(0) += entry.minute - last_slept_minute;
            }
            GuardAction::StartedShift(guard_number) => {
                if !sleep_counts.contains_key(&guard_number) {
                    sleep_counts.insert(guard_number, 0);
                }
                current_guard = guard_number;
            }
        }
    }

    *sleep_counts.iter().max_by_key(|x| x.1).unwrap().0
}

fn sleepiest_minute(log: &BTreeSet<LogEntry>, guard: i32) -> i32 {
    let mut sleep_counts = HashMap::new();
    let mut current_guard = -1;
    let mut last_slept_minute = 0;

    for entry in log {
        // Unless it's the guard we're checking we don't care.
        match entry.action {
            GuardAction::FellAsleep => {
                if current_guard == guard {
                    last_slept_minute = entry.minute;
                }
            }
            GuardAction::WokeUp => {
                if current_guard == guard {
                    for i in last_slept_minute..entry.minute {
                        // Increment all the minutes we were sleeping for
                        *sleep_counts.entry(i).or_insert(0) += 1;
                    }
                }
            }
            GuardAction::StartedShift(guard_number) => {
                current_guard = guard_number;
            }
        }
    }

    *sleep_counts.iter().max_by_key(|x| x.1).unwrap().0
}
