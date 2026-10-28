from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from queue import Empty, Queue
from threading import Event, Thread
from typing import Any

from sysinsight.analysis.health_score import calculate_health_score
from sysinsight.analysis.rules import evaluate_rules
from sysinsight.core.collector import Collector
from sysinsight.diagnostics.performance_test import (
    MAX_DURATION_SECONDS,
    assess_test_risk,
    run_cpu_benchmark,
)


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
        self._latest_metrics: dict[str, Any] = {}
        self._benchmark_events: Queue[tuple[str, Any]] = Queue()
        self._benchmark_stop: Event | None = None
        self._benchmark_active = False
        self._nav_buttons: dict[str, tk.Button] = {}
        self._pages: dict[str, tk.Frame] = {}
        self._current_page = "Dashboard"
        self._refresh_after_id: str | None = None
        self._hardware_values: dict[str, tk.Label] = {}
        self._diagnostic_values: dict[str, tk.Label] = {}
        self.root = tk.Tk()
        self.refresh_interval = tk.IntVar(master=self.root, value=2)
        self.root.title("SysInsight Pro")
        self.root.geometry("1080x820")
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

        for name, icon in (
            ("Dashboard", "▦"),
            ("Hardware", "◈"),
            ("Performance", "⌁"),
            ("Diagnostics", "✓"),
            ("Settings", "⚙"),
        ):
            self._nav_item(sidebar, name, icon)

        tk.Label(
            sidebar,
            text="LIVE MONITORING",
            bg="#0e1828",
            fg=self.ACCENT,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="bottom", anchor="w", padx=23, pady=(0, 24))

        self.page_container = tk.Frame(outer, bg=self.BACKGROUND)
        self.page_container.pack(side="left", fill="both", expand=True, padx=30, pady=25)
        content = tk.Frame(self.page_container, bg=self.BACKGROUND)
        self._pages["Dashboard"] = content

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

        self._build_feature_pages()
        self.show_page("Dashboard")

    def _build_performance_test(self, parent: tk.Frame) -> None:
        panel = tk.Frame(parent, bg=self.PANEL, padx=18, pady=13)
        panel.pack(fill="x", pady=(12, 0))
        header = tk.Frame(panel, bg=self.PANEL)
        header.pack(fill="x")
        tk.Label(
            header,
            text="BOUNDED CPU PERFORMANCE TEST",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")
        controls = tk.Frame(header, bg=self.PANEL)
        controls.pack(side="right")
        tk.Label(controls, text="Duration", bg=self.PANEL, fg=self.MUTED).pack(side="left", padx=(0, 7))
        self.test_duration = tk.StringVar(value="10")
        ttk.Spinbox(
            controls,
            textvariable=self.test_duration,
            from_=1,
            to=MAX_DURATION_SECONDS,
            increment=1,
            width=4,
            state="readonly",
        ).pack(side="left", padx=(0, 10))
        self.test_button = tk.Button(
            controls,
            text="Run short test",
            command=self._start_benchmark,
            bg=self.ACCENT,
            fg="#08131e",
            activebackground="#68e8cb",
            activeforeground="#08131e",
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=7,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        )
        self.test_button.pack(side="left")
        self.stop_test_button = tk.Button(
            controls,
            text="Stop",
            command=self._stop_benchmark,
            state="disabled",
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            activebackground="#233650",
            activeforeground=self.TEXT,
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=7,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        )
        self.stop_test_button.pack(side="left", padx=(8, 0))
        self.test_status = tk.Label(
            panel,
            text="Short, single-threaded benchmark. Maximum 15 seconds; not a full-system stress test.",
            bg=self.PANEL,
            fg=self.MUTED,
            justify="left",
            anchor="w",
            font=("Segoe UI", 9),
        )
        self.test_status.pack(fill="x", pady=(9, 0))

    def _nav_item(self, parent: tk.Frame, name: str, icon: str) -> None:
        button = tk.Button(
            parent,
            text=f"{icon}   {name}",
            command=lambda page=name: self.show_page(page),
            bg="#0e1828",
            fg=self.MUTED,
            activebackground=self.PANEL_LIGHT,
            activeforeground=self.TEXT,
            font=("Segoe UI", 10),
            padx=15,
            pady=11,
            anchor="w",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
        )
        button.pack(fill="x", padx=12, pady=2)
        self._nav_buttons[name] = button

    def _build_feature_pages(self) -> None:
        hardware = self._new_page("Hardware", "Hardware Overview", "Live device readings from this computer.")
        self._build_hardware_page(hardware)

        performance = self._new_page(
            "Performance",
            "Performance & Risk",
            "Review current load and run a brief, cancellable CPU benchmark.",
        )
        self._build_performance_test(performance)
        self.performance_summary = tk.Label(
            performance,
            text="Waiting for a system scan...",
            bg=self.PANEL,
            fg=self.TEXT,
            justify="left",
            anchor="nw",
            padx=18,
            pady=16,
            font=("Segoe UI", 11),
        )
        self.performance_summary.pack(fill="x", pady=(14, 0))

        diagnostics = self._new_page(
            "Diagnostics",
            "Diagnostics & Risk",
            "These checks report available telemetry; they do not certify hardware or run a stability stress test.",
        )
        self._build_diagnostics_page(diagnostics)

        settings = self._new_page(
            "Settings",
            "Application Settings",
            "Adjust the live dashboard refresh interval.",
        )
        self._build_settings_page(settings)

    def _new_page(self, key: str, title: str, subtitle: str) -> tk.Frame:
        page = tk.Frame(self.page_container, bg=self.BACKGROUND)
        self._pages[key] = page
        header = tk.Frame(page, bg=self.BACKGROUND)
        header.pack(fill="x", pady=(0, 22))
        tk.Label(
            header,
            text=title,
            bg=self.BACKGROUND,
            fg=self.TEXT,
            font=("Segoe UI", 23, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header,
            text=subtitle,
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))
        return page

    def _build_hardware_page(self, parent: tk.Frame) -> None:
        panel = tk.Frame(parent, bg=self.PANEL, padx=20, pady=16)
        panel.pack(fill="x")
        rows = (
            ("cpu", "CPU"),
            ("ram", "Memory"),
            ("gpu", "Graphics"),
            ("disk", "Storage"),
            ("network", "Network"),
            ("thermal", "Temperature sensors"),
        )
        for key, title in rows:
            row = tk.Frame(panel, bg=self.PANEL)
            row.pack(fill="x", pady=8)
            tk.Label(
                row, text=title, bg=self.PANEL, fg=self.MUTED, width=23, anchor="w",
                font=("Segoe UI", 10, "bold"),
            ).pack(side="left")
            value = tk.Label(
                row, text="Waiting for scan...", bg=self.PANEL, fg=self.TEXT, anchor="w",
                font=("Segoe UI", 10),
            )
            value.pack(side="left", fill="x", expand=True)
            self._hardware_values[key] = value

    def _build_diagnostics_page(self, parent: tk.Frame) -> None:
        panel = tk.Frame(parent, bg=self.PANEL, padx=20, pady=16)
        panel.pack(fill="x")
        checks = (
            ("cpu", "CPU load telemetry"),
            ("ram", "Memory pressure"),
            ("gpu", "GPU telemetry"),
            ("disk", "Storage capacity"),
            ("network", "Network counters"),
            ("thermal", "Temperature monitoring"),
        )
        for key, label in checks:
            row = tk.Frame(panel, bg=self.PANEL)
            row.pack(fill="x", pady=8)
            tk.Label(row, text=label, bg=self.PANEL, fg=self.TEXT, anchor="w").pack(side="left")
            result = tk.Label(row, text="Not checked", bg=self.PANEL, fg=self.MUTED, anchor="e")
            result.pack(side="right")
            self._diagnostic_values[key] = result

        tk.Button(
            parent,
            text="Run telemetry checks",
            command=self._run_telemetry_checks,
            bg=self.ACCENT,
            fg="#08131e",
            activebackground="#68e8cb",
            relief="flat",
            padx=15,
            pady=9,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        ).pack(anchor="w", pady=(14, 0))

    def _build_settings_page(self, parent: tk.Frame) -> None:
        panel = tk.Frame(parent, bg=self.PANEL, padx=20, pady=18)
        panel.pack(fill="x")
        tk.Label(
            panel,
            text="Automatic refresh interval",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w")
        tk.Label(
            panel,
            text="Choose how often the app updates live readings.",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(4, 12))
        controls = tk.Frame(panel, bg=self.PANEL)
        controls.pack(anchor="w")
        ttk.Spinbox(controls, from_=1, to=10, textvariable=self.refresh_interval, width=5).pack(side="left")
        tk.Label(controls, text="seconds", bg=self.PANEL, fg=self.MUTED).pack(side="left", padx=(7, 14))
        tk.Button(
            controls,
            text="Apply",
            command=self._apply_settings,
            bg=self.ACCENT,
            fg="#08131e",
            activebackground="#68e8cb",
            relief="flat",
            padx=13,
            pady=7,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side="left")

    def show_page(self, name: str) -> None:
        page = self._pages.get(name)
        if page is None:
            return
        for current in self._pages.values():
            current.pack_forget()
        page.pack(fill="both", expand=True)
        self._current_page = name
        for page_name, button in self._nav_buttons.items():
            selected = page_name == name
            button.configure(
                bg=self.PANEL_LIGHT if selected else "#0e1828",
                fg=self.ACCENT if selected else self.MUTED,
                font=("Segoe UI", 10, "bold" if selected else "normal"),
            )
        if name == "Diagnostics":
            self._run_telemetry_checks()

    def _apply_settings(self) -> None:
        try:
            seconds = int(self.refresh_interval.get())
        except (tk.TclError, ValueError):
            messagebox.showerror("Invalid setting", "Refresh interval must be a whole number from 1 to 10.", parent=self.root)
            return
        if not 1 <= seconds <= 10:
            messagebox.showerror("Invalid setting", "Refresh interval must be between 1 and 10 seconds.", parent=self.root)
            return
        self.refresh_interval.set(seconds)
        self._schedule_refresh()
        messagebox.showinfo("Settings saved", f"Dashboard refresh interval set to {seconds} seconds.", parent=self.root)

    def _run_telemetry_checks(self) -> None:
        if not self._latest_metrics:
            for label in self._diagnostic_values.values():
                label.configure(text="Waiting for scan", fg=self.WARNING)
            return
        metrics = self._latest_metrics
        checks = {
            "cpu": (
                f"{metrics['cpu'].get('utilization', 0):g}% CPU load",
                self.ACCENT if metrics["cpu"].get("utilization", 0) < 85 else self.WARNING,
            ),
            "ram": (
                f"{metrics['ram'].get('used_percent', 0):g}% used",
                self.ACCENT if metrics["ram"].get("used_percent", 0) < 90 else self.WARNING,
            ),
            "gpu": (
                "Available" if metrics["gpu"].get("status") != "UNAVAILABLE" else "Telemetry unavailable",
                self.ACCENT if metrics["gpu"].get("status") != "UNAVAILABLE" else self.WARNING,
            ),
            "disk": (
                f"{metrics['disk'].get('free_gb', 0):g} GB free",
                self.ACCENT if metrics["disk"].get("used_percent", 0) < 90 else self.WARNING,
            ),
            "network": ("Counters available", self.ACCENT),
            "thermal": (
                f"{metrics['thermal'].get('cpu_temperature_c', 0):g}°C"
                if metrics["thermal"].get("temperature_monitoring_available")
                else "Sensor unavailable",
                self.ACCENT if metrics["thermal"].get("temperature_monitoring_available") else self.WARNING,
            ),
        }
        for key, (text, color) in checks.items():
            self._diagnostic_values[key].configure(text=text, fg=color)

    def _update_feature_pages(self, metrics: dict[str, Any], health: dict[str, Any], alerts: list[str]) -> None:
        cpu = metrics["cpu"]
        ram = metrics["ram"]
        gpu = metrics["gpu"]
        disk = metrics["disk"]
        network = metrics["network"]
        thermal = metrics["thermal"]
        hardware_text = {
            "cpu": f"{cpu.get('cores', '—')} logical cores · {cpu.get('frequency_mhz', 0):g} MHz · {cpu.get('utilization', 0):g}% load",
            "ram": f"{ram.get('used_gb', 0):g} / {ram.get('total_gb', 0):g} GB · {ram.get('used_percent', 0):g}% used",
            "gpu": f"{gpu.get('name', 'Unknown')} · {gpu.get('utilization', 0):g}% · {self._temperature(gpu.get('temperature_c'))}",
            "disk": f"{disk.get('free_gb', 0):g} GB free of {disk.get('total_gb', 0):g} GB · {disk.get('used_percent', 0):g}% used",
            "network": f"Sent {network.get('bytes_sent', 0):,} bytes · Received {network.get('bytes_recv', 0):,} bytes",
            "thermal": (
                f"CPU {self._temperature(thermal.get('cpu_temperature_c'))} · "
                f"GPU {self._temperature(thermal.get('gpu_temperature_c'))}"
            ),
        }
        for key, text in hardware_text.items():
            self._hardware_values[key].configure(text=text)
        self.performance_summary.configure(
            text=(
                f"Current health score: {health['score']:g}/100 ({health['status']})\n"
                f"CPU load: {cpu.get('utilization', 0):g}%   ·   Memory: {ram.get('used_percent', 0):g}%\n"
                f"Temperature monitoring: {'available' if thermal.get('temperature_monitoring_available') else 'unavailable'}\n"
                f"Current alerts: {', '.join(alerts) if alerts else 'None'}"
            )
        )
        if self._current_page == "Diagnostics":
            self._run_telemetry_checks()

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
        self._refresh_after_id = None
        if self._benchmark_active:
            self._schedule_refresh()
            return
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
            self._schedule_refresh()

    def _update_widgets(
        self,
        metrics: dict[str, Any],
        health: dict[str, Any],
        alerts: list[str],
    ) -> None:
        self._latest_metrics = metrics
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
                f"{metrics['cpu'].get('cores', '—')} logical cores · "
                f"{metrics['cpu'].get('frequency_mhz', 0):g} MHz · "
                f"{self._temperature(metrics['thermal'].get('cpu_temperature_c'))}",
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
        self._update_feature_pages(metrics, health, alerts)

    def _start_benchmark(self) -> None:
        try:
            duration = int(self.test_duration.get())
        except ValueError:
            messagebox.showerror("Invalid duration", "Choose a whole number of seconds.", parent=self.root)
            return
        if not 1 <= duration <= MAX_DURATION_SECONDS:
            messagebox.showerror(
                "Invalid duration",
                f"Choose a duration from 1 to {MAX_DURATION_SECONDS} seconds.",
                parent=self.root,
            )
            return
        if not self._latest_metrics:
            messagebox.showinfo("System scan required", "Wait for the first system scan before testing.", parent=self.root)
            return

        risk = assess_test_risk(self._latest_metrics)
        if risk["level"] == "HIGH":
            messagebox.showwarning(
                "Test blocked by risk check",
                "The current system state is too risky for a CPU performance test:\n\n"
                + "\n".join(f"• {reason}" for reason in risk["reasons"]),
                parent=self.root,
            )
            return

        warning = (
            "This is a brief single-threaded CPU workload, not a stability test. "
            "The run is capped at 15 seconds and can be stopped at any time. "
            "Do not run it if the computer is already hot or behaving abnormally."
        )
        if risk["reasons"]:
            warning += "\n\nRisk notes:\n" + "\n".join(f"• {reason}" for reason in risk["reasons"])
        if not messagebox.askyesno("Confirm bounded performance test", warning, parent=self.root):
            return

        self._benchmark_active = True
        self._benchmark_stop = Event()
        self.test_button.configure(state="disabled")
        self.stop_test_button.configure(state="normal")
        self.refresh_button.configure(state="disabled")
        self.test_status.configure(text=f"Running bounded CPU test ({duration} seconds)...", fg=self.WARNING)
        worker = Thread(target=self._benchmark_worker, args=(duration, self._benchmark_stop), daemon=True)
        worker.start()
        self.root.after(200, self._poll_benchmark_events)

    def _benchmark_worker(self, duration: int, stop_event: Event) -> None:
        try:
            result = run_cpu_benchmark(
                duration,
                stop_event,
                lambda update: self._benchmark_events.put(("progress", update)),
            )
            self._benchmark_events.put(("result", result))
        except Exception as exc:
            self._benchmark_events.put(("error", exc))

    def _stop_benchmark(self) -> None:
        if self._benchmark_stop is not None:
            self._benchmark_stop.set()
            self.stop_test_button.configure(state="disabled")
            self.test_status.configure(text="Stopping test...", fg=self.WARNING)

    def _poll_benchmark_events(self) -> None:
        try:
            while True:
                event, payload = self._benchmark_events.get_nowait()
                if event == "progress":
                    elapsed = payload["elapsed_seconds"]
                    total = payload["duration_seconds"]
                    temperature = payload["cpu_temperature_c"]
                    temperature_text = f" · CPU {temperature:.0f}°C" if temperature > 0 else ""
                    self.test_status.configure(
                        text=f"Running: {elapsed:.0f}/{total} seconds{temperature_text} · Stop is available",
                        fg=self.WARNING,
                    )
                elif event == "result":
                    self._finish_benchmark(payload)
                elif event == "error":
                    self._finish_benchmark(None)
                    messagebox.showerror("Performance test failed", str(payload), parent=self.root)
        except Empty:
            pass
        if self._benchmark_active and self.root.winfo_exists():
            self.root.after(200, self._poll_benchmark_events)

    def _finish_benchmark(self, result: dict[str, Any] | None) -> None:
        self._benchmark_active = False
        self._benchmark_stop = None
        self.test_button.configure(state="normal")
        self.stop_test_button.configure(state="disabled")
        self.refresh_button.configure(state="normal", text="⟳  Refresh")
        if result is not None:
            outcome = {
                "completed": "Completed",
                "cancelled": "Stopped by user",
                "thermal_stop": "Stopped: CPU temperature reached 85°C",
            }.get(result["status"], result["status"])
            self.test_status.configure(
                text=(
                    f"{outcome} · {result['operations_per_second']:,} operations/second "
                    f"· elapsed {result['duration_seconds']:.2f}s"
                ),
                fg=self.ACCENT if result["status"] == "completed" else self.WARNING,
            )
        self.refresh()

    @staticmethod
    def _current_time() -> str:
        from datetime import datetime

        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def _temperature(value: Any) -> str:
        return f"{value:g}°C" if isinstance(value, (int, float)) and value > 0 else "temperature unavailable"

    def _close(self) -> None:
        if self._benchmark_stop is not None:
            self._benchmark_stop.set()
        if self._refresh_after_id is not None:
            self.root.after_cancel(self._refresh_after_id)
            self._refresh_after_id = None
        self.root.destroy()

    def _schedule_refresh(self) -> None:
        if self._refresh_after_id is not None:
            self.root.after_cancel(self._refresh_after_id)
        self._refresh_after_id = self.root.after(
            max(1, self.refresh_interval.get()) * 1000,
            self.refresh,
        )

    def run(self) -> None:
        self._refresh_after_id = self.root.after(100, self.refresh)
        self.root.mainloop()
