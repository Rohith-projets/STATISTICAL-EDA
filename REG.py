import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def show_lmplot(dataset):
    st.title("Seaborn LMPlot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Independent variable")
            y_var = st.selectbox("Y-axis variable", options=dataset.columns, index=1 if len(dataset.columns)>1 else 0, help="Dependent variable")       
            # Faceting parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns)>2 else 0, help="Variable for color grouping")
                palette = st.text_input("Color palette", value="viridis", help="Color mapping method")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of hue levels")
                markers = st.text_input("Markers", value="o", help="Marker styles for each hue level")
            else:
                hue_var, palette, hue_order, markers = None, None, None, "o"    
            use_col = st.checkbox("Use column faceting", False)
            if use_col:
                col_var = st.selectbox("Column variable", options=dataset.columns, help="Variable for column faceting")
                col_wrap = st.number_input("Columns per row", min_value=1, value=None, help="Wrap columns at this width")
                col_order = st.multiselect("Column order", options=sorted(dataset[col_var].unique()) if use_col and col_var in dataset.columns else [], help="Order of columns")
            else:
                col_var, col_wrap, col_order = None, None, None          
            use_row = st.checkbox("Use row faceting", False)
            if use_row and not use_col:
                row_var = st.selectbox("Row variable", options=dataset.columns, help="Variable for row faceting")
                row_order = st.multiselect("Row order", options=sorted(dataset[row_var].unique()) if use_row and row_var in dataset.columns else [], help="Order of rows")
            else:
                row_var, row_order = None, None           
            # Regression parameters
            st.subheader("Regression Parameters")
            fit_reg = st.checkbox("Fit regression", True, help="Estimate and plot regression model")
            if fit_reg:
                ci = st.slider("Confidence interval", 0, 100, 95, help="Size of confidence interval for regression")
                order = st.number_input("Polynomial order", min_value=1, value=1, help="Degree of polynomial regression")
                logistic = st.checkbox("Logistic regression", False, help="Fit logistic regression model")
                lowess = st.checkbox("LOWESS regression", False, help="Fit locally weighted regression")
                robust = st.checkbox("Robust regression", False, help="Fit robust to outliers regression")
                logx = st.checkbox("Log-x regression", False, help="Fit y~log(x) regression")
                truncate = st.checkbox("Truncate regression", True, help="Limit regression to data range")         
            # Scatterplot parameters
            st.subheader("Scatterplot Parameters")
            scatter = st.checkbox("Show scatterplot", True, help="Display underlying observations")
            if scatter:
                x_jitter = st.slider("X-axis jitter", 0.0, 1.0, 0.0, help="Random noise added to x values")
                y_jitter = st.slider("Y-axis jitter", 0.0, 1.0, 0.0, help="Random noise added to y values")
                x_estimator = st.selectbox("X-estimator", options=[None, "mean", "median"], index=0, help="Function to apply to x values")
                x_bins = st.number_input("X-bins", min_value=0, value=0, help="Number of bins for x variable")           
            # Display parameters
            st.subheader("Display Parameters")
            height = st.number_input("Facet height", min_value=1, value=5, help="Height (in inches) of each facet")
            aspect = st.number_input("Aspect ratio", min_value=0.1, value=1.0, help="Width/height ratio of each facet")
            legend = st.checkbox("Show legend", True, help="Display legend for hue levels")          
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')          
        with col2:
            if plot_button:
                st.subheader("Generated LMPlot")
                try:
                    g = sns.lmplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,col=col_var if use_col else None,row=row_var if use_row else None,palette=palette if use_hue else None,col_wrap=col_wrap,height=height,aspect=aspect,markers=markers,hue_order=hue_order if use_hue and hue_order else None,col_order=col_order if use_col and col_order else None,row_order=row_order if use_row and row_order else None,legend=legend,x_estimator=x_estimator if scatter and x_estimator else None,x_bins=x_bins if scatter and x_bins else None,scatter=scatter,fit_reg=fit_reg,ci=ci if fit_reg else None,order=order if fit_reg else None,logistic=logistic if fit_reg else False,lowess=lowess if fit_reg else False,robust=robust if fit_reg else False,logx=logx if fit_reg else False,truncate=truncate if fit_reg else True,x_jitter=x_jitter if scatter else None,y_jitter=y_jitter if scatter else None)
                    st.pyplot(g)
                    st.session_state['last_lmplot'] = g
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_lmplot' in st.session_state:
            st.pyplot(st.session_state['last_lmplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_regplot(dataset):
    st.title("Seaborn RegPlot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Independent variable")
            y_var = st.selectbox("Y-axis variable", options=dataset.columns, index=1 if len(dataset.columns)>1 else 0, help="Dependent variable") 
            # Scatterplot parameters
            st.subheader("Scatterplot Parameters")
            scatter = st.checkbox("Show scatterplot", True, help="Display underlying observations")
            if scatter:
                x_jitter = st.slider("X-axis jitter", 0.0, 1.0, 0.0, help="Random noise added to x values")
                y_jitter = st.slider("Y-axis jitter", 0.0, 1.0, 0.0, help="Random noise added to y values")
                x_estimator = st.selectbox("X-estimator", options=[None, "mean", "median"], index=0, help="Function to apply to x values")
                x_bins = st.number_input("X-bins", min_value=0, value=0, help="Number of bins for x variable")
                marker = st.text_input("Marker style", value="o", help="Marker symbol for scatter points")
                color = st.color_picker("Base color", value="#1f77b4", help="Color for plot elements")       
            # Regression parameters
            st.subheader("Regression Parameters")
            fit_reg = st.checkbox("Fit regression", True, help="Estimate and plot regression model")
            if fit_reg:
                ci = st.slider("Confidence interval", 0, 100, 95, help="Size of confidence interval for regression")
                n_boot = st.number_input("Bootstrap samples", min_value=1, value=1000, help="Number of bootstrap resamples")
                order = st.number_input("Polynomial order", min_value=1, value=1, help="Degree of polynomial regression")
                logistic = st.checkbox("Logistic regression", False, help="Fit logistic regression model")
                lowess = st.checkbox("LOWESS regression", False, help="Fit locally weighted regression")
                robust = st.checkbox("Robust regression", False, help="Fit robust to outliers regression")
                logx = st.checkbox("Log-x regression", False, help="Fit y~log(x) regression")
                truncate = st.checkbox("Truncate regression", True, help="Limit regression to data range")
                dropna = st.checkbox("Drop NA values", True, help="Remove missing values before fitting")    
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')         
        with col2:
            if plot_button:
                st.subheader("Generated RegPlot")
                try:
                    fig, ax = plt.subplots()
                    sns.regplot(data=dataset,x=x_var,y=y_var,x_estimator=x_estimator if scatter and x_estimator else None,x_bins=x_bins if scatter and x_bins else None,scatter=scatter,fit_reg=fit_reg,ci=ci if fit_reg else None,n_boot=n_boot if fit_reg else None,order=order if fit_reg else None,logistic=logistic if fit_reg else False,lowess=lowess if fit_reg else False,robust=robust if fit_reg else False,logx=logx if fit_reg else False,truncate=truncate if fit_reg else True,dropna=dropna,x_jitter=x_jitter if scatter else None,y_jitter=y_jitter if scatter else None,color=color if scatter else None,marker=marker if scatter else None,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_regplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}") 
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_regplot' in st.session_state:
            st.pyplot(st.session_state['last_regplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_residplot(dataset):
    st.title("Seaborn ResidPlot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Predictor variable")
            y_var = st.selectbox("Y-axis variable", options=dataset.columns, index=1 if len(dataset.columns)>1 else 0, help="Response variable")
            # Residual plot parameters
            st.subheader("Residual Plot Parameters")
            lowess = st.checkbox("LOWESS smoother", False, help="Fit a lowess smoother to residuals")
            order = st.number_input("Polynomial order", min_value=1, value=1, help="Order of polynomial regression for residuals")
            robust = st.checkbox("Robust regression", False, help="Use robust linear regression")
            dropna = st.checkbox("Drop NA values", True, help="Remove missing values before fitting")
            color = st.color_picker("Plot color", value="#1f77b4", help="Color for all plot elements")
            # Partial regression parameters
            st.subheader("Partial Regression Parameters")
            use_x_partial = st.checkbox("Use x-partial", False)
            if use_x_partial:
                x_partial = st.multiselect("X-partial variables", options=dataset.columns, help="Confounding variables to remove from x")
            else:
                x_partial = None  
            use_y_partial = st.checkbox("Use y-partial", False)
            if use_y_partial:
                y_partial = st.multiselect("Y-partial variables", options=dataset.columns, help="Confounding variables to remove from y")
            else:
                y_partial = None 
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')     
        with col2:
            if plot_button:
                st.subheader("Generated ResidPlot")
                try:
                    fig, ax = plt.subplots()
                    sns.residplot(data=dataset,x=x_var,y=y_var,x_partial=x_partial if use_x_partial else None,y_partial=y_partial if use_y_partial else None,lowess=lowess,order=order,robust=robust,dropna=dropna,color=color,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_residplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")    
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_residplot' in st.session_state:
            st.pyplot(st.session_state['last_residplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_heatmap(dataset):
    st.title("Seaborn Heatmap Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Data selection
            numeric_cols = dataset.select_dtypes(include=['number']).columns
            if len(numeric_cols) < 2:
                st.warning("Need at least 2 numeric columns for heatmap")
                return
            # Heatmap data parameters
            st.subheader("Data Parameters")
            use_corr = st.checkbox("Use correlation matrix", True, help="Plot correlation matrix of numeric columns")
            if not use_corr:
                x_var = st.selectbox("X-axis variable", options=numeric_cols, index=0)
                y_var = st.selectbox("Y-axis variable", options=numeric_cols, index=1)
                data = dataset.pivot_table(index=y_var, columns=x_var, aggfunc='size', fill_value=0)
            else:
                data = dataset[numeric_cols].corr()
            # Color parameters
            st.subheader("Color Parameters")
            cmap = st.selectbox("Colormap", options=["viridis", "coolwarm", "Spectral", "YlOrRd", "Blues"], index=1)
            center = st.number_input("Center value", value=None, help="Value to center colormap")
            robust = st.checkbox("Robust scaling", False, help="Use robust quantiles for color range")
            vmin = st.number_input("Minimum value", value=None, help="Minimum value for colormap")
            vmax = st.number_input("Maximum value", value=None, help="Maximum value for colormap")
            # Annotation parameters
            st.subheader("Annotation Parameters")
            annot = st.checkbox("Show values", False, help="Display values in each cell")
            if annot:
                fmt = st.text_input("Value format", value=".2g", help="String formatting for annotations")
                annot_size = st.slider("Annotation size", 6, 20, 10)
                annot_kws = {"size": annot_size}
            else:
                fmt = ".2g"
                annot_kws = None   
            # Appearance parameters
            st.subheader("Appearance Parameters")
            linewidths = st.slider("Grid line width", 0.0, 2.0, 0.5)
            linecolor = st.color_picker("Grid line color", value="#ffffff")
            square = st.checkbox("Square cells", True, help="Make cells square-shaped")
            cbar = st.checkbox("Show colorbar", True, help="Display color scale")     
            # Label parameters
            st.subheader("Label Parameters")
            xticklabels = st.checkbox("Show x-tick labels", True)
            yticklabels = st.checkbox("Show y-tick labels", True)    
            plot_button = st.button("Generate Heatmap", use_container_width=True, type='primary')       
        with col2:
            if plot_button:
                st.subheader("Generated Heatmap")
                try:
                    fig, ax = plt.subplots(figsize=(10, 8))
                    sns.heatmap(data=data,vmin=vmin,vmax=vmax,cmap=cmap,center=center,robust=robust,annot=annot,fmt=fmt,annot_kws=annot_kws,linewidths=linewidths,linecolor=linecolor,cbar=cbar,square=square,xticklabels=xticklabels,yticklabels=yticklabels,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_heatmap'] = fig
                except Exception as e:
                    st.error(f"Error generating heatmap: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Heatmap")
        if 'last_heatmap' in st.session_state:
            st.pyplot(st.session_state['last_heatmap'])
        else:
            st.info("No heatmap generated yet. Please create one in the 'Implement Plots' tab.")
def show_clustermap(dataset):
    st.title("Seaborn ClusterMap Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Data selection
            numeric_cols = dataset.select_dtypes(include=['number']).columns
            if len(numeric_cols) < 2:
                st.warning("Need at least 2 numeric columns for clustermap")
                return
            # Data parameters
            st.subheader("Data Parameters")
            use_corr = st.checkbox("Use correlation matrix", True, help="Plot correlation matrix of numeric columns")
            if not use_corr:
                data = dataset[numeric_cols]
            else:
                data = dataset[numeric_cols].corr()
            # Clustering parameters
            st.subheader("Clustering Parameters")
            row_cluster = st.checkbox("Cluster rows", True)
            col_cluster = st.checkbox("Cluster columns", True)
            method = st.selectbox("Linkage method", ["average", "single", "complete", "ward"], index=0)
            metric = st.selectbox("Distance metric", ["euclidean", "correlation", "cityblock", "cosine"], index=0) 
            # Normalization parameters
            st.subheader("Normalization Parameters")
            z_score = st.selectbox("Z-score normalization", [None, 0, 1], index=0, help="0 for rows, 1 for columns")
            standard_scale = st.selectbox("Standard scaling", [None, 0, 1], index=0,help="0 for rows, 1 for columns")
            # Color parameters
            st.subheader("Color Parameters")
            cmap = st.selectbox("Colormap", ["viridis", "coolwarm", "Spectral", "YlOrRd", "Blues"], index=1)
            center = st.number_input("Center value", value=None, help="Value to center colormap")
            robust = st.checkbox("Robust scaling", False, help="Use robust quantiles for color range")
            # Annotation parameters
            st.subheader("Annotation Parameters")
            annot = st.checkbox("Show values", False, help="Display values in each cell")
            if annot:
                fmt = st.text_input("Value format", value=".2g", help="String formatting for annotations")
                annot_size = st.slider("Annotation size", 6, 20, 10)
                annot_kws = {"size": annot_size}
            else:
                fmt = ".2g"
                annot_kws = None     
            # Appearance parameters
            st.subheader("Appearance Parameters")
            figsize = st.slider("Figure size", 5, 20, 10)
            linewidths = st.slider("Grid line width", 0.0, 2.0, 0.5)
            linecolor = st.color_picker("Grid line color", value="#ffffff")
            cbar = st.checkbox("Show colorbar", True, help="Display color scale")          
            plot_button = st.button("Generate ClusterMap", use_container_width=True, type='primary')           
        with col2:
            if plot_button:
                st.subheader("Generated ClusterMap")
                try:
                    g = sns.clustermap(data=data,method=method,metric=metric,z_score=z_score if z_score is not None else None,standard_scale=standard_scale if standard_scale is not None else None,figsize=(figsize, figsize),row_cluster=row_cluster,col_cluster=col_cluster,cmap=cmap,center=center,robust=robust,annot=annot,fmt=fmt,annot_kws=annot_kws,linewidths=linewidths,linecolor=linecolor,cbar=cbar)
                    st.pyplot(g.fig)
                    st.session_state['last_clustermap'] = g.fig
                except Exception as e:
                    st.error(f"Error generating clustermap: {str(e)}")
    with tab2:
        st.subheader("Previously Generated ClusterMap")
        if 'last_clustermap' in st.session_state:
            st.pyplot(st.session_state['last_clustermap'])
        else:
            st.info("No clustermap generated yet. Please create one in the 'Implement Plots' tab.")
