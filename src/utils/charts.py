import plotly.express as px

"""
📈 DATA VISUALIZATION & ANALYTICS MOTOR LAYER (Kağan Aydın)
TR: Veri setinin Keşifsel Veri Analizi (EDA) grafiklerinin Plotly ile responsive 
    ve yüksek kontrastlı olarak çizdirildiği harici grafik motoru katmanıdır.
EN: External graphics engine layer where EDA charts are rendered using Plotly.
"""

def draw_traffic_peaks_chart(df, labels_dict, is_area=True):
    """Hourly traffic trend analytics layout"""
    hourly_data = df.groupby('HOUR')['NUMBER_OF_VEHICLES'].mean().reset_index()
    if is_area:
        fig = px.area(hourly_data, x='HOUR', y='NUMBER_OF_VEHICLES', labels=labels_dict)
        fig.update_traces(fillcolor='rgba(15, 23, 42, 0.04)', line_color='#0f172a', line_width=4)
    else:
        fig = px.line(hourly_data, x='HOUR', y='NUMBER_OF_VEHICLES', labels=labels_dict)
        fig.update_traces(line_color='#0f172a', line_width=4)
        
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=15, b=15, l=15, r=15), height=400,
        xaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(color='#0f172a', size=11, weight='bold'), title=dict(font=dict(color='#0f172a', size=12, weight='bold'))),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(color='#0f172a', size=11, weight='bold'), title=dict(font=dict(color='#0f172a', size=12, weight='bold')))
    )
    return fig

def draw_weekday_weekend_chart(df, labels_dict):
    """Temporal categorical comparison layout"""
    weekend_data = df.groupby('IS_WEEKEND')['NUMBER_OF_VEHICLES'].mean().reset_index()
    fig = px.bar(weekend_data, x='IS_WEEKEND', y='NUMBER_OF_VEHICLES', color='IS_WEEKEND', color_discrete_sequence=['#0f172a', '#94a3b8'], labels=labels_dict)
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', showlegend=False, margin=dict(t=15, b=15, l=15, r=15), height=450,
        xaxis=dict(showgrid=False, tickfont=dict(color='#0f172a', size=11, weight='bold'), title=dict(font=dict(color='#0f172a', size=12, weight='bold'))),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(color='#0f172a', size=11, weight='bold'), title=dict(font=dict(color='#0f172a', size=12, weight='bold')))
    )
    return fig

def draw_correlation_matrix(df, columns, display_labels):
    """Statistical feature importance heat matrix layout"""
    corr_matrix = df[columns].corr().values
    fig = px.imshow(corr_matrix, x=display_labels, y=display_labels, color_continuous_scale='blues')
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=15, b=15, l=15, r=15), height=450,
        xaxis=dict(tickfont=dict(color='#0f172a', size=11, weight='bold')), yaxis=dict(tickfont=dict(color='#0f172a', size=11, weight='bold')),
        coloraxis_colorbar=dict(tickfont=dict(color='#0f172a', size=11, weight='bold'), title=dict(font=dict(color='#0f172a', size=11, weight='bold')))
    )
    return fig