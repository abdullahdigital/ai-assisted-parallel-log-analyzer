use std::time::Instant;

pub struct Timer {
    start_time: Instant,
}

impl Timer {
    pub fn new() -> Timer {
        Timer {
            start_time: Instant::now(),
        }
    }

    pub fn elapsed_millis(&self) -> u128 {
        self.start_time.elapsed().as_millis()
    }
}
