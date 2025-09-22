# UNSAT-Core-Generation
## Dependencies

- [Yosys](https://github.com/YosysHQ/yosys) (for Verilog to CNF translation)
- [CaDiCaL](https://github.com/arminbiere/cadical) (SAT solver)
- [DRAT-trim](https://github.com/msoos/drat-trim) (UNSAT core extraction)

Make sure all tools are installed and available in your PATH.

## Quick Start

1. Synthesize the Verilog design into AIG:

   ```
   yosys -s synth2aig.ys
   ```

2. Convert AIG to CNF with mapping and query
   ```
   python aig2cnf.py top.aig d=1 f=0 g=1
   ```

3. Run the SAT solver on the CNF with a generated DRAT proof for UNSAT case:
   ```
   cadical problem.cnf proof.drat
   ```

4. Extract UNSAT core
   ```
   drat-trim problem.cnf proof.drat -c core.cnf
   ```
