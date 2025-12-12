from abc import abstractmethod, ABC
from pandas import DataFrame
import logging

import pandas as pd
from pathlib import Path
from typing import Union, Literal, List
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math

class EDA(ABC):
    logger = logging.getLogger(__name__)
    # def load_data(self, df: DataFrame):
    #     self.df = df.copy()

    @abstractmethod
    def standardize_categories(self, cleaned_df: DataFrame) -> DataFrame:
        pass


    def plot_class_distribution(
            self,
            df: pd.DataFrame,
            target: str,
            figsize: tuple = (6, 6),
            show_percent: bool = True,
            sort_desc: bool = True,
            palette: Union[str, list] = "deep",
            save_path: Union[str, Path, None] = None,
    ):
        """
        Plots class distribution as a pie chart.

        Args:
            df: pandas DataFrame containing the target column.
            target: name of the target/class column.
            figsize: figure size.
            show_percent: show count + percentage in labels.
            sort_desc: sort classes by count descending.
            palette: seaborn color palette name or list of colors.
            save_path: if provided, save the figure to this path.
        """
        if target not in df.columns:
            raise ValueError(f"Target column '{target}' not in DataFrame.")

        counts = df[target].value_counts(ascending=not sort_desc)
        total = counts.sum()
        labels = counts.index.astype(str)
        values = counts.values

        # Resolve colors from seaborn palette or list
        if isinstance(palette, str):
            colors = sns.color_palette(palette, n_colors=len(values))
        else:
            colors = palette

        fig, ax = plt.subplots(figsize=figsize)

        if show_percent:
            def autopct(pct):
                # pct is percentage; convert back to absolute count
                count = int(round(pct * total / 100.0))
                return f"{count} ({pct:.1f}%)"
        else:
            autopct = None

        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels if not show_percent else None,  # we'll show labels in legend instead
            autopct=autopct,
            startangle=90,
            colors=colors,
            wedgeprops=dict(edgecolor="white"),
            textprops=dict(color="black", fontsize=9),
        )

        ax.axis("equal")  # Equal aspect ratio ensures the pie is drawn as a circle.
        ax.set_title(f"Class distribution for '{target}'")

        # Put labels in legend so the pie stays clean
        ax.legend(
            wedges,
            labels,
            title=target,
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            frameon=False,
        )

        plt.tight_layout()
        if save_path:
            save_path = Path(save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Saved class distribution to: {save_path}")
        #plt.show()
        plt.close()


    def plot_correlation_heatmap(self, df: pd.DataFrame,
                                 features: Union[list, None] = None,
                                 method: Literal["pearson", "spearman", "kendall"] = "pearson",
                                 annot: bool = True,
                                 fmt: str = '.2f',
                                 cmap: str = 'coolwarm',
                                 figsize: tuple = (10, 8),
                                 mask_upper_triangle: bool = True,
                                 save_path: Union[str, Path, None] = None):
        """
        Plots a correlation heatmap for numeric features.
        Args:
            df: pandas DataFrame.
            features: list of columns to include. If None, uses all numeric columns.
            method: 'pearson', 'spearman', or 'kendall'.
            annot: whether to annotate correlation values.
            fmt: annotation format.
            cmap: colormap for heatmap.
            figsize: figure size.
            mask_upper_triangle: mask the upper triangle (avoid duplicate info).
            save_path: path to save the figure.
        """
        if features is None:
            data = df.select_dtypes(include=[np.number])
        else:
            data = df[features]

        if data.shape[1] == 0:
            raise ValueError("No numeric columns found for correlation matrix.")

        corr = data.corr(method=method)

        plt.figure(figsize=figsize)
        if mask_upper_triangle:
            mask = np.triu(np.ones_like(corr, dtype=bool))
        else:
            mask = None

        sns.heatmap(corr, mask=mask, annot=annot, fmt=fmt, cmap=cmap,
                    linewidths=0.5, square=False, cbar_kws={"shrink": 0.75})
        plt.title(f'Correlation heatmap ({method})')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved correlation heatmap to: {save_path}")
        #plt.show()
        plt.close()

    def plot_feature_distributions_fixed(self,
            df: pd.DataFrame,
            features: Union[List[str], None] = None,
            max_features: int = 50,
            sample: Union[int, float, None] = 5000,
            bins: int = 30,
            kde: bool = True,
            max_plots_per_page: int = 12,
            base_height_per_row: float = 2.6,
            base_width_per_col: float = 4.0,
            fontsize_title: int = 9,
            fontsize_ticks: int = 8,
            save_path_template: Union[str, Path, None] = None):
        """
        Robust plotting for many features:
         - Automatically chooses grid (cols x rows)
         - Chunks into multiple pages if too many features
         - Uses constrained_layout, small fonts, adjusted spacing to avoid overlap

        Args:
            df: dataframe
            features: list of features to plot. If None uses numeric+categorical up to max_features
            max_features: total features to consider
            sample: int (n), float (fraction) or None
            max_plots_per_page: how many subplots per figure/page (e.g. 12)
            save_path_template: optional template like "dist_page_{page}.png" to save pages
        """
        # select candidate features
        if features is None:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            cat_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
            features = numeric_cols + cat_cols
        # filter existing and limit
        features = [f for f in features if f in df.columns][:max_features]
        n = len(features)
        if n == 0:
            raise ValueError("No valid features to plot.")

        # sampling
        if sample is not None:
            if isinstance(sample, float) and 0 < sample < 1:
                plot_df = df.sample(frac=sample, random_state=42)
            elif isinstance(sample, int) and sample > 0:
                plot_df = df.sample(n=min(sample, len(df)), random_state=42)
            else:
                plot_df = df
        else:
            plot_df = df

        # chunk features into pages
        pages = [features[i:i + max_plots_per_page] for i in range(0, n, max_plots_per_page)]

        for page_idx, feat_page in enumerate(pages, start=1):
            m = len(feat_page)
            # choose cols dynamically to reduce rows: prefer 3-5 columns depending on m
            # heuristic: columns = min(5, max(2, int(ceil(sqrt(m)))))
            cols = min(5, max(2, math.ceil(math.sqrt(m))))
            rows = math.ceil(m / cols)

            fig_w = base_width_per_col * cols
            fig_h = base_height_per_row * rows

            fig, axes = plt.subplots(rows, cols, figsize=(fig_w, fig_h), constrained_layout=True)
            # flatten axes
            if isinstance(axes, (np.ndarray, list)):
                axes = axes.flatten()
            else:
                axes = [axes]

            for i, colname in enumerate(feat_page):
                ax = axes[i]
                if pd.api.types.is_numeric_dtype(plot_df[colname]):
                    sns.histplot(plot_df[colname].dropna(), bins=bins, kde=kde, stat='count', ax=ax)
                    ax.set_title(f"{colname}", fontsize=fontsize_title)
                    # lighten x tick labels for numeric
                    ax.tick_params(axis='x', labelrotation=0, labelsize=fontsize_ticks)
                else:
                    counts = plot_df[colname].value_counts(dropna=False).head(30)  # top categories
                    sns.barplot(x=counts.values, y=counts.index, ax=ax)
                    ax.set_title(f"{colname} (cat)", fontsize=fontsize_title)
                    ax.tick_params(axis='y', labelsize=fontsize_ticks)
                    # rotate long ylabels slightly
                    ax.set_yticklabels([str(t.get_text()) for t in ax.get_yticklabels()], fontsize=fontsize_ticks)

                # remove x label clutter
                ax.set_xlabel("")
                ax.set_ylabel("Count", fontsize=max(8, fontsize_ticks))

            # hide unused axes
            for j in range(m, len(axes)):
                axes[j].axis('off')

            # further adjust spacing if necessary
            plt.subplots_adjust(wspace=0.25, hspace=0.35, top=0.95, bottom=0.05, left=0.05, right=0.98)

            # save if requested
            if save_path_template:
                template_str = str(save_path_template)
                path = template_str.format(page=page_idx)
                plt.savefig(path, dpi=300, bbox_inches='tight')
                print(f"Saved page {page_idx} -> {path}")

            #plt.show()
            plt.close(fig)