# Measured on the real venue

pump.fun on Solana, July to October 2026, from private data that is not in this repo. None of this is a profitable strategy.

- Early holders sell into the crossing: 111,913 SOL sold vs 35,989 bought (3.11:1), net sellers on 90% of 2,264 coins.
- A buy decided as a coin crossed 50 virtual SOL filled at a median of 70.9, 1.2 s later (2,708 coins).
- At entry the next move is close to a coin flip, and holding loses about 0.14 points per second (591 coins).
- Round trip cost 6.21% at the clip first deployed and 3.97% at the best clip, about a quarter the size.
- Price is the ratio of the virtual reserves. The constant K is not constant on this venue: it drifted a median 82% inside one position. Each event's own paid price vs the reserves: median ratio 0.998, 92% within 5%.
- Every PumpSwap pool made by migration prices trades on a virtual SOL reserve 17.5845 SOL above what it holds, implied by each pool's own sales on 44 pools. The venue's events only report the real balance.
- On 2026-10-08 the program's `Global` account grew by one trailing byte without the published interface changing.
