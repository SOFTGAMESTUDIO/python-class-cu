from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any

from sysinsight.analysis.health_score import calculate_health_score
from sysinsight.analysis.rules import evaluate_rules
from sysinsight.core.collector import Collector


class Dashboard:
    REFRESH_INTERVAL_MS = 2_000
    BACKGROUND = "#0b1220"
    PANEL = "#111c2e"
    PANEL_LIGHT = "#17253a"
    TEXT = "#e6edf7"
    MUTED = "#91a2b9"
    ACCENT = "#45d6b5"
    WARNING = "#f5b942"

    def __init__(self) -> None:
        self.collector = Collector()
        self.root = tk.Tk()
        self.root.title("SysInsight Pro")
        self.root.geometry("1080x720")
        self.root.minsize(860, 600)
        self.root.configure(bg=self.BACKGROUND)
        self.root.protocol("WM_DELETE_WINDOW", self._close)

        self._configure_styles()
        self._build_layout()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "Metric.Horizontal.TProgressbar",
            troughcolor=self.PANEL_LIGHT,
            background=self.ACCENT,
            bordercolor=self.PANEL_LIGHT,
            lightcolor=self.ACCENT,
            darkcolor=self.ACCENT,
        )

    def _build_layout(self) -> None:
        outer = tk.Frame(self.root, bg=self.BACKGROUND)
        outer.pack(fill="both", expand=True)

        sidebar = tk.Frame(outer, bg="#0e1828", width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="SYSINSIGHT",
            bg="#0e1828",
            fg=self.TEXT,
            font=("Segoe UI", 19, "bold"),
        ).pack(anchor="w", padx=22, pady=(27, 0))
        tk.Label(
            sidebar,
            text="SYSTEM HEALTH & DIAGNOSTICS",
            bg="#0e1828",
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=23, pady=(3, 30))

        self._nav_item(sidebar, "▦   Dashboard", selected=True)
        self._nav_item(sidebar, "◈   Hardware")
        self._nav_item(sidebar, "⌁   Performance")
        self._nav_item(sidebar, "✓   Diagnostics")
        self._nav_item(sidebar, "⚙   Settings")

        tk.Label(
            sidebar,
            text="LIVE MONITORING",
            bg="#0e1828",
            fg=self.ACCENT,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="bottom", anchor="w", padx=23, pady=(0, 24))

        content = tk.Frame(outer, bg=self.BACKGROUND)
        content.pack(side="left", fill="both", expand=True, padx=30, pady=25)

        header = tk.Frame(content, bg=self.BACKGROUND)
        header.pack(fill="x")
        header_text = tk.Frame(header, bg=self.BACKGROUND)
        header_text.pack(side="left")
        tk.Label(
            header_text,
            text="System Dashboard",
            bg=self.BACKGROUND,
            fg=self.TEXT,
            font=("Segoe UI", 23, "bold"),
        ).pack(anchor="w")
        self.updated_label = tk.Label(
            header_text,
            text="Waiting for first system scan...",
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=("Segoe UI", 9),
        )
        self.updated_label.pack(anchor="w", pady=(3, 0))

        self.refresh_button = tk.Button(
            header,
            text="⟳  Refresh",
            command=self.refresh,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            activebackground="#233650",
            activeforeground=self.TEXT,
            relief="flat",
            borderwidth=0,
            padx=16,
            pady=9,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        self.refresh_button.pack(side="right", anchor="n", pady=4)

        self.health_panel = tk.Frame(content, bg=self.PANEL, padx=22, pady=17)
        self.health_panel.pack(fill="x", pady=(23, 17))
        health_head = tk.Frame(self.health_panel, bg=self.PANEL)
        health_head.pack(fill="x")
        tk.Label(
            health_head,
            text="SYSTEM HEALTH",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")
        self.health_status = tk.Label(
            health_head,
            text="SCANNING",
            bg=self.PANEL,
            fg=self.ACCENT,
            font=("Segoe UI", 9, "bold"),
        )
        self.health_status.pack(side="right")
        health_body = tk.Frame(self.health_panel, bg=self.PANEL)
        health_body.pack(fill="x", pady=(6, 0))
        self.health_score = tk.Label(
            health_body,
            text="--",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 34, "bold"),
        )
        self.health_score.pack(side="left")
        tk.Label(
            health_body,
            text="/ 100",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 13),
        ).pack(side="left", anchor="s", pady=(0, 7))
        self.health_message = tk.Label(
            health_body,
            text="Collecting current system metrics",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 10),
        )
        self.health_message.pack(side="left", padx=(18, 0), anchor="s", pady=(0, 11))

        self.metric_widgets: dict[str, dict[str, Any]] = {}
        metrics_frame = tk.Frame(content, bg=self.BACKGROUND)
        metrics_frame.pack(fill="both", expand=True)
        metric_specs = (
            ("cpu", "PROCESSOR", "CPU", "%"),
            ("ram", "MEMORY", "RAM", "%"),
            ("gpu", "GRAPHICS", "GPU", "%"),
            ("disk", "STORAGE", "Disk", "%"),
            ("network", "NETWORK", "Download", "MB/s"),
        )
        for index, (key, heading, value_name, unit) in enumerate(metric_specs):
            row, column = divmod(index, 2)
            card = tk.Frame(metrics_frame, bg=self.PANEL, padx=18, pady=15)
            card.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=(0, 10) if column == 0 else (10, 0),
                pady=(0, 14),
            )
            tk.Label(
                card,
                text=heading,
                bg=self.PANEL,
                fg=self.MUTED,
                font=("Segoe UI", 9, "bold"),
            ).pack(anchor="w")
            value_label = tk.Label(
                card,
                text="--",
                bg=self.PANEL,
                fg=self.TEXT,
                font=("Segoe UI", 23, "bold"),
            )
            value_label.pack(anchor="w", pady=(8, 0))
            detail_label = tk.Label(
                card,
                text=f"{value_name} utilization",
                bg=self.PANEL,
                fg=self.MUTED,
                font=("Segoe UI", 9),
            )
            detail_label.pack(anchor="w", pady=(2, 9))
            progress = ttk.Progressbar(
                card,
                style="Metric.Horizontal.TProgressbar",
                maximum=100,
                mode="determinate",
            )
            progress.pack(fill="x")
            self.metric_widgets[key] = {
                "value": value_label,
                "detail": detail_label,
                "progress": progress,
                "unit": unit,
            }

        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_rowconfigure(0, weight=1)
        metrics_frame.grid_rowconfigure(1, weight=1)
        metrics_frame.grid_rowconfigure(2, weight=1)

        alerts_panel = tk.Frame(content, bg=self.PANEL, padx=18, pady=13)
        alerts_panel.pack(fill="x", pady=(2, 0))
        tk.Label(
            alerts_panel,
            text="ALERTS & STATUS",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        self.alerts_label = tk.Label(
            alerts_panel,
            text="Starting system monitor...",
            bg=self.PANEL,
            fg=self.TEXT,
            justify="left",
            anchor="w",
            font=("Segoe UI", 10),
        )
        self.alerts_label.pack(fill="x", pady=(8, 0))

    def _nav_item(self, parent: tk.Frame, text: str, selected: bool = False) -> None:
        tk.Label(
            parent,
            text=text,
            bg=self.PANEL_LIGHT if selected else "#0e1828",
            fg=self.ACCENT if selected else self.MUTED,
            font=("Segoe UI", 10, "bold" if selected else "normal"),
            padx=15,
            pady=11,
            anchor="w",
        ).pack(fill="x", padx=12, pady=2)

    def _snapshot_metrics(self) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
        snapshot = self.collector.collect()
        metrics = {
            "cpu": snapshot.cpu,
            "ram": snapshot.ram,
            "gpu": snapshot.gpu,
            "disk": snapshot.disk,
            "network": snapshot.network,
            "thermal": snapshot.thermal,
        }
        return metrics, calculate_health_score(metrics), evaluate_rules(metrics)

    def refresh(self) -> None:
        self.refresh_button.configure(state="disabled", text="Scanning...")
        try:
            metrics, health, alerts = self._snapshot_metrics()
            self._update_widgets(metrics, health, alerts)
        except Exception as exc:
            messagebox.showerror(
                "System scan failed",
                f"SysInsight Pro could not collect system metrics.\n\n{exc}",
                parent=self.root,
            )
            self.alerts_label.configure(text=f"System scan failed: {exc}", fg="#ff7474")
        finally:
            self.refresh_button.configure(state="normal", text="⟳  Refresh")
            if self.root.winfo_exists():
                self.root.after(self.REFRESH_INTERVAL_MS, self.refresh)

    def _update_widgets(
        self,
        metrics: dict[str, Any],
        health: dict[str, Any],
        alerts: list[str],
    ) -> None:
        self.updated_label.configure(text=f"Last updated: {self._current_time()}")
        score = health["score"]
        status = health["status"]
        self.health_score.configure(text=f"{score:g}")
        self.health_status.configure(
            text=status,
            fg=self.ACCENT if status == "GOOD" else self.WARNING if status == "WATCH" else "#ff7474",
        )
        self.health_message.configure(
            text="Your system is operating normally" if status == "GOOD" else "Review the current system metrics"
        )

        values = {
            "cpu": (
                metrics["cpu"].get("utilization", 0),
                f"{metrics['cpu'].get('cores', '—')} logical cores · {metrics['cpu'].get('frequency_mhz', 0):g} MHz",
            ),
            "ram": (
                metrics["ram"].get("used_percent", 0),
                f"{metrics['ram'].get('used_gb', 0):g} / {metrics['ram'].get('total_gb', 0):g} GB used",
            ),
            "gpu": (
                metrics["gpu"].get("utilization", 0),
                f"{metrics['gpu'].get('name', 'GPU unavailable')} · {self._temperature(metrics['gpu'].get('temperature_c'))}",
            ),
            "disk": (
                metrics["disk"].get("used_percent", 0),
                f"{metrics['disk'].get('free_gb', 0):g} GB free",
            ),
            "network": (
                metrics["network"].get("download_mbps", 0),
                f"Upload {metrics['network'].get('upload_mbps', 0):g} MB/s",
            ),
        }
        for key, (value, detail) in values.items():
            widgets = self.metric_widgets[key]
            unit = widgets["unit"]
            if key == "network":
                widgets["value"].configure(text=f"{value:g} {unit}")
                widgets["progress"].configure(value=min(100, max(0, value)))
            else:
                widgets["value"].configure(text=f"{value:g}{unit}")
                widgets["progress"].configure(value=min(100, max(0, value)))
            widgets["detail"].configure(text=detail)

        if alerts:
            self.alerts_label.configure(
                text="\n".join(f"•  {alert}" for alert in alerts),
                fg=self.WARNING,
            )
        else:
            self.alerts_label.configure(text="✓  No critical alerts", fg=self.ACCENT)

    @staticmethod
    def _current_time() -> str:
        from datetime import datetime

        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def _temperature(value: Any) -> str:
        return f"{value:g}°C" if isinstance(value, (int, float)) and value > 0 else "temperature unavailable"

    def _close(self) -> None:
        self.root.destroy()

    def run(self) -> None:
        self.root.after(100, self.refresh)
        self.root.mainloop()
