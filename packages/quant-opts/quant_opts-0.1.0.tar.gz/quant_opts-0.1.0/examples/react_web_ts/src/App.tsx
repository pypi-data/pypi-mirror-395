import { useEffect, useState } from 'react';
import { price_call_bs } from 'quant-opts';

export default function App() {
  const [ready, setReady] = useState(true);
  const [spot, setSpot] = useState(105);
  const [strike, setStrike] = useState(100);
  const [mat, setMat] = useState(0.25);
  const [rate, setRate] = useState(0.03);
  const [div, setDiv] = useState(0.01);
  const [vol, setVol] = useState(0.22);
  const [output, setOutput] = useState<string>('Loading WASM…');

  useEffect(() => {
    setOutput('WASM loaded.');
  }, []);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const price = price_call_bs(spot, strike, mat, rate, div, vol);
      setOutput(`Call price: ${price.toFixed(6)}`);
    } catch (err) {
      setOutput(`Error: ${err}`);
    }
  };

  return (
    <main style={{ fontFamily: 'sans-serif', padding: '1.5rem', maxWidth: 480 }}>
      <h1>quant-opts React WASM demo</h1>
      <form onSubmit={onSubmit} style={{ display: 'grid', gap: '0.5rem' }}>
        <label>
          Spot
          <input type="number" step="0.01" value={spot} onChange={(e) => setSpot(Number(e.target.value))} />
        </label>
        <label>
          Strike
          <input type="number" step="0.01" value={strike} onChange={(e) => setStrike(Number(e.target.value))} />
        </label>
        <label>
          Maturity (years)
          <input type="number" step="0.001" value={mat} onChange={(e) => setMat(Number(e.target.value))} />
        </label>
        <label>
          Rate
          <input type="number" step="0.0001" value={rate} onChange={(e) => setRate(Number(e.target.value))} />
        </label>
        <label>
          Dividend
          <input type="number" step="0.0001" value={div} onChange={(e) => setDiv(Number(e.target.value))} />
        </label>
        <label>
          Volatility
          <input type="number" step="0.0001" value={vol} onChange={(e) => setVol(Number(e.target.value))} />
        </label>
        <button type="submit" disabled={!ready} style={{ padding: '0.5rem 1rem' }}>
          {ready ? 'Compute price' : 'Loading WASM…'}
        </button>
      </form>
      <pre style={{ background: '#f7f7f7', padding: '0.75rem', marginTop: '1rem' }}>{output}</pre>
    </main>
  );
}
