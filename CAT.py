import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def show_catplot(dataset):
    st.title("Seaborn Catplot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Categorical variable for x-axis")
            y_var = st.selectbox("Y-axis variable", options=[None] + list(dataset.columns), index=0, help="Numerical variable for y-axis")
            kind = st.selectbox("Plot kind", options=["strip", "swarm", "box", "violin", "boxen", "point", "bar", "count"], index=0, help="Type of categorical plot")
            
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable for color grouping")
                palette = st.text_input("Color palette", value="viridis", help="Color mapping method")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of hue levels")
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
            else:
                row_var, col_var, col_wrap = None, None, None
                
            # Estimation parameters
            if kind in ["point", "bar"]:
                estimator = st.selectbox("Estimator", options=["mean", "median", "sum", "min", "max", "count"], index=0, help="Statistical function for estimation")
                errorbar = st.selectbox("Error bar method", options=["ci", "pi", "se", "sd", None], index=0, help="Method for error bars")
                if errorbar in ["ci", "pi"]:
                    errorbar_level = st.slider("Confidence level", 1, 99, 95)
                    errorbar = (errorbar, errorbar_level)
                n_boot = st.number_input("Bootstrap samples", min_value=1, value=1000, help="Number of bootstrap samples")
            else:
                estimator, errorbar, n_boot = None, None, None
                
            # Additional parameters
            height = st.number_input("Facet height", min_value=1.0, value=5.0, step=0.5, help="Height in inches")
            aspect = st.number_input("Aspect ratio", min_value=0.1, value=1.0, step=0.1, help="Width = aspect * height")
            color = st.color_picker("Base color", value="#1f77b4", help="Color when hue is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
            
        with col2:
            if plot_button:
                st.subheader("Generated Catplot")
                try:
                    g = sns.catplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,row=row_var if use_facets and row_var else None,col=col_var if use_facets and col_var else None,col_wrap=col_wrap if use_facets and col_var and col_wrap else None,kind=kind,estimator=estimator if kind in ["point", "bar"] else None,errorbar=errorbar if kind in ["point", "bar"] else None,n_boot=n_boot if kind in ["point", "bar"] else None,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,height=height,aspect=aspect,color=color)
                    st.pyplot(g.fig)
                    st.session_state['last_catplot'] = g.fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
                    
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_catplot' in st.session_state:
            st.pyplot(st.session_state['last_catplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
          
def show_stripplot(dataset):
    st.title("Seaborn Stripplot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Categorical variable for x-axis")
            y_var = st.selectbox("Y-axis variable", options=dataset.columns, index=1 if len(dataset.columns) > 1 else 0, help="Numerical variable for y-axis")
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable for color grouping")
                palette = st.text_input("Color palette", value="viridis", help="Color mapping method")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of hue levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var, palette, hue_order, hue_norm = None, None, None, None
            # Strip plot parameters
            jitter = st.slider("Jitter amount", 0.0, 1.0, 0.4, help="Amount of jitter to reduce overplotting")
            dodge = st.checkbox("Dodge hue levels", False, help="Separate strips for different hue levels") if use_hue else False
            size = st.slider("Marker size", 1, 20, 5, help="Radius of markers in points")
            linewidth = st.slider("Edge line width", 0, 5, 0, help="Width of lines around points")
            edgecolor = st.color_picker("Edge color", value="gray", help="Color of lines around points")
            # Additional parameters
            log_scale = st.checkbox("Log scale", False, help="Use logarithmic axis scaling")
            color = st.color_picker("Base color", value="#1f77b4", help="Color when hue is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
        with col2:
            if plot_button:
                st.subheader("Generated Stripplot")
                try:
                    fig, ax = plt.subplots()
                    sns.stripplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,jitter=jitter,dodge=dodge,size=size,linewidth=linewidth,edgecolor=edgecolor,log_scale=log_scale,color=color,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_stripplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_stripplot' in st.session_state:
            st.pyplot(st.session_state['last_stripplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_swarmplot(dataset):
    st.title("Seaborn Swarmplot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Categorical variable for x-axis")
            y_var = st.selectbox("Y-axis variable", options=dataset.columns, index=1 if len(dataset.columns) > 1 else 0, help="Numerical variable for y-axis")
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable for color grouping")
                palette = st.text_input("Color palette", value="viridis", help="Color mapping method")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of hue levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var, palette, hue_order, hue_norm = None, None, None, None
            # Swarm plot parameters
            dodge = st.checkbox("Dodge hue levels", False, help="Separate swarms for different hue levels") if use_hue else False
            size = st.slider("Marker size", 1, 20, 5, help="Radius of markers in points")
            linewidth = st.slider("Edge line width", 0, 5, 0, help="Width of lines around points")
            edgecolor = st.color_picker("Edge color", value="#00FFAA", help="Color of lines around points")
            # Additional parameters
            log_scale = st.checkbox("Log scale", False, help="Use logarithmic axis scaling")
            color = st.color_picker("Base color", value="#1f77b4", help="Color when hue is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
        with col2:
            if plot_button:
                st.subheader("Generated Swarmplot")
                try:
                    fig, ax = plt.subplots()
                    sns.swarmplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,dodge=dodge,size=size,linewidth=linewidth,edgecolor=edgecolor,log_scale=log_scale,color=color,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_swarmplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_swarmplot' in st.session_state:
            st.pyplot(st.session_state['last_swarmplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_boxplot(dataset):
    st.title("Seaborn Boxplot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Categorical variable for x-axis")
            y_var = st.selectbox("Y-axis variable", options=dataset.columns, index=1 if len(dataset.columns) > 1 else 0, help="Numerical variable for y-axis")
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable for color grouping")
                palette = st.text_input("Color palette", value="viridis", help="Color mapping method")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of hue levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var, palette, hue_order, hue_norm = None, None, None, None
            # Boxplot parameters
            saturation = st.slider("Saturation", 0.0, 1.0, 0.75, help="Fill color saturation")
            fill = st.checkbox("Fill boxes", True, help="Use solid fill for boxes")
            dodge = st.selectbox("Dodge hue levels", options=["auto", True, False], index=0, help="Separate boxes for different hue levels") if use_hue else False
            width = st.slider("Width", 0.1, 1.0, 0.8, help="Width of each box")
            gap = st.slider("Gap", 0.0, 1.0, 0.0, help="Gap between dodged elements")
            whis = st.slider("Whisker length", 0.0, 5.0, 1.5, help="IQR multiplier for whiskers")
            linewidth = st.slider("Line width", 0.0, 5.0, None, help="Width of box outlines")
            fliersize = st.slider("Outlier size", 0.0, 10.0, None, help="Size of outlier markers")
            # Additional parameters
            log_scale = st.checkbox("Log scale", False, help="Use logarithmic axis scaling")
            color = st.color_picker("Base color", value="#1f77b4", help="Color when hue is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
        with col2:
            if plot_button:
                st.subheader("Generated Boxplot")
                try:
                    fig, ax = plt.subplots()
                    sns.boxplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,saturation=saturation,fill=fill,dodge=dodge if use_hue else None,width=width,gap=gap,whis=whis,linewidth=linewidth,fliersize=fliersize,log_scale=log_scale,color=color,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_boxplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_boxplot' in st.session_state:
            st.pyplot(st.session_state['last_boxplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_violinplot(dataset):
    st.title("Seaborn Violinplot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Categorical variable for x-axis")
            y_var = st.selectbox("Y-axis variable", options=dataset.columns, index=1 if len(dataset.columns) > 1 else 0, help="Numerical variable for y-axis")
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable for color grouping")
                palette = st.text_input("Color palette", value="viridis", help="Color mapping method")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of hue levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var, palette, hue_order, hue_norm = None, None, None, None
            # Violinplot parameters
            saturation = st.slider("Saturation", 0.0, 1.0, 0.75, help="Fill color saturation")
            fill = st.checkbox("Fill violins", True, help="Use solid fill for violins")
            inner = st.selectbox("Inner plot", ["box", "quart", "point", "stick", None], index=0, help="Representation of data in violin interior")
            split = st.checkbox("Split violins", False, help="Show un-mirrored distributions") if use_hue else False
            width = st.slider("Width", 0.1, 1.0, 0.8, help="Width of each violin")
            dodge = st.selectbox("Dodge hue levels", options=["auto", True, False], index=0, help="Separate violins for different hue levels") if use_hue else False
            gap = st.slider("Gap", 0.0, 1.0, 0.0, help="Gap between dodged elements")
            linewidth = st.slider("Line width", 0.0, 5.0, None, help="Width of violin outlines")
            cut = st.slider("Cut", 0.0, 5.0, 2.0, help="Extend density past extreme datapoints")
            gridsize = st.number_input("Grid size", min_value=10, value=100, help="Points in KDE evaluation grid")
            bw_method = st.selectbox("Bandwidth method", options=["scott", "silverman"], index=0, help="Method for KDE bandwidth")
            bw_adjust = st.slider("Bandwidth adjust", 0.1, 5.0, 1.0, help="Adjust KDE smoothing")
            density_norm = st.selectbox("Density norm", ["area", "count", "width"], index=0, help="Method to normalize violin widths")
            common_norm = st.checkbox("Common norm", False, help="Normalize density across all violins")
            # Additional parameters
            log_scale = st.checkbox("Log scale", False, help="Use logarithmic axis scaling")
            color = st.color_picker("Base color", value="#1f77b4", help="Color when hue is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
        with col2:
            if plot_button:
                st.subheader("Generated Violinplot")
                try:
                    fig, ax = plt.subplots()
                    sns.violinplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,saturation=saturation,fill=fill,inner=inner,split=split,width=width,dodge=dodge if use_hue else None,gap=gap,linewidth=linewidth,cut=cut,gridsize=gridsize,bw_method=bw_method,bw_adjust=bw_adjust,density_norm=density_norm,common_norm=common_norm,log_scale=log_scale,color=color,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_violinplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_violinplot' in st.session_state:
            st.pyplot(st.session_state['last_violinplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_pointplot(dataset):
    st.title("Seaborn Pointplot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Categorical variable for x-axis")
            y_var = st.selectbox("Y-axis variable", options=dataset.columns, index=1 if len(dataset.columns) > 1 else 0, help="Numerical variable for y-axis")
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable for color grouping")
                palette = st.text_input("Color palette", value="viridis", help="Color mapping method")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of hue levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var, palette, hue_order, hue_norm = None, None, None, None
            # Pointplot parameters
            estimator = st.selectbox("Estimator", options=["mean", "median", "sum", "min", "max", "count"], index=0, help="Statistical function for estimation")
            errorbar = st.selectbox("Error bar method", options=["ci", "pi", "se", "sd", None], index=0, help="Method for error bars")
            if errorbar in ["ci", "pi"]:
                errorbar_level = st.slider("Confidence level", 1, 99, 95)
                errorbar = (errorbar, errorbar_level)
            n_boot = st.number_input("Bootstrap samples", min_value=1, value=1000, help="Number of bootstrap samples")
            dodge = st.checkbox("Dodge hue levels", False, help="Separate points for different hue levels") if use_hue else False
            capsize = st.slider("Error bar cap size", 0.0, 0.5, 0.0, help="Width of caps on error bars")
            # Additional parameters
            log_scale = st.checkbox("Log scale", False, help="Use logarithmic axis scaling")
            color = st.color_picker("Base color", value="#1f77b4", help="Color when hue is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
        with col2:
            if plot_button:
                st.subheader("Generated Pointplot")
                try:
                    fig, ax = plt.subplots()
                    sns.pointplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,estimator=estimator,errorbar=errorbar,n_boot=n_boot,dodge=dodge if use_hue else None,capsize=capsize,log_scale=log_scale,color=color,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_pointplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_pointplot' in st.session_state:
            st.pyplot(st.session_state['last_pointplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_boxenplot(dataset):
    st.title("Seaborn Boxenplot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Categorical variable for x-axis (or numeric if native_scale=True)")
            y_var = st.selectbox("Y-axis variable", options=dataset.columns, index=1 if len(dataset.columns) > 1 else 0, help="Numerical variable for y-axis")
            # Orientation
            orient = st.selectbox("Orientation", options=["v", "h", "x", "y"], index=0,help="Plot orientation (v: vertical, h: horizontal)")
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0,help="Variable for color grouping")
                palette = st.text_input("Color palette", value="viridis", help="Color mapping method (name, list, or dict)")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of hue levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Normalization range for numeric hue (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
                dodge = st.selectbox("Dodge", options=["auto", True, False], index=0,help="Separate elements for hue levels ('auto' determines automatically)")
                saturation = st.slider("Color saturation", 0.0, 1.0, 0.75,help="Saturation level for fill colors")
            else:
                hue_var, palette, hue_order, hue_norm, dodge, saturation = None, None, None, None, None, 0.75        
            # Order parameters
            order = st.multiselect("Category order", options=sorted(dataset[x_var].unique()) if x_var in dataset.columns else [],help="Order of categories on x-axis")        
            # Boxenplot specific parameters
            st.subheader("Boxenplot Specifics")
            fill = st.checkbox("Fill boxes", True, help="Use solid patches (False for line art)")
            width = st.slider("Element width", 0.1, 2.0, 0.8,help="Width allotted to each element")
            gap = st.slider("Gap between elements", 0.0, 1.0, 0.0,help="Shrink factor to add gaps between dodged elements")
            linewidth = st.slider("Line width", 0.5, 5.0, 1.5,help="Width of lines framing plot elements")
            linecolor = st.color_picker("Line color", value="#333333",help="Color for line elements when fill=True")
            # Width method and depth parameters
            width_method = st.selectbox("Width method", options=["exponential", "linear", "area"], index=0,help="Method for width of letter value boxes")
            k_depth = st.selectbox("Depth method", options=["tukey", "proportion", "trustworthy", "full"], index=0,help="Number of levels to draw in each tail")
            # Outlier parameters
            showfliers = st.checkbox("Show outliers", True,help="Display outlier points")
            outlier_prop = st.slider("Outlier proportion", 0.001, 0.1, 0.007,help="Expected proportion of outliers (for k_depth='proportion')")
            trust_alpha = st.slider("Trust alpha", 0.01, 0.5, 0.05,help="Confidence threshold (for k_depth='trustworthy')")
            # Scale parameters
            log_scale = st.checkbox("Log scale", False,help="Use logarithmic axis scaling")
            native_scale = st.checkbox("Native scale", False,help="Maintain original scaling of numeric/datetime categories")
            # Color parameters
            color = st.color_picker("Base color", value="#1f77b4",help="Color when hue is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
        with col2:
            if plot_button:
                st.subheader("Generated Boxenplot")
                try:
                    fig, ax = plt.subplots()
                    sns.boxenplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,order=order if order else None,hue_order=hue_order if use_hue and hue_order else None,orient=orient,color=color,palette=palette if use_hue else None,saturation=saturation if use_hue else None,fill=fill,dodge=dodge if use_hue else None,width=width,gap=gap,linewidth=linewidth,linecolor=linecolor,width_method=width_method,k_depth=k_depth,outlier_prop=outlier_prop,trust_alpha=trust_alpha,showfliers=showfliers,hue_norm=hue_norm if use_hue and hue_norm else None,log_scale=log_scale,native_scale=native_scale,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_boxenplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")    
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_boxenplot' in st.session_state:
            st.pyplot(st.session_state['last_boxenplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
def show_countplot(dataset):
    st.title("Seaborn Countplot Customizer")
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Categorical variable for x-axis")
            y_var = st.selectbox("Y-axis variable", options=dataset.columns, index=1 if len(dataset.columns)>1 else 0, help="Categorical variable for y-axis (leave empty for count)")
            orient = st.selectbox("Orientation", options=["v","h","x","y"], index=0, help="Plot orientation (v: vertical, h: horizontal)")
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns)>2 else 0, help="Variable for color grouping")
                palette = st.text_input("Color palette", value="viridis", help="Color mapping method")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Order of hue levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
                dodge = st.selectbox("Dodge", options=["auto",True,False], index=0, help="Separate bars for hue levels")
            else:
                hue_var, palette, hue_order, hue_norm, dodge = None, None, None, None, None
            order = st.multiselect("Category order", options=sorted(dataset[x_var].unique()) if x_var in dataset.columns else [], help="Order of categories")
            stat = st.selectbox("Statistic", options=["count","percent","proportion","probability"], index=0, help="Statistic to compute")
            width = st.slider("Bar width", 0.1, 1.0, 0.8, help="Width of each bar")
            saturation = st.slider("Color saturation", 0.0, 1.0, 0.75, help="Saturation level for colors")
            fill = st.checkbox("Fill bars", True, help="Use solid bars")
            log_scale = st.checkbox("Log scale", False, help="Use logarithmic axis scaling")
            native_scale = st.checkbox("Native scale", False, help="Maintain original scaling of categories")
            color = st.color_picker("Base color", value="#1f77b4", help="Color when hue is not used")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
        with col2:
            if plot_button:
                st.subheader("Generated Countplot")
                try:
                    fig, ax = plt.subplots()
                    sns.countplot(data=dataset,x=x_var if orient in ["v","x"] else None,y=y_var if orient in ["h","y"] else None,hue=hue_var if use_hue else None,order=order if order else None,hue_order=hue_order if use_hue and hue_order else None,orient=orient,color=color,palette=palette if use_hue else None,saturation=saturation,fill=fill,hue_norm=hue_norm if use_hue and hue_norm else None,stat=stat,width=width,dodge=dodge if use_hue else None,log_scale=log_scale,native_scale=native_scale,ax=ax)
                    st.pyplot(fig)
                    st.session_state['last_countplot'] = fig
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_countplot' in st.session_state:
            st.pyplot(st.session_state['last_countplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
