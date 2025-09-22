# UNSAT-Core-Generation
## Dependencies

- [Yosys](https://github.com/YosysHQ/yosys) (for Verilog to CNF translation)
- [CaDiCaL](https://github.com/arminbiere/cadical) (SAT solver)
- [DRAT-trim](https://github.com/msoos/drat-trim) (UNSAT core extraction)

Make sure all tools are installed and available in your PATH.

## Quick Start

1. Synthesize your Verilog design and convert to CNF:

   ```
   yosys -s synth_to_cnf.ys
   ```

2. Run the SAT solver with proof logging enabled:
   ```
   cadical design.cnf --proof=proof.drat
   ```

3. Extract the UNSAT core from the proof:
   ```
   drat-trim design.cnf proof.drat -c core.cnf
   ```

4. Map the core clauses back to Verilog signals:
   ```
   python map_core_to_signals.py core.cnf mapping.json
   ```
