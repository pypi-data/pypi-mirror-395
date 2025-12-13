# WASI CLI (Rust -> wasm)

Build and run with wasmtime (or other WASI runtime):

```bash
rustup target add wasm32-wasip1
cargo build --target wasm32-wasip1 --example wasm_cli

wasmtime target/wasm32-wasip1/debug/examples/wasm_cli.wasm price \
  --spot 105 --strike 100 --mat 0.25 --rate 0.03 --div 0.01 --vol 0.22

wasmtime target/wasm32-wasip1/debug/examples/wasm_cli.wasm iv \
  --price 4.25 --spot 102 --strike 100 --mat 0.25 --rate 0.02 --div 0.0
```
