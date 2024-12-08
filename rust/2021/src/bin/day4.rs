use std::fs;

extern crate util;

#[derive(Debug, Copy, Clone)]
struct BoardEntry {
    number: usize,
    marked: bool,
}
type BoardMatrix = [[BoardEntry; 5]; 5];

trait BingoBoard {
    fn has_bingo(&self) -> bool;
    fn mark(&mut self, number: usize);
    fn clear(&mut self);
    fn sum_of_unmarked(&self) -> usize;
}

impl BingoBoard for BoardMatrix {
    fn has_bingo(&self) -> bool {
        // check across
        if self.iter().any(|row| row.iter().all(|x| x.marked)) {
            return true;
        }
    
        // check down
        // 0th of each board[*], then 1st of each board[*]...
        for i in 0..5 {
            if self.iter().map(|x| x[i]).all(|x| x.marked) {
                return true;
            }
        }
    
        // no need to check diagonals
    
        false
    }

    fn mark(&mut self, number: usize) {
        for n in self.iter_mut().flatten() {
            if n.number == number {
                n.marked = true;
            }
        }
    }

    fn clear(&mut self) {
        for entry in self.iter_mut().flatten() {
            entry.marked = false;
        }
    }

    fn sum_of_unmarked(&self) -> usize {
        self.iter().flatten().filter(|x| !x.marked).fold(0, |acc, x| acc + x.number)
    }
}

fn main() {
    // ingest file
    let input = fs::read_to_string("input/day4.txt")
        .expect("Failed to read file");

    // pull off numbers
    let (numbers, input) = input.split_once("\n").unwrap();
    let numbers: Vec<&str> = numbers.split(',').collect();
    let numbers = util::convert_vec(numbers);

    // init boards with the rest of the input
    let input: Vec<&str> = input.trim().split("\n\n").collect();
    let mut boards: Vec<BoardMatrix> = Vec::new();
    for board in input {
        let mut parsed_board = [[BoardEntry{number: 0, marked: false}; 5]; 5];
        for (i, row) in board.split('\n').enumerate() {
            for (j, col) in row.split_whitespace().enumerate() {
                parsed_board[i][j].number = str::parse(col).unwrap();
            }
        }
        boards.push(parsed_board);
    }

    part_a(&numbers, &mut boards);
    for b in &mut boards {
        b.clear();
    }
    part_b(&numbers, &mut boards);
}

// find first winning board
fn part_a(numbers: &[usize], boards: &mut Vec<BoardMatrix>) {
    'outer: for n in numbers {
        for board in &mut *boards {
            board.mark(*n);
            if board.has_bingo() {
                println!("first winning score: {}", board.sum_of_unmarked() * n);
                break 'outer;
            }
        }
    }
}

// find last winning board
fn part_b(numbers: &[usize], boards: &mut Vec<BoardMatrix>) {
    let mut bingo_count = 0;
    let total_boards = boards.len();

    'outer: for n in numbers {
        for board in &mut *boards {
            let already_bingo = board.has_bingo();
            board.mark(*n);
            if !already_bingo && board.has_bingo() {
                bingo_count += 1;
            }

            // check if this was the last bingo
            if bingo_count == total_boards {
                println!("last winning score: {}", board.sum_of_unmarked() * n);
                break 'outer;
            }
        }
    }
}
