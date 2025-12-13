//! Minimal entrypoint for wasm-bindgen build. The actual exported functions live in `src/lib.rs`
//! behind `#[cfg(target_arch = "wasm32")]` and are always compiled when targeting wasm32.
//!
//! For non-wasm targets this stub keeps `cargo fmt`/`cargo check --examples` happy.

#[cfg(target_arch = "wasm32")]
fn main() {
    // wasm-bindgen exports are initialized automatically by the generated JS glue.
}

#[cfg(not(target_arch = "wasm32"))]
fn main() {
    // This example only runs on wasm32.
}
