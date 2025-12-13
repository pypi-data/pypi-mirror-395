# Build helpers for WASM bindings from the `wasm_api` example.

WASM_EXAMPLE=wasm_api
WASM_FEATURES=wasm-example
WASM_TARGET=wasm32-unknown-unknown

.PHONY: wasm-bindings wasm-clean

# Build web (plain JS) and bundler/React bindings into target/wasm/
wasm-bindings:
	wasm-pack build --target web --out-dir target/wasm/pkg-web -- \
	  --example $(WASM_EXAMPLE)
	wasm-pack build --target bundler --out-dir target/wasm/pkg-react -- \
	  --example $(WASM_EXAMPLE)
	mkdir -p target/wasm/pkg-react/web
	cp target/wasm/pkg-web/quant_opts* target/wasm/pkg-react/web/
	# Ensure bundler package exports wasm artifacts and has proper entry fields for Vite/Rollup.
	node -e "const fs=require('fs');const p='target/wasm/pkg-react/package.json';const j=JSON.parse(fs.readFileSync(p));j.main='quant_opts.js';j.module='quant_opts.js';j.types='quant_opts.d.ts';j.files=['quant_opts_bg.wasm','quant_opts.js','quant_opts_bg.js','quant_opts.d.ts','web/quant_opts_bg.wasm','web/quant_opts.js','web/quant_opts_bg.js','web/quant_opts.d.ts','LICENSE.md'];j.exports={'./': './quant_opts.js','.': './quant_opts.js','./quant_opts_bg.wasm': './quant_opts_bg.wasm','./web': './web/quant_opts.js','./web/quant_opts_bg.wasm': './web/quant_opts_bg.wasm'};fs.writeFileSync(p,JSON.stringify(j,null,2));"

wasm-clean:
	rm -rf target/wasm/pkg-web target/wasm/pkg-react
