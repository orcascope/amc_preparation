# 2018 AMC 10A — verified solution methods

Each problem was solved by 2 independent blind solvers using the
math-olympiad skill (reasoning only, no tools). The official answer key was
the third vote. Every problem was unanimous (3 of 3) unless noted.

## P1 — (B) 11/7
Work from the inside out, repeating "take the reciprocal, then add 1": 3 → 1/3 + 1 = 4/3 → 3/4 + 1 = 7/4 → 4/7 + 1 = 11/7.
Pattern: x ↦ (x+1)/x, so each new numerator is numerator + denominator: 3/1, 4/3, 7/4, 11/7.
Trap: stopping one step early (7/4) or dropping the final +1 (4/7); neither is a choice, which is a useful warning sign.

## P2 — (A) 20% more
With Jacqueline's amount J: L = 1.5J and A = 1.25J, so L/A = 1.5/1.25 = 6/5. Liliane has 20% more than Alice.
Check with J = 4: L = 6, A = 5, and 6 is 20% more than 5.
Trap: subtracting the percentages (50% − 25% = 25%) gives (B). Percent increases compare by division, not subtraction.

## P3 — (E) February 12
Group the factors of 10!: 10! = (10·6)·(3·4·5)·(2·7·8·9) = 60 · 60 · 1008. So 10! seconds = 1008 hours = 42 days.
Noon on January 1 plus 42 days is "January 43" = February 12 (January has 31 days).
Trap: counting January 1 as day 1 of the 42 gives February 11, which is (D).

## P4 — (E) 24
First choose the 3 periods, no two adjacent: the 3 non-math periods leave 4 gaps (two ends and two middles), and choose 3 of them: C(4,3) = 4. The sets are {1,3,5}, {1,3,6}, {1,4,6}, {2,4,6}.
Then assign the three different courses: 3! = 6. Total 4 · 6 = 24.
Traps: only the "alternating" sets {1,3,5} and {2,4,6} give 12 (C); finding only 3 of the 4 sets gives 18 (D); forgetting that the courses are different gives 4.

## P5 — (D) (5, 6)
All three statements are false, so negate each one: Alice false → d < 6; Bob false → d > 5; Charlie false → d > 4. The overlap is 5 < d < 6.
Traps: ignoring Alice's statement gives (5, ∞), which is (E); ignoring Bob's gives (4, 6), which is (C). Endpoints are excluded: at d = 5 Bob is telling the truth, and at d = 6 Alice is.

## P6 — (B) 300
With N votes: likes 0.65N, dislikes 0.35N, and the score is the difference, 0.30N = 90. So N = 300.
Check: 195 likes, 105 dislikes, 195 − 105 = 90, and 195/300 = 65%.
Alternative: every 20 votes are 13 likes and 7 dislikes, which adds 6 to the score; 90/6 = 15 blocks of 20 = 300.
Trap: measuring from half the votes (65% − 50% = 15% of N = 90) gives 600, which is (E).

## P7 — (E) 9
4000 = 2^5 · 5^3, so 4000·(2/5)^n = 2^(5+n) · 5^(3−n). This is an integer exactly when both exponents are ≥ 0: −5 ≤ n ≤ 3. That is 9 integers.
Check the ends: n = 3 gives 256 and n = −5 gives 390625; one step further in either direction leaves a factor of 5 or 2 in the denominator.
Traps: counting only n ≥ 0 gives 4 (B); forgetting n = 0 gives 8 (D).

## P8 — (C) 2
Let n be the number of 5-cent coins. Then there are n + 3 dimes and q = 23 − (2n + 3) = 20 − 2n quarters.
Value: 5n + 10(n + 3) + 25(20 − 2n) = 320, so 530 − 35n = 320 and n = 6. Then 9 dimes and 8 quarters.
Check: 6 + 9 + 8 = 23 coins and 30 + 90 + 200 = 320 cents. Answer: 8 − 6 = 2.
Trap: answering the dimes-minus-nickels gap, 3, instead of the question gives (D).

## P9 — (E) 24
All triangles are similar, so areas scale with the square of the side ratio. DE is made of 4 bases of the smallest triangles (the 4 upward triangles sit side by side on it), so triangle ADE is 4 times as wide as a smallest triangle and has area 4² · 1 = 16.
Check: the segment above the strip is 3 small bases wide, so the top triangle has area 9, and 9 + 7 = 16.
Trapezoid DBCE = 40 − 16 = 24.
Traps: subtracting only the 7 small triangles gives 33, and scaling area linearly gives other non-choices. No common slip lands on another listed choice.

## P10 — (A) 8
Let a = √(49 − x²) and b = √(25 − x²). Then a² − b² = 24 no matter what x is. Since a² − b² = (a − b)(a + b) and a − b = 3, a + b = 24/3 = 8.
Existence check: a = 5.5, b = 2.5 give x² = 18.75, which works in both roots.
Trap: plugging in x = 0 without checking gives 7 + 5 = 12, which is (E). But x = 0 does not satisfy the equation (7 − 5 = 2, not 3).

## P11 — (E) 84
Subtract 1 from each die: e_i = d_i − 1 ≥ 0 with e_1 + … + e_7 = 3. No e_i can exceed 3, so the "at most 6" limit never matters. Stars and bars: C(9,3) = 84.
Check by cases on the 3 extra pips: all on one die, 7 ways; 2 and 1 on two dice, 7·6 = 42 ordered ways; 1 each on three dice, C(7,3) = 35. Total 84.
Traps: treating the {2,1} case as unordered (C(7,2) = 21) gives 63, which is (D); forgetting the {1,1,1} case gives 49, which is (B).

## P12 — (C) 3
From the line, x = 3 − 3y, so x ≥ 0 exactly when y ≤ 1. Split on the sign of y:
- y < 0: |x| − |y| = 3 − 2y = ±1 gives y = 1 or 2, neither negative. No solutions.
- 0 ≤ y ≤ 1: |x| − |y| = 3 − 4y = ±1 gives y = 1/2 (x = 3/2) or y = 1 (x = 0).
- y > 1: |x| − |y| = 2y − 3 = ±1 gives y = 2 (x = −3); y = 1 is not in this range.

Solutions: (3/2, 1/2), (0, 1), (−3, 2). All three check.
Picture: ||x| − |y|| = 1 is four V-shapes with vertices (±1, 0) and (0, ±1); the line passes exactly through the vertex (0, 1).
Traps: counting (0, 1) twice because y = 1 appears in two cases gives 4 (D); expecting a symmetric answer of 8 (E), but the line is not symmetric.

## P13 — (D) 15/8
Every point on the crease is the same distance from A and from B, so the crease lies on the perpendicular bisector of AB. It starts at the midpoint M of AB (AM = 5/2) and ends on leg AC (the long leg), at D with AD = 25/8 < 4.
Triangles AMD and ACB are right triangles sharing angle A, so they are similar: MD/AM = BC/AC = 3/4. So MD = (5/2)(3/4) = 15/8.
Coordinate check: A = (0,0), C = (4,0), B = (4,3); M = (2, 3/2); the bisector has slope −4/3 and meets y = 0 at x = 25/8. Length √((9/8)² + (12/8)²) = 15/8.
Traps: using the ratio upside down (AM · 4/3) gives 10/3, not a choice. Joining the midpoints of AB and BC gives 2 (E), but that segment is not the perpendicular bisector.

## P14 — (A) 80
Let x = 3^96 and y = 2^96. The fraction is (81x + 16y)/(x + y) = 81 − 65y/(x + y). The subtracted part is positive, and it is less than 1 because 64y < x, that is, 2^102 < 3^96 (true since 3^96 = 9^48 > 8^48 = 2^144). So the value is strictly between 80 and 81, and the answer is 80.
Idea: the fraction is a weighted average of 81 and 16 with almost all the weight on 81, so it is just under 81.
Traps: keeping only the big terms gives 81 (B), but the small terms pull it just below 81. Dividing term by term gives 81 + 16 = 97 (D). Treating the sums as (3 + 2)^k gives 5^4 = 625 (E).

## P15 — (D) 69
Let O be the big center and P, Q the small centers. Internal tangency: OP = OQ = 13 − 5 = 8, and the tangency points lie on the lines of centers, so A is on ray OP and B is on ray OQ with OA = OB = 13. External tangency: PQ = 10.
Triangles OAB and OPQ share the angle at O and have OA/OP = OB/OQ = 13/8, so they are similar. AB = 10 · 13/8 = 65/4, and 65 + 4 = 69.
Trap: using the ratio upside down gives AB = 10 · 8/13 = 80/13, so m + n = 93, which is (E).

## P16 — (D) 13
AC = √(400 + 441) = 29. The shortest segment from B to AC is the altitude, 20·21/29 = 420/29 ≈ 14.48 (between 14 and 15, since 14·29 = 406 and 15·29 = 435).
As the endpoint X slides from A to the foot H of the altitude, BX shrinks steadily from 20 to 14.48; from H to C it grows steadily from 14.48 to 21.
- A side: integer lengths 15, 16, …, 20, so 6 segments (including AB).
- C side: 15, 16, …, 21, so 7 segments (including BC).

Total 6 + 7 = 13. The altitude itself is not an integer, so nothing is counted twice.
Traps: counting each length only once gives 7 (not a choice). Counting 15–20 on both sides but forgetting 21 (BC) gives 12, which is (C).

## P17 — (C) 4
Split 1–12 into 6 chains in which each number divides the later ones: {1,2,4,8}, {3,6,12}, {5,10}, {7}, {9}, {11}. S can take at most one number from each chain, and |S| = 6, so it takes exactly one from each. So 7, 9 and 11 are in S.
- 1 is out (it divides everything).
- 3 is out, because 9 is in S.
- So S takes 6 or 12 from the chain {3,6,12}, and both are even, so 2 is out.

So every element is at least 4. The set {4, 5, 6, 7, 9, 11} works, so the least possible value is 4.
Traps: starting with the primes {2,3,5,7,11} and not seeing that no sixth number fits leads to 2 (A). Missing that 9 is forced leads to 3 (B). Stopping at the easy valid set {7, 8, 9, 10, 11, 12} gives 7 (E).

## P18 — (D) 3281
Add 3280 = 1 + 3 + … + 3^7 = (3^8 − 1)/2 to the expression. The digits become a_i + 1 ∈ {0, 1, 2}, which is ordinary base 3 with 8 digits. That covers every integer from 0 to 3^8 − 1 = 6560 exactly once. So the expression takes every integer from −3280 to 3280 exactly once.
The nonnegative ones are 0, 1, …, 3280: that is 3281.
Alternative: negating every digit shows the values are symmetric about 0, so (6561 + 1)/2 = 3281 are nonnegative.
Trap: using only 7 digits instead of 8 gives (3^7 + 1)/2 = 1094, which is (C). Forgetting to count 0 gives 3280 (not a choice).

## P19 — (E) 2/5
There are 5 · 20 = 100 equally likely pairs. Only the last digit of m matters. The 20 values of n contain exactly 5 of each remainder mod 4, and 10 even numbers.
- 11: always ends in 1, so 20 values of n.
- 13: 3, 9, 7, 1 repeats; ends in 1 when 4 | n, so 5 values.
- 15: always ends in 5, so 0 values.
- 17: 7, 9, 3, 1 repeats; ends in 1 when 4 | n, so 5 values.
- 19: 9, 1 repeats; ends in 1 when n is even, so 10 values.

Total 40/100 = 2/5.
Traps: treating 19 like 13 and 17 (only when 4 | n) gives 35/100 = 7/20 (D). Leaving out the 19 case gives 30/100 = 3/10 (C).

## P20 — (B) 1022
Symmetric means unchanged by all 8 symmetries of the square (4 rotations and 4 reflections). Cells that the symmetries move onto each other must have the same color, so count these groups of cells.
Put the center at (0,0). Every cell can be moved to exactly one cell (a, b) with 0 ≤ b ≤ a ≤ 3, which gives 1 + 2 + 3 + 4 = 10 groups. Check the sizes: 1 (center) + 3·4 (on the axes) + 3·4 (on the diagonals) + 3·8 (the rest) = 49.
Each group is black or white: 2^10 = 1024. Remove all-black and all-white: 1022.
Traps: using only the rotations gives 13 groups and 2^13 − 2 = 8190 (C), or 8192 (D) if you also forget to subtract 2. Forgetting to subtract 2 with the right count gives 1024 (not a choice).

## P21 — (E) a > 1/2
From the parabola, x² = y + a. Substitute into the circle: y² + y + a − a² = 0, which factors as (y + a)(y + 1 − a) = 0.
- y = −a gives x² = 0: the single point (0, −a), the parabola's vertex, for every a.
- y = a − 1 gives x² = 2a − 1: two new points when a > 1/2, the vertex again when a = 1/2, and nothing when a < 1/2.

So there are exactly 3 points exactly when a > 1/2. Check a = 1: (0, −1) and (±1, 0).
Alternative: eliminating y gives x²(x² − (2a − 1)) = 0, and each real x gives one point.
Trap: at a = 1/2 the "new" points collapse onto the vertex, so a = 1/2 gives only 1 point; choosing (D) misses this.

## P22 — (D) 13
24 = 2^3·3, 36 = 2^2·3^2, 54 = 2·3^3. A gcd takes the smaller exponent of each prime.
- b has 3^2 (from 36), and gcd(a, b) has only 3^1, so a has exactly 3^1.
- b has 2^3 (from 24), and gcd(b, c) has only 2^2, so c has exactly 2^2. Then gcd(c, d) has only 2^1, so d has exactly 2^1.
- a has at least 2^3 and d has at least 3^3.

So gcd(d, a) has exactly one 2 and one 3: it is 6k with k not divisible by 2 or 3. Between 70 and 100 that forces k = 13 (k = 12, 14, 15, 16 all fail), so gcd(d, a) = 78 and 13 divides a.
Example: a = 312, b = 72, c = 108, d = 702 satisfies everything, and 312 is not divisible by 5, 7, 11 or 17.
Trap: stopping at "gcd(d, a) is a multiple of 6" and picking 84 or 90 from 72, 78, 84, 90, 96 leads to 7 (B) or 5 (A).

## P23 — (D) 145/147
Put the right angle at the origin with the legs on the axes, so the hypotenuse is 3x + 4y = 12. A square of side s has far corner P = (s, s), which is its closest point to the hypotenuse.
Area method: join P to the three corners of the field. The three triangles have areas (1/2)(3)(s), (1/2)(4)(s) and (1/2)(5)(2) = 5, and they add up to the field's area 6. So 7s/2 = 1 and s = 2/7.
Planted fraction: (6 − 4/49)/6 = 1 − 2/147 = 145/147.
Coordinate check: |7s − 12|/5 = 2 gives s = 2/7 or 22/7; the second puts P outside the field.
Trap: assuming the square's diagonal lies along the altitude from the right angle (length 12/5) gives diagonal 2/5, area 2/25, and fraction 1 − 1/75 = 74/75, which is (E). The diagonal bisects the right angle, which is not the altitude direction unless the legs are equal.

## P24 — (D) 75
Angle bisector theorem: BG/GC = AB/AC = 50/10 = 5. Triangles ABG and AGC have the same height from A, so [ABG] = (5/6)(120) = 100.
DE is the midline (D, E midpoints), so it cuts every segment from A to BC in half: F is the midpoint of AG. Triangle ADF is triangle ABG shrunk by 1/2 from A, so [ADF] = (1/2)² · 100 = 25.
[FDBG] = [ABG] − [ADF] = 100 − 25 = 75.
Check: [ADE] = 120/4 = 30, and inside ADE the bisector splits DE in the ratio DF : FE = AD : AE = 5 : 1, so [ADF] = (5/6)(30) = 25 again.
Traps: subtracting all of triangle ADE (30) instead of ADF gives 70, which is (C). Shrinking area by 1/2 instead of 1/4 gives 100 − 50 = 50 (not a choice).

## P25 — (D) 18
With x = 10^n: A_n = a(x − 1)/9, B_n = b(x − 1)/9, C_n = c(x² − 1)/9. Divide the equation by (x − 1)/9 (never zero) and rearrange:
(9c − a²)·x + (9c − 9b + a²) = 0.
This is linear in x. If it holds for two different n (two different x), both coefficients must be 0: a² = 9c and b = 2a²/9. Then it holds for every n.
So 3 | a: a = 3 gives (b, c) = (2, 1), sum 6; a = 6 gives (8, 4), sum 18; a = 9 gives b = 18, not a digit.
Check a = 6, b = 8, c = 4: 44 − 8 = 36 = 6², and 4444 − 88 = 4356 = 66².
Alternative: use n = 1 and n = 2 directly: 11c − b = a² and 101c − b = 11a² give a² = 9c and b = 2c; the linear form shows these are also enough for every n.
Traps: forgetting that b must be a single digit leads to a = 9 and sum 36 (not a choice). Requiring the equation for only one n allows triples like (9, 7, 8), sum 24 (not a choice; it fails at n = 2).
