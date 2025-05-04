import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def show_scatterplot(dataset):
    st.title("Seaborn Scatterplot Customizer")
    # Create two tabs
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1],border=True)
        with col1:
            st.subheader("Plot Parameters")   
            # Basic parameters
            x_var = st.selectbox("X-axis variable",options=dataset.columns,index=0,help="Variable for the x-axis position of points") 
            y_var = st.selectbox("Y-axis variable",options=dataset.columns,index=1 if len(dataset.columns) > 1 else 0,help="Variable for the y-axis position of points")            
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable",options=dataset.columns,index=2 if len(dataset.columns) > 2 else 0,help="Variable that will produce points with different colors")                
                palette = st.text_input("Color palette",value="viridis",help="Method for choosing colors. Can be name of palette, list, or dict")
                hue_order = st.multiselect("Hue order",options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [],help="Specify order of processing for categorical levels")                
                hue_norm = st.text_input("Hue normalization",value="",help="Pair of values that set normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var,palette,hue_order,hue_norm = None,None,None,None
            # Size parameters
            use_size = st.checkbox("Use size grouping", False)
            if use_size:
                size_var = st.selectbox("Size variable",options=dataset.columns,index=3 if len(dataset.columns) > 3 else 0,help="Variable that will produce points with different sizes")
                sizes = st.text_input("Size range",value="10,100",help="Min and max size for points (e.g., '10,100')")
                sizes = tuple(map(int, sizes.split(','))) if sizes and ',' in sizes else (10, 100)
                size_order = st.multiselect("Size order",options=sorted(dataset[size_var].unique()) if use_size and size_var in dataset.columns else [],help="Specified order for appearance of size variable levels")                
                size_norm = st.text_input("Size normalization",value="",help="Normalization in data units for scaling (e.g., '0,1')")
                size_norm = tuple(map(float, size_norm.split(','))) if size_norm and ',' in size_norm else None
            else:
                size_var,sizes,size_order,size_norm = None,None,None,None        
            # Style parameters
            use_style = st.checkbox("Use style grouping", False)
            if use_style:
                style_var = st.selectbox("Style variable",options=dataset.columns,index=4 if len(dataset.columns) > 4 else 0,help="Variable that will produce points with different markers")               
                markers = st.checkbox("Use default markers",value=True,help="Whether to use default markers for different levels")                
                style_order = st.multiselect("Style order",options=sorted(dataset[style_var].unique()) if use_style and style_var in dataset.columns else [],help="Specified order for appearance of style variable levels")
            else:
                style_var,markers,style_order = None,True,None         
            # Legend and other parameters
            legend_type = st.selectbox("Legend type",options=["auto", "brief", "full", False],index=0,help="How to draw the legend. 'brief' shows sample values, 'full' shows all")          
            plot_button = st.button("Generate Plot",use_container_width=True,type='primary'),        
            with col2:
                if plot_button:
                    st.subheader("Generated Scatterplot")    
                    try:
                        # Create the plot
                        fig, ax = plt.subplots()
                        sns.scatterplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,size=size_var if use_size else None,style=style_var if use_style else None,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,sizes=sizes if use_size else None,size_order=size_order if use_size and size_order else None,size_norm=size_norm if use_size and size_norm else None,markers=markers if use_style else True,style_order=style_order if use_style and style_order else None,legend=legend_type,ax=ax)                    
                        st.pyplot(fig)        
                        # Store the plot in session state for the See Plots tab
                        st.session_state['last_plot'] = fig                 
                    except Exception as e:
                        st.error(f"Error generating plot: {str(e)}")  
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_plot' in st.session_state:
            st.pyplot(st.session_state['last_plot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")

def show_lineplot(dataset):
    st.title("Seaborn Lineplot Customizer")
    # Create two tabs
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")   
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Variable for the x-axis position") 
            y_var = st.selectbox("Y-axis variable", options=dataset.columns, index=1 if len(dataset.columns) > 1 else 0, help="Variable for the y-axis position")            
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable that will produce lines with different colors")                
                palette = st.text_input("Color palette", value="viridis", help="Method for choosing colors. Can be name of palette, list, or dict")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Specify order of processing for categorical levels")                
                hue_norm = st.text_input("Hue normalization", value="", help="Pair of values that set normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var, palette, hue_order, hue_norm = None, None, None, None
            # Size parameters
            use_size = st.checkbox("Use size grouping", False)
            if use_size:
                size_var = st.selectbox("Size variable", options=dataset.columns, index=3 if len(dataset.columns) > 3 else 0, help="Variable that will produce lines with different widths")
                sizes = st.text_input("Size range", value="1,5", help="Min and max line width (e.g., '1,5')")
                sizes = tuple(map(int, sizes.split(','))) if sizes and ',' in sizes else (1, 5)
                size_order = st.multiselect("Size order", options=sorted(dataset[size_var].unique()) if use_size and size_var in dataset.columns else [], help="Specified order for appearance of size variable levels")                
                size_norm = st.text_input("Size normalization", value="", help="Normalization in data units for scaling (e.g., '0,1')")
                size_norm = tuple(map(float, size_norm.split(','))) if size_norm and ',' in size_norm else None
            else:
                size_var, sizes, size_order, size_norm = None, None, None, None        
            # Style parameters
            use_style = st.checkbox("Use style grouping", False)
            if use_style:
                style_var = st.selectbox("Style variable", options=dataset.columns, index=4 if len(dataset.columns) > 4 else 0, help="Variable that will produce lines with different dashes/markers")               
                markers = st.checkbox("Use markers", value=True, help="Whether to show markers on the lines")                
                dashes = st.checkbox("Use dashed lines", value=True, help="Whether to use different dash styles for different levels")                
                style_order = st.multiselect("Style order", options=sorted(dataset[style_var].unique()) if use_style and style_var in dataset.columns else [], help="Specified order for appearance of style variable levels")
            else:
                style_var, markers, dashes, style_order = None, None, True, None         
            # Additional lineplot parameters
            units_var = st.selectbox("Units variable (optional)", options=[None] + list(dataset.columns), index=0, help="Grouping variable identifying sampling units (no legend entry)")
            estimator = st.selectbox("Aggregation method", options=['mean', 'median', 'sum', 'min', 'max', 'count', None], index=0, help="Method for aggregating multiple y values at same x level")
            errorbar = st.selectbox("Error bar method", options=['ci', 'pi', 'se', 'sd', None], index=0, help="Method for computing error bars (None to hide)")
            if errorbar in ['ci', 'pi']:
                errorbar_level = st.slider("Confidence interval level", 1, 99, 95, help="Confidence level for error bars (1-99)")
                errorbar = (errorbar, errorbar_level)
            n_boot = st.number_input("Number of bootstraps", min_value=1, value=1000, help="Number of bootstraps for confidence interval calculation")
            sort = st.checkbox("Sort lines", value=True, help="Sort data by x and y variables before plotting")
            err_style = st.radio("Error style", options=['band', 'bars'], index=0, help="Style for drawing confidence intervals")
            legend_type = st.selectbox("Legend type", options=["auto", "brief", "full", False], index=0, help="How to draw the legend")          
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary'),        
            with col2:
                if plot_button:
                    st.subheader("Generated Lineplot")    
                    try:
                        # Create the plot
                        fig, ax = plt.subplots()
                        sns.lineplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,size=size_var if use_size else None,style=style_var if use_style else None,units=units_var if units_var else None,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,sizes=sizes if use_size else None,size_order=size_order if use_size and size_order else None,size_norm=size_norm if use_size and size_norm else None,dashes=dashes if use_style else True,markers=markers if use_style else None,style_order=style_order if use_style and style_order else None,estimator=estimator,errorbar=errorbar,n_boot=n_boot,sort=sort,err_style=err_style,legend=legend_type,ax=ax)                    
                        st.pyplot(fig)        
                        # Store the plot in session state for the See Plots tab
                        st.session_state['last_lineplot'] = fig                 
                    except Exception as e:
                        st.error(f"Error generating plot: {str(e)}")  
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_lineplot' in st.session_state:
            st.pyplot(st.session_state['last_lineplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")

def show_relplot(dataset):
    st.title("Seaborn Relplot Customizer")
    # Create two tabs
    tab1, tab2 = st.tabs(["Implement Plots", "See Plots"])
    with tab1:
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("Plot Parameters")
            # Basic parameters
            x_var = st.selectbox("X-axis variable", options=dataset.columns, index=0, help="Variable for the x-axis position")
            y_var = st.selectbox("Y-axis variable", options=dataset.columns, index=1 if len(dataset.columns) > 1 else 0, help="Variable for the y-axis position")
            kind = st.radio("Plot kind", options=["scatter", "line"], index=0, help="Type of plot to draw (scatter or line)")
            # Hue parameters
            use_hue = st.checkbox("Use hue grouping", False)
            if use_hue:
                hue_var = st.selectbox("Hue variable", options=dataset.columns, index=2 if len(dataset.columns) > 2 else 0, help="Variable that will produce elements with different colors")
                palette = st.text_input("Color palette", value="viridis", help="Method for choosing colors. Can be name of palette, list, or dict")
                hue_order = st.multiselect("Hue order", options=sorted(dataset[hue_var].unique()) if use_hue and hue_var in dataset.columns else [], help="Specify order of processing for categorical levels")
                hue_norm = st.text_input("Hue normalization", value="", help="Pair of values that set normalization range (e.g., '0,100')")
                hue_norm = tuple(map(float, hue_norm.split(','))) if hue_norm and ',' in hue_norm else None
            else:
                hue_var, palette, hue_order, hue_norm = None, None, None, None
            # Size parameters
            use_size = st.checkbox("Use size grouping", False)
            if use_size:
                size_var = st.selectbox("Size variable", options=dataset.columns, index=3 if len(dataset.columns) > 3 else 0, help="Variable that will produce elements with different sizes")
                sizes = st.text_input("Size range", value="10,100" if kind == "scatter" else "1,5", help="Min and max size for elements (e.g., '10,100' for scatter, '1,5' for line)")
                default_sizes = (10, 100) if kind == "scatter" else (1, 5)
                sizes = tuple(map(int, sizes.split(','))) if sizes and ',' in sizes else default_sizes
                size_order = st.multiselect("Size order", options=sorted(dataset[size_var].unique()) if use_size and size_var in dataset.columns else [], help="Specified order for appearance of size variable levels")
                size_norm = st.text_input("Size normalization", value="", help="Normalization in data units for scaling (e.g., '0,1')")
                size_norm = tuple(map(float, size_norm.split(','))) if size_norm and ',' in size_norm else None
            else:
                size_var, sizes, size_order, size_norm = None, None, None, None
            # Style parameters
            use_style = st.checkbox("Use style grouping", False)
            if use_style:
                style_var = st.selectbox("Style variable", options=dataset.columns, index=4 if len(dataset.columns) > 4 else 0, help="Variable that will produce elements with different styles")
                markers = st.checkbox("Use markers", value=True, help="Whether to show markers on the elements")
                dashes = st.checkbox("Use dashed lines", value=True, help="Whether to use different dash styles for different levels (for line plots)")
                style_order = st.multiselect("Style order", options=sorted(dataset[style_var].unique()) if use_style and style_var in dataset.columns else [], help="Specified order for appearance of style variable levels")
            else:
                style_var, markers, dashes, style_order = None, None, True, None
            # Faceting parameters
            use_facets = st.checkbox("Use faceting", False)
            if use_facets:
                row_var = st.selectbox("Row faceting variable", options=[None] + list(dataset.columns), index=0, help="Variable to create row facets")
                col_var = st.selectbox("Column faceting variable", options=[None] + list(dataset.columns), index=0, help="Variable to create column facets")
                col_wrap = st.number_input("Columns per row", min_value=1, value=3, help="Wrap column facets at this width") if col_var else None
                row_order = st.multiselect("Row order", options=sorted(dataset[row_var].unique()), help="Order to organize the rows of the grid") if row_var else None
                col_order = st.multiselect("Column order", options=sorted(dataset[col_var].unique()), help="Order to organize the columns of the grid") if col_var else None
            else:
                row_var, col_var, col_wrap, row_order, col_order = None, None, None, None, None
            # Additional parameters
            units_var = st.selectbox("Units variable (optional)", options=[None] + list(dataset.columns), index=0, help="Grouping variable identifying sampling units (no legend entry)")
            height = st.number_input("Facet height (inches)", min_value=1.0, value=5.0, step=0.5, help="Height of each facet in inches")
            aspect = st.number_input("Facet aspect ratio", min_value=0.1, value=1.0, step=0.1, help="Aspect ratio of each facet (width = aspect * height)")
            legend_type = st.selectbox("Legend type", options=["auto", "brief", "full", False], index=0, help="How to draw the legend")
            plot_button = st.button("Generate Plot", use_container_width=True, type='primary')
            with col2:
                if plot_button:
                    st.subheader("Generated Relplot")
                    try:
                        g = sns.relplot(data=dataset,x=x_var,y=y_var,hue=hue_var if use_hue else None,size=size_var if use_size else None,style=style_var if use_style else None,units=units_var if units_var else None,row=row_var if use_facets and row_var else None,col=col_var if use_facets and col_var else None,col_wrap=col_wrap if use_facets and col_var and col_wrap else None,palette=palette if use_hue else None,hue_order=hue_order if use_hue and hue_order else None,hue_norm=hue_norm if use_hue and hue_norm else None,sizes=sizes if use_size else None,size_order=size_order if use_size and size_order else None,size_norm=size_norm if use_size and size_norm else None,markers=markers if use_style else None,dashes=dashes if use_style and kind == "line" else None,style_order=style_order if use_style and style_order else None,kind=kind,height=height,aspect=aspect,legend=legend_type)
                        st.pyplot(g.fig)
                        st.session_state['last_relplot'] = g.fig
                    except Exception as e:
                        st.error(f"Error generating plot: {str(e)}")
    with tab2:
        st.subheader("Previously Generated Plot")
        if 'last_relplot' in st.session_state:
            st.pyplot(st.session_state['last_relplot'])
        else:
            st.info("No plot generated yet. Please create a plot in the 'Implement Plots' tab.")
