import logging
from pathlib import Path
from typing import Union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

from aiq.churn.algo.evaluators.base import BaseEvaluator
from aiq.churn.utility import save_dict_as_json


try:
    from sklearn.metrics import roc_curve, auc
except Exception:
    roc_curve = None
    auc = None

class ClassificationEvaluator(BaseEvaluator):
    logger = logging.getLogger(__name__)
    def __init__(self, model):
        super().__init__(model)
        self.y_pred_ = None
        self.y_prob_ = None
        self.metrics_ = {}
        self.class_report_ = None
        self.y_test_ = None

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series):
        self.y_pred_ = self.model.predict(X_test)
        self.y_test_ = y_test

        if hasattr(self.model, 'predict_proba'):
            self.y_prob_ = self.model.predict_proba(X_test)[:, 1]

        cm = confusion_matrix(y_test, self.y_pred_)
        self.metrics_ = {
            "accuracy": accuracy_score(y_test, self.y_pred_),
            "precision": precision_score(y_test, self.y_pred_),
            "recall": recall_score(y_test, self.y_pred_),
            "f1_score": f1_score(y_test, self.y_pred_),
            "roc_auc": roc_auc_score(y_test, self.y_prob_) if self.y_prob_ is not None else "N/A",
            "confusion_matrix": cm.tolist()
        }
        self.class_report_ = classification_report(y_test, self.y_pred_, output_dict=True)
        return self

    def display_report(self):
        self.logger.info("=" * 40)
        self.logger.info("      Classification Evaluation Report (Test)    ")
        self.logger.info("=" * 40)
        self.logger.info(f"Model Class: {self.model.__class__.__name__}\n")

        for key, value in self.metrics_.items():
            if key != "confusion_matrix":
                self.logger.info(f"{key:<12}: {value:.4f}" if isinstance(value, float) else f"{key:<12}: {value}")

        #print("\n--- Classification Report ---")
        #print(classification_report(self.y_test_, self.y_pred_))

        self.logger.info("\nConfusion Matrix:\n %s", np.array(self.metrics_["confusion_matrix"]).tolist())

        self.logger.info("=" * 40)

    def save_results(self, path: Union[str, Path]):
        if not self.metrics_:
            raise RuntimeError("No results to save. Run evaluate() first.")

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        results = {
            "metrics": self.metrics_,
            "classification_report": self.class_report_
        }
        save_dict_as_json(results, path)
        self.logger.info(f"Evaluation results saved to: %s",path)

    def plot_confusion_matrix(self, save_path: Union[str, Path, None] = None):
        if 'confusion_matrix' not in self.metrics_:
            raise RuntimeError("You must run evaluate() before plotting.")

        cm = np.array(self.metrics_["confusion_matrix"])
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Predicted Negative', 'Predicted Positive'],
                    yticklabels=['Actual Negative', 'Actual Positive'])
        plt.title('Confusion Matrix', fontsize=16)
        plt.ylabel('Actual Label')
        plt.xlabel('Predicted Label')

        if save_path:
            path = Path(save_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(path)
            self.logger.info(f"Confusion matrix plot saved to: {path}")
        #plt.show()
        plt.close()


    def run(self, X_test, y_test, results_path=None, plot_path=None):
        self.evaluate(X_test, y_test)
        self.display_report()
        if plot_path:
            self.plot_confusion_matrix(plot_path)
        if results_path:
            self.save_results(results_path)


    def plot_roc_curve(self, save_path: Union[str, Path, None] = None, pos_label=1):
        """
        Plot ROC curve for a binary classifier.

        This function is defensive: it will try several attribute names that
        may exist on the evaluator (y_true_, y_score_, y_test_, y_prob_,
        y_pred_proba_) or precomputed values in self.metrics_.

        Args:
            save_path: optional path to save the figure.
            pos_label: the positive class label used when computing ROC (default 1).
        """
        if auc is None or roc_curve is None:
            raise RuntimeError("scikit-learn is required for ROC plotting (roc_curve, auc).")

        # 1) Try to read precomputed values from self.metrics_
        fpr = tpr = thresholds = roc_auc = None
        if hasattr(self, "metrics_") and isinstance(self.metrics_, dict):
            m = self.metrics_
            # support m['roc_curve'] = dict(...)
            if "roc_curve" in m and isinstance(m["roc_curve"], dict):
                rc = m["roc_curve"]
                fpr = np.asarray(rc.get("fpr")) if rc.get("fpr") is not None else None
                tpr = np.asarray(rc.get("tpr")) if rc.get("tpr") is not None else None
                thresholds = np.asarray(rc.get("thresholds")) if rc.get("thresholds") is not None else None
                roc_auc = rc.get("auc", None)
            # support m['fpr'], m['tpr'], optional m['auc']
            elif "fpr" in m and "tpr" in m:
                fpr = np.asarray(m.get("fpr"))
                tpr = np.asarray(m.get("tpr"))
                thresholds = np.asarray(m.get("thresholds")) if "thresholds" in m else None
                roc_auc = m.get("auc", None)

        # 2) If not available, compute from stored arrays (try multiple attribute names)
        if fpr is None or tpr is None:
            # Ground truth candidates
            y_true = getattr(self, "y_true_", None)
            if y_true is None:
                y_true = getattr(self, "y_test_", None)

            # Score/proba candidates
            y_score = getattr(self, "y_score_", None)
            if y_score is None:
                # some code uses y_prob_
                y_score = getattr(self, "y_prob_", None)
            if y_score is None:
                # full proba matrix fallback (common name used in some pipelines)
                yp = getattr(self, "y_pred_proba_", None)
                if yp is not None and isinstance(yp, np.ndarray) and yp.ndim == 2:
                    y_score = yp[:, 1]
            # also support 'y_prob_' as 2D array directly
            if y_score is None and hasattr(self, "y_prob_"):
                yp2 = getattr(self, "y_prob_")
                if isinstance(yp2, np.ndarray) and yp2.ndim == 2:
                    y_score = yp2[:, 1]

            # if we still cannot compute, error
            if y_true is None or y_score is None:
                raise RuntimeError(
                    "Cannot compute ROC: provide either precomputed ROC in self.metrics_ or ensure "
                    "one of these pairs is present on the evaluator: "
                    "(y_true_ & y_score_), (y_test_ & y_prob_), or y_pred_proba_ (n x 2 matrix)."
                )

            # ensure numpy arrays
            y_true = np.asarray(y_true)
            y_score = np.asarray(y_score)

            # If user passed a 2D probability array accidentally, take column 1
            if y_score.ndim == 2 and y_score.shape[1] >= 2:
                y_score = y_score[:, 1]

            # compute ROC
            fpr, tpr, thresholds = roc_curve(y_true, y_score, pos_label=pos_label)
            roc_auc = auc(fpr, tpr)

            # store computed ROC in metrics_ for future usage
            try:
                if not hasattr(self, "metrics_") or not isinstance(self.metrics_, dict):
                    self.metrics_ = {}
                self.metrics_["roc_curve"] = {
                    "fpr": fpr.tolist(),
                    "tpr": tpr.tolist(),
                    "thresholds": thresholds.tolist(),
                    "auc": float(roc_auc)
                }
            except Exception:
                # ignore storage errors (shouldn't happen) but don't break plotting
                pass

        # 3) Plot
        plt.figure(figsize=(7, 6))
        plt.plot(fpr, tpr, lw=2, label=f"ROC (AUC = {roc_auc:.4f})" if roc_auc is not None else "ROC curve")
        plt.plot([0, 1], [0, 1], color="grey", lw=1, linestyle="--", label="Random (AUC = 0.5)")
        plt.xlim([-0.02, 1.02])
        plt.ylim([-0.02, 1.02])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate (Recall)")
        plt.title("ROC curve")
        plt.grid(alpha=0.3)
        plt.legend(loc="lower right", fontsize=10)

        # Optionally annotate best threshold (You may store best threshold in metrics_, e.g. 'best_threshold')
        best_thresh = None
        if hasattr(self, "metrics_") and isinstance(self.metrics_, dict):
            best_thresh = self.metrics_.get("best_threshold") or self.metrics_.get("best_thresh") or None

        if best_thresh is None and thresholds is not None:
            # pick threshold maximizing TPR - FPR (Youden's J)
            youden_idx = np.argmax(tpr - fpr)
            best_thresh = float(thresholds[youden_idx])
            # add marker
            plt.scatter(fpr[youden_idx], tpr[youden_idx], s=60, c="red", zorder=10,
                        label=f"Best thr: {best_thresh:.3f}")
            plt.legend(loc="lower right", fontsize=10)

        # Save / show
        if save_path:
            p = Path(save_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(p, dpi=300, bbox_inches="tight")
            print(f"ROC plot saved to: {p}")
        #plt.show()
        plt.close()

    def plot_precision_recall_curve(self, save_path: Union[str, Path, None] = None, pos_label=1):
        """
        Robust Precision-Recall plotting with diagnostics and graceful handling of degenerate inputs.
        """
        try:
            from sklearn.metrics import precision_recall_curve, average_precision_score
        except Exception:
            raise RuntimeError(
                "scikit-learn required for PR plotting (precision_recall_curve, average_precision_score).")

        # Try to load precomputed curve
        precision = recall = thresholds = avg_prec = None
        if hasattr(self, "metrics_") and isinstance(self.metrics_, dict):
            m = self.metrics_
            if "pr_curve" in m and isinstance(m["pr_curve"], dict):
                pc = m["pr_curve"]
                precision = np.asarray(pc.get("precision")) if pc.get("precision") is not None else None
                recall = np.asarray(pc.get("recall")) if pc.get("recall") is not None else None
                thresholds = np.asarray(pc.get("thresholds")) if pc.get("thresholds") is not None else None
                avg_prec = pc.get("average_precision", None)

        # If not present, compute from available attributes
        if precision is None or recall is None:
            # pick y_true
            y_true = getattr(self, "y_true_", None) or getattr(self, "y_test_", None)
            # pick y_score / prob
            y_score = getattr(self, "y_score_", None) or getattr(self, "y_prob_", None)
            if y_score is None:
                yp = getattr(self, "y_pred_proba_", None)
                if yp is not None and isinstance(yp, np.ndarray) and yp.ndim == 2:
                    y_score = yp[:, 1]
            # another fallback
            if y_score is None and hasattr(self, "y_prob_"):
                yp2 = getattr(self, "y_prob_")
                if isinstance(yp2, np.ndarray) and yp2.ndim == 2:
                    y_score = yp2[:, 1]

            if y_true is None or y_score is None:
                raise RuntimeError(
                    "Cannot compute PR curve: ensure precomputed 'pr_curve' in metrics_ or "
                    "that evaluator has (y_test_ & y_prob_) or (y_true_ & y_score_) or y_pred_proba_."
                )

            y_true = np.asarray(y_true).ravel()
            y_score = np.asarray(y_score).ravel()
            if y_score.ndim == 2 and y_score.shape[1] >= 2:
                y_score = y_score[:, 1]

            # Basic diagnostics
            n = y_true.shape[0]
            pos_count = int(np.sum(y_true == pos_label))
            pos_rate = pos_count / max(1, n)
            print(f"PR DIAG: n={n}, positives={pos_count} ({pos_rate:.3%})")
            # show some sample scores to debug
            try:
                print("PR DIAG: y_score sample:", np.unique(np.round(y_score[:20], 4)))
            except Exception:
                pass

            # handle degenerate cases: no positives or constant scores
            if pos_count == 0:
                # cannot compute meaningful PR curve
                precision = np.array([1.0])  # convention: precision=1 when no positive predictions?
                recall = np.array([0.0])
                thresholds = np.array([])
                avg_prec = None
                degenerate_msg = "No positive samples in y_true — PR curve not defined."
            elif np.all(y_score == y_score[0]):
                # constant score for all samples
                precision, recall, thresholds = precision_recall_curve(y_true, y_score, pos_label=pos_label)
                try:
                    avg_prec = float(average_precision_score(y_true, y_score))
                except Exception:
                    avg_prec = None
                degenerate_msg = "All predicted scores are constant — PR curve may be degenerate."
            else:
                # Normal case
                precision, recall, thresholds = precision_recall_curve(y_true, y_score, pos_label=pos_label)
                try:
                    avg_prec = float(average_precision_score(y_true, y_score))
                except Exception:
                    avg_prec = None
                degenerate_msg = None

            # persist computed values
            try:
                if not hasattr(self, "metrics_") or not isinstance(self.metrics_, dict):
                    self.metrics_ = {}
                self.metrics_["pr_curve"] = {
                    "precision": precision.tolist(),
                    "recall": recall.tolist(),
                    "thresholds": thresholds.tolist() if thresholds is not None else None,
                    "average_precision": float(avg_prec) if avg_prec is not None else None
                }
            except Exception:
                pass

        # Ensure 1-D arrays
        precision = np.asarray(precision).ravel()
        recall = np.asarray(recall).ravel()
        if thresholds is not None:
            thresholds = np.asarray(thresholds).ravel()

        # Validate lengths
        if precision.size == 0 or recall.size == 0:
            raise RuntimeError("Computed precision/recall arrays are empty — cannot plot PR curve.")

        # Plot
        plt.figure(figsize=(7, 6))
        # step plot (common for PR)
        plt.step(recall, precision, where='post', lw=2,
                 label=f"AP = {avg_prec:.4f}" if avg_prec is not None else "PR curve")
        # fill area (works with 1-D arrays)
        try:
            plt.fill_between(recall, precision, alpha=0.2, step='post')
        except TypeError:
            # older matplotlib versions may not support step arg for fill_between
            plt.fill_between(recall, precision, alpha=0.2)

        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title("Precision-Recall curve")
        plt.grid(alpha=0.3)
        plt.legend(loc="lower left")

        # annotate best threshold (F1-maximizing) if thresholds available
        if thresholds is not None and thresholds.size > 0 and precision.size >= 2:
            prec_for_thr = precision[:-1]
            rec_for_thr = recall[:-1]
            # avoid divide-by-zero
            denom = (prec_for_thr + rec_for_thr + 1e-12)
            f1_scores = (2 * prec_for_thr * rec_for_thr) / denom
            best_idx = int(np.nanargmax(f1_scores))
            best_thr = float(thresholds[best_idx])
            plt.scatter(rec_for_thr[best_idx], prec_for_thr[best_idx], s=60, c="red", zorder=10,
                        label=f"Best thr (F1): {best_thr:.3f}")
            plt.legend(loc="lower left")

        # If degenerate, add text to explain
        if 'degenerate_msg' in locals() and degenerate_msg is not None:
            plt.gcf().text(0.02, 0.95, degenerate_msg, fontsize=9, color='red')

        # Save / show
        if save_path:
            p = Path(save_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(p, dpi=300, bbox_inches="tight")
            print(f"PR plot saved to: {p}")
        #plt.show()
        plt.close()


    def plot_calibration_dashboard(self,
                                   save_path: Union[str, Path, None] = None,
                                   n_bins: int = 10,
                                   n_bootstrap: int = 200,
                                   ci: float = 0.90,
                                   show_brier_decomp: bool = False):
        """
        calibration dashboard:
          - Reliability curve (with optional bootstrap CI)
          - Histogram of predicted probabilities
          - ECE, MCE, Brier score computed and annotated
        """
        try:
            from sklearn.calibration import calibration_curve
            from sklearn.metrics import brier_score_loss
        except Exception:
            raise RuntimeError(
                "scikit-learn is required for calibration dashboard (calibration_curve, brier_score_loss).")

        # ---- Safely pick y_true and y_prob without using `or` on Series ----
        y_true = getattr(self, "y_test_", None)
        if y_true is None:
            y_true = getattr(self, "y_true_", None)

        y_prob = getattr(self, "y_prob_", None)
        if y_prob is None:
            y_prob = getattr(self, "y_score_", None)

        # fallback to y_pred_proba_ or y_pred_proba if available (many different pipelines use different names)
        if y_prob is None:
            yp = getattr(self, "y_pred_proba_", None) or getattr(self, "y_pred_proba", None)
            if yp is not None:
                try:
                    yp_arr = np.asarray(yp)
                    if yp_arr.ndim == 2 and yp_arr.shape[1] >= 2:
                        y_prob = yp_arr[:, 1]
                    elif yp_arr.ndim == 1:
                        y_prob = yp_arr
                except Exception:
                    y_prob = None

        if y_true is None or y_prob is None:
            raise RuntimeError(
                "Calibration dashboard requires y_test_ (or y_true_) and y_prob_ (or y_score_ or y_pred_proba_). Run evaluate() first.")

        # Convert to 1-D numpy arrays
        y_true = np.asarray(y_true).ravel()
        y_prob = np.asarray(y_prob).ravel()
        if y_prob.ndim != 1:
            # if accidentally 2D with single column, flatten
            y_prob = y_prob.reshape(-1)

        # If y_prob is 2D keep only positive-class column if shape[1] >= 2
        if y_prob.ndim == 2 and y_prob.shape[1] >= 2:
            y_prob = y_prob[:, 1]

        n = len(y_true)
        if n == 0 or len(y_prob) == 0:
            raise RuntimeError("Empty arrays for y_true or y_prob - cannot compute calibration.")

        pos = int(np.sum(y_true == 1))
        prevalence = pos / max(1, n)

        # Compute reliability curve (use quantile bins for plotting to avoid empty bins)
        try:
            prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=n_bins, strategy='quantile')
        except Exception:
            # fallback to default strategy
            prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=n_bins)

        # Compute ECE and MCE using equal-width bins (standard approach)
        bins = np.linspace(0.0, 1.0, n_bins + 1)
        # digitize returns indices 1..n_bins, subtract 1 so it is 0..n_bins-1
        bin_ids = np.digitize(y_prob, bins) - 1
        ece = 0.0
        mce = 0.0
        for i in range(n_bins):
            mask = bin_ids == i
            if not np.any(mask):
                continue
            bin_size = mask.sum()
            bin_acc = float(np.mean(y_true[mask]))
            bin_conf = float(np.mean(y_prob[mask]))
            w = bin_size / n
            ece += w * abs(bin_conf - bin_acc)
            mce = max(mce, abs(bin_conf - bin_acc))

        # Brier score
        brier = float(brier_score_loss(y_true, y_prob))

        # Optional bootstrap CI for reliability curve
        lower = upper = None
        if n_bootstrap and n_bootstrap > 0:
            boot_matrix = np.full((n_bootstrap, len(prob_true)), np.nan, dtype=float)
            rng = np.random.default_rng(seed=42)
            for b in range(n_bootstrap):
                idx = rng.integers(0, n, n)
                yt = y_true[idx]
                yp = y_prob[idx]
                try:
                    pt, pp = calibration_curve(yt, yp, n_bins=n_bins, strategy='quantile')
                except Exception:
                    try:
                        pt, pp = calibration_curve(yt, yp, n_bins=n_bins)
                    except Exception:
                        pt = None
                if pt is not None and len(pt) == len(prob_true):
                    boot_matrix[b, :] = pt
            # compute percentile CI, ignoring nan rows
            alpha = 1.0 - ci
            lower = np.nanpercentile(boot_matrix, 100.0 * (alpha / 2.0), axis=0)
            upper = np.nanpercentile(boot_matrix, 100.0 * (1.0 - alpha / 2.0), axis=0)

        # --- Plotting: two-panel layout (replacement) ---
        # Enable constrained layout globally for this figure
        plt.rcParams['figure.constrained_layout.use'] = True

        fig = plt.figure(figsize=(14, 6), constrained_layout=True)
        gs = GridSpec(1, 3, width_ratios=[2, 1, 0.05], figure=fig)

        # Left big plot (reliability curve)
        ax_main = fig.add_subplot(gs[0, 0])

        # Right column split into two rows: histogram (top) and metrics box (bottom)
        sub_gs = GridSpecFromSubplotSpec(2, 1,
                                         subplot_spec=gs[0, 1],
                                         height_ratios=[3, 1],
                                         hspace=0.12)
        ax_hist_top = fig.add_subplot(sub_gs[0, 0])
        ax_metrics = fig.add_subplot(sub_gs[1, 0])

        # --- LEFT: reliability curve ---
        ax_main.plot([0, 1], [0, 1], linestyle='--', color='k', label='Perfect')
        ax_main.plot(prob_pred, prob_true, marker='o', lw=2, label='Model')

        if lower is not None and upper is not None:
            # fill CI using the bin midpoints (prob_pred). stepless fill is fine here.
            ax_main.fill_between(prob_pred, lower, upper, color='C0', alpha=0.22, step='mid',
                                 label=f'{int(ci * 100)}% CI')

        ax_main.set_xlabel('Predicted probability (mean in bin)')
        ax_main.set_ylabel('Fraction of positives (observed)')
        ax_main.set_xlim(0, 1)
        ax_main.set_ylim(0, 1)
        ax_main.set_title('Calibration (Reliability) Curve')
        ax_main.grid(alpha=0.25)
        ax_main.legend(loc='upper left', fontsize=9)

        # --- RIGHT TOP: histogram of predicted probabilities ---
        ax_hist_top.hist(y_prob, bins=20, range=(0, 1), alpha=0.85, color='#ffad60', edgecolor='k', linewidth=0.4)
        ax_hist_top.set_title('Probability Distribution', pad=8)
        ax_hist_top.set_xlabel('Predicted probability')
        ax_hist_top.set_ylabel('Count')
        ax_hist_top.grid(False)

        # Make histogram ticks/labels a bit smaller so it fits nicely
        for item in ([ax_hist_top.title, ax_hist_top.xaxis.label, ax_hist_top.yaxis.label] +
                     ax_hist_top.get_xticklabels() + ax_hist_top.get_yticklabels()):
            item.set_fontsize(9)

        metrics_text = (
            f"N = {n}\n"
            f"Positives = {pos} ({prevalence:.2%})\n\n"
            f"ECE = {ece:.4f}\n"
            f"MCE = {mce:.4f}\n"
            f"Brier = {brier:.4f}\n"
            f"Bins = {n_bins}\n"
            f"AP = {self.metrics_.get('pr_curve', {}).get('average_precision') if isinstance(self.metrics_, dict) else 'N/A'}"
        )

        ax_metrics.axis('off')
        # left=0.01 and top=0.98 places text nicely within the little axes; use monospace for alignment
        ax_metrics.text(0.01, 0.98, metrics_text, fontsize=9, fontfamily='monospace',
                        verticalalignment='top', horizontalalignment='left',
                        wrap=True,
                        bbox=dict(boxstyle="round,pad=0.6", facecolor="white", edgecolor="black", alpha=0.95))

        # Title and final layout tweaks
        #plt.suptitle('Calibration Dashboard', fontsize=14, y=0.98)

        if save_path:
            p = Path(save_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(p, dpi=300, bbox_inches='tight')
            print(f"Calibration dashboard saved to: {p}")

        #plt.show()
        plt.close()

        # store calibration numbers in metrics_
        try:
            if not hasattr(self, 'metrics_') or not isinstance(self.metrics_, dict):
                self.metrics_ = {}
            self.metrics_['calibration'] = {
                'prob_true': prob_true.tolist(),
                'prob_pred': prob_pred.tolist(),
                'bins': n_bins,
                'ece': float(ece),
                'mce': float(mce),
                'brier': float(brier)
            }
        except Exception:
            pass
