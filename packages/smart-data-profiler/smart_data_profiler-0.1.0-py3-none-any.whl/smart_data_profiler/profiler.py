import pandas as pd
import numpy as np
from jinja2 import Template
import os
import matplotlib.pyplot as plt
import seaborn as sns


class SmartProfiler:

    def __init__(self, data):
        """Initialize the profiler with a CSV path or pandas DataFrame."""
        if isinstance(data, str):
            self.df = pd.read_csv(data)
        elif isinstance(data, pd.DataFrame):
            self.df = data
        else:
            raise ValueError("Please provide a valid CSV file path or DataFrame.")

        self.report = {}

    def analyze(self):
        """Analyze dataset structure and compute basic stats."""
        df = self.df

        self.report["shape"] = df.shape
        self.report["columns"] = list(df.columns)
        self.report["dtypes"] = df.dtypes.astype(str).to_dict()
        self.report["missing"] = df.isnull().sum().to_dict()
        self.report["describe"] = df.describe(include="all").to_dict()

        self.report["outliers"] = self.detect_outliers()
        self.report["heatmap_path"] = self.generate_correlation_heatmap()
        self.report["insights"] = self.generate_insights()

        return self.report

    def health_score(self):
        """Compute a simple dataset health score (based on missing values)."""
        total_cells = self.df.shape[0] * self.df.shape[1]
        missing = self.df.isnull().sum().sum()
        score = 100 - (missing / total_cells * 100)
        return round(score, 2)

    def generate_html(self, output_file="report.html"):
        """Generate an HTML report using a Jinja2 template."""
        template_path = os.path.join(os.path.dirname(__file__), "templates", "report_template.html")

        with open(template_path, "r", encoding="utf-8") as file:
            template = Template(file.read())

        html = template.render(report=self.report, score=self.health_score())

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ Report generated successfully: {output_file}")

    def detect_outliers(self):
        """Detect outliers in numeric columns using the IQR method."""
        df = self.df.select_dtypes(include=[np.number])
        outlier_summary = {}

        for col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_summary[col] = {
                "count": len(outliers),
                "percentage": round(len(outliers) / len(df) * 100, 2)
            }

        self.report["outliers"] = outlier_summary
        return outlier_summary

    def generate_correlation_heatmap(self, output_path="correlation_heatmap.png"):
        """Generate and save a correlation heatmap for numeric columns."""
        df = self.df.select_dtypes(include=[np.number])

        if df.empty or df.shape[1] < 2:
            print("⚠️ Not enough numeric columns for correlation heatmap.")
            return None

        corr = df.corr(numeric_only=True)
        plt.figure(figsize=(6, 4))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Heatmap", fontsize=14)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        print(f"🖼️ Heatmap saved: {output_path}")
        return output_path

    def generate_insights(self):
        """Generate human-readable insights from the dataset."""
        insights = []

        # 1️⃣ Missing values
        missing = self.report.get("missing", {})
        for col, count in missing.items():
            if count > 0:
                percentage = round((count / len(self.df)) * 100, 2)
                insights.append(
                    f"🔹 Column '{col}' has {count} missing values ({percentage}%) — consider filling with median or mode."
                )

        # 2️⃣ Outlier detection
        outliers = self.report.get("outliers", {})
        for col, info in outliers.items():
            if info["percentage"] > 10:
                insights.append(
                    f"⚠️ Column '{col}' has {info['percentage']}% outliers — consider applying normalization or winsorization."
                )

        # 3️⃣ Correlation analysis
        df = self.df.select_dtypes(include=[np.number])
        if df.shape[1] >= 2:
            corr = df.corr(numeric_only=True)
            for i in range(len(corr.columns)):
                for j in range(i + 1, len(corr.columns)):
                    val = corr.iloc[i, j]
                    if abs(val) > 0.8:
                        c1, c2 = corr.columns[i], corr.columns[j]
                        insights.append(
                            f"🔗 Columns '{c1}' and '{c2}' are highly correlated (corr = {val:.2f}) — consider removing one."
                        )

        # 4️⃣ If no issues found
        if not insights:
            insights.append("✅ Dataset looks healthy — no major issues detected!")

        self.report["insights"] = insights
        return insights
