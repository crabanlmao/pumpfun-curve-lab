from dataclasses import dataclass

LAMPORTS = 1_000_000_000
INIT_VSOL = 30 * LAMPORTS
INIT_VTOK = 1_073_000_000_000_000


@dataclass(frozen=True)
class Curve:
    vsol: int = INIT_VSOL
    vtok: int = INIT_VTOK

    @property
    def price(self):
        return self.vsol / self.vtok

    def buy_exact_sol(self, lamports):
        tokens = self.vtok * lamports // (self.vsol + lamports)
        return tokens, Curve(self.vsol + lamports, self.vtok - tokens)

    def cost_for_tokens(self, tokens):
        if not 0 < tokens < self.vtok:
            raise ValueError("tokens out of range")
        return -(-self.vsol * tokens // (self.vtok - tokens))

    def buy_tokens(self, tokens):
        cost = self.cost_for_tokens(tokens)
        return cost, Curve(self.vsol + cost, self.vtok - tokens)

    def sell(self, tokens):
        out = self.vsol * tokens // (self.vtok + tokens)
        return out, Curve(self.vsol - out, self.vtok + tokens)

    def entry_slippage(self, lamports):
        tokens, _ = self.buy_exact_sol(lamports)
        return (lamports / tokens) / self.price - 1.0
