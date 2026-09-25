# 2018 AMC 10B — verified solution methods

Each problem was solved by 2 independent blind solvers using the
math-olympiad skill (reasoning only, no tools). The official answer key was
the third vote. Every problem was unanimous (3 of 3) unless noted.

## P1 — (A) 90
10 pieces fit along the 20-inch side and 9 along the 18-inch side: 10 · 9 = 90. Check by area: 360 / 4 = 90.
Traps: giving the pan's area, 360, is (E); dividing the area by 2 instead of by the piece area 4 gives 180, which is (C).

## P2 — (D) 67
Each 30 minutes is half an hour. First half hour: 30 miles. Second: 32.5 miles. Last: 96 − 62.5 = 33.5 miles in half an hour, so 67 mph.
Alternative: the three intervals are equal, so the overall average 96/1.5 = 64 is the mean of the three speeds: (60 + 65 + v)/3 = 64 gives v = 67.
Trap: answering with the overall average speed, 64, is (A).

## P3 — (B) 3
Swapping the two numbers inside a product, or swapping the two products, does not change the value. So only the way {1,2,3,4} splits into two pairs matters, and the partner of 1 decides it: 3 splits.
1·2 + 3·4 = 14, 1·3 + 2·4 = 11, 1·4 + 2·3 = 10. All different, so 3 values.
Traps: counting the 4! = 24 fillings as values gives (E); dividing out only the swaps inside each product (24/4) gives 6, which is (D).

## P4 — (B) 22
Opposite faces are equal, so the three face areas are XY, YZ, ZX = 24, 48, 72. Multiply: (XYZ)² = 24 · 48 · 72 = 2^10 · 3^4, so XYZ = 288. Then the edges are 288/48 = 6, 288/72 = 4, 288/24 = 12. Sum 22.
Check: 6·4 = 24, 4·12 = 48, 6·12 = 72.
Alternative: ZX/XY = 3 gives Z = 3Y; then YZ = 3Y² = 48 gives Y = 4.

## P5 — (D) 240
Complementary counting. All subsets: 2^8 = 256. Subsets with no prime use only 4, 6, 8, 9: 2^4 = 16 (including the empty set). 256 − 16 = 240.
Alternative: a nonempty set of primes (15 ways) times any set of non-primes (16 ways) = 240.
Traps: forgetting to subtract gives 256 (E); forgetting that 2 is prime gives 256 − 32 = 224 (C).

## P6 — (D) 1/5
Exactly 3 draws are needed when the first two chips add to at most 4 (the third chip then always pushes the sum above 4). The only such pairs are {1,2} and {1,3}. The first two chips are a random 2-element set, one of C(5,2) = 10, so the probability is 2/10 = 1/5.
Same with order: 4 ordered pairs out of 5 · 4 = 20.
Trap: counting the unordered pairs {1,2}, {1,3} over the 20 ordered outcomes gives 2/20 = 1/10, which is (B).

## P7 — (D) 19
If each small radius is r, the large radius is Nr. A = N · (πr²/2), and the large semicircle has area N² · (πr²/2). So B = (N² − N)(πr²/2) and A : B = N : N(N − 1) = 1 : (N − 1). Then N − 1 = 18, so N = 19.
Trap: reading 1 : 18 as A compared with the whole large semicircle gives N = 18, which is (C).

## P8 — (C) 12
Count horizontal toothpicks by level: the rows have n, n − 1, …, 1 squares, so the horizontal lines have 1, 2, …, n, n toothpicks, a total of n(n + 1)/2 + n. The staircase is symmetric about its diagonal, so there are equally many vertical toothpicks. Total T(n) = n(n + 1) + 2n = n(n + 3). Check: T(3) = 18.
n(n + 3) = 180 gives n = 12 (12 · 15 = 180).
Alternative: going from n − 1 to n steps adds 2n + 2 toothpicks: 4, 10, 18, 28, …, 180 at n = 12.
Trap: assuming the count grows in proportion (18 → 180 means 10 times as many steps) gives 30, which is (E).

## P9 — (D) 39
Replace every top face x by 7 − x. This pairs up the outcomes one-to-one and turns a sum S into 7 · 7 − S = 49 − S. So sum 10 and sum 49 − 10 = 39 are equally likely.
Check: sum 7 (all ones) and sum 42 (all sixes) each happen in exactly one way, and 7 + 42 = 49.
Trap: reflecting through the maximum instead, 42 − 10 = 32, gives (C).

## P10 — (E) 2
The base BCHE cuts the box in half. The upper half is a triangular prism with cross-section triangle BFE (legs 3 and 2, area 3) and length 1, so its volume is 3. That prism is the pyramid M-BCHE plus two small pyramids M-BFE and M-CGH. Each small one has base area 3 and height 1/2 (M is halfway along FG), so volume (1/3)(3)(1/2) = 1/2. The pyramid is 3 − 1/2 − 1/2 = 2.
Coordinate check: the base is a √13 × 1 rectangle in the plane 2x + 3z = 6, and M = (3, 1/2, 2) is 6/√13 from it: (1/3)(√13)(6/√13) = 2.
Trap: using 1/6 instead of 1/3 in the pyramid volume formula gives 1, which is (A).

## P11 — (C) p² + 26
Every prime p other than 3 leaves remainder 1 or 2 when divided by 3, so p² leaves remainder 1. Then p² + 26 leaves remainder 1 + 26 = 27, a multiple of 3, and it is bigger than 3, so it is not prime. For p = 3: 9 + 26 = 35 = 5 · 7, not prime either.
Each other choice is prime for some prime p: 5² + 16 = 41, 7² + 24 = 73, 5² + 46 = 71, 19² + 96 = 457.
Traps: forgetting to check p = 3 separately (the remainder argument does not cover it). For (E), the primes 2 through 17 all give composite values, so stopping early makes (E) look right; p = 19 gives the prime 457.

## P12 — (C) 50
Put the circle's center O at the origin, so A and B are opposite points and A + B = 0. The centroid is G = (A + B + C)/3 = C/3. So G moves on a circle of radius 12/3 = 4 about O, missing the two points where C = A or C = B.
Area: 16π ≈ 50.27, so 50.
Alternative: OC is the median from C (O is the midpoint of AB), and the centroid is 1/3 of the way from O to C.
Traps: computing the circumference 8π ≈ 25 instead of the area gives (A); using the big radius in the circumference, 24π ≈ 75, gives (E).

## P13 — (C) 505
The terms are 10^n + 1 for n = 2, 3, …, 2019. Since 10² = 100 ≡ −1 (mod 101), powers of 10 repeat every 4 steps: 10^n ≡ 1, 10, −1, −10 for n ≡ 0, 1, 2, 3 (mod 4). So 101 divides 10^n + 1 exactly when n ≡ 2 (mod 4): n = 2, 6, …, 2018, which is (2018 − 2)/4 + 1 = 505 terms.
Check: 101 = 101 · 1 and 1000001 = 101 · 9901 work; 1001, 10001, 100001 do not.
Traps: counting n ≡ 0 (mod 4) instead gives 504 (B); thinking every even exponent works gives 1009 (E).

## P14 — (D) 225
The mode appears 10 times, and every other value at most 9 times. With k distinct values the list holds at most 10 + 9(k − 1) numbers. We need 10 + 9(k − 1) ≥ 2018, so k − 1 ≥ 2008/9 ≈ 223.1, so k − 1 ≥ 224 and k ≥ 225. (With 224 values the most is 2017.)
Construction: one value 10 times, 223 values 9 times each, one value once: 10 + 2007 + 1 = 2018.
Traps: rounding 223.1 down gives 223 (B); rounding up correctly but forgetting to add the mode itself gives 224 (C).

## P15 — (A) 2(w + h)²
Look along the line from the sheet's center to one of its corners. It is perpendicular to one edge of the base, and it hits that edge at the edge's midpoint, w/2 from the center. When the corner is folded up the side and over the top to A, the paper along this line must cover h up the side and then w/2 across the top. So the center-to-corner distance (half the sheet's diagonal) is w/2 + h + w/2 = w + h. The diagonal is 2(w + h), so the area is (diagonal)²/2 = 2(w + h)².
Check h = 0: a flat square of side w folded like an envelope needs a sheet of area 2w², which matches.
Traps: using the box's surface area 2w² + 4wh gives (C); ignoring the height gives 2w² (D); treating w + h as the full diagonal instead of half gives (w + h)²/2, which is (B).

## P16 — (E) 4
For every integer n, n³ − n = (n − 1)n(n + 1) is a product of three consecutive integers, so it is divisible by 2 and by 3, hence by 6. So the sum of the cubes leaves the same remainder mod 6 as the sum itself, 2018^2018.
2018 ≡ 2 (mod 6), and powers of 2 mod 6 go 2, 4, 2, 4, …; the exponent 2018 is even, so the remainder is 4.
Check: 2018^2018 is even and is 1 more than a multiple of 3 (2018 ≡ −1 mod 3, even power), and 4 is the only remainder mod 6 that is both.
Traps: reducing the base to 2 and forgetting the exponent gives 2 (C); "it is even and huge, so divisible by 6" gives 0 (A).

## P17 — (B) 7
Let the side be s. The four corner triangles have legs x along the length-8 sides and y along the length-6 sides (the equal sides force all four corners to match), so s = 8 − 2x = 6 − 2y and s² = x² + y².
With x = (8 − s)/2 and y = (6 − s)/2: 4s² = (8 − s)² + (6 − s)², so s² + 14s − 50 = 0 and s = −7 ± 3√11. The side is positive: s = −7 + 3√11 ≈ 2.95 (then x ≈ 2.5 < 4). So k + m + n = −7 + 3 + 11 = 7.
Traps: taking the negative root −7 − 3√11 gives −7 − 3 + 11 = 1 (A); dropping the minus sign on k gives 7 + 3 + 11 = 21 (C).

## P18 — (D) 96
Seats: second row a1 a2 a3, third row b1 b2 b3 (b directly behind a). Put any of the 6 children in the middle front seat a2. That child's sibling cannot sit in a1 or a3 (next to it) or b2 (behind it), so it goes in b1 or b3: 2 ways. Say b1. The child in b3 has a sibling who cannot sit in b2 (next to it) or a3 (in front of it), so that sibling must take a1: 4 choices for the b3 child. The last pair takes a3 and b2, which are diagonal, in either order: 2 ways.
Total 6 · 2 · 4 · 2 = 96.
Alternative: each row must hold one child from each family; choose the front-row child of each family (8), order the front row (6), and order the back row so no one is behind their sibling (2): 8 · 6 · 2 = 96.

## P19 — (E) 11
Age differences never change. Let d = Chloe's age − Zoe's age. When Zoe is z, Chloe is z + d, which is a multiple of z exactly when z divides d. So the number of such birthdays is the number of divisors of d, which is 9. Numbers with 9 divisors look like p²q² or p^8: 36, 100, 196, …. A realistic parent gives d = 36, so Chloe is 37 and Joey is 38. (The question's "two digits" confirms it: with d = 100 or 196, Joey's next good age would be 202 or 394.)
Joey's age z + 37 is a multiple of z exactly when z divides 37, which is prime. After today (z = 1) the next time is z = 37, when Joey is 74 = 2 · 37. Digit sum 7 + 4 = 11.
Check: Chloe's good birthdays come when Zoe is 1, 2, 3, 4, 6, 9, 12, 18, 36 — nine of them.

## P20 — (B) 2017
Write the recursion for n and n + 1 and add them: f(n + 1) = −f(n − 2) + 2n + 1. Doing it again three steps later and subtracting gives f(m + 6) = f(m) + 6 for all m ≥ 1.
2018 = 2 + 6 · 336, so f(2018) = f(2) + 6 · 336 = 1 + 2016 = 2017.
Check: f(1…10) = 1, 1, 3, 6, 8, 8, 7, 7, 9, 12, and each term is the one six places before plus 6.
Traps: guessing f(n) = n from values like f(7) = 7 gives 2018 (C).

## P21 — (C) 340
323 = 17 · 19. Let d be the next divisor after 323. If d shared no factor with 323, then n would be a multiple of 323 · d ≥ 323 · 324 > 9999, too big. So d is a multiple of 17 or 19 above 323: the smallest is 340 = 17 · 20 (next are 342 = 18 · 19 and 357).
340 works: n = 2² · 5 · 17 · 19 = 6460. A divisor strictly between 323 and 340 would pair with a divisor strictly between 6460/340 = 19 and 6460/323 = 20, and there is none.
Traps: 324 (A) or 330 (B) ignore that the next divisor must share a factor with 323; 646 (E) assumes the next divisor must be 2 · 323. (361 = 19² is impossible: n would need to be a multiple of 2 · 17 · 361 = 12274.)

## P22 — (C) 0.29
x and y are at most 1, so the side 1 is the longest, and the triangle is obtuse exactly when the angle across from it is: x² + y² < 1. A triangle exists when x + y > 1 (the other two conditions always hold). In the unit square this is the quarter circle minus the triangle below x + y = 1: π/4 − 1/2 ≈ 0.785 − 0.5 = 0.285, closest to 0.29.
Traps: forgetting the triangle condition gives π/4 ≈ 0.79 (E); finding only the probability of a triangle gives 0.50 (D); using the acute condition x² + y² > 1 gives 1 − π/4 ≈ 0.21 (A).

## P23 — (B) 2
Let g = gcd and L = lcm. Since a · b = g · L, the equation is gL + 63 = 20L + 12g, which factors as (L − 12)(g − 20) = 177 = 3 · 59. Both factors must be positive (negative ones make g or L negative). The four options for (L, g) are (13, 197), (15, 79), (71, 23), (189, 21), and only the last has g dividing L.
So g = 21, L = 189, and a = 21m, b = 21n with mn = 9 and m, n sharing no factor: (1, 9) or (9, 1). The pairs are (21, 189) and (189, 21).
Check: 21 · 189 + 63 = 4032 = 20 · 189 + 12 · 21.
Trap: counting all four factor pairs without checking that the gcd divides the lcm gives 4, which is (C).

## P24 — (C) 15√3/32
Triangle XYZ is equilateral with side 3/2, area 9√3/16. Each of its corners pokes out past one side of triangle ACE, so the hexagon is XYZ with three small corner triangles cut off. At X, line AC cuts XY at distance 1/2 from X and XZ at distance 1/4 from X, with a 60° angle between, so each corner has area (1/2)(1/2)(1/4)(√3/2) = √3/32. Hexagon = 9√3/16 − 3√3/32 = 15√3/32.
Check from the other triangle: ACE has side √3 and area 3√3/4 = 24√3/32; each side of XYZ cuts off an equilateral corner of side 3/4 (area 3√3/32), and 24√3/32 − 9√3/32 = 15√3/32.
Traps: stopping at the area of XYZ gives 9√3/16 (E); assuming the cut-off corners are equilateral with side 1/2 (or that the hexagon is regular with side 1/2) gives 3√3/8 (A). The hexagon's sides actually alternate 3/4 and √3/4.

## P25 — (C) 199
Divide by 10,000: x²/10000 = x − ⌊x⌋, the fractional part of x, which is in [0, 1). So x² < 10000 and −100 < x < 100.
On each stretch [n, n + 1), the fractional part climbs from 0 toward 1 while x²/10000 changes much more slowly, so the two cross exactly once, as long as x²/10000 is still below 1 at the right end: (n + 1)² < 10000, that is −101 < n < 99. At n = 0 the crossing is x = 0 itself.
So n runs from −100 to 98: 199 values of n, one solution each.
Traps: counting every stretch from −100 to 99 forgets that on [99, 100) the parabola reaches 1 only at x = 100, which is not included: 200 (D). Also counting x = ±100 as solutions pushes the count higher (E).
