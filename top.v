// top.v
// Circuit:
//   c = and(d, b)
//   e = not(b)
//   g = and(f, c, e)
//
// Property to check: under d=1 and f=0, does there exist b such that g=1

module top (b, d, f, g);
    input b, d, f;
    output g;
    wire c, e;

    assign c = d & b;
    assign e = ~b;
    assign g = f & c & e;
endmodule