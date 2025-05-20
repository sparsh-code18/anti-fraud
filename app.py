from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)
app.secret_key = 'supersecretmre'

df = pd.read_csv('Anti_Fraud_Centre_Data.csv')


@app.route('/')
def landing():
    # flash('Welcome to the Flask App', 'info')
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/form', methods=['GET','POST'])
def forminput():
    return render_template('form.html')

@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

#Graph Functions
def complain_submission_method():
    complaint_methods = df['Complaint Received Type'].value_counts().reset_index()
    complaint_methods.columns = ['Method', 'Count']

    fig1 = px.bar(complaint_methods,
                x='Method',
                y='Count',
                title='Most Used Complaint Submission Methods',
                template='plotly_white',
                color='Count',
                color_continuous_scale='Viridis')

    fig1.update_layout(
        title_x=0.5,
        xaxis_title='Submission Method',
        yaxis_title='Number of Complaints',
        showlegend=False,
        plot_bgcolor='white',
        xaxis_tickangle=45
    )
    graph1 = pio.to_html(fig1, full_html=False)
    return graph1

# solicitation
def complain_solicitation_method():
    solicitation_methods = df['Solicitation Method'].value_counts().reset_index()
    solicitation_methods.columns = ['Method', 'Count']

    fig2 = px.pie(solicitation_methods,
             values='Count',
             names='Method',
             title='Distribution of Fraud Solicitation Methods',
             hole=0.4,  # Creates a donut chart
             color_discrete_sequence=px.colors.qualitative.Set3)

    fig2.update_layout(
    title_x=0.5,
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.5,
        xanchor='center',
        x=0.5
    )
)
    graph2 = pio.to_html(fig2, full_html=False)
    return graph2

#distribution of solicitation methods
def complain_distribution_method():
    df['Dollar Loss Clean'] = df['Dollar Loss /pertes financires'].astype(str).str.replace('$', '')
    df['Dollar Loss Clean'] = df['Dollar Loss Clean'].str.replace(',', '')
    df['Dollar Loss Clean'] = pd.to_numeric(df['Dollar Loss Clean'], errors='coerce')

# 3. Correlation between solicitation method and dollar loss (Box Plot)
    fig3 = px.box(df,
            x='Solicitation Method',
            y='Dollar Loss Clean',
            title='Dollar Loss Distribution by Solicitation Method',
            template='plotly_white',
            color='Solicitation Method',
            color_discrete_sequence=px.colors.qualitative.Set3)

    fig3.update_layout(
    title_x=0.5,
    xaxis_title='Solicitation Method',
    yaxis_title='Dollar Loss ($)',
    showlegend=False,
    xaxis_tickangle=45,
    plot_bgcolor='white',
    height=600  # Make the plot taller for better visibility
)

    graph3 = pio.to_html(fig3, full_html=False)
    return graph3

#demographic analysis
def age_group_method():
    age_group_counts = df.groupby("Victim Age Range / Tranche d'ge des victimes").size().reset_index(name='Count')

    fig1 = px.bar(age_group_counts, 
             x="Victim Age Range / Tranche d'ge des victimes", 
             y='Count',
             title='Cases by Age Group',
             template='plotly_white',
             color='Count',
             color_continuous_scale='Viridis')

    fig1.update_layout(
    title_x=0.5,
    xaxis_title='Age Group',
    yaxis_title='Number of Cases',
    showlegend=False,
    plot_bgcolor='white'
)
    graph1 = pio.to_html(fig1, full_html=False)
    return graph1

# case gender
def case_gender_method():
    gender_counts = df.groupby('Gender').size().reset_index(name='Count')

    fig2 = px.pie(gender_counts, 
             values='Count', 
             names='Gender',
             title='Distribution of Cases by Gender',
             hole=0.4,
             color_discrete_sequence=px.colors.qualitative.Set3)

    fig2.update_layout(
    title_x=0.5,
    showlegend=True
)
    graph2 = pio.to_html(fig2, full_html=False)
    return graph2


#average dollar loss

def average_dollar_loss_method():
    df['Dollar Loss Clean'] = df['Dollar Loss /pertes financires'].astype(str).str.replace('$', '')
    df['Dollar Loss Clean'] = df['Dollar Loss Clean'].str.replace(',', '')
    df['Dollar Loss Clean'] = pd.to_numeric(df['Dollar Loss Clean'], errors='coerce')

# 3. Cross-tab: Age group vs. Dollar loss (Heatmap)
# Create pivot table for age group vs dollar loss
    pivot_table = df.pivot_table(
           values='Dollar Loss Clean',
           index="Victim Age Range / Tranche d'ge des victimes",
           aggfunc='mean',
           fill_value=0
).round(2)

    fig3 = px.imshow(pivot_table,
            aspect='auto',
            title='Average Dollar Loss by Age Group',
            color_continuous_scale='RdYlBu_r')

    fig3.update_layout(
            title_x=0.5,
            xaxis_title='',
            yaxis_title='Age Group',
            coloraxis_colorbar_title='Avg Dollar Loss ($)',
            height=400  # Make the heatmap taller for better visibility
)

    graph3 = pio.to_html(fig3, full_html=False)
    return graph3

#distribution of lang
def distribution_lang_method():
   lang_counts = df.groupby('Language of Correspondence').size().reset_index(name='Count')

   fig4 = px.pie(lang_counts,
             values='Count',
             names='Language of Correspondence',
             title='Distribution by Language of Correspondence',
             color_discrete_sequence=px.colors.qualitative.Set2)

   fig4.update_layout(
            title_x=0.5,
            showlegend=True
)

   graph4 = pio.to_html(fig4, full_html=False)
   return graph4

#distribution by gender
def gender_method():
    age_gender_dist = pd.crosstab(df["Victim Age Range / Tranche d'ge des victimes"], df['Gender'])

    fig5 = px.bar(age_gender_dist,
             title='Age Group Distribution by Gender',
             template='plotly_white',
             barmode='stack',
             color_discrete_sequence=px.colors.qualitative.Safe)

    fig5.update_layout(
    title_x=0.5,
    xaxis_title='Age Group',
    yaxis_title='Count',
    showlegend=True,
    legend_title='Gender',
    plot_bgcolor='white'
)
    graph5 = pio.to_html(fig5, full_html=False)
    return graph5

#victims by age
def victims_by_age_method():
    avg_victims = df.groupby("Victim Age Range / Tranche d'ge des victimes")['Number of Victims / Nombre de victimes'].mean().reset_index()

    fig6 = px.bar(avg_victims,
             x="Victim Age Range / Tranche d'ge des victimes",
             y='Number of Victims / Nombre de victimes',
             title='Average Number of Victims by Age Group',
             template='plotly_white',
             color='Number of Victims / Nombre de victimes',
             color_continuous_scale='Viridis')

    fig6.update_layout(
            title_x=0.5,
            xaxis_title='Age Group',
            yaxis_title='Average Number of Victims',
            showlegend=False,
            plot_bgcolor='white'
    )
    graph6 = pio.to_html(fig6, full_html=False)
    return graph6

#distribution of cases by gender

def gender_method():
    lang_gender_dist = pd.crosstab(df['Language of Correspondence'], df['Gender'])

    fig7 = px.bar(lang_gender_dist,
             title='Distribution of Cases by Language and Gender',
             template='plotly_white',
             barmode='group',
             color_discrete_sequence=px.colors.qualitative.Set3)

    fig7.update_layout(
    title_x=0.5,
    xaxis_title='Language of Correspondence',
    yaxis_title='Count',
    showlegend=True,
    legend_title='Gender',
    plot_bgcolor='white'
)
    graph7 = pio.to_html(fig7, full_html=False)
    return graph7

#fraud analysis
def fraud_method():
    fraud_categories = df['Fraud and Cybercrime Thematic Categories'].value_counts().reset_index()
    fraud_categories.columns = ['Category', 'Count']

    fig1 = px.bar(fraud_categories,
             x='Count',
             y='Category',
             orientation='h',
             title='Distribution of Fraud and Cybercrime Categories',
             template='plotly_white',
             color='Count',
             color_continuous_scale='Viridis')

    fig1.update_layout(
    title={
        'text': 'Distribution of Fraud and Cybercrime Categories',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Number of Cases',
    yaxis_title='',
    showlegend=False,
    plot_bgcolor='white',
    height=600  # Make it taller for better readability
)
    graph1 = pio.to_html(fig1, full_html=False)
    return graph1

#dollar loss
def dollar_loss_method():
    fraud_loss = df.groupby('Fraud and Cybercrime Thematic Categories').agg({
    'Dollar Loss Clean': 'sum',
    'Numro d\'identification / Number ID': 'count'  # Count of cases
}).reset_index()



# Calculate percentage of total loss
    total_loss = fraud_loss['Dollar Loss Clean'].sum()
    fraud_loss['Percentage'] = (fraud_loss['Dollar Loss Clean'] / total_loss * 100).round(2)

# Create labels with category, loss amount and case count
    fraud_loss['Label'] = fraud_loss.apply(
    lambda x: f"{x['Fraud and Cybercrime Thematic Categories']}<br>"
             f"${x['Dollar Loss Clean']:,.0f}<br>"
             f"({x['Percentage']}%)<br>"
             f"{x['Numro d\'identification / Number ID']:,} cases",
    axis=1
)

    fig2 = px.treemap(
    fraud_loss,
    path=[px.Constant('All Types'), 'Fraud and Cybercrime Thematic Categories'],
    values='Dollar Loss Clean',
    custom_data=['Label'],
    title='Dollar Loss Distribution by Fraud Type',
    template='plotly_white',
    color='Dollar Loss Clean',
    color_continuous_scale='Viridis'
)

    fig2.update_traces(
    hovertemplate='%{customdata[0]}<extra></extra>',
    textinfo='label+value'
)

    fig2.update_layout(
    title={
        'text': 'Dollar Loss Distribution by Fraud Type',
        'x': 0.5,
        'xanchor': 'center'
    },
    height=600
)
    graph2 = pio.to_html(fig2, full_html=False)
    return graph2


#co-occurence 
def co_occurence_method():
    cooccurrence = pd.crosstab(
    df['Fraud and Cybercrime Thematic Categories'],
    df['Complaint Type']
)

# Convert to percentage for better visualization
    cooccurrence_pct = cooccurrence.div(cooccurrence.sum(axis=1), axis=0) * 100

    fig3 = px.bar(
    cooccurrence_pct.reset_index().melt(
        id_vars='Fraud and Cybercrime Thematic Categories',
        var_name='Complaint Type',
        value_name='Percentage'
    ),
    x='Fraud and Cybercrime Thematic Categories',
    y='Percentage',
    color='Complaint Type',
    title='Co-occurrence of Fraud Types and Complaint Types',
    template='plotly_white',
    color_discrete_sequence=px.colors.qualitative.Set3
)

    fig3.update_layout(
    title={
        'text': 'Co-occurrence of Fraud Types and Complaint Types',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Fraud Category',
    yaxis_title='Percentage',
    barmode='stack',
    showlegend=True,
    legend_title='Complaint Type',
    plot_bgcolor='white',
    height=600,
    xaxis={'tickangle': 45}
)
    graph3 = pio.to_html(fig3, full_html=False)
    return graph3


#temporal

def temporal_method():
    monthly_cases = df.groupby('YearMonth').size().reset_index()
    monthly_cases.columns = ['YearMonth', 'Count']
    monthly_cases['YearMonth'] = monthly_cases['YearMonth'].astype(str)

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
    x=monthly_cases['YearMonth'],
    y=monthly_cases['Count'],
    mode='lines+markers',
    name='Number of Cases',
    line=dict(color='rgb(67, 147, 195)', width=2),
    marker=dict(size=6)
))

    fig1.update_layout(
    title={
        'text': 'Number of Fraud Cases Over Time',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Time Period',
    yaxis_title='Number of Cases',
    template='plotly_white',
    showlegend=False,
    plot_bgcolor='white',
    xaxis=dict(tickangle=45)
)
    graph1 = pio.to_html(fig1, full_html=False)
    return graph1


#total dollar loss
def total_dollar_loss_method():
    monthly_loss = df.groupby('YearMonth')['Dollar Loss Clean'].sum().reset_index()
    monthly_loss.columns = ['YearMonth', 'Total Dollar Loss']
    monthly_loss['YearMonth'] = monthly_loss['YearMonth'].astype(str)

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
    x=monthly_loss['YearMonth'],
    y=monthly_loss['Total Dollar Loss'],
    mode='lines+markers',
    name='Total Dollar Loss',
    line=dict(color='rgb(255, 127, 14)', width=2),
    marker=dict(size=6)
))

    fig2.update_layout(
    title={
        'text': 'Total Dollar Loss Over Time',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Time Period',
    yaxis_title='Total Dollar Loss ($)',
    template='plotly_white',
    showlegend=False,
    plot_bgcolor='white',
    xaxis=dict(tickangle=45)
)
    graph2 = pio.to_html(fig2, full_html=False)
    return graph2

#seasonal pattern
def seasonal_pattern_method():
    df['YearMonth'] = pd.to_datetime(df['YearMonth'], format='%Y%m')
    df['Month'] = df['YearMonth'].dt.month

    monthly_avg_loss = df.groupby('Month')['Dollar Loss Clean'].mean().reset_index()
    monthly_avg_loss.columns = ['Month', 'Average Dollar Loss']

    fig3 = px.line(monthly_avg_loss,
             x='Month',
             y='Average Dollar Loss',
             title='Average Dollar Loss by Month',
             template='plotly_white',
             markers=True)

    fig3.update_layout(
    title={
        'text': 'Average Dollar Loss by Month',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Month',
    yaxis_title='Average Dollar Loss ($)',
    showlegend=False,
    plot_bgcolor='white'
)
    graph3 = pio.to_html(fig3, full_html=False)
    return graph3




#overview
def overview():
    case_counts = df['Complaint Type'].value_counts().reset_index()
    case_counts.columns = ['Category', 'Count']

    fig1 = px.pie(case_counts, 
             values='Count',
             names='Category',
             title='Distribution of Cases by Type',
             color_discrete_sequence=px.colors.qualitative.Set3,
             hole=0.4)  # Makes it a donut chart

    fig1.update_layout(
    title_x=0.5,
    showlegend=True,
    annotations=[dict(text=f'Total Cases:<br>{case_counts["Count"].sum():,}', 
                     x=0.5, y=0.5, font_size=15, showarrow=False)]
)
    graph1 = pio.to_html(fig1, full_html=False)
    return graph1


#total loss
def total_loss_method():
    # Clean and format the Dollar Loss Clean column
    df['Dollar Loss Clean'] = df['Dollar Loss /pertes financires'].astype(str).str.replace('$', '')
    df['Dollar Loss Clean'] = df['Dollar Loss Clean'].str.replace(',', '')
    df['Dollar Loss Clean'] = pd.to_numeric(df['Dollar Loss Clean'], errors='coerce')

    # Group by complaint type and calculate total loss
    complaint_loss = df.groupby('Complaint Type')['Dollar Loss Clean'].sum().reset_index()
    complaint_loss = complaint_loss.sort_values('Dollar Loss Clean', ascending=False)

    fig2 = px.bar(
        complaint_loss,
        x='Complaint Type',
        y='Dollar Loss Clean',
        title='Total Dollar Loss by Complaint Type',
        color='Dollar Loss Clean',
        color_continuous_scale='Viridis'
    )

    fig2.update_layout(
        title_x=0.5,
        xaxis_title='Complaint Type',
        yaxis_title='Total Dollar Loss ($)',
        showlegend=False,
        plot_bgcolor='white',
        xaxis_tickangle=45,
        yaxis=dict(tickformat='$,.0f'),
        height=500
    )
    
    graph2 = pio.to_html(fig2, full_html=False)
    return graph2

#complain type
def complain_type_method():
    complaint_types = df['Complaint Type'].value_counts().reset_index()
    complaint_types.columns = ['Type', 'Count']

    fig3 = px.bar(complaint_types,
             x='Type',
             y='Count',
             title='Distribution of Complaint Types',
             template='plotly_white',
             color='Count',
             color_continuous_scale='Viridis')

    fig3.update_layout(
    title_x=0.5,
    xaxis_title='Complaint Type',
    yaxis_title='Number of Complaints',
    showlegend=False,
    plot_bgcolor='white'
)
    graph3 = pio.to_html(fig3, full_html=False)
    return graph3

#fraud intensity
def fraud_intensity_method():
     province_metrics = df.groupby('Province/State').agg({
    'Dollar Loss Clean': ['sum', 'count']
}).reset_index()

     province_metrics.columns = ['Province/State', 'Total Loss', 'Case Count']

# Create text for hover information
     province_metrics['Hover Text'] = province_metrics.apply(
    lambda x: f"Province/State: {x['Province/State']}<br>" +
             f"Total Loss: ${x['Total Loss']:,.2f}<br>" +
             f"Number of Cases: {x['Case Count']:,}",
    axis=1
)

     fig4 = px.treemap(
    province_metrics,
    path=[px.Constant('All Provinces/States'), 'Province/State'],
    values='Total Loss',
    color='Total Loss',
    custom_data=['Hover Text'],
    color_continuous_scale='RdYlBu_r',
    title='Fraud Intensity Across Provinces/States'
)

     fig4.update_traces(
    hovertemplate='%{customdata[0]}<extra></extra>',
    textinfo='label+value'
)

     fig4.update_layout(
    title_x=0.5,
    height=600
)

     graph4 = pio.to_html(fig4, full_html=False)
     return graph4

#geographic
def fraud_case_method():
    country_counts = df['Country'].str.strip().value_counts().reset_index()
    country_counts.columns = ['Country', 'Fraud Cases']

    fig1 = px.choropleth(
    country_counts,
    locations='Country',
    locationmode='country names',
    color='Fraud Cases',
    color_continuous_scale='Reds',
    title='Fraud Cases by Country'
)

    graph1 = pio.to_html(fig1, full_html=False)
    return graph1

#proviences
def provience_method():
    province_counts = df['Province/State'].dropna().str.strip().value_counts().nlargest(10).reset_index()
    province_counts.columns = ['Province/State', 'Fraud Cases']

    fig2 = px.bar(
    province_counts,
    x='Province/State',
    y='Fraud Cases',
    title='Top 10 Provinces/States with Highest Fraud Cases',
    color='Fraud Cases',
    color_continuous_scale='Blues'
)
    graph2 = pio.to_html(fig2, full_html=False)
    return graph2

#average dollar loss
def average_dollar_loss_method():
    df['Dollar Loss /pertes financires'] = df['Dollar Loss /pertes financires'].replace('[\$,]', '', regex=True)
    df['Dollar Loss /pertes financires'] = pd.to_numeric(df['Dollar Loss /pertes financires'], errors='coerce')

# Calculate average dollar loss per province
    avg_loss_by_province = df.groupby('Province/State')['Dollar Loss /pertes financires']\
                         .mean().dropna().sort_values(ascending=False).head(10).reset_index()
    avg_loss_by_province.columns = ['Province/State', 'Average Dollar Loss']

# Create bar chart
    fig = px.bar(
    avg_loss_by_province,
    x='Province/State',
    y='Average Dollar Loss',
    title='Top 10 Provinces/States by Average Dollar Loss',
    color='Average Dollar Loss',
    color_continuous_scale='Oranges'
)

#financial 
def distribution_method():
    dollar_loss_data = df[df['Dollar Loss Clean'] > 0]['Dollar Loss Clean']

    fig1 = go.Figure()

# Add histogram
    fig1.add_trace(go.Histogram(
    x=dollar_loss_data,
    name='Dollar Loss',
    nbinsx=50,
    marker_color='rgb(67, 147, 195)'
))

    fig1.update_layout(
    title={
        'text': 'Distribution of Dollar Losses',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Dollar Loss ($)',
    yaxis_title='Frequency',
    template='plotly_white',
    showlegend=False,
    plot_bgcolor='white',
    height=500,
    bargap=0.1
)
    graph1 = pio.to_html(fig1, full_html=False)
    return graph1

#average dollar loss
def average_dollar_loss_method():
    complaint_stats = df.groupby('Complaint Type').agg({
    'Dollar Loss Clean': ['mean', 'count', 'sum']
}).reset_index()

# Flatten column names
    complaint_stats.columns = ['Complaint Type', 'Average Loss', 'Count', 'Total Loss']

# Sort by average loss and filter for types with significant cases
    complaint_stats = complaint_stats[complaint_stats['Count'] >= 5]
    complaint_stats = complaint_stats.sort_values('Average Loss', ascending=True)

    fig2 = go.Figure()

# Add horizontal bar chart
    fig2.add_trace(go.Bar(
    x=complaint_stats['Average Loss'],
    y=complaint_stats['Complaint Type'],
    orientation='h',
    marker=dict(
        color=complaint_stats['Average Loss'],
        colorscale='Viridis'
    ),
    text=complaint_stats['Count'].apply(lambda x: f'n={x}'),
    textposition='inside'
))

    fig2.update_layout(
    title={
        'text': 'Average Dollar Loss by Complaint Type',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Average Dollar Loss ($)',
    yaxis_title='Complaint Type',
    template='plotly_white',
    showlegend=False,
    plot_bgcolor='white',
    height=600,
    xaxis=dict(tickformat='$,.0f')
)

    graph2 = pio.to_html(fig2, full_html=False)
    return graph2

# relationship
def relationship_method():
    fig3 = px.scatter(
    df[df['Dollar Loss Clean'] > 0],  # Filter out zero losses
    x='Number of Victims / Nombre de victimes',
    y='Dollar Loss Clean',
    color='Complaint Type',
    size='Dollar Loss Clean',
    size_max=30,
    opacity=0.7,
    title='Number of Victims vs. Dollar Loss',
    template='plotly_white',
    hover_data={
        'Number of Victims / Nombre de victimes': True,
        'Dollar Loss Clean': ':$,.2f',
        'Complaint Type': True
    }
)

    fig3.update_layout(
    title={
        'text': 'Relationship between Number of Victims and Dollar Loss',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Number of Victims',
    yaxis_title='Dollar Loss ($)',
    plot_bgcolor='white',
    height=600,
    legend_title='Complaint Type',
    legend=dict(
        yanchor='top',
        y=0.99,
        xanchor='left',
        x=1.02
    ),
    yaxis=dict(type='log', tickformat='$,.0f')
)

# Update marker appearance
    fig3.update_traces(
    marker=dict(line=dict(width=1, color='DarkSlateGrey'))
)
    graph3 = pio.to_html(fig3, full_html=False)
    return graph3



#Analysis pages connectivity
@app.route('/complain')
def complain():
    graph1 = complain_submission_method()
    graph2 = complain_solicitation_method()
    graph3 = complain_distribution_method()
    return render_template('complain.html', graph1=graph1 , graph2=graph2 , graph3=graph3)


@app.route('/demographic')
def demographic():
    graph1 = age_group_method()
    graph2 = case_gender_method()
    graph3 = average_dollar_loss_method()
    graph4 = distribution_lang_method()
    graph5 = gender_method()
    graph6 = victims_by_age_method()
    graph7 = gender_method()
    return render_template('demographic.html', graph1=graph1 , graph2=graph2 , graph3=graph3 , graph4=graph4 , graph5=graph5, graph6=graph6 , graph7=graph7)



@app.route('/fraud')
def fraud():
    # Process Dollar Loss Clean column
    df['Dollar Loss Clean'] = df['Dollar Loss /pertes financires'].astype(str).str.replace('$', '')
    df['Dollar Loss Clean'] = df['Dollar Loss Clean'].str.replace(',', '')
    df['Dollar Loss Clean'] = pd.to_numeric(df['Dollar Loss Clean'], errors='coerce')
    
    graph1 = fraud_method()
    graph2 = dollar_loss_method()
    graph3 = co_occurence_method()
    return render_template('fraud.html', graph1=graph1 , graph2=graph2, graph3=graph3)


@app.route('/temporal')
def temporal():
    graph1 = temporal_method()
    graph2 = total_dollar_loss_method()
    graph3 = seasonal_pattern_method()
    return render_template('temporal.html', graph1=graph1, graph2=graph2, graph3=graph3)


@app.route('/overview')
def overview_page():
    graph1 = overview()
    graph2 = total_loss_method()
    graph3 = complain_type_method()
    graph4 = fraud_intensity_method()
    return render_template('overview.html', graph1=graph1, graph2=graph2, graph3=graph3, graph4=graph4)

@app.route('/geographic')
def geographic():
    graph1 = fraud_case_method()
    graph2 = provience_method()
    graph3 = average_dollar_loss_method()
    return render_template('geographic.html', graph1=graph1, graph2=graph2, graph3=graph3)

@app.route('/financial')
def financial():
    graph1 = distribution_method()
    graph2 = average_dollar_loss_method()
    graph3 = relationship_method()
    return render_template('financial.html', graph1=graph1, graph2=graph2, graph3=graph3)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)