import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

OUT = pathlib.Path(__file__).parent
FONT = "DejaVu Sans"
LINE_H = 0.22
PAD = 0.14

class Box:
    def __init__(self, name, role, members, kind="", abstract=False):
        self.name, self.role, self.members, self.kind, self.abstract = name, role, members, kind, abstract
        self.w = self.h = self.cx = self.cy = 0.0
    def top(self, fx=0.5): return (self.cx - self.w/2 + fx*self.w, self.cy + self.h/2)
    def bottom(self, fx=0.5): return (self.cx - self.w/2 + fx*self.w, self.cy - self.h/2)
    def left(self, fy=0.5): return (self.cx - self.w/2, self.cy + self.h/2 - fy*self.h)
    def right(self, fy=0.5): return (self.cx + self.w/2, self.cy + self.h/2 - fy*self.h)

def measure(fig, ax, boxes):
    r = fig.canvas.get_renderer()
    def width(text, size, weight="normal", style="normal"):
        t = ax.text(0, 0, text, fontsize=size, fontname=FONT, fontweight=weight, fontstyle=style)
        w = t.get_window_extent(r).width / fig.dpi
        t.remove()
        return w
    for b in boxes:
        ws = [width("["+b.role+"]", 7.5), width(b.name, 9.5, "bold"), *[width(m, 8.5) for m in b.members]]
        if b.kind: ws.append(width("«"+b.kind+"»", 8))
        b.w = max(ws) + 2*PAD + 0.1
        lines = 1 + 1 + (1 if b.kind else 0) + max(len(b.members), 1)
        b.h = lines*LINE_H + 2*PAD - 0.05

def draw_box(ax, b):
    x, y = b.cx - b.w/2, b.cy - b.h/2
    ax.add_patch(Rectangle((x, y), b.w, b.h, fc="white", ec="black", lw=1.1, zorder=3))
    top = b.cy + b.h/2
    band = LINE_H + 0.02
    ax.add_patch(Rectangle((x, top-band), b.w, band, fc="white", ec="black", lw=1.1, zorder=4))
    ax.text(b.cx, top-band/2, "["+b.role+"]", ha="center", va="center", fontsize=7.5, fontname=FONT, color="black", zorder=5)
    ty = top - band - PAD*0.55
    if b.kind:
        ax.text(b.cx, ty, "«"+b.kind+"»", ha="center", va="top", fontsize=8, fontname=FONT, zorder=5)
        ty -= LINE_H*0.9
    ax.text(b.cx, ty, b.name, ha="center", va="top", fontsize=9.5, fontname=FONT, fontweight="bold",
            fontstyle="italic" if b.abstract else "normal", zorder=5)
    ty -= LINE_H*1.05
    ax.plot([x, x+b.w], [ty+0.03, ty+0.03], color="black", lw=1.1, zorder=5)
    ty -= 0.06
    for m in b.members:
        ax.text(x+PAD, ty, m, ha="left", va="top", fontsize=8.5, fontname=FONT, zorder=5)
        ty -= LINE_H

def arrow(ax, pts, head, dashed=False, label=None, lpos=None):
    pts = [tuple(p) for p in pts]
    if head:
        (x0,y0),(x1,y1) = pts[-2], pts[-1]
        dx,dy = x1-x0, y1-y0
        n = (dx*dx+dy*dy)**0.5
        ux,uy = dx/n, dy/n
        px,py = -uy, ux
        L,W = 0.20, 0.09
        bx,by = x1-ux*L, y1-uy*L
        if head == "hollow":
            pts[-1] = (bx,by)
            ax.add_patch(Polygon([(x1,y1),(bx+px*W,by+py*W),(bx-px*W,by-py*W)], closed=True, fc="white", ec="black", lw=1.1, zorder=6))
        else:
            ax.plot([bx+px*W,x1,bx-px*W],[by+py*W,y1,by-py*W], color="black", lw=1.1, zorder=6)
    xs,ys = zip(*pts)
    ax.plot(xs, ys, color="black", lw=1.1, ls=(0,(5,3)) if dashed else "-", zorder=2, solid_capstyle="butt")
    if label:
        ax.text(*lpos, label, ha="center", va="bottom", fontsize=8, fontname=FONT, zorder=7,
                bbox=dict(fc="white", ec="none", pad=1.0))

fig = plt.figure(figsize=(9.6, 6.0), dpi=100)
ax = fig.add_axes([0,0,1,1])

client = Box("Main", "Client", ["+ main(args: String[]): void"])
nav = Box("Navigator", "Context", ["- strategy: RouteStrategy", "+ setStrategy(strategy: RouteStrategy): void",
                                   "+ plan(distanceKm: double): String"])
rs = Box("RouteStrategy", "Strategy", ["+ planRoute(distanceKm: double): String"], "interface")
car = Box("CarStrategy", "Concrete Strategy", ["+ planRoute(distanceKm: double): String"])
walk = Box("WalkStrategy", "Concrete Strategy", ["+ planRoute(distanceKm: double): String"])
cycle = Box("CycleStrategy", "Concrete Strategy", ["+ planRoute(distanceKm: double): String"])
boxes = [client, nav, rs, car, walk, cycle]
measure(fig, ax, boxes)

client.cx, client.cy = 1.7, 5.1
nav.cx, nav.cy = 1.7, 3.5
rs.cx, rs.cy = 6.2, 3.5
car.cx, car.cy = 6.2, 2.0
walk.cx, walk.cy = 6.2, 0.95
cycle.cx, cycle.cy = 6.2, -0.1
for b in (car, walk, cycle):
    b.w = max(car.w, walk.w, cycle.w)
W = 9.6; H = 6.4
fig.set_size_inches(W, H)

for b in boxes: draw_box(ax, b)

arrow(ax, [client.bottom(), nav.top()], "open", label="creates / uses", lpos=(client.cx+1.0, (client.bottom()[1]+nav.top()[1])/2))
arrow(ax, [nav.right(), rs.left()], "open", dashed=True, label="strategy", lpos=((nav.right()[0]+rs.left()[0])/2, nav.cy+0.18))
gap = (car.top()[1] + rs.bottom()[1]) / 2
arrow(ax, [car.top(), rs.bottom()], "hollow", dashed=True)
xm = walk.right()[0] + 0.5
arrow(ax, [walk.right(), (xm, walk.cy), (xm, gap), rs.bottom()[0], ], None, dashed=True) if False else None
arrow(ax, [walk.left(0.2), (walk.left(0.2)[0]-0.3, walk.cy), (walk.left(0.2)[0]-0.3, gap), (rs.bottom(0.3)[0], gap), rs.bottom(0.3)], "hollow", dashed=True)
arrow(ax, [cycle.right(), (xm, cycle.cy), (xm, gap), (rs.bottom(0.7)[0], gap), rs.bottom(0.7)], "hollow", dashed=True)

ax.set_xlim(0, W); ax.set_ylim(-0.9, H-0.6); ax.set_aspect("equal"); ax.axis("off")
for ext in ("png","svg"):
    fig.savefig(OUT / f"strategy.{ext}", dpi=200, bbox_inches="tight", facecolor="white")
print("done")
