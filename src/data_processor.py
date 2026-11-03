"""
数据清洗与分析模块
负责数据清洗、异常检测和统计分析
"""
import pandas as pd
from typing import List, Dict
import os


class DataProcessor:
    def __init__(self):
        self.stats = {
            "total": 0,
            "empty_filled": 0,
            "duplicates_removed": 0,
            "outliers_detected": 0
        }
        self.summary = {}

    def process(self, records: List[Dict]) -> pd.DataFrame:
        """主处理流程：清洗 + 异常检测 + 统计"""
        df = pd.DataFrame([r["fields"] for r in records])
        self.stats["total"] = len(df)

        # 1. 填充空值
        df = self._fill_empty_values(df)

        # 2. 去重
        df = self._remove_duplicates(df)

        # 3. 格式标准化
        df = self._normalize_formats(df)

        # 4. 异常检测（3σ 原则）
        df = self._detect_outliers(df)

        # 5. 统计分析
        self._generate_summary(df)

        return df

    def _fill_empty_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """填充空值：字符串列填'未知'，数值列填0"""
        for col in df.columns:
            if df[col].dtype == "object":
                empty_count = df[col].isna().sum()
                df[col] = df[col].fillna("未知")
                self.stats["empty_filled"] += empty_count
            elif pd.api.types.is_numeric_dtype(df[col]):
                empty_count = df[col].isna().sum()
                df[col] = df[col].fillna(0)
                self.stats["empty_filled"] += empty_count
        return df

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """去除重复数据"""
        before = len(df)
        df = df.drop_duplicates()
        self.stats["duplicates_removed"] = before - len(df)
        return df

    def _normalize_formats(self, df: pd.DataFrame) -> pd.DataFrame:
        """格式标准化：字符串去首尾空格"""
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].str.strip()
        return df

    def _detect_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """异常检测：3σ 原则，超出均值±3倍标准差的标记为异常"""
        numeric_cols = df.select_dtypes(include=["number"]).columns
        outlier_count = 0

        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            if std == 0:
                continue
            # 标记异常值
            outliers = df[(df[col] < mean - 3*std) | (df[col] > mean + 3*std)]
            outlier_count += len(outliers)

        self.stats["outliers_detected"] = outlier_count
        return df

    def _generate_summary(self, df: pd.DataFrame) -> Dict:
        """生成统计摘要"""
        summary = {
            "row_count": len(df),
            "col_count": len(df.columns),
            "columns": list(df.columns)
        }

        numeric_cols = df.select_dtypes(include=["number"]).columns
        if len(numeric_cols) > 0:
            summary["numeric_stats"] = {}
            for col in numeric_cols:
                summary["numeric_stats"][col] = {
                    "mean": round(df[col].mean(), 2),
                    "max": round(df[col].max(), 2),
                    "min": round(df[col].min(), 2),
                    "std": round(df[col].std(), 2)
                }

        self.summary = summary
        return summary

    def generate_report(self, output_path: str = "output/sync_report.md") -> str:
        """生成 Markdown 格式的同步报告"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        lines = ["# 数据同步报告\n"]
        lines.append(f"## 处理统计")
        lines.append(f"- 总记录数：{self.stats['total']}")
        lines.append(f"- 填充空值：{self.stats['empty_filled']} 处")
        lines.append(f"- 去除重复：{self.stats['duplicates_removed']} 条")
        lines.append(f"- 检测到异常值：{self.stats['outliers_detected']} 条\n")

        if self.summary.get("numeric_stats"):
            lines.append("## 数值列统计")
            for col, stats in self.summary["numeric_stats"].items():
                lines.append(f"### {col}")
                lines.append(f"- 均值：{stats['mean']}")
                lines.append(f"- 最大值：{stats['max']}")
                lines.append(f"- 最小值：{stats['min']}")
                lines.append(f"- 标准差：{stats['std']}\n")

        report_content = "\n".join(lines)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        return output_path

    def get_stats(self) -> Dict:
        return self.stats

    def get_summary(self) -> Dict:
        return self.summary


if __name__ == "__main__":
    processor = DataProcessor()
    print("数据处理器初始化完成")
