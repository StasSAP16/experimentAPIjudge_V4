import matplotlib.pyplot as plt
import numpy as np
import os

# ==========================================
# ДАННЫЕ ДЛЯ ВИЗУАЛИЗАЦИИ
# ==========================================
metrics_ds = {
    'coverage': 80.0,
    'metrics': {
        'Functional Equivalence': {'percentage': 70.0},
        'Granularity Difference': {'percentage': 60.0},
        'No Match': {'percentage': 0.0}, # Инвертируется в 100
        'Identical Match': {'percentage': 0.0}
    }
}

metrics_gg = {
    'coverage': 60.0,
    'metrics': {
        'Functional Equivalence': {'percentage': 50.0},
        'Granularity Difference': {'percentage': 30.0},
        'No Match': {'percentage': 20.0}, # Инвертируется в 80
        'Identical Match': {'percentage': 40.0}
    }
}

# Цвета для моделей (скорректированы для идеального совпадения с оригиналом)
colors_ds = '#348ABD'  # Мягкий синий (DeepSeek)
colors_gg = '#E24A33'  # Красно-оранжевый (Gemini-2.5-flash)

# ==========================================
# VISUALIZATION
# ==========================================
def plot_radar_chart(metrics_ds, metrics_gg, colors_ds, colors_gg, output_path='./radar_chart.png'):
    # Инициализация графика
    fig4, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))
    
    # Категории для диаграммы
    categories = ['Coverage', 'Functional\nEq %', 'Granularity\nDiff %', 'No Match\n(inverted)', 'Identical\nMatch %', 'JSON\nCompliance']
    N = len(categories)
    
    # Значения (нормализованы к шкале 0-100)
    # No Match инвертирован: чем меньше ошибок, тем лучше (100 - value)
    ds_values = [
        metrics_ds['coverage'],
        metrics_ds['metrics']['Functional Equivalence']['percentage'],
        metrics_ds['metrics']['Granularity Difference']['percentage'],
        100 - metrics_ds['metrics']['No Match']['percentage'],
        metrics_ds['metrics']['Identical Match']['percentage'],
        100  # JSON Compliance
    ]
    
    gg_values = [
        metrics_gg['coverage'],
        metrics_gg['metrics']['Functional Equivalence']['percentage'],
        metrics_gg['metrics']['Granularity Difference']['percentage'],
        100 - metrics_gg['metrics']['No Match']['percentage'],
        metrics_gg['metrics']['Identical Match']['percentage'],
        100
    ]
    
    # Вычисляем угол для каждой категории
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Замыкаем полигон
    
    ds_values += ds_values[:1]
    gg_values += gg_values[:1]
    
    # Построение графика DeepSeek
    ax.plot(angles, ds_values, 'o-', linewidth=3, label='DeepSeek', color=colors_ds)
    ax.fill(angles, ds_values, alpha=0.25, color=colors_ds)
    
    # Построение графика Gemini
    ax.plot(angles, gg_values, 'o-', linewidth=3, label='Gemini-2.5-flash', color=colors_gg)
    ax.fill(angles, gg_values, alpha=0.25, color=colors_gg)
    
    # Настройка осей и меток
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=9, color='gray')
    ax.grid(True, alpha=0.3)
    
    # Заголовок и легенда
    ax.set_title('Model Performance Radar Chart\n(Bigger area = better overall performance)',
                 fontsize=14, fontweight='bold', pad=30)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
    
    plt.tight_layout()
    
    # Безопасное сохранение
    save_dir = os.path.dirname(output_path)
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    print(f"✅ Radar chart saved to {output_path}")
    plt.show()

# ==========================================
# ЗАПУСК
# ==========================================
if __name__ == "__main__":
    plot_radar_chart(metrics_ds, metrics_gg, colors_ds, colors_gg)