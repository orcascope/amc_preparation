# 2022 AMC 10A — verified solution methods

Each problem was solved by 2 independent blind solvers using the
math-olympiad skill (reasoning only, no tools). The official answer key was
the third vote. Every problem was unanimous (3 of 3) unless noted.

## P1 — (D) 109/33
Work from the inside out: 3 + 1/3 = 10/3, so its reciprocal is 3/10. Next 3 + 3/10 = 33/10, whose reciprocal is 10/33. Last, 3 + 10/33 = 109/33.
Trap: (C) 33/10 is the middle level, not the final value. Check: the value must lie between 3.3 and 10/3.

## P2 — (B) 7
Constant speed makes laps proportional to time: 15·27/57 = 135/19 ≈ 7.1. Each lap takes 57/15 = 3.8 min, so 7 laps take 26.6 min ≤ 27.
Benchmark: 27/57 is a bit under 1/2, so the answer is a bit under 7.5.

## P3 — (E) 5
Let the third number be x. Then the second is x + 40 and the first is 6x. So 8x + 40 = 96, giving x = 7. The numbers are 42, 47 and 7, and |42 − 47| = 5.
Trap: misreading "third is 40 less than second" as b = z − 40.

## P4 — (E) 100ℓm/x
100 km = 100m miles. That takes 100m/x gallons, which is 100mℓ/x liters.
Sanity checks: higher mpg must give fewer liters, so x goes in the denominator. Larger ℓ or m must give more liters.

## P5 — (C) 2 − √2
P lies on AB and Q on BC, with AP = QC = s. Corner triangle PBQ is a right isosceles triangle with legs 1 − s and hypotenuse PQ = s. So √2(1 − s) = s, which gives s = √2/(1+√2) = 2 − √2.
Alternative: project A→P→Q→C onto AB: s + s·(√2/2) = 1.

## P6 — (A) 3 − 2a
√((a−1)²) = |a − 1| = 1 − a when a < 0. The inner expression becomes a − 2 − (1 − a) = 2a − 3, which is negative, so its absolute value is 3 − 2a. Check a = −1: the expression is 5, and only (A) gives 5.
Trap: replacing √((a−1)²) by a − 1 gives |−1| = 1, which is (C).

## P7 — (B) 6
18 = 2·3², 45 = 3²·5, 180 = 2²·3²·5. n divides 180.
The LCM takes the max exponent: the power of 2 is 2, the power of 5 is 1, and the power of 3 is at most 2.
The GCD with 45 takes the min exponent: min(b, 2) = 1, so b = 1.
So n = 60, and its digit sum is 6.

## P8 — (D) 36
The mean is (20 + X)/6 and must equal 1, 2, 5, 7 or X.
- Mean 1 gives X = −14. Rejected.
- Mean 2 gives X = −8. Rejected.
- Mean 5 gives X = 10.
- Mean 7 gives X = 22.
- Mean X gives X = 4.

Sum: 4 + 10 + 22 = 36.
Trap: forgetting mean = X gives 32, which is (C).

## P9 — (D) 540
TL, TR and BM all touch each other, so they need 5·4·3 = 60 colorings. BL touches only TL and BM, which have different colors: 3 choices. BR touches only TR and BM: 3 choices. Total: 60·9 = 540.
Alternative: BM first (5 ways), then the path BL–TL–TR–BR with 4 colors: 4·3·3·3 = 108. Total 5·108 = 540.

## P10 — (E) 18
Card x × y: x² + y² = 64. The inner notch corners are (1,1) and (x−1, y−1), so (x−2)² + (y−2)² = 32. Expanding gives 72 − 4(x+y) = 32, so x + y = 10. Then xy = ((x+y)² − (x²+y²))/2 = (100 − 64)/2 = 18.
The dimensions 5 ± √7 are real and both greater than 2.

## P11 — (C) 7
Use 4096 = 2^12. The left side is 2^(m−6) and the right side is 2^(1 − 12/m). Equal exponents give m² − 7m + 12 = 0, so m = 3 or 4. Both check. Sum = 7.

## P12 — (A) 7
Types: T (truth-teller), L (liar), A (alternater: truth, lie, truth), B (alternater: lie, truth, lie).
- Q1 "yes" comes from T, L and B: T + L + B = 22.
- Q2 "yes" comes from L and B: L + B = 15.
- Q3 "yes" comes from B only: B = 9.

So L = 6, T = 7 and A = 9. Truth-tellers say yes only to Q1, so they get 7 pieces.
Trap: liars answer "no" to "Are you a liar?".

## P13 — (C) 10
Angle bisector theorem: AB : AC = 2 : 3. Reflect B across AP to B′, which lies on AC with AB′ = 2k and B′C = k. Line BB′ ⟂ AP, so D is on line BB′. The homothety centred at B′ with ratio −2 sends C to A and B to D, so AD = 2·BC = 10.
Similar-triangle version: triangle AB′D ~ triangle CB′B with ratio AB′/CB′ = 2.

## P14 — (E) 144
None of 8–14 can be the smaller number of a pair, since 2·8 = 16 > 14. So pairs are {small from 1–7, large from 8–14} with large ≥ 2·small.
Assign partners from the most restricted:
- 7 → 14: 1 way.
- 6 → {12, 13}: 2 ways.
- 5 → {10..13} minus used: 3 ways.
- 4 → {8..13} minus used: 4 ways.
- 1, 2, 3 take the rest: 3! = 6 ways.

Total: 1·2·3·4·6 = 144.

## P15 — (D) 1565
7² + 24² = 15² + 20² = 625 = 25². Law of cosines on diagonal AC, together with B + D = 180°, forces B = D = 90°. So AC = 25 is a diameter.
The circle has area 625π/4. The quadrilateral has area 84 + 150 = 234.
The difference is (625π − 936)/4, so a + b + c = 625 + 936 + 4 = 1565.

## P16 — (D) 30
The new volume is (a+2)(b+2)(c+2) = abc + 2(ab+bc+ca) + 4(a+b+c) + 8. Vieta gives abc = 3/5, ab+bc+ca = 29/10 and a+b+c = 39/10. Total: 3/5 + 29/5 + 78/5 + 8 = 30.
Shortcut: p(−2) = −300 = −10·V, so V = 30. The roots are 3, 1/2 and 2/5.

## P17 — (D) 13
0.(abc repeating) = (100a+10b+c)/999, and the right side is (a+b+c)/27. So 100a + 10b + c = 37(a+b+c), which simplifies to 7a = 3b + 4c.
Mod 7: b ≡ c, so b = c or |b − c| = 7.
- b = c gives a = b = c: 9 numbers.
- |b − c| = 7 gives 481, 592, 518 and 629: 4 numbers.

Total: 13.
Trap: allowing a zero digit would add 407 and 370 (15 numbers, which is not a choice), so check that digits are nonzero.

## P18 — (A) 359
Track the angle θ of the point. T_k sends θ to 180 − k − θ. Two consecutive steps, T_k then T_{k+1}, send θ to θ − 1. So θ_{2m} = −m and θ_{2m+1} = 179 − m.
- Even n needs m ≡ 0 (mod 360), so n = 720.
- Odd n needs m = 179, so n = 359.

Minimum: 359.
Trap: only checking even n gives 720.

## P19 — (C) 5
L_17 = 17·L_16, so h = Σ L_17/k. Every term with k ≤ 16 is divisible by 17, so h ≡ L_16 (mod 17).
L_16 = 2⁴·3²·5·7·11·13 ≡ (−1)·9·(35)·(143) ≡ (−1)·9·1·7 = −63 ≡ 5 (mod 17).

## P20 — (E) 206
The second difference removes the arithmetic part: g(r−1)² = 57 − 120 + 91 = 28. Integrality and positivity, with a = 57 − g ≥ 1 and so on, force g = 7 and r = 3.
The geometric sequence is 7, 21, 63, 189. The arithmetic sequence is 50, 39, 28, 17. Fourth term: 189 + 17 = 206.
The case g = 28, r = 2 fails because an arithmetic term goes negative.

## P21 — (B) 7
Seen from above, each hexagon's top edge sits 1 unit outward from its square edge. The rim is horizontal at height √2, and the tilt is found from the shared edges.
The projected octagon has vertices (±1/2, ±3/2) and (±3/2, ±1/2). That is a 3×3 square minus 4 corner triangles of area 1/2, so the area is 9 − 2 = 7.
Decomposition: 1 (square) + 4 (rectangles) + 2 (triangles) = 7.
Note: this octagon is not regular (its sides alternate between 1 and √2). No simple mistake leads to (C).

## P22 — (D) 8178
Exactly two passes means the first pass takes 1..k and the second takes k+1..13, for some 1 ≤ k ≤ 12. Both blocks are increasing in position, and k+1 sits left of k.
Interleavings for a given k: C(13,k). Subtract 1 for the identity ordering.
Sum over k = 1..12: 2^13 − 2 − 12 = 8178. Check with n = 3: 4 orderings.

## P23 — (B) 1/3
Coordinates: A(−a,0), D(a,0), B(−b,h), C(b,h), P(x,y).
- PD² − PA² = −4ax = 15.
- PC² − PB² = −4bx = 5.

So 15/(4a) = 5/(4b), which gives a = 3b and BC/AD = 1/3. The configuration exists, for example with a = 2.
(Ptolemy's theorem on the cyclic trapezoid gives the same result.)

## P24 — (E) 1296
Sort the digits so that b1 ≤ … ≤ b5. The condition becomes b_j ≤ j − 1 for every j. These strings are called parking functions.

Casework on the number of zeros gives these counts:

| Zeros | Strings |
|---|---|
| 5 | 1 |
| 4 | 20 |
| 3 | 150 |
| 2 | 500 |
| 1 | 625 |

The total is 1296 = 6^4.

Pollak's circle argument gives the same count. Use 6 spots on a circle, so there are 6^5 strings with digits mod 6. Rotating every digit by the same amount gives 6 strings, and exactly one of them leaves spot 5 empty. That gives 6^5 / 6 = 6^4.

Small checks match the formula: length 2 gives 3 strings, and length 3 gives 16.

## P25 — (B) 337
Let the edge lengths be r, s, t, and let T span x from −a to b, so a + b = t. A square of side n holds (n+1)² lattice points.

1. The 9/4 condition gives r+1 = 3m and s+1 = 2m.
2. R and S share the 2m lattice points on the y-axis. So |R ∪ S| = 9m² + 4m² − 2m = 13m² − 2m.
3. |S∩T| = (a+1)(t+1) and |R∩T| = (b+1)(t+1). The y-axis points of T are counted in both.
4. The "27 times" condition gives (a+1)/(4m²) = 27(b+1)/(9m²). So a+1 = 12(b+1), which means t+1 = 13(b+1) − 1.
5. The "1/4" condition gives 4(t+1)² = m(13m − 2). Here m must be even, so write m = 2n. Then (t+1)² = n(13n − 1).
6. The factors n and 13n − 1 share no common factor, so each is a perfect square: n = p² and 13p² − 1 = q².
7. Try p = 1 to 4: none works. p = 5 gives q = 18. So m = 50, t+1 = pq = 90, and t+1 = 90 = 13·7 − 1 works with b = 6 and a = 83.
8. This gives r = 149, s = 99, t = 89. The sum is 337, and the sum increases with p, so 337 is the minimum.

Trap: forgetting the shared y-axis points in |R ∪ S|, or the y-axis points of T.
