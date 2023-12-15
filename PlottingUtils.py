import matplotlib.pyplot as plt

def plot_multiple_charts(charts_data):
    num_charts = len(charts_data)
    
    if num_charts % 2 == 0:
        rows, cols = num_charts // 2, 2
    else:
        rows, cols = (num_charts + 1) // 2, 1

    fig, axs = plt.subplots(rows, cols, figsize=(12, 8))
    fig.tight_layout(pad=5.0)

    for idx, chart_data in enumerate(charts_data):
        if num_charts % 2 == 0:
            ax = axs[idx // cols, idx % cols]
        else:
            ax = axs[idx, 0] if num_charts == 1 else axs[idx // 2, idx % 2]

        ax.plot(chart_data['x'], chart_data['y'], label=chart_data['title'])
        ax.set_xlabel(chart_data['x_label'])
        ax.set_ylabel(chart_data['y_label'])
        ax.set_title(chart_data['title'])
        ax.legend()

    plt.show()


def overlay_multiple_charts(data_list, x_label, y_label, title):
    plt.figure(figsize=(10, 6))
    markers = ['o', 's', '^', '*', 'D']  
    
    for idx, data in enumerate(data_list):
        plt.scatter(data['x'], data['y'], label=data['label'], marker=markers[idx])
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.show()

