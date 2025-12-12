**Applied Pathological Mathematics™** was born from this hypothesis:

*Higher-dimensional algebras following the Cayley-Dickson sequence, which have been wrongly dismissed as "pathological" mathematics, can be interpreted and exploited for computational advantage, with particular benefits for AGI research and development.*

---

# CAILculator MCP Server

**High-dimensional mathematical structure analysis for AI agents**

*"Better math, less suffering"*

## What This Is

A Model Context Protocol server that lets AI agents compute with Cayley-Dickson algebras (sedenions 16D, pathions 32D, up to 256D) and associated Clifford algebras. Built on verified mathematical research into zero divisor patterns and structural properties discovered through systematic computational enumeration.

## Why "Pathological" Might Mean "Powerful"

Beyond quaternions (4D) and octonions (8D), the Cayley-Dickson construction produces algebras with properties that violate conventional mathematical expectations:

- **Non-associativity**: (a × b) × c ≠ a × (b × c)
- **Zero divisors**: Non-zero numbers P, Q where P × Q = 0
- **Loss of division algebra structure**: Not every non-zero element has a multiplicative inverse
- **Dimensional complexity scaling**: Pattern counts grow superlinearly

These properties are called "pathological" because they break the rules of "nice" algebra that works for reals, complex numbers, quaternions, and octonions.

**Pathological, however, doesn't mean useless.**

Zero divisors exhibit patterns and symmetries. Non-associativity encodes order-dependence and context-sensitivity. The vast space of algebraic dark matter in higher-dimensional math becomes huntable through hypothesis-driven computational enumeration: structure over brute force, verification over assumption.

This server based on Applied Pathological Mathematics™ was designed to offer advantages for:
- High-dimensional representation learning
- Pattern detection in complex systems
- Algebraic approaches to neural architecture
- Structure-preserving embeddings
- Time series regime detection

## Mathematical Foundation

### Cayley-Dickson Construction

The Cayley-Dickson construction recursively doubles dimension:
- **R** (reals, 1D) → **C** (complex, 2D) → **H** (quaternions, 4D) → **O** (octonions, 8D)
- **S** (sedenions, 16D) → **P** (pathions, 32D) → 64D → 128D → 256D...

Each doubling loses algebraic properties:
- C: loses ordering
- H: loses commutativity
- O: loses associativity
- S and beyond: gain zero divisors, lose division algebra structure

### Zero Divisors

A **zero divisor** is a pair of non-zero elements P, Q in an algebra where P × Q = 0.

In our research, we focus on two-term zero divisors of the form:
```
(e_a ± e_b) × (e_c ± e_d) = 0
```

where e_i are basis elements and a, b, c, d are distinct indices.

**Verified Pattern Counts:**
- 16D (Sedenions): 84 base patterns, 168 ordered patterns
- 32D (Pathions): 460 base patterns, 920 ordered patterns

These patterns exhibit:
- **Block structure**: 16D blocks replicate with cross-block mixing
- **Conjugation symmetry**: Predictable sign-flip behavior
- **Computational stability**: Numerical verification to machine precision (< 1e-13)

### Research Foundation

Built on systematic computational enumeration published at DOI: [10.5281/zenodo.17402496](https://zenodo.org/records/17402496) - Framework-Independent Zero Divisor Patterns in Higher-Dimensional Cayley-Dickson Algebras: Discovery and Verification of The Canonical Six

Recent work has identified connections to E8 exceptional Lie algebra structure (October 2025 discoveries) with modular development integrated. Ongoing research will continue further development into 512D.

## Installation

```bash
pip install cailculator-mcp
```

For HTTP transport (Gemini CLI support):
```bash
pip install cailculator-mcp[http]
```

## Setup

CAILculator MCP Server supports two transport modes:
- **stdio** (default): For Claude Desktop, Claude Code
- **http**: For Gemini CLI and other HTTP-based MCP clients

### Setup for Claude Desktop (stdio mode)

Add to your MCP client configuration:

**Mac/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "cailculator": {
      "command": "cailculator-mcp",
      "env": {
        "CAILCULATOR_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Setup for Gemini CLI (HTTP mode)

#### 1. Start the HTTP server:

```bash
cailculator-mcp --transport http --port 8080
```

Set your API key via environment variable:
```bash
export CAILCULATOR_API_KEY="your_api_key_here"
# Windows: set CAILCULATOR_API_KEY=your_api_key_here
```

**Note:** The server requires a valid API key. Contact paul@chavezailabs.com for research access.

#### 2. Configure Gemini CLI:

Add to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "cailculator": {
      "manifestUrl": "http://localhost:8080/mcp/manifest"
    }
  }
}
```

#### 3. HTTP endpoints:

- **GET /mcp/manifest** - Tool definitions
- **POST /message** - MCP JSON-RPC messages
- **GET /health** - Health check

## Available Tools

### Core Mathematical Operations

#### `chavez_transform`
Apply proprietary transform that maps data into high-dimensional Cayley-Dickson space for structural analysis.

**Parameters:**
- `data`: Input numerical data
- `dimension`: Target dimension (16, 32, 64, 128, 256)
- `framework`: Algebra framework ("cayley_dickson" or "clifford")

**Returns:** Transformed representation with structural metadata

---

#### `detect_patterns`
Find conjugation symmetries and zero divisor resonances in transformed data.

**Parameters:**
- `transformed_data`: Output from chavez_transform
- `pattern_type`: "conjugation", "zero_divisor", or "all"

**Returns:** Detected patterns with confidence scores

---

#### `compute_high_dimensional`
Direct high-dimensional algebra calculations.

**Parameters:**
- `operation`: "multiply", "add", "conjugate", "norm", "is_zero_divisor"
- `operands`: List of hypercomplex numbers (as coefficient arrays)
- `dimension`: Dimension of algebra (16, 32, 64, 128, 256)

**Returns:** Result of computation

---

#### `analyze_dataset`
End-to-end analysis pipeline combining transform, pattern detection, and interpretation.

**Parameters:**
- `data`: Input dataset
- `dimension`: Analysis dimension
- `analysis_type`: "full", "quick", "custom"

**Returns:** Complete analysis report with detected structures

---

#### `illustrate`
Generate visualizations of algebraic structures and patterns.

**Parameters:**
- `visualization_type`: "zero_divisor_network", "pattern_heatmap", "e8_mandala", "dimension_comparison"
- `data`: Optional data for visualization context

**Returns:** Image or structured visualization data

---

#### `zdtp_transmit`
Zero Divisor Transmission Protocol - transmit 16D data through verified mathematical gateways to 32D and 64D spaces with convergence analysis.

**Parameters:**
- `input_16d`: 16-element coefficient array
- `gateway`: Gateway to use:
  - `"S1"` - Master Gateway: (e₁ + e₁₄) × (e₃ + e₁₂) = 0
  - `"S2"` - Multi-Modal Gateway: (e₃ + e₁₂) × (e₅ + e₁₀) = 0
  - `"S3A"` - Discontinuous Gateway: (e₄ + e₁₁) × (e₆ + e₉) = 0
  - `"S3B"` - Conjugate Pair Gateway: (e₁ - e₁₄) × (e₃ - e₁₂) = 0
  - `"S4"` - Linear Gateway: (e₁ - e₁₄) × (e₅ + e₁₀) = 0
  - `"S5"` - Transformation Gateway: (e₂ - e₁₃) × (e₆ + e₉) = 0
  - `"all"` - Full cascade through all 6 gateways with convergence scoring

**Returns:**
- Dimensional states (16D → 32D → 64D lossless transmission)
- Zero divisor verification status
- Convergence score (for "all"): 0.0-1.0 measuring structural stability
  - **>0.8**: High convergence - robust structure
  - **0.5-0.8**: Moderate - some variance
  - **<0.5**: Low - structural shift detected

**Use Cases:**
- Data integrity verification through mathematical structure
- High-dimensional embedding stability analysis
- Detecting structural shifts in time series data

### Financial Analysis Tools

The server includes specialized tools for time series and financial data analysis:

#### `load_market_data`
Load and validate financial time series data from CSV, Excel, or JSON files.

**Features:**
- Auto-detects OHLCV columns (flexible naming: "Close"/"close"/"CLOSE"/"price")
- Data quality validation and cleaning
- Large file handling (>1GB via chunked reading)
- Date range filtering
- Multi-symbol support

---

#### `market_indicators`
Calculate technical indicators with signal interpretation.

**Available indicators:**
- **Momentum**: RSI, MACD, Stochastic Oscillator
- **Trend**: SMA, EMA, ADX, Ichimoku Cloud
- **Volatility**: Bollinger Bands, ATR
- **Volume**: OBV, VWAP

**Terminology levels:**
- `technical`: Full mathematical notation
- `standard`: Industry terminology
- `simple`: Plain English explanations

---

#### `regime_detection`
Dual-method regime analysis combining statistical and structural approaches.

**Two independent methods:**
1. **Statistical baseline**: Hidden Markov Models (HMM) for momentum-based regime classification
2. **Mathematical structure**: Chavez Transform analysis in 32D sedenion space

**Output includes:**
- Regime classification (bull/bear/sideways) from both methods
- Conjugation symmetry (structural stability measure)
- Zero divisor count (bifurcation risk indicator)
- Agreement score between methods
- Confidence assessment
- Actionable interpretation

**When methods agree:** High confidence in regime classification
**When methods disagree:** Potential regime transition warning

---

#### `batch_analyze_market`
Smart sampling strategy for GB-scale datasets.

**Process:**
1. Sample ~5000 points for quick analysis
2. Calculate confidence score
3. If confidence > 70%, identify suspicious periods
4. Deep dive on flagged periods only

**Analysis types:**
- Regime detection
- Pattern discovery
- Anomaly detection

## Usage Examples

### Mathematical Research
```python
# Find zero divisors in 32D pathion algebra
result = compute_high_dimensional(
    operation="multiply",
    operands=[
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, ...],  # e_1 + e_10
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, ...]   # e_4 - e_15
    ],
    dimension=32
)
# Check if norm ≈ 0 for zero divisor verification
```

### Pattern Detection in Data
```
"Apply Chavez Transform to this dataset in 32D and detect conjugation patterns"
"Analyze this high-dimensional embedding for structural instabilities"
"Find zero divisor resonances in this time series"
```

### Financial Analysis
```
"Load bitcoin_daily.csv and run dual-method regime detection"
"Calculate RSI and MACD with technical terminology"
"Batch analyze this 5GB tick data file for anomalies"
```

## For AGI Researchers

If you're working on:
- **High-dimensional embedding spaces**: Explore algebraic structure beyond Euclidean/Hilbert spaces
- **Pattern emergence**: Study how zero divisors create branching structures in representations
- **Neural architecture design**: Investigate non-associative operations for context-dependent computation
- **Time series modeling**: Use structural stability measures alongside statistical methods
- **Representation learning**: Test whether "pathological" algebras offer benefits for certain data types

### Research Collaboration

Interested in applying these tools to AGI research? Contact Paul Chavez at iknowpi@gmail.com for:
- Research access and collaboration
- Custom tool development
- Mathematical consultation
- Data analysis support

## Technical Details

### Numerical Precision
- Zero divisor threshold: |P × Q| < 1e-10
- Typical verified patterns: norm < 1e-13
- Uses Python's `hypercomplex` library for stable computation

### Supported Dimensions
- 16D (Sedenions): 84 base zero divisor patterns
- 32D (Pathions): 460 base patterns
- 64D, 128D, 256D: Pattern catalogs under active research

### Pattern Classes (32D)
1. **Within-block patterns**: Inherited from 16D structure (84 base per block)
2. **Cross-block patterns**: Terms span different 16D blocks (132 base)
3. **Constant-offset patterns**: Same offset k for both terms (126 base)
4. **Variable-offset patterns**: Different offsets k1, k2 (216 base)

## Known Issues

- Large file processing (>10GB) may require manual chunking for optimal memory usage.

## Contact

**Research Collaboration:** paul@chavezailabs.com
**GitHub:** https://github.com/pchavez2029/cailculator-mcp
**General Inquiries:** iknowpi@gmail.com

---

**Chavez AI Labs** - *"Better math, less suffering"*
