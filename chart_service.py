import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class ChartService:
    @staticmethod
    def generate_portfolio_pie_chart(category_values: dict, total_val_toman: float) -> io.BytesIO:
        """
        تولید نمودار دایره‌ای زیبا و حرفه‌ای از توزیع سبد دارایی
        """
        # فیلتر مقادیر بیشتر از صفر
        data = {k: v for k, v in category_values.items() if v > 0}
        if not data:
            return None

        labels = list(data.keys())
        values = list(data.values())

        # رنگ‌های مدرن و شیک مالی
        colors = ['#FFD700', '#C0C0C0', '#FFA500', '#00C853', '#00E5FF', '#AB47BC']

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(aspect="equal"), dpi=150)

        # رسم نمودار دوناتی
        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,
            autopct='%1.1f%%',
            pctdistance=0.75,
            colors=colors[:len(values)],
            startangle=140,
            wedgeprops=dict(width=0.45, edgecolor='#1E1E1E', linewidth=2)
        )

        for autotext in autotexts:
            autotext.set_color('#FFFFFF')
            autotext.set_fontsize(11)
            autotext.set_weight('bold')

        # راهنمای لژند در کنار نمودار
        legend_labels = [
            f"{label}: {val:,.0f} T ({val/total_val_toman*100:.1f}%)"
            for label, val in zip(labels, values)
        ]
        ax.legend(
            wedges,
            legend_labels,
            title="Asset Distribution",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=10,
            frameon=False
        )

        ax.set_title(f"Portfolio Breakdown\nTotal: {int(total_val_toman):,d} Tomans", fontsize=13, weight='bold', pad=20, color='#E0E0E0')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=False, facecolor='#121212')
        buf.seek(0)
        plt.close(fig)
        return buf

chart_service = ChartService()
