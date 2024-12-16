import streamlit as st
import math
from scipy import stats

def calculate_margin_of_error(population, samples, proportion, confidence_level):
    """
    Calculate the margin of error for a given population and sample.
    
    Parameters:
    - population: Total population size
    - samples: Number of samples
    - proportion: Expected proportion (p)
    - confidence_level: Desired confidence level (e.g., 95)
    
    Returns:
    Margin of error
    """
    # Calculate z-score based on confidence level
    z_score = stats.norm.ppf((1 + confidence_level/100) / 2)
    
    # Calculate standard error
    p = proportion
    n = samples
    
    # Finite population correction factor
    finite_population_correction = math.sqrt((population - n) / (population - 1))
    
    # Margin of error calculation
    margin_of_error = z_score * math.sqrt((p * (1-p)) / n) * finite_population_correction
    
    return margin_of_error

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Margin of Error Calculator", 
        page_icon="📊", 
        layout="wide"
    )
    
    # Sidebar for additional information
    with st.sidebar:
        st.header("📚 About This App")
        st.markdown("""
        ### Margin of Error Calculator
        A tool to help you understand statistical sampling precision.
        
        ### Project Links
        - [GitHub Repository](https://github.com/Resident-Eve/margin-of-error-calculator)
        - [Report an Issue](https://github.com/Resident-Eve/margin-of-error-calculator/issues)
        
        ### How to Use
        1. Enter your population size
        2. Input number of samples
        3. Adjust proportion and confidence level
        4. Click "Calculate" to see the margin of error
        
        ### Want to Contribute?
        Star the repo, open issues, or submit pull requests!
        """)
        
        # Add a contact or feedback section
        st.divider()
        st.subheader("📬 Feedback")
        contact_form = st.form(key="contact_form")
        name = contact_form.text_input("Your Name")
        email = contact_form.text_input("Your Email")
        message = contact_form.text_area("Your Feedback")
        submit_button = contact_form.form_submit_button("Send Feedback")
        
        if submit_button:
            # Note: In a real app, you'd implement actual email/feedback submission
            st.success("Thank you for your feedback! We'll review it soon.")
    
    # Main content
    st.title("📊 Margin of Error Calculator")
    st.markdown("""
    This tool helps you calculate the margin of error for a survey or sample.
    
    ### What is Margin of Error?
    The margin of error tells you how much you can expect your survey results to differ 
    from the true population value. It helps quantify the precision of your sample.
    """)
    
    # Input columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Population input with help
        population = st.number_input(
            "Total Population Size", 
            min_value=1, 
            value=1000, 
            help="The total number of people or items in the group you're studying. "
                 "For example, total number of users in a platform."
        )
        
        # Confidence level input with help
        confidence_level = st.select_slider(
            "Confidence Level", 
            options=[90, 95, 99], 
            value=95,
            help="How confident you want to be in your results. "
                 "95% is most commonly used, meaning you're 95% sure the true value "
                 "falls within the margin of error."
        )
    
    with col2:
        # Available samples input with help
        samples = st.number_input(
            "Number of Samples", 
            min_value=1, 
            value=100, 
            help="The number of surveys or responses you've collected. "
                 "Larger sample sizes reduce the margin of error."
        )
        
        # Proportion input with help
        proportion = st.slider(
            "Sample Proportion", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.5,
            step=0.01,
            help="Expected proportion of the population with the characteristic "
                 "you're measuring. 0.5 is most conservative (maximizes uncertainty)."
        )
    
    # Calculate button
    if st.button("Calculate Margin of Error", type="primary"):
        # Validate inputs
        if samples > population:
            st.error("Number of samples cannot be larger than population size!")
        else:
            # Calculate margin of error
            margin = calculate_margin_of_error(population, samples, proportion, confidence_level)
            
            # Display results
            st.success(f"📏 Margin of Error: ±{margin:.4f} or {margin*100:.2f}%")
            
            # Detailed explanation
            st.markdown("""
            ### What does this mean?
            - If your survey shows 50% of users like a feature, 
              the true percentage in the entire population 
              is likely between {lower} and {upper}.
            - A smaller margin of error means more precise results.
            """.format(
                lower=f"{50-margin*100:.2f}%", 
                upper=f"{50+margin*100:.2f}%"
            ))
    
    # Additional information section
    st.markdown("""
    ### Tips for Improving Margin of Error
    - Increase sample size
    - Ensure representative sampling
    - Use appropriate confidence levels
    """)

if __name__ == "__main__":
    main()