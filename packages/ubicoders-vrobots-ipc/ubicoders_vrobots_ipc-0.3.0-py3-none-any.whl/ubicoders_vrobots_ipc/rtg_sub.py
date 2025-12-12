# rtg_spN.py — N subplots; gracefully handle too few / too many channels
import argparse
import json
import signal
import sys
from collections import deque
from typing import Sequence, List, Optional
import numpy as np
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import zenoh
colors = ['r', 'g', 'b', 'y', 'c', 'm', 'w']


# ---------- Data buffer with padding/truncation
class DataBufferN:
    def __init__(self, n_channels: int, maxlen: int = 1000):
        self.n = n_channels
        self.ts = deque(maxlen=maxlen)
        self.ys: List[deque] = [deque(maxlen=maxlen) for _ in range(n_channels)]

    def append(self, t: float, values_in: Sequence[float]):
        # coerce to list
        if not isinstance(values_in, (list, tuple)):
            values_in = [values_in]

        # truncate or pad with NaN
        values = list(values_in[: self.n])
        if len(values) < self.n:
            values.extend([np.nan] * (self.n - len(values)))

        # append shared time and per-channel values
        self.ts.append(t)
        for i, v in enumerate(values):
            self.ys[i].append(v)

    def get_all(self):
        ts = list(self.ts)
        chans = [list(yq) for yq in self.ys]
        return ts, chans


# ---------- Plot window with N stacked plots sharing X (time) axis
class RealTimePlotN(QtWidgets.QMainWindow):
    def __init__(
        self,
        *,
        n_channels: int,
        fps: int = 60,
        buffer_secs: float = 5.0,
        labels: Optional[Sequence[str]] = None,
        background: str = "k",
    ):
        super().__init__()
        self.setWindowTitle(f"PyQtGraph — {n_channels}× real-time viewer")
        self.buffer_secs = buffer_secs

        maxlen = int(buffer_secs * fps) + 2
        self.buffer = DataBufferN(n_channels=n_channels, maxlen=maxlen)

        # Layout
        pg.setConfigOptions(antialias=True)
        layout = pg.GraphicsLayoutWidget()        # <- no show=True
        layout.setBackground(background)
        self.setCentralWidget(layout)

        # Build plots/curves
        self.plots: List[pg.PlotItem] = []
        self.curves: List[pg.PlotDataItem] = []
        labels = list(labels) if labels is not None else [f"Ch {i+1}" for i in range(n_channels)]

        for i in range(n_channels):
            p = layout.addPlot(row=i, col=0)
            p.showGrid(x=True, y=True, alpha=0.3)
            p.setLabel("left", labels[i] if i < len(labels) else f"Ch {i+1}")
            p.setLabel("bottom", "Time", units="s")
            if i < len(colors):
                pen = pg.mkPen(colors[i], width=2)
            else:
                pen = pg.mkPen(width=2)  # default
            c = p.plot(pen=pen)
            self.plots.append(p)
            self.curves.append(c)

        # Link X axes
        for p in self.plots[1:]:
            p.setXLink(self.plots[0])

        # Initial ranges
        self.plots[0].setXRange(0, buffer_secs, padding=0)
        for p in self.plots:
            p.enableAutoRange(axis=pg.ViewBox.YAxis, enable=True)

        # Redraw timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(int(1000 / fps))

    def add_sample(self, t: float, values: Sequence[float]):
        self.buffer.append(t, values)

    def update_plot(self):
        ts, chans = self.buffer.get_all()
        if not ts:
            return
        t_end = ts[-1]
        self.plots[0].setXRange(max(0.0, t_end - self.buffer_secs), t_end, padding=0)
        for curve, ys in zip(self.curves, chans):
            curve.setData(ts, ys)


# ---------- Zenoh callback (accepts [t, y], [t, [..]], or {"t":..,"values":[..]})
def make_zenoh_callback(window: RealTimePlotN):
    def on_zenoh_sample(sample):
        try:
            payload = sample.payload.to_bytes()
            obj = json.loads(payload)

            if isinstance(obj, dict):
                t = obj["t"]
                values = obj["values"]
            else:
                if len(obj) != 2:
                    raise ValueError("expected [t, values]")
                t, values = obj
            window.add_sample(float(t), values)
        except Exception as e:
            print(f"[ZenohSub] bad payload: {e}")
    return on_zenoh_sample


# --- Public API --------------------------------------------------------------

def start_rtg(
    *,
    channels: int = 3,
    fps: int = 50,
    buffer_secs: float = 6.0,
    topic: str = "vr/0/rtg",
    labels: Optional[Sequence[str]] = None,
    background: str = "k",
    start_event_loop: bool = True,
):
    """
    Create a real-time viewer and a Zenoh subscriber.

    Returns:
        If start_event_loop=False:
            (app, window, session, subscriber)
        Else:
            never returns (blocks in the Qt event loop)
    """
    # Reuse existing QApplication if the caller already created one
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    lbls = list(labels) if labels is not None else ["X", "Y", "Z", "W"][:channels]
    window = RealTimePlotN(
        n_channels=channels,
        fps=fps,
        buffer_secs=buffer_secs,
        labels=lbls,
        background=background,
    )
    # size heuristic per number of channels
    window.resize(900, 160 * channels + 30)
    window.show()

    # Zenoh wiring
    session = zenoh.open(zenoh.Config())
    subscriber = session.declare_subscriber(topic, make_zenoh_callback(window))
    print(f"[ZenohSub] Subscribed to '{topic}' for {channels} channels")

    # Make Ctrl+C work only if we own the loop
    if start_event_loop:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            sys.exit(app.exec_())
        finally:
            subscriber.undeclare()
            session.close()
    else:
        return app, window, session, subscriber


def stop_rtg(session, subscriber):
    """Gracefully stop the Zenoh pieces you received from start_rtg(..., start_event_loop=False)."""
    try:
        subscriber.undeclare()
    finally:
        session.close()

def main():
    """CLI entrypoint: parse args and run the viewer (blocking)."""
    parser = argparse.ArgumentParser(
        description="Real-time multi-channel plotter using PyQtGraph + Zenoh"
    )
    parser.add_argument("-c", "--channels", type=int, default=3,
                        help="Number of subplots (channels) [default: 3]")
    parser.add_argument("-f", "--fps", type=int, default=50,
                        help="Qt redraw rate [default: 50]")
    parser.add_argument("-b", "--buffer-secs", type=float, default=6.0,
                        help="Time window length in seconds [default: 6.0]")
    parser.add_argument("-t", "--topic", type=str, default="vr/0/rtg",
                        help="Zenoh topic to subscribe to [default: vr/0/rtg]")
    parser.add_argument("--background", type=str, default="k",
                        help="Plot background color [default: 'k']")
    args = parser.parse_args()

    # Run and block
    start_rtg(
        channels=args.channels,
        fps=args.fps,
        buffer_secs=args.buffer_secs,
        topic=args.topic,
        background=args.background,
        start_event_loop=True,
    )

# --- Script mode -------------------------------------------------------------
if __name__ == "__main__":
    main()
