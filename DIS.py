import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def show_displot(dataset):
    st.title("Seaborn Displot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Variable for the x-axis position")
            y_var = st.selectbox("Y-axis variable", options=[None] + list(dataset.columns), index=0, help="Variable for the y-axis position (optional)")
            kind = st.radio("Plot kind", options=["hist", "kde", "ecdf"], index=0, help="Type of distribution plot")
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable that determines color of plot elements")
                palette = st.text_input("Color palette", value="viridis", help="Method for choosing colors")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of categorical levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var, palette, hue_order, hue_norm = None, None, None, None
            # Faceting parameters
            use_facets = st.checkbox("Use faceting", False)
            if use_facets:
                row_var = st.selectbox("Row faceting variable", options=[None] + list(dataset.columns), index=0, help="Variable for row facets")
                col_var = st.selectbox("Column faceting variable", options=[None] + list(dataset.columns), index=0, help="Variable for column facets")
                col_wrap = st.number_input("Columns per row", min_value=1, value=3, help="Wrap column facets") if col_var else None
                row_order = st.multiselect("Row order", options=sorted(dataset[row_var].unique()), help="Row facet order") if row_var else None
                col_order = st.multiselect("Column order", options=sorted(dataset[col_var].unique()), help="Column facet order") if col_var else None
            else:
                row_var, col_var, col_wrap, row_order, col_order = None, None, None, None, None
            # Additional parameters
            rug = st.checkbox("Show rug plot", False, help="Show marginal ticks for each observation")
            log_scale = st.checkbox("Log scale", False, help="Use logarithmic axis scaling")
            height = st.number_input("Facet height (inches)", min_value=1.0, value=5.0, step=0.5, help="Height of each facet")
            aspect = st.number_input("Aspect ratio", min_value=0.1, value=1.0, step=0.1, help="Width = aspect * height")
            legend = st.checkbox("Show legend", True, help="Display legend for semantic variables")
            color = st.color_picker("Base color", value="#1f77b4", help="Color when hue mapping is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
        with col2:
            if plot_button:
                st.subheader("Generated Displot")
                try:
                    g = sns.displot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,row=row_var if use_facets and row_var else None,col=col_var if use_facets and col_var else None,col_wrap=col_wrap if use_facets and col_var and col_wrap else None,kind=kind,rug=rug,log_scale=log_scale,legend=legend,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,color=color,row_order=row_order if use_facets and row_var and row_order else None,col_order=col_order if use_facets and col_var and col_order else None,height=height,aspect=aspect)
                    st.pyplot(g.fig)
                    st.session_state['last_displot'] = g.fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_displot' in st.session_state:
            st.pyplot(st.session_state['last_displot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_histplot(dataset):
    st.title("Seaborn Histplot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Variable for the x-axis position")
            y_var = st.selectbox("Y-axis variable", options=[None] + list(dataset.columns), index=0, help="Variable for the y-axis position (optional)")
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable that determines color of plot elements")
                palette = st.text_input("Color palette", value="viridis", help="Method for choosing colors")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of categorical levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var, palette, hue_order, hue_norm = None, None, None, None
            # Histogram parameters
            stat = st.selectbox("Statistic", options=["count", "frequency", "probability", "percent", "density"], index=0, help="Aggregate statistic to compute in each bin")
            bins = st.text_input("Bins", value="auto", help="Number of bins or binning method")
            binwidth = st.number_input("Bin width", min_value=0.0, value=0.0, help="Width of each bin (0 for automatic)")
            discrete = st.checkbox("Discrete bins", False, help="Center bins on integer values")
            cumulative = st.checkbox("Cumulative", False, help="Show cumulative counts")
            common_bins = st.checkbox("Common bins", True, help="Use same bins across groups")
            common_norm = st.checkbox("Common norm", True, help="Normalize across all groups")
            multiple = st.selectbox("Multiple elements", options=["layer", "dodge", "stack", "fill"], index=0, help="How to display multiple groups")
            element = st.selectbox("Element type", options=["bars", "step", "poly"], index=0, help="Visual representation")
            fill = st.checkbox("Fill", True, help="Fill space under histogram")
            shrink = st.slider("Shrink", 0.1, 1.0, 1.0, help="Scale width of bars")
            # KDE parameters
            kde = st.checkbox("Show KDE", False, help="Add kernel density estimate")
            # Additional parameters
            log_scale = st.checkbox("Log scale", False, help="Use logarithmic axis scaling")
            legend = st.checkbox("Show legend", True, help="Display legend for semantic variables")
            color = st.color_picker("Base color", value="#1f77b4", help="Color when hue mapping is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
        with col2:
            if plot_button:
                st.subheader("Generated Histplot")
                try:
                    fig, ax = plt.subplots()
                    sns.histplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,stat=stat,bins=None if bins == "auto" else (int(bins) if bins.isdigit() else bins),binwidth=binwidth if binwidth > 0 else None,discrete=discrete,cumulative=cumulative,common_bins=common_bins,common_norm=common_norm,multiple=multiple,element=element,fill=fill,shrink=shrink,kde=kde,log_scale=log_scale,legend=legend,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,color=color,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_histplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_histplot' in st.session_state:
            st.pyplot(st.session_state['last_histplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_kdeplot(dataset):
    st.title("Seaborn KDE Plot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Variable for the x-axis position")
            y_var = st.selectbox("Y-axis variable", options=[None] + list(dataset.columns), index=0, help="Variable for the y-axis position (optional)")
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable that determines color of plot elements")
                palette = st.text_input("Color palette", value="viridis", help="Method for choosing colors")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of categorical levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var, palette, hue_order, hue_norm = None, None, None, None
            # KDE parameters
            fill = st.checkbox("Fill", False, help="Fill under the KDE curve")
            multiple = st.selectbox("Multiple elements", options=["layer", "stack", "fill"], index=0, help="How to display multiple groups")
            common_norm = st.checkbox("Common norm", True, help="Normalize across all groups")
            common_grid = st.checkbox("Common grid", False, help="Use same evaluation grid for each KDE")
            cumulative = st.checkbox("Cumulative", False, help="Show cumulative distribution")
            bw_method = st.selectbox("Bandwidth method", options=["scott", "silverman"], index=0, help="Smoothing bandwidth method")
            bw_adjust = st.slider("Bandwidth adjust", 0.1, 5.0, 1.0, help="Adjust smoothing bandwidth")
            levels = st.number_input("Contour levels", min_value=1, value=10, help="Number of contour levels (bivariate only)")
            gridsize = st.number_input("Grid size", min_value=10, value=200, help="Points on evaluation grid")
            cut = st.number_input("Cut", min_value=0, value=3, help="Extend evaluation grid beyond data limits")
            # Additional parameters
            log_scale = st.checkbox("Log scale", False, help="Use logarithmic axis scaling")
            legend = st.checkbox("Show legend", True, help="Display legend for semantic variables")
            color = st.color_picker("Base color", value="#1f77b4", help="Color when hue mapping is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
        with col2:
            if plot_button:
                st.subheader("Generated KDE Plot")
                try:
                    fig, ax = plt.subplots()
                    sns.kdeplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,fill=fill,multiple=multiple,common_norm=common_norm,common_grid=common_grid,cumulative=cumulative,bw_method=bw_method,bw_adjust=bw_adjust,levels=levels,gridsize=gridsize,cut=cut,log_scale=log_scale,legend=legend,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,color=color,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_kdeplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_kdeplot' in st.session_state:
            st.pyplot(st.session_state['last_kdeplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_ecdfplot(dataset):
    st.title("Seaborn ECDF Plot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Variable for the x-axis position")
            y_var = st.selectbox("Y-axis variable", options=[None] + list(dataset.columns), index=0, help="Variable for the y-axis position (optional)")
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable that determines color of plot elements")
                palette = st.text_input("Color palette", value="viridis", help="Method for choosing colors")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of categorical levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var, palette, hue_order, hue_norm = None, None, None, None
            # ECDF parameters
            stat = st.selectbox("Statistic", options=["proportion", "percent", "count"], index=0, help="Distribution statistic to compute")
            complementary = st.checkbox("Complementary", False, help="Plot 1 - CDF instead of CDF")
            # Additional parameters
            log_scale = st.checkbox("Log scale", False, help="Use logarithmic axis scaling")
            legend = st.checkbox("Show legend", True, help="Display legend for semantic variables")
            color = st.color_picker("Base color", value="#1f77b4", help="Color when hue mapping is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
        with col2:
            if plot_button:
                st.subheader("Generated ECDF Plot")
                try:
                    fig, ax = plt.subplots()
                    sns.ecdfplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,stat=stat,complementary=complementary,log_scale=log_scale,legend=legend,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,color=color,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_ecdfplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_ecdfplot' in st.session_state:
            st.pyplot(st.session_state['last_ecdfplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_rugplot(dataset):
    st.title("Seaborn Rugplot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Variable for the x-axis position")
            y_var = st.selectbox("Y-axis variable", options=[None] + list(dataset.columns), index=0, help="Variable for the y-axis position (optional)")
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable that determines color of plot elements")
                palette = st.text_input("Color palette", value="viridis", help="Method for choosing colors")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of categorical levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var, palette, hue_order, hue_norm = None, None, None, None
            # Rugplot parameters
            height = st.number_input("Height", min_value=0.001, max_value=1.0, value=0.025, step=0.005, help="Proportion of axes covered by each rug element")
            expand_margins = st.checkbox("Expand margins", True, help="Increase axes margins to avoid overlap")
            legend = st.checkbox("Show legend", True, help="Display legend for semantic variables")
            color = st.color_picker("Base color", value="#1f77b4", help="Color when hue mapping is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
        with col2:
            if plot_button:
                st.subheader("Generated Rugplot")
                try:
                    fig, ax = plt.subplots()
                    sns.rugplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,height=height,expand_margins=expand_margins,legend=legend,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,color=color,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_rugplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_rugplot' in st.session_state:
            st.pyplot(st.session_state['last_rugplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
