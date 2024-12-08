use std::fs;
use std::str::FromStr;
use std::collections::HashMap;

#[derive(Debug, Hash, Eq, PartialEq)]
struct Coordinate {
    x: usize,
    y: usize,
}

#[derive(Debug)]
struct LineSegment {
    start: Coordinate,
    end: Coordinate,
}

impl FromStr for Coordinate {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (x, y) = match s.split_once(",") {
            Some((x, y)) => (x, y),
            None => return Err(format!("Failed to split coordinate pair: {}", s)),
        };

        let x = match x.parse() {
            Ok(n) => n,
            Err(e) => return Err(format!("Failed to parse x coordinate: {}", e)),
        };
        let y = match y.parse() {
            Ok(n) => n,
            Err(e) => return Err(format!("Failed to parse y coordinate: {}", e)),
        };

        Ok(Coordinate {x, y})
    }
}

impl FromStr for LineSegment {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (left, right) = match s.split_once(" -> ") {
            Some((left, right)) => (left, right),
            None => return Err(format!("Failed to split line segment: {}", s)),
        };

        let left = match left.parse() {
            Ok(n) => n,
            Err(e) => return Err(format!("Failed to parse left side of line segment: {}", e)),
        };
        let right = match right.parse() {
            Ok(n) => n,
            Err(e) => return Err(format!("Failed to parse right side of line segment: {}", e)),
        };

        Ok(LineSegment {start: left, end: right})
    }
}

impl LineSegment {
    fn is_horizontal(&self) -> bool {
        self.start.y == self.end.y
    }

    fn is_vertical(&self) -> bool {
        self.start.x == self.end.x
    }

    fn all_x(&self) -> Box<dyn DoubleEndedIterator<Item = usize>> {
        if self.start.x < self.end.x {
            Box::new(self.start.x..=self.end.x)
        } else {
            Box::new((self.end.x..=self.start.x).rev())
        }
    }

    fn all_y(&self) -> Box<dyn DoubleEndedIterator<Item = usize>> {
        if self.start.y < self.end.y {
            Box::new(self.start.y..=self.end.y)
        } else {
            Box::new((self.end.y..=self.start.y).rev())
        }
    }

    fn points_on_line(&self) -> Vec<Coordinate> {
        let mut points = Vec::new();

        if self.is_vertical() {
            for y in self.all_y() {
                points.push(Coordinate{x: self.start.x, y});
            }
        } else if self.is_horizontal() {
            for x in self.all_x() {
                points.push(Coordinate{x, y: self.start.y});
            }
        } else {
            // diagonal line, so we can just zip the iterators
            let zipped = self.all_x().zip(self.all_y());
            for (x, y) in zipped {
                points.push(Coordinate{x, y});
            }
        }

        points
    }
}

fn main() {
    // ingest file
    let input = fs::read_to_string("input/day5.txt")
        .expect("Failed to read file");
    let input: Vec<&str> = input.lines().collect();
    // TODO parse into line segments
    let mut segments = Vec::new();
    for line in input {
        segments.push(line.parse::<LineSegment>().unwrap())
    }

    part_a(&segments);
    part_b(&segments);
}

fn part_a(input: &[LineSegment]) {
    let mut grid = HashMap::new();
    for segment in input {
        // if it's horizontal or vertical
        if segment.is_horizontal() || segment.is_vertical() {
            // increment a counter for each of the points it passes through
            for p in segment.points_on_line() {
                // mark in hashmap
                let count = grid.entry(p).or_insert(0);
                *count += 1;
            }
        }
    }

    // count points with 2+
    let intersections = grid.iter().filter(|pair| *pair.1 >= 2).count();
    println!("a: found {} intersections", intersections);
}

fn part_b(input: &[LineSegment]) {
    let mut grid = HashMap::new();
    for segment in input {
        // increment a counter for each of the points it passes through
        for p in segment.points_on_line() {
            // mark in hashmap
            let count = grid.entry(p).or_insert(0);
            *count += 1;
        }
    }

    // count points with 2+
    let intersections = grid.iter().filter(|pair| *pair.1 >= 2).count();
    println!("b: found {} intersections", intersections);
}