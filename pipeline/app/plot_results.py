from pathlib import Path
import pandas as pd
import seaborn as sns


def plot_per_vs_snr(metrics_data: list[dict], output_plot_path: str | Path) -> None:
    df = pd.DataFrame(metrics_data)

    sns.set_theme(style="whitegrid")

    plot = sns.lineplot(data=df, x="snr_db", y="per", hue="lang", marker="o")

    sns.lineplot(
        data=df,
        x="snr_db",
        y="per",
        color="black",
        linestyle="--",
        label="Mean",
        ax=plot,
    )

    plot.set_xlim(max(df["snr_db"]) + 2, min(df["snr_db"]) - 2)
    plot.set(title="PER vs SNR (dB)", xlabel="SNR (dB)", ylabel="Phoneme Error Rate")

    fig = plot.get_figure()
    fig.savefig(str(output_plot_path))
