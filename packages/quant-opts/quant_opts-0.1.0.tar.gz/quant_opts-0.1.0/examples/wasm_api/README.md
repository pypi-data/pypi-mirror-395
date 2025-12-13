# WASM bindings (wasm-bindgen)

WASM exports są budowane przez `make wasm-bindings`, co generuje:
- `target/wasm/pkg-web` (plain web)
- `target/wasm/pkg-react` (bundler)

Szybki start (web):
```bash
make wasm-bindings
cd examples/vanilla_web_js
python -m http.server 8989  # otwórz http://localhost:8989
```

Szybki start (React, bundler):
```bash
make wasm-bindings
cd examples/react_web_ts
npm install --no-package-lock
npm run build
```

Eksporty WASM (`price_call_bs`, `rational_iv_bs`) są zdefiniowane w `src/lib.rs` (gated tylko na `target_arch = "wasm32"`). Ten katalog zawiera jedynie stub `main.rs` potrzebny, by `cargo fmt/check --examples` działał na innych targetach.
